"""
Helper functions for cart management, orders, and navigation
"""
import streamlit as st
import random
from datetime import datetime


def add_to_cart(product, qty, add_mode=True):
    """Add product to cart. If add_mode=True, adds qty to existing. If False, sets qty."""
    if qty > 0:
        for item in st.session_state.cart:
            if item['id'] == product['id']:
                if add_mode:
                    item['qty'] += qty
                else:
                    item['qty'] = qty
                return
        st.session_state.cart.append({**product, "qty": qty})


def set_cart_qty(product, qty):
    """Set the quantity of a product in cart (replaces existing qty)"""
    if qty > 0:
        for item in st.session_state.cart:
            if item['id'] == product['id']:
                item['qty'] = qty
                return
        st.session_state.cart.append({**product, "qty": qty})
    else:
        remove_from_cart(product['id'])


def remove_from_cart(product_id):
    """Remove a product from the cart"""
    st.session_state.cart = [item for item in st.session_state.cart if item['id'] != product_id]


def calculate_total():
    """Calculate the total price of items in cart"""
    return sum(item['price'] * item['qty'] for item in st.session_state.cart)


def place_order():
    """Place an order with current cart items"""
    total = calculate_total()
    status = "Pending Approval" if total > 200 else "Auto-Approved"
    
    new_order = {
        "Order ID": f"ORD-{random.randint(1000, 9999)}",
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Requester": "Site Foreman",
        "Total (EUR)": total,
        "Status": status,
        "Items": st.session_state.cart.copy()
    }
    st.session_state.orders.insert(0, new_order)
    st.session_state.cart = []
    st.session_state.cart_version += 1
    return status


def navigate_to(page):
    """Navigate to a different page"""
    st.session_state.current_page = page

