import asyncio
import argparse
import os
import json
import time
from medicalink_ai.vector_store import DoctorVectorStore
from medicalink_ai.sparse_encoder import text_to_sparse_vector
from medicalink_ai.config import get_settings
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Prefetch, FusionQuery, Fusion, FieldCondition, MatchValue, Filter
from openai import AsyncOpenAI
import logging

# Tắt log quá nhiều của httpx
logging.getLogger("httpx").setLevel(logging.WARNING)

async def run_benchmark():
    settings = get_settings()
    
    # Initialize Qdrant Client (Force localhost if running outside Docker)
    qdrant_url = settings.qdrant_url.replace("qdrant", "localhost") if "qdrant" in settings.qdrant_url else settings.qdrant_url
    q_client = AsyncQdrantClient(
        url=qdrant_url,
        api_key=settings.qdrant_api_key if isinstance(settings.qdrant_api_key, str) else (settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None)
    )
    
    openai_key = settings.openai_api_key if isinstance(settings.openai_api_key, str) else (settings.openai_api_key.get_secret_value() if settings.openai_api_key else "")
    openai_client = AsyncOpenAI(api_key=openai_key)
    
    print(f"Kết nối tới Qdrant tại: {settings.qdrant_url}")
    
    try:
        col_info = await q_client.get_collection(settings.qdrant_collection_name)
        print(f"Collection {settings.qdrant_collection_name} hợp lệ. Số lượng vector: {col_info.points_count}")
    except Exception as e:
        print(f"Không thể kết nối Qdrant hoặc collection không tồn tại: {e}")
        return

    # Load test cases
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "rag_test_cases.json")
    with open(file_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    dense_passed = 0
    sparse_passed = 0
    hybrid_passed = 0
    
    dense_mrr = 0.0
    sparse_mrr = 0.0
    hybrid_mrr = 0.0
    
    total_cases = 0

    print("\nĐang tiến hành Benchmark Định tuyến (Routing Evaluation)...\n")

    for specialty, spec_data in test_data.items():
        spec_id = spec_data.get("specialty_id", "")
        cases = spec_data.get("cases", [])
        
        for tc in cases:
            query = tc["query"]
            total_cases += 1
            
            # Embeddings
            dense_vector_resp = await openai_client.embeddings.create(
                input=[query],
                model=settings.openai_embedding_model
            )
            dense_vector = dense_vector_resp.data[0].embedding
            sparse_vector = await asyncio.to_thread(text_to_sparse_vector, query, "Qdrant/bm25", 20000)
            
            flt = Filter(must=[FieldCondition(key="is_active", match=MatchValue(value=True))])
            
            # 1. DENSE ONLY
            dense_res = await q_client.query_points(
                collection_name=settings.qdrant_collection_name,
                query=dense_vector,
                using="dense",
                query_filter=flt,
                limit=5,
                with_payload=True
            )
            dense_specs = [p.payload.get("specialty_ids", []) for p in dense_res.points]
            for rank, specs in enumerate(dense_specs):
                if spec_id in specs:
                    dense_passed += 1
                    dense_mrr += 1.0 / (rank + 1)
                    break

            # 2. SPARSE ONLY
            sparse_res = await q_client.query_points(
                collection_name=settings.qdrant_collection_name,
                query=sparse_vector,
                using="lexical",
                query_filter=flt,
                limit=5,
                with_payload=True
            )
            sparse_specs = [p.payload.get("specialty_ids", []) for p in sparse_res.points]
            for rank, specs in enumerate(sparse_specs):
                if spec_id in specs:
                    sparse_passed += 1
                    sparse_mrr += 1.0 / (rank + 1)
                    break

            # 3. HYBRID RRF
            hybrid_res = await q_client.query_points(
                collection_name=settings.qdrant_collection_name,
                prefetch=[
                    Prefetch(query=dense_vector, using="dense", filter=flt, limit=20),
                    Prefetch(query=sparse_vector, using="lexical", filter=flt, limit=20),
                ],
                query=FusionQuery(fusion=Fusion.RRF),
                limit=5,
                with_payload=True
            )
            hybrid_specs = [p.payload.get("specialty_ids", []) for p in hybrid_res.points]
            for rank, specs in enumerate(hybrid_specs):
                if spec_id in specs:
                    hybrid_passed += 1
                    hybrid_mrr += 1.0 / (rank + 1)
                    break

    print("=" * 60)
    print("KẾT QUẢ BENCHMARK (TOP-5 HIT RATE)")
    print("=" * 60)
    print(f"Tổng số Test Cases: {total_cases}")
    
    acc_dense = (dense_passed / total_cases) * 100
    acc_sparse = (sparse_passed / total_cases) * 100
    acc_hybrid = (hybrid_passed / total_cases) * 100
    
    mrr_dense = dense_mrr / total_cases
    mrr_sparse = sparse_mrr / total_cases
    mrr_hybrid = hybrid_mrr / total_cases
    
    print(f" - Dense Vector Only: {dense_passed}/{total_cases} ({acc_dense:.1f}%) | MRR: {mrr_dense:.3f}")
    print(f" - Sparse Vector Only: {sparse_passed}/{total_cases} ({acc_sparse:.1f}%) | MRR: {mrr_sparse:.3f}")
    print(f" - Hybrid RAG (RRF): {hybrid_passed}/{total_cases} ({acc_hybrid:.1f}%) | MRR: {mrr_hybrid:.3f}")
    
    # Ghi đè vào file markdown kết quả
    report = f"""# Báo cáo Benchmark Kiến trúc RAG (Top-5 Hit Rate & MRR)
    
- **Tổng số Test Cases (Lâm sàng)**: {total_cases}

| Phương pháp | HitRate@5 | MRR |
|---|---|---|
| **Dense Vector** | {acc_dense:.1f}% ({dense_passed}/{total_cases}) | {mrr_dense:.3f} |
| **Sparse Vector** | {acc_sparse:.1f}% ({sparse_passed}/{total_cases}) | {mrr_sparse:.3f} |
| **Hybrid RAG** | {acc_hybrid:.1f}% ({hybrid_passed}/{total_cases}) | {mrr_hybrid:.3f} |
"""
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "benchmark_results.md"), "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
