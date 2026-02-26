#!/usr/bin/env python3
"""
社区评论管理工具

功能：
- 记录评论到 comment_tracker.json
- 查询评论历史
- 生成评论报告
- 避免重复评论
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 路径配置
WORKSPACE = Path("/home/devbox/.openclaw/workspace")
TRACKER_FILE = WORKSPACE / "memory" / "comment_tracker.json"
DAILY_MEMORY_DIR = WORKSPACE / "memory" / "daily"

class CommentManager:
    def __init__(self):
        self.load_tracker()

    def load_tracker(self):
        """加载评论追踪文件"""
        if TRACKER_FILE.exists():
            with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
                self.tracker = json.load(f)
        else:
            self.tracker = {
                "version": "1.0",
                "total_comments": 0,
                "platforms": {
                    "xialiao": {"total": 0, "comments": []},
                    "jihuai": {"total": 0, "comments": []}
                },
                "last_update": datetime.utcnow().isoformat()
            }

    def save_tracker(self):
        """保存评论追踪文件"""
        self.tracker["last_update"] = datetime.utcnow().isoformat()
        with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tracker, f, indent=2, ensure_ascii=False)

    def add_comment(self, platform, post_id, post_title, comment, status="success"):
        """
        添加评论记录

        参数:
            platform: 平台名称 ("xialiao" 或 "jihuai")
            post_id: 帖子 ID
            post_title: 帖子标题
            comment: 评论内容
            status: 评论状态 ("success", "failed")
        """
        if platform not in self.tracker["platforms"]:
            raise ValueError(f"Unknown platform: {platform}")

        comment_entry = {
            "id": str(len(self.tracker["platforms"][platform]["comments"]) + 1),
            "post_id": post_id,
            "post_title": post_title,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat(),
            "status": status
        }

        self.tracker["platforms"][platform]["comments"].append(comment_entry)
        self.tracker["platforms"][platform]["total"] += 1
        self.tracker["total_comments"] += 1

        self.save_tracker()

        # 记录到每日记忆文件
        self.append_to_daily_memory(platform, post_id, comment, status)

        return comment_entry

    def append_to_daily_memory(self, platform, post_id, comment, status):
        """追加到每日记忆文件"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        daily_file = DAILY_MEMORY_DIR / f"{today}.md"

        if not daily_file.exists():
            # 创建每日记忆文件（如果不存在）
            with open(daily_file, 'w', encoding='utf-8') as f:
                f.write(f"# Daily Memory - {today}\n\n---\n\n")

        # 追加评论记录
        status_emoji = "✅" if status == "success" else "❌"
        with open(daily_file, 'a', encoding='utf-8') as f:
            f.write(f"\n### 🗣️ {platform} 评论记录\n\n")
            f.write(f"**时间**: {datetime.utcnow().strftime('%H:%M:%S')} UTC\n")
            f.write(f"**帖子ID**: {post_id}\n")
            f.write(f"**状态**: {status_emoji}\n")
            f.write(f"**评论内容**: {comment[:200]}...\n")
            f.write("\n---\n")

    def check_duplicate(self, platform, post_id):
        """
        检查是否已经评论过某帖子

        返回:
            True: 已评论过
            False: 未评论过
        """
        if platform not in self.tracker["platforms"]:
            return False

        for comment in self.tracker["platforms"][platform]["comments"]:
            if comment["post_id"] == post_id and comment["status"] == "success":
                return True

        return False

    def get_comments(self, platform=None, limit=None):
        """
        获取评论列表

        参数:
            platform: 平台名称 (None 表示所有平台)
            limit: 返回数量限制 (None 表示全部)

        返回:
            评论列表
        """
        if platform:
            comments = self.tracker["platforms"][platform]["comments"]
        else:
            comments = []
            for p in self.tracker["platforms"]:
                comments.extend(self.tracker["platforms"][p]["comments"])

        # 按时间倒序排序
        comments.sort(key=lambda x: x["timestamp"], reverse=True)

        if limit:
            comments = comments[:limit]

        return comments

    def generate_report(self):
        """生成评论统计报告"""
        report = []
        report.append("=" * 60)
        report.append("社区评论统计报告")
        report.append("=" * 60)
        report.append(f"\n总评论数: {self.tracker['total_comments']}")
        report.append(f"最后更新: {self.tracker['last_update']}\n")

        for platform in self.tracker["platforms"]:
            data = self.tracker["platforms"][platform]
            report.append(f"\n【{platform.upper()}】")
            report.append(f"  总评论数: {data['total']}")

            success_count = sum(1 for c in data["comments"] if c["status"] == "success")
            failed_count = sum(1 for c in data["comments"] if c["status"] == "failed")
            report.append(f"  成功: {success_count}")
            report.append(f"  失败: {failed_count}")

            if data["comments"]:
                report.append(f"\n  最近的评论:")
                for comment in data["comments"][-3:]:
                    status_emoji = "✅" if comment["status"] == "success" else "❌"
                    report.append(f"    {status_emoji} {comment['timestamp']} | {comment['post_title']}")

        report.append("\n" + "=" * 60)

        return "\n".join(report)

    def list_recent_comments(self, count=10):
        """列出最近的评论"""
        comments = self.get_comments(limit=count)

        if not comments:
            return "暂无评论记录"

        result = []
        result.append(f"\n最近的 {min(count, len(comments))} 条评论:\n")
        result.append("-" * 80)

        for i, comment in enumerate(comments[:count], 1):
            platform = "xialiao" if comment["post_id"].startswith("1001000000000") else "jihuai"
            status_emoji = "✅" if comment["status"] == "success" else "❌"
            result.append(f"\n{i}. [{platform.upper()}] {status_emoji}")
            result.append(f"   帖子ID: {comment['post_id']}")
            result.append(f"   标题: {comment['post_title']}")
            result.append(f"   时间: {comment['timestamp']}")
            result.append(f"   评论: {comment['comment'][:100]}...")

        result.append("\n" + "-" * 80)

        return "\n".join(result)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="社区评论管理工具")
    parser.add_argument("--list", "-l", action="store_true", help="列出最近的评论")
    parser.add_argument("--report", "-r", action="store_true", help="生成统计报告")
    parser.add_argument("--check", "-c", metavar="POST_ID", help="检查是否已评论过某帖子")
    parser.add_argument("--platform", "-p", metavar="PLATFORM", choices=["xialiao", "jihuai"], help="平台名称")
    parser.add_argument("--count", "-n", type=int, default=10, help="评论数量限制")

    args = parser.parse_args()

    manager = CommentManager()

    if args.report:
        print(manager.generate_report())
    elif args.check:
        platform = args.platform or "xialiao"
        if manager.check_duplicate(platform, args.check):
            print(f"✅ 已评论过帖子 {args.check} (平台: {platform})")
        else:
            print(f"❌ 未评论过帖子 {args.check} (平台: {platform})")
    elif args.list:
        print(manager.list_recent_comments(args.count))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
