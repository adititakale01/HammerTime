"""
Reusable UI components: sidebar, order summary, product description
"""
import streamlit as st
from utils import calculate_total, place_order, navigate_to


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("## Procurement Assistant")
        st.markdown("---")
        
        pages = [
            ("🏠", "Dashboard"),
            ("📋", "Orders"),
            ("📊", "Reports")
        ]
        
        for icon, page in pages:
            is_active = st.session_state.current_page == page
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True, type=btn_type):
                navigate_to(page)
                st.rerun()
        
        st.markdown("---")
        st.caption("Hackathon Demo v2.0")


def render_order_summary():
    """Render the order summary component"""
    st.markdown("### Order Summary")
    
    if not st.session_state.cart:
        st.markdown("*Your cart is empty*")
        return
    
    for item in st.session_state.cart:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
            st.caption(f"{item['qty']} pcs")
        with col2:
            subtotal = item['price'] * item['qty']
            st.markdown(f"€{subtotal:.2f}")
    
    st.markdown("---")
    
    total = calculate_total()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Total**")
    with col2:
        st.markdown(f"**€{total:.2f}**")
    
    st.markdown("")
    
    if st.button("Place order", type="primary", use_container_width=True):
        status = place_order()
        if status == "Pending Approval":
            st.info(f"Order sent for approval")
        else:
            st.success(f"Order placed successfully!")
        st.rerun()


def render_product_description(product):
    """Render product description card"""
    st.markdown("### Product Description")
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 2rem;">{product.get('icon', '🔩')}</span>
        <div>
            <div style="font-weight: 600; color: #1E3A5F;">{product['name']}</div>
            <div style="color: #64748B; font-size: 0.9rem;">{product['description']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

