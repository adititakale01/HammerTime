"""
Procurement Assistant - Main Entry Point
"""
import streamlit as st


# Page config must be first Streamlit command
st.set_page_config(page_title="HAMMA", page_icon="Frontend/assets/favicon.png", layout="wide")

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

import base64
from pathlib import Path


def main():
    """Main application entry point"""
    # Apply styles
    apply_styles(st)
    
        # Initialize session state
    init_session_state()
    
    

    # helper to build data URI for local logo
    def img_to_data_uri(path: str) -> str:
        p = Path(path)
        if not p.exists():
            return path
        data = p.read_bytes()
        mime = "image/png"
        if p.suffix.lower() in (".jpg", ".jpeg"):
            mime = "image/jpeg"
        elif p.suffix.lower() == ".svg":
            mime = "image/svg+xml"
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"

    # Load splash HTML template and embed logo data URI; fallback to a simple inline block
    tpl_path = Path("Frontend/assets/splash_template.html")
    logo_path = "Frontend/assets/HAMMA_bluebg.png"
    logo_uri = img_to_data_uri(logo_path)
    if tpl_path.exists():
        tpl = tpl_path.read_text(encoding='utf-8')
        splash_html = tpl.replace("{{LOGO_URI}}", logo_uri)
        st.markdown(splash_html, unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display:flex;align-items:center;gap:0.75rem;padding:0.5rem 0;'><img src='{logo_uri}' width='48' style='border-radius:6px;'/><div><div style='font-size:1.25rem;font-weight:700;color:#1E3A5F;'>Procurement Assistant</div><div style='color:#64748B;font-size:0.9rem;margin-top:2px;'>Onsite procurement recommendations</div></div></div>", unsafe_allow_html=True)

    # Render sidebar navigation
    render_sidebar()
    st.logo("Frontend/assets/HAMMA.png")
    
    # Route to appropriate view
    if st.session_state.current_page == "Dashboard":
        tab1, tab2, tab3 = st.tabs([" AI Search", " Chat Bot", " Image Search"])
        
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
