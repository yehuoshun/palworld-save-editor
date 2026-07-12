"""
测试脚本：验证存档读取功能。
用法：python test_reader.py <Level.sav>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.parsers import extract_pal_detail, extract_pals, extract_players, extract_save_info
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

    # 测试帕鲁详情
    pals = extract_pals(data)
    if pals:
        first = pals[0]
        detail = extract_pal_detail(data, str(first["instance_id"]))
        if detail:
            print(f"\n=== 帕鲁详情示例 ===")
            print(f"  名称: {detail['nickname']} ({detail['character_id']})")
            print(f"  等级: {detail['level']}  性别: {detail['gender']}")
            print(f"  HP: {detail['hp']}/{detail['max_hp']}")
            print(f"  天赋: HP+{detail['talent_hp']} 攻+{detail['talent_attack']} 防+{detail['talent_defense']}")
            print(f"  魂强化: HP+{detail['soul_hp']} 攻+{detail['soul_attack']} 防+{detail['soul_defense']} 手工+{detail['soul_craftspeed']}")
            print(f"  星级: {detail['star_rank']}  亲密度: {detail['friendship']}")
            print(f"  主动技能: {len(detail['active_skills'])} 个")
            print(f"  被动技能: {len(detail['passive_skills'])} 个")
            print(f"  工作适应: {detail['work_suitability']}")

    print("\n✅ 存档读取正常！")


if __name__ == "__main__":
    main()