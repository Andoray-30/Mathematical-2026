# Claim-Evidence 映射表

**确定时间**: 2026-06-05
**目的**: 确保论文每个结论都有对应证据支撑

---

## 映射原则

1. **每个 Claim 必须有至少一个 Evidence**
2. **Evidence 必须来自 results/ 或 figures/ 或 docs/**
3. **不允许编造数据或结论**
4. **GPT-5.5 审查结果只作为辅助说明，不作为数值证据**

---

## 问题一 Claim-Evidence 映射

### Claim 1.1: 图像质量可由语义保真度、技术质量、结构完整性三维度综合评价

| Evidence | 路径 | 说明 |
|----------|------|------|
| 语义审查结果 | `docs/vision_review.md` | GPT-5.5 对 8 张图像的语义描述和瑕疵标注 |
| 技术指标数据 | `results/final/image_metrics.csv` | 15 个技术指标的计算结果 |
| 题面要求 | `docs/problem_statement_verified.md` | 题目明确要求三维度评价 |

### Claim 1.2: 语义保真度可由关键词匹配率量化

| Evidence | 路径 | 说明 |
|----------|------|------|
| 关键词匹配表 | `results/final/image_dimension_scores.csv` | 语义保真度得分 |
| 审查标签 | `docs/vision_review.md` | 主体、风格、瑕疵等级 |

### Claim 1.3: 技术质量可由 Laplacian、Tenengrad、熵等指标量化

| Evidence | 路径 | 说明 |
|----------|------|------|
| 技术指标 | `results/final/image_metrics.csv` | 包含 laplacian_var、tenengrad、entropy 等 |
| 指标热力图 | `figures/final/image_metrics_heatmap.png` | 可视化各指标差异 |

### Claim 1.4: 结构完整性可由边缘密度、结构代理、噪声惩罚量化

| Evidence | 路径 | 说明 |
|----------|------|------|
| 结构指标 | `results/final/image_metrics.csv` | 包含 edge_density、structure_proxy、noise_estimate |
| 维度得分 | `results/final/image_dimension_scores.csv` | 结构完整性维度得分 |

---

## 问题二 Claim-Evidence 映射

### Claim 2.1: AHP 能体现题目对各指标的重视程度

| Evidence | 路径 | 说明 |
|----------|------|------|
| AHP 权重 | `results/final/ahp_weights.csv` | 主观权重结果 |
| 一致性检验 | `results/final/ahp_weights.csv` | CR < 0.1 |
| 判断矩阵 | 附录B | AHP 判断矩阵 |

### Claim 2.2: 熵权法能从数据差异中提取客观权重

| Evidence | 路径 | 说明 |
|----------|------|------|
| 熵权权重 | `results/final/entropy_weights.csv` | 客观权重结果 |
| 指标离散度 | `results/final/image_metrics.csv` | 各指标标准差 |

### Claim 2.3: 组合赋权能兼顾主观判断和客观数据

| Evidence | 路径 | 说明 |
|----------|------|------|
| 组合权重 | `results/final/combined_weights.csv` | 最终权重 |
| 权重对比图 | `figures/final/combined_weights_bar.png` | AHP vs 熵权 vs 组合 |

### Claim 2.4: TOPSIS 能给出可排序、可分级的综合质量结果

| Evidence | 路径 | 说明 |
|----------|------|------|
| 综合得分 | `results/final/image_scores.csv` | TOPSIS 贴近度和排名 |
| 得分柱状图 | `figures/final/image_scores_bar.png` | 可视化排名 |
| 质量等级 | `results/final/image_scores.csv` | 优秀/良好/一般/较差 |

### Claim 2.5: 1.png、5.jpg、6.jpg 质量较高

| Evidence | 路径 | 说明 |
|----------|------|------|
| 综合排名 | `results/final/image_scores.csv` | TOPSIS 排名 |
| 视觉审查 | `docs/vision_review.md` | GPT-5.5 判断为高质量 |
| 指标数据 | `results/final/image_metrics.csv` | 技术指标对比 |

### Claim 2.6: 内容类型对不同维度指标敏感性不同

| Evidence | 路径 | 说明 |
|----------|------|------|
| 敏感性分析 | `results/final/sensitivity_analysis.csv` | 权重扰动下的排名变化 |
| 敏感性图 | `figures/final/sensitivity_rank_change.png` | 可视化排名变化 |

### Claim 2.7: 跨模型排序一致性较高

| Evidence | 路径 | 说明 |
|----------|------|------|
| 灰色关联校验 | `results/final/gray_relation_check.csv` | Spearman 相关系数 |
| 校验图 | `figures/final/gray_relation_rank_check.png` | 排名对比 |

---

## 问题三 Claim-Evidence 映射

### Claim 3.1: 视频时序质量可由 SSIM、帧差、光流、闪烁检测量化

| Evidence | 路径 | 说明 |
|----------|------|------|
| 时序指标 | `results/final/video_metrics.csv` | 逐帧 SSIM、帧差、光流等 |
| SSIM 曲线 | `figures/final/video_ssim.png` | 可视化帧间一致性 |

### Claim 3.2: 时序失稳分数能定位异常帧

| Evidence | 路径 | 说明 |
|----------|------|------|
| 失稳分数 | `results/final/video_metrics.csv` | I_t 计算结果 |
| 异常帧列表 | `results/final/video_anomaly_frames.csv` | 帧 50、53、62 |
| 失稳曲线 | `figures/final/video_instability_score.png` | 可视化失稳分数 |

### Claim 3.3: 帧 50、53 影响低，帧 62 影响中

| Evidence | 路径 | 说明 |
|----------|------|------|
| 异常帧解释 | `docs/vision_review.md` | GPT-5.5 语义解释 |
| 时序指标 | `results/final/video_metrics.csv` | 具体数值 |
| 异常检测图 | `figures/final/anomaly_detection.png` | 可视化异常帧 |

### Claim 3.4: 车流视频未发现严重时序失稳

| Evidence | 路径 | 说明 |
|----------|------|------|
| 视频质量汇总 | `results/final/video_quality_summary.csv` | 整体质量指数 |
| 异常帧比例 | `results/final/video_anomaly_frames.csv` | 异常帧占比 |
| 视觉审查 | `docs/vision_review.md` | 连续性良好 |

---

## 参数优化 Claim-Evidence 映射

### Claim 4.1: 质量短板可反推生成参数优化方向

| Evidence | 路径 | 说明 |
|----------|------|------|
| 短板诊断 | `results/final/image_dimension_scores.csv` | 低分维度 |
| 参数建议 | `results/final/parameter_optimization_suggestions.csv` | 优化建议表 |
| 指标数据 | `results/final/image_metrics.csv` | 具体指标值 |

### Claim 4.2: 清晰度不足可提高分辨率和采样步数

| Evidence | 路径 | 说明 |
|----------|------|------|
| Laplacian 值 | `results/final/image_metrics.csv` | 清晰度指标 |
| 参数建议 | `results/final/parameter_optimization_suggestions.csv` | 对应建议 |

### Claim 4.3: 语义偏离可强化提示词

| Evidence | 路径 | 说明 |
|----------|------|------|
| 语义得分 | `results/final/image_dimension_scores.csv` | 语义保真度得分 |
| 审查结果 | `docs/vision_review.md` | GPT-5.5 语义分析 |

---

## GPT-5.5 使用说明

### GPT-5.5 用于

| 任务 | 输出 | 用途 |
|------|------|------|
| 图像语义审查 | 文本描述 | 辅助说明，不作为数值证据 |
| 异常帧解释 | 文本解释 | 辅助说明，不作为数值证据 |
| 论文逻辑审查 | 修改建议 | 论文写作参考 |

### GPT-5.5 不用于

- ❌ 直接生成数值指标
- ❌ 直接决定最终排名
- ❌ 替代本地代码计算
- ❌ 编造 prompt 缺失信息

---

*确定时间: 2026-06-05*
