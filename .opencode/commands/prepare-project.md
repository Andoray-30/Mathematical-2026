---
name: prepare-project
description: "检查项目准备状态 - 验证目录结构、AGENTS.md、skills、requirements"
---

# 准备项目

检查当前项目的准备状态。

## 执行步骤

1. **检查目录结构**
   - 确认 `docs/`, `src/`, `results/`, `figures/`, `paper/`, `support/` 存在
   - 确认 `.opencode/skills/` 和 `.opencode/commands/` 存在

2. **检查核心文件**
   - `AGENTS.md` 是否存在且内容完整
   - `requirements.txt` 是否存在
   - `.opencode/skills/math-modeling/SKILL.md` 是否存在
   - `.opencode/skills/aigc-quality-eval/SKILL.md` 是否存在

3. **检查 B 题文件**
   - `B题：AI生成内容的质量评估与参数优化/` 是否存在
   - PDF、图片、视频文件是否完整

4. **检查 Python 环境**
   - Python 是否安装
   - 虚拟环境是否创建
   - 依赖是否安装

5. **输出状态报告**

## 输出格式

```
## 项目准备状态

### ✅ 已完成
- [x] 目录结构
- [x] AGENTS.md
- ...

### ⚠️ 待完成
- [ ] Python 环境
- [ ] 依赖安装
- ...

### 📋 下一步
1. 安装 Python
2. 创建虚拟环境
3. 安装依赖
```
