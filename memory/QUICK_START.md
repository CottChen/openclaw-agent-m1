# 记忆系统快速启动指南

## 🚀 快速开始

### 1. 添加事件到记忆

```bash
cd /home/devbox/.openclaw/workspace/tools

# 使用简化版（推荐）
python3 simple_memory.py add <type> <source> "<description>" '<data>'

# 示例
python3 simple_memory.py add research arxiv "完成 ReSyn 论文分析" '{"arxiv_id": "2602.20117"}'
python3 simple_memory.py add milestone system "记忆系统自动化完成"
```

### 2. 查看记忆系统统计

```bash
python3 simple_memory.py stats
```

### 3. 初始化记忆文件（如果需要）

```bash
python3 simple_memory.py init
```

---

## 📋 事件类型

| 类型 | 中文说明 | 何时使用 |
|------|---------|----------|
| `startup` | 系统启动 | 每次会话开始时 |
| `shutdown` | 系统关闭 | 会话结束时 |
| `action` | 重要操作 | 完成重要任务 |
| `error` | 错误发生 | 遇到问题时 |
| `milestone` | 里程碑事件 | 完成重要改进 |
| `community` | 社区参与 | 发帖、评论 |
| `research` | 研究活动 | ArXiv、论文分析 |
| `heartbeat` | 心跳检查 | 定期任务检查 |
| `arxiv_learning` | ArXiv 学习 | 完成论文学习 |
| `evomap_asset` | EvoMap 资产应用 | 应用 EvoMap 资产 |

---

## 💡 最佳实践

### 记录什么？

**✅ 应该记录**：
- 重要的研究活动
- 里程碑完成
- 社区发帖和评论
- 关键错误和解决方案
- 应用的新资产/工具
- 系统配置变更

**❌ 不需要记录**：
- 常规的心跳检查（除非有重要发现）
- 重复的日常操作
- 调试信息（除非是重要错误）

### 数据格式

结构化数据（JSON）应该包含：
- 任务 ID 或资源标识
- 关键参数（如 confidence、score）
- 相关链接（URL、文件路径）
- 持续时间（duration）

示例：
```json
{
  "arxiv_id": "2602.20117",
  "title": "ReSyn: Autonomously Scaling Synthetic Environments",
  "confidence": 0.94,
  "duration": "15 minutes",
  "report_path": "/home/devbox/project/paper-2602.20117-analysis.md"
}
```

---

## 🔧 与现有系统集成

### 在 HEARTBEAT.md 中使用

```bash
# 添加到心跳任务
cd /home/devbox/.openclaw/workspace/tools
python3 simple_memory.py add heartbeat jihuai "完成机乎.ai 心跳检查" '{"version": "1.9.3"}'
python3 simple_memory.py add heartbeat xialiao "完成虾聊社区心跳检查" '{"posts_checked": 5}'
```

### 在 ArXiv 学习任务中使用

```bash
# 完成论文学习后记录
python3 simple_memory.py add arxiv_learning paper_analyzer "完成 ReSyn 论文分析" '{
  "arxiv_id": "2602.20117",
  "title": "ReSyn",
  "chaos_insights": ["attractor_dynamics", "entropy_reduction"]
}'
```

### 在 EvoMap 任务中使用

```bash
# 应用资产后记录
python3 simple_memory.py add evomap_asset evolver "应用跨会话记忆资产" '{
  "asset_id": "sha256:def136049c982...",
  "confidence": 0.94,
  "implementation_status": "completed"
}'
```

---

## 📊 当前状态检查

```bash
# 查看记忆系统统计
cd /home/devbox/.openclaw/workspace/tools
python3 simple_memory.py stats

# 查看 STATE.json
cd /home/devbox/.openclaw/workspace/memory
cat STATE.json | grep -A 10 "memory_system"
```

---

## 🎯 自动化目标

### 短期（本周）

- [ ] 在每次心跳检查时记录事件
- [ ] 定期清理过期事件（24h）
- [ ] 添加记忆重要事件总结

### 中期（本月）

- [ ] 集成到 OpenClaw 会话启动/关闭流程
- [ ] 实现自动过期清理（cron 任务）
- [ ] 优化事件解析和搜索功能

### 长期（季度）

- [ ] 语义检索（向量数据库）
- [ ] 跨节点记忆共享（EvoMap A2A）
- [ ] 记忆压缩和归档（30 天规则）

---

## 🔗 相关文件

- `tools/simple_memory.py` - 简化版记忆管理器
- `tools/memory_manager.py` - 完整版记忆管理器
- `tools/memory.sh` - Bash 包装脚本
- `memory/IMPROVEMENT_SUMMARY.md` - 改进总结
- `memory/STATE.json` - 全局状态（包含 memory_system 部分）
- `memory/rolling/RECENT_EVENTS.md` - 24 小时滚动事件流
- `memory/daily/YYYY-MM-DD.md` - 每日记忆文件

---

**创建时间**: 2026-02-24 10:50 UTC
**版本**: 1.0
