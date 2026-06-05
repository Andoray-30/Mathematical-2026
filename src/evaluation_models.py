"""
Phase 3: Comprehensive evaluation model with 3-dimension AHP/Entropy/TOPSIS.

This script implements the evaluation model on the three dimension scores:
- S_sem: Semantic consistency
- S_tech: Technical quality  
- S_str: Structural integrity

AHP is applied to the 3x3 dimension matrix (not 10+ indicators).
Entropy weight is calculated on the 3-dimension score matrix.
Combined weight: w = eta * w_AHP + (1-eta) * w_entropy

Input: results/final/image_dimension_scores.csv
Output: 
- results/final/image_weights.csv
- results/final/image_topsis_scores.csv
"""
import os
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent

# File paths
DIMENSION_SCORES = ROOT / "results" / "final" / "image_dimension_scores.csv"
OUTPUT_DIR = ROOT / "results" / "final"
WEIGHTS_FILE = OUTPUT_DIR / "image_weights.csv"
TOPSIS_FILE = OUTPUT_DIR / "image_topsis_scores.csv"


def ahp_weights(matrix):
    """
    Calculate AHP weights from judgment matrix.
    
    Returns weights and consistency ratio CR.
    CR < 0.1 indicates acceptable consistency.
    """
    n = matrix.shape[0]
    
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_idx = np.argmax(eigenvalues.real)
    lambda_max = eigenvalues[max_idx].real
    
    w = eigenvectors[:, max_idx].real
    w = w / w.sum()
    
    CI = (lambda_max - n) / (n - 1) if n > 1 else 0
    
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    ri = RI[n - 1] if n <= len(RI) else 1.49
    
    CR = CI / ri if ri > 0 else 0
    CR = max(CR, 0)  # Avoid negative floating point errors
    
    return w, CR


def entropy_weight(matrix):
    """
    Calculate entropy weight from decision matrix.
    
    matrix: (n_samples, n_indicators)
    Returns weights for each indicator.
    """
    col_sums = matrix.sum(axis=0)
    col_sums[col_sums == 0] = 1e-8
    P = matrix / col_sums
    
    n = matrix.shape[0]
    k = 1.0 / np.log(n) if n > 1 else 1.0
    
    P_log = np.where(P > 0, P * np.log(P + 1e-10), 0)
    e = -k * P_log.sum(axis=0)
    
    d = 1 - e
    
    d_sum = d.sum()
    if d_sum == 0:
        return np.ones(matrix.shape[1]) / matrix.shape[1]
    w = d / d_sum
    
    return w


def topsis(matrix, weights):
    """
    Perform TOPSIS ranking.
    
    matrix: (n_samples, n_indicators)
    weights: (n_indicators,)
    
    Returns closeness scores and ranks.
    """
    col_norms = np.sqrt((matrix ** 2).sum(axis=0))
    col_norms[col_norms == 0] = 1e-8
    R = matrix / col_norms
    
    V = R * weights
    
    A_plus = V.max(axis=0)
    A_minus = V.min(axis=0)
    
    D_plus = np.sqrt(((V - A_plus) ** 2).sum(axis=1))
    D_minus = np.sqrt(((V - A_minus) ** 2).sum(axis=1))
    
    D_sum = D_plus + D_minus
    D_sum[D_sum == 0] = 1e-8
    C = D_minus / D_sum
    
    ranks = np.argsort(np.argsort(-C)) + 1
    
    return C, ranks


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 3: Evaluation Models (AHP/Entropy/TOPSIS)")
    print("=" * 60)
    
    print(f"Loading dimension scores from {DIMENSION_SCORES}...")
    df = pd.read_csv(DIMENSION_SCORES)
    print(f"  Loaded {len(df)} images")
    
    D = df[['S_sem', 'S_tech', 'S_str']].values
    filenames = df['filename'].values
    
    A = np.array([
        [1, 1/2, 1],
        [2, 1, 2],
        [1, 1/2, 1]
    ])
    
    print("\nAHP Judgment Matrix:")
    print(f"  Semantic  Technical  Structural")
    for i, row in enumerate(A):
        print(f"  {row[0]:>8.2f}  {row[1]:>9.2f}  {row[2]:>10.2f}")
    
    w_ahp, CR = ahp_weights(A)
    print(f"\nAHP Weights:")
    print(f"  Semantic:  {w_ahp[0]:.4f}")
    print(f"  Technical: {w_ahp[1]:.4f}")
    print(f"  Structural: {w_ahp[2]:.4f}")
    print(f"  Consistency Ratio (CR): {CR:.4f}")
    
    if CR >= 0.1:
        print("  WARNING: CR >= 0.1, AHP judgment matrix may be inconsistent!")
    else:
        print("  [OK] CR < 0.1, AHP judgment matrix is consistent")
    
    w_entropy = entropy_weight(D)
    print(f"\nEntropy Weights:")
    print(f"  Semantic:  {w_entropy[0]:.4f}")
    print(f"  Technical: {w_entropy[1]:.4f}")
    print(f"  Structural: {w_entropy[2]:.4f}")
    
    eta = 0.6
    w_combined = eta * w_ahp + (1 - eta) * w_entropy
    print(f"\nCombined Weights (eta={eta}):")
    print(f"  Semantic:  {w_combined[0]:.4f}")
    print(f"  Technical: {w_combined[1]:.4f}")
    print(f"  Structural: {w_combined[2]:.4f}")
    
    weights_df = pd.DataFrame({
        'dimension': ['semantic', 'technical', 'structural'],
        'w_ahp': w_ahp,
        'w_entropy': w_entropy,
        'w_combined': w_combined,
        'eta': [eta] * 3,
        'ahp_CR': [CR] * 3
    })
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    weights_df.to_csv(WEIGHTS_FILE, index=False)
    print(f"\nSaved weights to {WEIGHTS_FILE}")
    
    print("\nPerforming TOPSIS ranking...")
    C, ranks = topsis(D, w_combined)
    
    assert len(np.unique(ranks)) == len(ranks), "ERROR: Duplicate ranks found!"
    assert ranks[np.argmax(C)] == 1, "ERROR: Max closeness should have rank 1!"
    assert not np.any(np.isnan(C)), "ERROR: NaN values in closeness scores!"
    
    results_df = pd.DataFrame({
        'filename': filenames,
        'S_sem': df['S_sem'],
        'S_tech': df['S_tech'],
        'S_str': df['S_str'],
        'closeness': np.round(C, 4),
        'rank': ranks
    })
    
    results_df = results_df.sort_values('rank').reset_index(drop=True)
    
    def get_quality_level(c):
        if c >= 0.8:
            return '优秀'
        elif c >= 0.6:
            return '良好'
        elif c >= 0.4:
            return '一般'
        else:
            return '较差'
    
    results_df['quality_level'] = results_df['closeness'].apply(get_quality_level)
    
    results_df.to_csv(TOPSIS_FILE, index=False)
    print(f"Saved TOPSIS scores to {TOPSIS_FILE}")
    
    print("\n" + "=" * 60)
    print("TOPSIS Ranking Results:")
    print("=" * 60)
    print(f"{'Rank':<6} {'Filename':<12} {'S_sem':>8} {'S_tech':>8} {'S_str':>8} {'Closeness':>10} {'Quality'}")
    print("-" * 60)
    for _, row in results_df.iterrows():
        print(f"{row['rank']:<6} {row['filename']:<12} {row['S_sem']:>8.2f} {row['S_tech']:>8.2f} {row['S_str']:>8.2f} {row['closeness']:>10.4f} {row['quality_level']}")
    
    print("\nVerification:")
    print(f"  Total images: {len(results_df)}")
    print(f"  Rank range: [{results_df['rank'].min()}, {results_df['rank'].max()}]")
    print(f"  Closeness range: [{results_df['closeness'].min():.4f}, {results_df['closeness'].max():.4f}]")
    print(f"  No duplicate ranks: {len(results_df['rank'].unique()) == len(results_df)}")
    print(f"  Max closeness rank = 1: {results_df.loc[results_df['closeness'].idxmax(), 'rank'] == 1}")
    print(f"  No NaN values: {not results_df.isnull().any().any()}")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
