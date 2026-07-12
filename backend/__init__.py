from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Palworld Save Editor", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0"}


@app.post("/api/load")
def load_save(save_path: str):
    """加载存档文件。"""
    from backend.save_reader import get_save_info, load_sav

    try:
        data = load_sav(save_path)
        info = get_save_info(data)
        return {"success": True, "info": info}
    except FileNotFoundError:
        return {"success": False, "error": f"存档不存在: {save_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/pals")
def list_pals(save_path: str):
    """列出存档中的所有帕鲁。"""
    from backend.save_reader import load_sav

    try:
        data = load_sav(save_path)
        world_data = data.get("properties", {}).get("worldSaveData", {}).get("value", {})
        character_map = world_data.get("CharacterSaveParameterMap", {}).get("value", [])

        pals = []
        for entry in character_map:
            raw = entry.get("value", {}).get("RawData", {}).get("value", {})
            obj = raw.get("object", {}).get("SaveParameter", {}).get("value", {})
            if not obj:
                continue
            is_player = obj.get("IsPlayer", False)
            if isinstance(is_player, dict):
                is_player = is_player.get("value", False)
            if is_player:
                continue

            pals.append({
                "instance_id": entry.get("key", {}).get("value", {}).get("InstanceId", {}).get("value", "unknown"),
                "character_id": obj.get("CharacterID", {}).get("value", "unknown"),
                "nickname": obj.get("NickName", {}).get("value", ""),
                "level": obj.get("Level", {}).get("value", 1),
                "gender": obj.get("Gender", {}).get("value", "Unknown"),
                "hp": obj.get("HP", {}).get("value", {}).get("Value", {}).get("value", 0),
            })

        return {"success": True, "count": len(pals), "pals": pals}
    except Exception as e:
        return {"success": False, "error": str(e)}