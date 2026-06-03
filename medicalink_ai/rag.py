from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any, cast

from openai import AsyncOpenAI

from medicalink_ai.config import Settings
from medicalink_ai.eval_log import StepTimer, append_rag_eval, build_eval_record
from medicalink_ai.gemini_llm import generate_json_with_gemini
from medicalink_ai.rerank import RerankMode, rerank_pipeline
from medicalink_ai.semantic_cache import SemanticCacheService
from medicalink_ai.vector_store import DoctorVectorStore

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """Bạn là trợ lý y tế chỉ được trả lời dựa trên danh sách bác sĩ được cấp (ngữ cảnh).
Nhiệm vụ: gợi ý các bác sĩ phù hợp nhất với mô tả triệu chứng của bệnh nhân.
Quy tắc:
- Chỉ chọn bác sĩ có trong ngữ cảnh; không bịa bác sĩ hoặc chuyên khoa.
- Mỗi bác sĩ phải dùng đúng doctor_id từ ngữ cảnh (UUID chuỗi).
- Trả về JSON duy nhất với cấu trúc:
{"recommendations":[{"doctor_id":"...","reason":"... ngắn gọn tiếng Việt..."}]}
- reason tối đa 2 câu, thân thiện, không chẩn đoán chắc chắn thay bác sĩ.
"""


@dataclass(slots=True, kw_only=True)
class DoctorRagService:
    store: DoctorVectorStore
    openai: AsyncOpenAI
    settings: Settings
    semantic_cache: SemanticCacheService | None = None

    async def recommend(
        self,
        symptoms: str,
        top_k: int,
        *,
        specialty_ids: list[str] | None = None,
        extracted_symptoms: list[str] | None = None,
        cqu_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        timer = StepTimer()
        
        if cqu_data is None:
            cqu_data = {}
        
        # 1. Semantic Cache check
        if self.settings.semantic_cache_enabled and self.semantic_cache:
            cached_result = await self.semantic_cache.get_cache(symptoms)
            if cached_result:
                cached_result["_cached"] = True
                
                # We still append to eval log for metrics (with 0 latency)
                append_rag_eval(
                    self.settings.rag_eval_log_path,
                    build_eval_record(
                        query=symptoms,
                        top_k=top_k,
                        retrieved_ids=[],
                        recommended_ids=[r.get("doctor_id") for r in cached_result.get("recommendations", [])],
                        hybrid_used=False,
                        legacy_collection=False,
                        rerank_mode="cached",
                        latency_ms=timer.elapsed_ms(),
                        extra={"cache_hit": True},
                    ),
                )
                return cached_result

        top_k = max(1, min(top_k, 15))
        retrieve_limit = min(max(top_k * 6, 30), 80)
        prov = (self.settings.llm_provider or "openai").strip().lower()
        spec_filter = specialty_ids or None

        # Determine the query string for vector search
        search_query = symptoms
        if extracted_symptoms:
            search_query = "Triệu chứng: " + ", ".join(extracted_symptoms)
            logger.info("Using compressed symptoms for search: %s", search_query)

        import asyncio
        candidates = []
        hybrid_used = False
        legacy_col = False
        
        if spec_filter and len(spec_filter) > 0:
            per_spec_limit = max(10, retrieve_limit // len(spec_filter) + 5)
            results = []
            for sp_id in spec_filter:
                try:
                    cands, _, _ = await self.store.search_active(
                        search_query,
                        limit=per_spec_limit,
                        filter_specialty_ids=[sp_id]
                    )
                    results.append((cands, False, False))
                except Exception as e:
                    logger.warning(f"Error searching specialty {sp_id}: {e}")
                    results.append(([], False, False))
            
            seen_docs = set()
            for i, (cands, is_hybrid, is_legacy) in enumerate(results):
                hybrid_used = hybrid_used or is_hybrid
                legacy_col = legacy_col or is_legacy
                
                for c in cands:
                    doc_id = c.get("doctor_id")
                    if doc_id not in seen_docs:
                        seen_docs.add(doc_id)
                        c["intent_rank"] = i
                        candidates.append(c)
                        
            candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
            candidates = candidates[:retrieve_limit]
        else:
            candidates, hybrid_used, legacy_col = await self.store.search_active(
                search_query,
                limit=retrieve_limit,
                filter_specialty_ids=spec_filter,
            )
        if not candidates:
            out = {
                "recommendations": [],
                "message": "Chưa có hồ sơ bác sĩ để gợi ý. Hãy chạy đồng bộ knowledge base hoặc kiểm tra Qdrant.",
            }
            append_rag_eval(
                self.settings.rag_eval_log_path,
                build_eval_record(
                    query=symptoms,
                    top_k=top_k,
                    retrieved_ids=[],
                    recommended_ids=[],
                    hybrid_used=hybrid_used,
                    legacy_collection=legacy_col,
                    rerank_mode=str(self.settings.rag_rerank_mode),
                    latency_ms=timer.elapsed_ms(),
                    extra={"empty": True},
                ),
            )
            return out

        mode_raw = (self.settings.rag_rerank_mode or "lexical").strip().lower()
        if mode_raw not in ("none", "lexical", "flashrank"):
            mode_raw = "lexical"
        rmode = cast(RerankMode, mode_raw)

        ranked = rerank_pipeline(
            symptoms,
            candidates,
            mode=rmode,
            lexical_weight=float(self.settings.rag_rerank_lexical_weight),
            flashrank_model=self.settings.flashrank_model,
            flashrank_cache_dir=self.settings.flashrank_cache_dir or None,
            flashrank_pool=int(self.settings.rag_rerank_pool),
            cqu_data=cqu_data,
            settings=self.settings,
        )

        ctx_max = max(5, int(self.settings.retrieval_llm_context_max))
        for_llm = ranked[:ctx_max]

        ctx_lines = []
        for c in for_llm:
            ctx_lines.append(
                json.dumps(
                    {
                        "doctor_id": c.get("doctor_id"),
                        "full_name": c.get("full_name"),
                        "specialties": c.get("specialties_label"),
                        "experience_years": c.get("experience_years"),
                        "education": c.get("education"),
                        "procedures": c.get("procedures"),
                        "score": c.get("score"),
                    },
                    ensure_ascii=False,
                )
            )
        context_block = "\n".join(ctx_lines)

        user_msg = f"Triệu chứng / mô tả của bệnh nhân:\n{symptoms}\n\nNgữ cảnh bác sĩ:\n{context_block}\n\nChọn tối đa {top_k} bác sĩ phù hợp nhất dựa trên chuyên môn, kinh nghiệm, đào tạo, và dịch vụ thủ thuật họ cung cấp. Hãy đưa ra lý do khách quan."

        temp = float(self.settings.rag_llm_temperature)
        if prov == "gemini":
            raw = await generate_json_with_gemini(
                api_key=self.settings.google_genai_api_key.strip(),
                model=self.settings.google_genai_model.strip(),
                system_instruction=SYSTEM_PROMPT,
                user_content=user_msg,
                timeout_ms=max(5_000, int(self.settings.google_genai_timeout_ms)),
                temperature=temp,
            )
        else:
            completion = await self.openai.chat.completions.create(
                model=self.settings.openai_chat_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                response_format={"type": "json_object"},
                temperature=temp,
            )
            raw = completion.choices[0].message.content or "{}"
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("LLM JSON parse failed, fallback regex")
            parsed = _fallback_parse(raw, for_llm, top_k)

        recs = parsed.get("recommendations") if isinstance(parsed, dict) else None
        if not isinstance(recs, list):
            recs = []

        allowed = {str(c["doctor_id"]) for c in for_llm if c.get("doctor_id")}
        cleaned: list[dict[str, str]] = []
        for r in recs[:top_k]:
            if not isinstance(r, dict):
                continue
            did = str(r.get("doctor_id") or "")
            if did not in allowed:
                continue
            reason = str(r.get("reason") or "").strip()
            cleaned.append({"doctor_id": did, "reason": reason})

        if len(cleaned) < top_k:
            cleaned = _fill_from_candidates(cleaned, for_llm, top_k)

        rec_ids = [x["doctor_id"] for x in cleaned[:top_k]]
        ret_ids = [
            str(c.get("doctor_id")) for c in ranked if c.get("doctor_id")
        ]

        append_rag_eval(
            self.settings.rag_eval_log_path,
            build_eval_record(
                query=symptoms,
                top_k=top_k,
                retrieved_ids=ret_ids[:60],
                recommended_ids=rec_ids,
                hybrid_used=hybrid_used,
                legacy_collection=legacy_col,
                rerank_mode=mode_raw,
                latency_ms=timer.elapsed_ms(),
                extra={
                    "retrieve_n": len(candidates),
                    "after_rerank_n": len(ranked),
                    "llm_context_n": len(for_llm),
                    "llm_provider": prov,
                },
            ),
        )

        final_result = {"recommendations": cleaned[:top_k]}
        
        # Save to Semantic Cache
        if self.settings.semantic_cache_enabled and self.semantic_cache:
            await self.semantic_cache.set_cache(symptoms, final_result)

        return final_result


def _fallback_parse(
    raw: str,
    candidates: list[dict[str, Any]],
    top_k: int,
) -> dict[str, Any]:
    out: list[dict[str, str]] = []
    for m in re.finditer(
        r'"doctor_id"\s*:\s*"([^"]+)"\s*,\s*"reason"\s*:\s*"([^"]*)"',
        raw,
    ):
        out.append({"doctor_id": m.group(1), "reason": m.group(2)})
        if len(out) >= top_k:
            break
    return {"recommendations": out}


def _fill_from_candidates(
    existing: list[dict[str, str]],
    candidates: list[dict[str, Any]],
    top_k: int,
) -> list[dict[str, str]]:
    have = {x["doctor_id"] for x in existing}
    for c in candidates:
        if len(existing) >= top_k:
            break
        did = str(c.get("doctor_id") or "")
        if not did or did in have:
            continue
        have.add(did)
        existing.append(
            {
                "doctor_id": did,
                "reason": "Gợi ý dựa trên độ tương đồng kỹ thuật với mô tả của bạn (không thay cho tư vấn y khoa).",
            }
        )
    return existing
