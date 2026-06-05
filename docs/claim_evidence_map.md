# Claim-Evidence Map

**Updated**: 2026-06-05
**Status**: Active

---

## Claim Registry

| Claim ID | Section | Claim Text | Evidence File | Figure/Table | Validation File | Status |
|----------|---------|------------|---------------|--------------|-----------------|--------|
| C1 | Problem 2 | 5.jpg has highest overall quality | results/final/image_topsis_scores.csv | Table 6, Figure 4 | results/final/gray_relation_scores.csv | Closed |
| C2 | Problem 2 | 7.jpg has higher technical quality than semantic/structural | results/final/image_dimension_scores.csv | Figure 3 | - | Closed |
| C3 | Problem 2 | Top-3 ranking is stable across all scenarios | results/final/rank_stability.csv | Figure 6 | results/final/sensitivity_summary.csv | Closed |
| C4 | Problem 3 | Video has anomaly frames at 50/53/62 | results/final/video_anomaly_frames.csv | Figure 8 | results/final/video_metrics.csv | Closed |
| C5 | Problem 3 | Video temporal quality score is 57.03 | results/final/video_summary.csv | Figure 7 | - | Closed |
| C6 | Parameter | Resolution increase is top priority for improvement | results/final/parameter_optimization_suggestions.csv | Table 9, Figure 9 | - | Closed |
| C7 | Model Eval | TOPSIS and GRA rankings are highly consistent (Spearman=0.976) | results/final/rank_consistency.csv | Figure 5 | - | Closed |
| C8 | Model Eval | AHP judgment matrix is consistent (CR<0.1) | results/final/image_weights.csv | Table 4 | - | Closed |
| C9 | Problem 1 | Semantic dimension uses structured labels | results/intermediate/vision_labels.csv | Table 2 | - | Closed |
| C10 | Problem 1 | Technical dimension uses moderate-type transform | results/final/image_dimension_scores.csv | - | src/dimension_scores.py | Closed |
| C11 | Problem 3 | Warp-SSIM separates natural motion from artifacts | results/final/video_metrics.csv | Figure 8 | - | Closed |
| C12 | Problem 1 | noise_estimate is diagnostic only, not in main score | src/dimension_scores.py | - | - | Closed |
| C13 | Problem 2 | 1.png semantic review high but TOPSIS rank 5 | docs/ranking_interpretation_notes.md | - | results/final/image_dimension_scores.csv | Closed |
| C14 | Problem 2 | 7.jpg multimodal review medium but TOPSIS rank 2 | docs/ranking_interpretation_notes.md | - | results/final/image_dimension_scores.csv | Closed |
| C15 | Problem 3 | 15 anomaly frames are candidate temporal fluctuations | docs/video_interpretation_notes.md | - | results/final/video_anomaly_frames.csv | Closed |
| C16 | Problem 3 | Warp-SSIM improvement is negative (not "improvement") | docs/video_interpretation_notes.md | - | results/final/video_metrics.csv | Closed |
| C17 | Problem 2 | Per-image shortfall diagnosis available | results/final/image_shortfall_diagnosis.csv | - | - | Closed |

---

## Evidence File Inventory

### results/final/

| File | Description | Used By |
|------|-------------|---------|
| image_metrics.csv | Raw image metrics (15 indicators) | C10 |
| image_dimension_scores.csv | Three-dimension scores (S_sem, S_tech, S_str) | C2, C10 |
| image_weights.csv | AHP/Entropy/Combined weights | C8 |
| image_topsis_scores.csv | TOPSIS ranking and closeness | C1 |
| gray_relation_scores.csv | Grey relation analysis scores | C1, C7 |
| rank_consistency.csv | Spearman/Kendall correlation | C7 |
| sensitivity_summary.csv | Sensitivity analysis results | C3 |
| rank_stability.csv | Rank stability across scenarios | C3 |
| video_metrics.csv | Video temporal metrics with warp-SSIM | C4, C11 |
| video_anomaly_frames.csv | Anomaly frames detected | C4 |
| video_summary.csv | Video quality summary | C5 |
| parameter_optimization_suggestions.csv | Parameter priority suggestions | C6 |
| results_final.xlsx | Consolidated Excel workbook | All |

### results/intermediate/

| File | Description | Used By |
|------|-------------|---------|
| vision_labels.csv | Structured multimodal labels | C9 |

### figures/final/

| File | Description | Used By |
|------|-------------|---------|
| image_dimension_scores.png | Dimension scores bar chart | C2 |
| image_ranking.png | TOPSIS ranking bar chart | C1 |
| weight_comparison.png | Weight comparison chart | C8 |
| gray_topsis_consistency.png | TOPSIS vs GRA scatter plot | C7 |
| sensitivity_tornado.png | Sensitivity tornado chart | C3 |
| video_instability_curve.png | Video instability curve | C4, C5 |
| anomaly_frames_panel.png | Anomaly frames comparison | C4, C11 |
| parameter_priority_heatmap.png | Parameter effect heatmap | C6 |

---

## Innovation Points Evidence

### Innovation 1: Equivalent Semantic Reference + Structured Labels

**Claim**: Semantic consistency is measured using structured labels from multimodal review, not raw prompt matching.

**Evidence**:
- results/intermediate/vision_labels.csv (21 columns, 8 images)
- src/vision_review_to_csv.py (parsing logic)
- docs/vision_review.md (source material)

**Status**: Implemented

### Innovation 2: Moderate-type Technical Indicator Monotonicity

**Claim**: Brightness/saturation indicators use median-MAD moderate-type transform.

**Evidence**:
- src/dimension_scores.py (moderate_transform function)
- results/final/image_dimension_scores.csv (transformed scores)

**Status**: Implemented

### Innovation 3: Optical Flow Compensated Warp-SSIM

**Claim**: Warp-SSIM separates natural motion from generation artifacts.

**Evidence**:
- src/video_metrics.py (warp_frame function)
- results/final/video_metrics.csv (warp_ssim_loss column)
- results/final/video_anomaly_frames.csv (anomaly detection)

**Status**: Implemented

### Innovation 4: Shortfall-to-Parameter Priority Model

**Claim**: Parameter optimization is based on quality shortfalls, not arbitrary suggestions.

**Evidence**:
- src/parameter_optimization.py (priority calculation)
- config/parameter_effect_matrix.csv (effect matrix)
- results/final/parameter_optimization_suggestions.csv (priorities)

**Status**: Implemented

---

*Updated: 2026-06-05*
