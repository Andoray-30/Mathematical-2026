---
name: aigc-quality-eval
description: "2026 中青杯 B 题专用技能 - AI 生成图像/视频质量评价与参数优化。包含图像质量评价、视频质量评价、AHP/熵权法/TOPSIS 综合排序、多模态审查流程。"
---

# AIGC 质量评价技能 - B 题专用

本技能专为 2026 中青杯 B 题（AI 生成内容的质量评估与参数优化）设计。

---

## 建模路线

### 1. 图像质量评价

#### 1.1 语义保真度
- 由 GPT-5.5 Deep Agent 负责审查
- 检查生成内容是否符合题意
- 输出：`docs/vision_review.md`

#### 1.2 技术质量（本地代码计算）
- Laplacian 方差（清晰度）
- Tenengrad 梯度（聚焦度）
- 亮度均值与标准差
- 饱和度均值与标准差
- 图像熵（信息量）

#### 1.3 结构完整性（本地代码计算）
- Canny 边缘密度
- 噪声估计
- 结构完整性代理指标

---

### 2. 图像技术指标清单

| 指标 | 计算方法 | 方向 | 说明 |
|------|----------|------|------|
| width | 直接读取 | - | 图像宽度 |
| height | 直接读取 | - | 图像高度 |
| aspect_ratio | width/height | - | 宽高比 |
| laplacian_var | cv2.Laplacian 方差 | 正向 | 越大越清晰 |
| tenengrad | Sobel 梯度平方和 | 正向 | 越大越聚焦 |
| brightness_mean | HSV V 通道均值 | 适中 | 过亮过暗都不好 |
| brightness_std | HSV V 通道标准差 | 正向 | 越大对比度越好 |
| saturation_mean | HSV S 通道均值 | 正向 | 越大色彩越鲜艳 |
| saturation_std | HSV S 通道标准差 | 正向 | 越大色彩变化越丰富 |
| entropy | 信息熵 | 正向 | 越大信息量越多 |
| edge_density | Canny 边缘占比 | 正向 | 越大细节越多 |
| noise_estimate | 高斯差估计 | 负向 | 越小噪声越少 |
| structure_proxy | 综合代理指标 | 正向 | 结构完整性 |

---

### 3. 图像综合排序

#### 3.1 AHP 主观权重
- 构建判断矩阵
- 计算特征向量
- 一致性检验（CR < 0.1）

#### 3.2 熵权法客观权重
- 数据标准化（min-max 或 z-score）
- 计算信息熵
- 计算权重

#### 3.3 组合赋权
- 乘法归一化：w = (w_ahp * w_entropy) / Σ(w_ahp * w_entropy)
- 或线性加权：w = α * w_ahp + (1-α) * w_entropy

#### 3.4 TOPSIS 排序
- 正向化处理
- 标准化
- 计算正负理想解
- 计算相对贴近度
- 排序

#### 3.5 质量等级划分
- 优秀：C ≥ 0.8
- 良好：0.6 ≤ C < 0.8
- 一般：0.4 ≤ C < 0.6
- 较差：C < 0.4

#### 3.6 敏感性分析
- 调整权重 ±10%
- 观察排序变化
- 计算 Spearman 排序相关系数

---

### 4. 视频质量评价

#### 4.1 视频基础信息
- 分辨率
- FPS
- 帧数
- 时长
- 文件大小

#### 4.2 抽帧策略
- 短视频（< 30s）：全帧分析
- 长视频：每秒抽 1 帧
- 输出：`figures/video_frames/`

#### 4.3 Contact Sheet
- 拼接关键帧为网格图
- 输出：`figures/video_contact_sheet.png`
- 供 GPT-5.5 审查

#### 4.4 时序指标（相邻帧计算）

| 指标 | 计算方法 | 说明 |
|------|----------|------|
| ssim_prev | 结构相似性 | 帧间一致性 |
| frame_diff_mean | 像素差均值 | 运动幅度 |
| brightness_delta | 亮度变化 | 闪烁检测 |
| saturation_delta | 饱和度变化 | 色彩稳定性 |
| optical_flow_magnitude_mean | Farneback 光流幅值 | 运动强度 |
| optical_flow_angle_change | 光流方向变化 | 运动方向稳定性 |

#### 4.5 时序失稳惩罚项
- instability_score = w1 * (1 - ssim) + w2 * frame_diff + w3 * brightness_delta

#### 4.6 异常帧定位
- 阈值：instability_score > μ + 2σ
- 输出：`results/video_anomaly_frames.csv`

---

### 5. 多模态审查（GPT-5.5 负责）

#### 5.1 GPT-5.5 职责
- 图像语义保真度审查
- 视频关键帧异常解释
- 论文逻辑和表达审稿

#### 5.2 GPT-5.5 禁止事项
- ❌ 不允许直接生成数值指标
- ❌ 不允许编造题面没有的信息
- ❌ 不确定内容必须标注"不确定"

#### 5.3 审查输出
- `docs/vision_review.md`
- 格式：
  ```
  ## 图像 1.png 审查
  - 语义描述：...
  - 异常标注：...
  - 不确定项：...
  ```

---

### 6. 输出文件清单

| 文件 | 内容 |
|------|------|
| `results/media_inventory.csv` | 媒体文件清单 |
| `results/image_metrics.csv` | 图像技术指标 |
| `results/image_scores.csv` | 图像综合得分 |
| `results/video_basic_info.csv` | 视频基础信息 |
| `results/video_metrics.csv` | 视频时序指标 |
| `results/video_anomaly_frames.csv` | 异常帧列表 |
| `results/final_summary.csv` | 最终汇总 |
| `results/results.xlsx` | Excel 汇总表 |
| `figures/*.png` | 图表（PNG） |
| `figures/*.svg` | 图表（SVG） |
| `paper/outline.md` | 论文大纲 |
| `paper/draft.md` | 论文草稿 |

---

## 脚本调用顺序

```powershell
python src/check_env.py          # 检查环境
python src/extract_pdf.py        # 提取 PDF
python src/extract_docx.py       # 提取 DOCX
python src/inspect_media.py      # 检查媒体
python src/image_metrics.py      # 图像指标
python src/video_slice.py        # 视频抽帧
python src/video_metrics.py      # 视频指标
python src/evaluation_models.py  # 综合评价
python src/export_excel.py       # 导出 Excel
python src/plot_results.py       # 生成图表
```

或一键运行：
```powershell
python src/main.py
```

---

*专为 2026 中青杯 B 题设计*
*Last updated: 2026-06-04*
