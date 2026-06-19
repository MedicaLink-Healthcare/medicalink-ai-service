import asyncio
import os
import json
from dotenv import load_dotenv
load_dotenv()

from medicalink_ai.gemini_llm import generate_json_with_gemini

SYSTEM = """You are an expert Medical Triage AI. Your goal is to extract structured medical symptoms from patient descriptions.
You must output JSON matching this structure:
{
  "is_medical_query": bool,
  "symptoms": [string],
  "negated_symptoms": [string],
  "patient_demographic": string,
  "duration": string,
  "severity": "low" | "medium" | "high",
  "common_priors": [string],
  "dangerous_priors": [string],
  "clarification_question": string,
  "triage_level": "routine" | "urgent" | "critical",
  "urgency_score": float (0.0 to 1.0),
  "note": string,
  "emergency_reason": string
}
Rules:
1. "is_medical_query": false if completely unrelated to health/medicine/booking (e.g. "thời tiết", "chào bạn", "cách nấu ăn", "Trời hôm nay quá đẹp").
"""

async def main():
    api_key = os.environ.get("GOOGLE_GENAI_API_KEY")
    model = "gemini-2.5-flash"
    prompt = "Patient description:\ntôi muốn khám bệnh"
    res = await generate_json_with_gemini(api_key=api_key, model=model, system_instruction=SYSTEM, user_content=prompt, timeout_ms=10000, temperature=0.0)
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
