"""NLU: map symptoms to specialty IDs from a fixed catalog with Clinical Intelligence (Phase 2)."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from openai import AsyncOpenAI

from medicalink_ai.config import Settings
from medicalink_ai.gemini_llm import generate_json_with_gemini
from medicalink_ai.vector_store_specialty import SpecialtyVectorStore

logger = logging.getLogger(__name__)

# Phase 2: Rule-based Emergency Detector (Deterministic)
RED_FLAGS = [
    r"đau ngực dữ dội", r"khó thở nặng", r"khó thở cấp", r"liệt nửa người", 
    r"mất ý thức", r"chảy máu nhiều", r"đột quỵ", r"ngất xỉu", r"đau tim", 
    r"co giật", r"nhồi máu", r"tai biến", r"không thở được", r"hôn mê", 
    r"đau thắt ngực", r"xuất huyết", r"vã mồ hôi lạnh", r"tức ngực dữ dội"
]
RED_FLAG_PATTERN = re.compile("|".join(RED_FLAGS), re.IGNORECASE)


SYSTEM = """You are a medical natural language parser. Your task is to extract medical symptoms, evaluate triage acuity, and act as a Clinical Prior Engine to support semantic routing.
Return a single JSON object with this exact structure:
{
  "symptoms": ["triệu chứng 1", "triệu chứng 2", ...],
  "negated_symptoms": ["triệu chứng phủ định 1", "triệu chứng phủ định 2", ...],
  "severity": "low" | "medium" | "high",
  "duration": "string (e.g. '2 tháng', 'vài ngày', or empty)",
  "patient_demographic": "string (e.g. 'bé 5 tuổi', 'nam 60 tuổi', or empty)",
  "common_priors": ["bệnh phổ biến 1", "bệnh phổ biến 2"],
  "dangerous_priors": ["bệnh nguy hiểm 1"],
  "clarification_question": "string (only if symptoms are too vague, otherwise empty)",
  "note": "1–2 short friendly Vietnamese sentences for the patient",
  "triage_level": "routine" | "urgent" | "critical",
  "urgency_score": float (0.0 to 1.0),
  "emergency_reason": "string (only if critical or urgent, otherwise empty)",
  "is_medical_query": boolean
}

CRITICAL RULES:
1. CLINICAL QUERY UNDERSTANDING:
   - `symptoms`: Positive symptoms only (e.g. "ho", "sốt").
   - `negated_symptoms`: Symptoms the patient explicitly denies (e.g. "không ho", "không đau ngực").
   - `duration`: Extract the duration of the symptoms if mentioned.
   - `patient_demographic`: Extract age, gender, or patient type (e.g. "bé nhà tôi", "trẻ em") if mentioned.
2. CLINICAL PRIORS: 
   - `common_priors`: List 1-2 most statistically probable common conditions for these symptoms (e.g., "trào ngược dạ dày", "viêm họng").
   - `dangerous_priors`: List 1 worst-case life-threatening condition to rule out (e.g., "ung thư phổi").
   - Consider `patient_demographic` when generating priors.
3. CLARIFICATION: If symptoms are too vague (e.g., "đau bụng", "mệt"), generate a short `clarification_question` to ask the patient for more details.
4. TRIAGE LEVEL:
   - "routine": Normal symptoms.
   - "urgent": Needs prompt attention.
   - "critical": LIFE-THREATENING emergency (đau ngực, đột quỵ, khó thở cấp).
5. Keep symptoms concise (1-3 words). Do NOT invent symptoms.
6. OUT OF SCOPE: If the user query is clearly not related to health, symptoms, or booking a doctor (e.g. "cách nấu cơm", "thời tiết"), set "is_medical_query" to false. Otherwise, true.
"""

def detect_rule_based_emergency(text: str) -> bool:
    if RED_FLAG_PATTERN.search(text):
        return True
    return False

async def suggest_specialties_from_catalog(
    *,
    symptoms: str,
    catalog: list[dict[str, Any]],
    settings: Settings,
    openai: AsyncOpenAI,
    specialty_store: SpecialtyVectorStore | None = None,
) -> dict[str, Any]:
    if not catalog:
        return {"specialty_ids": [], "note": "No specialties in catalog."}

    user_msg = f"Patient description:\n{symptoms.strip()}"
    
    # 1. Rule-based Emergency Detection (Deterministic)
    rule_based_critical = detect_rule_based_emergency(symptoms)

    prov = (settings.llm_provider or "openai").strip().lower()
    temp = 0.0 # Force deterministic extraction
    try:
        if prov == "gemini":
            raw = await generate_json_with_gemini(
                api_key=settings.google_genai_api_key.strip(),
                model=settings.google_genai_model.strip(),
                system_instruction=SYSTEM,
                user_content=user_msg,
                timeout_ms=max(5_000, int(settings.google_genai_timeout_ms)),
                temperature=temp,
            )
        else:
            completion = await openai.chat.completions.create(
                model=settings.openai_chat_model,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user_msg},
                ],
                response_format={"type": "json_object"},
                temperature=temp,
            )
            raw = completion.choices[0].message.content or "{}"
        parsed = json.loads(raw)
    except Exception as e:
        logger.warning("Symptom extraction failed: %s", e)
        parsed = {}

    is_medical_query = bool(parsed.get("is_medical_query", True))
    if not is_medical_query:
        logger.info("[Triage Evaluation] Out of scope query detected. Rejecting.")
        return {
            "specialty_ids": [],
            "note": "Hệ thống MedicaLink chỉ hỗ trợ tư vấn và gợi ý bác sĩ chuyên khoa. Xin vui lòng đặt các câu hỏi liên quan đến sức khỏe và triệu chứng bệnh.",
            "extracted_symptoms": [],
            "negated_symptoms": [],
            "patient_demographic": "",
            "symptom_duration": "",
            "severity": "low",
            "common_priors": [],
            "dangerous_priors": [],
            "clarification_question": "",
            "triage_level": "routine",
            "urgency_score": 0.0,
            "is_emergency": False,
            "emergency_reason": "",
            "routing_confidence": 0.0,
            "is_fallback": True,
            "fallback_reason": "out_of_scope",
        }

    extracted_symptoms = parsed.get("symptoms", [])
    if not isinstance(extracted_symptoms, list):
        extracted_symptoms = []
    extracted_symptoms = [str(x).lower().strip() for x in extracted_symptoms if str(x).strip()]

    negated_symptoms = parsed.get("negated_symptoms", [])
    if not isinstance(negated_symptoms, list):
        negated_symptoms = []
    negated_symptoms = [str(x).lower().strip() for x in negated_symptoms if str(x).strip()]

    patient_demographic = str(parsed.get("patient_demographic") or "").strip()
    symptom_duration = str(parsed.get("duration") or "").strip()
    severity = str(parsed.get("severity") or "low").strip()

    common_priors = parsed.get("common_priors", [])
    if not isinstance(common_priors, list): common_priors = []
    
    dangerous_priors = parsed.get("dangerous_priors", [])
    if not isinstance(dangerous_priors, list): dangerous_priors = []
    
    clarification_question = str(parsed.get("clarification_question") or "").strip()

    llm_triage_level = str(parsed.get("triage_level") or "routine").lower()
    urgency_score = float(parsed.get("urgency_score") or 0.1)
    
    # 2. Logic Fusion (Rule-based OR LLM)
    is_critical = rule_based_critical or (llm_triage_level == "critical")
    final_triage_level = "critical" if is_critical else llm_triage_level
    
    if is_critical and urgency_score < 0.8:
        urgency_score = 0.95 # Force high score if rule-based caught it

    note = str(parsed.get("note") or "").strip()
    if not note:
        note = "Dưới đây là các gợi ý phù hợp với triệu chứng của bạn."

    emergency_reason = str(parsed.get("emergency_reason") or "").strip()
    if is_critical and not emergency_reason:
        emergency_reason = "Cảnh báo khẩn cấp: Triệu chứng của bạn có dấu hiệu nguy hiểm. Vui lòng đến ngay phòng khám Cấp cứu hoặc gọi xe cấp cứu gần nhất."

    # Observability Logging
    logger.info(
        "[Triage Evaluation] rule_based_critical=%s | llm_triage=%s | final_triage=%s | urgency=%.2f",
        rule_based_critical, llm_triage_level, final_triage_level, urgency_score
    )

    out_ids = []
    confidence = 0.0
    is_fallback = False
    fallback_reason = ""

    # 3. Semantic Vector Routing (Hybrid)
    if specialty_store and extracted_symptoms:
        query_text = ", ".join(extracted_symptoms)
        prior_text = ", ".join([str(x) for x in common_priors + dangerous_priors if str(x).strip()])
        
        try:
            # 0% Prior Influence: Completely rely on pure Symptom embedding for Retrieval (RAG-centric)
            hits = await specialty_store.search_specialties(query_symptoms=query_text, query_priors="", limit=5)
            if hits:
                confidence = hits[0].get("confidence_score", 0.0)
                
                # Filter hits to prevent returning irrelevant specialties
                # Keep a hit if its score is within 30% of the top score, or it has a good score (> 0.60)
                valid_hits = []
                for h in hits:
                    score = h.get("confidence_score", 0.0)
                    if score >= confidence * 0.70 or score > 0.60:
                        valid_hits.append(h)
                    if len(valid_hits) >= 3:
                        break
                
                out_ids = [hit["id"] for hit in valid_hits if hit.get("id")]
                
                # 4. Confidence Calibration & Fallback
                if confidence < 0.35:
                    is_fallback = True
                    fallback_reason = "low_confidence"
                    
                    # Add Bác sĩ gia đình / Nội tổng quát to top of out_ids
                    gp_names = ["bác sĩ gia đình", "nội tổng quát"]
                    gp_ids = []
                    for c in catalog:
                        name_lower = str(c.get("name") or "").strip().lower()
                        if any(p in name_lower for p in gp_names):
                            gp_ids.append(c["id"])
                            
                    # Deduplicate and insert at top
                    for gid in reversed(gp_ids):
                        if gid in out_ids:
                            out_ids.remove(gid)
                        out_ids.insert(0, gid)
                        
                    logger.info("[Confidence Calibration] Confidence %.2f < 0.35. Triggered fallback to GP.", confidence)
                    
        except Exception as e:
            logger.error("Semantic search failed, fallback to none: %s", e)

    # 4.5 Demographic & Domain Rule-based Overrides (Fixing Semantic Shortcomings)
    demo_lower = patient_demographic.lower()
    query_lower = symptoms.lower()
    
    nhi_khoa_id = next((c["id"] for c in catalog if "nhi" in c.get("name", "").lower()), None)
    san_phu_khoa_id = next((c["id"] for c in catalog if "sản" in c.get("name", "").lower() or "phụ khoa" in c.get("name", "").lower()), None)
    noi_tong_quat_id = next((c["id"] for c in catalog if "tổng quát" in c.get("name", "").lower() or "gia đình" in c.get("name", "").lower()), None)
    
    # Rule 1: Nhi khoa (Pediatrics) - Triggered by demographic or strong keywords
    child_words = ["trẻ", "bé", "con tôi", "cháu", "sơ sinh"]
    if nhi_khoa_id and any(w in demo_lower for w in child_words) or any(f" {w} " in f" {query_lower} " for w in child_words):
        if nhi_khoa_id in out_ids:
            out_ids.remove(nhi_khoa_id)
        out_ids.insert(0, nhi_khoa_id)
        logger.info("[Rule Override] Forced Nhi Khoa (Pediatrics) based on demographic keywords.")
        
    # Rule 2: Sản phụ khoa (Obstetrics & Gynecology)
    obgyn_words = ["kinh nguyệt", "mang thai", "vùng kín", "âm đạo", "tử cung", "trễ kinh", "có thai", "buồng trứng", "huyết trắng", "khí hư", "que 2 vạch", "phụ khoa"]
    if san_phu_khoa_id and any(w in query_lower for w in obgyn_words):
        if san_phu_khoa_id in out_ids:
            out_ids.remove(san_phu_khoa_id)
        out_ids.insert(0, san_phu_khoa_id)
        logger.info("[Rule Override] Forced Sản phụ khoa based on domain-specific keywords.")



    # 5. Emergency Override Layer Enhancement
    if is_critical:
        # We don't bypass semantic routing anymore, but we ensure priority critical specialties are present
        note = emergency_reason
        priority_names = ["cấp cứu"] # Removed hardcoded "thần kinh", "tim mạch" as semantic routing handles them better
        priority_ids = []
        for c in catalog:
            name_lower = str(c.get("name") or "").strip().lower()
            if any(p in name_lower for p in priority_names):
                priority_ids.append(c["id"])
        
        # Add to top without replacing
        for pid in reversed(priority_ids):
            if pid in out_ids:
                out_ids.remove(pid)
            out_ids.insert(0, pid)

    if not out_ids:
        note = "Không tìm thấy chuyên khoa khớp chính xác, gợi ý bác sĩ tổng quát hoặc bạn tự chọn chuyên khoa."
        gp_names = ["bác sĩ gia đình", "nội tổng quát"]
        for c in catalog:
            name_lower = str(c.get("name") or "").strip().lower()
            if any(p in name_lower for p in gp_names):
                out_ids.append(c["id"])
    # Production Observability Event (JSON for ELK/Grafana)
    logger.info(
        "metrics_event: %s",
        json.dumps({
            "event": "clinical_triage",
            "urgency_score": urgency_score,
            "is_emergency": is_critical,
            "is_fallback": is_fallback,
            "fallback_reason": fallback_reason,
            "routing_confidence": confidence,
            "triage_level": final_triage_level,
            "severity": severity,
            "symptoms_count": len(extracted_symptoms)
        })
    )

    return {
        "specialty_ids": out_ids, 
        "note": note,
        "extracted_symptoms": extracted_symptoms,
        "negated_symptoms": negated_symptoms,
        "patient_demographic": patient_demographic,
        "symptom_duration": symptom_duration,
        "severity": severity,
        "common_priors": common_priors,
        "dangerous_priors": dangerous_priors,
        "clarification_question": clarification_question,
        "triage_level": final_triage_level,
        "urgency_score": urgency_score,
        "is_emergency": is_critical,
        "emergency_reason": emergency_reason,
        "routing_confidence": confidence,
        "is_fallback": is_fallback,
        "fallback_reason": fallback_reason,
    }
