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
    spec_filter = ["cmna8cf9e42b9c14beca968d2", "cmn7c81420344b546258ba767", "cmn258c9a1889e048699dcfda", "cmn305ee71e46d24f2396fe68", "cmn4132816e364b4603a2fed9"]
    
    per_spec_limit = 10
    for i, sp_id in enumerate(spec_filter):
        cands, _, _ = await store.search_active(
            symptoms,
            limit=per_spec_limit,
            filter_specialty_ids=[sp_id]
        )
        print(f"Specialty index {i} ({sp_id}): got {len(cands)} candidates")

if __name__ == "__main__":
    asyncio.run(main())
