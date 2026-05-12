"""
Đánh giá chất lượng retrieval của RAG (Precision@k, Recall@k).
Chạy: python -m medicalink_ai.scripts.evaluate_rag
"""

import asyncio
import logging
from typing import Any

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient

from medicalink_ai.config import get_settings
from medicalink_ai.vector_store import DoctorVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ví dụ dataset đơn giản
TEST_DATASET = [
    {
        "query": "bác sĩ tim mạch ở Đà Nẵng",
        "expected_ids": ["12", "45"]
    },
    {
        "query": "đau đầu kinh niên",
        "expected_ids": ["7", "89"]
    }
]

async def evaluate(store: DoctorVectorStore, dataset: list[dict[str, Any]], k: int = 5) -> None:
    total_precision = 0.0
    total_recall = 0.0

    for item in dataset:
        query = str(item["query"])
        expected_ids = {str(eid) for eid in item["expected_ids"]}

        candidates, _, _ = await store.search_active(query, limit=k)
        retrieved_ids = [str(c["doctor_id"]) for c in candidates if c.get("doctor_id")]
        retrieved_set = set(retrieved_ids)

        # Precision@k: (Relevant retrieved) / (Total retrieved)
        relevant_retrieved = len(retrieved_set.intersection(expected_ids))
        precision = relevant_retrieved / len(retrieved_set) if retrieved_set else 0.0

        # Recall@k: (Relevant retrieved) / (Total relevant)
        recall = relevant_retrieved / len(expected_ids) if expected_ids else 0.0

        total_precision += precision
        total_recall += recall

        logger.info(f"Query: '{query}'")
        logger.info(f"  Expected: {expected_ids}")
        logger.info(f"  Retrieved: {retrieved_ids}")
        logger.info(f"  Precision@{k}: {precision:.2f}, Recall@{k}: {recall:.2f}\n")

    avg_precision = total_precision / len(dataset) if dataset else 0.0
    avg_recall = total_recall / len(dataset) if dataset else 0.0

    logger.info("--- EVALUATION SUMMARY ---")
    logger.info(f"Average Precision@{k}: {avg_precision:.2f}")
    logger.info(f"Average Recall@{k}: {avg_recall:.2f}")


async def main() -> None:
    s = get_settings()
    if not s.openai_api_key:
        logger.warning("Thiếu OPENAI_API_KEY. Không thể chạy evaluation nếu không có API key.")
        return

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
        max_embedding_chars=s.max_embedding_chars,
        hybrid_enabled=s.rag_hybrid_enabled,
        dense_name=s.dense_vector_name,
        sparse_name=s.sparse_vector_name,
        sparse_model_name=s.fastembed_sparse_model,
        prefetch_limit=s.retrieval_prefetch_limit,
    )

    await evaluate(store, TEST_DATASET, k=5)

if __name__ == "__main__":
    asyncio.run(main())
