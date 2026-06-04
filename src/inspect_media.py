"""Inspect media files (images and videos)."""
import cv2
import csv
from pathlib import Path
from PIL import Image

def inspect_image(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            channels = len(img.getbands())
        
        file_size = Path(image_path).stat().st_size
        
        return {
            'filename': Path(image_path).name,
            'path': str(image_path),
            'format': Path(image_path).suffix[1:].upper(),
            'width': width,
            'height': height,
            'channels': channels,
            'file_size_bytes': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2)
        }
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return None

def inspect_video(video_path):
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return None
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        cap.release()
        
        file_size = Path(video_path).stat().st_size
        
        return {
            'filename': Path(video_path).name,
            'path': str(video_path),
            'width': width,
            'height': height,
            'fps': round(fps, 2),
            'frame_count': frame_count,
            'duration_seconds': round(duration, 2),
            'file_size_bytes': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2)
        }
    except Exception as e:
        print(f"Error reading {video_path}: {e}")
        return None

def main():
    b_problem_dir = Path("B题：AI生成内容的质量评估与参数优化")
    
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']
    images = []
    for ext in image_extensions:
        images.extend(b_problem_dir.rglob(ext))
    
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    videos = []
    for ext in video_extensions:
        videos.extend(b_problem_dir.rglob(ext))
    
    print(f"Found {len(images)} images and {len(videos)} videos")
    
    image_data = []
    for img_path in sorted(images):
        print(f"Inspecting: {img_path.name}")
        data = inspect_image(img_path)
        if data:
            image_data.append(data)
    
    video_data = []
    for vid_path in videos:
        print(f"Inspecting: {vid_path.name}")
        data = inspect_video(vid_path)
        if data:
            video_data.append(data)
    
    output_path = Path("results/media_inventory.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    all_data = image_data + video_data
    if all_data:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
            writer.writeheader()
            writer.writerows(all_data)
        print(f"\nSaved to: {output_path}")

if __name__ == "__main__":
    main()
