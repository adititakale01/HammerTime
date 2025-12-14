"""
Reports View - Analytics and metrics
"""
import streamlit as st
import requests
from config import API_BASE_URL


def reports_view():
    """Display reports and analytics"""
    st.markdown("### Reports & Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_orders = len(st.session_state.orders)
        st.metric("Total Orders", total_orders)
    
    with col2:
        # Only count approved orders (exclude declined)
        total_spend = sum(
            o['Total (EUR)'] for o in st.session_state.orders 
            if o.get('Status') != 'Order Declined'
        ) if st.session_state.orders else 0
        st.metric("Total Spend", f"€{total_spend:.2f}")
    
    with col3:
        pending = len([o for o in st.session_state.orders if o['Status'] == 'Pending Approval'])
        st.metric("Pending Approvals", pending)
    
    st.markdown("---")
    
    # Auto-Approved Orders Section
    if st.session_state.reports:
        st.markdown("### Auto-Approved Orders")
        
        for order in st.session_state.reports:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{order['Order ID']}**")
                    st.caption(f"{order['Date']} • {order['Requester']}")
                with col2:
                    st.markdown(f"€{order['Total (EUR)']:.2f}")
                with col3:
                    if st.button("Generate Contract", key=f"contract_{order['Order ID']}"):
                        # Prepare parts list for the contract
                        parts_list = []
                        for item in order['Items']:
                            parts_list.append({
                                "id": item.get('id', ''),
                                "name": item.get('name', ''),
                                "description": item.get('description', ''),
                                "quantity": item.get('qty', 0),
                                "price": item.get('price', 0.0),
                                "supplier": item.get('supplier', '')
                            })
                        
                        # Call the backend endpoint
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/generate_contract",
                                json={
                                    "order_number": order['Order ID'],
                                    "parts_list": parts_list
                                }
                            )
                            if response.status_code == 200:
                                # Save the PDF file
                                pdf_filename = f"contract_{order['Order ID']}.pdf"
                                with open(pdf_filename, 'wb') as f:
                                    f.write(response.content)
                                st.success(f"Contract generated and saved as {pdf_filename}")
                                
                                # Provide download button
                                st.download_button(
                                    label="Download Contract",
                                    data=response.content,
                                    file_name=pdf_filename,
                                    mime="application/pdf"
                                )
                            else:
                                st.error(f"Failed to generate contract: {response.text}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
    else:
        st.info("No auto-approved orders yet.")

