"""
Đồng bộ ban đầu: GET /api/doctors/profile/public (paginate) -> embed -> Qdrant.

Chạy:  python -m medicalink_ai.scripts.batch_sync

Cần: API gateway + Qdrant + OPENAI_API_KEY; không cần RabbitMQ.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from tqdm import tqdm

from medicalink_ai.config import get_settings
from medicalink_ai.vector_store import DoctorVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_all_public_doctors(base_url: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    page = 1
    limit = 50
    async with httpx.AsyncClient(timeout=60.0) as client:
        while True:
            url = f"{base_url.rstrip('/')}/api/doctors/profile/public"
            r = await client.get(url, params={"page": page, "limit": limit})
            r.raise_for_status()
            body = r.json()
            chunk = body.get("data") or []
            for item in chunk:
                if isinstance(item, dict):
                    out.append(item)
            meta = body.get("meta") or {}
            has_next = bool(meta.get("hasNext"))
            logger.info("page %s: +%s doctors", page, len(chunk))
            if not has_next or not chunk:
                break
            page += 1
    return out


async def main() -> None:
    s = get_settings()
    if not s.openai_api_key:
        raise SystemExit("Thiếu OPENAI_API_KEY")

    openai = AsyncOpenAI(api_key=s.openai_api_key)
    qdrant_kw: dict[str, Any] = {"url": s.qdrant_url}
    if (s.qdrant_api_key or "").strip():
        qdrant_kw["api_key"] = s.qdrant_api_key.strip()
    qdrant = AsyncQdrantClient(**qdrant_kw)
    store = DoctorVectorStore(
        qdrant=qdrant,
        openai=openai,
        collection_name=s.qdrant_collection_name,
        embedding_model=s.openai_embedding_model,
        openai_api_key=s.openai_api_key,
        embedding_version=s.embedding_version,
        max_embedding_tokens=s.max_embedding_tokens,
        hybrid_enabled=s.rag_hybrid_enabled,
        dense_name=s.dense_vector_name,
        sparse_name=s.sparse_vector_name,
        sparse_model_name=s.fastembed_sparse_model,
        prefetch_limit=s.retrieval_prefetch_limit,
    )
    
    # Delete old collection to prevent orphaned data from soft-deleted doctors
    try:
        await qdrant.delete_collection(s.qdrant_collection_name)
        logger.info(f"Deleted old collection {s.qdrant_collection_name} to clear stale data")
    except Exception as e:
        logger.warning(f"Could not delete collection (maybe not exists): {e}")

    await store.ensure_collection()

    doctors = await fetch_all_public_doctors(s.api_gateway_base_url)
    logger.info("Total doctors from API: %s", len(doctors))

    # Chuẩn bị dữ liệu
    for d in doctors:
        if "isActive" not in d:
            d["isActive"] = True

    # Batching (ví dụ: batch_size = 20)
    batch_size = 20
    batches = [doctors[i:i + batch_size] for i in range(0, len(doctors), batch_size)]

    for batch in tqdm(batches, desc="Upserting to Qdrant", unit="batch"):
        await store.upsert_doctors(batch)

    logger.info("Batch sync done.")


def cli() -> None:
    """Entry point cho `medicalink-ai-sync` (console_scripts)."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
