import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

import httpx

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient

from medicalink_ai.config import get_settings
from medicalink_ai.vector_store_specialty import SpecialtyVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_all_public_specialties(base_url: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    page = 1
    limit = 50
    async with httpx.AsyncClient(timeout=60.0) as client:
        while True:
            url = f"{base_url.rstrip('/')}/api/specialties/public"
            r = await client.get(url, params={"page": page, "limit": limit})
            r.raise_for_status()
            body = r.json()
            chunk = body.get("data") or []
            for item in chunk:
                if isinstance(item, dict):
                    out.append(item)
            meta = body.get("meta") or {}
            has_next = bool(meta.get("hasNext"))
            logger.info("page %s: +%s specialties", page, len(chunk))
            if not has_next or not chunk:
                break
            page += 1
    return out

async def main():
    settings = get_settings()

    if not settings.openai_api_key:
        logger.error("Missing OPENAI_API_KEY")
        return

    qdrant_kw = {"url": settings.qdrant_url}
    if (settings.qdrant_api_key or "").strip():
        qdrant_kw["api_key"] = settings.qdrant_api_key.strip()

    qdrant = AsyncQdrantClient(**qdrant_kw)
    openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    store = SpecialtyVectorStore(
        qdrant=qdrant,
        openai=openai_client,
        collection_name="specialties",
        embedding_model=settings.openai_embedding_model,
    )

    specialties = await fetch_all_public_specialties(settings.api_gateway_base_url)

    logger.info("Found %d specialties from API. Starting upsert to Qdrant...", len(specialties))
    await store.upsert_specialties(specialties)
    logger.info("Sync complete!")

if __name__ == "__main__":
    asyncio.run(main())
