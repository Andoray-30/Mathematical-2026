# 图表计划 v2

**生成时间**: 2026-06-05
**用途**: 论文图表规划（压缩版）
**原则**: 正文最多7张图、5张表，其他结果放附录

---

## 正文图表

### 图（7张）

| 图号 | 名称 | 来源文件 | 用途 | 状态 |
|------|------|----------|------|------|
| 图1 | 总体框架图 | [待补图] | 展示"评价—诊断—优化"闭环 | 待补 |
| 图2 | 图像维度得分柱状图 | figures/final/image_dimension_scores.png | 展示8张图在语义、技术、结构上的差异 | ✅ |
| 图3 | TOPSIS排名柱状图 | figures/final/image_ranking.png | 展示综合排序结果 | ✅ |
| 图4 | TOPSIS vs GRA散点图 | figures/final/gray_topsis_consistency.png | 展示排序一致性验证 | ✅ |
| 图5 | 敏感性龙卷风图 | figures/final/sensitivity_tornado.png | 展示排名稳健性 | ✅ |
| 图6 | 视频失稳曲线 | figures/final/video_instability_curve.png | 展示时序失稳分数与异常帧 | ✅ |
| 图7 | 参数优先级热力图 | figures/final/parameter_priority_heatmap.png | 展示参数-维度作用矩阵 | ✅ |

### 表（5张）

| 表号 | 名称 | 来源文件 | 用途 | 状态 |
|------|------|----------|------|------|
| 表1 | TOPSIS综合排序结果 | results/final/image_topsis_scores.csv | 展示排名、贴近度、质量等级 | ✅ |
| 表2 | 组合权重计算 | results/final/image_weights.csv | 展示AHP/熵权/组合权重 | ✅ |
| 表3 | 稳健性验证汇总 | results/final/rank_consistency.csv + rank_stability.csv | 展示灰色关联和敏感性结果 | ✅ |
| 表4 | 视频时序指标汇总 | results/final/video_summary.csv | 展示视频分析核心结果 | ✅ |
| 表5 | 参数优化优先级 | results/final/parameter_optimization_suggestions.csv | 展示Top-5参数调整建议 | ✅ |

---

## 附录图表

### 附录图

| 图号 | 名称 | 来源文件 | 用途 |
|------|------|----------|------|
| 图A1 | 权重对比图 | figures/final/weight_comparison.png | 详细展示AHP/熵权/组合权重 |
| 图A2 | 异常帧面板 | figures/final/anomaly_frames_panel.png | 展示异常帧SSIM对比 |
| 图A3 | 图像指标热力图 | figures/final/image_metrics_heatmap.png | 展示15个指标的原始数据 |

### 附录表

| 表号 | 名称 | 来源文件 | 用途 |
|------|------|----------|------|
| 表A1 | 图像技术指标明细 | results/final/image_metrics.csv | 15个指标的原始数值 |
| 表A2 | 结构化标签示例 | results/intermediate/vision_labels.csv | 语义标签结构 |
| 表A3 | 样本级短板诊断 | results/final/image_shortfall_diagnosis.csv | 每图的最弱维度和主要缺陷 |
| 表A4 | 异常帧详细列表 | results/final/video_anomaly_frames.csv | 15个异常帧的详细指标 |
| 表A5 | 灰色关联分析详细结果 | results/final/gray_relation_scores.csv | 各图的灰色关联度 |
| 表A6 | 敏感性分析详细结果 | results/final/sensitivity_summary.csv | 6种场景的排名变化 |

---

## 图表规范

1. **图格式**: PNG + SVG 双输出，分辨率 ≥ 150 DPI
2. **表格式**: 三线表，无竖线
3. **字体**: 中文使用宋体或黑体，英文使用 Times New Roman
4. **引用**: 正文中每个图表必须引用并分析
5. **分析要求**: 正文图表分析 ≥ 100 字，附录图表可简要说明

---

## 与v1的主要变化

| 变化 | v1 | v2 | 原因 |
|------|----|----|------|
| 正文图数量 | 10张 | 7张 | 压缩至20页以内 |
| 正文表数量 | 11张 | 5张 | 压缩至20页以内 |
| 附录图 | 0张 | 3张 | 移至附录 |
| 附录表 | 0张 | 6张 | 移至附录 |
| 总体框架图 | 待补 | 待补 | 仍需手工制作 |
| 数据预处理流程图 | 待补 | 删除 | 简化表述 |

---

*生成时间: 2026-06-05*
