"""
Phase 4a: Grey Relation Analysis for robustness verification.

This script performs Grey Relation Analysis (GRA) to verify TOPSIS ranking.
GRA is suitable for small sample scenarios with incomplete information.

Input: 
- results/final/image_dimension_scores.csv
- results/final/image_weights.csv

Output:
- results/final/gray_relation_scores.csv
- results/final/rank_consistency.csv
"""
import os
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).parent.parent

# File paths
DIMENSION_SCORES = ROOT / "results" / "final" / "image_dimension_scores.csv"
WEIGHTS_FILE = ROOT / "results" / "final" / "image_weights.csv"
OUTPUT_DIR = ROOT / "results" / "final"
GRA_SCORES_FILE = OUTPUT_DIR / "gray_relation_scores.csv"
CONSISTENCY_FILE = OUTPUT_DIR / "rank_consistency.csv"


def gray_relation_coefficient(matrix, ideal, rho=0.5):
    """
    Calculate grey relation coefficient for each element.
    
    matrix: (n_samples, n_indicators)
    ideal: (n_indicators,) - ideal solution
    rho: distinguishing coefficient (default 0.5)
    """
    # Calculate absolute differences
    delta = np.abs(matrix - ideal)
    
    # Find min and max differences
    delta_min = delta.min()
    delta_max = delta.max()
    
    # Avoid division by zero
    if delta_max == 0:
        return np.ones_like(delta)
    
    # Grey relation coefficient
    xi = (delta_min + rho * delta_max) / (delta + rho * delta_max)
    
    return xi


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 4a: Grey Relation Analysis")
    print("=" * 60)
    
    # Load dimension scores
    print(f"Loading dimension scores from {DIMENSION_SCORES}...")
    df = pd.read_csv(DIMENSION_SCORES)
    print(f"  Loaded {len(df)} images")
    
    # Load weights
    print(f"Loading weights from {WEIGHTS_FILE}...")
    weights_df = pd.read_csv(WEIGHTS_FILE)
    w = weights_df['w_combined'].values
    print(f"  Loaded weights: {w}")
    
    # Extract dimension score matrix
    D = df[['S_sem', 'S_tech', 'S_str']].values
    filenames = df['filename'].values
    
    # Ideal solution (max of each dimension)
    ideal = D.max(axis=0)
    print(f"\nIdeal solution: S_sem={ideal[0]:.2f}, S_tech={ideal[1]:.2f}, S_str={ideal[2]:.2f}")
    
    # Calculate grey relation coefficients
    print("\nCalculating grey relation coefficients...")
    xi = gray_relation_coefficient(D, ideal, rho=0.5)
    
    # Calculate grey relation degree (weighted sum of coefficients)
    GRG = (xi * w).sum(axis=1)
    
    # Rank by GRG (descending)
    gra_ranks = np.argsort(np.argsort(-GRG)) + 1
    
    # Load TOPSIS ranks for comparison
    topsis_file = OUTPUT_DIR / "image_topsis_scores.csv"
    if topsis_file.exists():
        topsis_df = pd.read_csv(topsis_file)
        topsis_ranks = topsis_df['rank'].values
    else:
        print("WARNING: TOPSIS scores not found. Run evaluation_models.py first.")
        topsis_ranks = np.arange(1, len(df) + 1)
    
    # Save GRA scores
    gra_df = pd.DataFrame({
        'filename': filenames,
        'xi_sem': np.round(xi[:, 0], 4),
        'xi_tech': np.round(xi[:, 1], 4),
        'xi_str': np.round(xi[:, 2], 4),
        'GRG': np.round(GRG, 4),
        'gra_rank': gra_ranks
    })
    gra_df = gra_df.sort_values('gra_rank').reset_index(drop=True)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    gra_df.to_csv(GRA_SCORES_FILE, index=False)
    print(f"\nSaved GRA scores to {GRA_SCORES_FILE}")
    
    # Calculate rank consistency
    print("\nCalculating rank consistency...")
    
    # Ensure we're comparing the same order
    # Create a mapping from filename to ranks
    topsis_rank_map = dict(zip(topsis_df['filename'], topsis_ranks))
    gra_rank_map = dict(zip(gra_df['filename'], gra_df['gra_rank']))
    
    # Align ranks by filename
    aligned_topsis = []
    aligned_gra = []
    for fname in filenames:
        aligned_topsis.append(topsis_rank_map.get(fname, 0))
        aligned_gra.append(gra_rank_map.get(fname, 0))
    
    aligned_topsis = np.array(aligned_topsis)
    aligned_gra = np.array(aligned_gra)
    
    # Spearman correlation
    spearman_corr, spearman_p = stats.spearmanr(aligned_topsis, aligned_gra)
    
    # Kendall tau
    kendall_tau, kendall_p = stats.kendalltau(aligned_topsis, aligned_gra)
    
    # Top-3 agreement
    top3_topsis = set(np.argsort(aligned_topsis)[:3])
    top3_gra = set(np.argsort(aligned_gra)[:3])
    top3_agreement = len(top3_topsis & top3_gra) / 3
    
    # Save consistency metrics
    consistency_df = pd.DataFrame({
        'metric': ['spearman_rho', 'spearman_p_value', 'kendall_tau', 'kendall_p_value', 
                   'top3_agreement', 'total_images'],
        'value': [spearman_corr, spearman_p, kendall_tau, kendall_p, 
                  top3_agreement, len(df)]
    })
    consistency_df.to_csv(CONSISTENCY_FILE, index=False)
    print(f"Saved rank consistency to {CONSISTENCY_FILE}")
    
    # Print results
    print("\n" + "=" * 60)
    print("Grey Relation Analysis Results:")
    print("=" * 60)
    print(f"{'Filename':<12} {'xi_sem':>8} {'xi_tech':>8} {'xi_str':>8} {'GRG':>8} {'GRA Rank':>10}")
    print("-" * 60)
    for _, row in gra_df.iterrows():
        print(f"{row['filename']:<12} {row['xi_sem']:>8.4f} {row['xi_tech']:>8.4f} {row['xi_str']:>8.4f} {row['GRG']:>8.4f} {row['gra_rank']:>10}")
    
    print("\n" + "=" * 60)
    print("Rank Consistency (TOPSIS vs GRA):")
    print("=" * 60)
    print(f"{'Filename':<12} {'TOPSIS Rank':>12} {'GRA Rank':>10} {'Diff':>6}")
    print("-" * 60)
    for i, fname in enumerate(filenames):
        diff = abs(aligned_topsis[i] - aligned_gra[i])
        print(f"{fname:<12} {aligned_topsis[i]:>12} {aligned_gra[i]:>10} {diff:>6}")
    
    print("\nConsistency Metrics:")
    print(f"  Spearman rho: {spearman_corr:.4f} (p={spearman_p:.4f})")
    print(f"  Kendall tau: {kendall_tau:.4f} (p={kendall_p:.4f})")
    print(f"  Top-3 agreement: {top3_agreement:.2%}")
    
    if spearman_corr > 0.8:
        print("\n  [OK] High rank consistency between TOPSIS and GRA")
    elif spearman_corr > 0.6:
        print("\n  [OK] Moderate rank consistency between TOPSIS and GRA")
    else:
        print("\n  [WARNING] Low rank consistency - review model assumptions")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
