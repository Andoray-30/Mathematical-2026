# 参考文献核验报告

**生成时间**: 2026-06-05
**核验目的**: 确保参考文献真实性、格式和正文引用一致性

---

## 一、核验结果总览

| 编号 | 状态 | 问题说明 |
|------|------|----------|
| [1] | ✅ 保留 | AIGCIQA2023，arXiv:2307.00211，已验证 |
| [2] | ✅ 保留 | AGIQA-1K，arXiv:2303.12618，已验证 |
| [3] | ✅ 保留 | TIER，arXiv:2401.03854，已验证 |
| [4] | ✅ 保留 | MINT-IQA，arXiv:2405.07346，已验证 |
| [5] | ✅ 保留 | SSIM原始论文，Wang et al. 2004，经典文献 |
| [6] | ✅ 保留 | AHP方法，Saaty 1980，经典文献 |
| [7] | ✅ 保留 | 熵权法，Shannon 1948，经典文献 |
| [8] | ✅ 保留 | TOPSIS方法，Hwang & Yoon 1981，经典文献 |
| [9] | ✅ 保留 | 灰色系统理论，Deng 1989，经典文献 |
| [10] | ✅ 保留 | 光流方法，Farnebäck 2003，经典文献 |
| [11] | ✅ 保留 | AHP-熵权组合，Li et al. 2013 |
| [12] | ✅ 保留 | 熵权-TOPSIS组合，Ecer 2020 |
| [13] | ✅ 保留 | 灰色关联分析，Gerus-Gościewska 2021 |
| [14] | ✅ 保留 | 灰色关联分析应用，Hsiao 2017 |
| [15] | ❌ 修正 | 作者和题名错误，需修正 |
| [16] | ❌ 修正 | 作者错误，年份需修正 |
| [17] | ✅ 保留 | 3D-SSIM，Wang et al. 2012 |
| [18] | ✅ 保留 | 光流VQA，Gunasekar et al. 2016 |
| [19] | 🔧 格式修正 | AI工具引用格式需调整 |
| [20] | 🔧 格式修正 | AI工具引用格式需调整 |
| [21] | 🔧 格式修正 | AI工具引用格式需调整 |

---

## 二、修正文献详情

### [15] 原始引用（错误）

```
[15] Danier D, Li Z, Bull D. PSNRDIV: A Motion Divergence Weighted Quality Metric for Video Frame Interpolation[J]. arXiv preprint arXiv:2510.01361, 2025.
```

**问题**：
- 作者错误：正确作者是 Conall Daly, Darren Ramsook, Anil Kokaram
- 题名错误：正确题名是 "An Efficient Quality Metric for Video Frame Interpolation Based on Motion-Field Divergence"
- 会议信息缺失：IEEE 17th International Conference on Quality of Multimedia Experience 2025

**修正后**：
```
[15] Daly C, Ramsook D, Kokaram A. An Efficient Quality Metric for Video Frame Interpolation Based on Motion-Field Divergence[C]//Proceedings of the 17th International Conference on Quality of Multimedia Experience. 2025.
```

---

### [16] 原始引用（错误）

```
[16] Janowski L, Kowalski M, Mikołajczyk T, et al. Temporally Aware Objective Quality Metric for Immersive Video[J]. Applied Sciences, 2025, 16(1): 274.
```

**问题**：
- 作者错误：正确作者是 Jakub Stankowski, Bartosz Sojka, Tomasz Grajek, Adrian Dziembowski
- 年份错误：正确年份是2026年（发表于2025年12月26日）

**修正后**：
```
[16] Stankowski J, Sojka B, Grajek T, et al. Temporally Aware Objective Quality Metric for Immersive Video[J]. Applied Sciences, 2026, 16(1): 274.
```

---

### [19]-[21] AI工具引用格式修正

**原始格式**（不符合中青杯要求）：
```
[19] OpenAI. GPT-5.5[EB/OL]. OpenAI, 2026-06-04.
```

**中青杯要求格式**：
```
[编号] 工具名称，版本/型号，开发机构/公司，使用日期
```

**修正后**：
```
[19] GPT-5.5, GPT-5.5, OpenAI, 2026-06-04
[20] OpenCode, 最新版本, OhMyOpenCode, 2026-06-04
[21] Gemini, 3.1-pro-preview, Google, 2026-06-04
```

---

## 三、文献分类与论文对应关系

| 类别 | 编号 | 对应论文章节 |
|------|------|-------------|
| AIGC质量评价 | [1]-[4] | 问题一：AIGC图像质量评价背景 |
| 图像质量评价基础 | [5] | 问题一：SSIM定义 |
| AHP方法 | [6] | 问题二：AHP权重计算 |
| 熵权法 | [7] | 问题二：熵权计算 |
| TOPSIS方法 | [8] | 问题二：TOPSIS排序 |
| 灰色系统理论 | [9] | 问题二：灰色关联校验 |
| 光流方法 | [10] | 问题三：光流计算 |
| AHP-熵权组合 | [11]-[12] | 问题二：组合赋权 |
| 灰色关联分析 | [13]-[14] | 问题二：稳健性验证 |
| 视频质量评价 | [15]-[18] | 问题三：视频时序失稳检测 |
| AI工具 | [19]-[21] | AI工具使用声明 |

---

## 四、删除或替换文献

无删除文献。所有文献经核验后保留或修正。

---

## 五、核验结论

1. **保留文献**：16篇（[1]-[14], [17]-[18]）
2. **修正文献**：2篇（[15], [16]）- 作者、题名、年份修正
3. **格式修正**：3篇（[19]-[21]）- AI工具引用格式调整
4. **总计**：21篇

---

*生成时间: 2026-06-05*
