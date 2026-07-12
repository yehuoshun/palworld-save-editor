"""
存档加载器：封装 palworld-save-tools，提供 sav ↔ json 互转。
"""
import time
from pathlib import Path
from typing import Any

from palworld_save_tools.gvas import GvasFile
from palworld_save_tools.palsav import compress_gvas_to_sav, decompress_sav_to_gvas
from palworld_save_tools.paltypes import PALWORLD_CUSTOM_PROPERTIES, PALWORLD_TYPE_HINTS


def load_sav(sav_path: str | Path) -> dict[str, Any]:
    """加载 .sav 文件，返回 Python dict。"""
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

    save_game_class = gvas_file.header.save_game_class_name
    if "PalWorldSaveGame" in save_game_class or "LocalWorldSaveGame" in save_game_class:
        save_type = 0x32
    else:
        save_type = 0x31

    sav_data = compress_gvas_to_sav(written, save_type)
    with open(sav_path, "wb") as f:
        f.write(sav_data)

    print(f"存档保存完成: {sav_path.name} ({len(sav_data):,} bytes)")