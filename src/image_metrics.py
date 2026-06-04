"""Calculate image quality metrics."""
import cv2
import numpy as np
import csv
from pathlib import Path
from skimage.measure import shannon_entropy

def calculate_laplacian_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def calculate_tenengrad(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    return np.mean(gx**2 + gy**2)

def calculate_brightness_saturation(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = hsv[:, :, 2]
    saturation = hsv[:, :, 1]
    return {
        'brightness_mean': np.mean(brightness),
        'brightness_std': np.std(brightness),
        'saturation_mean': np.mean(saturation),
        'saturation_std': np.std(saturation)
    }

def calculate_entropy(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return shannon_entropy(gray)

def calculate_edge_density(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return np.sum(edges > 0) / edges.size

def calculate_noise_estimate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return np.std(lap)

def calculate_structure_proxy(metrics):
    score = (
        0.3 * min(metrics['laplacian_var'] / 1000, 1) +
        0.3 * min(metrics['tenengrad'] / 10000, 1) +
        0.2 * (1 - min(metrics['noise_estimate'] / 100, 1)) +
        0.2 * min(metrics['edge_density'] * 10, 1)
    )
    return score

def process_image(image_path):
    image = cv2.imread(str(image_path))
    if image is None:
        return None
    
    height, width = image.shape[:2]
    aspect_ratio = width / height
    
    metrics = {
        'filename': Path(image_path).name,
        'path': str(image_path),
        'width': width,
        'height': height,
        'aspect_ratio': round(aspect_ratio, 4),
        'laplacian_var': round(calculate_laplacian_variance(image), 4),
        'tenengrad': round(calculate_tenengrad(image), 4),
        'entropy': round(calculate_entropy(image), 4),
        'edge_density': round(calculate_edge_density(image), 4),
        'noise_estimate': round(calculate_noise_estimate(image), 4)
    }
    
    bs = calculate_brightness_saturation(image)
    metrics.update({k: round(v, 4) for k, v in bs.items()})
    metrics['structure_proxy'] = round(calculate_structure_proxy(metrics), 4)
    
    return metrics

def main():
    b_problem_dir = Path("B题：AI生成内容的质量评估与参数优化/附件1")
    if not b_problem_dir.exists():
        print(f"Directory not found: {b_problem_dir}")
        return
    
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    images = []
    for ext in image_extensions:
        images.extend(b_problem_dir.glob(ext))
    
    if not images:
        print("No images found")
        return
    
    print(f"Processing {len(images)} images...")
    
    results = []
    for img_path in sorted(images):
        print(f"Processing: {img_path.name}")
        metrics = process_image(img_path)
        if metrics:
            results.append(metrics)
    
    output_path = Path("results/image_metrics.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nSaved to: {output_path}")

if __name__ == "__main__":
    main()
