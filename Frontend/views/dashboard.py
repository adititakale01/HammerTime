"""
Dashboard View - Product Search with AI recommendations
"""
import streamlit as st
import requests
from utils import add_to_cart
from components import render_order_summary
from config import API_BASE_URL


def dashboard_view():
    """Main dashboard view with product search"""
    main_col, summary_col = st.columns([2.5, 1])
    
    with main_col:
        st.markdown("## AI Search")
        
        # Search with button
        search_col, btn_col = st.columns([3, 1])
        with search_col:
            search_query = st.text_input(
                "Search",
                placeholder="Search by product or task (e.g. 'Drywall', '500 screws M4',...)",
                label_visibility="collapsed",
                value=st.session_state.last_search_query
            )
        with btn_col:
            search_clicked = st.button("Search", use_container_width=True)
        
        # Clear results button
        if st.session_state.search_results:
            if st.button("Clear Results", type="secondary", key="dashboard_clear_results"):
                st.session_state.search_results = None
                st.session_state.last_search_query = ""
                st.rerun()
        
        # AI Search Results from Backend
        if search_query and search_clicked:
            st.session_state.last_search_query = search_query
            with st.spinner(f"🔍 Searching for: {search_query}"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/receive_user_prompt",
                        json={"prompt": search_query}
                    )
                    response.raise_for_status()
                    response_data = response.json()
                    
                    if response_data and "items" in response_data and "explanation" in response_data:
                        api_items = response_data["items"]
                        recommendations = []
                        
                        for api_item in api_items:
                            recommendations.append({
                                "id": api_item.get("artikel_id"),
                                "name": api_item.get("artikelname"),
                                "qty": api_item.get("anzahl"),
                                "price": api_item.get("preis_stk"),
                                "category": api_item.get("kategorie"),
                                "supplier": api_item.get("lieferant"),
                                "subtotal": api_item.get("preis_stk", 0) * api_item.get("anzahl", 0),
                                "lagerbestand": api_item.get("lagerbestand", 0),  # Current stock
                                "needs_order": api_item.get("needs_order", api_item.get("anzahl", 0)),  # Additional needed
                                "is_preferred": api_item.get("is_preferred", False),  # Preferred supplier
                                "lead_time_days": api_item.get("lead_time_days", 7)  # Lead time
                            })
                        
                        st.session_state.search_results = {
                            "explanation": response_data['explanation'],
                            "recommendations": recommendations,
                            "requireApproval": response_data.get("requireApproval", False)
                        }
                    else:
                        st.error("Invalid response format from API.")
                        st.session_state.search_results = None
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"API request failed: {str(e)}")
                    st.session_state.search_results = None
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
                    st.session_state.search_results = None
        
        # Display stored search results
        if st.session_state.search_results:
            results = st.session_state.search_results
            recommendations = results["recommendations"]
            
            st.success("✨ AI Recommendation")
            st.markdown(f"**{results['explanation']}**")
            
            st.divider()
            st.markdown("### Recommended Materials")
            
            if recommendations:
                col_spacer, col_btn = st.columns([3, 1])
                with col_btn:
                    if st.button("Add All to Cart", type="primary", use_container_width=True):
                        for rec in recommendations:
                            add_to_cart(rec, rec["qty"])
                        st.toast(f"✅ Added {len(recommendations)} items to cart!")
                
                st.divider()
                
                for idx, rec in enumerate(recommendations):
                    with st.container(border=True):
                        c1, c2, c3, c4, c5, c6 = st.columns([0.5, 2, 1, 1, 1, 0.8])
                        with c1:
                            st.markdown("<div style='font-size: 2rem; text-align: center;'>🔩</div>", unsafe_allow_html=True)
                        with c2:
                            # Show preferred badge next to supplier
                            is_preferred = rec.get('is_preferred', False)
                            lead_time = rec.get('lead_time_days', 7)
                            st.markdown(f"**{rec['name']}**")
                            if is_preferred:
                                st.markdown(f"""
                                <span style="color: #64748B; font-size: 0.875rem;">{rec['category']} | </span>
                                <span style="display: inline-block; background: #FEF2F2; border: 1.5px solid #EF4444; border-radius: 4px; padding: 1px 6px; font-size: 0.75rem; color: #DC2626; font-weight: 600;">⭐ {rec['supplier']}</span>
                                """, unsafe_allow_html=True)
                            else:
                                st.caption(f"{rec['category']} | {rec['supplier']}")
                        with c3:
                            st.markdown(f"**Qty: {rec['qty']}**")
                            st.caption(f"€{rec['subtotal']:.2f}")
                        with c4:
                            # Show inventory status
                            stock = rec.get('lagerbestand', 0)
                            needs = rec.get('needs_order', rec['qty'])
                            if stock >= rec['qty']:
                                st.markdown(f"✅ **In Stock**")
                                st.caption(f"{stock} available")
                            elif stock > 0:
                                st.markdown(f"⚠️ **Low Stock**")
                                st.caption(f"Need {needs} more")
                            else:
                                st.markdown(f"❌ **Order**")
                                st.caption(f"Need {needs}")
                        with c5:
                            # Show lead time
                            st.markdown(f"🚚 **{lead_time}d**")
                            st.caption("lead time")
                        with c6:
                            if st.button("Add", key=f"rec_{rec['id']}_{idx}", use_container_width=True):
                                add_to_cart(rec, rec["qty"])
                                st.toast(f"✅ Added {rec['name']} to cart!")
                
                total_estimate = sum(r["subtotal"] for r in recommendations)
                st.divider()
                st.metric("Total Estimate", f"€{total_estimate:.2f}")
                
                if results.get("requireApproval", False):
                    st.info("⚠️ This order will require approval (over budget threshold)")
            else:
                st.warning("No matching items found in catalog.")
        
        # Show helpful message when no search yet
        if not st.session_state.search_results:
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #64748B;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h3 style="color: #1E3A5F; margin-bottom: 0.5rem;">Search for materials or tasks!</h3>
                <p>Describe what you need and HAMMA! will recommend the best products for the job.</p>
                <p style="font-size: 0.9rem; color: #94A3B8;">Try: "Tools for installing drywall"</p>
            </div>
            """, unsafe_allow_html=True)
    
    with summary_col:
        with st.container(border=True):
            render_order_summary(key_prefix="dashboard")

