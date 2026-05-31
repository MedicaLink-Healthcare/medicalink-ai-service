from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

logger = logging.getLogger(__name__)

DEFAULT_VECTOR_SIZE = 1536


@dataclass(slots=True, kw_only=True)
class SpecialtyVectorStore:
    """Qdrant store for Specialty profiles to enable Semantic Vector Routing."""

    qdrant: AsyncQdrantClient
    openai: AsyncOpenAI
    collection_name: str = "specialties"
    embedding_model: str = "text-embedding-3-small"

    async def embed_text(self, text: str) -> list[float]:
        response = await self.openai.embeddings.create(
            input=[text.replace("\n", " ").strip()],
            model=self.embedding_model,
        )
        return response.data[0].embedding

    async def ensure_collection(self) -> None:
        try:
            await self.qdrant.get_collection(self.collection_name)
            return
        except Exception:
            pass

        # Create dense-only collection for specialties (simpler, highly effective for short text)
        await self.qdrant.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=DEFAULT_VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
        logger.info("Created Qdrant collection %s", self.collection_name)

    def _build_specialty_text(self, spec: dict[str, Any]) -> str:
        name = str(spec.get("name") or "").strip()
        parts = [f"Chuyên khoa: {name}"]
        
        for key, prefix in [("aliases", "Tên gọi khác: "), ("keywords", "Từ khóa: "), ("common_symptoms", "Triệu chứng thường gặp: ")]:
            arr = spec.get(key)
            if isinstance(arr, list) and arr:
                clean_arr = [str(x).strip() for x in arr if str(x).strip()]
                if clean_arr:
                    parts.append(prefix + ", ".join(clean_arr))
                    
        return "\n".join(parts)

    async def upsert_specialties(self, specialties: list[dict[str, Any]]) -> None:
        if not specialties:
            return
        await self.ensure_collection()
        
        import uuid
        points = []
        for spec in specialties:
            sid = str(spec.get("id") or "").strip()
            if not sid:
                continue
                
            point_id = str(uuid.uuid5(uuid.NAMESPACE_OID, sid))
            text = self._build_specialty_text(spec)
            dense = await self.embed_text(text)
            
            points.append(
                PointStruct(
                    id=point_id, 
                    vector=dense,
                    payload=spec,
                )
            )
            
        if points:
            await self.qdrant.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info("Upserted %s specialties to Qdrant", len(points))

    async def search_specialties(
        self,
        query_symptoms: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Returns top K specialties for the given symptoms using Cosine Similarity."""
        await self.ensure_collection()
        
        if not query_symptoms.strip():
            return []
            
        vector = await self.embed_text(query_symptoms)
        
        res = await self.qdrant.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit,
            with_payload=True,
        )
        hits = res.points or []
        
        out = []
        for h in hits:
            pl = h.payload or {}
            out.append({
                "id": pl.get("id"),
                "name": pl.get("name"),
                "score": h.score,
            })
        return out
