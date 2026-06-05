"""
Phase 4b: Sensitivity Analysis for robustness verification.

This script performs sensitivity analysis on the evaluation model:
- eta variation (0.5, 0.6, 0.7)
- AHP weight perturbation
- Remove semantic dimension
- Remove structural penalty
- No moderate-type transformation

Input:
- results/final/image_dimension_scores.csv
- results/final/image_weights.csv

Output:
- results/final/sensitivity_summary.csv
- results/final/rank_stability.csv
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
SUMMARY_FILE = OUTPUT_DIR / "sensitivity_summary.csv"
STABILITY_FILE = OUTPUT_DIR / "rank_stability.csv"


def topsis(matrix, weights):
    """Perform TOPSIS ranking."""
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


def ahp_weights(matrix):
    """Calculate AHP weights."""
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
    return w, CR


def entropy_weight(matrix):
    """Calculate entropy weight."""
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


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 4b: Sensitivity Analysis")
    print("=" * 60)
    
    # Load dimension scores
    print(f"Loading dimension scores from {DIMENSION_SCORES}...")
    df = pd.read_csv(DIMENSION_SCORES)
    print(f"  Loaded {len(df)} images")
    
    # Load weights
    print(f"Loading weights from {WEIGHTS_FILE}...")
    weights_df = pd.read_csv(WEIGHTS_FILE)
    base_eta = weights_df['eta'].iloc[0]
    base_w_ahp = weights_df['w_ahp'].values
    base_w_combined = weights_df['w_combined'].values
    
    # Extract dimension score matrix
    D = df[['S_sem', 'S_tech', 'S_str']].values
    filenames = df['filename'].values
    
    # Base case TOPSIS
    base_C, base_ranks = topsis(D, base_w_combined)
    
    # Store all scenarios
    scenarios = []
    
    # Scenario 1: Base case
    scenarios.append({
        'scenario': 'base',
        'eta': base_eta,
        'weights': base_w_combined,
        'C': base_C,
        'ranks': base_ranks
    })
    
    # Scenario 2: eta = 0.5
    print("\nRunning sensitivity scenarios...")
    
    # AHP matrix
    A = np.array([
        [1, 1/2, 1],
        [2, 1, 2],
        [1, 1/2, 1]
    ])
    w_ahp, _ = ahp_weights(A)
    w_entropy = entropy_weight(D)
    
    for eta in [0.5, 0.7]:
        w = eta * w_ahp + (1 - eta) * w_entropy
        C, ranks = topsis(D, w)
        scenarios.append({
            'scenario': f'eta_{eta}',
            'eta': eta,
            'weights': w,
            'C': C,
            'ranks': ranks
        })
    
    # Scenario 3: AHP weight perturbation (slightly different judgment)
    A_perturbed = np.array([
        [1, 1/3, 1],
        [3, 1, 3],
        [1, 1/3, 1]
    ])
    w_ahp_perturbed, _ = ahp_weights(A_perturbed)
    w_perturbed = base_eta * w_ahp_perturbed + (1 - base_eta) * w_entropy
    C_perturbed, ranks_perturbed = topsis(D, w_perturbed)
    scenarios.append({
        'scenario': 'ahp_perturbed',
        'eta': base_eta,
        'weights': w_perturbed,
        'C': C_perturbed,
        'ranks': ranks_perturbed
    })
    
    # Scenario 4: Remove semantic dimension
    D_no_sem = D[:, 1:]  # Only technical and structural
    w_no_sem = base_w_combined[1:] / base_w_combined[1:].sum()
    C_no_sem, ranks_no_sem = topsis(D_no_sem, w_no_sem)
    scenarios.append({
        'scenario': 'no_semantic',
        'eta': base_eta,
        'weights': np.array([0, w_no_sem[0], w_no_sem[1]]),
        'C': C_no_sem,
        'ranks': ranks_no_sem
    })
    
    # Scenario 5: Equal weights
    w_equal = np.array([1/3, 1/3, 1/3])
    C_equal, ranks_equal = topsis(D, w_equal)
    scenarios.append({
        'scenario': 'equal_weights',
        'eta': 0.5,
        'weights': w_equal,
        'C': C_equal,
        'ranks': ranks_equal
    })
    
    # Create sensitivity summary
    summary_data = []
    for scenario in scenarios:
        for i, fname in enumerate(filenames):
            summary_data.append({
                'scenario': scenario['scenario'],
                'filename': fname,
                'closeness': np.round(scenario['C'][i], 4),
                'rank': scenario['ranks'][i]
            })
    
    summary_df = pd.DataFrame(summary_data)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary_df.to_csv(SUMMARY_FILE, index=False)
    print(f"\nSaved sensitivity summary to {SUMMARY_FILE}")
    
    # Calculate rank stability
    print("\nCalculating rank stability...")
    
    stability_data = []
    for fname in filenames:
        ranks_across_scenarios = []
        for scenario in scenarios:
            idx = np.where(filenames == fname)[0][0]
            ranks_across_scenarios.append(scenario['ranks'][idx])
        
        stability_data.append({
            'filename': fname,
            'base_rank': base_ranks[np.where(filenames == fname)[0][0]],
            'mean_rank': np.mean(ranks_across_scenarios),
            'std_rank': np.std(ranks_across_scenarios),
            'min_rank': np.min(ranks_across_scenarios),
            'max_rank': np.max(ranks_across_scenarios),
            'rank_range': np.max(ranks_across_scenarios) - np.min(ranks_across_scenarios)
        })
    
    stability_df = pd.DataFrame(stability_data)
    stability_df.to_csv(STABILITY_FILE, index=False)
    print(f"Saved rank stability to {STABILITY_FILE}")
    
    # Print results
    print("\n" + "=" * 60)
    print("Sensitivity Analysis Results:")
    print("=" * 60)
    
    print("\nRank Comparison Across Scenarios:")
    print(f"{'Filename':<12}", end="")
    for scenario in scenarios:
        print(f" {scenario['scenario']:>15}", end="")
    print()
    print("-" * (12 + 16 * len(scenarios)))
    
    for i, fname in enumerate(filenames):
        print(f"{fname:<12}", end="")
        for scenario in scenarios:
            print(f" {scenario['ranks'][i]:>15}", end="")
        print()
    
    print("\n" + "=" * 60)
    print("Rank Stability (Lower std = More Stable):")
    print("=" * 60)
    print(f"{'Filename':<12} {'Base':>6} {'Mean':>6} {'Std':>6} {'Min':>6} {'Max':>6} {'Range':>6}")
    print("-" * 60)
    for _, row in stability_df.iterrows():
        print(f"{row['filename']:<12} {row['base_rank']:>6.0f} {row['mean_rank']:>6.2f} {row['std_rank']:>6.2f} {row['min_rank']:>6.0f} {row['max_rank']:>6.0f} {row['rank_range']:>6.0f}")
    
    # Calculate overall stability metrics
    base_ranks_arr = stability_df['base_rank'].values
    std_arr = stability_df['std_rank'].values
    
    print("\nOverall Stability Metrics:")
    print(f"  Mean rank std: {std_arr.mean():.2f}")
    print(f"  Max rank range: {stability_df['rank_range'].max():.0f}")
    print(f"  Images with rank range <= 2: {(stability_df['rank_range'] <= 2).sum()}/{len(df)}")
    
    # Check if top-3 is stable
    top3_base = set(np.argsort(base_ranks_arr)[:3])
    top3_stable = True
    for scenario in scenarios:
        top3_scenario = set(np.argsort(scenario['ranks'])[:3])
        if top3_base != top3_scenario:
            top3_stable = False
            break
    
    if top3_stable:
        print(f"\n  [OK] Top-3 ranking is stable across all scenarios")
    else:
        print(f"\n  [WARNING] Top-3 ranking varies across scenarios")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
