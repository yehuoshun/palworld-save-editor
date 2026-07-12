"""
路由注册：导入所有路由模块并注册到 app。
"""
from backend.routes import health, load, pal_detail, pals, players


def register_all(app):
    health.register(app)
    load.register(app)
    pals.register(app)
    players.register(app)
    pal_detail.register(app)