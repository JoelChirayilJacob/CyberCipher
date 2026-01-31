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
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        color: white;
        border: None;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #dc3545;
        color: white;
        border: None;
    }
    div.stButton > button:not([kind="primary"]):not([kind="secondary"]) {
        background-color: #6c757d;
        color: white;
        border: None;
    }
    </style>
    """, unsafe_allow_html=True)

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
if 'new_signals_detected' not in st.session_state:
    st.session_state.new_signals_detected = False
if 'expand_approve' not in st.session_state:
    st.session_state.expand_approve = False
if 'expand_reject' not in st.session_state:
    st.session_state.expand_reject = False

memory = load_memory()
context = observe()
new_tickets_count = len([
    t for t in context.get("tickets", []) 
    if t["merchant_id"] not in memory.get("helped_merchants", {}) or 
    memory.get("helped_merchants", {}).get(t["merchant_id"], {}).get("status") == "pending_approval"
])

if new_tickets_count > 0 and not st.session_state.new_signals_detected:
    st.session_state.new_signals_detected = True

if st.session_state.new_signals_detected and new_tickets_count > 0:
    st.toast(f"{new_tickets_count} new signal(s) detected! Click 'Scan for New Migration Issues' to analyze.")
    with st.container():
        col_alert1, col_alert2 = st.columns([3, 1])
        with col_alert1:
            st.warning(f"**New Migration Signals Detected:** {new_tickets_count} unresolved issue(s) found.")

if st.button("Scan for New Migration Issues", type="secondary"):
    st.session_state.new_signals_detected = False
    with st.spinner("Analyzing signals and filtering known issues..."):
        memory = load_memory() 
        context = observe() 
        
        new_tickets = [
            t for t in context.get("tickets", []) 
            if t["merchant_id"] not in memory.get("helped_merchants", {}) or 
            memory.get("helped_merchants", {}).get(t["merchant_id"], {}).get("status") == "pending_approval"
        ]
        
        if new_tickets:
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

if st.session_state.current_issue:
    issue = st.session_state.current_issue
    decision_result = st.session_state.current_decision
    st.markdown("---")
    
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        confidence_value = float(issue.get('confidence', 0))
        st.markdown(f"**Confidence Score:** {confidence_value*100:.0f}%")
        st.progress(confidence_value) 
    with col2:
        risk_value = str(issue.get("risk_level", "unknown")).upper()
        color = "red" if risk_value == "HIGH" else "orange" if risk_value == "MEDIUM" else "green"
        st.markdown(f"**Risk Level:** :{color}[{risk_value}]")
    with col3:
        if decision_result:
            st.markdown(f"**Action Type:** {decision_result['action_type']}")
            st.markdown(f"**Tool:** `{decision_result.get('tool', 'None')}`")
    
    st.markdown("#### Proposed Action Plan")
    action_steps = issue["recommended_action"].split(". ")
    for step in action_steps:
        if step.strip():
            st.markdown(f"* {step.strip()}")
    
    st.write("") 
    
    is_action_taken = st.session_state.action_status is not None
    
    if not st.session_state.expand_approve and not st.session_state.expand_reject:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Approve", type="primary", use_container_width=True, disabled=is_action_taken, key="approve_btn"):
                st.session_state.expand_approve = True
                st.session_state.expand_reject = False
                st.rerun()
        with c2:
            if st.button("Reject", type="secondary", use_container_width=True, disabled=is_action_taken, key="reject_btn"):
                st.session_state.expand_reject = True
                st.session_state.expand_approve = False
                st.rerun()
    
    elif st.session_state.expand_approve:
        st.success("**Approve this action?**")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("Confirm", type="primary", use_container_width=True, key="approve_confirm"):
                with st.spinner("Executing action..."):
                    execution_result = act(decision_result, issue)
                    st.session_state.execution_result = execution_result
                    
                    context = observe()
                    current_merchants = [t["merchant_id"] for t in context.get("tickets", [])]
                    update_memory(current_merchants, issue, status="resolved") 
                    
                    st.session_state.action_status = "Action Approved & Resolved"
                    st.session_state.expand_approve = False
                    st.rerun()
        with col_cancel:
            if st.button("Cancel", type="secondary", use_container_width=True, key="approve_cancel"):
                st.session_state.expand_approve = False
                st.rerun()
    
    elif st.session_state.expand_reject:
        st.warning("**Reject this action?**")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("Confirm", type="primary", use_container_width=True, key="reject_confirm"):
                st.session_state.action_status = "Action Rejected"
                st.session_state.execution_result = None
                st.session_state.expand_reject = False
                st.rerun()
        with col_cancel:
            if st.button("Cancel", type="secondary", use_container_width=True, key="reject_cancel"):
                st.session_state.expand_reject = False
                st.rerun()

    if st.session_state.action_status:
        if "Approved" in st.session_state.action_status:
            st.success(f"**{st.session_state.action_status}**")
        else:
            st.warning(f"**{st.session_state.action_status}**")


st.markdown("---")
st.markdown("**Decision History**")
if st.session_state.audit_log:
    st.table(pd.DataFrame(st.session_state.audit_log))

with st.expander("Debug: View Agent Long-Term Memory"):
    st.json(load_memory())