"""
GET /api/health — 健康检查。
"""


def register(app):
    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": "0.1.0"}