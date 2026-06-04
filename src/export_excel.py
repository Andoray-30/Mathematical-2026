"""Export all results to Excel."""
import pandas as pd
from pathlib import Path

def main():
    results_dir = Path("results")
    csv_files = [
        ('media_inventory', 'Media Inventory'),
        ('image_metrics', 'Image Metrics'),
        ('image_scores', 'Image Scores'),
        ('video_basic_info', 'Video Basic Info'),
        ('video_metrics', 'Video Metrics'),
        ('video_anomaly_frames', 'Video Anomaly Frames'),
        ('final_summary', 'Final Summary')
    ]
    
    output_path = results_dir / "results.xlsx"
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for csv_name, sheet_name in csv_files:
            csv_path = results_dir / f"{csv_name}.csv"
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"  {csv_name}.csv -> {sheet_name}")
            else:
                print(f"  {csv_name}.csv - not found")
        
        indicator_desc = pd.DataFrame({
            'Indicator': ['laplacian_var', 'tenengrad', 'brightness_mean', 'brightness_std',
                          'saturation_mean', 'saturation_std', 'entropy', 'edge_density',
                          'noise_estimate', 'structure_proxy'],
            'Description': ['Laplacian variance (sharpness)', 'Tenengrad gradient (focus)',
                            'Brightness mean', 'Brightness std (contrast)', 'Saturation mean',
                            'Saturation std', 'Shannon entropy (information)', 'Canny edge density',
                            'Noise estimate', 'Structure completeness proxy'],
            'Direction': ['Positive', 'Positive', 'Moderate', 'Positive', 'Positive',
                          'Positive', 'Positive', 'Positive', 'Negative', 'Positive']
        })
        indicator_desc.to_excel(writer, sheet_name='Indicator Description', index=False)
    
    print(f"\nExcel saved to: {output_path}")

if __name__ == "__main__":
    main()
