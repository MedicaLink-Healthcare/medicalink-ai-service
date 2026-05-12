import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, cast

from fastembed import TextEmbedding
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, PointStruct, ScoredPoint, VectorParams

logger = logging.getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class SemanticCacheService:
    qdrant: AsyncQdrantClient
    collection_name: str = "query_cache"
    threshold: float = 0.95
    model_name: str = "BAAI/bge-small-en-v1.5"

    _model: TextEmbedding | None = None

    def _get_model(self) -> TextEmbedding:
        if self._model is None:
            logger.info(f"Loading Semantic Cache embedding model: {self.model_name}")
            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    def _embed_query(self, query: str) -> list[float]:
        # FastEmbed is CPU-bound, wrapped in to_thread during async call
        model = self._get_model()
        embeddings = list(model.embed([query]))
        if not embeddings:
            return []
        # Convert numpy array to list
        return [float(x) for x in embeddings[0]]

    async def ensure_collection(self) -> None:
        exists = await self.qdrant.collection_exists(self.collection_name)
        if not exists:
            # We initialize the model to check its vector size
            dummy = await asyncio.to_thread(self._embed_query, "dummy_init")
            vector_size = len(dummy)
            if vector_size == 0:
                logger.error("Failed to initialize Semantic Cache model")
                return

            logger.info(f"Creating semantic cache collection '{self.collection_name}' with size {vector_size}")
            await self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
        else:
            logger.info(f"Semantic cache collection '{self.collection_name}' already exists.")

    async def get_cache(self, query: str) -> dict[str, Any] | None:
        try:
            vector = await asyncio.to_thread(self._embed_query, query)
            if not vector:
                return None

            results = await self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=1,
                score_threshold=self.threshold,
            )
            if results:
                hit: ScoredPoint = results[0]
                logger.info(f"Semantic cache HIT for query '{query}' (score: {hit.score:.4f})")
                payload = hit.payload or {}
                result_str = str(payload.get("result_json") or "")
                if result_str:
                    return cast(dict[str, Any], json.loads(result_str))
            return None
        except Exception as e:
            logger.error(f"Error reading semantic cache: {e}", exc_info=True)
            return None

    async def set_cache(self, query: str, result: dict[str, Any]) -> None:
        try:
            vector = await asyncio.to_thread(self._embed_query, query)
            if not vector:
                return

            # Avoid ID collisions for exact same queries by using uuid5
            point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"cache:{query}"))

            await self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "query": query,
                            "result_json": json.dumps(result, ensure_ascii=False),
                            "created_at": int(time.time()),
                        },
                    )
                ],
            )
            logger.info(f"Saved query '{query}' to semantic cache")
        except Exception as e:
            logger.error(f"Error writing semantic cache: {e}", exc_info=True)
