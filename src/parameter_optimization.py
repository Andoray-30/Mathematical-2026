"""
Phase 6: Parameter optimization priority model.

This script implements the shortfall-to-parameter priority mapping:
- Calculate quality shortfalls for each dimension
- Apply parameter-dimension effect matrix
- Calculate priority scores for each parameter adjustment

Input:
- results/final/image_dimension_scores.csv
- results/final/video_summary.csv
- config/parameter_effect_matrix.csv

Output:
- results/final/parameter_optimization_suggestions.csv
- figures/final/parameter_priority_heatmap.png/svg
"""
import os
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent

# File paths
DIMENSION_SCORES = ROOT / "results" / "final" / "image_dimension_scores.csv"
VIDEO_SUMMARY = ROOT / "results" / "final" / "video_summary.csv"
EFFECT_MATRIX = ROOT / "config" / "parameter_effect_matrix.csv"
OUTPUT_DIR = ROOT / "results" / "final"
SUGGESTIONS_FILE = OUTPUT_DIR / "parameter_optimization_suggestions.csv"


def create_default_effect_matrix():
    """Create default parameter-dimension effect matrix."""
    # Parameters
    parameters = [
        'prompt_detail',
        'negative_prompt_strength',
        'cfg_scale',
        'sampling_steps',
        'resolution',
        'structure_control_strength',
        'local_inpainting',
        'temporal_consistency_control',
        'color_brightness_rescale',
        'frame_interpolation_or_smoothing'
    ]
    
    # Dimensions: semantic, technical, structural, temporal
    # Effect matrix: positive values indicate improvement potential
    # Negative values indicate potential side effects
    effects = {
        'prompt_detail': [0.8, 0.1, 0.2, 0.0],
        'negative_prompt_strength': [0.3, 0.2, 0.3, 0.0],
        'cfg_scale': [0.5, 0.3, 0.2, 0.0],
        'sampling_steps': [0.1, 0.7, 0.2, 0.0],
        'resolution': [0.1, 0.8, 0.3, 0.0],
        'structure_control_strength': [0.2, 0.2, 0.8, 0.0],
        'local_inpainting': [0.1, 0.3, 0.7, 0.0],
        'temporal_consistency_control': [0.0, 0.1, 0.1, 0.9],
        'color_brightness_rescale': [0.0, 0.5, 0.1, 0.2],
        'frame_interpolation_or_smoothing': [0.0, 0.2, 0.1, 0.7]
    }
    
    df = pd.DataFrame(effects, index=['semantic', 'technical', 'structural', 'temporal']).T
    df.index.name = 'parameter'
    df = df.reset_index()
    
    return df


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 6: Parameter Optimization Priority Model")
    print("=" * 60)
    
    # Load or create effect matrix
    if EFFECT_MATRIX.exists():
        print(f"Loading effect matrix from {EFFECT_MATRIX}...")
        effect_df = pd.read_csv(EFFECT_MATRIX)
    else:
        print("Creating default effect matrix...")
        effect_df = create_default_effect_matrix()
        os.makedirs(EFFECT_MATRIX.parent, exist_ok=True)
        effect_df.to_csv(EFFECT_MATRIX, index=False)
        print(f"  Saved to {EFFECT_MATRIX}")
    
    parameters = effect_df['parameter'].values
    dimensions = ['semantic', 'technical', 'structural', 'temporal']
    M = effect_df[dimensions].values
    
    print(f"\nEffect Matrix:")
    print(f"{'Parameter':<35} {'semantic':>10} {'technical':>10} {'structural':>10} {'temporal':>10}")
    print("-" * 75)
    for i, param in enumerate(parameters):
        print(f"{param:<35} {M[i, 0]:>10.2f} {M[i, 1]:>10.2f} {M[i, 2]:>10.2f} {M[i, 3]:>10.2f}")
    
    # Load dimension scores
    print(f"\nLoading dimension scores from {DIMENSION_SCORES}...")
    dim_df = pd.read_csv(DIMENSION_SCORES)
    print(f"  Loaded {len(dim_df)} images")
    
    # Load video summary
    video_temporal = 0.57  # Default if not available
    if VIDEO_SUMMARY.exists():
        print(f"Loading video summary from {VIDEO_SUMMARY}...")
        video_df = pd.read_csv(VIDEO_SUMMARY)
        video_temporal = video_df['S_temp'].values[0] / 100
        print(f"  Video temporal score: {video_temporal:.4f}")
    
    # Calculate shortfalls
    print("\nCalculating quality shortfalls...")
    
    # Thresholds (default 0.80)
    thresholds = {
        'semantic': 0.80,
        'technical': 0.80,
        'structural': 0.80,
        'temporal': 0.80
    }
    
    # Weights for each dimension
    weights = {
        'semantic': 0.25,
        'technical': 0.40,
        'structural': 0.25,
        'temporal': 0.10
    }
    
    # Calculate average dimension scores
    avg_scores = {
        'semantic': dim_df['S_sem'].mean() / 100,
        'technical': dim_df['S_tech'].mean() / 100,
        'structural': dim_df['S_str'].mean() / 100,
        'temporal': video_temporal
    }
    
    print(f"\nAverage Scores:")
    for dim, score in avg_scores.items():
        shortfall = max(0, thresholds[dim] - score)
        print(f"  {dim}: score={score:.4f}, threshold={thresholds[dim]:.2f}, shortfall={shortfall:.4f}")
    
    # Calculate priority for each parameter
    print("\nCalculating parameter priorities...")
    
    suggestions = []
    
    for i, param in enumerate(parameters):
        # Calculate shortfall-weighted priority
        priority = 0
        direction_sum = 0
        
        for j, dim in enumerate(dimensions):
            shortfall = max(0, thresholds[dim] - avg_scores[dim])
            weight = weights[dim]
            effect = M[i, j]
            
            priority += weight * shortfall * max(effect, 0)
            direction_sum += weight * shortfall * effect
        
        # Determine direction
        if direction_sum > 0.01:
            direction = 'increase'
        elif direction_sum < -0.01:
            direction = 'decrease'
        else:
            direction = 'neutral'
        
        # Determine affected dimensions
        affected = []
        for j, dim in enumerate(dimensions):
            if M[i, j] > 0.3:
                affected.append(dim)
        
        suggestions.append({
            'parameter': param,
            'priority_score': np.round(priority, 4),
            'direction': direction,
            'affected_dimensions': ', '.join(affected),
            'semantic_effect': M[i, 0],
            'technical_effect': M[i, 1],
            'structural_effect': M[i, 2],
            'temporal_effect': M[i, 3]
        })
    
    # Sort by priority (descending)
    suggestions_df = pd.DataFrame(suggestions)
    suggestions_df = suggestions_df.sort_values('priority_score', ascending=False).reset_index(drop=True)
    
    # Add rank
    suggestions_df['rank'] = range(1, len(suggestions_df) + 1)
    
    # Save suggestions
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    suggestions_df.to_csv(SUGGESTIONS_FILE, index=False)
    print(f"\nSaved parameter suggestions to {SUGGESTIONS_FILE}")
    
    # Print results
    print("\n" + "=" * 60)
    print("Parameter Optimization Priority Ranking:")
    print("=" * 60)
    print(f"{'Rank':<6} {'Parameter':<35} {'Priority':>10} {'Direction':>10} {'Affected Dimensions'}")
    print("-" * 80)
    for _, row in suggestions_df.iterrows():
        print(f"{row['rank']:<6} {row['parameter']:<35} {row['priority_score']:>10.4f} {row['direction']:>10} {row['affected_dimensions']}")
    
    print("\n" + "=" * 60)
    print("Recommendations Summary:")
    print("=" * 60)
    
    # Top 3 priorities
    top3 = suggestions_df.head(3)
    print("\nTop 3 Priority Adjustments:")
    for _, row in top3.iterrows():
        print(f"\n{row['rank']}. {row['parameter']}")
        print(f"   Priority: {row['priority_score']:.4f}")
        print(f"   Direction: {row['direction']}")
        print(f"   Affects: {row['affected_dimensions']}")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
