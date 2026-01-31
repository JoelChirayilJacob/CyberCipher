from tools import AgentTools
from actions import act
import json

# Simulate a LOW RISK decision that triggers auto-fix
simulated_decision = {
    "action_type": "AUTO_FIX",
    "tool": "fix_webhook_config",
    "requires_approval": False,
    "reason": "High confidence, low risk - safe to auto-execute",
    "recommended_action": "Auto-fix webhook configuration for merchant m5"
}

simulated_analysis = {
    "hypothesis": "Webhook URL format changed in headless migration",
    "root_cause": "migration_misconfiguration",
    "confidence": 0.95,
    "risk_level": "low",
    "recommended_action": "Fix webhook config for m5, m6",
    "affected_merchants_estimate": 2
}

print("=== DEMONSTRATING AUTO-FIX ===")
print(f"Decision: {simulated_decision['action_type']}")
print(f"Tool: {simulated_decision['tool']}")
print(f"Requires Approval: {simulated_decision['requires_approval']}")
print()

print("=== EXECUTING TOOL ===")
result = act(simulated_decision, simulated_analysis)

print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
print(f"\nTool Execution Result:")
print(json.dumps(result['tool_result'], indent=2))

print("\n=== DEMONSTRATING ESCALATION ===")
escalation_decision = {
    "action_type": "ESCALATE",
    "tool": "escalate_to_engineering",
    "requires_approval": True,
    "reason": "Risk level high requires human oversight",
    "recommended_action": "Escalate payment API issue to engineering"
}

result2 = act(escalation_decision, simulated_analysis)
print(f"Status: {result2['status']}")
print(f"Message: {result2['message']}")
