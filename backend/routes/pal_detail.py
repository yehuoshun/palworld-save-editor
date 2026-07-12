"""
GET /api/pal/{instance_id} — 单个帕鲁完整详情。
"""
from backend.parsers import extract_pal_detail
from backend.save_reader import load_sav


def register(app):
    @app.get("/api/pal/{instance_id}")
    def api_pal_detail(save_path: str, instance_id: str):
        try:
            data = load_sav(save_path)
            pal = extract_pal_detail(data, instance_id)
            if pal is None:
                return {"success": False, "error": f"帕鲁不存在: {instance_id}"}
            return {"success": True, "pal": pal}
        except Exception as e:
            return {"success": False, "error": str(e)}