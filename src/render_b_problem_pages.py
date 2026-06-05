"""
Re-render B题 PDF pages to figures/vision_inputs/b_problem_pages/
Only renders the actual problem statement PDF, not the integrity notice or rules.
"""
import fitz  # PyMuPDF
import os

# Paths
pdf_path = r"F:\Mathematical 2026\B题：AI生成内容的质量评估与参数优化\B题：AI生成内容的质量评估与参数优化.pdf"
output_dir = r"F:\Mathematical 2026\figures\vision_inputs\b_problem_pages"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Open PDF
doc = fitz.open(pdf_path)
print(f"PDF: {pdf_path}")
print(f"Pages: {len(doc)}")
print(f"Output: {output_dir}")
print()

# Render each page
for i, page in enumerate(doc):
    # Render at 200 DPI for good quality
    mat = fitz.Matrix(200/72, 200/72)
    pix = page.get_pixmap(matrix=mat)
    
    # Save
    output_path = os.path.join(output_dir, f"page_{i+1:03d}.png")
    pix.save(output_path)
    
    # Print info
    text = page.get_text()[:100].replace('\n', ' ')
    print(f"Page {i+1}: {output_path}")
    print(f"  Size: {pix.width}x{pix.height}")
    print(f"  Text preview: {text}...")
    print()

doc.close()
print("Done!")
