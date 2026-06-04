"""Main pipeline script."""
import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print('='*60)
    
    script_path = Path("src") / script_name
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], capture_output=False, text=True)
        if result.returncode == 0:
            print(f"  {description} completed successfully")
            return True
        else:
            print(f"  {description} failed with return code {result.returncode}")
            return False
    except Exception as e:
        print(f"  {description} failed with error: {e}")
        return False

def main():
    print("="*60)
    print("2026 中青杯 B 题 - AI 生成内容质量评估")
    print("="*60)
    
    steps = [
        ("check_env.py", "Environment Check"),
        ("extract_pdf.py", "PDF Extraction"),
        ("extract_docx.py", "DOCX Extraction"),
        ("inspect_media.py", "Media Inspection"),
        ("image_metrics.py", "Image Metrics Calculation"),
        ("video_slice.py", "Video Frame Extraction"),
        ("video_metrics.py", "Video Metrics Calculation"),
        ("evaluation_models.py", "Evaluation Models"),
        ("export_excel.py", "Excel Export"),
        ("plot_results.py", "Plot Generation")
    ]
    
    results = []
    for script, description in steps:
        success = run_script(script, description)
        results.append((description, success))
    
    print("\n" + "="*60)
    print("Pipeline Summary")
    print("="*60)
    
    all_success = True
    for description, success in results:
        status = "SUCCESS" if success else "FAILED"
        print(f"  {status}: {description}")
        if not success:
            all_success = False
    
    print("\n" + "="*60)
    if all_success:
        print("All steps completed successfully!")
        print("\nOutput files:")
        print("  - results/*.csv")
        print("  - results/results.xlsx")
        print("  - figures/*.png")
        print("  - figures/*.svg")
    else:
        print("Some steps failed. Please check the errors above.")
    print("="*60)

if __name__ == "__main__":
    main()
