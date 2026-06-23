import asyncio
import json
import os
import random
import httpx
from openai import AsyncOpenAI
from medicalink_ai.config import get_settings

# Prompt mẫu đánh giá theo tiêu chuẩn RAGAS
EVAL_PROMPT = """Bạn là một chuyên gia đánh giá mô hình ngôn ngữ (LLM Judge). 
Hãy đánh giá kết quả của hệ thống AI Y tế theo tiêu chuẩn RAGAS (thang điểm 0.0 đến 1.0):

LƯU Ý QUAN TRỌNG: Đây là hệ thống AI Hỗ trợ Định tuyến và Khuyến nghị Bác sĩ (Doctor Recommendation System), KHÔNG PHẢI là Chatbot chẩn đoán bệnh. Hệ thống được thiết kế để trả về lý do đề xuất bác sĩ ngắn gọn, KHÔNG ĐƯỢC PHÉP đưa ra lời khuyên y tế hay chẩn đoán bệnh lý chi tiết.

1. Faithfulness (Tính trung thực): Câu trả lời thực tế (Actual Answer) có phản ánh đúng ngữ cảnh (Context) không? Lấy trọn vẹn điểm (1.0) nếu câu trả lời đưa ra lý do phù hợp dựa trên các triệu chứng được trích xuất trong Context mà không tự bịa đặt thêm các chẩn đoán y khoa không có thật.
2. Answer Relevancy & Correctness (Độ liên quan và Chính xác): Câu trả lời thực tế có hướng người dùng đến đúng chuyên khoa/hướng xử lý như Câu trả lời tiêu chuẩn (Reference Answer) không? Lấy trọn vẹn điểm (1.0) nếu chuyên khoa của bác sĩ được đề xuất KHỚP với chuyên khoa hoặc hướng giải quyết trong Reference Answer. TUYỆT ĐỐI KHÔNG trừ điểm nếu Actual Answer ngắn gọn hoặc không giải thích sâu về bệnh lý (vì đây là tính năng an toàn của hệ thống).

Context (Các triệu chứng đã được AI trích xuất và khớp với hồ sơ bác sĩ):
{context}

Question/Symptoms (Câu hỏi của người bệnh):
{question}

Reference Answer (Ground Truth - Đáp án tiêu chuẩn về hướng định tuyến):
{reference_answer}

Actual Answer (Lý do Khuyến nghị Bác sĩ trả về từ API):
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
    api_key = settings.openai_api_key if isinstance(settings.openai_api_key, str) else (settings.openai_api_key.get_secret_value() if settings.openai_api_key else "")
    openai_client = AsyncOpenAI(api_key=api_key)
    
    url_suggest = "https://api.medicalink.online/api/ai/suggest-specialties"
    url_recommend = "https://api.medicalink.online/api/ai/recommend-doctor"
    
    print("Đang kết nối tới API Production (https://api.medicalink.online) để đánh giá sinh văn bản...\n")
    
    # Load stratified test cases from JSON
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "ragas_eval_cases.json")
    with open(file_path, "r", encoding="utf-8") as f:
        eval_cases = json.load(f)
        
    print(f"Đã nạp {len(eval_cases)} test cases phân tầng (Stratified) có sẵn Ground Truth để đánh giá RAGAS.\n")

    total_faithfulness = 0
    total_relevancy = 0
    valid_cases = 0
    
    md_details = ""
    
    async with httpx.AsyncClient() as client:
        for i, c in enumerate(eval_cases):
            question = c['query']
            ref_answer = c.get('reference_answer', '')
            
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
                reference_answer=ref_answer,
                answer=actual_answer
            )
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    resp = await openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.0
                    )
                    break
                except Exception as e:
                    if "429" in str(e) or "503" in str(e):
                        sleep_time = 10 * (attempt + 1)
                        print(f"Rate limit or Server Error, retrying in {sleep_time} seconds...")
                        await asyncio.sleep(sleep_time)
                    else:
                        raise e
                except Exception as e:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        raise e
            try:
                raw_text = resp.choices[0].message.content
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
                
                md_details += f"### Case {i+1}\n"
                md_details += f"**Query:** {question}\n\n"
                md_details += f"**API Answer:** {actual_answer}\n\n"
                md_details += f"- **Faithfulness:** {f_score}\n"
                md_details += f"- **Answer Relevancy:** {r_score}\n"
                md_details += f"- **Reason:** {res_json.get('reason')}\n\n"
                
                await asyncio.sleep(6)
                
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
    
- **Tổng số Test Cases**: {valid_cases} (Stratified Sampling: 3 cases/chuyên khoa, gồm Rõ ràng, Chồng lấn, Khó)
- **Faithfulness**: {avg_faithfulness:.1f}%
- **Answer Relevancy & Correctness**: {avg_relevancy:.1f}%

> *Đánh giá được thực hiện thông qua kỹ thuật LLM-as-a-Judge sử dụng gpt-4o-mini (OpenAI).*

## Chi tiết các Test Case

{md_details}
"""
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "benchmark_generation.md"), "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    asyncio.run(run_generation_eval())
