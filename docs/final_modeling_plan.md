# 最终建模方案

**确定时间**: 2026-06-05
**决策者**: Oracle
**最终路线**: Route 1.5 (AHP-熵权-TOPSIS 主模型 + 轻量增强)

---

## 1. 最终路线选择

### 1.1 选择结论

采用 **Route 1.5：AHP-熵权-TOPSIS 主模型 + 轻量 Route 2 增强**

不采用 Route 3（SIF-TQSI 跨模态框架）

### 1.2 选择理由

| 维度 | Route 1 | Route 2 | Route 3 | Route 1.5 |
|------|---------|---------|---------|-----------|
| 创新性 | 低 | 中高 | 高 | 中 |
| 风险 | 低 | 中 | 高 | 低-中 |
| 可行性 | 高 | 中 | 低 | 高 |
| 题意匹配 | 高 | 中高 | 中 | 高 |
| 评委接受度 | 高 | 中 | 低 | 高 |

**核心判断**：本题是评价类数学建模题，最重要的是指标可解释、结果可复现、图表可追溯。

---

## 2. 核心模型链条

```
输入数据 (8张图像 + 1个视频 + 题面要求)
    ↓
图像基础指标提取 (15个指标)
    ↓
三维度归并 (语义保真度 + 技术质量 + 结构完整性)
    ↓
权重确定 (AHP主观权重 + 熵权法客观权重 → 组合权重)
    ↓
图像综合评价 (TOPSIS排序 + 质量等级划分)
    ↓
可靠性增强 (敏感性分析 + 灰色关联校验)
    ↓
视频时序质量评价 (SSIM + 帧差 + 光流 + 闪烁)
    ↓
时序失稳判定 (异常帧定位 + 失稳分数)
    ↓
参数优化建议 (质量短板反推生成参数)
    ↓
输出结果 (CSV + Excel + 图表 + 论文)
```

---

## 3. 问题一：NR-IQA 模型

### 3.1 模型定义

**综合质量指数**：

```
Q_img = w_sem × S_sem + w_tech × S_tech + w_struct × S_struct
```

### 3.2 语义保真度 (S_sem)

**权重**：0.30

**构成**：
- 主体对象匹配度
- 属性描述符合度
- 场景关系合理性
- 风格指令一致性

**量化方式**：
- 关键词匹配率（首选）
- GPT-5.5 审查标签辅助（补充）
- CLIP 相似度（如环境支持）

### 3.3 技术质量 (S_tech)

**权重**：0.40

**指标**：

| 指标 | 方向 | 说明 |
|------|------|------|
| laplacian_var | 正向 | 清晰度 |
| tenengrad | 正向 | 聚焦度 |
| brightness_std | 正向 | 对比度 |
| saturation_mean | 正向 | 色彩鲜明度 |
| saturation_std | 正向 | 色彩层次 |
| entropy | 正向 | 信息量 |
| noise_estimate | 负向 | 噪声惩罚 |

### 3.4 结构完整性 (S_struct)

**权重**：0.30

**指标**：

| 指标 | 方向 | 说明 |
|------|------|------|
| edge_density | 正向 | 边缘密度 |
| structure_proxy | 正向 | 结构代理 |
| noise_estimate | 负向 | 伪影惩罚 |

### 3.5 权重确定

**一级维度权重**（AHP）：

| 维度 | 权重 |
|------|------|
| 语义保真度 | 0.30 |
| 技术质量 | 0.40 |
| 结构完整性 | 0.30 |

**二级指标权重**：AHP + 熵权法组合

**组合公式**：

```
w_j = (w_AHP,j × w_E,j) / Σ(w_AHP,j × w_E,j)
```

---

## 4. 问题二：图像质量评估算法

### 4.1 评估流程

```
指标提取 → 正向化/标准化 → AHP权重 → 熵权权重 → 组合权重 → TOPSIS → 排名/等级
```

### 4.2 TOPSIS 排序

**相对贴近度**：

```
C_i = D_i⁻ / (D_i⁺ + D_i⁻)
```

### 4.3 质量等级划分

| 等级 | 条件 |
|------|------|
| 优秀 | C_i ≥ 0.8 |
| 良好 | 0.6 ≤ C_i < 0.8 |
| 一般 | 0.4 ≤ C_i < 0.6 |
| 较差 | C_i < 0.4 |

### 4.4 内容类型敏感性分析

**方法**：权重扰动法

- 每次将一个维度权重 ±10%
- 重新计算 TOPSIS
- 观察排名变化
- 计算 Spearman 相关系数

### 4.5 跨模型可靠性校验

**主模型**：TOPSIS

**校验模型**：灰色关联分析

**一致性指标**：Spearman 排序相关系数

---

## 5. 问题三：视频时序质量模型

### 5.1 时序指标

| 指标 | 说明 |
|------|------|
| SSIM_t | 帧间结构相似性 |
| frame_diff_t | 帧差均值 |
| brightness_delta_t | 亮度突变 |
| saturation_delta_t | 饱和度突变 |
| optical_flow_magnitude_t | 光流幅值 |
| optical_flow_angle_change_t | 光流方向变化 |

### 5.2 时序失稳分数

```
I_t = 0.4 × (1 - SSIM_t) + 0.3 × normalized(frame_diff_t) + 0.3 × normalized(brightness_delta_t)
```

### 5.3 异常帧判定

**阈值条件**：

```
I_t > μ_I + 2σ_I
```

其中 μ_I 和 σ_I 分别为全视频失稳分数的均值和标准差。

### 5.4 视频整体质量

```
Q_video = 1 - mean(I_t) - λ × anomaly_ratio
```

建议 λ = 0.2

### 5.5 车流视频分析结论

基于多模态审查结果：
- 视频整体连续性良好
- 异常帧 50、53 影响低
- 异常帧 62 影响中（驾驶员面部自然变化）
- 未发现严重时序失稳

---

## 6. 参数优化建议

### 6.1 短板反推模型

**诊断公式**：

```
D_ij = w_j × (1 - z_ij)
```

其中 z_ij 为归一化指标分数，D_ij 越大说明该维度短板越严重。

### 6.2 参数优化映射表

| 质量短板 | 诊断指标 | 参数建议 |
|----------|----------|----------|
| 清晰度不足 | Laplacian、Tenengrad 偏低 | 提高分辨率，增加采样步数 |
| 噪声/伪影偏高 | noise_estimate 偏高 | 增加采样步数，降低过强随机性 |
| 亮度闪烁 | brightness_delta 偏高 | 增强帧间一致性约束 |
| 色彩不稳定 | saturation_delta 偏高 | 固定风格提示词 |
| 运动不连续 | optical_flow_angle_change 偏高 | 减小运动幅度，加强 motion consistency |
| 语义偏离 | 关键词匹配/GPT 审查发现偏差 | 强化主体、属性、场景关系提示词 |
| 结构畸形 | edge_density、structure_proxy 异常 | 增加结构约束提示词 |

### 6.3 优化优先级

```
priority = shortfall_score × importance_weight
```

---

## 7. 需要重新生成的结果

### 7.1 results/final/

| 文件 | 内容 |
|------|------|
| media_inventory.csv | 媒体文件清单 |
| image_metrics.csv | 图像技术指标 |
| image_dimension_scores.csv | 图像三维度得分 |
| ahp_weights.csv | AHP 权重 |
| entropy_weights.csv | 熵权法权重 |
| combined_weights.csv | 组合权重 |
| image_scores.csv | 图像综合得分 |
| sensitivity_analysis.csv | 敏感性分析 |
| gray_relation_check.csv | 灰色关联校验 |
| video_basic_info.csv | 视频基础信息 |
| video_metrics.csv | 视频时序指标 |
| video_anomaly_frames.csv | 视频异常帧 |
| video_quality_summary.csv | 视频质量汇总 |
| parameter_optimization_suggestions.csv | 参数优化建议 |
| final_summary.csv | 最终汇总 |
| results.xlsx | Excel 总表 |

### 7.2 figures/final/

| 文件 | 内容 |
|------|------|
| image_metrics_heatmap.png/svg | 图像指标热力图 |
| image_dimension_scores_radar.png/svg | 维度得分雷达图 |
| image_scores_bar.png/svg | 综合得分柱状图 |
| combined_weights_bar.png/svg | 组合权重柱状图 |
| sensitivity_rank_change.png/svg | 敏感性排名变化图 |
| gray_relation_rank_check.png/svg | 灰色关联校验图 |
| video_ssim.png/svg | 视频 SSIM 曲线 |
| video_frame_diff.png/svg | 视频帧差曲线 |
| video_instability_score.png/svg | 失稳分数曲线 |
| anomaly_detection.png/svg | 异常帧检测图 |
| video_contact_sheet.png | 视频关键帧拼图 |

---

*确定时间: 2026-06-05*
*决策者: Oracle*
