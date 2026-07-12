"""
POST /api/load — 加载存档，返回基本信息。
"""
from backend.parsers import extract_save_info
from backend.save_reader import load_sav


def register(app):
    @app.post("/api/load")
    def api_load(save_path: str):
        try:
            data = load_sav(save_path)
            info = extract_save_info(data)
            return {"success": True, "info": info}
        except FileNotFoundError:
            return {"success": False, "error": f"存档不存在: {save_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}