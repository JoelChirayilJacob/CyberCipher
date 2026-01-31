import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = """
You are an agentic AI for SaaS migration support.

Detect patterns across signals.
Infer root cause.
Estimate impact.
Recommend safe actions.

Root cause must be one of:
migration_misconfiguration
platform_regression
documentation_gap
merchant_error
unknown

INPUT SIGNALS:
{signals}

Return ONLY valid JSON:
{{
  "hypothesis": "",
  "root_cause": "",
  "confidence": 0.0,
  "affected_merchants_estimate": 0,
  "reasoning": "",
  "recommended_action": "",
  "risk_level": "low|medium|high"
}}
"""


def reason(context):
    try:
        filled_prompt = PROMPT.format(
            signals=json.dumps(context, indent=2)
        )
        
        print("[DEBUG] Calling Gemini API...")
        
        # Use strict JSON mode
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=filled_prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        print(f"[DEBUG] Got response!")
        
        # With JSON mode, response is already clean JSON
        return json.loads(response.text)
    
    except Exception as e:
        print(f"[ERROR] Reasoning failed: {e}")
        # Return fallback
        return {
            "hypothesis": "API Error",
            "root_cause": "unknown",
            "confidence": 0.0,
            "affected_merchants_estimate": 0,
            "reasoning": str(e),
            "recommended_action": "Manual review needed",
            "risk_level": "high"
        }
