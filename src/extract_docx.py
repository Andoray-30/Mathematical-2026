"""Extract content from DOCX files."""
from docx import Document
from pathlib import Path

def extract_docx(docx_path):
    doc = Document(docx_path)
    content = []
    for para in doc.paragraphs:
        if para.text.strip():
            style = para.style.name if para.style else "Normal"
            content.append({'text': para.text, 'style': style})
    return content

def save_as_markdown(content, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Extracted Document\n\n")
        for item in content:
            style = item['style']
            text = item['text']
            if 'Heading 1' in style:
                f.write(f"# {text}\n\n")
            elif 'Heading 2' in style:
                f.write(f"## {text}\n\n")
            elif 'Heading 3' in style:
                f.write(f"### {text}\n\n")
            else:
                f.write(f"{text}\n\n")

def main():
    b_problem_dir = Path("B题：AI生成内容的质量评估与参数优化")
    
    for ext in ['*.docx', '*.doc']:
        for doc_path in b_problem_dir.glob(ext):
            print(f"\nProcessing: {doc_path.name}")
            
            if doc_path.suffix == '.doc':
                print("WARNING: .doc format detected.")
                print("Please convert to .docx using LibreOffice:")
                print(f'  soffice --headless --convert-to docx "{doc_path}"')
                continue
            
            try:
                content = extract_docx(str(doc_path))
                output_path = Path("docs") / f"{doc_path.stem}_extracted.md"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                save_as_markdown(content, output_path)
                print(f"Saved to: {output_path}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
