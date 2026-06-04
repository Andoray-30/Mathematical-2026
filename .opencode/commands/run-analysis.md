---
name: run-analysis
description: "运行分析流程 - 计算图像/视频指标、综合评价、生成图表"
---

# 运行分析

计算图像和视频质量指标，进行综合评价。

## 前置条件

确保已运行 `prepare-media`，且以下文件存在：
- `results/media_inventory.csv`
- `figures/video_frames/`

## 执行步骤

1. **计算图像指标**
   ```powershell
   python src/image_metrics.py
   ```
   - 输出：`results/image_metrics.csv`

2. **计算视频指标**
   ```powershell
   python src/video_metrics.py
   ```
   - 输出：`results/video_metrics.csv`
   - 输出：`results/video_anomaly_frames.csv`

3. **综合评价**
   ```powershell
   python src/evaluation_models.py
   ```
   - 输出：`results/image_scores.csv`
   - 输出：`results/final_summary.csv`

4. **导出 Excel**
   ```powershell
   python src/export_excel.py
   ```
   - 输出：`results/results.xlsx`

5. **生成图表**
   ```powershell
   python src/plot_results.py
   ```
   - 输出：`figures/*.png`
   - 输出：`figures/*.svg`

## 输出文件

| 文件 | 内容 |
|------|------|
| `results/image_metrics.csv` | 图像技术指标 |
| `results/video_metrics.csv` | 视频时序指标 |
| `results/video_anomaly_frames.csv` | 异常帧列表 |
| `results/image_scores.csv` | 图像综合得分 |
| `results/final_summary.csv` | 最终汇总 |
| `results/results.xlsx` | Excel 汇总表 |
| `figures/*.png` | 图表（PNG） |

## 后续步骤

运行完成后，可执行：
- `vision-review` - 让 GPT-5.5 审查结果
- `write-paper` - 开始撰写论文
