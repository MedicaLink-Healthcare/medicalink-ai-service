import urllib.request
import json

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
        data = json.loads(res).get('data', {})
        ids = data.get('specialty_ids', [])
        names = get_specialty_names(ids)
        print(f"Query: {query}\nResult: {', '.join(names)}\n")
    except Exception as e:
        print(f"Error on {query}: {e}")

queries = [
    "trẻ đi ngoài phân lỏng, nôn trớ nhiều sau khi ăn",
    "rối loạn kinh nguyệt nhiều tháng nay, hay đau quặn bụng dưới",
    "tôi hay bị ợ chua lúc rạng sáng nhưng không buồn nôn"
]

for q in queries:
    test_api(q)
