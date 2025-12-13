"""
Image Search View - Analyze images (handwritten lists or photos of parts)
"""
import streamlit as st
import requests
import base64
from config import API_BASE_URL
from components import render_chat_message, render_order_summary
from utils import add_to_cart


def process_image_response():
    """Call the AI backend to analyze the image and process the response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze_image",
            json={
                "image_base64": st.session_state.image_uploaded_data["base64"],
                "media_type": st.session_state.image_uploaded_data["media_type"],
                "messages": st.session_state.image_chat_messages
            }
        )
        
        if response.ok:
            result = response.json()
            
            if result["type"] == "question":
                st.session_state.image_chat_messages.append({
                    "role": "assistant",
                    "content": result["content"]
                })
            elif result["type"] == "recommendations":
                st.session_state.image_chat_recommendations = result["content"]
                explanation = result["content"].get("explanation", "Here are my recommendations:")
                st.session_state.image_chat_messages.append({
                    "role": "assistant",
                    "content": f"✅ {explanation}"
                })
            elif result["type"] == "error":
                st.session_state.image_chat_messages.append({
                    "role": "assistant",
                    "content": f"❌ Error: {result['content']}"
                })
        else:
            st.session_state.image_chat_messages.append({
                "role": "assistant",
                "content": f"❌ Backend Error: {response.status_code}"
            })
    except Exception as e:
        st.session_state.image_chat_messages.append({
            "role": "assistant",
            "content": f"❌ Could not connect to backend: {e}"
        })
    
    st.session_state.image_chat_pending = False


def add_user_message(user_message: str):
    """Add user message to chat and set pending flag"""
    st.session_state.image_chat_messages.append({
        "role": "user",
        "content": user_message
    })
    st.session_state.image_chat_pending = True


def image_search_view():
    """Image search view with upload and chat-based analysis"""
    
    # Two column layout
    main_col, summary_col = st.columns([3, 1])
    
    with main_col:
        st.markdown("### 📷 Image Search")
        st.caption("Upload a handwritten list or photo of parts. AI will analyze and help you order.")
        
        # Image Upload Section
        with st.container(border=True):
            uploaded_file = st.file_uploader(
                "Upload Image",
                type=["png", "jpg", "jpeg"],
                label_visibility="collapsed",
                key="image_uploader"
            )
            
            if uploaded_file is not None:
                # Store image data
                image_bytes = uploaded_file.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                # Determine media type
                if uploaded_file.type:
                    media_type = uploaded_file.type
                else:
                    ext = uploaded_file.name.split('.')[-1].lower()
                    media_type = f"image/{ext}" if ext in ['png', 'jpg', 'jpeg'] else "image/jpeg"
                
                # Check if this is a new image
                if (st.session_state.image_uploaded_data is None or 
                    st.session_state.image_uploaded_data.get("base64") != image_base64):
                    st.session_state.image_uploaded_data = {
                        "base64": image_base64,
                        "media_type": media_type,
                        "name": uploaded_file.name
                    }
                    # Reset chat for new image
                    st.session_state.image_chat_messages = []
                    st.session_state.image_chat_recommendations = None
                
                # Show uploaded image
                col_img, col_action = st.columns([2, 1])
                
                with col_img:
                    st.image(image_bytes, caption=uploaded_file.name, use_container_width=True)
                
                with col_action:
                    st.markdown("**Ready to analyze!**")
                    st.caption("Click below to have AI analyze your image.")
                    
                    if st.button("🔍 Analyze Image", type="primary", use_container_width=True, key="analyze_btn"):
                        # Start analysis with initial message
                        st.session_state.image_chat_messages = [{
                            "role": "user",
                            "content": "Please analyze this image and identify what materials I need to order."
                        }]
                        st.session_state.image_chat_pending = True
                        st.rerun()
        
        # Chat History
        if st.session_state.image_chat_messages:
            st.markdown("---")
            st.markdown("### 💬 Conversation")
            
            for msg in st.session_state.image_chat_messages:
                render_chat_message(msg["role"], msg["content"])
            
            # Process pending AI response
            if st.session_state.image_chat_pending:
                with st.spinner("🤖 AI is analyzing..."):
                    process_image_response()
                st.rerun()
            
            # Text input for follow-up
            st.markdown("---")
            user_input = st.text_input(
                "Reply to AI",
                placeholder="e.g., 'I need the 5x60mm ones' or 'Yes, 10 of each'",
                key="image_chat_text_input",
                label_visibility="collapsed"
            )
            
            col_send, col_clear = st.columns([1, 1])
            
            with col_send:
                if st.button("📤 Send", key="image_chat_send", use_container_width=True):
                    if user_input and user_input.strip():
                        add_user_message(user_input.strip())
                        st.rerun()
            
            with col_clear:
                if st.button("🗑️ Clear", key="image_chat_clear", use_container_width=True):
                    st.session_state.image_chat_messages = []
                    st.session_state.image_chat_recommendations = None
                    st.session_state.image_chat_pending = False
                    st.session_state.image_uploaded_data = None
                    st.rerun()
        
        # Show Recommendations
        if st.session_state.image_chat_recommendations:
            st.markdown("---")
            st.markdown("### 📦 Recommended Materials")
            
            recommendations = st.session_state.image_chat_recommendations
            items = recommendations.get("items", [])
            
            if items:
                for item in items:
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 0.8, 0.8])
                    
                    with col1:
                        is_preferred = item.get('is_preferred', False)
                        supplier = item.get('lieferant', '')
                        kategorie = item.get('kategorie', '')
                        st.markdown(f"**{item.get('artikelname', item.get('artikel_id', 'Unknown'))}**")
                        if is_preferred:
                            st.markdown(f"""
                            <span style="color: #64748B; font-size: 0.875rem;">{kategorie} | </span>
                            <span style="display: inline-block; background: #FEF2F2; border: 1.5px solid #EF4444; border-radius: 4px; padding: 1px 6px; font-size: 0.75rem; color: #DC2626; font-weight: 600;">⭐ {supplier}</span>
                            """, unsafe_allow_html=True)
                        else:
                            st.caption(f"{kategorie} | {supplier}")
                    
                    with col2:
                        st.markdown(f"Qty: **{item.get('anzahl', 0)}**")
                        lead_time = item.get('lead_time_days', 7)
                        st.caption(f"🚚 {lead_time}d lead")
                    
                    with col3:
                        # Show inventory status
                        stock = item.get('lagerbestand', 0)
                        qty_needed = item.get('anzahl', 0)
                        needs = item.get('needs_order', qty_needed)
                        if stock >= qty_needed:
                            st.markdown(f"✅ **In Stock**")
                            st.caption(f"{stock} avail.")
                        elif stock > 0:
                            st.markdown(f"⚠️ **Low**")
                            st.caption(f"Need {needs}")
                        else:
                            st.markdown(f"❌ **Order**")
                            st.caption(f"Need {needs}")
                    
                    with col4:
                        st.markdown(f"**€{item.get('preis_gesamt', 0):.2f}**")
                    
                    with col5:
                        if st.button("➕", key=f"add_img_{item.get('artikel_id', '')}"):
                            product = {
                                'id': item.get('artikel_id', ''),
                                'name': item.get('artikelname', item.get('artikel_id', '')),
                                'price': item.get('preis_stk', 0),
                                'description': item.get('kategorie', ''),
                                'supplier': item.get('lieferant', ''),
                                'icon': '🔩'
                            }
                            add_to_cart(product, item.get('anzahl', 1))
                            st.toast(f"Added {item.get('artikelname', '')} to cart!")
                
                # Total and Add All
                st.markdown("---")
                total = recommendations.get("total", 0)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"### Total: €{total:.2f}")
                with col2:
                    if st.button("🛒 Add All to Cart", key="add_all_img", type="primary", use_container_width=True):
                        for item in items:
                            product = {
                                'id': item.get('artikel_id', ''),
                                'name': item.get('artikelname', item.get('artikel_id', '')),
                                'price': item.get('preis_stk', 0),
                                'description': item.get('kategorie', ''),
                                'supplier': item.get('lieferant', ''),
                                'icon': '🔩'
                            }
                            add_to_cart(product, item.get('anzahl', 1))
                        st.success("✅ All items added to cart!")
                        st.session_state.image_chat_recommendations = None
                        st.rerun()
    
    # Order Summary
    with summary_col:
        with st.container(border=True):
            render_order_summary(key_prefix="image_search")
