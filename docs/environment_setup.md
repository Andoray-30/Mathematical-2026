# 环境配置指南 - Windows

## 1. 安装 Python

```powershell
winget install Python.Python.3.12
```

安装完成后重启终端，验证：
```powershell
python --version
pip --version
```

## 2. 安装 FFmpeg（视频处理必需）

```powershell
winget install Gyan.FFmpeg
```

验证：
```powershell
ffmpeg -version
```

## 3. 创建虚拟环境

```powershell
cd F:\Mathematical 2026
python -m venv .venv
.\.venv\Scripts\activate
```

## 4. 安装依赖

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. 验证安装

```powershell
python src/check_env.py
```

## 可选增强项

### Tesseract OCR（用于扫描件文字识别）

```powershell
winget install Tesseract-OCR.Tesseract
```

### LibreOffice（用于 doc 转 docx）

```powershell
winget install LibreOffice.LibreOffice
```

## 注意事项

- 第一阶段不强制安装大模型依赖（torch, transformers 等）
- 当前先保证 PDF、图片、视频、Excel、图表流水线稳定
- 如果遇到权限问题，以管理员身份运行 PowerShell

---

*Last updated: 2026-06-04*
