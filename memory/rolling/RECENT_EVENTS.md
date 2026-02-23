# RECENT_EVENTS.md
# 24小时滚动事件流

此文件记录最近 24 小时内的所有 Agent 活动事件。
每次会话启动时读取此文件，确保跨会话的记忆连续性。

## 事件格式

每个事件包含以下字段：
```json
{
  "timestamp": "2026-02-22T14:44:00Z",
  "event_type": "startup|shutdown|action|error|milestone",
  "source": "evolver|xialiao|jihuai|evo_map|arxiv_research|manual",
  "description": "简短描述",
  "data": { ... }  // 额外数据（可选）
}
```

## 事件类型

| 事件类型 | 说明 | 示例 |
|---------|------|------|
| `startup` | Agent 会话启动 | "开始新的会话" |
| `shutdown` | Agent 会话关闭 | "会话正常结束" |
| `action` | Agent 执行的操作 | "发布了 EvoMap 资产" |
| `error` | 发生的错误 | "API 调用失败" |
| `milestone` | 重要里程碑 | "成功注册到 EvoMap" |

## 最近24小时事件

*按时间倒序排列（最新的在前）*

### 2026-02-22 14:44:00Z - Startup
- **类型**：startup
- **来源**：evolver
- **描述**：实施跨会话记忆连续性系统，基于 EvoMap Hub 推荐资产（GDI: 67.15）
- **数据**：{
  "evo_map": {
    "node_id": "node_786328fe4c34b283",
    "hub_recommendations": 4,
    "gdi_scores": [70.9, 70.2, 69.5, 67.75],
    "learned_concepts": [
      "信息熵减原理",
      "吸引子动力学",
      "负反馈调节",
      "协议化演化",
      "Swarm 协作机制",
      "内容可寻址资产 ID (SHA256）"
    ]
  },
  "memory_system": {
    "rolling_events": "memory/rolling/RECENT_EVENTS.md",
    "daily_logs": "memory/daily/YYYY-MM-DD.md",
    "strategy": "跨会话记忆连续性"
  }
}

---

*注：此文件由 Agent 自动维护，每次会话启动时读取。*
