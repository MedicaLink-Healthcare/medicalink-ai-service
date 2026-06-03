import asyncio
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

from medicalink_ai.config import get_settings
from medicalink_ai.intent_specialty import suggest_specialties_from_catalog
from medicalink_ai.vector_store_specialty import SpecialtyVectorStore
from qdrant_client import AsyncQdrantClient
from openai import AsyncOpenAI

async def test():
    s = get_settings()
    qc = AsyncQdrantClient(url=s.qdrant_url, api_key=s.qdrant_api_key)
    oa = AsyncOpenAI(api_key=s.openai_api_key) if s.llm_provider=='openai' else None
    
    # Simple catalog mock
    cat = [
        {'id': 'cmn0d8db982b8a74ee1808972', 'name': 'Nội khoa', 'aliases': [], 'keywords': [], 'common_symptoms': []},
        {'id': 'cmn8e15f11b477a48e2989d59', 'name': 'Tim mạch', 'aliases': [], 'keywords': [], 'common_symptoms': []},
        {'id': 'nhi_khoa_123', 'name': 'Nhi khoa', 'aliases': [], 'keywords': [], 'common_symptoms': []}
    ]
    
    vs = SpecialtyVectorStore(qdrant=qc, openai=oa, collection_name='specialties', embedding_model='test')
    
    query = "con tôi 5 tuổi bị đau bụng kéo dài 3 tháng nay nhưng không bị nôn mửa"
    print(f"Testing query: {query}")
    res = await suggest_specialties_from_catalog(
        symptoms=query, 
        catalog=cat, 
        settings=s, 
        openai=oa, 
        specialty_store=vs
    )
    
    print("\n[RESULT]")
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test())
