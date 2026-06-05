"""
Phase 2: Calculate image dimension scores with moderate-type transform.

This script implements the three-dimension scoring system:
- S_sem: Semantic consistency (from vision labels)
- S_tech: Technical quality (with moderate-type transform for brightness/saturation)
- S_str: Structural integrity (from metrics and vision labels)

Input: 
- results/final/image_metrics_final.csv (or image_metrics.csv)
- results/intermediate/vision_labels.csv

Output: results/final/image_dimension_scores.csv
"""
import os
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent

# File paths
METRICS_FILE = ROOT / "results" / "final" / "image_metrics_final.csv"
if not METRICS_FILE.exists():
    METRICS_FILE = ROOT / "results" / "image_metrics.csv"
VISION_LABELS = ROOT / "results" / "intermediate" / "vision_labels.csv"
OUTPUT_DIR = ROOT / "results" / "final"
OUTPUT_FILE = OUTPUT_DIR / "image_dimension_scores.csv"


def moderate_transform(x, c=2.5):
    """
    Median-MAD moderate-type transform.
    T(x) = max(0, 1 - |x - median(x)| / (c * MAD(x) + eps))
    """
    x = np.array(x, dtype=float)
    x_med = np.median(x)
    x_mad = np.median(np.abs(x - x_med))
    eps = 1e-8
    transformed = np.clip(1 - np.abs(x - x_med) / (c * x_mad + eps), 0, 1)
    return transformed


def normalize_positive(x):
    """Min-max normalization for positive indicators."""
    x = np.array(x, dtype=float)
    x_min, x_max = x.min(), x.max()
    if x_max - x_min < 1e-8:
        return np.ones_like(x) * 0.5
    return (x - x_min) / (x_max - x_min)


def log_normalize(x):
    """Log normalization for highly skewed indicators."""
    x = np.array(x, dtype=float)
    x_log = np.log1p(x)
    return normalize_positive(x_log)


def calculate_technical_score(metrics_df):
    """
    Calculate technical quality score S_tech.
    
    Sharpness: laplacian_var, tenengrad, edge_density (positive, log-normalized)
    Naturalness: brightness_mean, brightness_std, saturation_mean, saturation_std (moderate-type)
    noise_estimate: diagnostic only, not in main score
    """
    # Sharpness indicators (positive, log-normalized)
    sharpness_cols = ['laplacian_var', 'tenengrad', 'edge_density']
    sharpness_weights = [0.5, 0.4, 0.1]
    
    sharpness_scores = []
    for col in sharpness_cols:
        if col in metrics_df.columns:
            sharpness_scores.append(log_normalize(metrics_df[col].values))
        else:
            sharpness_scores.append(np.zeros(len(metrics_df)))
    
    sharpness = sum(w * s for w, s in zip(sharpness_weights, sharpness_scores))
    
    # Naturalness indicators (moderate-type transform)
    naturalness_cols = ['brightness_mean', 'brightness_std', 'saturation_mean', 'saturation_std']
    naturalness_weights = [0.4, 0.25, 0.2, 0.15]
    
    naturalness_scores = []
    for col in naturalness_cols:
        if col in metrics_df.columns:
            naturalness_scores.append(moderate_transform(metrics_df[col].values))
        else:
            naturalness_scores.append(np.zeros(len(metrics_df)))
    
    naturalness = sum(w * s for w, s in zip(naturalness_weights, naturalness_scores))
    
    # Combine: 65% sharpness + 35% naturalness
    S_tech = 100 * (0.65 * sharpness + 0.35 * naturalness)
    
    # Diagnostic noise (not in main score)
    diagnostic_noise = np.zeros(len(metrics_df))
    if 'noise_estimate' in metrics_df.columns:
        diagnostic_noise = metrics_df['noise_estimate'].values
    
    return S_tech, diagnostic_noise


def calculate_semantic_score(vision_labels_df):
    """
    Calculate semantic consistency score S_sem.
    
    Based on: subject_ok, attribute_ok, scene_ok, relation_ok, style_ok
    Penalty: anatomy_error, relation_error, missing_subject
    """
    # Positive semantic slots
    positive_cols = ['subject_ok', 'attribute_ok', 'scene_ok', 'relation_ok', 'style_ok']
    positive_weights = [0.3, 0.2, 0.2, 0.15, 0.15]
    
    positive_scores = []
    for col in positive_cols:
        if col in vision_labels_df.columns:
            positive_scores.append(vision_labels_df[col].values.astype(float))
        else:
            positive_scores.append(np.ones(len(vision_labels_df)))
    
    label_score = sum(w * s for w, s in zip(positive_weights, positive_scores))
    
    # Penalty terms
    penalty_cols = ['anatomy_error', 'relation_error', 'missing_subject']
    penalty_weights = [0.4, 0.3, 0.3]
    
    penalty_scores = []
    for col in penalty_cols:
        if col in vision_labels_df.columns:
            penalty_scores.append(vision_labels_df[col].values.astype(float))
        else:
            penalty_scores.append(np.zeros(len(vision_labels_df)))
    
    semantic_penalty = sum(w * p for w, p in zip(penalty_weights, penalty_scores))
    
    # S_sem = 100 * clip(label_score - 0.20 * penalty, 0, 1)
    S_sem = 100 * np.clip(label_score - 0.20 * semantic_penalty, 0, 1)
    
    return S_sem, semantic_penalty


def calculate_structural_score(metrics_df, vision_labels_df):
    """
    Calculate structural integrity score S_str.
    
    Global: structure_proxy, edge_density
    Local penalties: hand_error, face_error, limb_error, boundary_error, 
                     texture_artifact, text_artifact
    Geometry: occlusion_ok, perspective_ok
    """
    # Global structural indicators
    v1 = np.zeros(len(metrics_df))
    v2 = np.zeros(len(metrics_df))
    
    if 'structure_proxy' in metrics_df.columns:
        v1 = normalize_positive(metrics_df['structure_proxy'].values)
    if 'edge_density' in metrics_df.columns:
        v2 = normalize_positive(metrics_df['edge_density'].values)
    
    # Part integrity from vision labels
    part_error_cols = ['hand_error', 'face_error', 'limb_error', 'boundary_error', 
                       'texture_artifact', 'text_artifact']
    part_error_weights = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]
    
    part_errors = []
    for col in part_error_cols:
        if col in vision_labels_df.columns:
            part_errors.append(vision_labels_df[col].values.astype(float))
        else:
            part_errors.append(np.zeros(len(vision_labels_df)))
    
    structural_penalty = sum(w * e for w, e in zip(part_error_weights, part_errors))
    part_integrity = 1 - structural_penalty
    
    # Geometry consistency
    geometry_cols = ['occlusion_ok', 'perspective_ok']
    geometry_weights = [0.5, 0.5]
    
    geometry_scores = []
    for col in geometry_cols:
        if col in vision_labels_df.columns:
            geometry_scores.append(vision_labels_df[col].values.astype(float))
        else:
            geometry_scores.append(np.ones(len(vision_labels_df)))
    
    geometry = sum(w * s for w, s in zip(geometry_weights, geometry_scores))
    
    # S_str = 100 * clip(0.45*v1 + 0.15*v2 + 0.25*part_integrity + 0.15*geometry, 0, 1)
    S_str = 100 * np.clip(0.45 * v1 + 0.15 * v2 + 0.25 * part_integrity + 0.15 * geometry, 0, 1)
    
    return S_str, structural_penalty


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 2: Dimension Scores Calculator")
    print("=" * 60)
    
    # Load data
    print(f"Loading metrics from {METRICS_FILE}...")
    metrics_df = pd.read_csv(METRICS_FILE)
    print(f"  Loaded {len(metrics_df)} images")
    
    print(f"Loading vision labels from {VISION_LABELS}...")
    vision_labels_df = pd.read_csv(VISION_LABELS)
    print(f"  Loaded {len(vision_labels_df)} labels")
    
    # Merge on filename
    if 'filename' in metrics_df.columns and 'filename' in vision_labels_df.columns:
        df = pd.merge(metrics_df, vision_labels_df, on='filename', how='left')
    else:
        # Assume same order
        df = metrics_df.copy()
        for col in vision_labels_df.columns:
            if col != 'filename':
                df[col] = vision_labels_df[col].values
    
    # Fill NaN in vision labels with defaults
    vision_label_cols = ['subject_ok', 'attribute_ok', 'scene_ok', 'relation_ok', 'style_ok',
                         'anatomy_error', 'relation_error', 'missing_subject',
                         'hand_error', 'face_error', 'limb_error', 'boundary_error',
                         'texture_artifact', 'text_artifact',
                         'geometry_ok', 'occlusion_ok', 'perspective_ok']
    for col in vision_label_cols:
        if col not in df.columns:
            df[col] = 0 if 'error' in col or 'artifact' in col else 1
        df[col] = df[col].fillna(0 if 'error' in col or 'artifact' in col else 1)
    
    # Calculate dimension scores
    print("\nCalculating dimension scores...")
    
    S_tech, diagnostic_noise = calculate_technical_score(df)
    S_sem, semantic_penalty = calculate_semantic_score(df)
    S_str, structural_penalty = calculate_structural_score(df, vision_labels_df)
    
    # Create output DataFrame
    output_df = pd.DataFrame({
        'filename': df['filename'],
        'S_sem': np.round(S_sem, 2),
        'S_tech': np.round(S_tech, 2),
        'S_str': np.round(S_str, 2),
        'semantic_penalty': np.round(semantic_penalty, 3),
        'structural_penalty': np.round(structural_penalty, 3),
        'diagnostic_noise': np.round(diagnostic_noise, 4),
        'notes': [''] * len(df)
    })
    
    # Add notes for images with issues
    for idx, row in output_df.iterrows():
        notes = []
        if row['semantic_penalty'] > 0.1:
            notes.append(f"semantic_penalty={row['semantic_penalty']:.2f}")
        if row['structural_penalty'] > 0.1:
            notes.append(f"structural_penalty={row['structural_penalty']:.2f}")
        output_df.at[idx, 'notes'] = '; '.join(notes)
    
    # Save output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved dimension scores to {OUTPUT_FILE}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"{'Filename':<12} {'S_sem':>8} {'S_tech':>8} {'S_str':>8} {'Notes'}")
    print("-" * 60)
    for _, row in output_df.iterrows():
        print(f"{row['filename']:<12} {row['S_sem']:>8.2f} {row['S_tech']:>8.2f} {row['S_str']:>8.2f} {row['notes']}")
    
    print("\nDimension Statistics:")
    print(f"  S_sem: mean={S_sem.mean():.2f}, std={S_sem.std():.2f}, range=[{S_sem.min():.2f}, {S_sem.max():.2f}]")
    print(f"  S_tech: mean={S_tech.mean():.2f}, std={S_tech.std():.2f}, range=[{S_tech.min():.2f}, {S_tech.max():.2f}]")
    print(f"  S_str: mean={S_str.mean():.2f}, std={S_str.std():.2f}, range=[{S_str.min():.2f}, {S_str.max():.2f}]")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
