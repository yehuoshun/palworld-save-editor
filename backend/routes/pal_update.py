"""
POST /api/pal/{id}/update — 修改单个帕鲁属性并保存。
"""
from backend.save_reader import load_sav, save_sav


def register(app):
    @app.post("/api/pal/{instance_id}/update")
    def api_update_pal(save_path: str, instance_id: str, fields: dict):
        """
        修改帕鲁属性。fields 是要更新的字段字典。
        目前支持：level, exp, nickname, gender, hp, max_hp, stomach, sanity,
                 star_rank, talent_hp, talent_attack, talent_defense,
                 soul_hp, soul_attack, soul_defense, soul_craftspeed,
                 active_skills, passive_skills, friendship
        """
        try:
            data = load_sav(save_path)

            world_data = data["properties"]["worldSaveData"]["value"]
            character_map = world_data["CharacterSaveParameterMap"]["value"]

            for entry in character_map:
                key = entry.get("key", {})
                sid = _safe_get(key, "value", "InstanceId", "value")
                if str(sid) != str(instance_id):
                    continue

                obj = _get_save_parameter(entry)
                if not obj:
                    return {"success": False, "error": "帕鲁数据无效"}

                _apply_fields(obj, fields)
                save_sav(save_path, data)
                return {"success": True, "message": "已保存"}

            return {"success": False, "error": f"帕鲁不存在: {instance_id}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def _get_save_parameter(entry: dict) -> dict | None:
    raw = entry.get("value", {}).get("RawData", {}).get("value", {})
    return raw.get("object", {}).get("SaveParameter", {}).get("value")


def _safe_get(d: dict, *keys, default=None):
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, {})
    return d if d != {} else default


def _set_value(parent: dict, key: str, value):
    """设置 GVAS 嵌套结构中的值。"""
    if key not in parent:
        parent[key] = {}
    if isinstance(parent[key], dict):
        parent[key]["value"] = value
    else:
        parent[key] = {"value": value}


def _apply_fields(obj: dict, fields: dict):
    """将修改字段写入帕鲁对象。"""
    scalar_fields = {
        "level": "Level",
        "exp": "Exp",
        "nickname": "NickName",
        "gender": "Gender",
        "hp": "HP",
        "max_hp": "MaxHP",
        "stomach": "Stomach",
        "sanity": "SanityValue",
        "star_rank": "Rank",
        "talent_hp": "Talent_HP",
        "talent_attack": "Talent_Shot",
        "talent_defense": "Talent_Defense",
        "soul_hp": "Rank_HP",
        "soul_attack": "Rank_Attack",
        "soul_defense": "Rank_Defense",
        "soul_craftspeed": "Rank_CraftSpeed",
        "friendship": "FriendShipPoint",
    }

    for field_name, obj_key in scalar_fields.items():
        if field_name in fields:
            _set_value(obj, obj_key, fields[field_name])

    # HP 是嵌套结构
    if "hp" in fields:
        hp = obj.get("HP", {})
        if isinstance(hp, dict):
            hp_val = hp.get("value", hp)
            if isinstance(hp_val, dict):
                hp_val["Value"] = {"value": fields["hp"]}
            else:
                hp["value"] = fields["hp"]

    # 列表字段
    if "active_skills" in fields:
        _set_array(obj, "EquipWaza", fields["active_skills"])
    if "passive_skills" in fields:
        _set_array(obj, "PassiveSkillList", fields["passive_skills"])


def _set_array(parent: dict, key: str, values: list):
    """设置数组字段。"""
    if key not in parent:
        parent[key] = {}
    parent[key]["value"] = {
        "values": [{"value": v} for v in values]
    }