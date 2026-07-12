"""
FastAPI 应用入口。
"""
from backend.app import app
from backend.routes import register_all

register_all(app)