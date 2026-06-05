"""
Phase 7b: Generate all final figures.

This script generates all required figures for the paper:
- framework_flowchart.png/svg
- image_dimension_scores.png/svg
- image_ranking.png/svg
- weight_comparison.png/svg
- gray_topsis_consistency.png/svg
- sensitivity_tornado.png/svg
- video_instability_curve.png/svg
- anomaly_frames_panel.png
- parameter_priority_heatmap.png/svg

Input: All CSV files in results/final/
Output: figures/final/*.png and *.svg
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ROOT = Path(__file__).parent.parent

RESULTS_DIR = ROOT / "results" / "final"
FIGURES_DIR = ROOT / "figures" / "final"


def plot_dimension_scores():
    """Plot image dimension scores bar chart."""
    df = pd.read_csv(RESULTS_DIR / "image_dimension_scores.csv")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(df))
    width = 0.25
    
    ax.bar(x - width, df['S_sem'], width, label='Semantic', alpha=0.8)
    ax.bar(x, df['S_tech'], width, label='Technical', alpha=0.8)
    ax.bar(x + width, df['S_str'], width, label='Structural', alpha=0.8)
    
    ax.set_xlabel('Image')
    ax.set_ylabel('Score')
    ax.set_title('Image Dimension Scores')
    ax.set_xticks(x)
    ax.set_xticklabels(df['filename'], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "image_dimension_scores.png", dpi=150, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "image_dimension_scores.svg", bbox_inches='tight')
    plt.close()
    print("  Saved image_dimension_scores.png/svg")


def plot_image_ranking():
    """Plot TOPSIS ranking bar chart."""
    df = pd.read_csv(RESULTS_DIR / "image_topsis_scores.csv")
    df = df.sort_values('rank')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#2ecc71' if q == '优秀' else '#3498db' if q == '良好' else '#f39c12' if q == '一般' else '#e74c3c' 
              for q in df['quality_level']]
    
    bars = ax.bar(df['filename'], df['closeness'], color=colors, alpha=0.8)
    
    ax.set_xlabel('Image')
    ax.set_ylabel('TOPSIS Closeness')
    ax.set_title('Image Quality Ranking (TOPSIS)')
    ax.set_ylim(0, 1.1)
    
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(i, row['closeness'] + 0.02, f"Rank {row['rank']}", ha='center', va='bottom')
    
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', alpha=0.8, label='Excellent'),
        Patch(facecolor='#3498db', alpha=0.8, label='Good'),
        Patch(facecolor='#f39c12', alpha=0.8, label='Average'),
        Patch(facecolor='#e74c3c', alpha=0.8, label='Poor')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "image_ranking.png", dpi=150, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "image_ranking.svg", bbox_inches='tight')
    plt.close()
    print("  Saved image_ranking.png/svg")


def plot_weight_comparison():
    """Plot AHP vs Entropy vs Combined weights."""
    df = pd.read_csv(RESULTS_DIR / "image_weights.csv")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = np.arange(len(df))
    width = 0.25
    
    ax.bar(x - width, df['w_ahp'], width, label='AHP', alpha=0.8)
    ax.bar(x, df['w_entropy'], width, label='Entropy', alpha=0.8)
    ax.bar(x + width, df['w_combined'], width, label='Combined', alpha=0.8)
    
    ax.set_xlabel('Dimension')
    ax.set_ylabel('Weight')
    ax.set_title('Weight Comparison (AHP vs Entropy vs Combined)')
    ax.set_xticks(x)
    ax.set_xticklabels(df['dimension'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "weight_comparison.png", dpi=150, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "weight_comparison.svg", bbox_inches='tight')
    plt.close()
    print("  Saved weight_comparison.png/svg")


def plot_gray_topsis_consistency():
    """Plot TOPSIS vs GRA rank comparison."""
    topsis_df = pd.read_csv(RESULTS_DIR / "image_topsis_scores.csv")
    gra_df = pd.read_csv(RESULTS_DIR / "gray_relation_scores.csv")
    
    merged = pd.merge(topsis_df[['filename', 'rank']], gra_df[['filename', 'gra_rank']], on='filename')
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.scatter(merged['rank'], merged['gra_rank'], s=100, alpha=0.6)
    
    for _, row in merged.iterrows():
        ax.annotate(row['filename'], (row['rank'], row['gra_rank']), 
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    ax.plot([0, 9], [0, 9], 'r--', alpha=0.5, label='Perfect agreement')
    
    ax.set_xlabel('TOPSIS Rank')
    ax.set_ylabel('GRA Rank')
    ax.set_title('TOPSIS vs Grey Relation Rank Comparison')
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "gray_topsis_consistency.png", dpi=150, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "gray_topsis_consistency.svg", bbox_inches='tight')
    plt.close()
    print("  Saved gray_topsis_consistency.png/svg")


def plot_sensitivity_tornado():
    """Plot sensitivity analysis tornado chart."""
    df = pd.read_csv(RESULTS_DIR / "rank_stability.csv")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    df = df.sort_values('rank_range', ascending=True)
    
    y_pos = np.arange(len(df))
    
    ax.barh(y_pos, df['rank_range'], alpha=0.8, color='#3498db')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['filename'])
    ax.set_xlabel('Rank Range Across Scenarios')
    ax.set_title('Sensitivity Analysis: Rank Stability')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "sensitivity_tornado.png", dpi=150, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "sensitivity_tornado.svg", bbox_inches='tight')
    plt.close()
    print("  Saved sensitivity_tornado.png/svg")


def plot_video_instability_curve():
    """Plot video instability score curve."""
    df = pd.read_csv(RESULTS_DIR / "video_metrics.csv")
    summary = pd.read_csv(RESULTS_DIR / "video_summary.csv")
    
    threshold = summary['threshold'].values[0]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df['timestamp'], df['instability_score'], 'b-', linewidth=1, label='Instability Score')
    ax.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold ({threshold:.2f})')
    
    anomalies = df[df['is_anomaly']]
    ax.scatter(anomalies['timestamp'], anomalies['instability_score'], 
              color='red', s=50, zorder=5, label='Anomaly Frames')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Instability Score')
    ax.set_title('Video Temporal Instability Score')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "video_instability_curve.png", dpi=150, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "video_instability_curve.svg", bbox_inches='tight')
    plt.close()
    print("  Saved video_instability_curve.png/svg")


def plot_anomaly_frames_panel():
    """Plot anomaly frames comparison panel."""
    df = pd.read_csv(RESULTS_DIR / "video_metrics.csv")
    anomalies = df[df['is_anomaly']].head(6)
    
    if len(anomalies) == 0:
        print("  No anomaly frames to plot")
        return
    
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()
    
    for i, (_, row) in enumerate(anomalies.iterrows()):
        if i >= 6:
            break
        ax = axes[i]
        
        metrics = ['ssim_loss', 'warp_ssim_loss']
        values = [row['ssim_loss'], row['warp_ssim_loss']]
        
        x = np.arange(len(metrics))
        ax.bar(x, values, alpha=0.8, color=['#3498db', '#e74c3c'])
        ax.set_xticks(x)
        ax.set_xticklabels(['SSIM', 'Warp-SSIM'])
        ax.set_ylabel('Loss')
        ax.set_title(f"Frame {row['frame_idx']} ({row['timestamp']:.2f}s)")
        ax.set_ylim(0, 0.4)
        ax.grid(True, alpha=0.3, axis='y')
    
    for i in range(len(anomalies), 6):
        axes[i].set_visible(False)
    
    plt.suptitle('Anomaly Frames: SSIM vs Warp-SSIM Loss', fontsize=14)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "anomaly_frames_panel.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved anomaly_frames_panel.png")


def plot_parameter_priority_heatmap():
    """Plot parameter optimization priority heatmap."""
    df = pd.read_csv(RESULTS_DIR / "parameter_optimization_suggestions.csv")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    params = df['parameter'].values
    dimensions = ['semantic_effect', 'technical_effect', 'structural_effect', 'temporal_effect']
    dim_labels = ['Semantic', 'Technical', 'Structural', 'Temporal']
    
    data = df[dimensions].values
    
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(np.arange(len(dim_labels)))
    ax.set_xticklabels(dim_labels)
    ax.set_yticks(np.arange(len(params)))
    ax.set_yticklabels(params)
    
    for i in range(len(params)):
        for j in range(len(dim_labels)):
            text = ax.text(j, i, f'{data[i, j]:.1f}',
                         ha="center", va="center", color="black", fontsize=9)
    
    ax.set_title('Parameter-Dimension Effect Matrix')
    fig.colorbar(im, ax=ax, label='Effect Strength')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "parameter_priority_heatmap.png", dpi=150, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / "parameter_priority_heatmap.svg", bbox_inches='tight')
    plt.close()
    print("  Saved parameter_priority_heatmap.png/svg")


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 7b: Generate Final Figures")
    print("=" * 60)
    
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    print("\nGenerating figures...")
    
    plot_dimension_scores()
    plot_image_ranking()
    plot_weight_comparison()
    plot_gray_topsis_consistency()
    plot_sensitivity_tornado()
    plot_video_instability_curve()
    plot_anomaly_frames_panel()
    plot_parameter_priority_heatmap()
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
