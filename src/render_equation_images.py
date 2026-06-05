"""
Render all 13 model equations as high-resolution PNG images.

Uses matplotlib mathtext (no external LaTeX compiler required).
Output: figures/equations/eq_01.png through eq_13.png

Usage:
    python src/render_equation_images.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl


EQUATIONS = [
    (
        "eq_01",
        r"$S_{\mathrm{sem}}^{(i)} = 100 \cdot \mathrm{clip}\!\left(\, l_i - 0.20\, p_i \,\right)$",
        r"Semantic fidelity score $S_{\mathrm{sem}}$",
    ),
    (
        "eq_02",
        r"$S_{\mathrm{tech}}^{(i)} = 100 \cdot \left(0.65\, C_i + 0.35\, N_i\right)$",
        r"Technical quality score $S_{\mathrm{tech}}$",
    ),
    (
        "eq_03",
        r"$T(x) = \max\!\left(0,\ 1 - \frac{|x - \tilde{x}|}{c \cdot \mathrm{MAD} + \varepsilon}\right)$",
        r"Robustness transformation $T(x)$",
    ),
    (
        "eq_04",
        r"$S_{\mathrm{str}}^{(i)} = 100 \cdot \mathrm{clip}\!\left(\, 0.45\, v_{i1} + 0.15\, v_{i2} + 0.25\, I_i^{\mathrm{part}} + 0.15\, G_i \,\right)$",
        r"Structural integrity score $S_{\mathrm{str}}$",
    ),
    (
        "eq_05",
        r"$Q_{\mathrm{img}}^{(i)} = w_{\mathrm{sem}}\, S_{\mathrm{sem}}^{(i)} + w_{\mathrm{tech}}\, S_{\mathrm{tech}}^{(i)} + w_{\mathrm{str}}\, S_{\mathrm{str}}^{(i)}$",
        r"Composite image quality $Q_{\mathrm{img}}$",
    ),
    (
        "eq_06",
        r"$e_j = -\frac{1}{\ln m} \sum_{i=1}^{m} p_{ij} \ln\!\left(p_{ij} + \varepsilon\right)$",
        r"Information entropy $e_j$",
    ),
    (
        "eq_07",
        r"$w_j^{E} = \frac{1 - e_j}{\sum_{k=1}^{n}(1 - e_k)}$",
        r"Entropy weight $w_j^{E}$",
    ),
    (
        "eq_08",
        r"$w_j = \eta \cdot w_j^{\mathrm{AHP}} + (1 - \eta) \cdot w_j^{E}$",
        r"Combined weight $w_j$",
    ),
    (
        "eq_09",
        r"$C_i = \frac{D_i^{-}}{D_i^{+} + D_i^{-}}$",
        r"TOPSIS closeness coefficient $C_i$",
    ),
    (
        "eq_10",
        r"$z_t^{(k)} = \max\!\left(0,\ \frac{x_t^{(k)} - \mathrm{med}\!\left(x^{(k)}\right)}{1.4826 \cdot \mathrm{MAD}\!\left(x^{(k)}\right) + \varepsilon}\right)$",
        r"Robust z-score $z_t^{(k)}$",
    ),
    (
        "eq_11",
        r"$I_t = 0.22\, z_t^{(1)} + 0.18\, z_t^{(2)} + 0.10\, z_t^{(3)} + 0.08\, z_t^{(4)} + 0.14\, z_t^{(5)} + 0.08\, z_t^{(6)} + 0.20\, z_t^{(7)}$",
        r"Temporal instability score $I_t$",
    ),
    (
        "eq_12",
        r"$d_{ij} = \max\!\left(0,\ \theta_j - r_{ij}\right)$",
        r"Shortfall distance $d_{ij}$",
    ),
    (
        "eq_13",
        r"$P_{ig} = \sum_{j} w_j \cdot d_{ij} \cdot \max\!\left(m_{jg},\ 0\right)$",
        r"Group penalty score $P_{ig}$",
    ),
]


def render_equation(eq_id: str, latex: str, label: str, out_dir: str) -> str:
    """Render a single equation to PNG."""
    fig = plt.figure(figsize=(14, 2.5))
    fig.patch.set_alpha(0.0)

    fig.text(
        0.5, 0.55, latex,
        fontsize=22,
        ha="center", va="center",
        usetex=False,
    )

    fig.text(
        0.5, 0.10, label,
        fontsize=12,
        ha="center", va="center",
        color="#555555",
        usetex=False,
    )

    path = os.path.join(out_dir, f"{eq_id}.png")
    fig.savefig(path, dpi=300, bbox_inches="tight", transparent=True, pad_inches=0.3)
    plt.close(fig)
    return path


def main() -> int:
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures", "equations")
    os.makedirs(out_dir, exist_ok=True)

    rendered = []
    for eq_id, latex, label in EQUATIONS:
        path = render_equation(eq_id, latex, label, out_dir)
        size_kb = os.path.getsize(path) / 1024
        rendered.append((eq_id, size_kb))
        print(f"  {eq_id}.png  ({size_kb:.1f} KB)")

    print(f"\nRendered {len(rendered)} equations to {out_dir}")

    # Quick sanity check
    issues = []
    for eq_id, size_kb in rendered:
        if size_kb < 5:
            issues.append(f"{eq_id}.png suspiciously small ({size_kb:.1f} KB)")
        if size_kb > 100:
            issues.append(f"{eq_id}.png unusually large ({size_kb:.1f} KB)")

    if issues:
        print("Warnings:")
        for w in issues:
            print(f"  - {w}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
