# Paper Outline

**Topic**: AI-Generated Content Quality Assessment and Parameter Optimization
**Competition**: 2026 中青杯 Mathematical Modeling Competition (Problem B)
**Route**: Route 1.5 (AHP-Entropy-TOPSIS + Lightweight Enhancements)

---

## Paper Structure

### 1. Abstract (350-450 words)

**Content**:
- Context: AIGC proliferation and quality assessment gap
- Problem: Three sub-problems (NR-IQA model, image evaluation, video temporal quality)
- Method: Three-dimension evaluation framework with AHP-Entropy-TOPSIS
- Results: Key ranking and anomaly findings
- Innovation: Four innovation points
- Robustness: Sensitivity and grey relation verification

**Key Evidence**:
- TOPSIS ranking results (Table 6)
- Video anomaly summary (Figure 8)

---

### 2. Problem Restatement (400-700 words)

**Content**:
- Restate B题 background and objectives
- Three sub-problems in own words
- Input/output relationships

**Evidence**: docs/problem_statement_verified.md

---

### 3. Problem Analysis (700-1000 words)

**Content**:
- Why image quality needs three dimensions (not just clarity)
- Why video must separate spatial and temporal quality
- Why parameter optimization should be inverse diagnosis

**Figure**: Framework flowchart (figures/final/framework_flowchart.png)

---

### 4. Model Assumptions (300-500 words)

**Assumptions**:
1. Image quality can be evaluated by semantic, technical, structural dimensions
2. AHP judgment matrix reflects problem requirements
3. Entropy weight captures data variation
4. Temporal instability can be quantified by SSIM, frame difference, brightness delta
5. Quality shortfalls can inform parameter optimization suggestions

---

### 5. Symbol Definitions (250-400 words)

**Key Symbols**:
- Q_img: Image comprehensive quality index [0,1]
- S_sem: Semantic fidelity score [0,100]
- S_tech: Technical quality score [0,100]
- S_str: Structural integrity score [0,100]
- w_j: Combined weight for dimension j
- C_i: TOPSIS closeness for image i
- I_t: Temporal instability score for frame t
- Q_video: Video comprehensive quality index

---

### 6. Data Source and Preprocessing (700-1000 words)

**Content**:
- Data source: 8 AI-generated images + 1 traffic video
- Preprocessing: Image metrics extraction (15 indicators)
- Video frame extraction (121 frames)
- Multimodal review structuring
- Data normalization and moderate-type transform

**Tables**:
- Image metrics summary (Table 1)
- Vision labels structure (Table 2)

**Figure**: Data preprocessing flowchart

---

### 7. Problem 1: NR-IQA Model (1400-2000 words)

**Content**:
- Three-dimension definition (semantic, technical, structural)
- Semantic fidelity: Equivalent reference description + structured labels
- Technical quality: Sharpness + naturalness (moderate-type transform)
- Structural integrity: Global proxy + local penalty
- Comprehensive evaluation model formula

**Formulas**:
- S_sem = 100 * clip(label_score - 0.20 * penalty, 0, 1)
- S_tech = 100 * (0.65 * sharpness + 0.35 * naturalness)
- S_str = 100 * clip(0.45*v1 + 0.15*v2 + 0.25*part_integrity + 0.15*geometry, 0, 1)

**Tables**:
- Dimension definitions (Table 3)
- AHP judgment matrix (Table 4)

---

### 8. Problem 2: Image Quality Evaluation (1400-2000 words)

**Content**:
- AHP weight calculation (CR<0.1)
- Entropy weight calculation
- Combined weight (eta=0.6)
- TOPSIS ranking
- Quality level classification
- Content type sensitivity analysis
- Cross-model reliability verification

**Figures**:
- Dimension scores bar chart (Figure 3)
- TOPSIS ranking (Figure 4)
- Weight comparison (Figure 5)
- TOPSIS vs GRA consistency (Figure 6)
- Sensitivity tornado (Figure 7)

**Tables**:
- TOPSIS results (Table 6)
- Rank stability (Table 7)

---

### 9. Problem 3: Video Temporal Quality (1200-1800 words)

**Content**:
- Temporal indicators (SSIM, frame diff, optical flow, warp-SSIM)
- Robust z-score normalization
- Instability score formula
- Anomaly detection (median + 2.5*MAD threshold)
- Video comprehensive quality score
- Anomaly frame analysis

**Formulas**:
- I_t = 0.22*z1 + 0.18*z2 + ... + 0.20*z7
- Threshold = median(I) + 2.5 * MAD(I)
- S_temp = 100*(1-mean(min(I,1))) - 10*anomaly_ratio

**Figures**:
- Video instability curve (Figure 8)
- Anomaly frames panel (Figure 9)

**Tables**:
- Video metrics summary (Table 8)
- Anomaly frames list (Table 9)

---

### 10. Parameter Optimization Suggestions (800-1200 words)

**Content**:
- Shortfall-to-parameter priority model
- Parameter-dimension effect matrix
- Priority score calculation
- Top priority adjustments

**Formulas**:
- shortfall = max(0, threshold - score)
- priority = sum(weight * shortfall * max(effect, 0))

**Figures**:
- Parameter priority heatmap (Figure 10)

**Tables**:
- Parameter suggestions (Table 10)

---

### 11. Model Evaluation and Promotion (500-900 words)

**Strengths**:
- Interpretable three-dimension framework
- Robust ranking (sensitivity + grey relation)
- Novel warp-SSIM for video
- Practical parameter optimization

**Limitations**:
- No original prompts available
- Small sample size (8 images, 1 video)
- No closed-loop regeneration verification

**Extensions**:
- CLIP/BLIP integration
- More samples and videos
- Real parameter optimization experiments

---

### 12. AI Tool Usage Statement (150-250 words)

**Statement**:
> This study used OpenCode for code organization and document management, and GPT-5.5 with Google multimodal models for semantic review and anomaly explanation of PDF pages, images, and video keyframes. These AI tools were used only for structured labeling and auxiliary explanations, not for generating final numerical results, model parameters, ranking conclusions, or charts. All indicator calculations, comprehensive evaluations, sensitivity analyses, grey relation verification, and result exports were completed by the authors' programs locally and manually verified.

---

### 13. References

**Key References**:
- AIGCIQA2023, AGIQA-3K, AGHI-QA (AIGC image quality)
- CLIP, CLIPScore, BLIP (text-image alignment)
- VBench, VBench-2.0, STREAM (video quality)
- ControlNet, Text2Video-Zero, TokenFlow (structure/temporal control)
- Classifier-Free Guidance, Zero Terminal SNR (generation parameters)
- Grey System Theory, Morris/Saltelli sensitivity (small sample robustness)

---

### 14. Appendix (2-5 pages)

**Content**:
- AHP judgment matrix and CR calculation
- Parameter effect matrix
- Sensitivity analysis scenarios
- Code snippets for key algorithms
- Additional figures and tables

---

## Figure List

| Figure | Description | File |
|--------|-------------|------|
| Figure 1 | Framework flowchart | framework_flowchart.png |
| Figure 2 | Data preprocessing flowchart | (to be created) |
| Figure 3 | Image dimension scores | image_dimension_scores.png |
| Figure 4 | TOPSIS ranking | image_ranking.png |
| Figure 5 | Weight comparison | weight_comparison.png |
| Figure 6 | TOPSIS vs GRA consistency | gray_topsis_consistency.png |
| Figure 7 | Sensitivity tornado | sensitivity_tornado.png |
| Figure 8 | Video instability curve | video_instability_curve.png |
| Figure 9 | Anomaly frames panel | anomaly_frames_panel.png |
| Figure 10 | Parameter priority heatmap | parameter_priority_heatmap.png |

---

## Table List

| Table | Description | Source |
|-------|-------------|--------|
| Table 1 | Image metrics summary | results/final/image_metrics.csv |
| Table 2 | Vision labels structure | results/intermediate/vision_labels.csv |
| Table 3 | Dimension definitions | Paper text |
| Table 4 | AHP judgment matrix | results/final/image_weights.csv |
| Table 5 | Entropy weights | results/final/image_weights.csv |
| Table 6 | TOPSIS results | results/final/image_topsis_scores.csv |
| Table 7 | Rank stability | results/final/rank_stability.csv |
| Table 8 | Video metrics summary | results/final/video_summary.csv |
| Table 9 | Anomaly frames | results/final/video_anomaly_frames.csv |
| Table 10 | Parameter suggestions | results/final/parameter_optimization_suggestions.csv |

---

*Created: 2026-06-05*
