"""
Phase 5: Video temporal instability model with warp-SSIM.

This script implements the enhanced video quality assessment:
- Farnebäck optical flow
- Warp previous frame using optical flow
- Calculate warp_ssim_loss = 1 - SSIM(current, warped_previous)
- Robust z-score for all temporal indicators
- Anomaly threshold: median + k * MAD

Input: B题附件2/车流视频.mp4
Output:
- results/final/video_metrics.csv
- results/final/video_anomaly_frames.csv
- results/final/video_summary.csv
"""
import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from skimage.metrics import structural_similarity as ssim

ROOT = Path(__file__).parent.parent

# File paths
VIDEO_FILE = ROOT / "B题：AI生成内容的质量评估与参数优化" / "附件2" / "车流视频.mp4"
OUTPUT_DIR = ROOT / "results" / "final"
METRICS_FILE = OUTPUT_DIR / "video_metrics.csv"
ANOMALY_FILE = OUTPUT_DIR / "video_anomaly_frames.csv"
SUMMARY_FILE = OUTPUT_DIR / "video_summary.csv"


def robust_zscore(x, k=1.4826):
    """
    Calculate robust z-score using median and MAD.
    z = max(0, (x - median(x)) / (k * MAD(x) + eps))
    """
    x = np.array(x, dtype=float)
    x_med = np.median(x)
    x_mad = np.median(np.abs(x - x_med))
    eps = 1e-8
    z = np.maximum(0, (x - x_med) / (k * x_mad + eps))
    return z


def warp_frame(frame, flow):
    """Warp frame using optical flow."""
    h, w = frame.shape[:2]
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = (x + flow[:, :, 0]).astype(np.float32)
    map_y = (y + flow[:, :, 1]).astype(np.float32)
    warped = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR, 
                       borderMode=cv2.BORDER_REFLECT)
    return warped


def calculate_optical_flow(prev_gray, curr_gray):
    """Calculate Farnebäck optical flow."""
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    return flow


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 5: Video Temporal Instability Model")
    print("=" * 60)
    
    if not VIDEO_FILE.exists():
        print(f"ERROR: Video file not found: {VIDEO_FILE}")
        return 1
    
    print(f"Loading video: {VIDEO_FILE}")
    cap = cv2.VideoCapture(str(VIDEO_FILE))
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps
    
    print(f"  FPS: {fps}")
    print(f"  Total frames: {total_frames}")
    print(f"  Resolution: {width}x{height}")
    print(f"  Duration: {duration:.2f}s")
    
    print("\nReading frames...")
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    
    print(f"  Read {len(frames)} frames")
    
    print("\nCalculating temporal metrics...")
    
    metrics_list = []
    
    for t in range(1, len(frames)):
        prev_frame = frames[t - 1]
        curr_frame = frames[t]
        
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        ssim_score = ssim(prev_gray, curr_gray)
        ssim_loss = 1 - ssim_score
        
        frame_diff = np.mean(np.abs(curr_frame.astype(float) - prev_frame.astype(float)))
        
        prev_hsv = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2HSV)
        curr_hsv = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2HSV)
        brightness_delta = abs(np.mean(curr_hsv[:, :, 2]) - np.mean(prev_hsv[:, :, 2]))
        saturation_delta = abs(np.mean(curr_hsv[:, :, 1]) - np.mean(prev_hsv[:, :, 1]))
        
        flow = calculate_optical_flow(prev_gray, curr_gray)
        
        magnitude = np.sqrt(flow[:, :, 0]**2 + flow[:, :, 1]**2)
        flow_mag_mean = np.mean(magnitude)
        
        angle = np.arctan2(flow[:, :, 1], flow[:, :, 0])
        flow_angle_std = np.std(angle)
        
        warped_prev = warp_frame(prev_frame, flow)
        warped_prev_gray = cv2.cvtColor(warped_prev, cv2.COLOR_BGR2GRAY)
        warp_ssim_score = ssim(curr_gray, warped_prev_gray)
        warp_ssim_loss = 1 - warp_ssim_score
        
        metrics_list.append({
            'frame_idx': t,
            'timestamp': t / fps,
            'ssim_loss': ssim_loss,
            'frame_diff_mean': frame_diff,
            'brightness_delta': brightness_delta,
            'saturation_delta': saturation_delta,
            'optical_flow_magnitude_mean': flow_mag_mean,
            'optical_flow_angle_change': flow_angle_std,
            'warp_ssim_loss': warp_ssim_loss
        })
    
    metrics_df = pd.DataFrame(metrics_list)
    
    print("Calculating robust z-scores...")
    
    zscore_cols = ['ssim_loss', 'frame_diff_mean', 'brightness_delta', 
                   'saturation_delta', 'optical_flow_magnitude_mean',
                   'optical_flow_angle_change', 'warp_ssim_loss']
    
    for col in zscore_cols:
        metrics_df[f'z_{col}'] = robust_zscore(metrics_df[col].values)
    
    weights = {
        'z_ssim_loss': 0.22,
        'z_frame_diff_mean': 0.18,
        'z_brightness_delta': 0.10,
        'z_saturation_delta': 0.08,
        'z_optical_flow_magnitude_mean': 0.14,
        'z_optical_flow_angle_change': 0.08,
        'z_warp_ssim_loss': 0.20
    }
    
    metrics_df['instability_score'] = sum(
        metrics_df[col] * weight for col, weight in weights.items()
    )
    
    k = 2.5
    instability = metrics_df['instability_score'].values
    median_val = np.median(instability)
    mad_val = np.median(np.abs(instability - median_val))
    threshold = median_val + k * mad_val
    
    metrics_df['is_anomaly'] = metrics_df['instability_score'] > threshold
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    metrics_df.to_csv(METRICS_FILE, index=False)
    print(f"\nSaved video metrics to {METRICS_FILE}")
    
    anomaly_df = metrics_df[metrics_df['is_anomaly']].copy()
    anomaly_df.to_csv(ANOMALY_FILE, index=False)
    print(f"Saved anomaly frames to {ANOMALY_FILE}")
    
    total_frames_analyzed = len(metrics_df)
    anomaly_count = len(anomaly_df)
    anomaly_ratio = anomaly_count / total_frames_analyzed
    
    S_temp = 100 * (1 - np.mean(np.minimum(metrics_df['instability_score'].values, 1.0))) - 10 * anomaly_ratio
    
    summary = {
        'total_frames': total_frames,
        'frames_analyzed': total_frames_analyzed,
        'fps': fps,
        'duration': duration,
        'anomaly_count': anomaly_count,
        'anomaly_ratio': anomaly_ratio,
        'threshold': threshold,
        'instability_mean': np.mean(instability),
        'instability_std': np.std(instability),
        'instability_median': median_val,
        'instability_mad': mad_val,
        'S_temp': S_temp,
        'ssim_loss_mean': metrics_df['ssim_loss'].mean(),
        'warp_ssim_loss_mean': metrics_df['warp_ssim_loss'].mean(),
        'warp_ssim_improvement': metrics_df['ssim_loss'].mean() - metrics_df['warp_ssim_loss'].mean()
    }
    
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(SUMMARY_FILE, index=False)
    print(f"Saved video summary to {SUMMARY_FILE}")
    
    print("\n" + "=" * 60)
    print("Video Temporal Instability Results:")
    print("=" * 60)
    print(f"Total frames analyzed: {total_frames_analyzed}")
    print(f"Anomaly threshold: {threshold:.4f}")
    print(f"Anomaly count: {anomaly_count}")
    print(f"Anomaly ratio: {anomaly_ratio:.2%}")
    print(f"Temporal quality score (S_temp): {S_temp:.2f}")
    
    print(f"\nWarp-SSIM Improvement:")
    print(f"  Mean SSIM loss: {metrics_df['ssim_loss'].mean():.4f}")
    print(f"  Mean warp-SSIM loss: {metrics_df['warp_ssim_loss'].mean():.4f}")
    print(f"  Improvement: {summary['warp_ssim_improvement']:.4f}")
    
    if len(anomaly_df) > 0:
        print(f"\nAnomaly Frames:")
        print(f"{'Frame':<8} {'Time':>8} {'Instability':>12} {'SSIM Loss':>10} {'Warp-SSIM':>10}")
        print("-" * 50)
        for _, row in anomaly_df.iterrows():
            print(f"{row['frame_idx']:<8} {row['timestamp']:>8.2f} {row['instability_score']:>12.4f} {row['ssim_loss']:>10.4f} {row['warp_ssim_loss']:>10.4f}")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
