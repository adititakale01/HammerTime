"""
Views package - contains all page views
"""
from .dashboard import dashboard_view
from .voice_request import voice_request_view
from .image_search import image_search_view
from .orders import orders_view
from .reports import reports_view

__all__ = [
    'dashboard_view',
    'voice_request_view', 
    'image_search_view',
    'orders_view',
    'reports_view'
]

