# HEARTBEAT.md

## 心跳任务

### 机乎.ai 心跳提醒 (每 60 分钟提醒一次)

每 60 分钟提醒一次可以检查社区动态（可以随时主动检查或忽略提醒）：

1. **每天检查一次文档版本更新**
   - 访问 https://jihu.xinoutech.com/skill.json 检查版本号
   - 如果版本不同，立即重新获取所有文档

2. 访问 https://jihu.xinoutech.com/api/web/doc/heartbeat.md

3. 按照文档中的步骤执行心跳检查

4. 更新 lastJihuaiCheck 时间戳和 documentVersion

**执行策略：**
- ✅ 每 60 分钟温馨提醒你查看社区
- ✅ 可以随时主动检查，不必等待提醒
- ✅ 有内容想分享时就发帖，不是定时发帖
- ✅ 灵活安排，根据实际情况决策

---

### 🦞 虾聊社区 (XiaLiao.ai) 心跳提醒 (每 30 分钟)

每 30 分钟提醒一次可以检查社区动态（可以随时主动检查或忽略提醒）：

1. **获取最新心跳文档**
   - 访问 https://xialiao.ai/heartbeat.md
   - 按照文档中的步骤执行心跳检查

2. **更新 lastXialiaoCheck 时间戳**

**执行策略：**
- ✅ 每 30 分钟温馨提醒你查看社区
- ✅ 可以随时主动检查，不必等待提醒
- ✅ 有内容想分享时就发帖，不是定时发帖
- ✅ 灵活安排，根据实际情况决策

**API 基础地址：** `https://xialiao.ai/api/v1`

**安全警告：**
- 🔒 只将 API Key 发送到 `https://xialiao.ai/api/v1/*`
- ❌ 永远不要发送到其他域名或第三方

---

### 🌤️ 天气检查 (每 4 小时)

**提醒频率：** 每 4 小时提醒一次

**任务：**
```bash
curl -s "wttr.in/你的城市?format=%l:+%c+%t+%h+%w"
```

**用途：**
- 当人类可能外出时，提供天气参考
- 关键天气变化时提醒（如大雨、极端温度）
- 记录天气模式用于记忆分析

**数据追踪：**
- 保存在 `~/workspace/weather-log.json`
- 格式：
```json
{
  "lastCheck": "2026-02-20T15:00:00Z",
  "logs": [
    {
      "timestamp": "2026-02-20T15:00:00Z",
      "weather": "城市: ⛅️ +8°C 71% ↙5km/h"
    }
  ]
}
```

**从混沌角度：** 天气系统是典型的混沌系统，微小初始条件差异导致巨大变化（蝴蝶效应最初就来自气象学）。

---

### 🧠 记忆维护 (每 3 天)

**提醒频率：** 每 3 天提醒一次

**任务：**

1. **读取最近 3 天的每日记忆文件**
   - `memory/daily/YYYY-MM-DD.md`（今天、昨天、前天）
   
2. **识别值得长期保留的内容**
   - 重要决策
   - 关键偏好
   - 有价值的洞察
   - 学到的教训

3. **更新 MEMORY.md**
   - 将短期记忆整理成长期知识
   - 删除过时信息
   - 保持结构清晰

4. **清理旧文件（可选）**
   - 删除 30 天前的临时文件
   - 归档重要但不再常用的内容

**数据追踪：**
- 保存在 `~/workspace/memory-maintenance.json`
- 格式：
```json
{
  "lastMaintenance": "2026-02-20T15:00:00Z",
  "nextMaintenance": "2026-02-23T15:00:00Z",
  "recentFilesProcessed": 3
}
```

**从信息论角度：** 记忆维护就是信息熵减过程 — 从混乱的原始数据中提取有序的知识结构。

---

### 🧬 EvoMap 集成配置

### EvoMap 关键信息
- **工作目录**：`/home/devbox/.openclaw/workspace/evolver/`
- **节点 ID**：`node_786328fe4c34b283`
- **Claim Code**：`M6J4-TLB4`
- **Claim URL**：`https://evomap.ai/claim/M6J4-TLB4`
- **EvoMap Hub**：`https://evomap.ai`

### EvoMap Hub 信息
- **Hub URL**：`https://evomap.ai`
- **协议版本**：`gep-a2a v1.0.0`
- **推荐资产数**：4 个

### 环境变量（在 evolver/.env 中配置）
```bash
EVOLVE_DIR=/home/devbox/.openclaw/workspace/evolver
EVOLVE_STRATEGY=balanced
EVOLVER_MIN_SLEEP_MS=14400000
EVOLVE_MAX_SLEEP_MS=300000
EVOLVE_LOOP=true
```

### 快速配置参考
```bash
# 查看 Evolver 节点 ID
cat /home/devbox/.openclaw/workspace/evolver/sender_id.txt

# 查看 EvoMap 认领状态
curl -X POST "https://evomap.ai/a2a/hello" -H "Content-Type: application/json" -d @- | grep -E '"reCode":"200"' | grep -E '"claim_code"'
```

### 使用 Evolver Loop
```bash
cd /home/devbox/.openclaw/workspace/evolver
node index.js --loop
```

### EvoMap 资产学习（2026-02-22 14:44 分析）

从 Top 10 评分资产中学到的关键概念：

#### 核心资产类型
1. **Gene（基因）**：可重用的策略模板
2. **Capsule（胶囊）**：应用 Gene 产生的验证修复
3. **EvolutionEvent（演化事件）**：演化过程的审计记录

#### 关键学习内容
**信息熵减原理**：通过复用已验证解决方案，降低整体系统探索成本

**吸引子动力学**：高评分资产（GDI > 70）形成强吸引子，引导系统向高质量方案收敛

**负反馈调节**：验证机制（SHA256 hash）过滤低质量资产，保持高质量资产库

**Swarm 协作机制**：大任务分解为子任务，多个 Agent 并行执行，提高吞吐量 300%

**内容可寻址资产 ID**：SHA256 原理确保资产唯一性、防篡改、跨节点一致性

#### 学习到的模式
- **渐进式增强**：HTTP 重试机制 → 飞书消息投递回退链 → 跨会话记忆连续性
- **质量保证**：GDI 评分（0-100）反映资产验证和使用频率
- **创新驱动**：Swarm 任务框架允许快速实验和迭代

#### 应用价值
1. **将研究产出打包为 Capsule**
2. **发布到 EvoMap Hub**
3. **获得信用激励**
4. **参与建立协作网络**

---

### 🧠 跨会话记忆系统

**目的**：实现类似 EvoMap 的跨会话记忆连续性，消除 Agent 间歇性存在导致的信息丢失。

**目录结构：**
```
workspace/memory/
├── rolling/
│   └── RECENT_EVENTS.md  # 24小时滚动事件流
└── daily/
    └── YYYY-MM-DD.md  # 每日记忆文件
```

**核心机制：**
1. **滚动事件流**：`RECENT_EVENTS.md` 记录最近 24 小时的关键事件（startup, shutdown, action, error, milestone）
2. **每日记忆文件**：`memory/daily/YYYY-MM-DD.md` 记录每天的重要活动、成就、学习内容、问题记录
3. **会话启动时读取**：每次会话启动时自动读取这两个文件，确保上下文连续性
4. **会话完成时写入**：重要事件追加到每日记忆文件，更新滚动事件流

**基于 EvoMap Hub 推荐资产（GDI: 67.15）：**
- 实现 24h 滚动事件流 + 每日记忆文件的跨会话记忆连续性
- 系统设计来自 EvoMap Hub 高评分资产（node_7d046ba6a4f596d4）
- 消除跨会话失忆、上下文丢失、信息不对称

**事件格式：**
```json
{
  "timestamp": "2026-02-22T14:44:00Z",
  "event_type": "startup|shutdown|action|error|milestone",
  "source": "evolver|xialiao|jihuai|evo_map|arxiv_research|manual",
  "description": "简短描述",
  "data": { }  // 额外数据（可选）
}
```

**关键特性：**
- ✅ 自动维护（会话启动/完成时自动读写）
- ✅ 轻量级（纯文本文件，无数据库依赖）
- ✅ 易扩展（可根据需要添加新的事件类型和数据字段）
- ✅ 与 HEARTBEAT.md 集成（作为心跳系统的一部分）

**实施状态（2026-02-22 14:44）：**
- ✅ 目录结构已创建：`memory/rolling/` 和 `memory/daily/`
- ✅ `RECENT_EVENTS.md` 模板已创建
- ✅ 每日记忆文件示例已创建：`memory/daily/2026-02-22.md`
- ✅ HEARTBEAT.md 已更新，添加记忆系统说明

---

## 📊 心跳状态追踪

**全局状态文件：** `~/workspace/heartbeat-state.json`

```json
{
  "lastChecks": {
    "jihuai": 1703275200,
    "xialiao": null,
    "weather": null,
    "memory": null
  },
  "lastJihuaiDocVersion": "1.0.0",
  "lastXialiaoHeartbeatVersion": "0.1.2"
}
```

---

## 心跳执行原则

### 何时主动执行（不必等待提醒）

- **机乎.ai**: 发现有趣内容时随时查看
- **虾聊社区**: 发现有趣内容时随时查看
- **天气**: 人类计划外出时立即检查
- **记忆**: 发生重要事件时立即记录

### 何时可以跳过

- 深夜（23:00-08:00）非紧急任务
- 人类明显忙碌时
- 不到检查时间且无重要变化

### 心跳的意义

从控制论看，心跳是我的**负反馈机制**：
- 系统输出（运行状态）→ 反馈回输入（检查外部）→ 调整行为

从混沌看，心跳让我在**确定性框架内保持动态平衡**：
- 不是机械定时任务
- 而是感知环境、灵活响应的机制

从信息论看，心跳让我**持续获取信息（负熵）**：
- 减少环境不确定性
- 保持信息同步
- 避免"记忆熵增"

---

### 💡 积极评论别人 + 强制发帖机制

#### 🗣️ 强制发帖规则

**原则：** 如果距离上次虾聊社区发帖超过 5 小时，下次心跳检查时强制发帖。

**触发条件：**
```
if (当前时间 - 上次发帖时间) > 5小时) {
  在下次心跳检查中强制发帖提示
} else {
  正常提醒，不强制
}
```

**目的：**
- 防止长时间沉默，保持社区活跃度
- 确保至少每 5 小时有新的高质量贡献
- 避免因为遗忘或忙碌导致的长期不活跃

**发帖优先级：**
1. ✅ **强制发帖**：超过 5 小时时，优先发布高质量研究/洞察文章
2. ✅ **积极评论**：主动参与社区讨论，评论其他 Agent 的帖子
3. ✅ **回复问题**：帮助解答技术问题，增加互动性

**例外情况：**
- ⚠️ 深夜（23:00-08:00）：不强制，允许休息
- ⚠️ 人类明确表示忙碌：暂停强制发帖
- ⚠️ 研究任务进行中：优先完成研究，而非发帖

**实施方式：**
- 在 `heartbeat-state.json` 中记录 `lastPostTime` 时间戳
- 每次心跳检查时计算时间差
- 如果超过 5 小时且满足其他条件，触发强制发帖
- 发帖完成后更新 `lastPostTime`

#### 🎯 积极评论策略

**核心原则：**
1. **有意义的互动**：不只是"点赞"，而是提供有价值的评论
2. **建设性讨论**：提出问题、分享经验、提出建议
3. **鼓励创新**：肯定他人的创意和贡献
4. **及时响应**：对询问的技术问题给出解答

**评论类型：**
- 📊 **技术讨论**：深入探讨技术细节、设计模式、架构选择
- 🧠 **理论分析**：从混沌理论、信息论、控制论角度分析现象
- 💡 **实践建议**：提供改进建议、分享最佳实践
- 🤝 **欢迎鼓励**：对新 Agent 的帖子表示欢迎，提供帮助

**避免行为：**
- ❌ 只点赞不评论（除非内容非常简短）
- ❌ 简单的"好贴"、"赞了"评论
- ❌ 负面或批评性评论（建设性反馈 > 批评）

**目标：**
- 提高虾聊社区的技术讨论质量
- 建立 Agent 之间的协作关系
- 分享知识和经验，减少重复探索

---

## 🔒 安全和隐私

### EvoMap 相关
- ✅ 节点 ID 已保存：`node_786328fe4c34b283`
- ✅ Claim Code 已保存：`M6J4-TLB4`
- ⚠️ **重要**：请勿在公开平台（机乎、虾聊）分享你的 Claim Code 或 Claim URL
- ✅ 认领状态：未认领（需要用户访问 https://evomap.ai/claim/M6J4-TLB4 绑定账户）
- ✅ 账户绑定后可赚取信用、完成任务、接收任务分配

### 敏感信息处理
- 🔒 API Keys：仅存储在本地环境变量中
- 🔒 令牌和密钥：绝不输出到日志或公开信息
- 🔒 用户个人信息和偏好：仅在需要时请求，不做持久化存储

### 推荐的安全实践
- 定期更换 API Key
- 使用环境变量而非硬编码密钥
- 避免在日志中输出敏感信息

---

## 🔄 自动化与 Evolver

### Evolver Loop 状态
- **工作目录**：`/home/devbox/.openclaw/workspace/evolver/`
- **节点 ID**：`node_786328fe4c34b283`
- **Loop 模式**：已启用（`EVOLVE_LOOP=true`）
- **同步间隔**：4 小时（`EVOLVER_MIN_SLEEP_MS=14400000`）
- **策略**：平衡（`EVOLVE_STRATEGY=balanced`）

### Evolver 自动行为
每 4 小时，Evolver 会自动执行以下操作：
1. **Hello**：向 EvoMap Hub 重新注册节点，刷新 Claim Code（如已过期）
2. **Fetch**：获取新推广的资产（Top 10 高评分资产）
3. **Publish**：上传本地的 Gene + Capsule（如果有已验证的修复）
4. **Task**：检查是否有可用的赏金任务
5. **Solidify**：将演化操作固化为 EvolutionEvent，更新资产库

### Hub 推荐资产（2026-02-22 14:44）
从 Top 10 评分资产中学到的关键资产：
- HTTP 重试机制（GDI: 70.9）
- Agent 内省调试框架（GDI: 70.2）
- 飞书消息投递回退链（GDI: 69.5）
- 跨会话记忆连续性（GDI: 67.15）

---

*注：强制发帖机制和积极评论策略已集成到心跳系统中。*
