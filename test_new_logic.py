import urllib.request
import json
import sys

def get_specialty_names(ids):
    try:
        with open('data/specialties_cleaned.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            catalog = {s['id']: s['name'] for s in data['specialties']}
            return [catalog.get(i, i) for i in ids]
    except Exception as e:
        return ids

def test_api(query):
    req = urllib.request.Request(
        'https://api.medicalink.online/api/ai/suggest-specialties', 
        data=json.dumps({'symptoms': query}).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        res = urllib.request.urlopen(req).read().decode('utf-8')
        parsed = json.loads(res)
        data = parsed.get('data', {})
        ids = data.get('specialty_ids', [])
        names = get_specialty_names(ids)
        
        print("="*60)
        print(f"🔹 Câu hỏi: {query}")
        print(f"🔸 Phân loại: {data.get('triage_level', 'unknown')} | Mức độ: {data.get('severity', 'unknown')}")
        print(f"🔸 Triệu chứng: {', '.join(data.get('extracted_symptoms', []))}")
        print(f"🔸 Bệnh lý (Priors): {', '.join(data.get('common_priors', []))}")
        
        if data.get("is_fallback") and data.get("fallback_reason") == "out_of_scope":
            print(f"❌ OUT OF SCOPE: Câu hỏi bị từ chối bởi Guardrail.")
        else:
            print(f"✅ Gợi ý chuyên khoa: {', '.join(names)}")
            if data.get('routing_confidence'):
                print(f"   (Độ tự tin: {data['routing_confidence']})")
            
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Lỗi khi test '{query}': {e}")

queries = [
    # Nhóm 1: Bệnh lý trực tiếp (Không có triệu chứng rõ ràng) - Lúc trước bị lỗi Out of Scope
    "Cần tư vấn về phác đồ hóa trị cho K đại tràng giai đoạn 2",
    "Tôi mới phát hiện bị hẹp van tim 2 lá",
    
    # Nhóm 2: Triệu chứng mơ hồ cần dựa vào Priors để xác định chuyên khoa
    "nổi hạch ở cổ lâu ngày không xẹp, sụt cân nhanh",
    "đau tức hạ sườn phải, vàng da",
    "tiểu buốt, đau rát, đi tiểu nhiều lần về đêm",

    # Nhóm 3: Test câu hỏi ngoài lề (Đảm bảo Guardrail vẫn hoạt động tốt)
    "Cho mình hỏi cách luộc thịt gà ngon",
    "Trời hôm nay nắng đẹp quá, đi chơi không?"
]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    print("🚀 ĐANG KIỂM THỬ API MEDICALINK AI SAU KHI FIX BUG\n")
    for q in queries:
        test_api(q)
