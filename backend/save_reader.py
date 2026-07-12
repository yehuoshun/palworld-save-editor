"""
存档加载器：封装 palworld-save-tools 的 API，提供 sav ↔ json 互转。
"""

import json
import time
from pathlib import Path
from typing import Any

from palworld_save_tools.gvas import GvasFile
from palworld_save_tools.palsav import compress_gvas_to_sav, decompress_sav_to_gvas
from palworld_save_tools.paltypes import PALWORLD_CUSTOM_PROPERTIES, PALWORLD_TYPE_HINTS


def load_sav(sav_path: str | Path) -> dict[str, Any]:
    """加载 .sav 文件，返回 Python dict（JSON 结构）。"""
    sav_path = Path(sav_path)
    if not sav_path.exists():
        raise FileNotFoundError(f"存档不存在: {sav_path}")

    start = time.perf_counter()

    with open(sav_path, "rb") as f:
        data = f.read()

    raw_gvas, _ = decompress_sav_to_gvas(data)
    gvas_file = GvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES)
    result = gvas_file.dump()

    elapsed = time.perf_counter() - start
    print(f"存档加载完成: {sav_path.name} ({len(data):,} bytes) → {elapsed:.2f}s")
    return result


def save_sav(sav_path: str | Path, data: dict[str, Any]) -> None:
    """将 Python dict 写回 .sav 文件。"""
    sav_path = Path(sav_path)

    gvas_file = GvasFile.load(data)
    written = gvas_file.write(PALWORLD_CUSTOM_PROPERTIES)

    # 检测存档类型
    save_game_class = gvas_file.header.save_game_class_name
    if "PalWorldSaveGame" in save_game_class or "LocalWorldSaveGame" in save_game_class:
        save_type = 0x32
    else:
        save_type = 0x31

    sav_data = compress_gvas_to_sav(written, save_type)

    with open(sav_path, "wb") as f:
        f.write(sav_data)

    print(f"存档保存完成: {sav_path.name} ({len(sav_data):,} bytes)")


def load_json(json_path: str | Path) -> dict[str, Any]:
    """加载 .json 文件（用于调试/分析）。"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_save_info(data: dict[str, Any]) -> dict[str, Any]:
    """提取存档基本信息。"""
    world_data = data.get("properties", {}).get("worldSaveData", {}).get("value", {})

    character_map = world_data.get("CharacterSaveParameterMap", {}).get("value", [])
    pal_count = 0
    player_count = 0
    for entry in character_map:
        raw = entry.get("value", {}).get("RawData", {}).get("value", {})
        obj = raw.get("object", {}).get("SaveParameter", {}).get("value", {})
        if not obj:
            continue
        is_player = obj.get("IsPlayer", False)
        if isinstance(is_player, dict):
            is_player = is_player.get("value", False)
        if is_player:
            player_count += 1
        else:
            pal_count += 1

    return {
        "world_name": world_data.get("worldName", {}).get("value", "Unknown"),
        "pal_count": pal_count,
        "player_count": player_count,
        "guild_count": len(
            world_data.get("GroupSaveDataMap", {}).get("value", [])
        ),
    }