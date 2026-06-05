"""
Generate methodology pipeline flowchart for the paper.

Outputs:
  figures/final/framework_flowchart.png  (300 DPI)
  figures/final/framework_flowchart.svg
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path as MPath
from pathlib import Path

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "figures" / "final"


def draw_rounded_box(ax, x, y, w, h, text, fc, ec, fontsize=9, linewidth=1.2):
    """Draw a rounded rectangle with centered text."""
    box = mpatches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.08",
        facecolor=fc, edgecolor=ec, linewidth=linewidth,
        zorder=2,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', zorder=3)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color='#555555'):
    """Draw a simple arrow from (x1,y1) to (x2,y2)."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=1.5, connectionstyle='arc3,rad=0'),
                zorder=1)


def draw_sub_items(ax, x_center, y, items, fontsize=7):
    """Draw small sub-items below a main box."""
    n = len(items)
    total_w = 0.6
    gap = total_w / n
    for i, item in enumerate(items):
        xi = x_center - total_w / 2 + gap / 2 + i * gap
        ax.text(xi, y, item, ha='center', va='center', fontsize=fontsize,
                color='#333333', style='italic', zorder=3)


def generate():
    fig, ax = plt.subplots(figsize=(10, 16))
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.3, 9.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Layout parameters
    cx = 0.5          # center x
    bw = 0.85         # box width
    bh = 0.45         # box height (main stages)
    bh_sub = 0.35     # box height (sub-items)
    y_start = 9.0
    dy = 0.95         # vertical spacing between stages

    # Color palette (muted academic tones)
    c_input   = '#E8F0FE'   # light blue
    c_process = '#D6E4F0'   # steel blue
    c_eval    = '#FFF3CD'   # warm yellow
    c_weight  = '#D4EDDA'   # light green
    c_rank    = '#C3E6CB'   # green
    c_verify  = '#F5C6CB'   # light red/pink
    c_video   = '#E2D9F3'   # light purple
    c_diag    = '#FFE0B2'   # light orange
    c_opt     = '#B3E5FC'   # sky blue
    ec_default = '#444444'

    # --- Stage 1: Problem Input ---
    y1 = y_start
    draw_rounded_box(ax, cx, y1, bw, bh, '1. 题目输入\nProblem Input', c_input, ec_default, fontsize=10)

    # --- Stage 2: Data Preprocessing ---
    y2 = y1 - dy
    draw_rounded_box(ax, cx, y2, bw, bh, '2. 图像/视频数据预处理\nImage / Video Data Preprocessing', c_process, ec_default, fontsize=9)
    draw_arrow(ax, cx, y1 - bh / 2, cx, y2 + bh / 2)

    # --- Stage 3: Three-Dimension Evaluation ---
    y3 = y2 - dy
    draw_rounded_box(ax, cx, y3, bw, bh, '3. 图像三维度评价\nImage Three-Dimension Evaluation', c_eval, ec_default, fontsize=9)
    draw_arrow(ax, cx, y2 - bh / 2, cx, y3 + bh / 2)
    # Sub-dimensions
    sub_y3 = y3 - bh / 2 - 0.18
    draw_sub_items(ax, cx, sub_y3, ['语义保真度', '技术质量', '结构完整性'], fontsize=7.5)

    # --- Stage 4: Combined Weighting ---
    y4 = y3 - dy - 0.15
    draw_rounded_box(ax, cx, y4, bw, bh, '4. AHP-熵权组合赋权\nAHP-Entropy Combined Weighting', c_weight, ec_default, fontsize=9)
    draw_arrow(ax, cx, sub_y3 - 0.1, cx, y4 + bh / 2)

    # --- Stage 5: TOPSIS Ranking ---
    y5 = y4 - dy
    draw_rounded_box(ax, cx, y5, bw, bh, '5. TOPSIS综合排序\nTOPSIS Comprehensive Ranking', c_rank, ec_default, fontsize=9)
    draw_arrow(ax, cx, y4 - bh / 2, cx, y5 + bh / 2)

    # --- Stage 6: Grey Relation & Sensitivity ---
    y6 = y5 - dy
    draw_rounded_box(ax, cx, y6, bw, bh, '6. 灰色关联与敏感性验证\nGrey Relation & Sensitivity Verification', c_verify, ec_default, fontsize=9)
    draw_arrow(ax, cx, y5 - bh / 2, cx, y6 + bh / 2)

    # --- Stage 7: Video Temporal Instability ---
    y7 = y6 - dy - 0.15
    draw_rounded_box(ax, cx, y7, bw, bh + 0.1, '7. 视频时序失稳检测\nVideo Temporal Instability Detection', c_video, ec_default, fontsize=9)
    draw_arrow(ax, cx, y6 - bh / 2, cx, y7 + (bh + 0.1) / 2)
    # Sub-methods
    sub_y7 = y7 - (bh + 0.1) / 2 - 0.2
    draw_sub_items(ax, cx, sub_y7, ['SSIM', '光流', 'Warp-SSIM', '候选波动帧'], fontsize=7.5)

    # --- Stage 8: Quality Shortfall Diagnosis ---
    y8 = y7 - dy - 0.25
    draw_rounded_box(ax, cx, y8, bw, bh, '8. 质量短板诊断\nQuality Shortfall Diagnosis', c_diag, ec_default, fontsize=9)
    draw_arrow(ax, cx, sub_y7 - 0.12, cx, y8 + bh / 2)

    # --- Stage 9: Parameter Optimization ---
    y9 = y8 - dy
    draw_rounded_box(ax, cx, y9, bw, bh, '9. 参数优化优先级建议\nParameter Optimization Priority', c_opt, ec_default, fontsize=9)
    draw_arrow(ax, cx, y8 - bh / 2, cx, y9 + bh / 2)

    # Feedback arrow from Stage 9 back to Stage 2 (right side)
    # Curved arrow on the right indicating iteration
    ax.annotate(
        '', xy=(cx + bw / 2 + 0.06, y2),
        xytext=(cx + bw / 2 + 0.06, y9),
        arrowprops=dict(
            arrowstyle='->', color='#888888', lw=1.2,
            connectionstyle='arc3,rad=-0.35',
        ),
        zorder=1,
    )
    ax.text(cx + bw / 2 + 0.16, (y2 + y9) / 2, '迭代\n反馈',
            ha='center', va='center', fontsize=7, color='#666666',
            style='italic')

    # Title
    ax.text(cx, y_start + 0.4, 'B题方法论流程图',
            ha='center', va='center', fontsize=13, fontweight='bold')

    plt.tight_layout(pad=0.5)
    out_png = OUT_DIR / "framework_flowchart.png"
    out_svg = OUT_DIR / "framework_flowchart.svg"
    fig.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(out_svg, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved {out_png}")
    print(f"  Saved {out_svg}")


if __name__ == "__main__":
    generate()
