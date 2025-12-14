"""
Orders View - Display order history
"""
import streamlit as st
from config import ADMIN_PASSWORD


def orders_view():
    """Display order history"""
    st.markdown("### Order History")
    
    if st.session_state.orders:
        for idx, order in enumerate(st.session_state.orders):
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{order['Order ID']}**")
                    st.caption(f"{order['Date']} • {order['Requester']}")
                with col2:
                    st.markdown(f"€{order['Total (EUR)']:.2f}")
                with col3:
                    status = order['Status']
                    if status == "Pending Approval":
                        st.warning(status)
                    elif status in ["Auto-Approved", "Approved", "Admin Approved"]:
                        st.success(status)
                    elif status == "Order Declined":
                        st.error(status)
                    else:
                        st.info(status)
                
                # Show re-approve option for declined orders
                if order['Status'] == "Order Declined":
                    with st.expander("🔓 Admin Re-approval", expanded=False):
                        pwd_col, btn_col = st.columns([2, 1])
                        with pwd_col:
                            admin_pwd = st.text_input(
                                "Admin Password", 
                                type="password", 
                                key=f"reapprove_pwd_{order['Order ID']}_{idx}",
                                placeholder="Enter admin password"
                            )
                        with btn_col:
                            st.write("")  # Spacing
                            if st.button("✓ Re-approve", key=f"reapprove_btn_{order['Order ID']}_{idx}", type="primary"):
                                if admin_pwd == ADMIN_PASSWORD:
                                    # Update order status
                                    order['Status'] = "Admin Approved"
                                    # Add to reports for contract generation
                                    if order not in st.session_state.reports:
                                        st.session_state.reports.append(order)
                                    st.success("✅ Order re-approved!")
                                    st.rerun()
                                else:
                                    st.error("❌ Incorrect password")
    else:
        st.info("No orders yet. Create a request or add products to your cart.")

