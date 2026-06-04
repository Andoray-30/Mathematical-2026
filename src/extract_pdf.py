"""Extract text and images from PDF files."""
import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path

def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num, page in enumerate(doc):
        text += f"\n--- Page {page_num + 1} ---\n"
        text += page.get_text()
    doc.close()
    return text

def render_pages(pdf_path, output_dir, dpi=300):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc):
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat)
        output_path = output_dir / f"page_{page_num + 1:03d}.png"
        pix.save(str(output_path))
        pages.append(output_path)
        print(f"  Saved: {output_path.name}")
    doc.close()
    return pages

def main():
    b_problem_dir = Path("B题：AI生成内容的质量评估与参数优化")
    pdf_files = list(b_problem_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found")
        return
    
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")
        print("-" * 40)
        
        text = extract_text_pymupdf(str(pdf_path))
        
        output_path = Path("docs") / f"{pdf_path.stem}_extracted.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {pdf_path.name}\n\n")
            f.write(text)
        print(f"Text saved to: {output_path}")
        
        pages_dir = Path("figures/pdf_pages")
        render_pages(str(pdf_path), pages_dir)

if __name__ == "__main__":
    main()
