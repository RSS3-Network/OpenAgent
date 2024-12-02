from .openai import router as openai_router
from .widget import router as widget_router
from .health import router as health_router

__all__ = [
    'openai_router',
    'widget_router',
    'health_router'
]
