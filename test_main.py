from observer import observe
from reasoner import reason
from decision import decide
from actions import act

print("Starting agent...")

print("1. Observing...")
context = observe()
print(f"Context: {context}")

print("\n2. Reasoning...")
analysis = reason(context)
print(f"Analysis: {analysis}")

print("\n3. Deciding...")
decision_result = decide(analysis)
print(f"Decision: {decision_result}")

print("\n4. Acting...")
result = act(decision_result)
print(f"Result: {result}")

print("\n--- AGENT THINKING ---")
print(analysis)

print("\n--- AGENT DECISION ---")
print(result)
