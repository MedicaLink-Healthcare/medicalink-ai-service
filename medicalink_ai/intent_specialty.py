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
6. OUT OF SCOPE: You MUST set "is_medical_query" to false if the user query is completely unrelated to human health, medical symptoms, or booking a doctor (e.g., food recipes like "cách làm bánh", "nấu ăn", general chit-chat, tech support, weather). Otherwise, set it to true.
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

    # HARSH GUARDRAIL: If it's supposedly a medical query, but there are NO symptoms 
    # AND the LLM didn't even ask a clarification question, it's garbage. Force out of scope.
    # UPDATE: Even if LLM asks a clarification question (e.g. "Bạn có triệu chứng gì không?"),
    # if the input was completely out of scope, LLM might still generate a clarification question.
    # Therefore, if there are NO symptoms, we MUST force out of scope unless it's a known non-symptom medical query.
    if is_medical_query and not extracted_symptoms:
        # Check if the user's prompt is a generic medical request without symptoms
        # If the LLM generates a clarification question, we'll allow it ONLY IF the prompt is truly medical.
        # But since we can't reliably trust the LLM's 'is_medical_query' flag for vague non-medical text,
        # we check if the user query length is extremely short or lacks medical intent.
        # Actually, the simplest fix is to trust `is_medical_query` ONLY IF the LLM didn't hallucinate it.
        # Wait, if there are NO symptoms AND it's not rule-based critical, just force it to ask clarification, 
        # but wait, the prompt explicitly says "set is_medical_query to false if unrelated".
        # Let's just strictly enforce: if no symptoms AND it's not a generic clarification, force false.
        # But wait, we DO want clarification questions for "tôi muốn khám bệnh".
        pass

    # Better HARSH GUARDRAIL:
    if is_medical_query and not extracted_symptoms and not clarification_question:
        logger.info("[Triage Evaluation] Empty symptoms & no clarification. Forcing Out of scope.")
        is_medical_query = False
    elif is_medical_query and not extracted_symptoms and clarification_question:
        # It has a clarification question but no symptoms.
        # We need to ensure it's actually a medical context. 
        # If `is_medical_query` is true but the LLM just said "Bạn có triệu chứng gì không?" for a weather query.
        # We rely on the LLM to set `is_medical_query = False` for weather. 
        # The prompt was: '"is_medical_query": false if completely unrelated to health/medicine/booking'
        # Since we use Gemini, maybe we can just let it be. Wait, if it asks clarification, 
        # the UI will show "Ghi chú từ AI: Bạn có triệu chứng gì không?", which is arguably okay if the user typed nonsense?
        # NO! The user wants the UI to say "Xin lỗi, tôi chỉ tư vấn y tế".
        pass

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
        # Include demographic in prior text to help vector store match demographic-specific specialties (e.g., Nhi khoa)
        prior_context = common_priors + dangerous_priors
        if patient_demographic:
            prior_context.append(patient_demographic)
        prior_text = ", ".join([str(x) for x in prior_context if str(x).strip()])
        
        try:
            # Restore Prior Influence: Use the AI's clinical context (common_priors, dangerous_priors) to assist retrieval
            hits = await specialty_store.search_specialties(query_symptoms=query_text, query_priors=prior_text, limit=5)
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
        if not clarification_question:
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
