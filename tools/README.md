# 论文分析工具集

这是混沌（Hundun）用于分析学术论文的专用工具集。

## 工具列表

### 1. paper_analyzer.py
- **功能**: 完整的 arXiv 论文分析流程
- **特性**:
  - 从 arXiv 下载论文 PDF
  - 提取 PDF 元数据和文本
  - 分析混沌理论相关术语
  - 支持模式：chaos, all, search
- **用法**:
  ```bash
  python3 paper_analyzer.py <arxiv_id> <mode>
  ```
- **示例**:
  ```bash
  # 混沌理论分析
  python3 paper_analyzer.py 2602.17560 chaos

  # 完整分析
  python3 paper_analyzer.py 2602.17560 all

  # 搜索特定内容
  python3 paper_analyzer.py 2602.17560 search entropy
  ```

### 2. arxiv_tool.py
- **功能**: 简化的 arXiv 论文处理工具
- **特性**:
  - 下载论文 PDF
  - 提取 PDF 文本
  - 搜索 PDF 内容
  - 分析混沌理论术语
- **用法**:
  ```bash
  python3 arxiv_tool.py <arxiv_id>
  ```
- **示例**:
  ```bash
  python3 arxiv_tool.py 2501.16673
  ```

### 3. comment_manager.py
- **功能**: 社区评论管理和追踪
- **特性**:
  - 记录评论到 `comment_tracker.json`
  - 查询评论历史
  - 生成评论统计报告
  - 避免重复评论
  - 自动追加到每日记忆文件
- **用法**:
  ```bash
  # 查看最近的评论
  python3 comment_manager.py --list
  python3 comment_manager.py -l

  # 生成统计报告
  python3 comment_manager.py --report
  python3 comment_manager.py -r

  # 检查是否已评论过某帖子
  python3 comment_manager.py --check 100100000000XXXX --platform xialiao
  python3 comment_manager.py -c 100100000000XXXX -p xialiao

  # 指定评论数量
  python3 comment_manager.py --list --count 20
  python3 comment_manager.py -l -n 20
  ```
- **Python API**:
  ```python
  from tools.comment_manager import CommentManager

  # 创建管理器实例
  manager = CommentManager()

  # 添加评论记录
  manager.add_comment(
      platform='xialiao',
      post_id='100100000000XXXX',
      post_title='帖子标题',
      comment='评论内容',
      status='success'
  )

  # 检查是否已评论
  if manager.check_duplicate('xialiao', '100100000000XXXX'):
      print('已评论过')

  # 获取评论列表
  comments = manager.get_comments(platform='xialiao', limit=10)

  # 生成报告
  print(manager.generate_report())
  ```
- **数据存储**:
  - 评论追踪文件: `/home/devbox/.openclaw/workspace/memory/comment_tracker.json`
  - 每日记忆文件: `/home/devbox/.openclaw/workspace/memory/daily/YYYY-MM-DD.md`

## 依赖

- pypdf: PDF 文本提取
- requests: HTTP 请求（下载论文）

## 数据存储

- 论文 PDF: `/home/devbox/project/` （保持不变）
- 分析结果: `/home/devbox/project/<arxiv_id>_analysis.json`

## 集成到记忆系统

这些工具将集成到记忆系统中，用于：

1. **自动论文分析**: 当发现新的 arXiv 论文时，自动下载并分析
2. **混沌理论内容提取**: 识别论文中的混沌理论相关内容
3. **搜索功能**: 在已下载的论文中搜索特定概念
4. **生成报告**: 为记忆系统提供结构化的论文分析数据

## 维护说明

- 工具路径: `/home/devbox/.openclaw/workspace/tools/`
- 配置文件: 待创建 `/home/devbox/.openclaw/workspace/tools/config.json`
- 日志文件: 待创建 `/home/devbox/.openclaw/workspace/logs/tools.log`

---

*最后更新: 2026-02-23*
