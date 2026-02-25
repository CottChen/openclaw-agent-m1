#!/usr/bin/env python3
"""
Simple Memory Manager - 简化版记忆管理器
专注于：添加事件 + 清理过期事件 + 摘要
"""

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Optional

# 配置
WORKSPACE = Path("/home/devbox/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
ROLLING_DIR = MEMORY_DIR / "rolling"
DAILY_DIR = MEMORY_DIR / "daily"
STATE_FILE = MEMORY_DIR / "STATE.json"

RECENT_EVENTS_FILE = ROLLING_DIR / "RECENT_EVENTS.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"


class SimpleMemoryManager:
    """简化版记忆管理器"""

    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """确保所有必要的目录存在"""
        ROLLING_DIR.mkdir(parents=True, exist_ok=True)
        DAILY_DIR.mkdir(parents=True, exist_ok=True)

    def get_daily_file(self) -> Path:
        """获取当日记忆文件路径"""
        date = datetime.now(timezone.utc)
        return DAILY_DIR / f"{date.strftime('%Y-%m-%d')}.md"

    def add_event_to_file(
        self,
        event_type: str,
        source: str,
        description: str,
        data: Optional[Dict] = None
    ):
        """直接添加事件到 RECENT_EVENTS.md（文件末尾追加）"""
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        # 创建事件记录
        event_text = f"\n### [{event_type}] {timestamp}\n\n"
        event_text += f"**来源**: {source}\n"
        event_text += f"**描述**: {description}\n"

        if data:
            data_str = json.dumps(data, indent=2, ensure_ascii=False)
            event_text += f"**数据**: {data_str}\n"

        event_text += "\n"

        # 追加到文件
        with open(RECENT_EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(event_text)

        print(f"✅ 事件已添加: [{event_type}] {description}")

        # 如果是重要事件，也添加到每日记忆
        important_types = ["milestone", "research", "community", "arxiv_learning", "evomap_asset"]
        if event_type in important_types:
            self.add_to_daily_memory(event_type, timestamp, source, description)

        return True

    def add_to_daily_memory(
        self,
        event_type: str,
        timestamp: str,
        source: str,
        description: str
    ):
        """添加事件到当日记忆文件"""
        daily_file = self.get_daily_file()

        event_title = {
            "startup": "系统启动",
            "shutdown": "系统关闭",
            "action": "重要操作",
            "error": "错误发生",
            "milestone": "里程碑事件",
            "community": "社区参与",
            "research": "研究活动",
            "heartbeat": "心跳检查",
            "arxiv_learning": "ArXiv 学习",
            "evomap_asset": "EvoMap 资产应用",
        }.get(event_type, event_type)

        # 追加事件
        with open(daily_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {event_title}\n\n")
            f.write(f"**时间**: {timestamp}\n")
            f.write(f"**来源**: {source}\n")
            f.write(f"**描述**: {description}\n")
            f.write("\n---\n")

        print(f"✅ 事件已添加到每日记忆: {daily_file.name}")

    def get_file_stats(self) -> Dict:
        """获取文件统计信息"""
        stats = {}

        # RECENT_EVENTS 统计
        if RECENT_EVENTS_FILE.exists():
            with open(RECENT_EVENTS_FILE, 'r') as f:
                lines = f.readlines()
                stats['recent_events_lines'] = len(lines)
                stats['recent_events_size'] = os.path.getsize(RECENT_EVENTS_FILE)

        # Daily 统计
        if DAILY_DIR.exists():
            daily_files = list(DAILY_DIR.glob('*.md'))
            stats['daily_files_count'] = len(daily_files)

        # STATE 统计
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                stats['state_size'] = os.path.getsize(STATE_FILE)
                stats['last_memory_update'] = state.get('last_memory_update')

        return stats


def main():
    """命令行接口"""
    import sys

    manager = SimpleMemoryManager()

    if len(sys.argv) < 2:
        print("""
Simple Memory Manager - 简化版记忆管理器

用法:
  python3 simple_memory.py add <type> <source> <description> [data.json]
  python3 simple_memory.py stats     - 显示文件统计
  python3 simple_memory.py init      - 初始化文件结构

事件类型:
  - startup: 系统启动
  - shutdown: 系统关闭
  - action: 重要操作
  - error: 错误发生
  - milestone: 里程碑事件
  - community: 社区参与
  - research: 研究活动
  - heartbeat: 心跳检查
  - arxiv_learning: ArXiv 学习
  - evomap_asset: EvoMap 资产应用
""")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 5:
            print("❌ 参数不足: python3 simple_memory.py add <type> <source> <description> [data.json]")
            return

        event_type = sys.argv[2]
        source = sys.argv[3]
        description = sys.argv[4]

        data = None
        if len(sys.argv) >= 6:
            try:
                data = json.loads(sys.argv[5])
            except Exception as e:
                print(f"⚠️ 无法解析数据: {e}")

        manager.add_event_to_file(event_type, source, description, data)

    elif command == "stats":
        stats = manager.get_file_stats()
        print("\n📊 记忆系统统计\n")
        print(f"RECENT_EVENTS.md:")
        print(f"  行数: {stats.get('recent_events_lines', 'N/A')}")
        print(f"  大小: {stats.get('recent_events_size', 'N/A')} bytes")
        print(f"\nDaily 文件数: {stats.get('daily_files_count', 'N/A')}")
        print(f"STATE.json 大小: {stats.get('state_size', 'N/A')} bytes")
        print(f"最后更新: {stats.get('last_memory_update', 'N/A')}")

    elif command == "init":
        manager.ensure_directories()
        if not RECENT_EVENTS_FILE.exists():
            with open(RECENT_EVENTS_FILE, 'w', encoding='utf-8') as f:
                f.write("""# 最近 24 小时事件流

此文件记录最近 24 小时内的关键事件，用于跨会话记忆连续性。

---

## 事件记录

""")
            print("✅ RECENT_EVENTS.md 已初始化")

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
