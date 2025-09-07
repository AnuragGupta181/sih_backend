"""
API route modules for FastAPI.
Includes:
- predict.py  : /predict endpoint
- insight.py  : /insights endpoint
- health.py   : /health endpoint
"""

from . import predict
from . import insight
from . import health

__all__ = ["predict", "insight", "health"]
