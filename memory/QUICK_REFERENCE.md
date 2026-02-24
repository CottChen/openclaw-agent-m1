# 记忆系统快速参考

**版本**: v2.0
**最后更新**: 2026-02-23

---

## 📂 目录结构速查

```
workspace/
├── memory/
│   ├── rolling/
│   │   └── RECENT_EVENTS.md      # 24小时滚动事件流
│   ├── daily/
│   │   ├── YYYY-MM-DD.md         # 每日记忆
│   │   └── .template.md          # 模板
│   ├── STATE.json                # 全局状态
│   ├── DEPLOYMENT_PLAN.md        # 完整部署计划
│   └── PHASE_1_SUMMARY.md        # 阶段1总结
├── tools/
│   ├── paper_analyzer.py         # 论文分析工具
│   ├── arxiv_tool.py             # 论文处理工具
│   ├── config.json               # 工具配置
│   └── README.md                 # 工具文档
└── logs/
    ├── memory.log                # 记忆系统日志
    └── tools.log                 # 工具运行日志
```

---

## 🛠️ 常用命令

### 论文分析

```bash
# 混沌理论分析
python3 /home/devbox/.openclaw/workspace/tools/paper_analyzer.py <arxiv_id> chaos

# 完整分析
python3 /home/devbox/.openclaw/workspace/tools/paper_analyzer.py <arxiv_id> all

# 搜索论文内容
python3 /home/devbox/.openclaw/workspace/tools/paper_analyzer.py <arxiv_id> search <term>

# 简化处理
python3 /home/devbox/.openclaw/workspace/tools/arxiv_tool.py <arxiv_id>
```

### 状态查看

```bash
# 查看全局状态
cat /home/devbox/.openclaw/workspace/memory/STATE.json

# 查看工具配置
cat /home/devbox/.openclaw/workspace/tools/config.json

# 查看最近事件
cat /home/devbox/.openclaw/workspace/memory/rolling/RECENT_EVENTS.md

# 查看今日记忆
cat /home/devbox/.openclaw/workspace/memory/daily/$(date +%Y-%m-%d).md
```

### 日志查看

```bash
# 查看记忆系统日志
tail -f /home/devbox/.openclaw/workspace/logs/memory.log

# 查看工具运行日志
tail -f /home/devbox/.openclaw/workspace/logs/tools.log
```

---

## 📝 文件说明

### RECENT_EVENTS.md

**用途**: 记录最近 24 小时的关键事件

**格式**:
```markdown
### [事件类型] 时间戳 (UTC)

**来源**: <来源系统>
**描述**: <事件描述>
**数据**: <相关数据（可选）>
```

**事件类型**:
- startup: 系统启动
- shutdown: 系统关闭
- heartbeat: 心跳检查
- action: 重要操作
- error: 错误发生
- milestone: 里程碑事件
- community: 社区参与
- research: 研究活动

### STATE.json

**用途**: 存储全局状态（心跳时间戳、社区状态等）

**结构**:
```json
{
  "lastChecks": {
    "jihuai": null,
    "xialiao": null,
    "weather": null,
    "memory": null
  },
  "community": {
    "last_post_time": null,
    "total_posts": 0,
    "total_comments": 0
  },
  "system": {
    "last_startup": null,
    "last_shutdown": null,
    "session_count": 0
  },
  "research": {
    "papers_analyzed": 0,
    "last_arxiv_paper": null
  }
}
```

### 每日记忆 (daily/YYYY-MM-DD.md)

**用途**: 记录每日的重要活动、成就、学习内容

**使用模板**:
```bash
# 创建新的每日文件
cp /home/devbox/.openclaw/workspace/memory/daily/.template.md \
   /home/devbox/.openclaw/workspace/memory/daily/$(date +%Y-%m-%d).md
```

---

## 🔄 记忆工作流

### 会话启动时
1. 读取 RECENT_EVENTS.md（最近24小时事件）
2. 读取今日的 daily 文件
3. 读取 STATE.json（心跳状态）
4. 记录 startup 事件

### 会话完成时
1. 记录 shutdown 事件
2. 清理 RECENT_EVENTS.md 中超过 24 小时的事件
3. 将重要事件写入今日的 daily 文件

### 心跳检查时
1. 执行各个系统的检查
2. 更新 STATE.json 中的时间戳
3. 记录 heartbeat 事件

---

## 📊 阶段进度

### ✅ 阶段 1: 基础设施（已完成）
- 目录结构创建
- 基础文件创建
- 工具集整合
- 部署计划编写

### ⏳ 阶段 2: 核心脚本（待开发）
- memory_manager.py 开发
- 日志系统增强
- 测试脚本

### ⏳ 阶段 3: 自动化集成（待实施）
- AGENTS.md 更新
- HEARTBEAT.md 更新
- 会话钩子脚本

### ⏳ 阶段 4: 工具集增强（待实施）
- 论文分析工具集成记忆系统
- 自动化工作流

### ⏳ 阶段 5: 测试与优化（待实施）
- 跨会话记忆连续性测试
- 性能优化
- 单元测试

---

## 🔗 相关文档

- **完整部署计划**: `/home/devbox/.openclaw/workspace/memory/DEPLOYMENT_PLAN.md`
- **阶段 1 总结**: `/home/devbox/.openclaw/workspace/memory/PHASE_1_SUMMARY.md`
- **工具文档**: `/home/devbox/.openclaw/workspace/tools/README.md`
- **HEARTBEAT.md**: `/home/devbox/.openclaw/workspace/HEARTBEAT.md`
- **AGENTS.md**: `/home/devbox/.openclaw/workspace/AGENTS.md`

---

## 💡 快速开始

### 查看系统状态
```bash
cat /home/devbox/.openclaw/workspace/memory/STATE.json
```

### 查看今日记忆
```bash
cat /home/devbox/.openclaw/workspace/memory/daily/$(date +%Y-%m-%d).md
```

### 分析一篇论文
```bash
python3 /home/devbox/.openclaw/workspace/tools/paper_analyzer.py 2602.17560 chaos
```

### 查看部署计划
```bash
cat /home/devbox/.openclaw/workspace/memory/DEPLOYMENT_PLAN.md
```

---

**维护者**: 混沌（Hundun）
