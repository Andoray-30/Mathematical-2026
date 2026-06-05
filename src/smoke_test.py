"""Smoke test - verify basic environment and file availability."""
import sys
import importlib
import subprocess
from pathlib import Path

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

def check_python():
    """Check Python version."""
    version = sys.version_info
    return f"Python {version.major}.{version.minor}.{version.micro}", version.major >= 3 and version.minor >= 8

def check_dependencies():
    """Check required packages."""
    required = [
        'numpy', 'pandas', 'scipy', 'sklearn',
        'matplotlib', 'cv2', 'skimage', 'PIL',
        'fitz', 'pdfplumber', 'pypdf', 'docx',
        'openpyxl', 'xlsxwriter', 'tqdm', 'imageio'
    ]
    results = []
    all_ok = True
    for pkg in required:
        try:
            importlib.import_module(pkg)
            results.append(f"  [OK] {pkg}")
        except ImportError:
            results.append(f"  [FAIL] {pkg} - NOT INSTALLED")
            all_ok = False
    return '\n'.join(results), all_ok

def check_ffmpeg():
    """Check FFmpeg availability."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
        return "FFmpeg available", result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "FFmpeg not found", False

def check_files():
    """Check B题 files existence."""
    b_dir = Path("B题：AI生成内容的质量评估与参数优化")
    checks = []
    all_ok = True
    
    # Check PDF
    pdf_files = list(b_dir.glob("*.pdf"))
    if pdf_files:
        checks.append(f"  [OK] PDF files: {len(pdf_files)}")
    else:
        checks.append(f"  [FAIL] No PDF files found")
        all_ok = False
    
    # Check images
    img_dir = b_dir / "附件1"
    if img_dir.exists():
        images = list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpg"))
        checks.append(f"  [OK] Images: {len(images)}")
    else:
        checks.append(f"  [FAIL] 附件1 directory not found")
        all_ok = False
    
    # Check video
    vid_dir = b_dir / "附件2"
    if vid_dir.exists():
        videos = list(vid_dir.glob("*.mp4"))
        checks.append(f"  [OK] Videos: {len(videos)}")
    else:
        checks.append(f"  [FAIL] 附件2 directory not found")
        all_ok = False
    
    # Check template
    templates = list(b_dir.glob("*.doc")) + list(b_dir.glob("*.docx"))
    if templates:
        checks.append(f"  [OK] Template: {templates[0].name}")
    else:
        checks.append(f"  [FAIL] No template found")
        all_ok = False
    
    return '\n'.join(checks), all_ok

def check_directories():
    """Check writable directories."""
    dirs = ['results', 'figures', 'docs', 'paper', 'support']
    results = []
    all_ok = True
    
    for d in dirs:
        path = Path(d)
        path.mkdir(exist_ok=True)
        test_file = path / '.write_test'
        try:
            test_file.write_text('test', encoding='utf-8')
            test_file.unlink()
            results.append(f"  [OK] {d}/ writable")
        except Exception as e:
            results.append(f"  [FAIL] {d}/ not writable: {e}")
            all_ok = False
    
    return '\n'.join(results), all_ok

def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("Smoke Test - Environment Verification")
    print("=" * 60)
    
    report = []
    report.append("# Smoke Test Report\n")
    
    # 1. Python
    print("\n1. Python Version")
    msg, ok = check_python()
    print(f"  {msg}")
    report.append(f"## 1. Python\n- {msg}\n- Status: {'PASS' if ok else 'FAIL'}\n")
    
    # 2. Dependencies
    print("\n2. Dependencies")
    msg, ok = check_dependencies()
    print(msg)
    report.append(f"## 2. Dependencies\n{msg}\n- Status: {'PASS' if ok else 'FAIL'}\n")
    
    # 3. FFmpeg
    print("\n3. FFmpeg")
    msg, ok = check_ffmpeg()
    print(f"  {msg}")
    report.append(f"## 3. FFmpeg\n- {msg}\n- Status: {'PASS' if ok else 'FAIL'}\n")
    
    # 4. B题 Files
    print("\n4. B题 Files")
    msg, ok = check_files()
    print(msg)
    report.append(f"## 4. B题 Files\n{msg}\n- Status: {'PASS' if ok else 'FAIL'}\n")
    
    # 5. Directories
    print("\n5. Directories")
    msg, ok = check_directories()
    print(msg)
    report.append(f"## 5. Directories\n{msg}\n- Status: {'PASS' if ok else 'FAIL'}\n")
    
    # Save report
    output_path = Path("results/smoke_test_report.txt")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text('\n'.join(report), encoding='utf-8')
    
    print(f"\n{'=' * 60}")
    print(f"Report saved to: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
