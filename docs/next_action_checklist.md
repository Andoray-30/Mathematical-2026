# 下一步行动清单

**确定时间**: 2026-06-05
**当前阶段**: 正式建模准备完成，进入结果生成阶段

---

## 已完成事项

- [x] 题面核验：确认B题PDF已正确提取
- [x] PDF页面图修正：重新渲染2张B题页面图
- [x] 多模态审查：完成8张图像和视频的GPT-5.5审查
- [x] 建模方案设计：Metis设计3套路线
- [x] 方案批判：Momus完成路线 critique
- [x] 最终决策：Oracle确定Route 1.5
- [x] 输出文档：
  - `docs/problem_statement_verified.md`
  - `docs/problem_statement_verification_report.md`
  - `docs/final_modeling_plan.md`
  - `docs/innovation_points.md`
  - `docs/paper_structure_plan.md`
  - `docs/claim_evidence_map.md`

---

## 待完成事项

### Phase 4: 代码修改与结果生成

**优先级**: 高
**负责人**: Sisyphus + 编程手

#### 4.1 修改现有脚本

- [ ] 修改 `src/image_metrics.py`
  - 确保输出到 `results/final/image_metrics.csv`
  - 包含15个指标

- [ ] 修改 `src/video_metrics.py`
  - 确保输出到 `results/final/video_metrics.csv`
  - 包含SSIM、帧差、光流、亮度/饱和度变化

- [ ] 修改 `src/evaluation_models.py`
  - 新增三维度归并逻辑
  - 新增组合赋权
  - 新增敏感性分析
  - 新增灰色关联校验
  - 输出到 `results/final/`

- [ ] 修改 `src/export_excel.py`
  - 汇总所有结果到 `results/final/results.xlsx`

- [ ] 修改 `src/plot_results.py`
  - 输出到 `figures/final/`
  - 包含所有必需图表

#### 4.2 新增脚本

- [ ] 新增 `src/dimension_scores.py`
  - 计算三维度得分
  - 输出到 `results/final/image_dimension_scores.csv`

- [ ] 新增 `src/sensitivity_analysis.py`
  - 权重扰动分析
  - 输出到 `results/final/sensitivity_analysis.csv`

- [ ] 新增 `src/gray_relation.py`
  - 灰色关联校验
  - 输出到 `results/final/gray_relation_check.csv`

- [ ] 新增 `src/parameter_optimization.py`
  - 短板诊断
  - 参数建议
  - 输出到 `results/final/parameter_optimization_suggestions.csv`

#### 4.3 运行完整流水线

- [ ] 运行 `python src/main.py`
  - 生成所有 `results/final/` 文件
  - 生成所有 `figures/final/` 文件

#### 4.4 验证结果

- [ ] 检查 `results/final/` 是否包含16个文件
- [ ] 检查 `figures/final/` 是否包含21个文件
- [ ] 验证数据完整性

---

### Phase 5: 论文撰写

**优先级**: 高
**负责人**: 论文手

#### 5.1 论文大纲

- [ ] 根据 `docs/paper_structure_plan.md` 创建论文大纲
- [ ] 确定各章节字数分配

#### 5.2 论文正文

- [ ] 撰写摘要
- [ ] 撰写问题重述
- [ ] 撰写问题分析
- [ ] 撰写模型假设
- [ ] 撰写符号说明
- [ ] 撰写数据来源与预处理
- [ ] 撰写问题一模型建立与求解
- [ ] 撰写问题二模型建立与求解
- [ ] 撰写问题三模型建立与求解
- [ ] 撰写模型评价与推广
- [ ] 撰写参考文献
- [ ] 撰写AI工具使用声明
- [ ] 撰写附录

#### 5.3 论文审查

- [ ] 使用GPT-5.5进行逻辑审查
- [ ] 检查Claim-Evidence映射完整性
- [ ] 检查图表引用正确性
- [ ] 检查格式规范

---

### Phase 6: 最终提交

**优先级**: 中
**负责人**: Sisyphus

#### 6.1 论文PDF生成

- [ ] 将论文转换为PDF
- [ ] 命名为 `B2026XXXXX.pdf`

#### 6.2 支撑材料打包

- [ ] 创建 `support/ai_usage_log.md`
- [ ] 创建 `support/README.md`
- [ ] 打包为 `B2026XXXXX材料.zip`

#### 6.3 最终检查

- [ ] 检查论文是否包含身份信息
- [ ] 检查数据是否可追溯
- [ ] 检查AI工具使用声明是否完整

---

## 时间安排建议

| 阶段 | 时间 | 任务 |
|------|------|------|
| Phase 4 | Day 1-2 | 代码修改、结果生成、验证 |
| Phase 5 | Day 2-3 | 论文撰写、审查 |
| Phase 6 | Day 3 | 最终提交准备 |

---

## 风险与应对

| 风险 | 应对措施 |
|------|----------|
| 代码运行失败 | 检查依赖、调试代码 |
| 结果与预期不符 | 检查数据、调整参数 |
| 论文写作超时 | 优先完成核心章节 |
| 格式不规范 | 使用论文模板 |

---

## 关键提醒

1. **不要使用archive中的测试结果作为最终结果**
2. **所有结果必须重新生成到results/final/**
3. **所有图表必须重新生成到figures/final/**
4. **GPT-5.5不直接生成数值指标**
5. **论文中不出现身份信息**

---

*确定时间: 2026-06-05*
