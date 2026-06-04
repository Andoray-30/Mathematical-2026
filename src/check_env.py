"""Check Python environment and dependencies."""
import sys
import importlib
from pathlib import Path

def check_python_version():
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("WARNING: Python 3.8+ recommended")
        return False
    return True

def check_dependencies():
    required = [
        'numpy', 'pandas', 'scipy', 'scikit-learn',
        'matplotlib', 'cv2', 'skimage', 'PIL',
        'fitz', 'pdfplumber', 'pypdf', 'docx',
        'openpyxl', 'xlsxwriter', 'tqdm', 'imageio'
    ]
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            missing.append(package)
    return missing

def check_ffmpeg():
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ FFmpeg is available")
            return True
    except FileNotFoundError:
        pass
    print("  ✗ FFmpeg - NOT FOUND")
    return False

def main():
    print("=" * 60)
    print("Environment Check")
    print("=" * 60)
    
    print("\n1. Python Version")
    python_ok = check_python_version()
    
    print("\n2. Dependencies")
    missing = check_dependencies()
    
    print("\n3. FFmpeg")
    ffmpeg_ok = check_ffmpeg()
    
    print("\n" + "=" * 60)
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
    
    report_path = Path("results/env_report.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Environment Check Report\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Python: {'OK' if python_ok else 'ISSUE'}\n")
        f.write(f"FFmpeg: {'OK' if ffmpeg_ok else 'ISSUE'}\n")
        if missing:
            f.write(f"Missing: {', '.join(missing)}\n")
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()
