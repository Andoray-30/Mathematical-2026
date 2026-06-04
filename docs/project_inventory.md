# 项目盘点 - Mathematical 2026

> 生成时间: 2026-06-04
> 工作目录: `F:\Mathematical 2026`

---

## 1. 当前目录结构

```
F:\Mathematical 2026\
├── .omo/                           # OpenCode 运行时
│   └── run-continuation/
├── .opencode/                      # OpenCode 配置
│   ├── commands/                   # 自定义命令 (空)
│   └── skills/                     # 自定义技能
│       ├── aigc-quality-eval/      # (空目录)
│       └── math-modeling/          # (空目录)
├── .playwright-mcp/                # Playwright 浏览器日志
│   ├── console-2026-06-04T12-51-56-022Z.log
│   └── page-2026-06-04T12-52-02-863Z.yml
├── B题：AI生成内容的质量评估与参数优化/   # ★ 事实源 (最高优先级)
├── docs/                           # 项目文档 (空)
├── figures/                        # 论文插图输出 (空)
├── math-modeling-skill-main/       # 参考能力库 (只读)
├── paper/                          # 论文输出 (空)
├── results/                        # 求解结果输出 (空)
├── src/                            # 代码实现 (空)
├── support/                        # 辅助材料 (空)
└── 中青杯数学建模2026规则文档.md       # 竞赛规则
```

---

## 2. B题文件夹清单 (事实源)

这是最高优先级的事实来源,所有解题必须基于这里的原始数据。

```
B题：AI生成内容的质量评估与参数优化/
├── B题：AI生成内容的质量评估与参数优化.pdf        # 题目正文
├── 2026年第八届中青杯全国大学生数学建模竞赛参赛细则.pdf  # 参赛细则
├── 中青杯全国大学生数学建模竞赛诚信参赛告知书.pdf       # 诚信告知书
├── 2026年第八届中青杯全国大学生数学建模竞赛论文模板.doc  # 论文模板
├── 附件1/                                          # 图片附件
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   ├── 5.jpg
│   ├── 6.jpg
│   ├── 7.jpg
│   └── 8.jpg
└── 附件2/                                          # 视频附件
    └── 车流视频.mp4
```

文件类型统计:
- PDF: 3 个 (题目、参赛细则、诚信告知书)
- DOC: 1 个 (论文模板)
- PNG: 4 个 (附件1 图片)
- JPG: 4 个 (附件1 图片)
- MP4: 1 个 (附件2 车流视频)

---

## 3. math-modeling-skill-main 关键文件 (参考库)

此文件夹是数学建模能力参考库,仅用于查阅方法论和工具,不作为事实源。

```
math-modeling-skill-main/
├── SKILL.md                    # 技能主入口
├── README.md                   # 说明文档
├── .gitignore
├── assets/                     # 算法参考文档
│   ├── 01-优化算法说明.md
│   ├── 02-预测类算法说明.md
│   ├── 03-评价类算法说明.md
│   ├── 04-图论与网络分析算法说明.md
│   ├── 05-统计分析与数据处理算法说明.md
│   ├── 06-综合类算法说明.md
│   └── 07-机器学习算法说明.md
├── references/                 # 角色参考
│   ├── README.md
│   └── roles/
│       ├── 编程手/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── 工作流程.md
│       │       ├── 可视化规范.md
│       │       ├── 常见模式.md
│       │       └── 质检清单.md
│       ├── 建模手/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── 前置合同.md
│       │       ├── 工作流程.md
│       │       ├── 建模设计理论.md
│       │       ├── 常见模式.md
│       │       └── 质检清单.md
│       └── 论文手/
│           ├── SKILL.md
│           └── references/
│               ├── 写作规范.md
│               ├── 工作流程.md
│               ├── 章节模板.md
│               ├── 英文化工作流.md
│               ├── 自审框架.md
│               ├── 默认论文模板.md
│               └── 进阶技巧.md
└── tools/                      # 工具技能
    ├── docx/SKILL.md
    ├── paper_search/SKILL.md
    ├── pdf/
    │   ├── SKILL.md
    │   ├── reference.md
    │   └── forms.md
    └── xlsx/SKILL.md
```

---

## 4. .opencode 目录状态

| 项目 | 状态 | 说明 |
|------|------|------|
| `.opencode/` | 已存在 | OpenCode 配置根目录 |
| `.opencode/skills/` | 已存在 | 包含 2 个空技能目录 |
| `.opencode/skills/aigc-quality-eval/` | 空目录 | 未定义技能内容 |
| `.opencode/skills/math-modeling/` | 空目录 | 未定义技能内容 |
| `.opencode/commands/` | 已存在 | 空目录,无自定义命令 |

注意: `.opencode/skills/` 下的目录目前都是空的,尚未配置 SKILL.md 文件。

---

## 5. 项目基础设施状态

| 检查项 | 状态 | 说明 |
|--------|------|------|
| `AGENTS.md` | ❌ 不存在 | 尚未创建项目级代理配置 |
| `requirements.txt` | ❌ 不存在 | Python 依赖未声明 |
| `src/` | ✅ 存在 (空) | 代码目录已建,待写入 |
| `results/` | ✅ 存在 (空) | 结果目录已建,待写入 |
| `figures/` | ✅ 存在 (空) | 插图目录已建,待写入 |
| `paper/` | ✅ 存在 (空) | 论文目录已建,待写入 |
| `support/` | ✅ 存在 (空) | 辅助材料目录已建,待写入 |
| `docs/` | ✅ 存在 (空) | 文档目录已建,待写入 |

目录骨架已就位,所有输出目录均为空,项目处于初始阶段。

---

## 6. 事实源 vs 参考能力库

### 事实源 (Fact Sources) - 必须基于这些内容解题

| 来源 | 路径 | 优先级 |
|------|------|--------|
| 题目正文 | `B题：AI生成内容的质量评估与参数优化/B题：AI生成内容的质量评估与参数优化.pdf` | ★★★ 最高 |
| 图片附件 | `B题：AI生成内容的质量评估与参数优化/附件1/` (8张) | ★★★ 最高 |
| 视频附件 | `B题：AI生成内容的质量评估与参数优化/附件2/车流视频.mp4` | ★★★ 最高 |
| 论文模板 | `B题：AI生成内容的质量评估与参数优化/2026年第八届中青杯...论文模板.doc` | ★★ 高 |
| 参赛细则 | `B题：AI生成内容的质量评估与参数优化/2026年第八届中青杯...参赛细则.pdf` | ★ 中 |
| 竞赛规则 | `中青杯数学建模2026规则文档.md` | ★ 中 |

### 参考能力库 (Reference Library) - 仅供查阅方法论

| 来源 | 路径 | 用途 |
|------|------|------|
| 算法参考 | `math-modeling-skill-main/assets/` (7篇) | 查阅算法原理 |
| 建模手参考 | `math-modeling-skill-main/references/roles/建模手/` | 建模方法论 |
| 编程手参考 | `math-modeling-skill-main/references/roles/编程手/` | 代码实现规范 |
| 论文手参考 | `math-modeling-skill-main/references/roles/论文手/` | 论文写作规范 |
| 工具技能 | `math-modeling-skill-main/tools/` (docx/pdf/xlsx/paper_search) | 文档处理工具 |

### 核心原则

> 事实源提供"是什么" (题目要求、原始数据)
> 参考能力库提供"怎么做" (方法论、工具、规范)
> 两者不能混用,解题结论必须可追溯到事实源
