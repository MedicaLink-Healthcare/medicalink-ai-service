from __future__ import annotations

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client import models as qm
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    SparseVectorParams,
    ChangeAliasesOperation,
    CreateAliasOperation,
)

from medicalink_ai.sparse_encoder import text_to_sparse_vector

logger = logging.getLogger(__name__)

DEFAULT_VECTOR_SIZE = 1536


@dataclass(slots=True, kw_only=True)
class SpecialtyVectorStore:
    """Qdrant store for Specialty profiles to enable Semantic Vector Routing with Alias Migration."""

    qdrant: AsyncQdrantClient
    openai: AsyncOpenAI
    collection_name: str = "specialties"
    embedding_model: str = "text-embedding-3-small"
    dense_name: str = "dense"
    sparse_name: str = "lexical"
    sparse_model_name: str = "Qdrant/bm25"
    hybrid_enabled: bool = True

    async def embed_text(self, text: str) -> list[float]:
        response = await self.openai.embeddings.create(
            input=[text.replace("\n", " ").strip()],
            model=self.embedding_model,
        )
        return response.data[0].embedding

    async def _create_hybrid_collection(self, target_name: str) -> None:
        if self.hybrid_enabled:
            await self.qdrant.create_collection(
                collection_name=target_name,
                vectors_config={
                    self.dense_name: VectorParams(
                        size=DEFAULT_VECTOR_SIZE,
                        distance=Distance.COSINE,
                    )
                },
                sparse_vectors_config={
                    self.sparse_name: SparseVectorParams(),
                },
            )
        else:
            await self.qdrant.create_collection(
                collection_name=target_name,
                vectors_config=VectorParams(
                    size=DEFAULT_VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

    async def ensure_collection(self) -> None:
        try:
            await self.qdrant.get_collection(self.collection_name)
            return
        except Exception:
            pass

        # If it doesn't exist at all, we create v0 and alias it so the system can run immediately
        init_col = f"{self.collection_name}_v0"
        await self._create_hybrid_collection(init_col)
        await self.qdrant.update_collection_aliases(
            change_aliases_operations=[
                CreateAliasOperation(
                    create_alias=qm.CreateAlias(collection_name=init_col, alias_name=self.collection_name)
                )
            ]
        )
        logger.info("Created initial Qdrant collection %s with alias %s", init_col, self.collection_name)

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
            
        # 1. Check if self.collection_name is currently a normal collection (legacy)
        is_normal_collection = False
        try:
            collections_res = await self.qdrant.get_collections()
            col_names = [c.name for c in collections_res.collections]
            if self.collection_name in col_names:
                aliases_res = await self.qdrant.get_aliases()
                is_alias = any(a.alias_name == self.collection_name for a in aliases_res.aliases)
                is_normal_collection = not is_alias
        except Exception:
            pass
            
        # 2. Create new target collection for zero-downtime migration
        target_col = f"{self.collection_name}_v{int(time.time())}"
        await self._create_hybrid_collection(target_col)
        logger.info("Created new versioned collection %s for upsert", target_col)
        
        points = []
        for spec in specialties:
            sid = str(spec.get("id") or "").strip()
            if not sid:
                continue
                
            point_id = str(uuid.uuid5(uuid.NAMESPACE_OID, sid))
            text = self._build_specialty_text(spec)
            dense = await self.embed_text(text)
            
            if self.hybrid_enabled:
                sparse = await asyncio.to_thread(text_to_sparse_vector, text, self.sparse_model_name, 5000)
                points.append(
                    PointStruct(
                        id=point_id, 
                        vector={
                            self.dense_name: dense,
                            self.sparse_name: sparse,
                        },
                        payload=spec,
                    )
                )
            else:
                points.append(
                    PointStruct(
                        id=point_id, 
                        vector=dense,
                        payload=spec,
                    )
                )
            
        if points:
            await self.qdrant.upsert(
                collection_name=target_col,
                points=points,
            )
            logger.info("Upserted %s specialties to %s", len(points), target_col)
            
        # 3. Swap aliases safely
        actions = []
        
        if is_normal_collection:
            logger.warning("Found normal collection %s, replacing with alias...", self.collection_name)
            await self.qdrant.delete_collection(self.collection_name)
            actions.append(CreateAliasOperation(create_alias=qm.CreateAlias(collection_name=target_col, alias_name=self.collection_name)))
            await self.qdrant.update_collection_aliases(change_aliases_operations=actions)
            logger.info("Swapped normal collection to alias %s pointing to %s", self.collection_name, target_col)
        else:
            old_cols_to_delete = []
            try:
                aliases_res = await self.qdrant.get_aliases()
                for a in aliases_res.aliases:
                    if a.alias_name == self.collection_name:
                        old_cols_to_delete.append(a.collection_name)
            except Exception:
                pass
                
            actions.append(CreateAliasOperation(create_alias=qm.CreateAlias(collection_name=target_col, alias_name=self.collection_name)))
            await self.qdrant.update_collection_aliases(change_aliases_operations=actions)
            logger.info("Swapped alias %s to point to %s", self.collection_name, target_col)
            
            # Clean up old collections in background
            for old_col in old_cols_to_delete:
                if old_col != target_col:
                    try:
                        await self.qdrant.delete_collection(old_col)
                        logger.info("Cleaned up old versioned collection %s", old_col)
                    except Exception as e:
                        logger.warning("Failed to delete old collection %s: %s", old_col, e)

    async def search_specialties(
        self,
        query_symptoms: str,
        query_priors: str = "",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Returns top K specialties using Weighted Hybrid Fusion (Symptoms 75% + Priors 25%)."""
        await self.ensure_collection()
        
        if not query_symptoms.strip():
            return []
            
        async def perform_search(query_text: str) -> list[Any]:
            vector = await self.embed_text(query_text)
            if self.hybrid_enabled:
                sparse = await asyncio.to_thread(text_to_sparse_vector, query_text, self.sparse_model_name, 5000)
                res = await self.qdrant.query_points(
                    collection_name=self.collection_name,
                    prefetch=[
                        qm.Prefetch(query=vector, using=self.dense_name, limit=limit * 2),
                        qm.Prefetch(query=sparse, using=self.sparse_name, limit=limit * 2),
                    ],
                    query=qm.FusionQuery(fusion=qm.Fusion.RRF),
                    limit=limit * 2,
                    with_payload=True,
                )
                return res.points or []
            else:
                res = await self.qdrant.query_points(
                    collection_name=self.collection_name,
                    query=vector,
                    limit=limit * 2,
                    with_payload=True,
                )
                return res.points or []

        hits_dict = {}
        
        # 1. Search Symptoms (Weight 0.75)
        symptom_points = await perform_search(query_symptoms)
        for h in symptom_points:
            sid = h.payload.get("id")
            if sid:
                hits_dict[sid] = {"payload": h.payload, "score": float(h.score or 0) * 0.75}

        # 2. Search Priors (Weight 0.25)
        if query_priors.strip():
            prior_points = await perform_search(query_priors)
            for h in prior_points:
                sid = h.payload.get("id")
                if sid:
                    if sid in hits_dict:
                        hits_dict[sid]["score"] += float(h.score or 0) * 0.25
                    else:
                        hits_dict[sid] = {"payload": h.payload, "score": float(h.score or 0) * 0.25}
            logger.info("[Specialty Retrieval] Weighted Fusion used (Symptoms 75%%, Priors 25%%).")
        else:
            logger.info("[Specialty Retrieval] Symptoms only used (no priors).")

        # 3. Sort by final score
        sorted_hits = sorted(hits_dict.values(), key=lambda x: x["score"], reverse=True)[:limit]
        
        out = []
        for h in sorted_hits:
            pl = h["payload"]
            # Confidence score scaling (since weight max is 1.0, same scale applies)
            conf = round(min(1.0, h["score"] * 1.5), 2) if self.hybrid_enabled else round(h["score"], 2)
            out.append({
                "id": pl.get("id"),
                "name": pl.get("name"),
                "score": h["score"],
                "confidence_score": conf
            })
        return out
