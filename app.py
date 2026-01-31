import streamlit as st
import pandas as pd
from observer import observe
from reasoner import reason
from actions import act
from memory import load_memory, update_memory 

# Rule: Prioritize Clarity. Use a clean, non-interactive title.
st.markdown("### 🛡️ CyberCipher | SaaS Migration Support")

if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []
if 'current_issue' not in st.session_state:
    st.session_state.current_issue = None
if 'action_status' not in st.session_state:
    st.session_state.action_status = None

# Button to trigger the agent loop
if st.button("Scan for New Migration Issues", type="primary"):
    with st.spinner("Analyzing signals and filtering known issues..."):
        # Load long-term memory to provide context and filter results
        memory = load_memory() 
        
        # 1. Observe all current signals
        context = observe() 
        
        # 2. Filter: Only identify merchants NOT in memory (includes 'pending' and 'resolved')
        # This prevents re-scanning issues that loop.py already caught.
        new_tickets = [
            t for t in context.get("tickets", []) 
            if t["merchant_id"] not in memory.get("helped_merchants", {})
        ]
        
        if new_tickets:
            # Only perform reasoning on brand new signals to save tokens
            new_context = {"tickets": new_tickets, "errors": context.get("errors", [])}
            analysis = reason(new_context, memory) 
            
            st.session_state.current_issue = analysis
            st.session_state.action_status = None  
            
            # Update UI Audit Log
            st.session_state.audit_log.append({
                "Root Cause": analysis["root_cause"],
                "Confidence": f"{analysis['confidence']*100:.0f}%",
                "Risk": analysis["risk_level"].upper()
            })
        else:
            st.session_state.current_issue = None
            st.success("No new issues detected. All current signals are already tracked in memory.")

# Display Logic for Active Issues
if st.session_state.current_issue:
    issue = st.session_state.current_issue
    st.markdown("---")
    
    # 1. Reasoning Chain (Transparency Rule)
    st.markdown("**Agent Reasoning Chain**")
    st.info(f"**Hypothesis:** {issue['hypothesis']}\n\n**Logic:** {issue['reasoning']}")
    
    # 2. Metrics (Clarity Rule)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Confidence Score:** {issue['confidence']*100:.0f}%")
        st.progress(issue['confidence']) 
    with col2:
        risk = issue["risk_level"].lower()
        color = "red" if risk == "high" else "orange" if risk == "medium" else "green"
        st.markdown(f"**Risk Level:** :{color}[{risk.upper()}]")
    
    # 3. Proposed Action
    st.markdown("**Proposed Action**")
    st.write(issue["recommended_action"])
    
    # 4. Human-in-the-Loop Buttons
    c1, c2 = st.columns([1, 4])
    
    if c1.button("Approve"):
        # Execute technical action
        act({"escalate": True, "action": issue["recommended_action"]})
        
        # UPDATE: Identify merchants and flip status to 'resolved'
        context = observe()
        current_merchants = [t["merchant_id"] for t in context.get("tickets", [])]
        
        # This is the "Feedback Loop" - confirming the agent was correct
        update_memory(current_merchants, issue, status="resolved") 
        
        st.session_state.action_status = "Action Approved & Resolved"
        
    if c2.button("Reject", type="primary"):
        st.session_state.action_status = "Action Rejected"

    if st.session_state.action_status:
        st.markdown(f"**{st.session_state.action_status}**")

# 5. Audit Log (Consistency Rule)
st.markdown("---")
st.markdown("**Decision History**")
if st.session_state.audit_log:
    st.table(pd.DataFrame(st.session_state.audit_log))

# 6. Memory Inspection (Auditability)
with st.expander("🛠️ Debug: View Agent Long-Term Memory"):
    st.json(load_memory())