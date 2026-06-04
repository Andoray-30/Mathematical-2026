"""Extract video frames and create contact sheet."""
import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

def extract_frames(video_path, output_dir, fps_interval=1):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return []
    
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / video_fps if video_fps > 0 else 0
    
    print(f"Video: {Path(video_path).name}")
    print(f"FPS: {video_fps}, Frames: {frame_count}, Duration: {duration:.2f}s")
    
    if duration <= 30:
        frame_interval = 1
    else:
        frame_interval = int(video_fps)
    
    frames = []
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_idx % frame_interval == 0:
            timestamp = frame_idx / video_fps
            frame_path = output_dir / f"frame_{frame_idx:06d}_{timestamp:.2f}s.png"
            cv2.imwrite(str(frame_path), frame)
            frames.append({
                'frame_idx': frame_idx,
                'timestamp': round(timestamp, 2),
                'path': str(frame_path)
            })
        
        frame_idx += 1
    
    cap.release()
    print(f"Extracted {len(frames)} frames")
    return frames

def create_contact_sheet(frames, output_path, cols=4, thumb_size=(320, 240)):
    if not frames:
        return
    
    if len(frames) > 16:
        indices = np.linspace(0, len(frames) - 1, 16, dtype=int)
        selected_frames = [frames[i] for i in indices]
    else:
        selected_frames = frames
    
    rows = (len(selected_frames) + cols - 1) // cols
    
    canvas_width = cols * thumb_size[0]
    canvas_height = rows * thumb_size[1]
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    
    for idx, frame_info in enumerate(selected_frames):
        row = idx // cols
        col = idx % cols
        
        img = Image.open(frame_info['path'])
        img = img.resize(thumb_size, Image.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        timestamp = frame_info['timestamp']
        draw.text((10, 10), f"t={timestamp:.1f}s", fill='red')
        
        x = col * thumb_size[0]
        y = row * thumb_size[1]
        canvas.paste(img, (x, y))
    
    canvas.save(str(output_path))
    print(f"Contact sheet saved to: {output_path}")

def main():
    import csv
    
    b_problem_dir = Path("B题：AI生成内容的质量评估与参数优化/附件2")
    if not b_problem_dir.exists():
        print(f"Directory not found: {b_problem_dir}")
        return
    
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    videos = []
    for ext in video_extensions:
        videos.extend(b_problem_dir.glob(ext))
    
    if not videos:
        print("No videos found")
        return
    
    for video_path in videos:
        print(f"\nProcessing: {video_path.name}")
        
        frames_dir = Path("figures/video_frames")
        frames = extract_frames(video_path, frames_dir)
        
        contact_sheet_path = Path("figures/video_contact_sheet.png")
        create_contact_sheet(frames, contact_sheet_path)

if __name__ == "__main__":
    main()
