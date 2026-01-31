import streamlit as st
import pandas as pd
from observer import observe
from reasoner import reason
from actions import act

# Rule: Prioritize Clarity. Use a clean, non-interactive title.
st.markdown("SaaS Migration Support")

if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []
if 'current_issue' not in st.session_state:
    st.session_state.current_issue = None
if 'action_status' not in st.session_state:
    st.session_state.action_status = None

# Button to trigger the agent loop
if st.button("Scan for Migration Issues", type="primary"):
    with st.spinner("Analyzing signals..."):
        context = observe()
        analysis = reason(context)
        st.session_state.current_issue = analysis
        st.session_state.action_status = None  # Reset status for new scan
        
        # Update Audit Log
        st.session_state.audit_log.append({
            "Root Cause": analysis["root_cause"],
            "Confidence": f"{analysis['confidence']*100:.0f}%",
            "Risk": analysis["risk_level"].upper()
        })

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
    with col2:
        risk = issue["risk_level"].lower()
        color = "red" if risk == "high" else "orange" if risk == "medium" else "green"
        st.markdown(f"**Risk Level:** :{color}[{risk.upper()}]")
    
    # 3. Proposed Action (Displayed as a paragraph)
    st.markdown("**Proposed Action**")
    st.write(issue["recommended_action"])
    
    # 4. Human-in-the-Loop Buttons (Interchanged Colors)
    # Approve is now default (grey/dark), Reject is now 'primary' (red/highlighted)
    c1, c2 = st.columns([1, 4])
    
    if c1.button("Approve"):
        # Executes backend logic without reprinting the full text
        act({"escalate": True, "action": issue["recommended_action"]})
        st.session_state.action_status = "Action Approved"
        
    if c2.button("Reject", type="primary"):
        st.session_state.action_status = "Action Rejected"

    # 5. Simple Feedback Message
    if st.session_state.action_status:
        st.markdown(f"**{st.session_state.action_status}**")

# 6. Audit Log (Consistency Rule)
st.markdown("---")
st.markdown("**Decision History**")
if st.session_state.audit_log:
    st.table(pd.DataFrame(st.session_state.audit_log))