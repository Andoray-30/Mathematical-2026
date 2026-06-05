"""
Phase 1: Convert vision_review.md to structured CSV labels.

This script parses the multimodal review document and generates structured
labels for each image, which will be used in dimension_scores.py.

Input: docs/vision_review.md
Output: results/intermediate/vision_labels.csv
"""
import os
import re
import csv
from pathlib import Path

# Project root
ROOT = Path(__file__).parent.parent

# File paths
VISION_REVIEW = ROOT / "docs" / "vision_review.md"
OUTPUT_DIR = ROOT / "results" / "intermediate"
OUTPUT_FILE = OUTPUT_DIR / "vision_labels.csv"

# Image files (8 images)
IMAGE_FILES = [
    "1.png", "2.png", "3.png", "4.png",
    "5.jpg", "6.jpg", "7.jpg", "8.jpg"
]

# Quality level mapping
QUALITY_MAP = {
    "高": 1.0,
    "中": 0.6,
    "低": 0.3
}

# Severity mapping
SEVERITY_MAP = {
    "轻微": 0.2,
    "中等": 0.5,
    "严重": 0.8,
    "无": 0.0
}


def parse_vision_review(filepath):
    """Parse vision_review.md and extract structured information for each image."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by image sections - use the actual format from vision_review.md
    # Format: ### 2.X 图像 filename (description)
    image_sections = re.split(r'### 2\.\d+ 图像 \S+', content)
    
    results = []
    
    for i, section in enumerate(image_sections[1:], 0):  # Skip first section (before images)
        if i >= len(IMAGE_FILES):
            break
            
        filename = IMAGE_FILES[i]
        label = {
            'filename': filename,
            'subject_ok': 1,
            'attribute_ok': 1,
            'scene_ok': 1,
            'relation_ok': 1,
            'style_ok': 1,
            'anatomy_error': 0,
            'relation_error': 0,
            'missing_subject': 0,
            'hand_error': 0,
            'face_error': 0,
            'limb_error': 0,
            'boundary_error': 0,
            'texture_artifact': 0,
            'text_artifact': 0,
            'geometry_ok': 1,
            'occlusion_ok': 1,
            'perspective_ok': 1,
            'semantic_notes': '',
            'structure_notes': '',
            'confidence': 0.8
        }
        
        # Extract quality judgment
        quality_match = re.search(r'质量判断[：:]\s*\*\*(\S+)\*\*', section)
        if quality_match:
            quality = quality_match.group(1)
            label['quality_level'] = QUALITY_MAP.get(quality, 0.6)
        
        # Get full section text for analysis
        section_lower = section.lower()
        
        # Check for hand errors - look for hand-related issues
        if re.search(r'手[部指].*?(不清晰|结构|边界|可疑|不够准确|形态)', section_lower):
            label['hand_error'] = 1
            label['anatomy_error'] = 1
        
        # Check for face errors
        if re.search(r'面部|五官', section_lower):
            label['face_error'] = 1
        
        # Check for boundary errors
        if re.search(r'边界.*?(融合|不够明确|不清)|融合.*?边界', section_lower):
            label['boundary_error'] = 1
        
        # Check for texture artifacts
        if re.search(r'纹理.*?(粘连|重复|模糊)|笔触|涂抹|团块', section_lower):
            label['texture_artifact'] = 1
        
        # Check for text artifacts
        if re.search(r'伪文字|文字.*?不可辨|签名', section_lower):
            label['text_artifact'] = 1
        
        # Check for relation errors
        if re.search(r'关系.*?(不清|含混|混乱|不够严谨|不明确)', section_lower):
            label['relation_error'] = 1
        
        # Check for limb errors
        if re.search(r'肢体|四肢|腿部|手臂', section_lower):
            label['limb_error'] = 1
        
        # Check for geometry/perspective issues
        if re.search(r'透视.*?(混乱|不自然|不严谨)|透视关系较混乱', section_lower):
            label['perspective_ok'] = 0
            label['geometry_ok'] = 0
        
        # Check semantic fidelity
        if re.search(r'主体明确|主体清晰', section_lower):
            label['subject_ok'] = 1
        elif re.search(r'主体.*?(不明确|无法确认|不可靠确认)', section_lower):
            label['subject_ok'] = 0
            label['missing_subject'] = 1
        
        # Check style consistency
        if re.search(r'风格一致|风格统一', section_lower):
            label['style_ok'] = 1
        elif re.search(r'风格.*?(不一致|降低)', section_lower):
            label['style_ok'] = 0
        
        # Extract notes from uncertain items
        uncertain_match = re.search(r'不确定项[：:](.*?)(?=\n###|\Z)', section, re.DOTALL)
        if uncertain_match:
            notes_text = uncertain_match.group(1).strip()
            notes_text = re.sub(r'\n- ', '; ', notes_text)
            notes_text = re.sub(r'\n', ' ', notes_text)
            label['semantic_notes'] = notes_text[:200]
        
        results.append(label)
    
    return results


def generate_template_csv():
    """Generate a template CSV if parsing fails."""
    template = []
    for filename in IMAGE_FILES:
        template.append({
            'filename': filename,
            'subject_ok': 1,
            'attribute_ok': 1,
            'scene_ok': 1,
            'relation_ok': 1,
            'style_ok': 1,
            'anatomy_error': 0,
            'relation_error': 0,
            'missing_subject': 0,
            'hand_error': 0,
            'face_error': 0,
            'limb_error': 0,
            'boundary_error': 0,
            'texture_artifact': 0,
            'text_artifact': 0,
            'geometry_ok': 1,
            'occlusion_ok': 1,
            'perspective_ok': 1,
            'semantic_notes': 'Manual review needed',
            'structure_notes': '',
            'confidence': 0.5
        })
    return template


def save_csv(labels, filepath):
    """Save labels to CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    fieldnames = [
        'filename', 'subject_ok', 'attribute_ok', 'scene_ok', 'relation_ok', 'style_ok',
        'anatomy_error', 'relation_error', 'missing_subject',
        'hand_error', 'face_error', 'limb_error', 'boundary_error',
        'texture_artifact', 'text_artifact',
        'geometry_ok', 'occlusion_ok', 'perspective_ok',
        'semantic_notes', 'structure_notes', 'confidence'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for label in labels:
            # Only write fields that are in fieldnames
            row = {k: v for k, v in label.items() if k in fieldnames}
            writer.writerow(row)
    
    print(f"Saved {len(labels)} labels to {filepath}")


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 1: Vision Review to CSV Converter")
    print("=" * 60)
    
    # Check if vision_review.md exists
    if not VISION_REVIEW.exists():
        print(f"Error: {VISION_REVIEW} not found!")
        print("Generating template CSV instead...")
        labels = generate_template_csv()
    else:
        print(f"Parsing {VISION_REVIEW}...")
        labels = parse_vision_review(VISION_REVIEW)
        
        # If parsing failed or returned empty, use template
        if not labels:
            print("Warning: Parsing returned no results. Using template...")
            labels = generate_template_csv()
        else:
            print(f"Successfully parsed {len(labels)} image reviews")
    
    # Save to CSV
    save_csv(labels, OUTPUT_FILE)
    
    # Print summary
    print("\nSummary:")
    print(f"  Total images: {len(labels)}")
    
    # Count errors
    error_counts = {
        'hand_error': sum(1 for l in labels if l.get('hand_error', 0)),
        'face_error': sum(1 for l in labels if l.get('face_error', 0)),
        'boundary_error': sum(1 for l in labels if l.get('boundary_error', 0)),
        'texture_artifact': sum(1 for l in labels if l.get('texture_artifact', 0)),
        'text_artifact': sum(1 for l in labels if l.get('text_artifact', 0)),
    }
    
    print("  Error distribution:")
    for error_type, count in error_counts.items():
        if count > 0:
            print(f"    {error_type}: {count} images")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
