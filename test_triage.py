import asyncio
import json
import sys
from pprint import pprint

from medicalink_ai.config import get_settings
from medicalink_ai.intent_specialty import suggest_specialties_from_catalog
from medicalink_ai.vector_store_specialty import SpecialtyVectorStore
from qdrant_client import AsyncQdrantClient
from openai import AsyncOpenAI

def get_specialty_names(ids):
    try:
        with open('data/specialties_cleaned.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            catalog = {s['id']: s['name'] for s in data['specialties']}
            return [catalog.get(i, i) for i in ids]
    except Exception as e:
        return ids

async def run_tests():
    settings = get_settings()
    
    # Init qdrant and openai
    qdrant = AsyncQdrantClient(url="http://localhost:6333", api_key=settings.qdrant_api_key)
    openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    # Init vector store
    store = SpecialtyVectorStore(
        qdrant=qdrant,
        openai=openai_client,
        collection_name="specialties",
        embedding_model=settings.openai_embedding_model,
        hybrid_enabled=settings.rag_hybrid_enabled
    )

    queries = [
        "Bị ù tai như tiếng ve kêu liên tục trong đầu, rất khó chịu",
        "Cần tư vấn về phác đồ hóa trị cho K đại tràng giai đoạn 2",
        "Tôi mới phát hiện bị hẹp van tim 2 lá",
        "nổi hạch ở cổ lâu ngày không xẹp, sụt cân nhanh",
        "đau tức hạ sườn phải, vàng da",
        "Cho mình hỏi cách luộc thịt gà ngon",
        "Trời hôm nay nắng đẹp quá, đi chơi không?",
    ]

    print("🚀 ĐANG KIỂM THỬ TRỰC TIẾP MODULE ĐỊNH TUYẾN CHUYÊN KHOA\n")
    for q in queries:
        print("="*80)
        print(f"🔹 CÂU HỎI: {q}")
        try:
            with open('data/specialties_cleaned.json', 'r', encoding='utf-8') as f:
                cat_data = json.load(f)['specialties']
            result = await suggest_specialties_from_catalog(
                symptoms=q,
                catalog=cat_data,
                settings=settings,
                openai=openai_client,
                specialty_store=store,
            )
            
            print(f"🔸 Phân loại: {result.get('triage_level')} | Mức độ: {result.get('severity')}")
            print(f"🔸 Triệu chứng: {', '.join(result.get('extracted_symptoms', []))}")
            print(f"🔸 Bệnh lý (Priors): {', '.join(result.get('common_priors', []))}")
            
            if result.get("is_fallback"):
                print(f"❌ FALLBACK: {result.get('fallback_reason')}")
            else:
                ids = result.get('specialty_ids', [])
                names = get_specialty_names(ids)
                print(f"✅ Gợi ý chuyên khoa: {', '.join(names)}")
                print(f"   Độ tự tin: {result.get('routing_confidence')}")
        except Exception as e:
            print(f"❌ LỖI: {e}")
        print("="*80 + "\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_tests())
