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


def extract_pal_detail(data: dict, instance_id: str) -> dict | None:
    """提取单个帕鲁的完整详情。"""
    world_data = data.get("properties", {}).get("worldSaveData", {}).get("value", {})
    character_map = world_data.get("CharacterSaveParameterMap", {}).get("value", [])

    for entry in character_map:
        key = entry.get("key", {})
        sid = _safe_get(key, "value", "InstanceId", "value")
        if str(sid) != str(instance_id):
            continue

        obj = _get_save_parameter(entry)
        if not obj:
            return None

        return {
            "instance_id": sid,
            "character_id": _safe_get(obj, "CharacterID", "value"),
            "nickname": _safe_get(obj, "NickName", "value", default=""),
            "level": _safe_get(obj, "Level", "value", default=1),
            "exp": _safe_get(obj, "Exp", "value", default=0),
            "gender": _safe_get(obj, "Gender", "value", default="Unknown"),
            "is_boss": _safe_get(obj, "IsBoss", "value", default=False),
            "is_lucky": _safe_get(obj, "IsLucky", "value", default=False),
            "is_tower": _safe_get(obj, "IsTower", "value", default=False),
            "hp": _extract_hp(obj),
            "max_hp": _safe_get(obj, "MaxHP", "value", default=0),
            "stomach": _safe_get(obj, "Stomach", "value", default=0.0),
            "sanity": _safe_get(obj, "SanityValue", "value", default=0.0),
            "star_rank": _safe_get(obj, "Rank", "value", default=0),
            "talent_hp": _safe_get(obj, "Talent_HP", "value", default=0),
            "talent_attack": _safe_get(obj, "Talent_Shot", "value", default=0),
            "talent_defense": _safe_get(obj, "Talent_Defense", "value", default=0),
            "soul_hp": _safe_get(obj, "Rank_HP", "value", default=0),
            "soul_attack": _safe_get(obj, "Rank_Attack", "value", default=0),
            "soul_defense": _safe_get(obj, "Rank_Defense", "value", default=0),
            "soul_craftspeed": _safe_get(obj, "Rank_CraftSpeed", "value", default=0),
            "active_skills": _extract_list(obj, "EquipWaza"),
            "learned_skills": _extract_list(obj, "MasteredWaza"),
            "passive_skills": _extract_list(obj, "PassiveSkillList"),
            "work_suitability": _extract_work_suitability(obj),
            "owner_uid": _safe_get(obj, "OwnerPlayerUId", "value"),
            "friendship": _safe_get(obj, "FriendShipPoint", "value", default=0),
        }

    return None


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


def _extract_list(obj: dict, key: str) -> list:
    """提取嵌套列表字段。"""
    val = obj.get(key, {})
    if isinstance(val, dict):
        val = val.get("value", val)
    if isinstance(val, dict):
        val = val.get("values", val)
    if isinstance(val, list):
        return [v.get("value", v) if isinstance(v, dict) else v for v in val]
    return []


def _extract_work_suitability(obj: dict) -> dict:
    """提取工作适应性。"""
    ranks = obj.get("GotWorkSuitabilityAddRankList", {})
    if isinstance(ranks, dict):
        ranks = ranks.get("value", ranks)
    if isinstance(ranks, dict):
        ranks = ranks.get("values", ranks)
    if not isinstance(ranks, list):
        return {}

    result = {}
    for entry in ranks:
        if not isinstance(entry, dict):
            continue
        ws = entry.get("WorkSuitability", {})
        if isinstance(ws, dict):
            ws = ws.get("value", ws)
        rank = entry.get("Rank", {})
        if isinstance(rank, dict):
            rank = rank.get("value", 0)
        result[str(ws)] = int(rank) if rank else 0
    return result


def _safe_get(d: dict, *keys, default=None):
    """安全地从嵌套字典中取值。"""
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, {})
    return d if d != {} else default