"""NLU: map symptoms to specialty IDs from a fixed catalog (IDs must match DB/Qdrant)."""

from __future__ import annotations

import json
import logging
from typing import Any

from openai import AsyncOpenAI

from medicalink_ai.config import Settings
from medicalink_ai.gemini_llm import generate_json_with_gemini

logger = logging.getLogger(__name__)

SYSTEM = """You are a medical natural language parser. Your task is to extract medical symptoms and keywords from the patient's Vietnamese description.
Return a single JSON object with this exact structure:
{"symptoms":["triệu chứng 1","triệu chứng 2",...], "note":"1–2 short friendly Vietnamese sentences for the patient"}
- Do NOT invent symptoms that are not explicitly or implicitly mentioned.
- Keep symptoms concise (1-3 words usually).
"""


async def suggest_specialties_from_catalog(
    *,
    symptoms: str,
    catalog: list[dict[str, Any]],
    settings: Settings,
    openai: AsyncOpenAI,
) -> dict[str, Any]:
    if not catalog:
        return {"specialty_ids": [], "note": "No specialties in catalog."}

    user_msg = f"Patient description:\n{symptoms.strip()}"

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
        return {
            "specialty_ids": [],
            "note": "Could not classify automatically; please select specialties yourself.",
        }

    extracted_symptoms = parsed.get("symptoms", [])
    if not isinstance(extracted_symptoms, list):
        extracted_symptoms = []
    extracted_symptoms = [str(x).lower().strip() for x in extracted_symptoms if str(x).strip()]

    note = str(parsed.get("note") or "").strip()
    if not note:
        note = "Dưới đây là các bác sĩ phù hợp với triệu chứng của bạn."

    # System Router: Keyword Match
    scores: list[tuple[str, int]] = []
    
    for spec in catalog:
        sid = str(spec.get("id", "")).strip()
        if not sid:
            continue
            
        score = 0
        search_corpus = [str(spec.get("name", "")).lower()]
        for arr_key in ["aliases", "common_symptoms", "keywords"]:
            arr = spec.get(arr_key)
            if isinstance(arr, list):
                search_corpus.extend([str(x).lower() for x in arr])
                
        # Count matches
        for sym in extracted_symptoms:
            for corpus_item in search_corpus:
                if sym in corpus_item or corpus_item in sym:
                    score += 1
                    
        if score > 0:
            scores.append((sid, score))
            
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    out_ids = [x[0] for x in scores[:4]]

    if not out_ids:
        note = "Không tìm thấy chuyên khoa khớp chính xác, gợi ý bác sĩ tổng quát hoặc bạn tự chọn chuyên khoa."

    return {
        "specialty_ids": out_ids, 
        "note": note,
        "extracted_symptoms": extracted_symptoms
    }
