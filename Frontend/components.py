"""
Reusable UI components: sidebar, order summary, product description
"""
import streamlit as st
from utils import calculate_total, place_order, navigate_to
from config import AUTO_APPROVAL_LIMIT, ADMIN_PASSWORD


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        
        pages = [
            ("", "Dashboard"),
            ("", "Orders"),
            ("", "Reports")
        ]
        
        for icon, page in pages:
            is_active = st.session_state.current_page == page
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True, type=btn_type):
                navigate_to(page)
                st.rerun()
        
        st.markdown("---")
        st.caption("Hackathon Demo v2.0", text_alignment="center")


def render_order_summary(key_prefix="default"):
    """Render the order summary component"""
    st.markdown("### Order Summary")
    
    # Show last order status banner if cart is empty
    if not st.session_state.cart:
        last_status = st.session_state.get('last_order_status')
        if last_status:
            if last_status == "Order Declined":
                st.markdown("""
                <div style="background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%); 
                            border: 2px solid #EF4444; border-radius: 12px; padding: 1.5rem; 
                            text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">❌</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #DC2626;">Order Declined</div>
                    <div style="font-size: 0.85rem; color: #991B1B; margin-top: 0.25rem;">
                        Admin can re-approve in Orders tab
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif last_status in ["Auto-Approved", "Admin Approved"]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%); 
                            border: 2px solid #10B981; border-radius: 12px; padding: 1.5rem; 
                            text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">✅</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #059669;">{last_status}</div>
                    <div style="font-size: 0.85rem; color: #047857; margin-top: 0.25rem;">
                        View in Orders & Reports tabs
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Button to clear status and start fresh
            if st.button("🛒 New Order", use_container_width=True, key=f"{key_prefix}_new_order_btn"):
                st.session_state.last_order_status = None
                st.rerun()
        else:
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
    
    # Show approval status
    requires_approval = total > AUTO_APPROVAL_LIMIT
    
    if requires_approval:
        st.warning(f"⚠️ Requires admin approval (over €{AUTO_APPROVAL_LIMIT})")
        admin_password = st.text_input(
            "Admin Password",
            type="password",
            placeholder="Enter admin password to approve",
            key=f"{key_prefix}_admin_password_input_{st.session_state.cart_version}"
        )
    else:
        st.success(f"✓ Auto-approved (under €{AUTO_APPROVAL_LIMIT})")
        admin_password = None
    
    st.markdown("")
    
    if st.button("Place order", type="primary", use_container_width=True, key=f"{key_prefix}_place_order_btn_{st.session_state.cart_version}"):
        if requires_approval:
            if admin_password == ADMIN_PASSWORD:
                status = place_order(custom_status="Admin Approved")
                st.session_state.last_order_status = "Admin Approved"
                st.rerun()
            elif admin_password:  # Wrong password entered
                status = place_order(custom_status="Order Declined")
                st.session_state.last_order_status = "Order Declined"
                st.rerun()
            else:  # No password entered
                st.warning("⚠️ Please enter admin password to place this order.")
        else:
            status = place_order()
            st.session_state.last_order_status = "Auto-Approved"
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


def render_chat_message(role, content):
    """Render a single chat message bubble"""
    # Convert newlines and bullet points to HTML
    formatted_content = content.replace('\n', '<br>').replace('• ', '<br>• ')
    # Clean up any double line breaks at the start
    if formatted_content.startswith('<br>'):
        formatted_content = formatted_content[4:]
    
    if role == "user":
        # User message - right aligned, blue
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
            <div style="background-color: #2563EB; color: white; padding: 0.75rem 1rem; border-radius: 12px 12px 0 12px; max-width: 80%;">
                {formatted_content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Assistant message - left aligned, gray
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
            <div style="background-color: #F1F5F9; color: #1E3A5F; padding: 0.75rem 1rem; border-radius: 12px 12px 12px 0; max-width: 80%; border: 1px solid #E2E8F0; line-height: 1.5;">
                {formatted_content}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_chat_history():
    """Render the full chat history"""
    for msg in st.session_state.voice_chat_messages:
        render_chat_message(msg["role"], msg["content"])

