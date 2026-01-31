import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

context = {
    "tickets": [
        {"merchant_id": "m1", "error": "401 payment API"}
    ]
}

SIMPLE_PROMPT = f"""
Analyze this support data and respond in JSON:
{json.dumps(context)}

Return exactly this format:
{{"root_cause": "migration_misconfiguration", "confidence": 0.8}}
"""

print("Testing reasoner...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=SIMPLE_PROMPT
)

print(f"Response: {response.text}")
