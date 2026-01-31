import time
from observer import observe
from reasoner import reason
from memory import load_memory, update_memory

def start_safe_loop():
    print("CyberCipher Loop Active (Token-Safe Mode).")
    # Initialize count to current state to avoid immediate trigger on startup
    initial_context = observe()
    last_processed_count = sum(e.get("count", 0) for e in initial_context.get("errors", []))

    while True:
        context = observe()
        memory = load_memory()
        
        # 1. Check for New Merchants
        active_tickets = context.get("tickets", [])
        new_tickets = [
            t for t in active_tickets 
            if t["merchant_id"] not in memory.get("helped_merchants", {})
        ]

        # 2. Check for ANY increase in Error Count
        error_count = sum(e.get("count", 0) for e in context.get("errors", []))

        # UPDATED GUARDRAIL: 
        # Triggers if there is AT LEAST 1 new ticket OR any increase in error count
        if len(new_tickets) > 0 or error_count > last_processed_count:
            print(f"New signals detected! Processing {len(new_tickets)} new merchant(s) or error spike.")
            
            # Pass memory to reasoner so it can check for patterns in history
            analysis = reason(context, memory)
            
            if analysis.get("confidence", 0) > 0.7:
                # Use only the IDs of the merchants that aren't already in memory
                merchant_ids = [t["merchant_id"] for t in new_tickets]
                
                # Mark as 'pending_approval' to claim the issue and save tokens
                update_memory(merchant_ids, analysis, status="pending_approval")
                
                print(f"Recorded {len(merchant_ids)} merchants as pending approval.")
            
            # Update the count to the new total to reset the trigger
            last_processed_count = error_count
        else:
            print("Signals unchanged. Skipping API call to save tokens.")

        # Sleep timer for testing
        time.sleep(30) 

if __name__ == "__main__":
    start_safe_loop()