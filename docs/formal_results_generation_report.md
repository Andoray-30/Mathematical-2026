# Formal Results Generation Report

**Generated**: 2026-06-05
**Route**: Route 1.5 (AHP-Entropy-TOPSIS + Lightweight Enhancements)

---

## Executive Summary

All phases of Route 1.5 enhancement have been completed successfully. The formal modeling pipeline is now fully operational with all required scripts, results, and figures generated.

---

## Implemented Scripts

| Script | Phase | Status | Description |
|--------|-------|--------|-------------|
| src/vision_review_to_csv.py | 1 | ✅ Complete | Converts multimodal review to structured labels |
| src/dimension_scores.py | 2 | ✅ Complete | Calculates three-dimension scores with moderate-type transform |
| src/evaluation_models.py | 3 | ✅ Complete | AHP/Entropy/TOPSIS on 3-dimension matrix |
| src/gray_relation.py | 4a | ✅ Complete | Grey relation analysis for robustness verification |
| src/sensitivity_analysis.py | 4b | ✅ Complete | Sensitivity analysis across scenarios |
| src/video_metrics.py | 5 | ✅ Complete | Video temporal instability with warp-SSIM |
| src/parameter_optimization.py | 6 | ✅ Complete | Parameter priority model based on shortfalls |
| src/export_excel.py | 7a | ✅ Complete | Consolidates all results into Excel workbook |
| src/plot_results.py | 7b | ✅ Complete | Generates all final figures |

---

## Output File Inventory

### results/final/

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| image_metrics.csv | 8 | 15 | Raw image metrics |
| image_dimension_scores.csv | 8 | 8 | Three-dimension scores |
| image_weights.csv | 3 | 6 | AHP/Entropy/Combined weights |
| image_topsis_scores.csv | 8 | 7 | TOPSIS ranking |
| gray_relation_scores.csv | 8 | 6 | Grey relation scores |
| rank_consistency.csv | 6 | 2 | Spearman/Kendall correlation |
| sensitivity_summary.csv | 48 | 4 | Sensitivity analysis |
| rank_stability.csv | 8 | 7 | Rank stability |
| video_metrics.csv | 120 | 18 | Video temporal metrics |
| video_anomaly_frames.csv | 15 | 18 | Anomaly frames |
| video_summary.csv | 1 | 15 | Video quality summary |
| parameter_optimization_suggestions.csv | 10 | 9 | Parameter priorities |
| results_final.xlsx | - | - | Consolidated workbook |

### results/intermediate/

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| vision_labels.csv | 8 | 21 | Structured multimodal labels |

### figures/final/

| File | Description |
|------|-------------|
| image_dimension_scores.png/svg | Dimension scores bar chart |
| image_ranking.png/svg | TOPSIS ranking |
| weight_comparison.png/svg | Weight comparison |
| gray_topsis_consistency.png/svg | TOPSIS vs GRA scatter |
| sensitivity_tornado.png/svg | Sensitivity tornado |
| video_instability_curve.png/svg | Video instability curve |
| anomaly_frames_panel.png | Anomaly frames comparison |
| parameter_priority_heatmap.png/svg | Parameter effect heatmap |

---

## Key Results

### Image Quality Ranking

| Rank | Filename | Closeness | Quality Level |
|------|----------|-----------|---------------|
| 1 | 5.jpg | 0.9867 | Excellent |
| 2 | 7.jpg | 0.8392 | Excellent |
| 3 | 6.jpg | 0.7945 | Good |
| 4 | 8.jpg | 0.4977 | Average |
| 5 | 1.png | 0.4573 | Average |
| 6 | 2.png | 0.2434 | Poor |
| 7 | 3.png | 0.1745 | Poor |
| 8 | 4.png | 0.0289 | Poor |

### Video Analysis

- **Total frames analyzed**: 120
- **Anomaly frames detected**: 15 (12.5%)
- **Temporal quality score**: 57.03
- **Anomaly threshold**: 0.9718 (median + 2.5*MAD)

### Robustness Verification

- **TOPSIS vs GRA**: Spearman ρ = 0.9762 (high consistency)
- **Sensitivity**: Mean rank std = 0.09 (very stable)
- **Top-3 stability**: 100% across all scenarios

### Parameter Optimization Priorities

| Rank | Parameter | Priority | Direction |
|------|-----------|----------|-----------|
| 1 | resolution | 0.1126 | increase |
| 2 | sampling_steps | 0.0943 | increase |
| 3 | local_inpainting | 0.0819 | increase |
| 4 | structure_control_strength | 0.0772 | increase |
| 5 | color_brightness_rescale | 0.0690 | increase |

---

## Innovation Points Status

| Innovation | Status | Evidence |
|------------|--------|----------|
| Equivalent Semantic Reference + Structured Labels | ✅ Implemented | vision_labels.csv |
| Moderate-type Technical Indicator Monotonicity | ✅ Implemented | dimension_scores.py |
| Optical Flow Compensated Warp-SSIM | ✅ Implemented | video_metrics.py |
| Shortfall-to-Parameter Priority Model | ✅ Implemented | parameter_optimization.py |

---

## Verification Checklist

- [x] All scripts run without errors
- [x] All output files generated
- [x] TOPSIS ranking verified (no duplicates, max closeness = rank 1)
- [x] AHP CR < 0.1
- [x] Grey relation consistency verified
- [x] Sensitivity analysis completed
- [x] Video anomaly frames detected
- [x] Parameter priorities calculated
- [x] Excel workbook consolidated
- [x] All figures generated

---

## Pending Items

1. **Framework flowchart**: Need to create manually or with diagram tool
2. **Data preprocessing flowchart**: Need to create manually
3. **Paper writing**: Ready to begin after results verification

---

*Generated: 2026-06-05*
