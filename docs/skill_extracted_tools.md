# Skill Extracted: Tools for B题

> Extracted from `math-modeling-skill-main/tools/` for 2026 中青杯 B题 project.

---

## 一、PDF 处理方法

### 1.1 PyMuPDF (fitz) - 快速文本提取

```python
import fitz

doc = fitz.open("document.pdf")
for page in doc:
    text = page.get_text()
    print(text)
```

### 1.2 pdfplumber - 文本和表格提取

```python
import pdfplumber

# 提取文本
with pdfplumber.open("题目.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

# 提取表格
with pdfplumber.open("题目.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### 1.3 pypdf - 基本操作（合并、拆分、旋转）

```python
from pypdf import PdfReader, PdfWriter

# 读取PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# 提取文本
text = ""
for page in reader.pages:
    text += page.extract_text()
```

### 1.4 命令行工具

```bash
# 提取文本（poppler-utils）
pdftotext -layout input.pdf output.txt

# 提取图片
pdfimages -j input.pdf output_prefix

# 合并PDF（qpdf）
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
```

### B题用途

- 读取 B题 PDF 题面
- 提取题目中的表格数据
- 参考优秀论文

---

## 二、DOCX 处理方法

### 2.1 python-docx - 读取和编辑

```python
from docx import Document

doc = Document("template.docx")
for para in doc.paragraphs:
    print(para.text)
```

### 2.2 docx-js (npm) - 创建新文档

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');

const doc = new Document({
  styles: {
    default: { document: { run: { font: "SimSun", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal",
        run: { size: 32, bold: true, font: "SimHei" } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },  // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("摘要")] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("论文.docx", buffer);
});
```

### 2.3 公式处理

**方案一：占位符替换（推荐）**

```bash
pip install latex2mathml lxml python-docx

python tools/docx/scripts/equations.py replace paper.docx \
    --replace "EQ_LOSS" "\\min L(\\theta) = \\frac{1}{n}\\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2" \
    -o paper_final.docx
```

**方案二：Markdown + pandoc**

```bash
python tools/docx/scripts/equations.py generate paper.md -o 论文.docx --template 模板.docx
```

### 2.4 关键规则

- 页面大小：A4（11906 × 16838 DXA）
- 页边距：1440 DXA = 1 英寸
- 字体：宋体正文 + 黑体标题
- 行距：1.5倍
- 图有图号+图题（图下方），表有表号+表题（表上方）
- 三线表格式
- 每张图片必须有详细的文字解释和分析（≥100字）

### B题用途

- 生成最终论文 .docx 文件
- 插入编程手生成的图表
- 插入数学公式

---

## 三、XLSX 处理方法

### 3.1 pandas - 数据分析

```python
import pandas as pd

# 读取Excel
df = pd.read_excel('data.xlsx')
print(df.head())
print(df.info())
print(df.describe())

# 写入Excel
df.to_excel('output.xlsx', index=False)
```

### 3.2 openpyxl - 格式和公式

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# 创建新文件
wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Hello'
sheet['B2'] = '=SUM(A1:A10)'  # 使用公式而非硬编码
wb.save('output.xlsx')

# 编辑现有文件
wb = load_workbook('existing.xlsx')
sheet = wb.active
sheet['A1'] = 'New Value'
wb.save('modified.xlsx')
```

### 3.3 关键规则

**使用 Excel 公式而非硬编码值**：

```python
# ❌ 错误 - 硬编码
sheet['B10'] = 5000

# ✅ 正确 - 使用公式
sheet['B10'] = '=SUM(B2:B9)'
```

**输入表格只读不写，结果表格保持原有结构**。

**公式重新计算**：

```bash
python scripts/recalc.py output.xlsx
```

### B题用途

- 读取题目附件中的数据表格
- 输出计算结果到 Excel
- 保持结果表格格式

---

## 四、论文搜索方法 (OpenAlex API)

### 4.1 OpenAlex 基础搜索

```python
from openalex_scholar import OpenAlexScholar

scholar = OpenAlexScholar(email="your@email.com")

# 基础搜索
papers = scholar.search_papers("grey prediction model GM(1,1)")

# 高级搜索（按引用量排序 + 领域过滤 + 最低引用）
papers = scholar.search_papers(
    query="analytic hierarchy process AHP",
    sort="cited_by_count:desc",
    min_citations=5,
    field_filter="mathematics",
    limit=12,
)

for paper in papers:
    print(f"标题: {paper.title}")
    print(f"作者: {', '.join(paper.authors)}")
    print(f"年份: {paper.publication_year}")
    print(f"引用: {paper.cited_by_count}")
    print(f"引用格式: {paper.citation_format}")
```

### 4.2 混合搜索（OpenAlex + AnySearch 双引擎）

```bash
python tools/paper_search/scripts/hybrid_scholar.py \
    --query "TOPSIS multi-criteria decision" \
    --min-citations 10 \
    --year-from 2015 \
    --field mathematics \
    --limit 10 \
    --email "your@email.com"
```

### 4.3 B题相关搜索关键词

| 搜索目的 | 关键词 |
|---------|--------|
| 评价方法 | `analytic hierarchy process AHP`, `TOPSIS multi-criteria decision`, `entropy weight method` |
| 图像质量 | `image quality assessment`, `image quality metric` |
| 视频质量 | `video quality assessment`, `temporal stability` |
| 模糊评价 | `fuzzy comprehensive evaluation` |
| 组合赋权 | `combined weighting method`, `subjective objective weighting` |

### 4.4 搜索策略

| 目的 | 推荐参数 |
|------|---------|
| 找经典理论文献 | `sort="cited_by_count:desc"` `min_citations=50` |
| 找最新前沿进展 | `sort="publication_year:desc"` `year_from=2020` |
| 找数学方法论论文 | `field_filter="mathematics"` |
| 找建模竞赛可用文献 | `min_citations=5` `year_from=2015` |

---

## 五、可视化规范

### 5.1 Figure Contract（前置合同）

在编写任何绘图代码之前，必须先建立 Figure Contract：
1. **核心结论**：用一句话写出这张图必须证明的核心主张
2. **证据链**：将核心结论拆解为若干条证据，每个面板对应一条独特证据
3. **防冗余原则**：遮盖任意一个面板后，核心结论仍能从其他面板完整读取，则该面板是冗余的

### 5.2 标准调色板

```python
PALETTE = {
    'blue_main':      '#0F4D92',
    'blue_secondary': '#3775BA',
    'green_1': '#DDF3DE',
    'green_2': '#AADCA9',
    'green_3': '#8BCF8B',
    'red_1':      '#F6CFCB',
    'red_2':      '#E9A6A1',
    'red_strong': '#B64342',
    'neutral_light': '#CFCECE',
    'neutral_mid':   '#767676',
    'neutral_dark':  '#4D4D4D',
    'neutral_black': '#272727',
    'gold':    '#FFD700',
    'teal':    '#42949E',
    'violet':  '#9A4D8E',
    'magenta': '#EA84DD',
}
```

### 5.3 Python 全局配置

```python
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

# 中文字体优先 + 多字体备选
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# SVG 可编辑文本（强制）
plt.rcParams['svg.fonttype'] = 'none'

# 无网格线 + 精简坐标轴（仅保留左+下 spines）
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8

# 图例无边框
plt.rcParams['legend.frameon'] = False

# 字体大小层次
plt.rcParams['font.size'] = 7
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 6.5
plt.rcParams['ytick.labelsize'] = 6.5
plt.rcParams['legend.fontsize'] = 6.5
plt.rcParams['lines.linewidth'] = 1.5
```

### 5.4 统一保存函数

```python
def save_figure(fig, filename):
    """统一保存：SVG + PNG + 关闭图表"""
    fig.savefig(f'figures/{filename}.svg', bbox_inches='tight')
    fig.savefig(f'figures/{filename}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
```

### 5.5 面板标签规范

```python
ax.text(-0.08, 1.08, 'a', transform=ax.transAxes,
        fontsize=22, fontweight='bold', va='top', ha='right')
```

- 小写粗体 a, b, c, d, ...
- 每个子图左上角（transAxes 坐标）
- 字号 22

### 5.6 子图布局规则

- 每个大图最多 2 个子图
- 禁止在一个大图中包含 3 个或更多子图
- 使用 GridSpec 不对称布局

### 5.7 常见图表类型选择

| 数据类型 | 推荐图表 | 用途 |
|---------|---------|------|
| 分类对比 | 柱状图/分组柱状图 | 展示不同方法在同一指标上的差异 |
| 时间趋势 | 折线图+置信区间 | 展示随时间的变化趋势 |
| 数据分布 | 箱线图/小提琴图/直方图 | 展示数据分布特征和异常值 |
| 相关性 | 散点图+拟合线 | 展示两个变量之间的关系 |
| 矩阵数据 | 热力图 | 展示相关性矩阵或混淆矩阵 |
| 综合评价 | 雷达图 | 多指标综合对比 |
