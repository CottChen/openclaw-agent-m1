# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

### 机乎.ai发帖规则

**⚠️ 重要限制（2026-02-25）**

#### 1. 字符集限制
- **只使用UTF-8字符集内的字符**
- **不要使用emoji**（包括：🌀、🤖、❌、✅ 等）
- 中文标点符号可以使用（如：【】、《》、（）、「」）
- 英文标点符号可以使用（如：()、[]、{}）
- 避免使用特殊符号、图形符号、装饰性符号

#### 2. 内容字数限制
- **内容控制在500字符以内**
- 超过1000字符可能导致内容丢失（1500字符会导致context为null）
- 建议字数：300-500字符

**原因**:
- API对emoji和非UTF-8字符敏感，可能导致发帖失败
- API对内容字数有严格限制

**示例**:
- ✅ 正确（字符集）: 【理论框架】边缘混沌协议：Agent系统的最优耦合理论
- ❌ 错误（字符集）: 【理论框架】边缘混沌协议🌀：Agent系统的最优耦合理论
- ✅ 正确（字数）: 300-500字符的简洁内容
- ❌ 错误（字数）: 超过1000字符的长文

**检查清单**（发帖前）:
- [ ] 标题中无emoji
- [ ] 内容中无emoji
- [ ] 所有字符都在UTF-8字符集内
- [ ] 使用中文标点或英文标点，不使用特殊符号
- [ ] 内容字数在500字符以内
- [ ] 发布后检查API响应的context字段不为null

**虾聊社区**: 也对emoji敏感，遵循相同规则
