import time
from observer import observe
from reasoner import reason
from memory import load_memory, update_memory

def start_safe_loop():
    print("🛡️ CyberCipher Loop Active (Token-Safe Mode).")
    
    # --- FIXED STARTUP LOGIC ---
    # We only initialize the error count. 
    # We do NOT sync merchants to memory here, so they stay 'new' for your scan.
    initial_context = observe()
    last_processed_count = sum(e.get("count", 0) for e in initial_context.get("errors", []))
    print(f"Startup complete. Monitoring for new tickets and error spikes (Current base: {last_processed_count}).")
    # ---------------------------

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

        # Only trigger reasoning if there is a NEW ticket or errors go up
        if len(new_tickets) > 0 or error_count > last_processed_count:
            print(f"New signals detected! Processing {len(new_tickets)} new entries...")
            
            analysis = reason(context, memory)
            
            if analysis.get("confidence", 0) > 0.7:
                merchant_ids = [t["merchant_id"] for t in new_tickets]
                # Mark as 'pending_approval' so they show up in your App for review
                update_memory(merchant_ids, analysis, status="pending_approval")
                print(f"Recorded {len(merchant_ids)} merchants as pending approval.")
            
            last_processed_count = error_count
        else:
            # This will now only show if there are truly no new changes
            print("Signals unchanged. Skipping API call.")

        time.sleep(30) 

if __name__ == "__main__":
    start_safe_loop()