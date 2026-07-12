"""
测试脚本：验证存档读取功能。
用法：python test_reader.py <Level.sav>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.parsers import extract_players, extract_save_info
from backend.save_reader import load_sav


def main():
    if len(sys.argv) < 2:
        print("用法: python test_reader.py <Level.sav>")
        sys.exit(1)

    sav_path = sys.argv[1]
    print(f"正在加载: {sav_path}")

    data = load_sav(sav_path)
    info = extract_save_info(data)

    print(f"\n=== 存档信息 ===")
    print(f"世界名称: {info['world_name']}")
    print(f"玩家数量: {info['player_count']}")
    print(f"帕鲁数量: {info['pal_count']}")
    print(f"公会数量: {info['guild_count']}")

    players = extract_players(data)
    if players:
        print(f"\n=== 玩家列表 ===")
        for p in players[:10]:
            print(f"  {p['nickname']} (Lv.{p['level']}) HP:{p['hp']}")
        if len(players) > 10:
            print(f"  ... 还有 {len(players) - 10} 个玩家")

    print("\n✅ 存档读取正常！")


if __name__ == "__main__":
    main()