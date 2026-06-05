# 支撑材料说明

**项目**: 2026年第八届中青杯全国大学生数学建模竞赛 B题
**题目**: AI生成内容的质量评估与参数优化
**生成日期**: 2026-06-05

---

## 项目概述

本项目针对B题"AI生成内容的质量评估与参数优化"，建立了一套完整的AI生成图像和视频质量评价体系。研究内容包括：

1. **图像质量评价**: 对8张AI生成图像进行多维度技术指标计算，采用AHP主观赋权与熵权法客观赋权相结合的组合赋权方法，通过TOPSIS和灰色关联分析进行综合排序
2. **视频质量评价**: 对车流视频进行抽帧分析，计算帧间SSIM、光流幅值、亮度波动等时序指标，定位异常帧并评估视频稳定性
3. **参数优化**: 基于图像质量短板诊断，提出针对性的参数优化建议

---

## 支撑材料清单

### 1. 源代码 (`src/`)

包含19个Python脚本，覆盖完整的分析流程：

- 数据预处理: `extract_pdf.py`, `extract_docx.py`, `inspect_media.py`, `video_slice.py`
- 指标计算: `image_metrics.py`, `video_metrics.py`, `dimension_scores.py`
- 综合评价: `evaluation_models.py`, `gray_relation.py`, `sensitivity_analysis.py`
- 参数优化: `image_shortfall_diagnosis.py`, `parameter_optimization.py`
- 结果输出: `export_excel.py`, `plot_results.py`, `main.py`

### 2. 最终结果 (`results/final/`)

包含14个结果文件：

- 图像指标: `image_metrics.csv`, `image_dimension_scores.csv`, `image_weights.csv`
- 图像排名: `image_topsis_scores.csv`, `gray_relation_scores.csv`
- 视频指标: `video_metrics.csv`, `video_summary.csv`, `video_anomaly_frames.csv`
- 稳定性分析: `rank_stability.csv`, `rank_consistency.csv`, `sensitivity_summary.csv`
- 参数优化: `image_shortfall_diagnosis.csv`, `parameter_optimization_suggestions.csv`
- 汇总表格: `results_final.xlsx`

### 3. 图表 (`figures/final/`)

包含15个图表文件（PNG和SVG格式）：

- 图像排名图: `image_ranking.png/.svg`
- 维度得分图: `image_dimension_scores.png/.svg`
- 权重对比图: `weight_comparison.png/.svg`
- 灰色关联一致性: `gray_topsis_consistency.png/.svg`
- 敏感性分析: `sensitivity_tornado.png/.svg`
- 参数优化热图: `parameter_priority_heatmap.png/.svg`
- 视频稳定性: `video_instability_curve.png/.svg`
- 异常帧面板: `anomaly_frames_panel.png`

### 4. 论文 (`paper/`)

包含16个文件：

- 论文草稿: `draft_v1.md` ~ `draft_v4.md`
- 论文大纲: `outline.md`
- 方程计划: `equation_plan.md`, `equation_plan_v2.md`
- 图表计划: `figure_table_plan.md`, `figure_table_plan_v2.md`
- 参考文献: `reference_list.md`, `reference_list_verified.md`
- 其他: `abstract_candidates.md`, `final_polish_report.md` 等

### 5. 文档 (`docs/`)

包含24个文档文件，记录项目分析过程：

- 题目分析: `problem_statement_verified.md`, `problem_statement_verification_report.md`
- 建模方案: `final_modeling_plan.md`, `claim_evidence_map.md`
- 审查报告: `vision_review.md`, `vision_review_test.md`
- 项目管理: `project_inventory.md`, `environment_setup.md`
- 其他技术文档和报告

### 6. 支撑材料 (`support/`)

- `README.md` - 本文件
- `ai_usage_log.md` - AI工具使用详情说明
- `support_materials_manifest.md` - 支撑材料文件清单

---

## 提交说明

### 论文提交

- 文件格式: PDF
- 命名格式: `B2026XXXXX.pdf`
- 提交截止: 2026年6月7日 17:00
- 提交方式: 登录官网 www.cycmcm.com 上传

### 支撑材料提交

- 文件格式: ZIP 或 RAR
- 命名格式: `B2026XXXXX材料.zip`
- 提交方式: 与论文一同上传至官网
- 备用邮箱: 3303055935@qq.com（仅官网无法提交时使用）

### 注意事项

1. 论文不得出现队员姓名、学校等身份信息
2. 论文页码须位于每页页脚中部，从"1"开始连续编号
3. 论文正文控制在20页以内
4. 所有引用资料须注明出处
5. 使用AI工具须在参考文献后声明，并提供AI工具使用详情说明

---

*生成时间: 2026-06-05*
