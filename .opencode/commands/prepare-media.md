---
name: prepare-media
description: "准备媒体文件 - 提取 PDF 文本、检查媒体、生成关键帧拼图"
---

# 准备媒体文件

处理 B 题附件，为后续分析做准备。

## 执行步骤

1. **提取 PDF 文本**
   ```powershell
   python src/extract_pdf.py
   ```
   - 输出：`docs/problem_statement.md`
   - 输出：`docs/pdf_extract_report.md`
   - 输出：`figures/pdf_pages/*.png`

2. **提取 DOCX 模板**
   ```powershell
   python src/extract_docx.py
   ```
   - 输出：`docs/template_extracted.md`

3. **检查媒体文件**
   ```powershell
   python src/inspect_media.py
   ```
   - 输出：`results/media_inventory.csv`

4. **视频抽帧**
   ```powershell
   python src/video_slice.py
   ```
   - 输出：`figures/video_frames/*.png`
   - 输出：`figures/video_contact_sheet.png`

## 输出文件

| 文件 | 内容 |
|------|------|
| `docs/problem_statement.md` | B 题文字内容 |
| `docs/pdf_extract_report.md` | PDF 提取报告 |
| `figures/pdf_pages/*.png` | PDF 页面图片 |
| `docs/template_extracted.md` | 论文模板结构 |
| `results/media_inventory.csv` | 媒体文件清单 |
| `figures/video_frames/*.png` | 视频帧 |
| `figures/video_contact_sheet.png` | 视频关键帧拼图 |

## 后续步骤

运行完成后，可执行：
- `run-analysis` - 运行指标计算
- `vision-review` - 让 GPT-5.5 审查图像/视频
