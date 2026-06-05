"""
Phase 6b: Image-level shortfall diagnosis.

This script generates per-image diagnostic reports identifying:
- Weakest dimension
- Main defect
- Recommended parameter adjustments

Input:
- results/final/image_dimension_scores.csv
- results/final/image_topsis_scores.csv
- results/intermediate/vision_labels.csv

Output: results/final/image_shortfall_diagnosis.csv
"""
import os
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent

DIMENSION_SCORES = ROOT / "results" / "final" / "image_dimension_scores.csv"
TOPSIS_SCORES = ROOT / "results" / "final" / "image_topsis_scores.csv"
VISION_LABELS = ROOT / "results" / "intermediate" / "vision_labels.csv"
OUTPUT_DIR = ROOT / "results" / "final"
OUTPUT_FILE = OUTPUT_DIR / "image_shortfall_diagnosis.csv"


def identify_main_defect(row):
    """Identify main defect based on vision labels and dimension scores."""
    defects = []
    
    if row.get('hand_error', 0):
        defects.append('手部结构异常')
    if row.get('face_error', 0):
        defects.append('面部细节问题')
    if row.get('limb_error', 0):
        defects.append('肢体结构问题')
    if row.get('boundary_error', 0):
        defects.append('边界融合问题')
    if row.get('texture_artifact', 0):
        defects.append('纹理伪影')
    if row.get('text_artifact', 0):
        defects.append('伪文字')
    if row.get('anatomy_error', 0):
        defects.append('解剖结构错误')
    if row.get('relation_error', 0):
        defects.append('空间关系不清')
    if row.get('geometry_ok', 1) == 0:
        defects.append('透视/几何问题')
    
    if not defects:
        if row.get('S_tech', 100) < 50:
            defects.append('技术指标偏低')
        if row.get('S_str', 100) < 50:
            defects.append('结构完整性不足')
        if not defects:
            defects.append('无明显缺陷')
    
    return '; '.join(defects[:3])


def get_weakest_dimension(row):
    """Identify the weakest dimension."""
    scores = {
        'semantic': row.get('S_sem', 100),
        'technical': row.get('S_tech', 100),
        'structural': row.get('S_str', 100)
    }
    return min(scores, key=scores.get)


def get_recommended_params(weakest_dim, main_defect):
    """Get recommended parameter adjustments."""
    params = {
        'semantic': ['prompt_detail', 'cfg_scale'],
        'technical': ['resolution', 'sampling_steps'],
        'structural': ['structure_control_strength', 'local_inpainting']
    }
    
    defect_params = {
        '手部结构异常': ['structure_control_strength', 'local_inpainting'],
        '面部细节问题': ['structure_control_strength', 'local_inpainting'],
        '肢体结构问题': ['structure_control_strength', 'local_inpainting'],
        '边界融合问题': ['structure_control_strength', 'cfg_scale'],
        '纹理伪影': ['sampling_steps', 'resolution'],
        '伪文字': ['prompt_detail', 'negative_prompt_strength'],
        '解剖结构错误': ['structure_control_strength', 'prompt_detail'],
        '空间关系不清': ['prompt_detail', 'cfg_scale'],
        '透视/几何问题': ['structure_control_strength', 'resolution'],
        '技术指标偏低': ['resolution', 'sampling_steps'],
        '结构完整性不足': ['structure_control_strength', 'local_inpainting']
    }
    
    rec1 = params.get(weakest_dim, ['resolution', 'sampling_steps'])
    
    for defect, p in defect_params.items():
        if defect in main_defect:
            rec2 = p
            break
    else:
        rec2 = rec1
    
    return rec1[0], rec2[0] if rec2 else rec1[1]


def main():
    """Main function."""
    print("=" * 60)
    print("Image Shortfall Diagnosis")
    print("=" * 60)
    
    print(f"Loading dimension scores from {DIMENSION_SCORES}...")
    dim_df = pd.read_csv(DIMENSION_SCORES)
    
    print(f"Loading TOPSIS scores from {TOPSIS_SCORES}...")
    topsis_df = pd.read_csv(TOPSIS_SCORES)
    
    print(f"Loading vision labels from {VISION_LABELS}...")
    vision_df = pd.read_csv(VISION_LABELS)
    
    merged = pd.merge(dim_df, topsis_df[['filename', 'rank', 'quality_level']], on='filename')
    merged = pd.merge(merged, vision_df, on='filename', how='left')
    
    print(f"  Merged {len(merged)} images")
    
    print("Generating diagnoses...")
    
    diagnoses = []
    for _, row in merged.iterrows():
        weakest = get_weakest_dimension(row)
        main_defect = identify_main_defect(row)
        rec1, rec2 = get_recommended_params(weakest, main_defect)
        
        diagnoses.append({
            'filename': row['filename'],
            'rank': row['rank'],
            'quality_level': row['quality_level'],
            'S_sem': row['S_sem'],
            'S_tech': row['S_tech'],
            'S_str': row['S_str'],
            'weakest_dimension': weakest,
            'main_defect': main_defect,
            'recommended_parameter_1': rec1,
            'recommended_parameter_2': rec2,
            'reason': f"{weakest}维度得分最低，主要缺陷: {main_defect}"
        })
    
    diag_df = pd.DataFrame(diagnoses)
    diag_df = diag_df.sort_values('rank').reset_index(drop=True)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    diag_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved diagnosis to {OUTPUT_FILE}")
    
    print("\n" + "=" * 60)
    print("Image Shortfall Diagnosis Results:")
    print("=" * 60)
    print(f"{'Rank':<6} {'Filename':<12} {'Quality':<8} {'Weakest':<12} {'Main Defect':<30} {'Param1':<25} {'Param2':<25}")
    print("-" * 120)
    for _, row in diag_df.iterrows():
        print(f"{row['rank']:<6} {row['filename']:<12} {row['quality_level']:<8} {row['weakest_dimension']:<12} {row['main_defect']:<30} {row['recommended_parameter_1']:<25} {row['recommended_parameter_2']:<25}")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
