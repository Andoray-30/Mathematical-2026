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

ROOT = Path(__file__).parent.parent

VISION_REVIEW = ROOT / "docs" / "vision_review.md"
OUTPUT_DIR = ROOT / "results" / "intermediate"
OUTPUT_FILE = OUTPUT_DIR / "vision_labels.csv"

IMAGE_FILES = [
    "1.png", "2.png", "3.png", "4.png",
    "5.jpg", "6.jpg", "7.jpg", "8.jpg"
]

QUALITY_MAP = {
    "高": 1.0,
    "中": 0.6,
    "低": 0.3
}


def extract_field(text, field_name):
    """Extract a field value from the section text."""
    pattern = rf'\*\*{field_name}\*\*[：:]\s*(.*?)(?=\n- \*\*|\n###|\Z)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        value = match.group(1).strip()
        value = re.sub(r'\n', ' ', value)
        return value
    return ''


def count_uncertain_items(text):
    """Count uncertain items and assess their strength."""
    uncertain_section = extract_field(text, '不确定项')
    if not uncertain_section:
        return 0, 0.8
    
    items = re.split(r'[；;]', uncertain_section)
    items = [item.strip() for item in items if item.strip()]
    
    strong_uncertain = 0
    for item in items:
        if any(keyword in item for keyword in ['无法确认', '不确定', '不能确认', '无法判断']):
            strong_uncertain += 1
    
    return len(items), strong_uncertain


def calculate_confidence(uncertain_count, strong_uncertain, quality_level):
    """Calculate confidence based on uncertainty and quality."""
    base_confidence = 0.9
    
    uncertainty_penalty = uncertain_count * 0.05
    strong_penalty = strong_uncertain * 0.1
    
    if quality_level == '高':
        quality_bonus = 0.05
    elif quality_level == '中':
        quality_bonus = 0.0
    else:
        quality_bonus = -0.1
    
    confidence = base_confidence - uncertainty_penalty - strong_penalty + quality_bonus
    return max(0.3, min(0.95, confidence))


def parse_vision_review(filepath):
    """Parse vision_review.md and extract structured information for each image."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    image_sections = re.split(r'### 2\.\d+ 图像 \S+', content)
    
    results = []
    
    for i, section in enumerate(image_sections[1:], 0):
        if i >= len(IMAGE_FILES):
            break
            
        filename = IMAGE_FILES[i]
        
        quality_match = re.search(r'质量判断[：:]\s*\*\*(\S+)\*\*', section)
        quality_level = quality_match.group(1) if quality_match else '中'
        quality_score = QUALITY_MAP.get(quality_level, 0.6)
        
        ai_defects = extract_field(section, 'AI生成瑕疵')
        structure_integrity = extract_field(section, '结构完整性')
        semantic_fidelity = extract_field(section, '语义保真度')
        uncertain_items = extract_field(section, '不确定项')
        
        uncertain_count, strong_uncertain = count_uncertain_items(section)
        confidence = calculate_confidence(uncertain_count, strong_uncertain, quality_level)
        
        semantic_notes = f"语义保真度: {semantic_fidelity[:150]}" if semantic_fidelity else ""
        structure_notes = f"结构完整性: {structure_integrity[:150]}" if structure_integrity else ""
        
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
            'semantic_notes': semantic_notes,
            'structure_notes': structure_notes,
            'confidence': round(confidence, 2),
            'vision_quality_level': quality_level,
            'vision_quality_score': quality_score,
            'ai_defects_summary': ai_defects[:200] if ai_defects else "",
            'uncertain_items_count': uncertain_count
        }
        
        section_lower = section.lower()
        
        if re.search(r'手[部指].*?(不清晰|结构|边界|可疑|不够准确|形态)', section_lower):
            label['hand_error'] = 1
            label['anatomy_error'] = 1
        
        if re.search(r'面部|五官', section_lower):
            label['face_error'] = 1
        
        if re.search(r'边界.*?(融合|不够明确|不清)|融合.*?边界', section_lower):
            label['boundary_error'] = 1
        
        if re.search(r'纹理.*?(粘连|重复|模糊)|笔触|涂抹|团块', section_lower):
            label['texture_artifact'] = 1
        
        if re.search(r'伪文字|文字.*?不可辨|签名', section_lower):
            label['text_artifact'] = 1
        
        if re.search(r'关系.*?(不清|含混|混乱|不够严谨|不明确)', section_lower):
            label['relation_error'] = 1
        
        if re.search(r'肢体|四肢|腿部|手臂', section_lower):
            label['limb_error'] = 1
        
        if re.search(r'透视.*?(混乱|不自然|不严谨)|透视关系较混乱', section_lower):
            label['perspective_ok'] = 0
            label['geometry_ok'] = 0
        
        if re.search(r'主体明确|主体清晰', section_lower):
            label['subject_ok'] = 1
        elif re.search(r'主体.*?(不明确|无法确认|不可靠确认)', section_lower):
            label['subject_ok'] = 0
            label['missing_subject'] = 1
        
        if re.search(r'风格一致|风格统一', section_lower):
            label['style_ok'] = 1
        elif re.search(r'风格.*?(不一致|降低)', section_lower):
            label['style_ok'] = 0
        
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
            'confidence': 0.5,
            'vision_quality_level': '中',
            'vision_quality_score': 0.6,
            'ai_defects_summary': '',
            'uncertain_items_count': 0
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
        'semantic_notes', 'structure_notes', 'confidence',
        'vision_quality_level', 'vision_quality_score',
        'ai_defects_summary', 'uncertain_items_count'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for label in labels:
            row = {k: v for k, v in label.items() if k in fieldnames}
            writer.writerow(row)
    
    print(f"Saved {len(labels)} labels to {filepath}")


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 1: Vision Review to CSV Converter")
    print("=" * 60)
    
    if not VISION_REVIEW.exists():
        print(f"Error: {VISION_REVIEW} not found!")
        print("Generating template CSV instead...")
        labels = generate_template_csv()
    else:
        print(f"Parsing {VISION_REVIEW}...")
        labels = parse_vision_review(VISION_REVIEW)
        
        if not labels:
            print("Warning: Parsing returned no results. Using template...")
            labels = generate_template_csv()
        else:
            print(f"Successfully parsed {len(labels)} image reviews")
    
    save_csv(labels, OUTPUT_FILE)
    
    print("\nSummary:")
    print(f"  Total images: {len(labels)}")
    
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
    
    print("\n  Quality levels:")
    for label in labels:
        print(f"    {label['filename']}: {label['vision_quality_level']} (confidence={label['confidence']})")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
