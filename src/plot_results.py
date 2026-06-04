"""Generate plots for the paper."""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from pathlib import Path

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def plot_image_metrics_heatmap(df, output_dir):
    metric_columns = ['laplacian_var', 'tenengrad', 'brightness_mean', 'brightness_std',
                      'saturation_mean', 'saturation_std', 'entropy', 'edge_density']
    data = df[metric_columns].values
    data_norm = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0) + 1e-10)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(data_norm, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(len(metric_columns)))
    ax.set_xticklabels(metric_columns, rotation=45, ha='right')
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['filename'])
    plt.colorbar(im, ax=ax, label='Normalized Value')
    ax.set_title('Image Metrics Heatmap')
    plt.tight_layout()
    plt.savefig(output_dir / 'image_metrics_heatmap.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'image_metrics_heatmap.svg', bbox_inches='tight')
    plt.close()
    print("  image_metrics_heatmap")

def plot_image_scores_bar(df, output_dir):
    fig, ax = plt.subplots(figsize=(10, 6))
    sorted_df = df.sort_values('closeness', ascending=True)
    colors = ['#2ecc71' if l == '优秀' else '#3498db' if l == '良好' else '#f39c12' if l == '一般' else '#e74c3c' for l in sorted_df['quality_level']]
    ax.barh(range(len(sorted_df)), sorted_df['closeness'], color=colors)
    ax.set_yticks(range(len(sorted_df)))
    ax.set_yticklabels(sorted_df['filename'])
    ax.set_xlabel('Closeness Score')
    ax.set_title('Image Quality Ranking (TOPSIS)')
    plt.tight_layout()
    plt.savefig(output_dir / 'image_scores_bar.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'image_scores_bar.svg', bbox_inches='tight')
    plt.close()
    print("  image_scores_bar")

def plot_video_ssim(df, output_dir):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['timestamp'], df['ssim_prev'], color='#3498db', linewidth=1)
    ax.fill_between(df['timestamp'], df['ssim_prev'], alpha=0.3, color='#3498db')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('SSIM')
    ax.set_title('Video Frame SSIM Over Time')
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'video_ssim.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'video_ssim.svg', bbox_inches='tight')
    plt.close()
    print("  video_ssim")

def plot_video_frame_diff(df, output_dir):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['timestamp'], df['frame_diff_mean'], color='#2ecc71', linewidth=1)
    ax.fill_between(df['timestamp'], df['frame_diff_mean'], alpha=0.3, color='#2ecc71')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Mean Difference')
    ax.set_title('Video Frame Difference Over Time')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'video_frame_diff.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'video_frame_diff.svg', bbox_inches='tight')
    plt.close()
    print("  video_frame_diff")

def plot_anomaly_detection(df, output_dir):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['timestamp'], df['instability_score'], color='#9b59b6', linewidth=1, label='Instability Score')
    anomalies = df[df['is_anomaly'] == True]
    ax.scatter(anomalies['timestamp'], anomalies['instability_score'], color='red', s=100, zorder=5, label='Anomaly')
    mean_score = df['instability_score'].mean()
    std_score = df['instability_score'].std()
    threshold = mean_score + 2 * std_score
    ax.axhline(y=threshold, color='red', linestyle='--', alpha=0.5, label=f'Threshold')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Instability Score')
    ax.set_title('Video Anomaly Detection')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'anomaly_detection.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'anomaly_detection.svg', bbox_inches='tight')
    plt.close()
    print("  anomaly_detection")

def main():
    output_dir = Path("figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    results_dir = Path("results")
    
    print("Generating plots...")
    
    image_metrics_path = results_dir / "image_metrics.csv"
    if image_metrics_path.exists():
        df_metrics = pd.read_csv(image_metrics_path)
        plot_image_metrics_heatmap(df_metrics, output_dir)
    
    image_scores_path = results_dir / "image_scores.csv"
    if image_scores_path.exists():
        df_scores = pd.read_csv(image_scores_path)
        plot_image_scores_bar(df_scores, output_dir)
    
    video_metrics_path = results_dir / "video_metrics.csv"
    if video_metrics_path.exists():
        df_video = pd.read_csv(video_metrics_path)
        plot_video_ssim(df_video, output_dir)
        plot_video_frame_diff(df_video, output_dir)
        if 'is_anomaly' in df_video.columns:
            plot_anomaly_detection(df_video, output_dir)
    
    print(f"\nAll plots saved to: {output_dir}")

if __name__ == "__main__":
    main()
