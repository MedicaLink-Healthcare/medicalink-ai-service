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

async def fetch_all_specialties_from_file() -> list[dict[str, Any]]:
    import json
    from pathlib import Path
    
    file_path = Path(__file__).parent.parent.parent / "data" / "specialties_cleaned.json"
    if not file_path.exists():
        logger.error(f"Cannot find {file_path}")
        return []
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("specialties", [])

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

    specialties = await fetch_all_specialties_from_file()

    logger.info("Found %d specialties from API. Starting upsert to Qdrant...", len(specialties))
    await store.upsert_specialties(specialties)
    logger.info("Sync complete!")

if __name__ == "__main__":
    asyncio.run(main())
