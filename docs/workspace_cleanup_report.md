# 工作区清理报告

**清理时间**: 2026-06-04
**清理目标**: 归档能力验收阶段产物，准备进入正式建模阶段

---

## 1. 已归档文件列表

### docs/ (6 个文件)

- `skill_extracted_workflow.md`
- `skill_extracted_algorithms.md`
- `skill_extracted_tools.md`
- `adaptation_report.md`
- `capability_acceptance_report.md`
- `B题：AI生成内容的质量评估与参数优化_extracted.md`

### results/ (7 个文件)

- `smoke_test_report.txt`
- `image_metrics.csv`
- `image_scores.csv`
- `final_summary.csv`
- `results.xlsx`
- `video_metrics.csv`
- `video_anomaly_frames.csv`

### figures/ (13 个项目)

**文件** (11 个):
- `image_metrics_heatmap.png/svg`
- `image_scores_bar.png/svg`
- `video_contact_sheet.png`
- `video_ssim.png/svg`
- `video_frame_diff.png/svg`
- `anomaly_detection.png/svg`

**目录** (2 个):
- `pdf_pages/`
- `video_frames/`

---

## 2. 未找到文件列表

### docs/

- `pdf_extract_report.md`

### results/

- `env_report.txt`
- `pipeline_log.txt`
- `pipeline_status.csv`
- `media_inventory.csv`
- `video_basic_info.csv`
- `video_instability_threshold.txt`
- `indicator_description.csv`

---

## 3. 保留的核心文件列表

### docs/

- `project_inventory.md`
- `environment_setup.md`
- `skill_to_b_problem_mapping.md`
- `vision_review_input_manifest.md`
- `vision_review_test.md`
- `workspace_cleanup_report.md`
- `capability_acceptance_summary.md`
- `multimodal_routing_policy.md`

### 根目录

- `AGENTS.md`
- `requirements.txt`
- `中青杯数学建模2026规则文档.md`

---

## 4. 当前主工作区目录结构

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

## 5. 归档目录结构

```
archive/capability_test_2026-06-04/
├── README.md
├── docs/
│   ├── skill_extracted_workflow.md
│   ├── skill_extracted_algorithms.md
│   ├── skill_extracted_tools.md
│   ├── adaptation_report.md
│   ├── capability_acceptance_report.md
│   └── B题：..._extracted.md
├── results/
│   ├── smoke_test_report.txt
│   ├── image_metrics.csv
│   ├── image_scores.csv
│   ├── final_summary.csv
│   ├── results.xlsx
│   ├── video_metrics.csv
│   └── video_anomaly_frames.csv
└── figures/
    ├── image_metrics_heatmap.png/svg
    ├── image_scores_bar.png/svg
    ├── video_contact_sheet.png
    ├── video_ssim.png/svg
    ├── video_frame_diff.png/svg
    ├── anomaly_detection.png/svg
    ├── pdf_pages/
    └── video_frames/
```

---

## 6. 当前项目阶段

能力验收阶段已完成，当前进入正式建模准备阶段。

---

## 7. 下一步建议

1. 运行或准备 GPT-5.5 多模态审查
2. 召开多智能体建模方案设计
3. 确定最终建模路线
4. 重新生成正式 `results/final/` 和 `figures/final/`
5. 再进入论文大纲和正文撰写

---

*清理时间: 2026-06-04*
