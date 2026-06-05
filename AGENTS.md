# AGENTS.md - 2026 中青杯 B 题项目规则

## 项目概述

本项目是 **2026 年第八届中青杯全国大学生数学建模竞赛 B 题**项目。

**B 题名称**：AI 生成内容的质量评估与参数优化

**当前阶段**：能力验收完成，进入正式建模准备阶段

---

## 事实源优先级

### 最高优先级（事实源）

1. **`B题：AI生成内容的质量评估与参数优化/`**
   - B 题题面 PDF
   - 附件图片（8张）
   - 附件视频（车流视频.mp4）
   - 论文模板
   - 参赛细则
   - 诚信告知书

2. **`中青杯数学建模2026规则文档.md`**
   - 竞赛规则
   - 提交规范
   - 论文格式要求
   - AI 工具使用说明

### 参考能力库（不是事实源）

3. **`math-modeling-skill-main/`**
   - 三阶段工作流
   - 算法资源库
   - 文档处理方法
   - 可视化规范
   - **不允许覆盖 B 题题面和规则**

---

## 智能体配置与分工

### 模型能力矩阵

| 模型 | 图像支持 | 上下文窗口 | 输出限制 | 用途 |
|------|----------|------------|----------|------|
| mimo-v2.5-pro | ❌ 文本 | 800K | 65K | 主执行、写作 |
| gpt-5.5 | ✅ 图像 | 840K | 102K | 多模态、复杂推理 |
| gemini-3.5-flash | ✅ 图像 | 800K | 51K | 多模态备选 |
| gemini-3.1-pro-preview | ✅ 图像 | - | - | 多模态专用 |
| deepseek-v4-flash-free | ❌ 文本 | - | - | 快速任务 |
| minimax-m3-free | ❌ 文本 | - | - | 低优先级任务 |

### 主智能体

| 智能体 | 模型 | 图像支持 | 擅长工作 |
|--------|------|----------|----------|
| **sisyphus** | mimo-v2.5-pro | ❌ | 项目规划、代码编写、文件整理、数据分析、图表生成 |
| **sisyphus-junior** | gpt-5.5 | ✅ | 任务执行、多模态审查、复杂推理 |
| **hephaestus** | gpt-5.5 | ✅ | 专用多模态审查、图像分析、视觉异常识别 |
| **oracle** | gpt-5.5 | ✅ | 架构咨询、复杂问题调试、技术决策 |
| **multimodal-looker** | gemini-3.1-pro-preview | ✅ | 多模态查看（可能超时） |

### 辅助智能体

| 智能体 | 模型 | 图像支持 | 擅长工作 |
|--------|------|----------|----------|
| **explore** | deepseek-v4-flash-free | ❌ | 代码搜索、模式发现、文件定位 |
| **librarian** | minimax-m3-free | ❌ | 文档查询、外部资源搜索 |
| **prometheus** | mimo-v2.5-pro | ❌ | 任务规划、工作流设计 |
| **metis** | gpt-5.5 | ✅ | 预规划分析、需求澄清 |
| **momus** | gpt-5.5 | ✅ | 计划审查、质量验证 |
| **atlas** | mimo-v2.5-pro | ❌ | 通用任务执行 |

### 任务分类

| 分类 | 模型 | 图像支持 | 适用场景 |
|------|------|----------|----------|
| **visual-engineering** | gpt-5.5 | ✅ | 前端、UI/UX、设计 |
| **ultrabrain** | gpt-5.5 | ✅ | 复杂逻辑、算法设计 |
| **deep** | gpt-5.5 | ✅ | 深度研究、自主问题解决 |
| **artistry** | gemini-3.1-pro-preview | ✅ | 创意任务、非传统方法 |
| **quick** | deepseek-v4-flash-free | ❌ | 快速修复、简单修改 |
| **unspecified-low** | minimax-m3-free | ❌ | 低优先级任务 |
| **unspecified-high** | mimo-v2.5-pro | ❌ | 高优先级通用任务 |
| **writing** | mimo-v2.5-pro | ❌ | 文档撰写、论文写作 |

---

## 多模态任务路由

### 图像相关任务

| 任务 | 执行者 | 原因 |
|------|--------|------|
| 图像技术指标计算 | Sisyphus (mimo-v2.5-pro) | OpenCV 计算，不需要图像理解 |
| 图像语义描述 | hephaestus (gpt-5.5) | 需要图像理解能力 |
| 视觉异常识别 | hephaestus (gpt-5.5) | 需要图像理解能力 |
| 语义保真度审查 | hephaestus (gpt-5.5) | 需要图像理解能力 |
| PDF 页面核验 | sisyphus-junior (gpt-5.5) | 需要图像理解能力 |

### 视频相关任务

| 任务 | 执行者 | 原因 |
|------|--------|------|
| 视频抽帧 | Sisyphus (mimo-v2.5-pro) | FFmpeg 命令行操作 |
| 视频时序指标 | Sisyphus (mimo-v2.5-pro) | OpenCV/SSIM 计算 |
| 关键帧连续性审查 | hephaestus (gpt-5.5) | 需要图像理解能力 |
| 异常帧语义解释 | hephaestus (gpt-5.5) | 需要图像理解能力 |

### 文本/代码任务

| 任务 | 执行者 | 原因 |
|------|--------|------|
| 代码编写 | Sisyphus (mimo-v2.5-pro) | 文本任务，不需要图像 |
| 数据分析 | Sisyphus (mimo-v2.5-pro) | 数值计算 |
| 图表生成 | Sisyphus (mimo-v2.5-pro) | matplotlib 代码 |
| 论文撰写 | Sisyphus (mimo-v2.5-pro) | 文本任务 |
| 代码搜索 | explore (deepseek) | 快速搜索 |
| 文档查询 | librarian (minimax) | 文档检索 |

---

## 关键约束

1. **所有可量化指标必须由本地代码生成**
   - 不允许 GPT-5.5 直接凭视觉感觉生成数值结果

2. **所有图表、CSV、Excel、论文结论必须可追溯到代码输出**

3. **不依赖 `look_at` 作为主流程**
   - 所有 PDF、Word、Excel、图片、视频必须优先通过本地脚本转成 Markdown、CSV、Excel、PNG/SVG 图表、关键帧拼图后再分析

4. **不允许编造数据、实验结果、图表、文献、AI 使用记录**

5. **所有结论必须能追溯到 `results/` 或 `figures/`**

6. **所有图表必须由代码生成**

7. **所有中间数据和最终结果必须保存**

8. **论文不得出现学校、队员姓名等身份信息**

---

## 目录结构

```
F:\Mathematical 2026\
├── AGENTS.md                       # 本文件
├── requirements.txt                # Python 依赖
├── 中青杯数学建模2026规则文档.md
├── B题：AI生成内容的质量评估与参数优化/  # 原始赛题资料（只读）
├── math-modeling-skill-main/       # 参考能力库（只读）
├── archive/                        # 归档目录
│   └── capability_test_2026-06-04/ # 能力验收阶段产物
├── docs/                           # 核心文档
│   ├── project_inventory.md
│   ├── environment_setup.md
│   ├── skill_to_b_problem_mapping.md
│   ├── vision_review_input_manifest.md
│   ├── vision_review_test.md
│   ├── workspace_cleanup_report.md
│   ├── capability_acceptance_summary.md
│   └── multimodal_routing_policy.md
├── src/                            # 源代码
│   ├── check_env.py
│   ├── smoke_test.py
│   ├── extract_pdf.py
│   ├── extract_docx.py
│   ├── inspect_media.py
│   ├── image_metrics.py
│   ├── video_slice.py
│   ├── video_metrics.py
│   ├── evaluation_models.py
│   ├── export_excel.py
│   ├── plot_results.py
│   └── main.py
├── results/                        # 结果数据
│   ├── final/                      # 正式建模最终结果
│   └── intermediate/               # 正式建模中间表格
├── figures/                        # 图表
│   ├── final/                      # 正式论文图表
│   ├── intermediate/               # 探索分析图
│   └── vision_inputs/              # GPT-5.5 输入材料
├── paper/                          # 论文
├── support/                        # 支撑材料
│   ├── ai_usage_log.md
│   └── README.md
└── .opencode/                      # OpenCode 配置
    ├── skills/
    │   ├── math-modeling/
    │   └── aigc-quality-eval/
    └── commands/
        ├── prepare-project.md
        ├── prepare-media.md
        ├── run-analysis.md
        ├── vision-review.md
        └── write-paper.md
```

---

## 最终交付物

1. **论文 PDF**
   - 命名格式：`B2026XXXXX.pdf`

2. **支撑材料 zip/rar**
   - 命名格式：`B2026XXXXX材料.zip`

3. **源代码**
   - `src/` 目录下所有 Python 脚本

4. **原始数据和派生数据**
   - `results/final/` 目录下最终结果
   - `results/intermediate/` 目录下中间表格

5. **图表**
   - `figures/final/` 目录下正式论文图表

6. **AI 工具使用说明**
   - `support/ai_usage_log.md`

7. **支撑材料说明**
   - `support/README.md`

---

## 禁止事项

1. ❌ 修改 B 题原始资料
2. ❌ 删除 math-modeling-skill-main
3. ❌ 编造数据、实验结果、图表、文献
4. ❌ 论文中出现身份信息
5. ❌ 让 GPT-5.5 直接生成数值指标
6. ❌ 静默跳过失败步骤
7. ❌ 使用 look_at 作为主流程
8. ❌ 将测试结果散落在 results/ 根目录

---

## 建模路线（B 题专用）

### 图像质量评价

- 语义保真度
- 技术质量
- 结构完整性

### 图像技术指标

- 分辨率
- Laplacian 清晰度
- Tenengrad 梯度
- 亮度均值与标准差
- 饱和度均值与标准差
- 图像熵
- Canny 边缘密度
- 噪声估计
- 结构完整性代理指标

### 图像综合排序

- AHP 主观权重
- 熵权法客观权重
- 组合赋权
- TOPSIS 排序
- 质量等级划分
- 敏感性分析

### 视频质量评价

- 视频基础信息
- 抽帧
- contact sheet
- 帧间 SSIM
- 帧差均值
- 亮度波动
- 饱和度波动
- Farneback 光流幅值
- 光流方向变化
- 时序失稳惩罚项
- 异常帧定位

---

## 已验证能力

| 能力 | 状态 | 说明 |
|------|------|------|
| Skill 加载 | ✅ | math-modeling 和 aigc-quality-eval |
| PDF 文本提取 | ✅ | B 题完整文字已提取 |
| PDF 页面渲染 | ✅ | 3 张页面图片 |
| 图片指标计算 | ✅ | 8 张图片 × 15 个指标 |
| 视频抽帧 | ✅ | 121 帧已提取 |
| 视频时序指标 | ✅ | SSIM、帧差、光流等 |
| AHP/熵权/TOPSIS | ✅ | 排名逻辑已修复 |
| Excel 输出 | ✅ | results.xlsx 已生成 |
| 图表输出 | ✅ | PNG 和 SVG 图表 |
| GPT-5.5 多模态审查 | ✅ | 测试通过 |

---

*Last updated: 2026-06-04*
