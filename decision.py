def decide(analysis):
    """
    Decide which action to take based on:
    - Confidence level
    - Risk level
    - Root cause type
    """
    
    confidence = analysis["confidence"]
    risk = analysis["risk_level"]
    root_cause = analysis["root_cause"]
    recommended = analysis["recommended_action"].lower()
    
    # HIGH CONFIDENCE + LOW RISK = Auto-fix
    if confidence >= 0.9 and risk == "low":
        if "webhook" in recommended:
            return {
                "action_type": "AUTO_FIX",
                "tool": "fix_webhook_config",
                "requires_approval": False,
                "reason": "High confidence, low risk - safe to auto-execute",
                "recommended_action": analysis["recommended_action"]
            }
        else:
            return {
                "action_type": "AUTO_FIX",
                "tool": "apply_temporary_fix",
                "requires_approval": False,
                "reason": "High confidence, low risk - safe to auto-execute",
                "recommended_action": analysis["recommended_action"]
            }
    
    # MEDIUM-HIGH CONFIDENCE + MEDIUM/HIGH RISK = Escalate
    elif confidence >= 0.7 and risk in ["medium", "high"]:
        return {
            "action_type": "ESCALATE",
            "tool": "escalate_to_engineering",
            "requires_approval": True,
            "reason": f"Risk level {risk} requires human oversight",
            "recommended_action": analysis["recommended_action"]
        }
    
    # DOCUMENTATION GAP = Update docs + notify
    elif root_cause == "documentation_gap":
        return {
            "action_type": "UPDATE_DOCS",
            "tool": "update_documentation",
            "requires_approval": True,
            "reason": "Documentation needs improvement",
            "recommended_action": analysis["recommended_action"]
        }
    
    # LOW CONFIDENCE = Monitor only
    else:
        return {
            "action_type": "MONITOR",
            "tool": None,
            "requires_approval": False,
            "reason": "Insufficient confidence - collecting more data",
            "recommended_action": "Waiting for more signals"
        }
