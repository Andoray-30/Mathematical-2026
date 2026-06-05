# Route 1.5 Enhancement Implementation Plan

**Created**: 2026-06-05
**Source**: Deep Research Report Analysis
**Status**: Active

---

## Executive Summary

Based on deep research analysis, Route1.5 is the correct framework but needs 4 key enhancements to reach competition-winning quality:

1. **Semantic**: Equivalent reference description + structured defect labels
2. **Technical**: Moderate-type monotonic transformation for brightness/saturation
3. **Video**: Warp-SSIM after optical flow compensation
4. **Parameter**: Shortfall-to-priority inverse mapping

---

## Phase 0: Documentation Consolidation ✅

- [x] Save deep research report as `docs/route15_deep_research_review.md`
- [x] Create `docs/route15_enhancement_implementation_plan.md` (this file)

---

## Phase 1: Structured Multimodal Labels

**Script**: `src/vision_review_to_csv.py`
**Input**: `docs/vision_review.md`, image filenames
**Output**: `results/intermediate/vision_labels.csv`

**Required Columns**:
- filename, subject_ok, attribute_ok, scene_ok, relation_ok, style_ok
- anatomy_error, relation_error, missing_subject
- hand_error, face_error, limb_error, boundary_error
- texture_artifact, text_artifact
- geometry_ok, occlusion_ok, perspective_ok
- semantic_notes, structure_notes, confidence

**Implementation**:
1. Parse vision_review.md to extract structured labels
2. If parsing fails, generate editable CSV template
3. Pre-fill with existing multimodal review content

---

## Phase 2: Image Dimension Score Reconstruction

**Script**: `src/dimension_scores.py`
**Input**: `results/final/image_metrics_final.csv`, `results/intermediate/vision_labels.csv`
**Output**: `results/final/image_dimension_scores.csv`

**Technical Quality S_tech**:
- Sharpness: laplacian_var, tenengrad, edge_density (positive)
- Naturalness: brightness_mean, brightness_std, saturation_mean, saturation_std (moderate-type via median-MAD)
- noise_estimate → diagnostic only, not in main score

**Semantic Consistency S_sem**:
- Based on subject_ok, attribute_ok, scene_ok, relation_ok, style_ok
- Penalty: anatomy_error, relation_error, missing_subject
- Fallback: structured labels (no CLIP/BLIP required)

**Structural Integrity S_str**:
- structure_proxy, edge_density
- part_integrity from hand_error, face_error, limb_error, boundary_error, texture_artifact, text_artifact
- geometry consistency from occlusion_ok, perspective_ok

**Output Columns**: filename, S_sem, S_tech, S_str, semantic_penalty, structural_penalty, diagnostic_noise, notes

---

## Phase 3: Comprehensive Evaluation Model Refactor

**Script**: `src/evaluation_models.py`
**Input**: `results/final/image_dimension_scores.csv`
**Output**: `results/final/image_weights.csv`, `results/final/image_topsis_scores.csv`

**Requirements**:
1. AHP only on 3x3 dimension matrix (not 10+ indicators)
2. Default AHP weights: semantic=0.25, technical=0.50, structural=0.25
3. Entropy weight on 3-dimension score matrix
4. Combined weight: w = eta * w_AHP + (1-eta) * w_entropy, eta=0.6
5. TOPSIS rank: closeness越大 rank越小
6. Assertions: rank 1 to n no duplicates, max closeness rank=1, no NaN

---

## Phase 4: Grey Relation & Sensitivity Analysis

**Scripts**: `src/gray_relation.py`, `src/sensitivity_analysis.py`

**gray_relation.py Output**:
- `results/final/gray_relation_scores.csv`
- `results/final/rank_consistency.csv`
- Spearman/Kendall correlation between TOPSIS and GRA

**sensitivity_analysis.py Output**:
- `results/final/sensitivity_summary.csv`
- `results/final/rank_stability.csv`

**Experiments**:
- eta = 0.5, 0.6, 0.7
- AHP weight perturbation
- Remove semantic dimension
- Remove structural penalty
- No moderate-type transformation
- Report rank changes and top-2/top-3 stability

---

## Phase 5: Video Temporal Instability Model Upgrade

**Script**: `src/video_metrics.py`
**Input**: `B题附件2/车流视频.mp4`
**Output**: 
- `results/final/video_metrics.csv`
- `results/final/video_anomaly_frames.csv`
- `results/final/video_summary.csv`
- `figures/final/video_instability_curve.png/svg`
- `figures/final/anomaly_frames_panel.png`

**New Features**:
1. Farnebäck optical flow
2. Warp previous frame to current using optical flow
3. warp_ssim_loss = 1 - SSIM(current, warped_previous)
4. Robust z-score for all temporal indicators
5. Anomaly threshold: median + k * MAD, default k=2.5
6. Output comparison of普通SSIM vs warp-SSIM anomalies

**Video Metrics Columns**:
frame_idx, timestamp, ssim_loss, frame_diff_mean, brightness_delta, saturation_delta, optical_flow_magnitude_mean, optical_flow_angle_change, warp_ssim_loss, instability_score, is_anomaly

---

## Phase 6: Parameter Optimization Priority Model

**Scripts**: 
- `config/parameter_effect_matrix.csv`
- `src/parameter_optimization.py`

**Output**:
- `results/final/parameter_optimization_suggestions.csv`
- `figures/final/parameter_priority_heatmap.png/svg`

**Parameters**:
- prompt_detail, negative_prompt_strength, cfg_scale, sampling_steps, resolution
- structure_control_strength, local_inpainting, temporal_consistency_control
- color_brightness_rescale, frame_interpolation_or_smoothing

**Dimensions**: semantic, technical, structural, temporal

**Formula**:
- shortfall = max(0, threshold - score)
- priority = sum(weight_j * shortfall_j * positive_effect_j)

---

## Phase 7: Unified Export & Visualization

**Scripts**: `src/export_excel.py`, `src/plot_results.py`

**Excel Output**: `results/final/results_final.xlsx`
- Sheets: Image Metrics, Vision Labels, Dimension Scores, Image Weights, TOPSIS Scores, Gray Relation, Sensitivity, Video Metrics, Video Summary, Video Anomalies, Parameter Suggestions

**Figure Output**: `figures/final/`
- framework_flowchart.png/svg
- image_dimension_scores.png/svg
- image_ranking.png/svg
- weight_comparison.png/svg
- gray_topsis_consistency.png/svg
- sensitivity_tornado.png/svg
- video_instability_curve.png/svg
- anomaly_frames_panel.png
- parameter_priority_heatmap.png/svg

---

## Phase 8: Evidence Loop & Writing Skeleton

**Update**:
- `docs/claim_evidence_map.md`
- `docs/next_action_checklist.md`
- `paper/outline.md`

**claim_evidence_map.md Columns**:
claim_id, paper_section, claim_text, evidence_file, figure_or_table, validation_file, status

**Requirement**: Every core conclusion must point to results/final/ or figures/final/. No archive/ references.

---

## Phase 9: Verification & Commit

**Run Full Pipeline**:
```
.venv\Scripts\python.exe src/image_metrics.py
.venv\Scripts\python.exe src/vision_review_to_csv.py
.venv\Scripts\python.exe src/dimension_scores.py
.venv\Scripts\python.exe src/evaluation_models.py
.venv\Scripts\python.exe src/gray_relation.py
.venv\Scripts\python.exe src/sensitivity_analysis.py
.venv\Scripts\python.exe src/video_metrics.py
.venv\Scripts\python.exe src/parameter_optimization.py
.venv\Scripts\python.exe src/export_excel.py
.venv\Scripts\python.exe src/plot_results.py
```

**Generate**: `docs/formal_results_generation_report.md`

**Git Commit**: `feat: Generate final Route1.5 modeling results`

---

## Innovation Points (Revised)

1. **Equivalent Semantic Reference + Structured Defect Labels**: Not "prompt matching" but "reference description consistency"
2. **Moderate-type Technical Indicator Monotonicity**: median-MAD transform for brightness/saturation
3. **Optical Flow Compensated Warp-SSIM**: Separate natural motion from generation artifacts
4. **Shortfall-to-Parameter Priority Model**: Inverse mapping from quality deficiencies to parameter adjustments

---

*Created: 2026-06-05*
