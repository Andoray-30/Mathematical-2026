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

## 多智能体分工

### Sisyphus / mimo-v2.5-pro 负责

- 项目规划
- 文件结构整理
- 读取文本文件
- 编写和运行 Python 脚本
- 本地环境检查
- PDF/DOCX/XLSX 解析脚本
- 图片/视频指标计算
- 结果表格、Excel、图表生成
- 论文 Markdown 草稿组织
- 支撑材料整理

### GPT-5.5 Deep Agent 负责

- 图片语义理解
- PDF 页面截图理解
- 视频关键帧/拼图理解
- 图像语义保真度审查
- 视频异常帧语义解释
- 论文逻辑和表达审稿

### 多模态路由策略

**Sisyphus 不支持图片输入**，多模态任务路由如下：

| 任务类型 | 执行者 | 说明 |
|----------|--------|------|
| 图像技术指标 | Sisyphus | OpenCV/SSIM/光流计算 |
| 视频时序指标 | Sisyphus | 帧差/光流/异常检测 |
| 图像语义描述 | GPT-5.5 | 物体/场景/风格识别 |
| 视觉异常识别 | GPT-5.5 | 伪影/扭曲/不一致 |
| 语义保真度审查 | GPT-5.5 | 提示词匹配度 |

**推荐 Agent**：
- 首选：`@sisyphus-junior`、`@hephaestus`
- 备选：`@oracle`、`@metis`、`@momus`
- 不推荐：`@multimodal-looker`（Gemini 模型可能超时）

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
