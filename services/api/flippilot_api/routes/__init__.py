"""
__init__.py for routes package
"""

from .health import router as health_router
from .watchlist import router as watchlist_router

__all__ = ["health_router", "watchlist_router"]
