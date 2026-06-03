"""Re-ranking nhẹ sau retrieval: FlashRank (cross-encoder nhẹ) hoặc tăng điểm lexical."""

from __future__ import annotations

import logging
import re
import unicodedata
from functools import lru_cache
from typing import Any, Literal

logger = logging.getLogger(__name__)

RerankMode = Literal["none", "lexical", "flashrank"]


def _normalize(text: str) -> str:
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t


def _tokens(text: str) -> set[str]:
    t = _normalize(text)
    return {x for x in re.split(r"[^\w]+", t) if len(x) >= 2}


def lexical_bonus(query: str, candidate: dict[str, Any]) -> float:
    """Điểm 0..1: overlap token giữa query và tên + chuyên khoa + snippet JSON."""
    qset = _tokens(query)
    if not qset:
        return 0.0
    blob = " ".join(
        str(candidate.get(k) or "")
        for k in ("full_name", "specialties_label", "source_json")
    )
    cset = _tokens(blob)
    if not cset:
        return 0.0
    inter = len(qset & cset)
    return min(1.0, inter / max(3.0, len(qset) * 0.5))


def blend_scores(
    query: str,
    candidates: list[dict[str, Any]],
    lexical_weight: float,
    cqu_data: dict[str, Any] | None = None,
    settings: Any = None,
) -> list[dict[str, Any]]:
    if not candidates:
        return candidates
        
    cqu = cqu_data or {}
    
    # 1. Base vector score normalization
    scores = [float(c.get("score") or 0.0) for c in candidates]
    mx = max(scores) if scores else 1.0
    mn = min(scores) if scores else 0.0
    span = mx - mn or 1.0
    
    # 2. Extract weights
    w_semantic = float(getattr(settings, "ranking_weight_semantic", 1.0 - lexical_weight)) if settings else (1.0 - lexical_weight)
    w_lexical = float(getattr(settings, "ranking_weight_lexical", lexical_weight)) if settings else lexical_weight
    w_experience = float(getattr(settings, "ranking_weight_experience", 0.0)) if settings else 0.0
    w_rating = float(getattr(settings, "ranking_weight_rating", 0.0)) if settings else 0.0
    w_demographic = float(getattr(settings, "ranking_weight_demographic", 0.0)) if settings else 0.0
    
    patient_demo = str(cqu.get("patient_demographic") or "").lower()
    negated_symptoms = cqu.get("negated_symptoms") or []
    
    enriched: list[tuple[float, dict[str, Any]]] = []
    for c in candidates:
        base = float(c.get("score") or 0.0)
        norm = (base - mn) / span
        
        lex = lexical_bonus(query, c)
        
        # Experience bonus (normalize to 0-1, assuming max useful exp is ~30 years)
        exp_years = float(c.get("experience_years") or 0)
        exp_norm = min(1.0, exp_years / 30.0)
        
        # Rating bonus (normalize to 0-1)
        rating = float(c.get("ratings") or 4.0)
        # map 3.5 -> 0, 5.0 -> 1.0 roughly
        rating_norm = max(0.0, min(1.0, (rating - 3.5) / 1.5))
        
        # Demographic bonus
        demo_bonus = 0.0
        if any(keyword in patient_demo for keyword in ("trẻ em", "bé", "con", "nhi")):
            pg = str(c.get("patient_groups") or "").lower()
            spec = str(c.get("specialties_label") or "").lower()
            if "trẻ em" in pg or "nhi khoa" in spec:
                demo_bonus = 1.0
        elif any(keyword in patient_demo for keyword in ("người già", "lớn tuổi", "cụ")):
            pg = str(c.get("patient_groups") or "").lower()
            spec = str(c.get("specialties_label") or "").lower()
            if "người cao tuổi" in pg or "người lớn" in pg or "lão khoa" in spec:
                demo_bonus = 1.0
        
        # Negation penalty
        negation_penalty = 0.0
        if negated_symptoms:
            c_text = " ".join(str(c.get(k) or "") for k in ("conditions", "symptoms")).lower()
            for neg in negated_symptoms:
                if neg in c_text:
                    negation_penalty += 0.2  # Penalize strongly if doctor is associated with negated symptom
        
        # Specialty Intent bonus
        intent_bonus = 0.0
        if "intent_rank" in c:
            rank = int(c["intent_rank"])
            intent_bonus = max(0.0, 1.0 - rank * 0.25)

        final = (
            norm * w_semantic +
            lex * w_lexical +
            exp_norm * w_experience +
            rating_norm * w_rating +
            demo_bonus * w_demographic +
            intent_bonus * 1.5
        )
        
        # Apply negation penalty
        final = max(0.0, final - negation_penalty)
        
        nc = dict(c)
        nc["score"] = final
        nc["rerank_lexical"] = lex
        nc["rerank_semantic"] = norm
        nc["rerank_exp"] = exp_norm
        nc["rerank_rating"] = rating_norm
        nc["rerank_demo"] = demo_bonus
        if "intent_rank" in c:
            nc["rerank_intent"] = intent_bonus
        if negation_penalty > 0:
            nc["negation_penalty"] = negation_penalty
            
        enriched.append((final, nc))
        
    enriched.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in enriched]


@lru_cache(maxsize=2)
def _flashrank_ranker(model_name: str, cache_dir: str):
    from flashrank import Ranker

    return Ranker(model_name=model_name, cache_dir=cache_dir)


def rerank_flashrank(
    query: str,
    candidates: list[dict[str, Any]],
    model_name: str = "ms-marco-MiniLM-L-12-v2",
    cache_dir: str | None = None,
    top_n: int | None = None,
) -> list[dict[str, Any]]:
    if not candidates:
        return []
    from flashrank import RerankRequest

    import tempfile

    cdir = cache_dir or tempfile.mkdtemp(prefix="medicalink_flashrank_")
    try:
        ranker = _flashrank_ranker(model_name, cdir)
    except Exception as e:
        logger.warning("FlashRank không khởi tạo được, bỏ qua: %s", e)
        return candidates
    passages: list[dict[str, str]] = []
    for i, c in enumerate(candidates):
        did = str(c.get("doctor_id") or i)
        text_parts = [
            str(c.get("full_name") or ""),
            str(c.get("specialties_label") or ""),
            (str(c.get("source_json") or ""))[:1200],
        ]
        passages.append({"id": did, "text": " | ".join(p for p in text_parts if p)})
    try:
        ranked = ranker.rerank(RerankRequest(query=query, passages=passages))
    except Exception as e:
        logger.warning("FlashRank.rerank lỗi: %s", e)
        return candidates
    by_id = {str(c.get("doctor_id")): dict(c) for c in candidates if c.get("doctor_id")}
    out: list[dict[str, Any]] = []
    for p in ranked:
        rid = str(p.get("id") or "")
        if rid in by_id:
            row = dict(by_id[rid])
            if "score" in p:
                row["score"] = float(p["score"])
            row["rerank_flashrank"] = True
            out.append(row)
    for c in candidates:
        cid = str(c.get("doctor_id") or "")
        if cid and cid not in {str(x.get("doctor_id")) for x in out}:
            out.append(dict(c))
    if top_n is not None:
        out = out[:top_n]
    return out


def rerank_pipeline(
    query: str,
    candidates: list[dict[str, Any]],
    *,
    mode: RerankMode,
    lexical_weight: float,
    flashrank_model: str,
    flashrank_cache_dir: str | None,
    flashrank_pool: int,
    cqu_data: dict[str, Any] | None = None,
    settings: Any = None,
) -> list[dict[str, Any]]:
    if not candidates:
        return []
    pool = candidates[: min(len(candidates), flashrank_pool)]
    if mode == "none":
        return pool
    if mode == "lexical":
        return blend_scores(query, pool, lexical_weight=max(0.0, min(lexical_weight, 0.9)), cqu_data=cqu_data, settings=settings)
    if mode == "flashrank":
        fr = rerank_flashrank(
            query,
            pool,
            model_name=flashrank_model,
            cache_dir=flashrank_cache_dir,
        )
        # Even with flashrank, we apply the multi-factor blend (experience, rating, demographic, etc.)
        # Here we use lexical_weight conceptually to blend flashrank (semantic) with lexical, 
        # but blend_scores uses settings to read ALL weights (semantic, lexical, experience, rating, demographic)
        return blend_scores(query, fr, lexical_weight=lexical_weight, cqu_data=cqu_data, settings=settings)
    return pool
