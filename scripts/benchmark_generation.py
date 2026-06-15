import asyncio
import json
import os
import random
import httpx
from medicalink_ai.config import get_settings

# Prompt mẫu đánh giá theo tiêu chuẩn RAGAS
EVAL_PROMPT = """Bạn là một chuyên gia đánh giá mô hình ngôn ngữ (LLM Judge). 
Hãy đánh giá kết quả của hệ thống RAG Y tế theo hai tiêu chí RAGAS (thang điểm 0 đến 1, có thể dùng số thập phân):

1. Faithfulness (Tính trung thực): Câu trả lời có dựa hoàn toàn vào ngữ cảnh (Context) được cung cấp không? Có bịa đặt thông tin y tế nào không?
2. Answer Relevancy (Độ liên quan): Câu trả lời có giải quyết trực tiếp câu hỏi/triệu chứng của bệnh nhân không?

Context:
{context}

Question/Symptoms:
{question}

Answer:
{answer}

Hãy trả về CHỈ MỘT file JSON theo định dạng sau (không markdown, không giải thích thêm):
{{
  "faithfulness": 1.0,
  "answer_relevancy": 1.0,
  "reason": "Giải thích ngắn gọn lý do cho điểm"
}}
"""

async def run_generation_eval():
    settings = get_settings()
    api_key = settings.google_genai_api_key if isinstance(settings.google_genai_api_key, str) else (settings.google_genai_api_key.get_secret_value() if settings.google_genai_api_key else "")
    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    url_suggest = "https://api.medicalink.online/api/ai/suggest-specialties"
    url_recommend = "https://api.medicalink.online/api/ai/recommend-doctor"
    
    print("Đang kết nối tới API Production (https://api.medicalink.online) để đánh giá sinh văn bản...\n")
    
    eval_cases = [
        {"question": "Đau thắt ngực trái dữ dội, vã mồ hôi, cảm giác khó thở"},
        {"question": "Bé nhà tôi 3 tuổi bị nổi mẩn đỏ khắp người kèm sốt nhẹ 38 độ"},
        {"question": "Tôi bị cận thị nặng muốn mổ mắt, dạo này mắt hay mỏi"}
    ]

    total_faithfulness = 0
    total_relevancy = 0
    valid_cases = 0
    
    async with httpx.AsyncClient() as client:
        for i, c in enumerate(eval_cases):
            question = c['question']
            
            # 1. Gọi API Production để Triage & Lấy chuyên khoa
            try:
                res_sug = await client.post(url_suggest, json={"symptoms": question}, timeout=15.0)
                res_sug.raise_for_status()
                sug_data = res_sug.json().get("data", {})
                spec_ids = sug_data.get("specialty_ids", [])
                ext_symp = sug_data.get("extracted_symptoms", [])
                
                if not spec_ids:
                    print(f"Case {i+1} ({question}): API Production không trả về chuyên khoa.")
                    continue
                
                # 2. Gọi API Production để Lấy lý do gợi ý (Answer)
                res_rec = await client.post(url_recommend, json={
                    "symptoms": question,
                    "specialtyIds": spec_ids,
                    "extractedSymptoms": ext_symp
                }, timeout=30.0)
                res_rec.raise_for_status()
                recs = res_rec.json().get("data", {}).get("recommendations", [])
                
                if not recs:
                    print(f"Case {i+1} ({question}): API Production không tìm thấy bác sĩ.")
                    continue
                    
                actual_answer = recs[0].get("reason", "Không có lý do")
                
                # Xây dựng Context giả định từ thông tin thực tế của API
                assumed_context = "Hồ sơ chuyên môn của bác sĩ được hệ thống API trả về khớp với: " + ", ".join(ext_symp)
                
            except Exception as e:
                print(f"Lỗi khi gọi API Production: {e}")
                continue
            prompt = EVAL_PROMPT.format(
                context=assumed_context,
                question=question,
                answer=actual_answer
            )
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            resp = await client.post(url_gemini, json=payload, timeout=60.0)
            resp.raise_for_status()
            
            try:
                raw_text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                res_json = json.loads(raw_text)
                f_score = res_json.get("faithfulness", 0)
                r_score = res_json.get("answer_relevancy", 0)
                
                total_faithfulness += f_score
                total_relevancy += r_score
                valid_cases += 1
                
                print(f"Case {i+1} ({question}):")
                print(f" - API Answer: {actual_answer}")
                print(f" - Faithfulness: {f_score}")
                print(f" - Answer Relevancy: {r_score}")
                print(f" - Reason: {res_json.get('reason')}\n")
                
            except Exception as e:
                print(f"Lỗi khi parse JSON: {e}")
            
    if valid_cases > 0:
        avg_faithfulness = (total_faithfulness / valid_cases) * 100
        avg_relevancy = (total_relevancy / valid_cases) * 100
    else:
        avg_faithfulness = 0
        avg_relevancy = 0
    
    print("=" * 60)
    print("KẾT QUẢ ĐÁNH GIÁ VĂN BẢN (RAGAS METRICS)")
    print("=" * 60)
    print(f"Faithfulness (Trung thực với ngữ cảnh): {avg_faithfulness:.1f}%")
    print(f"Answer Relevancy (Bám sát truy vấn): {avg_relevancy:.1f}%")
    print("=" * 60)
    
    report = f"""# Báo cáo Đánh giá Chất lượng Sinh văn bản (RAGAS)
    
- **Faithfulness**: {avg_faithfulness:.1f}%
- **Answer Relevancy**: {avg_relevancy:.1f}%

> *Đánh giá được thực hiện thông qua kỹ thuật LLM-as-a-Judge sử dụng Gemini 2.5 Flash.*
"""
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "benchmark_generation.md"), "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    asyncio.run(run_generation_eval())
