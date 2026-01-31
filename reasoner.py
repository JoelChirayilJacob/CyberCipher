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
    filled_prompt = PROMPT.format(
        signals=json.dumps(context, indent=2)
    )

    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents=filled_prompt
    )

    return json.loads(response.text)
