"""
存档数据解析：从 JSON 结构中提取帕鲁、玩家、公会信息。
"""


def extract_save_info(data: dict) -> dict:
    """提取存档基本信息。"""
    world_data = data.get("properties", {}).get("worldSaveData", {}).get("value", {})
    character_map = world_data.get("CharacterSaveParameterMap", {}).get("value", [])

    pal_count = 0
    player_count = 0
    for entry in character_map:
        if _is_player(entry):
            player_count += 1
        elif _is_valid_character(entry):
            pal_count += 1

    return {
        "world_name": world_data.get("worldName", {}).get("value", "Unknown"),
        "pal_count": pal_count,
        "player_count": player_count,
        "guild_count": len(world_data.get("GroupSaveDataMap", {}).get("value", [])),
    }


def extract_players(data: dict) -> list[dict]:
    """提取所有玩家列表。"""
    world_data = data.get("properties", {}).get("worldSaveData", {}).get("value", {})
    character_map = world_data.get("CharacterSaveParameterMap", {}).get("value", [])

    players = []
    for entry in character_map:
        obj = _get_save_parameter(entry)
        if not obj or not _is_player(entry):
            continue

        key = entry.get("key", {})
        players.append({
            "instance_id": _safe_get(key, "value", "InstanceId", "value"),
            "uid": _safe_get(key, "value", "PlayerUId", "value"),
            "nickname": _safe_get(obj, "NickName", "value", default=""),
            "level": _safe_get(obj, "Level", "value", default=1),
            "hp": _extract_hp(obj),
            "tech_points": _safe_get(obj, "TechnologyPoint", "value", default=0),
            "ancient_tech_points": _safe_get(obj, "bossTechnologyPoint", "value", default=0),
        })

    return players


def extract_pals(data: dict) -> list[dict]:
    """提取所有帕鲁列表。"""
    world_data = data.get("properties", {}).get("worldSaveData", {}).get("value", {})
    character_map = world_data.get("CharacterSaveParameterMap", {}).get("value", [])

    pals = []
    for entry in character_map:
        obj = _get_save_parameter(entry)
        if not obj or _is_player(entry):
            continue

        key = entry.get("key", {})
        pals.append({
            "instance_id": _safe_get(key, "value", "InstanceId", "value"),
            "character_id": _safe_get(obj, "CharacterID", "value"),
            "nickname": _safe_get(obj, "NickName", "value", default=""),
            "level": _safe_get(obj, "Level", "value", default=1),
            "gender": _safe_get(obj, "Gender", "value", default="Unknown"),
            "hp": _extract_hp(obj),
        })

    return pals


def _get_save_parameter(entry: dict) -> dict | None:
    """从 CharacterSaveParameterMap 条目中提取 SaveParameter。"""
    raw = entry.get("value", {}).get("RawData", {}).get("value", {})
    return raw.get("object", {}).get("SaveParameter", {}).get("value")


def _is_player(entry: dict) -> bool:
    """判断是否为玩家（而非帕鲁）。"""
    obj = _get_save_parameter(entry)
    if not obj:
        return False
    is_player = obj.get("IsPlayer", False)
    if isinstance(is_player, dict):
        is_player = is_player.get("value", False)
    return bool(is_player)


def _is_valid_character(entry: dict) -> bool:
    """判断是否为有效角色（有 SaveParameter）。"""
    return _get_save_parameter(entry) is not None


def _extract_hp(obj: dict) -> int:
    """从嵌套的 HP 结构中提取数值。"""
    hp = obj.get("HP", {})
    if isinstance(hp, dict):
        hp = hp.get("value", hp)
    if isinstance(hp, dict):
        hp = hp.get("Value", hp)
    if isinstance(hp, dict):
        hp = hp.get("value", 0)
    return hp if isinstance(hp, (int, float)) else 0


def _safe_get(d: dict, *keys, default=None):
    """安全地从嵌套字典中取值。"""
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, {})
    return d if d != {} else default