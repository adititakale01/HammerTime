"""
CSS Styles for the Procurement Assistant UI
"""

CUSTOM_CSS = """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #F1F5F9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1 {
        color: #1E3A5F !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem;
    }
    
    /* Navigation Items */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0.5rem;
        border-radius: 8px;
        color: #64748B;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .nav-item:hover {
        background-color: #F1F5F9;
        color: #1E3A5F;
    }
    
    .nav-item.active {
        background-color: #EFF6FF;
        color: #2563EB;
    }
    
    .nav-icon {
        margin-right: 0.75rem;
        font-size: 1.1rem;
    }
    
    /* Main Content Cards */
    .content-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    /* Product Cards */
    .product-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    
    .product-card:hover {
        border-color: #2563EB;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
    }
    
    .product-icon {
        width: 48px;
        height: 48px;
        background-color: #F1F5F9;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 1.5rem;
    }
    
    .product-info {
        flex: 1;
    }
    
    .product-name {
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 0.25rem;
    }
    
    .product-desc {
        font-size: 0.875rem;
        color: #64748B;
    }
    
    /* Order Summary Card */
    .summary-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .summary-title {
        font-weight: 700;
        color: #1E3A5F;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .summary-total {
        display: flex;
        justify-content: space-between;
        padding: 1rem 0 0.5rem;
        font-weight: 700;
        color: #1E3A5F;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    
    .stButton button[kind="primary"] {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton button[kind="primary"] p,
    .stButton button[kind="primary"] span,
    .stButton button[kind="primary"] * {
        color: white !important;
        background: transparent !important;
    }
    
    .stButton button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }
    
    .stButton button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #2563EB !important;
        border: 2px solid #2563EB !important;
    }
    
    .stButton button[kind="secondary"] p,
    .stButton button[kind="secondary"] span,
    .stButton button[kind="secondary"] * {
        color: #2563EB !important;
        background: transparent !important;
    }
    
    /* Search Input */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Number Input */
    .stNumberInput input {
        border-radius: 8px !important;
        text-align: center !important;
    }
    
    /* Section Headers */
    .section-header {
        font-weight: 700;
        color: #1E3A5F;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Text colors */
    .stMarkdown, p, span, label {
        color: #334155 !important;
    }
    
    h1, h2, h3, h4 {
        color: #1E3A5F !important;
    }
    
    /* Recommendation Card */
    .recommendation-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .recommendation-header {
        font-weight: 700;
        color: #1E3A5F;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .supplier-name {
        font-weight: 600;
        color: #2563EB;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .rec-item {
        color: #334155;
        margin-bottom: 0.5rem;
    }
    
    .lead-time {
        color: #64748B;
        font-size: 0.9rem;
        margin-top: 0.75rem;
    }
    
    .savings-badge {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    /* Voice Input Button */
    .voice-btn {
        background-color: #EFF6FF;
        border: 2px solid #2563EB;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .voice-btn:hover {
        background-color: #2563EB;
        color: white;
    }
    
    /* Order Details Table */
    .order-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .order-table th {
        text-align: left;
        padding: 0.75rem;
        background-color: #F8FAFC;
        color: #64748B;
        font-weight: 600;
        font-size: 0.85rem;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .order-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #F1F5F9;
        color: #334155;
    }
    </style>
"""


def apply_styles(st):
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

