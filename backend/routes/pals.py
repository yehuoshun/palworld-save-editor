"""
GET /api/pals — 列出存档中的所有帕鲁。
"""
from backend.parsers import extract_pals
from backend.save_reader import load_sav


def register(app):
    @app.get("/api/pals")
    def api_list_pals(save_path: str):
        try:
            data = load_sav(save_path)
            pals = extract_pals(data)
            return {"success": True, "count": len(pals), "pals": pals}
        except Exception as e:
            return {"success": False, "error": str(e)}