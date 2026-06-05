"""
Generate horizontal 2-row snake flowchart for the paper.

Layout: 8 stages in a snake pattern
  Row 1 (left→right): 1 → 2 → 3 → 4
  Turn: 4 ↓ 5
  Row 2 (right→left): 5 → 6 → 7 → 8
  Feedback: 8 → 1 (left side curved arrow)

Outputs:
  figures/final/framework_flowchart_v2.png  (300 DPI)
  figures/final/framework_flowchart_v2.svg
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "figures" / "final"


def draw_box(ax, cx, cy, w, h, text, fc, ec='#444444', fontsize=9, lw=1.3):
    """Draw a rounded rectangle with centered multi-line text."""
    box = mpatches.FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.06",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2,
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', zorder=3, linespacing=1.4)


def draw_arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.5):
    """Draw a simple arrow."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, connectionstyle='arc3,rad=0'),
                zorder=1)


def draw_turn_arrow(ax, x, y_top, y_bot, bw, color='#666666'):
    """Draw a vertical turn arrow on the right side connecting row 1 to row 2."""
    x_right = x + bw / 2 + 0.05
    ax.annotate('', xy=(x_right, y_bot + 0.55), xytext=(x_right, y_top - 0.55),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5,
                                connectionstyle='arc3,rad=0'),
                zorder=1)


def draw_sub_labels(ax, cx, cy, items, fontsize=7):
    """Draw small italic sub-items below a box."""
    n = len(items)
    total_w = 1.8
    gap = total_w / n
    for i, item in enumerate(items):
        xi = cx - total_w / 2 + gap / 2 + i * gap
        ax.text(xi, cy, item, ha='center', va='center', fontsize=fontsize,
                color='#444444', style='italic', zorder=3)


def generate():
    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(0.5, 9.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Layout constants
    bw = 2.3        # box width
    bh = 1.05       # box height
    y_top = 7.5     # top row center y
    y_bot = 3.5     # bottom row center y
    xs = [1.2, 3.8, 6.4, 9.0]  # x positions for 4 columns

    # Color palette (muted academic)
    colors = {
        1: '#E8F0FE',  # light blue
        2: '#D6E4F0',  # steel blue
        3: '#FFF3CD',  # warm yellow
        4: '#D4EDDA',  # light green
        5: '#C3E6CB',  # green
        6: '#F5C6CB',  # light pink
        7: '#E2D9F3',  # light purple
        8: '#FFE0B2',  # light orange
    }
    ec = '#444444'

    # Stage labels
    labels = {
        1: '1. 题目输入',
        2: '2. 图像/视频\n    预处理',
        3: '3. 图像三维评价',
        4: '4. 组合赋权与\n  TOPSIS排序',
        5: '5. 稳健性验证',
        6: '6. 视频时序检测',
        7: '7. 短板诊断',
        8: '8. 参数优化建议',
    }

    # === Row 1: stages 1→4 (left to right) ===
    for i, x in enumerate(xs):
        stage = i + 1
        draw_box(ax, x, y_top, bw, bh, labels[stage],
                 colors[stage], ec, fontsize=10)

    # Horizontal arrows row 1
    for i in range(3):
        x1 = xs[i] + bw / 2
        x2 = xs[i + 1] - bw / 2
        draw_arrow(ax, x1, y_top, x2, y_top)

    # === Row 2: stages 5→8 (right to left) ===
    for i, x in enumerate(xs):
        stage = 8 - i  # reverse order: 8,7,6,5
        draw_box(ax, x, y_bot, bw, bh, labels[stage],
                 colors[stage], ec, fontsize=10)

    # Horizontal arrows row 2 (right to left)
    for i in range(3):
        x1 = xs[3 - i] - bw / 2
        x2 = xs[2 - i] + bw / 2
        draw_arrow(ax, x1, y_bot, x2, y_bot)

    # === Turn arrow: stage 4 → stage 5 (right side, going down) ===
    draw_turn_arrow(ax, xs[3], y_top, y_bot, bw, color='#666666')

    # === Sub-labels ===
    # Stage 3 sub-dimensions
    sub_y3 = y_top - bh / 2 - 0.28
    draw_sub_labels(ax, xs[2], sub_y3, ['语义保真度', '技术质量', '结构完整性'], fontsize=7.5)

    # Stage 6 sub-methods
    sub_y6 = y_bot - bh / 2 - 0.28
    draw_sub_labels(ax, xs[1], sub_y6, ['SSIM', '光流', 'Warp-SSIM'], fontsize=7.5)

    # === Feedback arrow: stage 8 → stage 1 (left side, curved) ===
    x_left = xs[0] - bw / 2 - 0.05
    ax.annotate(
        '', xy=(x_left, y_top - 0.55),
        xytext=(x_left, y_bot + 0.55),
        arrowprops=dict(
            arrowstyle='->', color='#888888', lw=1.3,
            connectionstyle='arc3,rad=0.35',
        ),
        zorder=1,
    )
    ax.text(x_left - 0.22, (y_top + y_bot) / 2, '迭代\n反馈',
            ha='center', va='center', fontsize=7.5, color='#666666',
            style='italic')

    # === Title ===
    ax.text(5.5, 9.2, 'AIGC图像/视频质量评估与参数优化方法论流程图',
            ha='center', va='center', fontsize=13, fontweight='bold')

    # === Row labels ===
    ax.text(-0.3, y_top, '图像质量\n评价', ha='center', va='center',
            fontsize=8, color='#888888', style='italic')
    ax.text(-0.3, y_bot, '视频质量\n评价与优化', ha='center', va='center',
            fontsize=8, color='#888888', style='italic')

    plt.tight_layout(pad=0.3)

    out_png = OUT_DIR / "framework_flowchart_v2.png"
    out_svg = OUT_DIR / "framework_flowchart_v2.svg"
    fig.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(out_svg, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved {out_png}")
    print(f"  Saved {out_svg}")


if __name__ == "__main__":
    generate()
