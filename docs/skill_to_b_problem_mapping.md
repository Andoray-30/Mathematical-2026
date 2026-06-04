# Skill to B题 Problem Mapping

> 将 math-modeling-skill 组件映射到 2026 中青杯 B题需求。

---

## 一、B题概述

**B题名称**：AI 生成内容的质量评估与参数优化

**附件**：
- 附件1：8张AI生成图片
- 附件2：1段车流视频（车流视频.mp4）

**核心任务**：
1. 对8张图片进行质量评估与排序
2. 对视频进行质量评估
3. 参数优化建议

---

## 二、Skill 组件 → B题需求映射

### 2.1 建模手 → B题分析

| Skill 组件 | B题应用 |
|-----------|--------|
| Model Contract | 建立"AI内容质量评估"的核心结论、子问题拆解、模型映射 |
| 前置合同模板 | 子问题1：图像质量评价；子问题2：视频质量评价；子问题3：参数优化 |
| 防冗余原则 | 确保每个评价维度（语义、技术、结构）承载独特证据 |
| 三原则 | 优先使用AHP+熵权+TOPSIS等经典方法，避免过度复杂 |
| 评价类模式（模式7） | AHP主观权重 + 熵权法客观权重 → TOPSIS排序 |
| 缺失输入处理 | 当某些指标无法提取时，使用符号参数建模 |

### 2.2 编程手 → B题代码实现

| Skill 组件 | B题应用 |
|-----------|--------|
| 环境检查 | 检查 Python + OpenCV + numpy + matplotlib + scipy |
| 可视化规划 | EDA（指标分布）→ 中间（权重对比）→ 最终（排名结果） |
| Figure Contract | 每张图证明一个核心结论 |
| 标准调色板 | 使用 PALETTE 色系保持学术风格 |
| SVG+PNG双输出 | 所有图表同时输出矢量和位图 |
| 三线表 | 结果对比表使用三线表格式 |
| 表格处理 | 结果输出到 Excel，使用公式而非硬编码 |

### 2.3 论文手 → B题论文撰写

| Skill 组件 | B题应用 |
|-----------|--------|
| 论证构建 | "本文采用AHP-熵权-TOPSIS方法实现了AI内容质量的多维度评估" |
| Claim-Evidence映射 | 每个质量排名结论对应具体的图表证据 |
| 摘要六要素 | context(AI内容普及) → gap(缺乏质量评估) → approach(组合赋权) → result(排名) → implication(评估框架) → boundary(适用条件) |
| 引言五要素 | field scale → bottleneck → prior attempts → gap → present study |
| 证据阶梯 | system(评估流程) → validation(一致性检验) → main result(排名) → comparison(方法对比) → analysis(敏感性) |
| 去AI味指南 | 禁用"深入探讨"、"关键作用"等AI高频词 |
| 自审框架 | 四轮审查：论证逻辑 → 章节结构 → 表述质量 → 格式规范 |
| 图表规范 | 每张图片≥100字分析，三线表格式 |

---

## 三、算法映射

### 3.1 适用算法

| 算法 | B题用途 | 优先级 |
|------|--------|--------|
| **AHP** | 确定主观权重（专家对指标两两比较） | ⭐⭐⭐ |
| **熵权法** | 确定客观权重（从数据中提取） | ⭐⭐⭐ |
| **组合赋权** | AHP+熵权法线性组合 | ⭐⭐⭐ |
| **TOPSIS** | 对8张图片进行综合排序 | ⭐⭐⭐ |
| **模糊综合评价** | 处理主观性较强的指标 | ⭐⭐ |
| **敏感性分析** | 验证排名稳健性 | ⭐⭐⭐ |
| **数据预处理** | 标准化、异常值检测 | ⭐⭐⭐ |

### 3.2 不适用算法（排除）

| 算法类别 | 排除原因 |
|---------|---------|
| 优化算法（遗传、PSO、模拟退火） | B题是评价问题，不是优化问题 |
| 预测算法（灰色预测、ARIMA、LSTM） | B题不需要时间序列预测 |
| 图论算法（最短路径、最大流） | B题不涉及网络结构 |
| 聚类分析（K-Means、DBSCAN） | B题核心是排序评价，不是分类 |
| DEA | B题不是效率评价问题 |

### 3.3 推荐建模路线

```
B题建模路线：
1. 图像指标提取（代码计算）
   - 清晰度：Laplacian方差、Tenengrad梯度
   - 亮度：均值、标准差
   - 饱和度：均值、标准差
   - 信息量：图像熵
   - 边缘：Canny边缘密度
   - 噪声：噪声估计

2. 视频指标提取（代码计算）
   - 帧间SSIM
   - 帧差均值
   - 亮度/饱和度波动
   - 光流幅值
   - 异常帧定位

3. 数据预处理
   - 标准化（Min-Max或Z-score）
   - 异常值检测
   - 缺失值处理

4. AHP主观赋权
   - 构建判断矩阵
   - 计算权重
   - 一致性检验（CR < 0.1）

5. 熵权法客观赋权
   - 数据标准化
   - 计算信息熵
   - 计算权重

6. 组合赋权
   - w = α·w_ahp + (1-α)·w_entropy

7. TOPSIS排序
   - 向量标准化
   - 加权规范化
   - 正负理想解
   - 相对贴近度
   - 排名

8. 敏感性分析
   - 改变权重 ±10%/20%
   - 观察排名变化
   - 验证稳健性

9. 质量等级划分
   - 根据贴近度划分等级（优/良/中/差）
```

---

## 四、文件结构映射

```
F:\Mathematical 2026\
├── B题：AI生成内容的质量评估与参数优化/
│   ├── B题：AI生成内容的质量评估与参数优化.pdf    ← pdf skill 读取
│   ├── 附件1/ (8张图片)                          ← OpenCV 提取指标
│   └── 附件2/ (车流视频.mp4)                     ← OpenCV 抽帧+分析
├── src/
│   ├── image_metrics.py      ← 图像指标提取
│   ├── video_metrics.py      ← 视频指标提取
│   ├── ahp_weight.py         ← AHP主观赋权
│   ├── entropy_weight.py     ← 熵权法客观赋权
│   ├── topsis_ranking.py     ← TOPSIS排序
│   ├── sensitivity.py        ← 敏感性分析
│   ├── export_excel.py       ← 结果导出
│   └── plot_results.py       ← 可视化
├── results/
│   ├── image_metrics.csv     ← 图像指标数据
│   ├── video_metrics.csv     ← 视频指标数据
│   ├── weights.csv           ← 权重结果
│   ├── ranking.csv           ← 排名结果
│   └── results.xlsx          ← 汇总结果
├── figures/
│   ├── indicator_distribution.png    ← EDA图表
│   ├── weight_comparison.png         ← 权重对比
│   ├── topsis_ranking.png            ← 最终排名
│   ├── sensitivity_analysis.png      ← 敏感性分析
│   └── 图表面板.html                 ← 导航面板
└── paper/
    ├── 论文.docx              ← 最终论文
    └── Claim-Evidence映射.md   ← 论证映射
```

---

## 五、关键技术约束

### 5.1 当前模型限制

- mimo-v2.5-pro 不能直接处理 PDF/图片/视频
- 需要通过 Python 代码提取所有可量化指标
- 图片语义理解由 GPT-5.5 Deep Agent 负责

### 5.2 代码优先原则

- 所有可量化指标必须由本地代码生成
- 不允许 GPT-5.5 直接凭视觉感觉生成数值结果
- 所有图表、CSV、Excel、论文结论必须可追溯到代码输出

### 5.3 图像指标提取技术栈

```python
# 核心依赖
import cv2           # 图像处理
import numpy as np   # 数值计算
from scipy import stats  # 统计分析
from skimage.metrics import structural_similarity  # SSIM
```

### 5.4 视频处理技术栈

```python
# 抽帧
cap = cv2.VideoCapture("车流视频.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 帧间SSIM
from skimage.metrics import structural_similarity as ssim
score = ssim(frame1_gray, frame2_gray)

# 光流
flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
```

---

## 六、论文写作要点（B题专用）

### 6.1 国赛格式

- 语言：中文
- 摘要：300-1000字，3-5个关键字
- 人称：禁止使用第一人称（用"本文"而非"我们"）
- 叙述：多使用整段叙述，避免大量分点
- 图表：每张图片≥100字分析

### 6.2 去AI味要点

- ❌ "本文深入探讨了AI生成内容的质量评估问题，充分展示了数学建模的强大能力。"
- ✅ "本文采用AHP-熵权-TOPSIS方法对8张AI生成图片进行质量评估。在清晰度指标上，图片3的Laplacian方差为1256.3，排名第1。"

### 6.3 证据链要求

每个排名结论必须有对应证据：
- 图X：TOPSIS相对贴近度对比图
- 表Y：各指标权重和得分明细
- 公式Z：组合赋权公式

---

## 七、排除内容

以下 skill 内容与 B题无关，不纳入项目：

| 排除内容 | 原因 |
|---------|------|
| 优化算法（01-优化算法说明.md） | B题是评价问题 |
| 预测算法（02-预测类算法说明.md） | B题不需要预测 |
| 图论算法（04-图论与网络分析算法说明.md） | B题不涉及网络 |
| 综合算法（06-综合类算法说明.md） | 蒙特卡洛、排队论等不适用 |
| 机器学习（07-机器学习算法说明.md） | B题优先使用传统方法 |
| 美赛英文化工作流 | B题是国赛，用中文 |
| 进阶技巧（动词校准） | 美赛专用 |
| 优秀论文资源库中的美赛论文 | 仅参考国赛论文格式 |
