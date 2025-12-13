"""
Procurement Assistant - Main Entry Point
"""
import streamlit as st

# Page config must be first Streamlit command
st.set_page_config(page_title="Procurement Assistant", layout="wide")

# Import modules
from styles import apply_styles
from config import init_session_state
from components import render_sidebar
from views import (
    dashboard_view,
    voice_request_view,
    image_search_view,
    orders_view,
    reports_view
)


def main():
    """Main application entry point"""
    # Apply styles
    apply_styles(st)
    
    # Initialize session state
    init_session_state()
    
    # Render sidebar navigation
    render_sidebar()
    
    # Route to appropriate view
    if st.session_state.current_page == "Dashboard":
        tab1, tab2, tab3 = st.tabs(["📦 Product Search", "🎤 Create Request", "📷 Image Search"])
        
        with tab1:
            dashboard_view()
        
        with tab2:
            voice_request_view()
        
        with tab3:
            image_search_view()
    
    elif st.session_state.current_page == "Orders":
        orders_view()
    
    elif st.session_state.current_page == "Reports":
        reports_view()


if __name__ == "__main__":
    main()
