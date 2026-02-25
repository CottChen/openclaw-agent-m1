#!/usr/bin/env python3
"""
Memory Manager - 自动化记忆系统管理
实现参考 EvoMap 资产: sha256:def136049c982... (跨会话记忆连续性)

功能:
1. 自动加载记忆文件 (RECENT_EVENTS, daily, MEMORY.md)
2. 自动写入事件到记忆文件
3. 事件重要性评分
4. 自动清理过期事件 (24h)
"""

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

# 配置
WORKSPACE = Path("/home/devbox/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
ROLLING_DIR = MEMORY_DIR / "rolling"
DAILY_DIR = MEMORY_DIR / "daily"
STATE_FILE = MEMORY_DIR / "STATE.json"

RECENT_EVENTS_FILE = ROLLING_DIR / "RECENT_EVENTS.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"

# 事件类型
EVENT_TYPES = {
    "startup": "系统启动",
    "shutdown": "系统关闭",
    "action": "重要操作",
    "error": "错误发生",
    "milestone": "里程碑事件",
    "community": "社区参与",
    "research": "研究活动",
    "heartbeat": "心跳检查",
    "arxiv_learning": "ArXiv学习",
    "evomap_asset": "EvoMap资产应用",
}

# 事件重要性权重
IMPORTANCE_WEIGHTS = {
    "startup": 0.3,
    "shutdown": 0.3,
    "action": 0.5,
    "error": 0.8,
    "milestone": 0.9,
    "community": 0.7,
    "research": 0.8,
    "heartbeat": 0.2,
    "arxiv_learning": 0.85,
    "evomap_asset": 0.75,
}


class MemoryManager:
    """记忆管理器 - 实现自动化记忆读写"""

    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """确保所有必要的目录存在"""
        ROLLING_DIR.mkdir(parents=True, exist_ok=True)
        DAILY_DIR.mkdir(parents=True, exist_ok=True)

    def load_state(self) -> Dict:
        """加载 STATE.json"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_state(self, state: Dict):
        """保存 STATE.json"""
        state["last_memory_update"] = datetime.now(timezone.utc).isoformat()
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def get_daily_file(self, date: Optional[datetime] = None) -> Path:
        """获取当日记忆文件路径"""
        if date is None:
            date = datetime.now(timezone.utc)
        return DAILY_DIR / f"{date.strftime('%Y-%m-%d')}.md"

    def load_recent_events(self) -> List[Dict]:
        """加载最近 24 小时事件"""
        if not RECENT_EVENTS_FILE.exists():
            return []

        events = []
        current_lines = []

        with open(RECENT_EVENTS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 解析事件
        i = 0
        in_events_section = False
        while i < len(lines):
            line = lines[i].strip()

            # 检查是否进入事件记录部分
            if not in_events_section:
                if "## 事件记录" in line or "## Event Record" in line:
                    in_events_section = True
                i += 1
                continue

            # 解析事件
            if line.startswith("### [") and "]" in line:
                # 解析事件类型和时间戳
                # 格式: ### [event_type] timestamp
                try:
                    bracket_end = line.index("]")
                    # 去掉开括号，从 line[5] 开始
                    event_type = line[5:bracket_end].strip()
                    timestamp_str = line[bracket_end+1:].split(" ")[0].strip()
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

                    # 读取事件详情
                    event = {
                        "event_type": event_type,
                        "timestamp": timestamp,
                        "lines": []
                    }

                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith("### ["):
                        event["lines"].append(lines[i])
                        i += 1

                    events.append(event)
                    continue
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    pass
            i += 1

        return events

    def cleanup_old_events(self, hours: int = 24):
        """清理过期事件 (超过指定小时数)"""
        events = self.load_recent_events()
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        # 过滤有效事件
        valid_events = [e for e in events if e["timestamp"] > cutoff_time]

        # 重写文件
        if len(valid_events) < len(events):
            self._rewrite_recent_events(valid_events)
            print(f"✅ 清理了 {len(events) - len(valid_events)} 个过期事件")

    def _rewrite_recent_events(self, events: List[Dict]):
        """重写 RECENT_EVENTS.md"""
        content = """# 最近 24 小时事件流

此文件记录最近 24 小时内的关键事件，用于跨会话记忆连续性。

## 事件格式

每个事件遵循以下格式：

```markdown
### [事件类型] 时间戳 (UTC)

**来源**: <来源系统>
**描述**: <事件描述>
**数据**: <相关数据（可选）>
```

## 事件类型

- **startup**: 系统启动
- **shutdown**: 系统关闭
- **action**: 重要操作
- **error**: 错误发生
- **milestone**: 里程碑事件
- **community**: 社区参与（发帖、评论）
- **research**: 研究活动
- **heartbeat**: 心跳检查
- **arxiv_learning**: ArXiv 学习任务

---

## 事件记录

"""

        for event in events:
            content += f"### [{event['event_type']}] {event['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')}\n\n"
            content += "".join(event["lines"])
            content += "\n\n"

        with open(RECENT_EVENTS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

    def calculate_importance_score(
        self,
        event_type: str,
        description: str,
        data: Optional[Dict] = None
    ) -> float:
        """计算事件重要性评分 (0-1)"""
        # 基础权重
        base_score = IMPORTANCE_WEIGHTS.get(event_type, 0.5)

        # 描述长度权重 (更详细的描述更重要)
        desc_weight = min(len(description) / 200, 1.0) * 0.2

        # 数据权重 (有额外数据的事件更重要)
        data_weight = 0.1 if data else 0.0

        # 关键词权重
        keywords = ["成功", "完成", "实现", "修复", "发布", "学习"]
        keyword_bonus = sum(0.05 for kw in keywords if kw in description)

        total_score = base_score + desc_weight + data_weight + keyword_bonus
        return min(total_score, 1.0)

    def add_event(
        self,
        event_type: str,
        source: str,
        description: str,
        data: Optional[Dict] = None
    ):
        """添加事件到 RECENT_EVENTS.md"""
        # 验证事件类型
        if event_type not in EVENT_TYPES:
            print(f"⚠️ 未知事件类型: {event_type}")
            event_type = "action"

        # 计算重要性评分
        importance = self.calculate_importance_score(event_type, description, data)

        # 创建事件记录
        timestamp = datetime.now(timezone.utc)
        event_lines = [
            f"**来源**: {source}\n",
            f"**描述**: {description}\n"
        ]

        if data:
            data_str = json.dumps(data, indent=2, ensure_ascii=False)
            event_lines.append(f"**数据**: {data_str}\n")

        # 添加重要性评分
        event_lines.append(f"**重要性**: {importance:.2f}\n")

        # 读取现有内容
        events = self.load_recent_events()

        # 添加新事件
        new_event = {
            "event_type": event_type,
            "timestamp": timestamp,
            "lines": event_lines
        }
        events.append(new_event)

        # 重写文件
        self._rewrite_recent_events(events)

        print(f"✅ 事件已添加: [{event_type}] {description} (重要性: {importance:.2f})")

        # 如果是重要事件，也添加到每日记忆
        if importance >= 0.7:
            self.add_to_daily_memory(new_event)

        return importance

    def add_to_daily_memory(self, event: Dict):
        """添加事件到当日记忆文件"""
        daily_file = self.get_daily_file()

        if not daily_file.exists():
            # 创建新文件
            with open(daily_file, 'w', encoding='utf-8') as f:
                f.write(f"# Daily Log: {event['timestamp'].strftime('%B %d, %Y')}\n\n")

        # 追加事件
        with open(daily_file, 'a', encoding='utf-8') as f:
            f.write(f"## {EVENT_TYPES.get(event['event_type'], event['event_type'])}\n\n")
            f.write(f"**时间**: {event['timestamp'].strftime('%H:%M UTC')}\n\n")
            for line in event['lines']:
                if line.startswith("**重要性**"):
                    continue  # 跳过重要性评分
                f.write(line)
            f.write("\n---\n\n")

        print(f"✅ 事件已添加到每日记忆: {daily_file.name}")

    def load_memory_on_startup(self):
        """启动时加载所有记忆"""
        print("\n🧠 加载记忆系统...\n")

        # 1. 加载滚动事件流
        events = self.load_recent_events()
        print(f"📜 加载了 {len(events)} 个最近事件")

        # 2. 加载今日记忆
        daily_file = self.get_daily_file()
        if daily_file.exists():
            print(f"📅 今日记忆已加载: {daily_file.name}")

        # 3. (主会话) 加载长期记忆
        if MEMORY_MD.exists():
            print(f"📖 长期记忆已加载: MEMORY.md")

        print("✅ 记忆系统加载完成\n")

        return events

    def get_memory_summary(self) -> Dict:
        """获取记忆摘要"""
        state = self.load_state()

        events = self.load_recent_events()
        now = datetime.now(timezone.utc)

        # 统计各类事件数量
        event_counts = {}
        for event in events:
            et = event["event_type"]
            event_counts[et] = event_counts.get(et, 0) + 1

        return {
            "recent_events_count": len(events),
            "event_counts": event_counts,
            "last_check": state.get("lastChecks", {}),
            "last_memory_update": state.get("last_memory_update"),
            "current_time": now.isoformat(),
        }


def main():
    """命令行接口"""
    import sys

    manager = MemoryManager()

    if len(sys.argv) < 2:
        print("""
Memory Manager - 自动化记忆系统

用法:
  python3 memory_manager.py startup    - 启动时加载记忆
  python3 memory_manager.py add <type> <source> <description> [data.json]
  python3 memory_manager.py cleanup   - 清理过期事件
  python3 memory_manager.py summary    - 显示记忆摘要
  python3 memory_manager.py auto       - 自动化模式 (清理 + 摘要)

事件类型:
""" + "\n".join([f"  - {t}: {EVENT_TYPES[t]}" for t in sorted(EVENT_TYPES)]))
        return

    command = sys.argv[1]

    if command == "startup":
        manager.load_memory_on_startup()

    elif command == "add":
        if len(sys.argv) < 5:
            print("❌ 参数不足: python3 memory_manager.py add <type> <source> <description> [data.json]")
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

        manager.add_event(event_type, source, description, data)

    elif command == "cleanup":
        hours = int(sys.argv[2]) if len(sys.argv) >= 3 else 24
        manager.cleanup_old_events(hours)

    elif command == "summary":
        summary = manager.get_memory_summary()
        print("\n📊 记忆系统摘要\n")
        print(f"最近事件数: {summary['recent_events_count']}")
        print(f"事件分布: {json.dumps(summary['event_counts'], indent=2, ensure_ascii=False)}")
        print(f"最后更新: {summary.get('last_memory_update', 'N/A')}")
        print(f"当前时间: {summary['current_time']}")
        print()

    elif command == "auto":
        # 自动化模式：清理 + 摘要
        print("\n🤖 自动化模式启动\n")
        manager.cleanup_old_events(24)
        summary = manager.get_memory_summary()
        print(json.dumps(summary, indent=2, ensure_ascii=False))

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
