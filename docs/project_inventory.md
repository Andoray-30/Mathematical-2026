# 项目盘点 - Mathematical 2026

**更新时间**: 2026-06-04
**项目阶段**: 能力验收完成，进入正式建模准备阶段

---

## 1. 当前目录结构

```
F:\Mathematical 2026\
├── .git/                           # Git 配置
├── .gitignore                      # Git 忽略规则
├── .opencode/                      # OpenCode 配置
│   ├── commands/                   # 命令文件
│   └── skills/                     # 技能文件
├── AGENTS.md                       # 项目规则
├── B题：AI生成内容的质量评估与参数优化/  # 原始赛题资料（只读）
├── archive/                        # 归档目录
│   └── capability_test_2026-06-04/
├── docs/                           # 核心文档
├── figures/                        # 图表目录
│   ├── final/                      # 正式论文图表
│   ├── intermediate/               # 探索分析图
│   └── vision_inputs/              # GPT-5.5 输入材料
├── math-modeling-skill-main/       # 参考能力库（只读）
├── paper/                          # 论文目录
├── requirements.txt                # Python 依赖
├── results/                        # 结果目录
│   ├── final/                      # 正式建模最终结果
│   └── intermediate/               # 正式建模中间表格
├── src/                            # 源代码
├── support/                        # 支撑材料
└── 中青杯数学建模2026规则文档.md    # 竞赛规则
```

---

## 2. 原始赛题资料

**路径**: `B题：AI生成内容的质量评估与参数优化/`
**状态**: 只读保留，禁止修改

| 文件 | 说明 |
|------|------|
| B题：AI生成内容的质量评估与参数优化.pdf | 主题目 |
| 2026年第八届中青杯全国大学生数学建模竞赛参赛细则.pdf | 参赛细则 |
| 2026年第八届中青杯全国大学生数学建模竞赛论文模板.doc | 论文模板 |
| 中青杯全国大学生数学建模竞赛诚信参赛告知书.pdf | 诚信告知书 |
| 附件1/ (8张图片) | AI 生成图像样本 |
| 附件2/车流视频.mp4 | 视频样本 |

---

## 3. 参考能力库

**路径**: `math-modeling-skill-main/`
**状态**: 只读保留，禁止修改

| 目录 | 说明 |
|------|------|
| assets/ | 算法资源库（7 个算法说明） |
| references/ | 建模手/编程手/论文手工作流程 |
| tools/ | pdf/docx/xlsx/paper_search 工具 |

---

## 4. 代码工具链

**路径**: `src/`
**状态**: 保留全部脚本，不做算法改动

| 脚本 | 功能 |
|------|------|
| check_env.py | 环境检查 |
| smoke_test.py | 环境验证 |
| extract_pdf.py | PDF 提取 |
| extract_docx.py | DOCX 提取 |
| inspect_media.py | 媒体检查 |
| image_metrics.py | 图像指标 |
| video_slice.py | 视频抽帧 |
| video_metrics.py | 视频指标 |
| evaluation_models.py | AHP/熵权/TOPSIS |
| export_excel.py | Excel 导出 |
| plot_results.py | 图表生成 |
| main.py | 主流程 |

---

## 5. 正式输出目录

### results/

| 目录 | 用途 |
|------|------|
| results/final/ | 正式建模最终结果 |
| results/intermediate/ | 正式建模中间表格 |

### figures/

| 目录 | 用途 |
|------|------|
| figures/final/ | 正式论文图表 |
| figures/intermediate/ | 探索分析图 |
| figures/vision_inputs/ | GPT-5.5 输入材料 |

---

## 6. 归档目录

**路径**: `archive/capability_test_2026-06-04/`
**状态**: 保留，用于追溯

| 目录 | 内容 |
|------|------|
| docs/ | 6 个测试/提取类文档 |
| results/ | 7 个测试结果文件 |
| figures/ | 11 个测试图表 + 2 个目录 |

---

## 7. 核心文档

**路径**: `docs/`

| 文档 | 说明 |
|------|------|
| project_inventory.md | 本文件 |
| environment_setup.md | 环境配置指南 |
| skill_to_b_problem_mapping.md | Skill 到 B 题映射 |
| vision_review_input_manifest.md | GPT-5.5 输入清单 |
| vision_review_test.md | 多模态审查测试报告 |
| workspace_cleanup_report.md | 工作区清理报告 |
| capability_acceptance_summary.md | 能力验收摘要 |
| multimodal_routing_policy.md | 多模态路由策略 |

---

*更新时间: 2026-06-04*
