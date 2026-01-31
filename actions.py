from tools import AgentTools
import re

# Initialize tools
agent_tools = AgentTools()

def extract_merchant_ids(text):
    """Extract merchant IDs from text (e.g., 'm1', 'm2')"""
    matches = re.findall(r'\bm\d+\b', text.lower())
    return matches if matches else ["m1"]  # Default to m1 if none found

def act(decision, analysis=None):
    """
    Execute the action based on decision
    Returns execution result
    """
    
    action_type = decision.get("action_type")
    tool_name = decision.get("tool")
    
    # If no tool needed (MONITOR mode)
    if not tool_name:
        return {
            "status": "monitoring",
            "message": "Waiting for more data before taking action",
            "action_type": action_type
        }
    
    # If requires approval and not approved yet
    if decision.get("requires_approval"):
        return {
            "status": "pending_approval",
            "message": f"PROPOSED ACTION: {decision['recommended_action']} (needs approval)",
            "action_type": action_type,
            "tool": tool_name
        }
    
    # Execute the tool
    try:
        if tool_name == "fix_webhook_config":
            # Extract merchant IDs from analysis
            if analysis:
                merchant_ids = extract_merchant_ids(str(analysis))
                merchant_id = merchant_ids[0] if merchant_ids else "m1"
            else:
                merchant_id = "m1"
            
            result = agent_tools.fix_webhook_config(merchant_id)
            
        elif tool_name == "notify_merchant":
            if analysis:
                merchant_ids = extract_merchant_ids(str(analysis))
                merchant_id = merchant_ids[0] if merchant_ids else "m1"
                message = analysis.get("recommended_action", "Issue detected")
            else:
                merchant_id = "m1"
                message = "Issue detected"
            
            result = agent_tools.notify_merchant(merchant_id, message)
            
        elif tool_name == "escalate_to_engineering":
            if analysis:
                affected = extract_merchant_ids(str(analysis))
                summary = analysis.get("hypothesis", "Unknown issue")
                severity = analysis.get("risk_level", "medium")
            else:
                affected = ["m1"]
                summary = "Unknown issue"
                severity = "medium"
            
            result = agent_tools.escalate_to_engineering(
                issue_summary=summary,
                affected_merchants=affected,
                severity=severity
            )
            
        elif tool_name == "update_documentation":
            section = "headless_migration"
            content = decision.get("recommended_action", "")
            result = agent_tools.update_documentation(section, content)
            
        elif tool_name == "apply_temporary_fix":
            if analysis:
                merchant_ids = extract_merchant_ids(str(analysis))
                merchant_id = merchant_ids[0] if merchant_ids else "m1"
            else:
                merchant_id = "m1"
            
            fix_type = "api_key_reset"
            result = agent_tools.apply_temporary_fix(merchant_id, fix_type)
            
        else:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}
        
        return {
            "status": "executed",
            "action_type": action_type,
            "tool_result": result,
            "message": f"Successfully executed {tool_name}"
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "action_type": action_type,
            "error": str(e),
            "message": f"Failed to execute {tool_name}: {str(e)}"
        }
