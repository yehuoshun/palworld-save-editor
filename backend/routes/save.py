"""
POST /api/save — 保存修改后的存档。
"""
from backend.save_reader import load_sav, save_sav


def register(app):
    @app.post("/api/save")
    def api_save(save_path: str, output_path: str = None):
        """
        保存存档。output_path 为空则覆盖原文件。
        后续会支持传入 modified_pals/players 参数。
        """
        try:
            target = output_path or save_path
            data = load_sav(save_path)
            save_sav(target, data)
            return {"success": True, "message": f"存档已保存到 {target}"}
        except Exception as e:
            return {"success": False, "error": str(e)}