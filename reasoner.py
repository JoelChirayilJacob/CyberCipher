import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# IMPROVED PROMPT: Directs the AI to perform pattern recognition between memory and new signals
PROMPT = """
You are an autonomous AI Agent for SaaS migration support.

CORE OBJECTIVES:
1. Pattern Recognition: Compare current {signals} against AGENT MEMORY {memory}.
2. Feedback Loop: If a root cause was previously identified for a similar signal, reinforce or adjust the hypothesis.
3. Impact Analysis: Determine how many merchants are affected by the current pattern.

Root cause categories:
- migration_misconfiguration
- platform_regression
- documentation_gap
- merchant_error
- unknown

INSTRUCTIONS:
- Search AGENT MEMORY for previous actions taken for these merchant_ids.
- If the current error matches a historical trend, explain this in the 'reasoning' field.
- Ensure the 'recommended_action' is specific and actionable based on the detected root cause.
- Set 'confidence' as a decimal between 0.0 and 1.0:
  * 0.0-0.3: Very uncertain, conflicting signals
  * 0.3-0.5: Low confidence, needs more data
  * 0.5-0.7: Moderate confidence, some evidence
  * 0.7-0.9: High confidence, strong evidence
  * 0.9-1.0: Very high confidence, clear pattern or historical match

Return ONLY valid JSON:
{{
  "hypothesis": "Short summary of what is happening",
  "root_cause": "Select from categories above",
  "confidence": 0.85,
  "affected_merchants_estimate": 0,
  "reasoning": "Detailed explanation linking current signals to past memory",
  "recommended_action": "Specific fix or escalation step",
  "risk_level": "low|medium|high"
}}
"""

def reason(context, memory):
    """
    Analyzes current migration signals using historical memory to identify root causes.
    """
    try:
        # Fulfills the 'Learning from previous actions' requirement by injecting history
        filled_prompt = PROMPT.format(
            signals=json.dumps(context, indent=2),
            memory=json.dumps(memory, indent=2)
        )
        
        print(f"[DEBUG] Reasoning cycle started for {len(context.get('tickets', []))} merchants.")
        
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=filled_prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        print("[DEBUG] Reasoning complete. State updated.")
        return json.loads(response.text)
    
    except Exception as e:
        print(f"[ERROR] Agent reasoning failed: {e}")
        return {
            "hypothesis": "System degradation",
            "root_cause": "unknown",
            "confidence": 0.0,
            "affected_merchants_estimate": 0,
            "reasoning": f"Critical failure in reasoning module: {str(e)}",
            "recommended_action": "Restart agent services and check API quotas",
            "risk_level": "high"
        }