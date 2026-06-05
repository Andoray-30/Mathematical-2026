# 支撑材料文件清单

**项目**: 2026年第八届中青杯全国大学生数学建模竞赛 B题
**生成日期**: 2026-06-05

---

## 目录结构与文件统计

### 1. src/ - 源代码 (19个Python脚本)

| 文件名 | 用途 |
|--------|------|
| main.py | 主入口，串联完整分析流程 |
| check_env.py | 环境检查 |
| smoke_test.py | 冒烟测试 |
| extract_pdf.py | PDF文本提取 |
| extract_docx.py | Word文档提取 |
| inspect_media.py | 媒体文件检查 |
| video_slice.py | 视频抽帧 |
| image_metrics.py | 图像技术指标计算 |
| video_metrics.py | 视频时序指标计算 |
| dimension_scores.py | 维度得分计算 |
| evaluation_models.py | AHP/熵权法/TOPSIS评价模型 |
| gray_relation.py | 灰色关联分析 |
| sensitivity_analysis.py | 敏感性分析 |
| image_shortfall_diagnosis.py | 图像质量短板诊断 |
| parameter_optimization.py | 参数优化建议 |
| export_excel.py | Excel导出 |
| plot_results.py | 图表绘制 |
| render_b_problem_pages.py | B题PDF页面渲染 |
| vision_review_to_csv.py | 视觉审查结果转CSV |

### 2. results/final/ - 最终结果 (14个文件)

| 文件名 | 内容 |
|--------|------|
| image_metrics.csv | 8张图像×15个技术指标 |
| image_dimension_scores.csv | 图像维度综合得分 |
| image_weights.csv | AHP/熵权法/组合权重 |
| image_topsis_scores.csv | TOPSIS综合排名得分 |
| gray_relation_scores.csv | 灰色关联分析得分 |
| rank_consistency.csv | 排名一致性检验 |
| rank_stability.csv | 排名稳定性分析 |
| sensitivity_summary.csv | 敏感性分析汇总 |
| image_shortfall_diagnosis.csv | 图像质量短板诊断 |
| parameter_optimization_suggestions.csv | 参数优化建议 |
| video_metrics.csv | 视频帧级指标 |
| video_summary.csv | 视频汇总指标 |
| video_anomaly_frames.csv | 异常帧定位 |
| results_final.xlsx | 汇总Excel表格 |

### 3. figures/final/ - 最终图表 (15个文件)

| 文件名 | 内容 |
|--------|------|
| image_ranking.png / .svg | 图像综合排名图 |
| image_dimension_scores.png / .svg | 维度得分雷达图 |
| weight_comparison.png / .svg | 权重方法对比图 |
| gray_topsis_consistency.png / .svg | 灰色-TOPSIS一致性图 |
| sensitivity_tornado.png / .svg | 敏感性龙卷风图 |
| parameter_priority_heatmap.png / .svg | 参数优先级热力图 |
| video_instability_curve.png / .svg | 视频不稳定性曲线 |
| anomaly_frames_panel.png | 异常帧拼图面板 |

### 4. paper/ - 论文 (16个文件)

| 文件名 | 内容 |
|--------|------|
| outline.md | 论文大纲 |
| draft_v1.md ~ draft_v4.md | 论文草稿（4个版本） |
| equation_plan.md / _v2.md | 公式排版计划 |
| figure_table_plan.md / _v2.md | 图表排版计划 |
| reference_list.md | 参考文献列表 |
| reference_list_verified.md | 已验证参考文献 |
| reference_search_plan.md | 文献检索计划 |
| reference_verification_report.md | 文献验证报告 |
| abstract_candidates.md | 摘要候选 |
| final_polish_report.md | 最终润色报告 |
| README.md | 论文目录说明 |

### 5. docs/ - 文档 (24个文件)

| 文件名 | 内容 |
|--------|------|
| problem_statement_verified.md | 验证后的题目分析 |
| problem_statement_verification_report.md | 题目验证报告 |
| final_modeling_plan.md | 最终建模方案 |
| claim_evidence_map.md | 结论-证据映射 |
| vision_review.md | 多模态审查报告 |
| vision_review_test.md | 审查测试记录 |
| vision_review_input_manifest.md | 审查输入清单 |
| project_inventory.md | 项目资产清单 |
| environment_setup.md | 环境配置说明 |
| capability_acceptance_summary.md | 能力验收总结 |
| multimodal_routing_policy.md | 多模态路由策略 |
| innovation_points.md | 创新点总结 |
| paper_structure_plan.md | 论文结构规划 |
| paper_revision_notes.md | 论文修改笔记 |
| ranking_interpretation_notes.md | 排名解读说明 |
| video_interpretation_notes.md | 视频解读说明 |
| formal_results_generation_report.md | 正式结果生成报告 |
| deep-research-report.md | 深度研究报告 |
| 其他 | 路线增强计划、清理报告等 |

### 6. support/ - 支撑材料 (3个文件)

| 文件名 | 内容 |
|--------|------|
| README.md | 支撑材料说明 |
| ai_usage_log.md | AI工具使用详情说明 |
| support_materials_manifest.md | 本文件 |

---

## 文件总数统计

| 目录 | 文件数 | 说明 |
|------|--------|------|
| src/ | 19 | Python源代码 |
| results/final/ | 14 | 最终结果（CSV + XLSX） |
| figures/final/ | 15 | 最终图表（PNG + SVG） |
| paper/ | 16 | 论文草稿和参考材料 |
| docs/ | 24 | 项目文档 |
| support/ | 3 | 支撑材料 |
| **合计** | **91** | |

---

*生成时间: 2026-06-05*
