import json
import os

MEMORY_FILE = "data/agent_memory.json"

def load_memory():
    """Reads the long-term memory file or creates a new one if it doesn't exist."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    if not os.path.exists(MEMORY_FILE):
        return {"helped_merchants": {}, "history": []}
    
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def update_memory(merchant_ids, analysis, status="pending_approval"):
    """
    Updates memory with a specific status.
    Statuses: 'pending_approval' (set by loop) or 'resolved' (set by app button).
    """
    memory = load_memory()
    
    # Store history of the reasoning
    entry = {
        "timestamp": "recent",
        "root_cause": analysis["root_cause"],
        "recommended_action": analysis["recommended_action"],
        "status": status
    }
    memory["history"].append(entry)

    # Track specific merchants with their current status
    for mid in merchant_ids:
        memory["helped_merchants"][mid] = {
            "last_issue": analysis["root_cause"],
            "last_action": analysis["recommended_action"],
            "status": status  # This tracks if the human has approved it yet
        }
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)