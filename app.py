import streamlit as st
import pandas as pd
from observer import observe
from reasoner import reason
from decision import decide
from actions import act
from memory import load_memory, update_memory 

# Custom CSS to force specific button colors
st.markdown("""
    <style>
    /* Approve Button (Primary) - Green */
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        color: white;
        border: None;
    }
    /* Reject Button (Secondary/Standard) - Red */
    div.stButton > button[kind="secondary"] {
        background-color: #dc3545;
        color: white;
        border: None;
    }
    </style>
    """, unsafe_allow_html=True)

# Rule: Prioritize Clarity. Use a clean, non-interactive title.
st.markdown("### CyberCipher | SaaS Migration Support")

if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []
if 'current_issue' not in st.session_state:
    st.session_state.current_issue = None
if 'current_decision' not in st.session_state:
    st.session_state.current_decision = None
if 'action_status' not in st.session_state:
    st.session_state.action_status = None
if 'execution_result' not in st.session_state:
    st.session_state.execution_result = None

# Button to trigger the agent loop
if st.button("Scan for New Migration Issues", type="secondary"):
    with st.spinner("Analyzing signals and filtering known issues..."):
        memory = load_memory() 
        context = observe() 
        
        # --- UPDATED FILTER LOGIC ---
        # We find tickets that are either:
        # 1. Not in memory at all
        # 2. In memory but marked as 'pending_approval' (not yet resolved)
        new_tickets = [
            t for t in context.get("tickets", []) 
            if t["merchant_id"] not in memory.get("helped_merchants", {}) or 
            memory.get("helped_merchants", {}).get(t["merchant_id"], {}).get("status") == "pending_approval"
        ]
        
        if new_tickets:
            # Only perform reasoning on active (unresolved) signals
            new_context = {"tickets": new_tickets, "errors": context.get("errors", [])}
            analysis = reason(new_context, memory) 
            decision_result = decide(analysis)
            
            st.session_state.current_issue = analysis
            st.session_state.current_decision = decision_result
            st.session_state.action_status = None
            st.session_state.execution_result = None
            
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
    decision_result = st.session_state.current_decision
    st.markdown("---")
    
    # 1. Integrated Reasoning Box
    st.markdown("#### Agent Reasoning Chain")
    
    logic_points = issue['reasoning'].split(". ")
    formatted_logic = ""
    for point in logic_points:
        if point.strip():
            formatted_logic += f"\n- {point.strip().capitalize()}."

    st.info(
        f"**Hypothesis:** {issue['hypothesis']}  \n\n"
        f"**Key Findings:** \n{formatted_logic}"
    )
    
    # 2. Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Confidence Score:** {issue['confidence']*100:.0f}%")
        st.progress(issue['confidence']) 
    with col2:
        risk = issue["risk_level"].lower()
        color = "red" if risk == "high" else "orange" if risk == "medium" else "green"
        st.markdown(f"**Risk Level:** :{color}[{risk.upper()}]")
    with col3:
        if decision_result:
            st.markdown(f"**Action Type:** {decision_result['action_type']}")
            st.markdown(f"**Tool:** `{decision_result.get('tool', 'None')}`")
    
    # 3. Structured Proposed Action Plan
    st.markdown("#### Proposed Action Plan")
    action_steps = issue["recommended_action"].split(". ")
    for step in action_steps:
        if step.strip():
            st.markdown(f"* {step.strip()}")
    
    # 4. Human-in-the-Loop Buttons
    st.write("") 
    
    # Using 2 equal columns to ensure buttons are the same size
    c1, c2 = st.columns(2)
    
    is_action_taken = st.session_state.action_status is not None
    
    # Approve Button - Green via CSS + Primary Type
    if c1.button("Approve", type="primary", use_container_width=True, disabled=is_action_taken):
        with st.spinner("Executing action..."):
            execution_result = act(decision_result, issue)
            st.session_state.execution_result = execution_result
            
            context = observe()
            current_merchants = [t["merchant_id"] for t in context.get("tickets", [])]
            # Update memory to flip status from 'pending' to 'resolved'
            update_memory(current_merchants, issue, status="resolved") 
            
            st.session_state.action_status = "Action Approved & Resolved"
            st.rerun() 
        
    # Reject Button - Red via CSS + Secondary Type
    if c2.button("Reject", type="secondary", use_container_width=True, disabled=is_action_taken):
        st.session_state.action_status = "Action Rejected"
        st.session_state.execution_result = None
        st.rerun()

    # Status Feedback
    if st.session_state.action_status:
        if "Approved" in st.session_state.action_status:
            st.success(f"**{st.session_state.action_status}**")
        else:
            st.warning(f"**{st.session_state.action_status}**")


# 5. Audit Log
st.markdown("---")
st.markdown("**Decision History**")
if st.session_state.audit_log:
    st.table(pd.DataFrame(st.session_state.audit_log))

# 6. Memory Inspection
with st.expander("Debug: View Agent Long-Term Memory"):
    st.json(load_memory())