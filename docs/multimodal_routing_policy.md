# 多模态路由策略

**创建时间**: 2026-06-04
**适用范围**: 2026 中青杯 B 题项目

---

## 1. 模型能力边界

### Sisyphus / mimo-v2.5-pro

- **不支持**直接处理图片输入
- **负责**代码、脚本、结果、图表、文件组织
- **擅长**文本处理、数据分析、代码编写

### GPT-5.5

- **支持**图片理解
- **负责**多模态审查
- **擅长**图像语义描述、视觉异常识别

---

## 2. 多模态任务路由

### GPT-5.5 负责的任务

| 任务 | 输入 | 输出 |
|------|------|------|
| 图像语义描述 | 图片文件 | 文字描述 |
| 视觉异常识别 | 图片文件 | 异常标注 |
| 语义保真度审查 | 图片 + 提示词 | 审查报告 |
| PDF 页面图核验 | PDF 页面图片 | 文字提取 |
| 视频关键帧连续性审查 | 关键帧拼图 | 连续性评估 |
| 异常帧语义解释 | 异常帧截图 | 语义解释 |

### Sisyphus 负责的任务

| 任务 | 输入 | 输出 |
|------|------|------|
| 图像技术指标计算 | 图片文件 | CSV 数据 |
| 视频时序指标计算 | 视频文件 | CSV 数据 |
| AHP/熵权/TOPSIS | 指标数据 | 排名结果 |
| Excel 导出 | CSV 数据 | XLSX 文件 |
| 图表生成 | 数据 | PNG/SVG |

---

## 3. 推荐 Agent 路由

### 多模态任务首选

| Agent | 用途 | 优先级 |
|-------|------|--------|
| `@sisyphus-junior` | 通用任务执行 | 首选 |
| `@hephaestus` | 专用多模态审查 | 首选 |

### 备选 Agent

| Agent | 用途 | 优先级 |
|-------|------|--------|
| `@oracle` | 架构咨询 | 备选 |
| `@metis` | 预规划分析 | 备选 |
| `@momus` | 计划审查 | 备选 |

### 不推荐

| Agent | 原因 |
|-------|------|
| `@multimodal-looker` | primary model 仍是 Gemini，可能出现超时或 image endpoint 错误 |

---

## 4. 工作流示例

### 图像质量评价

```
1. Sisyphus: 运行 image_metrics.py → results/image_metrics.csv
2. Sisyphus: 运行 evaluation_models.py → results/image_scores.csv
3. GPT-5.5: 审查图片语义 → docs/vision_review.md
4. Sisyphus: 合并定量+定性结果 → 论文
```

### 视频质量评价

```
1. Sisyphus: 运行 video_slice.py → figures/video_frames/
2. Sisyphus: 运行 video_metrics.py → results/video_metrics.csv
3. GPT-5.5: 审查关键帧 → docs/vision_review.md
4. Sisyphus: 合并定量+定性结果 → 论文
```

---

## 5. 禁止事项

### GPT-5.5 不做

- ❌ 直接生成数值指标
- ❌ 修改 results 数据
- ❌ 编造题面没有的信息
- ❌ 替代 OpenCV/SSIM/光流计算

### Sisyphus 不做

- ❌ 直接处理图片输入
- ❌ 进行图像语义判断
- ❌ 生成视觉审查报告

---

*创建时间: 2026-06-04*
