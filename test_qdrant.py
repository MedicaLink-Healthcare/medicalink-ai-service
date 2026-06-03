import asyncio
from medicalink_ai.config import get_settings
from medicalink_ai.vector_store import DoctorVectorStore
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient

async def main():
    settings = get_settings()
    store = DoctorVectorStore(
        qdrant=AsyncQdrantClient(url="http://localhost:6333", api_key=settings.qdrant_api_key),
        openai=AsyncOpenAI(api_key=settings.openai_api_key),
        collection_name=settings.qdrant_collection_name,
        embedding_model=settings.openai_embedding_model,
        openai_api_key=settings.openai_api_key,
        hybrid_enabled=settings.rag_hybrid_enabled,
    )
    symptoms = "đau ngực và khó thở"
    sp_id = "cmna8cf9e42b9c14beca968d2"
    
    candidates, hybrid, legacy = await store.search_active(symptoms, limit=10, filter_specialty_ids=[sp_id])
    print(f"Got {len(candidates)} candidates. Hybrid: {hybrid}. Legacy: {legacy}")
    for c in candidates:
        print(c.get("full_name").encode('utf-8'))
    
if __name__ == "__main__":
    asyncio.run(main())
