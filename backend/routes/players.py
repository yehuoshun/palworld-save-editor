"""
GET /api/players — 列出存档中的所有玩家。
"""
from backend.parsers import extract_players
from backend.save_reader import load_sav


def register(app):
    @app.get("/api/players")
    def api_list_players(save_path: str):
        try:
            data = load_sav(save_path)
            players = extract_players(data)
            return {"success": True, "count": len(players), "players": players}
        except Exception as e:
            return {"success": False, "error": str(e)}