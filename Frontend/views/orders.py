"""
Orders View - Display order history
"""
import streamlit as st


def orders_view():
    """Display order history"""
    st.markdown("### Order History")
    
    if st.session_state.orders:
        for order in st.session_state.orders:
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
    else:
        st.info("No orders yet. Create a request or add products to your cart.")

