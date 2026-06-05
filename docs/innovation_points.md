# 论文创新点

**确定时间**: 2026-06-05
**路线**: Route 1.5

---

## 创新点总览

本论文采用 **Route 1.5：AHP-熵权-TOPSIS 主模型 + 轻量增强**，保留 3 个核心创新点：

---

## 创新点 1：三维度可解释 NR-IQA 指标体系

### 创新内容

将 AI 生成图像质量拆解为三个可解释维度：

1. **语义保真度 (Semantic Fidelity)**
   - 与提示词的匹配程度
   - 主体对象、属性描述、场景关系、风格指令四要素

2. **技术质量 (Technical Quality)**
   - 清晰度、噪声、伪影
   - 基于 Laplacian、Tenengrad、熵、噪声估计等指标

3. **结构完整性 (Structural Integrity)**
   - 物体畸形、边缘质量
   - 基于边缘密度、结构代理、噪声惩罚

### 创新价值

- 避免单一清晰度或单一美学指标评价失真
- 每个维度有明确的物理/统计意义
- 可解释性强，评委容易理解

### 证据支撑

- `results/final/image_dimension_scores.csv`
- `figures/final/image_dimension_scores_radar.png`

---

## 创新点 2：AHP-熵权组合赋权 TOPSIS 评价模型

### 创新内容

采用主客观组合赋权：

1. **AHP 主观权重**
   - 体现题目要求和专家偏好
   - 一致性检验 CR < 0.1

2. **熵权法客观权重**
   - 体现样本数据差异
   - 从指标离散程度自动确定

3. **组合权重**
   - 乘法归一化：`w_j = (w_AHP,j × w_E,j) / Σ(w_AHP,j × w_E,j)`
   - 兼顾主观判断和客观数据

4. **TOPSIS 综合排序**
   - 正负理想解
   - 相对贴近度
   - 可排序、可分级

### 创新价值

- 比纯 AHP 更客观
- 比纯熵权更有题意导向
- TOPSIS 给出可排序、可分级的综合质量结果

### 证据支撑

- `results/final/ahp_weights.csv`
- `results/final/entropy_weights.csv`
- `results/final/combined_weights.csv`
- `results/final/image_scores.csv`
- `figures/final/combined_weights_bar.png`

---

## 创新点 3：面向 AIGC 视频的时序失稳惩罚模型

### 创新内容

建立视频时序质量评价模型：

1. **时序指标**
   - SSIM：帧间结构相似性
   - 帧差均值：运动/画面变化幅度
   - 亮度突变：闪烁检测
   - 光流幅值和方向：运动连续性

2. **时序失稳分数**
   ```
   I_t = 0.4 × (1 - SSIM_t) + 0.3 × normalized(frame_diff_t) + 0.3 × normalized(brightness_delta_t)
   ```

3. **异常帧判定**
   - 阈值：`I_t > μ_I + 2σ_I`
   - 定位异常帧并解释原因

4. **视频整体质量**
   ```
   Q_video = 1 - mean(I_t) - λ × anomaly_ratio
   ```

### 创新价值

- 将时序稳定性纳入最终质量解释
- 异常帧可追溯、可解释
- 统一图像和视频评价框架

### 证据支撑

- `results/final/video_metrics.csv`
- `results/final/video_anomaly_frames.csv`
- `figures/final/video_instability_score.png`
- `figures/final/anomaly_detection.png`

---

## 创新点表达建议

### 论文摘要中的表达

> 本文构建"语义保真度-技术质量-结构完整性-时序稳定性"的分层质量评价体系，采用 AHP-熵权组合赋权与 TOPSIS 综合排序作为主评价模型，并通过维度敏感性分析、排序一致性校验和时序失稳检测增强模型可靠性。

### 论文正文中的表达

1. **问题一**：提出三维度可解释 NR-IQA 指标体系
2. **问题二**：采用 AHP-熵权组合赋权 TOPSIS 进行综合排序
3. **问题三**：建立时序失稳惩罚模型，定位异常帧并评估视频整体质量

### 避免的表达

- ❌ "跨模态语义图"
- ❌ "SIF-TQSI 框架"
- ❌ "深度学习模型"
- ❌ "泛化到所有 AIGC 模型"

---

*确定时间: 2026-06-05*
