# 适配报告 - 2026 中青杯 B 题项目

**生成时间**: 2026-06-04

---

## 1. 已创建文件列表

### 文档文件
| 文件 | 说明 |
|------|------|
| `AGENTS.md` | 项目级智能体规则 |
| `requirements.txt` | Python 依赖列表 |
| `docs/project_inventory.md` | 项目盘点报告 |
| `docs/skill_extracted_workflow.md` | 从 skill 提取的工作流 |
| `docs/skill_extracted_algorithms.md` | 从 skill 提取的算法说明 |
| `docs/skill_extracted_tools.md` | 从 skill 提取的工具使用方法 |
| `docs/skill_to_b_problem_mapping.md` | Skill 到 B 题的映射 |
| `docs/environment_setup.md` | 环境配置指南 |
| `docs/adaptation_report.md` | 本文件 |

### OpenCode Skills
| 文件 | 说明 |
|------|------|
| `.opencode/skills/math-modeling/SKILL.md` | 项目级数学建模技能 |
| `.opencode/skills/aigc-quality-eval/SKILL.md` | B 题专用质量评价技能 |

### OpenCode Commands
| 文件 | 说明 |
|------|------|
| `.opencode/commands/prepare-project.md` | 检查项目准备状态 |
| `.opencode/commands/prepare-media.md` | 准备媒体文件 |
| `.opencode/commands/run-analysis.md` | 运行分析流程 |
| `.opencode/commands/vision-review.md` | 多模态审查 |
| `.opencode/commands/write-paper.md` | 撰写论文 |

### Python 脚本
| 文件 | 说明 |
|------|------|
| `src/check_env.py` | 环境检查脚本 |
| `src/extract_pdf.py` | PDF 提取脚本 |
| `src/extract_docx.py` | DOCX 提取脚本 |
| `src/inspect_media.py` | 媒体检查脚本 |
| `src/image_metrics.py` | 图像指标计算脚本 |
| `src/video_slice.py` | 视频抽帧脚本 |
| `src/video_metrics.py` | 视频指标计算脚本 |
| `src/evaluation_models.py` | 综合评价模型脚本 |
| `src/export_excel.py` | Excel 导出脚本 |
| `src/plot_results.py` | 图表生成脚本 |
| `src/main.py` | 主流程脚本 |

---

## 2. 从 math-modeling-skill-main 提取的内容

### 已提取
- 三阶段工作流（建模分析 → 代码实现 → 论文撰写）
- Model Contract 前置合同框架
- AHP 层次分析法
- 熵权法
- TOPSIS 综合评价
- 组合赋权方法
- 敏感性分析
- Claim-Evidence 映射
- 自审清单
- PDF/DOCX/XLSX 处理方法
- 可视化规范

### 已排除
- 大规模优化算法（遗传算法、PSO 等）
- 时间序列预测（ARIMA、LSTM 等）
- 图论路径规划
- 美赛英文写作流程
- Outstanding Thesis 全量论文库
- 与 B 题无关的算法模板

---

## 3. B 题项目事实源

### 最高优先级
1. `B题：AI生成内容的质量评估与参数优化/`
   - B 题题面 PDF
   - 附件图片（8张）
   - 附件视频（车流视频.mp4）
   - 论文模板
   - 参赛细则
   - 诚信告知书

2. `中青杯数学建模2026规则文档.md`
   - 竞赛规则
   - 提交规范
   - 论文格式要求

### 参考能力库
3. `math-modeling-skill-main/`
   - 三阶段工作流
   - 算法资源库
   - 文档处理方法

---

## 4. 本地工具能力

| 工具 | 状态 | 说明 |
|------|------|------|
| PDF 处理 | ✅ | PyMuPDF + pdfplumber |
| DOCX 处理 | ✅ | python-docx |
| XLSX 处理 | ✅ | openpyxl + pandas |
| 图片处理 | ✅ | OpenCV + Pillow + scikit-image |
| 视频处理 | ✅ | OpenCV + FFmpeg |
| 图表生成 | ✅ | matplotlib + seaborn |
| 文献搜索 | ⚠️ | 需要网络连接 |

---

## 5. 环境状态

### 已完成
- [x] 目录结构创建
- [x] AGENTS.md 创建
- [x] requirements.txt 创建
- [x] OpenCode skills 创建
- [x] OpenCode commands 创建
- [x] Python 脚本创建

### 待完成
- [ ] Python 安装
- [ ] FFmpeg 安装
- [ ] 虚拟环境创建
- [ ] 依赖安装
- [ ] B 题 PDF 内容提取
- [ ] 图像/视频指标计算
- [ ] 综合评价
- [ ] 论文撰写

---

## 6. 下一步操作

### 第一步：环境配置
```powershell
# 安装 Python
winget install Python.Python.3.12

# 安装 FFmpeg
winget install Gyan.FFmpeg

# 创建虚拟环境
python -m venv .venv
.\.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 第二步：检查环境
```powershell
python src/check_env.py
```

### 第三步：准备媒体文件
```powershell
# 或使用 OpenCode command
python src/extract_pdf.py
python src/extract_docx.py
python src/inspect_media.py
python src/video_slice.py
```

### 第四步：运行分析
```powershell
python src/image_metrics.py
python src/video_metrics.py
python src/evaluation_models.py
python src/export_excel.py
python src/plot_results.py
```

### 第五步：一键运行
```powershell
python src/main.py
```

### 第六步：多模态审查
- 让 GPT-5.5 Deep Agent 审查 `figures/pdf_pages/*.png`
- 让 GPT-5.5 审查 `figures/video_contact_sheet.png`
- 输出 `docs/vision_review.md`

### 第七步：撰写论文
- 读取 `results/*.csv` 和 `figures/*.png`
- 按照 `中青杯数学建模2026规则文档.md` 格式要求
- 输出 `paper/draft.md`

---

## 7. 技术约束

1. **主模型限制**: mimo-v2.5-pro 不支持 PDF/图像直接输入
2. **多模态理解**: 由 GPT-5.5 Deep Agent 负责
3. **数据来源**: 所有可量化指标必须由本地代码生成
4. **可追溯性**: 所有结论必须能追溯到 `results/` 或 `figures/`
5. **禁止编造**: 不允许编造数据、实验结果、图表、文献

---

*Last updated: 2026-06-04*
