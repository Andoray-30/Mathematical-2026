"""Evaluation models: AHP, Entropy, TOPSIS."""
import numpy as np
import pandas as pd
from pathlib import Path

def min_max_normalize(data, positive_indicators, negative_indicators):
    normalized = data.copy()
    for col in data.columns:
        if col in positive_indicators:
            min_val, max_val = data[col].min(), data[col].max()
            normalized[col] = (data[col] - min_val) / (max_val - min_val) if max_val > min_val else 0.5
        elif col in negative_indicators:
            min_val, max_val = data[col].min(), data[col].max()
            normalized[col] = (max_val - data[col]) / (max_val - min_val) if max_val > min_val else 0.5
    return normalized

def ahp_weights(judgment_matrix):
    n = judgment_matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eig(judgment_matrix)
    max_idx = np.argmax(eigenvalues.real)
    max_eigenvalue = eigenvalues[max_idx].real
    weights = eigenvectors[:, max_idx].real
    weights = weights / weights.sum()
    
    RI = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    CI = (max_eigenvalue - n) / (n - 1) if n > 1 else 0
    CR = CI / RI.get(n, 1.45) if n > 2 else 0
    
    return {'weights': weights, 'max_eigenvalue': max_eigenvalue, 'CI': CI, 'CR': CR, 'consistent': CR < 0.1}

def entropy_weights(data):
    data_norm = data / data.sum(axis=0)
    n = data.shape[0]
    k = 1 / np.log(n)
    entropy = np.zeros(data.shape[1])
    for j in range(data.shape[1]):
        for i in range(n):
            if data_norm[i, j] > 0:
                entropy[j] -= k * data_norm[i, j] * np.log(data_norm[i, j])
    d = 1 - entropy
    weights = d / d.sum()
    return {'weights': weights, 'entropy': entropy, 'diversity': d}

def combination_weights(ahp_w, entropy_w, method='multiplicative'):
    if method == 'multiplicative':
        product = ahp_w * entropy_w
        return product / product.sum()
    elif method == 'linear':
        return 0.5 * ahp_w + 0.5 * entropy_w

def topsis(data, weights, positive_indicators, negative_indicators, column_names=None):
    data_norm = data / np.sqrt((data**2).sum(axis=0))
    weighted = data_norm * weights
    
    ideal_best = np.zeros(data.shape[1])
    ideal_worst = np.zeros(data.shape[1])
    
    if column_names is None:
        column_names = [f"col_{i}" for i in range(data.shape[1])]
    
    for j, col in enumerate(column_names):
        if col in positive_indicators:
            ideal_best[j] = weighted[:, j].max()
            ideal_worst[j] = weighted[:, j].min()
        elif col in negative_indicators:
            ideal_best[j] = weighted[:, j].min()
            ideal_worst[j] = weighted[:, j].max()
    
    dist_best = np.sqrt(((weighted - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst)**2).sum(axis=1))
    closeness = dist_worst / (dist_best + dist_worst)
    
    order = np.argsort(-closeness)
    rank = np.empty_like(order)
    rank[order] = np.arange(1, len(closeness) + 1)
    
    return {'closeness': closeness, 'rank': rank}

def assign_quality_levels(closeness):
    levels = []
    for c in closeness:
        if c >= 0.8: levels.append('优秀')
        elif c >= 0.6: levels.append('良好')
        elif c >= 0.4: levels.append('一般')
        else: levels.append('较差')
    return levels

def main():
    image_metrics_path = Path("results/image_metrics.csv")
    if not image_metrics_path.exists():
        print(f"File not found: {image_metrics_path}")
        print("Please run image_metrics.py first")
        return
    
    df = pd.read_csv(image_metrics_path)
    
    metric_columns = [
        'laplacian_var', 'tenengrad', 'brightness_mean', 'brightness_std',
        'saturation_mean', 'saturation_std', 'entropy', 'edge_density',
        'noise_estimate', 'structure_proxy'
    ]
    
    positive_indicators = [
        'laplacian_var', 'tenengrad', 'brightness_std', 'saturation_mean',
        'saturation_std', 'entropy', 'edge_density', 'structure_proxy'
    ]
    negative_indicators = ['noise_estimate']
    
    data = df[metric_columns].values
    data_normalized = min_max_normalize(pd.DataFrame(data, columns=metric_columns), positive_indicators, negative_indicators)
    
    # Example AHP judgment matrix (10x10 for 10 metrics)
    judgment_matrix = np.ones((len(metric_columns), len(metric_columns)))
    # Set relative importance (example: laplacian_var is 2x more important than brightness_mean)
    judgment_matrix[0, 2] = 2; judgment_matrix[2, 0] = 1/2
    judgment_matrix[0, 3] = 2; judgment_matrix[3, 0] = 1/2
    judgment_matrix[1, 2] = 2; judgment_matrix[2, 1] = 1/2
    judgment_matrix[1, 3] = 2; judgment_matrix[3, 1] = 1/2
    
    ahp_result = ahp_weights(judgment_matrix)
    print(f"AHP CR: {ahp_result['CR']:.4f} ({'OK' if ahp_result['consistent'] else 'FAIL'})")
    
    entropy_result = entropy_weights(data)
    
    combo_weights = combination_weights(ahp_result['weights'], entropy_result['weights'])
    print(f"Combined weights: {combo_weights.round(4)}")
    
    topsis_result = topsis(data_normalized.values, combo_weights, positive_indicators, negative_indicators, metric_columns)
    quality_levels = assign_quality_levels(topsis_result['closeness'])
    
    results_df = pd.DataFrame({
        'filename': df['filename'],
        'closeness': topsis_result['closeness'].round(4),
        'rank': topsis_result['rank'],
        'quality_level': quality_levels
    })
    
    output_path = Path("results/image_scores.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nImage scores saved to: {output_path}")
    
    summary_path = Path("results/final_summary.csv")
    results_df.to_csv(summary_path, index=False, encoding='utf-8')
    print(f"Final summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
