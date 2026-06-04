"""Calculate video temporal metrics."""
import cv2
import numpy as np
import csv
from pathlib import Path
from skimage.metrics import structural_similarity as ssim

def calculate_frame_diff(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    return np.mean(diff)

def calculate_brightness_delta(frame1, frame2):
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    return abs(np.mean(hsv2[:, :, 2]) - np.mean(hsv1[:, :, 2]))

def calculate_saturation_delta(frame1, frame2):
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    return abs(np.mean(hsv2[:, :, 1]) - np.mean(hsv1[:, :, 1]))

def calculate_optical_flow(frame1, frame2):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    return {
        'magnitude_mean': np.mean(magnitude),
        'angle_std': np.std(angle)
    }

def calculate_ssim_score(frame1, frame2):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    if gray1.shape != gray2.shape:
        gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))
    score, _ = ssim(gray1, gray2, full=True)
    return score

def process_video_frames(video_path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    metrics_list = []
    prev_frame = None
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        timestamp = frame_idx / fps
        
        if prev_frame is not None:
            frame_diff = calculate_frame_diff(prev_frame, frame)
            brightness_delta = calculate_brightness_delta(prev_frame, frame)
            saturation_delta = calculate_saturation_delta(prev_frame, frame)
            flow = calculate_optical_flow(prev_frame, frame)
            ssim_score = calculate_ssim_score(prev_frame, frame)
            
            instability = (
                0.4 * (1 - ssim_score) +
                0.3 * min(frame_diff / 50, 1) +
                0.3 * min(brightness_delta / 50, 1)
            )
            
            metrics = {
                'frame_index': frame_idx,
                'timestamp': round(timestamp, 2),
                'ssim_prev': round(ssim_score, 4),
                'frame_diff_mean': round(frame_diff, 4),
                'brightness_delta': round(brightness_delta, 4),
                'saturation_delta': round(saturation_delta, 4),
                'optical_flow_magnitude_mean': round(flow['magnitude_mean'], 4),
                'optical_flow_angle_change': round(flow['angle_std'], 4),
                'instability_score': round(instability, 4)
            }
            metrics_list.append(metrics)
        
        prev_frame = frame.copy()
        frame_idx += 1
        
        if frame_idx % 100 == 0:
            print(f"Processed {frame_idx}/{frame_count} frames")
    
    cap.release()
    return metrics_list

def detect_anomalies(metrics_list, threshold_std=2):
    if not metrics_list:
        return []
    
    scores = [m['instability_score'] for m in metrics_list]
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    threshold = mean_score + threshold_std * std_score
    
    anomalies = []
    for m in metrics_list:
        is_anomaly = m['instability_score'] > threshold
        m['is_anomaly'] = is_anomaly
        if is_anomaly:
            anomalies.append(m)
    
    return anomalies

def main():
    b_problem_dir = Path("B题：AI生成内容的质量评估与参数优化/附件2")
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    videos = []
    for ext in video_extensions:
        videos.extend(b_problem_dir.glob(ext))
    
    if not videos:
        print("No videos found")
        return
    
    video_path = videos[0]
    print(f"Processing: {video_path.name}")
    
    metrics_list = process_video_frames(video_path)
    if not metrics_list:
        print("No metrics calculated")
        return
    
    anomalies = detect_anomalies(metrics_list)
    print(f"Detected {len(anomalies)} anomalous frames")
    
    output_path = Path("results/video_metrics.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=metrics_list[0].keys())
        writer.writeheader()
        writer.writerows(metrics_list)
    print(f"Metrics saved to: {output_path}")
    
    if anomalies:
        anomaly_path = Path("results/video_anomaly_frames.csv")
        with open(anomaly_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=anomalies[0].keys())
            writer.writeheader()
            writer.writerows(anomalies)
        print(f"Anomalies saved to: {anomaly_path}")

if __name__ == "__main__":
    main()
