"""
Reports View - Analytics and metrics
"""
import streamlit as st


def reports_view():
    """Display reports and analytics"""
    st.markdown("### Reports & Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_orders = len(st.session_state.orders)
        st.metric("Total Orders", total_orders)
    
    with col2:
        total_spend = sum(o['Total (EUR)'] for o in st.session_state.orders) if st.session_state.orders else 0
        st.metric("Total Spend", f"€{total_spend:.2f}")
    
    with col3:
        pending = len([o for o in st.session_state.orders if o['Status'] == 'Pending Approval'])
        st.metric("Pending Approvals", pending)
    
    st.markdown("---")
    st.info("Detailed reports and analytics coming soon...")

