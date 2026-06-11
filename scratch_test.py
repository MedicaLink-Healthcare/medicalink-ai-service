import asyncio
from medicalink_ai.dependencies import get_specialty_vector_store

async def main():
    store = get_specialty_vector_store()
    
    cases = [
        ("Nhi Khoa", "bé 3 tuổi sốt cao 39 độ, ho đờm, bỏ bú", ""),
        ("Sản phụ khoa", "rối loạn kinh nguyệt nhiều tháng nay, hay đau quặn bụng dưới", ""),
        ("Tiêu hóa", "tôi hay bị ợ chua lúc rạng sáng nhưng không buồn nôn", ""),
        ("Tiêu hóa 2", "đau vùng dạ dày, uống thuốc dạ dày không đỡ, đi cầu phân đen", "")
    ]
    
    for name, symp, priors in cases:
        print(f"--- {name} ---")
        hits = await store.search_specialties(symp, priors, limit=3)
        for h in hits:
            print(f"[{h.get('confidence_score', 0.0):.3f}] {h.get('name')}")

if __name__ == "__main__":
    asyncio.run(main())
