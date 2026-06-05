"""
Phase 7a: Export all results to Excel workbook.

This script consolidates all final results into a single Excel workbook
for easy reference and submission.

Input: All CSV files in results/final/
Output: results/final/results_final.xlsx
"""
import os
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent

RESULTS_DIR = ROOT / "results" / "final"
OUTPUT_FILE = RESULTS_DIR / "results_final.xlsx"


def main():
    """Main function."""
    print("=" * 60)
    print("Phase 7a: Export to Excel")
    print("=" * 60)
    
    sheets = {
        'Image Metrics': 'image_metrics.csv',
        'Vision Labels': ROOT / "results" / "intermediate" / "vision_labels.csv",
        'Dimension Scores': 'image_dimension_scores.csv',
        'Image Weights': 'image_weights.csv',
        'TOPSIS Scores': 'image_topsis_scores.csv',
        'Gray Relation': 'gray_relation_scores.csv',
        'Rank Consistency': 'rank_consistency.csv',
        'Sensitivity': 'sensitivity_summary.csv',
        'Rank Stability': 'rank_stability.csv',
        'Video Metrics': 'video_metrics.csv',
        'Video Summary': 'video_summary.csv',
        'Video Anomalies': 'video_anomaly_frames.csv',
        'Parameter Suggestions': 'parameter_optimization_suggestions.csv'
    }
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        for sheet_name, file_name in sheets.items():
            if isinstance(file_name, Path):
                file_path = file_name
            else:
                file_path = RESULTS_DIR / file_name
            
            if file_path.exists():
                print(f"  Loading {sheet_name} from {file_path.name}...")
                df = pd.read_csv(file_path)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"    Added {len(df)} rows")
            else:
                print(f"  WARNING: {file_path.name} not found, skipping {sheet_name}")
    
    print(f"\nSaved Excel workbook to {OUTPUT_FILE}")
    
    print("\n" + "=" * 60)
    print("Excel Workbook Summary:")
    print("=" * 60)
    
    for sheet_name, file_name in sheets.items():
        if isinstance(file_name, Path):
            file_path = file_name
        else:
            file_path = RESULTS_DIR / file_name
        
        if file_path.exists():
            df = pd.read_csv(file_path)
            print(f"  {sheet_name}: {len(df)} rows x {len(df.columns)} columns")
        else:
            print(f"  {sheet_name}: [MISSING]")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    exit(main())
