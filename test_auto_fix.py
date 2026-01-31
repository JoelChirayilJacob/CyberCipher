from observer import observe
from reasoner import reason
from decision import decide
from actions import act
import json

# Override to use low-risk scenario
def load_events():
    with open("data/low_risk_scenario.json") as f:
        return json.load(f)

events = load_events()
tickets = [e for e in events if e["type"] == "support_ticket"]
errors = [e for e in events if e["type"] == "platform_error"]

context = {
    "tickets": tickets,
    "errors": errors
}

print("Testing with LOW RISK scenario...\n")

analysis = reason(context)
decision_result = decide(analysis)

print("\n=== AGENT THINKING ===")
print(f"Hypothesis: {analysis['hypothesis']}")
print(f"Root Cause: {analysis['root_cause']}")
print(f"Confidence: {analysis['confidence']*100:.0f}%")
print(f"Risk Level: {analysis['risk_level'].upper()}")

print("\n=== AGENT DECISION ===")
print(f"Action Type: {decision_result['action_type']}")
print(f"Tool: {decision_result.get('tool', 'None')}")
print(f"Approval Required: {decision_result.get('requires_approval', False)}")

# Execute if no approval needed
if not decision_result.get('requires_approval'):
    print("\n=== AUTO-EXECUTING ===")
    result = act(decision_result, analysis)
    print(f"{result['message']}")
    if result.get('tool_result'):
        print(f"\nTool Details: {json.dumps(result['tool_result'], indent=2)}")
else:
    print("\n=== NEEDS APPROVAL ===")
    result = act(decision_result, analysis)
    print(result['message'])
