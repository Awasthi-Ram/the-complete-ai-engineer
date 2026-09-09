"""
generate_textbook_diagrams.py — Generates publication-grade architectural and mathematical
diagrams for 'The Complete AI Engineer' textbook using matplotlib and Pillow.
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Styling parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['mathtext.fontset'] = 'dejavusans'

NAVY = '#0d1b2a'
BLUE = '#1b4965'
CYAN = '#5fa8d3'
LIGHT_BG = '#f8f9fa'
TEAL = '#2a9d8f'
ORANGE = '#e76f51'
RED = '#e63946'
GOLD = '#e9c46a'
BORDER = '#d0d7de'

def save_fig(fig, filename):
    filepath = os.path.join('.', filename)
    fig.savefig(filepath, dpi=250, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  [SAVED] {filename}")

print("Generating publication-grade textbook diagrams...")

# -------------------------------------------------------------
# 1. Roofline Model & GPU Memory Hierarchy (Chapter 0.1)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw={'width_ratios': [1, 1.2]})

# Left: Memory Hierarchy Pyramid
levels = [
    ("Registers & SRAM", "~1 ns", "~33 TB/s", 0.9, '#e76f51'),
    ("GPU L2 Cache", "5-10 ns", "6-8 TB/s", 0.75, '#f4a261'),
    ("HBM3 / VRAM", "20-40 ns", "3.35 TB/s", 0.60, '#2a9d8f'),
    ("PCIe Gen5 x16", "100-200 ns", "64 GB/s", 0.45, '#5fa8d3'),
    ("Host CPU RAM", "80-120 ns", "50-100 GB/s", 0.30, '#1b4965'),
    ("NVMe SSD", "10,000 ns", "4-7 GB/s", 0.15, '#0d1b2a')
]
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-0.8, 6.2)
ax1.axis('off')
ax1.set_title("GPU Memory & Latency Hierarchy", fontsize=12, fontweight='bold', color=NAVY, pad=12)

for i, (name, lat, bw, width, col) in enumerate(levels):
    y = 5 - i
    rect = patches.FancyBboxPatch((-width, y-0.35), width*2, 0.7, boxstyle="round,pad=0.04",
                                  facecolor=col, edgecolor='none', alpha=0.9)
    ax1.add_patch(rect)
    text_col = 'white' if col not in ['#f4a261', '#e9c46a'] else NAVY
    ax1.text(0, y, f"{name}\n({lat} | {bw})", ha='center', va='center',
             color=text_col, fontsize=8.5, fontweight='bold', linespacing=1.2)

# Right: Roofline Curve
ax2.set_title("The Roofline Model: Arithmetic Intensity", fontsize=12, fontweight='bold', color=NAVY, pad=12)
I = np.logspace(-1, 3, 300)
P_peak = 1000 # TFLOPs
B_peak = 3.35 # TB/s -> I* = 1000/3.35 ≈ 298.5
I_star = 150 # illustrative
P = np.minimum(P_peak, B_peak * 6.7 * I)

ax2.loglog(I, P, color=BLUE, lw=3, label="Performance Ceiling")
ax2.axvline(I_star, color=ORANGE, linestyle='--', lw=2, label=f"Machine Balance $I^* = P_{{peak}}/B_{{peak}}$")
ax2.axhline(P_peak, color='gray', linestyle=':', lw=1.5)

# Fill zones
ax2.fill_between(I[I <= I_star], 1, P[I <= I_star], color=CYAN, alpha=0.2, label="Memory-Bound Zone")
ax2.fill_between(I[I > I_star], 1, P[I > I_star], color=TEAL, alpha=0.2, label="Compute-Bound Zone")

ax2.text(10, 80, "MEMORY-BOUND\n(Softmax, LayerNorm,\nLLM Decode Batch=1)", fontsize=8.5,
         color=BLUE, fontweight='bold', ha='center', bbox=dict(boxstyle="round,pad=0.3", fc='white', ec=CYAN))
ax2.text(450, 400, "COMPUTE-BOUND\n(GEMM Matrix Mult,\nPre-fill / Training)", fontsize=8.5,
         color=TEAL, fontweight='bold', ha='center', bbox=dict(boxstyle="round,pad=0.3", fc='white', ec=TEAL))

ax2.set_xlabel(r"Arithmetic Intensity $I$ [FLOPs / Byte]", fontsize=10, fontweight='bold', color=NAVY)
ax2.set_ylabel(r"Attainable Performance [TFLOPs/sec]", fontsize=10, fontweight='bold', color=NAVY)
ax2.grid(True, which="both", ls="--", color=BORDER, alpha=0.6)
ax2.legend(loc='lower right', fontsize=8.5, framealpha=0.9)

save_fig(fig, "roofline_model_diagram.png")

# -------------------------------------------------------------
# 2. NumPy Strided Arrays & Memory Layout (Chapter 0.3)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.set_xlim(-0.5, 9.5)
ax.set_ylim(-1.5, 3.5)
ax.axis('off')
ax.set_title("NumPy Strided Arrays: 1D Contiguous Buffer to 2D Tensor View", fontsize=12, fontweight='bold', color=NAVY)

# 1D buffer
ax.text(0, 2.5, "1D Physical RAM Buffer (Contiguous Bytes in Memory):", fontsize=9.5, fontweight='bold', color=NAVY)
for i in range(6):
    rect = patches.Rectangle((i*1.4, 1.4), 1.2, 0.7, facecolor=CYAN, edgecolor=BLUE, lw=1.5)
    ax.add_patch(rect)
    ax.text(i*1.4 + 0.6, 1.75, f"[{i}]\n{i*10}", ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY)
    ax.text(i*1.4 + 0.6, 1.15, f"Byte {i*4}", ha='center', va='center', fontsize=7.5, color='#666')

# 2D view mapping
ax.text(0, 0.3, "2D Logical View: Shape (2, 3), Strides (12, 4) bytes (Row-Major):", fontsize=9.5, fontweight='bold', color=NAVY)
matrix = [[0, 1, 2], [3, 4, 5]]
for r in range(2):
    for c in range(3):
        val = matrix[r][c]
        rect = patches.Rectangle((c*1.4, -0.6 - r*0.7), 1.2, 0.6, facecolor=TEAL if r==0 else ORANGE,
                                 edgecolor=NAVY, lw=1.5, alpha=0.85)
        ax.add_patch(rect)
        ax.text(c*1.4 + 0.6, -0.3 - r*0.7, f"[{r},{c}] = {val*10}", ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white')

ax.text(5.0, -0.6, "Stride 0: jump 12 bytes to next row\nStride 1: jump 4 bytes to next col\nZero-Copy Transpose: swap strides to (4, 12)!",
        fontsize=9, color=NAVY, bbox=dict(boxstyle="round,pad=0.5", fc=LIGHT_BG, ec=BORDER), linespacing=1.4)

save_fig(fig, "numpy_strides_diagram.png")

# -------------------------------------------------------------
# 3. SVD Geometric Transformation (Chapter 1.1)
# -------------------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(11, 3.8))
fig.suptitle(r"Singular Value Decomposition (SVD): $\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$",
             fontsize=13, fontweight='bold', color=NAVY, y=1.03)

theta = np.linspace(0, 2*np.pi, 200)
circle_x, circle_y = np.cos(theta), np.sin(theta)

# Stage 1: Unit Circle with basis vectors
axs[0].plot(circle_x, circle_y, color=BLUE, lw=2)
axs[0].quiver([0, 0], [0, 0], [1, 0], [0, 1], angles='xy', scale_units='xy', scale=1, color=[ORANGE, TEAL], width=0.03)
axs[0].set_title(r"1. Unit Sphere in $\mathbb{R}^n$", fontsize=10.5, fontweight='bold', color=NAVY)
axs[0].text(0.7, 0.15, r"$\mathbf{v}_1$", color=ORANGE, fontweight='bold', fontsize=11)
axs[0].text(0.15, 0.7, r"$\mathbf{v}_2$", color=TEAL, fontweight='bold', fontsize=11)
axs[0].set_xlim(-1.5, 1.5); axs[0].set_ylim(-1.5, 1.5); axs[0].set_aspect('equal')
axs[0].grid(True, ls=":", color=BORDER)

# Stage 2: Scaling by Sigma
sigma1, sigma2 = 2.0, 0.8
ellipse_x, ellipse_y = sigma1 * circle_x, sigma2 * circle_y
axs[1].plot(ellipse_x, ellipse_y, color=BLUE, lw=2)
axs[1].quiver([0, 0], [0, 0], [sigma1, 0], [0, sigma2], angles='xy', scale_units='xy', scale=1, color=[ORANGE, TEAL], width=0.03)
axs[1].set_title(r"2. Stretch by $\mathbf{\Sigma}$ ($\sigma_1, \sigma_2$)", fontsize=10.5, fontweight='bold', color=NAVY)
axs[1].text(1.3, 0.15, r"$\sigma_1$", color=ORANGE, fontweight='bold', fontsize=11)
axs[1].text(0.15, 0.5, r"$\sigma_2$", color=TEAL, fontweight='bold', fontsize=11)
axs[1].set_xlim(-2.5, 2.5); axs[1].set_ylim(-2.5, 2.5); axs[1].set_aspect('equal')
axs[1].grid(True, ls=":", color=BORDER)

# Stage 3: Rotation by U
phi = np.pi / 6 # 30 deg
R = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
rot_coords = R @ np.vstack([ellipse_x, ellipse_y])
u1 = R @ np.array([sigma1, 0])
u2 = R @ np.array([0, sigma2])

axs[2].plot(rot_coords[0], rot_coords[1], color=BLUE, lw=2)
axs[2].quiver([0, 0], [0, 0], [u1[0], u2[0]], [u1[1], u2[1]], angles='xy', scale_units='xy', scale=1, color=[ORANGE, TEAL], width=0.03)
axs[2].set_title(r"3. Rotate by $\mathbf{U}$ into $\mathbb{R}^m$", fontsize=10.5, fontweight='bold', color=NAVY)
axs[2].text(u1[0]*0.7, u1[1]*0.7 + 0.2, r"$\sigma_1 \mathbf{u}_1$", color=ORANGE, fontweight='bold', fontsize=11)
axs[2].text(u2[0]*0.7 - 0.5, u2[1]*0.7, r"$\sigma_2 \mathbf{u}_2$", color=TEAL, fontweight='bold', fontsize=11)
axs[2].set_xlim(-2.5, 2.5); axs[2].set_ylim(-2.5, 2.5); axs[2].set_aspect('equal')
axs[2].grid(True, ls=":", color=BORDER)

save_fig(fig, "svd_geometry_diagram.png")

# -------------------------------------------------------------
# 4. Computational DAG & Reverse-Mode Autograd (Chapter 1.2)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title("Automatic Differentiation: Forward Evaluation vs Reverse VJP Backprop", fontsize=12, fontweight='bold', color=NAVY)

nodes = {
    'x': (1.5, 3.5, "$x=2$"),
    'y': (1.5, 1.5, "$y=3$"),
    'z': (4.5, 2.5, "$z = x \\cdot y$\n$= 6$"),
    'a': (7.0, 2.5, "$a = \\ln(z)$\n$\\approx 1.79$"),
    'L': (9.0, 2.5, "Loss $L$\n$= a$")
}

for name, (nx, ny, label) in nodes.items():
    circle = patches.FancyBboxPatch((nx-0.6, ny-0.45), 1.2, 0.9, boxstyle="round,pad=0.08",
                                    facecolor=LIGHT_BG, edgecolor=BLUE, lw=2)
    ax.add_patch(circle)
    ax.text(nx, ny, label, ha='center', va='center', fontsize=9.5, fontweight='bold', color=NAVY)

# Forward arrows
def draw_arrow(p1, p2, col, text, offset_y=0.25):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", color=col, lw=2))
    mid = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2 + offset_y)
    ax.text(mid[0], mid[1], text, fontsize=8, color=col, fontweight='bold', ha='center')

draw_arrow((2.2, 3.5), (3.8, 2.7), BLUE, "Forward", 0.2)
draw_arrow((2.2, 1.5), (3.8, 2.3), BLUE, "Forward", -0.3)
draw_arrow((5.2, 2.5), (6.3, 2.5), BLUE, "Forward", 0.25)
draw_arrow((7.7, 2.5), (8.3, 2.5), BLUE, "Forward", 0.25)

# Reverse VJP adjoint arrows (dashed red)
def draw_rev(p1, p2, text, offset_y=-0.35):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", color=RED, lw=2, ls="--"))
    mid = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2 + offset_y)
    ax.text(mid[0], mid[1], text, fontsize=8, color=RED, fontweight='bold', ha='center')

draw_rev((8.3, 2.3), (7.7, 2.3), r"$\bar{L}=1$")
draw_rev((6.3, 2.3), (5.2, 2.3), r"$\bar{a} \cdot \frac{1}{z} = \frac{1}{6}$")
draw_rev((3.8, 2.1), (2.2, 1.3), r"$\bar{z} \cdot x = \frac{2}{6}$", -0.25)
draw_rev((3.8, 2.9), (2.2, 3.7), r"$\bar{z} \cdot y = \frac{3}{6}$", 0.25)

ax.text(5.0, 0.3, "Reverse Mode: One single backward pass computes gradients with respect to ALL inputs simultaneously!",
        fontsize=9, color=NAVY, ha='center', bbox=dict(boxstyle="round,pad=0.4", fc='white', ec=BORDER))

save_fig(fig, "autograd_dag_diagram.png")

# -------------------------------------------------------------
# 5. Optimization Landscapes & Momentum (Chapter 1.5)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.5))
x = np.linspace(-3, 3, 200)
y = np.linspace(-2, 2, 200)
X, Y = np.meshgrid(x, y)
Z = 5 * X**2 + 0.5 * Y**2 # Ill-conditioned ravine

ax.contour(X, Y, Z, levels=[0.2, 1, 3, 7, 13, 22, 35], colors=BORDER, linewidths=1.2)
ax.set_title("Optimization Dynamics in Ill-Conditioned Ravines (Condition Number $\kappa \gg 1$)",
             fontsize=12, fontweight='bold', color=NAVY)

# Standard SGD (oscillating violently)
sgd_x = [2.5, -1.8, 1.3, -0.9, 0.6, -0.4, 0.2]
sgd_y = [1.8, 1.5, 1.2, 0.9, 0.7, 0.5, 0.3]
ax.plot(sgd_x, sgd_y, 'o--', color=RED, lw=1.8, label="Standard SGD (Severe Orthogonal Oscillations)")

# Momentum (smooth acceleration down valley)
mom_x = [2.5, 1.5, 0.5, 0.0, -0.1, 0.0]
mom_y = [1.8, 1.3, 0.8, 0.4, 0.1, 0.0]
ax.plot(mom_x, mom_y, 's-', color=TEAL, lw=2.5, label=r"Momentum $\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \alpha \nabla L$ (Damped Oscillations)")

# Minimum
ax.plot(0, 0, '*', color=GOLD, markersize=14, markeredgecolor=NAVY, label="Global Minimum $(0, 0)$")

ax.set_xlabel(r"Parameter $\theta_1$ (Steep Curvature $\lambda_{\max}$)", fontsize=10, fontweight='bold', color=NAVY)
ax.set_ylabel(r"Parameter $\theta_2$ (Flat Curvature $\lambda_{\min}$)", fontsize=10, fontweight='bold', color=NAVY)
ax.legend(loc='upper right', fontsize=8.5, framealpha=0.95)
ax.grid(True, ls=":", color=BORDER, alpha=0.5)

save_fig(fig, "optimization_ravine_diagram.png")

# -------------------------------------------------------------
# 6. SVM Maximum Margin & Kernel Trick (Chapter 2.6)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

# Left: 2D Maximum Margin Hyperplane
np.random.seed(42)
c1 = np.random.randn(15, 2)*0.4 + [1, 2]
c2 = np.random.randn(15, 2)*0.4 + [2.8, 0.8]
ax1.scatter(c1[:, 0], c1[:, 1], color=BLUE, label="Class +1", s=50, edgecolors=NAVY)
ax1.scatter(c2[:, 0], c2[:, 1], color=ORANGE, label="Class -1", s=50, edgecolors=NAVY)

lx = np.linspace(0.5, 3.5, 100)
# w·x + b = 0
ax1.plot(lx, -lx + 3.4, color=NAVY, lw=2.5, label=r"Hyperplane $\mathbf{w}^T \mathbf{x} + b = 0$")
ax1.plot(lx, -lx + 3.9, 'k--', lw=1.2, label=r"Margin $\mathbf{w}^T \mathbf{x} + b = +1$")
ax1.plot(lx, -lx + 2.9, 'k--', lw=1.2, label=r"Margin $\mathbf{w}^T \mathbf{x} + b = -1$")

# Circle support vectors
ax1.scatter([1.3, 1.8], [2.1, 1.6], s=120, facecolors='none', edgecolors=RED, lw=2, label="Support Vectors")
ax1.scatter([2.4, 2.0], [1.0, 1.4], s=120, facecolors='none', edgecolors=RED, lw=2)

ax1.set_title(r"Linear SVM: Maximum Margin $\frac{2}{\|\mathbf{w}\|_2}$", fontsize=11, fontweight='bold', color=NAVY)
ax1.legend(loc='lower left', fontsize=8)
ax1.grid(True, ls=":", color=BORDER)

# Right: Kernel Trick (Non-linear projection)
theta = np.linspace(0, 2*np.pi, 30)
inner_r = np.random.uniform(0.1, 0.6, 20)
inner_theta = np.random.uniform(0, 2*np.pi, 20)
in_x, in_y = inner_r*np.cos(inner_theta), inner_r*np.sin(inner_theta)

outer_r = np.random.uniform(1.2, 1.8, 30)
outer_theta = np.random.uniform(0, 2*np.pi, 30)
out_x, out_y = outer_r*np.cos(outer_theta), outer_r*np.sin(outer_theta)

ax2.scatter(in_x, in_y, color=BLUE, label="Class +1 (Inner)", s=45)
ax2.scatter(out_x, out_y, color=ORANGE, label="Class -1 (Ring)", s=45)
ax2.add_patch(patches.Circle((0, 0), 0.9, fill=False, edgecolor=RED, lw=2, ls='--', label=r"Non-Linear Boundary in 2D"))

ax2.set_title(r"Kernel Trick: $\phi(\mathbf{x}) \rightarrow$ Separable in $\mathbb{R}^3$", fontsize=11, fontweight='bold', color=NAVY)
ax2.set_xlim(-2.2, 2.2); ax2.set_ylim(-2.2, 2.2)
ax2.legend(loc='lower right', fontsize=8)
ax2.grid(True, ls=":", color=BORDER)

save_fig(fig, "svm_margin_kernel_diagram.png")

# -------------------------------------------------------------
# 7. XOR Linear Separability & Manifold Folding (Chapter 3.1)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

# 2D Input Space (Impossible to linearly separate)
ax1.scatter([0, 1], [0, 1], color=ORANGE, s=120, edgecolors=NAVY, zorder=5, label="XOR Output = 0")
ax1.scatter([0, 1], [1, 0], color=BLUE, s=120, edgecolors=NAVY, zorder=5, label="XOR Output = 1")
ax1.set_xlim(-0.4, 1.4); ax1.set_ylim(-0.4, 1.4)
ax1.axhline(0, color='gray', lw=1); ax1.axvline(0, color='gray', lw=1)
ax1.set_title("Input Space $(x_1, x_2)$: Non-Linearly Separable", fontsize=10.5, fontweight='bold', color=NAVY)
ax1.text(0.5, 0.5, "NO single linear hyperplane\ncan separate classes!", color=RED, fontweight='bold',
         ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", fc='#ffebee', ec=RED))
ax1.grid(True, ls=":", color=BORDER)
ax1.legend(loc='upper right', fontsize=8.5)

# Hidden Space (Linearly Separable after ReLU)
# Let h1 = ReLU(x1 + x2 - 0.5), h2 = ReLU(x1 + x2 - 1.5)
# (0,0) -> (0,0) [Output 0]
# (1,0) -> (0.5, 0) [Output 1]
# (0,1) -> (0.5, 0) [Output 1]
# (1,1) -> (1.5, 0.5) [Output 0]
ax2.scatter([0, 1.5], [0, 0.5], color=ORANGE, s=120, edgecolors=NAVY, zorder=5, label="Output = 0")
ax2.scatter([0.5], [0], color=BLUE, s=160, edgecolors=NAVY, zorder=5, label="Output = 1 (Collapsed)")
ax2.plot([-0.2, 1.2], [0.3, -0.1], color=TEAL, lw=2.5, label="Linear Separator in Hidden Space!")
ax2.set_xlim(-0.4, 1.8); ax2.set_ylim(-0.3, 0.8)
ax2.set_title("Hidden Space $(h_1, h_2)$: Linearly Separable!", fontsize=10.5, fontweight='bold', color=NAVY)
ax2.text(0.5, 0.4, "Hidden layer folds manifold:\nPoints are linearly separable", color=TEAL, fontweight='bold',
         fontsize=8.5, ha='center', bbox=dict(boxstyle="round,pad=0.3", fc='#e8f5e9', ec=TEAL))
ax2.grid(True, ls=":", color=BORDER)
ax2.legend(loc='lower right', fontsize=8.5)

save_fig(fig, "xor_linear_separability_diagram.png")

# -------------------------------------------------------------
# 8. Analytical Backprop Tensor Dimension Flow (Chapter 3.3)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.2)
ax.axis('off')
ax.set_title(r"2-Layer MLP Backpropagation: Matrix Dimensions & Gradient Transposition", fontsize=12, fontweight='bold', color=NAVY)

boxes = [
    (0.8, 3.8, r"$\mathbf{X}$" + "\n" + r"$[B \times d_{in}]$", CYAN),
    (2.8, 3.8, r"$\mathbf{Z}_1 = \mathbf{X}\mathbf{W}_1 + \mathbf{b}_1$" + "\n" + r"$[B \times d_h]$", LIGHT_BG),
    (5.2, 3.8, r"$\mathbf{A}_1 = \sigma(\mathbf{Z}_1)$" + "\n" + r"$[B \times d_h]$", LIGHT_BG),
    (7.5, 3.8, r"$\mathbf{Z}_2 = \mathbf{A}_1\mathbf{W}_2 + \mathbf{b}_2$" + "\n" + r"$[B \times C]$", LIGHT_BG),
    (9.6, 3.8, r"$\hat{\mathbf{Y}}, \mathcal{L}$" + "\n" + r"$[B \times C]$", GOLD)
]

for xpos, ypos, text, bg in boxes:
    rect = patches.FancyBboxPatch((xpos-0.7, ypos-0.5), 1.4, 1.0, boxstyle="round,pad=0.06",
                                  fc=bg, ec=BLUE, lw=1.5)
    ax.add_patch(rect)
    ax.text(xpos, ypos, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)

# Forward arrows
for x1, x2 in [(1.5, 2.1), (3.5, 4.5), (5.9, 6.8), (8.2, 8.9)]:
    ax.annotate("", xy=(x2, 3.8), xytext=(x1, 3.8), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))

# Backward gradient arrows
grad_boxes = [
    (9.6, 1.4, r"$\mathbf{\delta}_2 = \hat{\mathbf{Y}} - \mathbf{Y}$" + "\n" + r"$[B \times C]$", RED),
    (7.5, 1.4, r"$\frac{\partial \mathcal{L}}{\partial \mathbf{W}_2} = \mathbf{A}_1^T \mathbf{\delta}_2$" + "\n" + r"$[d_h \times C]$", ORANGE),
    (4.8, 1.4, r"$\mathbf{\delta}_1 = (\mathbf{\delta}_2 \mathbf{W}_2^T) \odot \sigma'(\mathbf{Z}_1)$" + "\n" + r"$[B \times d_h]$", RED),
    (1.8, 1.4, r"$\frac{\partial \mathcal{L}}{\partial \mathbf{W}_1} = \mathbf{X}^T \mathbf{\delta}_1$" + "\n" + r"$[d_{in} \times d_h]$", ORANGE)
]

for xpos, ypos, text, col in grad_boxes:
    rect = patches.FancyBboxPatch((xpos-0.9, ypos-0.5), 1.8, 1.0, boxstyle="round,pad=0.06",
                                  fc='white', ec=col, lw=2)
    ax.add_patch(rect)
    ax.text(xpos, ypos, text, ha='center', va='center', fontsize=8.2, fontweight='bold', color=col)

for x1, x2 in [(8.7, 8.4), (6.6, 5.7), (3.9, 2.7)]:
    ax.annotate("", xy=(x2, 1.4), xytext=(x1, 1.4), arrowprops=dict(arrowstyle="->", color=RED, lw=2, ls="--"))

save_fig(fig, "backprop_matrix_flow_diagram.png")

# -------------------------------------------------------------
# 9. Normalization Cubes (Chapter 3.5)
# -------------------------------------------------------------
fig, axs = plt.subplots(1, 4, figsize=(11, 3.4))
norms = [
    ("Batch Norm", "Normalizes across Batch (N)\nIndependent per Channel", TEAL),
    ("Layer Norm", "Normalizes across Channels & Spatial (C, L)\nIndependent per Sample (N)", BLUE),
    ("Instance Norm", "Normalizes across Spatial (L)\nIndependent per Sample & Channel", ORANGE),
    ("Group Norm", "Normalizes across Groups of Channels\nIndependent per Sample (N)", CYAN)
]

for i, (title, desc, col) in enumerate(norms):
    ax = axs[i]
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_title(title, fontsize=10.5, fontweight='bold', color=NAVY)
    
    # Draw isometric 3D cube
    p = patches.Rectangle((0.6, 0.6), 2.2, 2.2, fc=LIGHT_BG, ec=BORDER, lw=1.5)
    ax.add_patch(p)
    
    # Highlight slices
    if i == 0: # BatchNorm: slice across N
        p_act = patches.Rectangle((0.6, 0.6), 0.7, 2.2, fc=col, alpha=0.7, ec=NAVY, lw=1.5)
    elif i == 1: # LayerNorm: slice across C
        p_act = patches.Rectangle((0.6, 1.5), 2.2, 0.6, fc=col, alpha=0.7, ec=NAVY, lw=1.5)
    elif i == 2: # InstanceNorm
        p_act = patches.Rectangle((0.8, 1.5), 0.8, 0.6, fc=col, alpha=0.7, ec=NAVY, lw=1.5)
    else: # GroupNorm
        p_act = patches.Rectangle((0.6, 1.2), 2.2, 1.1, fc=col, alpha=0.7, ec=NAVY, lw=1.5)
    ax.add_patch(p_act)
    
    ax.text(2.0, 0.15, desc, ha='center', va='top', fontsize=7.5, color=NAVY, linespacing=1.2)

save_fig(fig, "normalization_cubes_diagram.png")

# -------------------------------------------------------------
# 10. ResNet Residual Block & Gradient Highway (Chapter 4.1)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title(r"ResNet Residual Block: Skip Connection Creates an Unobstructed Gradient Highway",
             fontsize=12, fontweight='bold', color=NAVY)

# Main Conv branch
blocks = [
    (2.0, 2.5, "Input\n" + r"$\mathbf{x}$", CYAN),
    (4.0, 2.5, "Weight Layer\n(Conv 3x3)", LIGHT_BG),
    (5.8, 2.5, "Weight Layer\n(Conv 3x3)", LIGHT_BG),
    (7.8, 2.5, r"$\oplus$" + "\nAddition", GOLD),
    (9.2, 2.5, "Output\n" + r"$\mathrm{ReLU}(\mathcal{F}(\mathbf{x}) + \mathbf{x})$", TEAL)
]

for xpos, ypos, text, bg in blocks:
    shape = "round,pad=0.08" if "Input" in text or "Output" in text else "square,pad=0.1"
    rect = patches.FancyBboxPatch((xpos-0.6, ypos-0.45), 1.2, 0.9, boxstyle=shape, fc=bg, ec=BLUE, lw=1.8)
    ax.add_patch(rect)
    ax.text(xpos, ypos, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)

# Main branch arrows
for x1, x2 in [(2.6, 3.4), (4.6, 5.2), (6.4, 7.2), (8.4, 8.6)]:
    ax.annotate("", xy=(x2, 2.5), xytext=(x1, 2.5), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))

# Residual Skip Connection (curved top arc)
arc = patches.Arc((4.9, 2.8), 5.8, 2.2, angle=0, theta1=20, theta2=160, color=ORANGE, lw=3, ls="--")
ax.add_patch(arc)
ax.annotate("", xy=(7.8, 3.0), xytext=(7.5, 3.3), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=3))
ax.text(4.9, 4.2, r"Identity Shortcut Connection $\mathbf{x}$ (Gradient Highway: $\frac{\partial \mathcal{L}}{\partial \mathbf{x}} = \frac{\partial \mathcal{L}}{\partial \mathbf{y}} \cdot \frac{\partial \mathcal{F}}{\partial \mathbf{x}} + \frac{\partial \mathcal{L}}{\partial \mathbf{y}} \cdot \mathbf{I}$)",
        ha='center', fontsize=8.8, color=ORANGE, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc='white', ec=ORANGE))

save_fig(fig, "resnet_block_diagram.png")

# -------------------------------------------------------------
# 11. U-Net Medical Segmentation Architecture (Chapter 4.2)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title("U-Net Architecture: Contracting Encoder, Bottleneck & Skip Concatenations",
             fontsize=12, fontweight='bold', color=NAVY)

# Encoder blocks (descending left)
enc_layers = [(1.2, 4.0, "572x572\n64 ch"), (2.2, 3.0, "284x284\n128 ch"), (3.2, 2.0, "140x140\n256 ch")]
for xpos, ypos, text in enc_layers:
    rect = patches.Rectangle((xpos-0.4, ypos-0.4), 0.8, 0.8, fc=CYAN, ec=BLUE, lw=1.5)
    ax.add_patch(rect)
    ax.text(xpos, ypos, text, ha='center', va='center', fontsize=7.5, color=NAVY, fontweight='bold')

# Bottleneck
rect = patches.Rectangle((4.6, 0.6), 0.8, 0.8, fc=NAVY, ec=BLUE, lw=2)
ax.add_patch(rect)
ax.text(5.0, 1.0, "Bottleneck\n28x28 | 1024 ch", ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

# Decoder blocks (ascending right)
dec_layers = [(6.8, 2.0, "UpConv\n256 ch"), (7.8, 3.0, "UpConv\n128 ch"), (8.8, 4.0, "Output Map\n388x388 | 2 ch")]
for xpos, ypos, text in dec_layers:
    rect = patches.Rectangle((xpos-0.4, ypos-0.4), 0.8, 0.8, fc=TEAL, ec=BLUE, lw=1.5)
    ax.add_patch(rect)
    ax.text(xpos, ypos, text, ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

# Skip connections (horizontal dashed lines)
for (x1, y1, _), (x2, y2, _) in zip(enc_layers, dec_layers):
    ax.annotate("", xy=(x2-0.4, y2), xytext=(x1+0.4, y1),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2, ls="--"))
    ax.text((x1+x2)/2, y1+0.2, "Skip Connection (Copy & Crop)", color=ORANGE, fontsize=7.5, ha='center', fontweight='bold')

save_fig(fig, "unet_architecture_diagram.png")

# -------------------------------------------------------------
# 12. Diffusion Models: Forward & Reverse SDE (Chapter 4.4)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')
ax.set_title("Diffusion Process: Forward Markov Noise Schedule vs Reverse Neural Denoising",
             fontsize=12, fontweight='bold', color=NAVY)

steps = [
    (1.2, 2.0, r"$\mathbf{x}_0$" + "\nClean Image", TEAL),
    (3.4, 2.0, r"$\mathbf{x}_t$" + "\nPartially Noisy", CYAN),
    (5.8, 2.0, r"$\mathbf{x}_{T-1}$" + "\nHeavy Noise", ORANGE),
    (8.2, 2.0, r"$\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$" + "\nPure Gaussian", RED)
]

for xpos, ypos, text, col in steps:
    rect = patches.FancyBboxPatch((xpos-0.8, ypos-0.5), 1.6, 1.0, boxstyle="round,pad=0.08", fc=col, ec=NAVY, lw=1.8)
    ax.add_patch(rect)
    ax.text(xpos, ypos, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

# Forward arrows (top)
ax.annotate("", xy=(7.4, 2.7), xytext=(2.0, 2.7), arrowprops=dict(arrowstyle="->", color=RED, lw=2.5))
ax.text(4.7, 3.0, r"Forward Diffusion $q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t \mathbf{I})$",
        ha='center', fontsize=9, color=RED, fontweight='bold')

# Reverse arrows (bottom)
ax.annotate("", xy=(2.0, 1.3), xytext=(7.4, 1.3), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.5))
ax.text(4.7, 0.85, r"Reverse Denoising $p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)$ guided by $\mathbf{\epsilon}_\theta(\mathbf{x}_t, t)$",
        ha='center', fontsize=9, color=TEAL, fontweight='bold')

save_fig(fig, "diffusion_process_diagram.png")

# -------------------------------------------------------------
# 13. Vision Transformer (ViT) Architecture (Chapter 4.5)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title("Vision Transformer (ViT): Patch Embedding, Positional Encoding & Encoder Blocks",
             fontsize=12, fontweight='bold', color=NAVY)

# Image patches
ax.text(1.2, 4.4, "Input Image (224x224)", fontsize=8.5, fontweight='bold', color=NAVY, ha='center')
for i in range(3):
    for j in range(3):
        ax.add_patch(patches.Rectangle((0.6 + j*0.4, 2.8 + i*0.4), 0.35, 0.35, fc=CYAN, ec=BLUE, lw=1))

# Linear projection & tokens
ax.annotate("", xy=(2.8, 3.4), xytext=(1.9, 3.4), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))
ax.text(2.35, 3.65, "Flatten &\nLinear Proj", fontsize=7.5, color=BLUE, ha='center', fontweight='bold')

tokens = [(3.4, 3.4, "[CLS] Token"), (4.4, 3.4, "Patch 1"), (5.3, 3.4, "Patch 2"), (6.2, 3.4, "... Patch N")]
for tx, ty, tname in tokens:
    rect = patches.Rectangle((tx-0.4, ty-0.35), 0.8, 0.7, fc=GOLD if "[CLS]" in tname else LIGHT_BG, ec=BLUE, lw=1.2)
    ax.add_patch(rect)
    ax.text(tx, ty, tname, fontsize=7.5, ha='center', va='center', fontweight='bold')

# Transformer block
rect_tf = patches.FancyBboxPatch((7.2, 1.8), 2.2, 2.5, boxstyle="round,pad=0.1", fc=BLUE, ec=NAVY, lw=2)
ax.add_patch(rect_tf)
ax.text(8.3, 3.6, "Transformer Encoder", color='white', fontweight='bold', fontsize=9, ha='center')
ax.text(8.3, 2.9, "• Multi-Head Attention\n• MLP with GELU\n• LayerNorm & Residuals", color=CYAN, fontsize=7.8, ha='center')
ax.text(8.3, 2.1, "x L Layers", color=GOLD, fontweight='bold', fontsize=8.5, ha='center')

# Output
ax.annotate("", xy=(8.3, 0.9), xytext=(8.3, 1.8), arrowprops=dict(arrowstyle="->", color=NAVY, lw=2))
rect_head = patches.FancyBboxPatch((7.4, 0.2), 1.8, 0.7, boxstyle="round,pad=0.05", fc=TEAL, ec=NAVY, lw=1.5)
ax.add_patch(rect_head)
ax.text(8.3, 0.55, "MLP Class Head\n(Logits)", color='white', fontweight='bold', fontsize=8, ha='center')

save_fig(fig, "vit_architecture_diagram.png")

# -------------------------------------------------------------
# 14. LoRA & QLoRA Low-Rank Adaptation (Chapter 5.5)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title(r"LoRA & QLoRA: $\mathbf{h} = \mathbf{W}_0 \mathbf{x} + \frac{\alpha}{r} \mathbf{B}\mathbf{A}\mathbf{x}$",
             fontsize=12, fontweight='bold', color=NAVY)

# Input x
rect_x = patches.Rectangle((0.6, 2.0), 1.0, 1.0, fc=CYAN, ec=BLUE, lw=1.5)
ax.add_patch(rect_x)
ax.text(1.1, 2.5, r"$\mathbf{x}$" + "\nInput", ha='center', va='center', fontweight='bold', color=NAVY, fontsize=9)

# Frozen Base Weight W0 (tall blue block)
rect_w = patches.FancyBboxPatch((3.0, 1.2), 2.2, 2.6, boxstyle="round,pad=0.08", fc='#cfd8dc', ec='#546e7a', lw=2)
ax.add_patch(rect_w)
ax.text(4.1, 2.5, "Frozen Base Weight\n" + r"$\mathbf{W}_0 \in \mathbb{R}^{d \times k}$" + "\n(4-bit NF4 in QLoRA)",
        ha='center', va='center', fontweight='bold', color=NAVY, fontsize=8.5)

# Trainable Adapters B and A (slender orange/teal blocks)
rect_a = patches.Rectangle((6.2, 3.0), 1.2, 0.6, fc=ORANGE, ec=NAVY, lw=1.5)
ax.add_patch(rect_a)
ax.text(6.8, 3.3, r"$\mathbf{A} \in \mathbb{R}^{r \times k}$", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)

rect_b = patches.Rectangle((6.2, 1.4), 1.2, 0.6, fc=TEAL, ec=NAVY, lw=1.5)
ax.add_patch(rect_b)
ax.text(6.8, 1.7, r"$\mathbf{B} \in \mathbb{R}^{d \times r}$", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)

ax.text(6.8, 2.4, r"Rank $r \ll d$" + "\n(e.g., $r=8, 16$)\n" + r"Scaled by $\frac{\alpha}{r}$",
        ha='center', va='center', color=NAVY, fontsize=8, fontweight='bold')

# Addition node
circle_add = patches.Circle((8.5, 2.5), 0.4, fc=GOLD, ec=NAVY, lw=2)
ax.add_patch(circle_add)
ax.text(8.5, 2.5, r"$\oplus$", ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY)

# Arrows
ax.annotate("", xy=(3.0, 2.5), xytext=(1.6, 2.5), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))
ax.annotate("", xy=(6.2, 3.3), xytext=(1.6, 2.8), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
ax.annotate("", xy=(6.2, 1.7), xytext=(1.6, 2.2), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
ax.annotate("", xy=(8.1, 2.5), xytext=(5.2, 2.5), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))
ax.annotate("", xy=(8.2, 2.7), xytext=(7.4, 3.3), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
ax.annotate("", xy=(8.2, 2.3), xytext=(7.4, 1.7), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))

save_fig(fig, "lora_architecture_diagram.png")

# -------------------------------------------------------------
# 15. LangGraph Stateful Multi-Agent Swarm (Chapter 5.8)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title("LangGraph Multi-Agent Swarm: Central State Graph & Conditional Routing",
             fontsize=12, fontweight='bold', color=NAVY)

# Central State
rect_state = patches.FancyBboxPatch((3.8, 2.0), 2.4, 1.4, boxstyle="round,pad=0.1", fc=LIGHT_BG, ec=BLUE, lw=2)
ax.add_patch(rect_state)
ax.text(5.0, 2.7, "Central AgentState\n(Dict / Pydantic)", ha='center', va='center', fontweight='bold', color=NAVY, fontsize=9)
ax.text(5.0, 2.2, "{messages, tool_calls,\ncode_diff, plan_status}", ha='center', va='center', fontsize=7.5, color='#555')

# Supervisor / Router
rect_sup = patches.FancyBboxPatch((5.0-0.9, 4.0), 1.8, 0.8, boxstyle="round,pad=0.08", fc=NAVY, ec=BLUE, lw=1.5)
ax.add_patch(rect_sup)
ax.text(5.0, 4.4, "Supervisor Agent\n(LLM Orchestrator)", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)

# Worker Nodes
workers = [
    (1.5, 2.2, "Coder Agent\n(Writes Code)", TEAL),
    (5.0, 0.5, "Reviewer Agent\n(Validates Tests)", ORANGE),
    (8.5, 2.2, "Research Agent\n(RAG Search)", CYAN)
]

for wx, wy, wtext, wcol in workers:
    rect = patches.FancyBboxPatch((wx-0.9, wy-0.4), 1.8, 0.8, boxstyle="round,pad=0.08", fc=wcol, ec=NAVY, lw=1.5)
    ax.add_patch(rect)
    tcol = 'white' if wcol != CYAN else NAVY
    ax.text(wx, wy, wtext, ha='center', va='center', color=tcol, fontweight='bold', fontsize=8)

# Bidirectional connecting edges
for wx, wy, _, _ in workers:
    ax.annotate("", xy=(wx, wy+0.4), xytext=(5.0, 4.0), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.8, ls="--"))

save_fig(fig, "langgraph_swarm_diagram.png")

# -------------------------------------------------------------
# 16. PagedAttention Virtual Memory Architecture (Chapter 5.10)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

# Traditional Contiguous Allocation
ax1.set_title("Traditional Serving: Contiguous Allocation\n(Severe Internal & External Fragmentation)",
              fontsize=10.5, fontweight='bold', color=RED)
ax1.set_xlim(0, 5); ax1.set_ylim(0, 5); ax1.axis('off')

# Request 1 reserved
ax1.add_patch(patches.Rectangle((0.5, 3.5), 3.8, 0.8, fc='#ffcdd2', ec=RED, lw=1.5))
ax1.add_patch(patches.Rectangle((0.5, 3.5), 1.2, 0.8, fc=RED, ec=RED, lw=1.5))
ax1.text(1.1, 3.9, "Req 1: Active", color='white', fontweight='bold', fontsize=7.5, ha='center')
ax1.text(2.8, 3.9, "Wasted Reserved VRAM (60-80% Idle!)", color=RED, fontweight='bold', fontsize=7.5, ha='center')

# Request 2 reserved
ax1.add_patch(patches.Rectangle((0.5, 2.0), 3.8, 0.8, fc='#ffcdd2', ec=RED, lw=1.5))
ax1.add_patch(patches.Rectangle((0.5, 2.0), 1.8, 0.8, fc=RED, ec=RED, lw=1.5))
ax1.text(1.4, 2.4, "Req 2: Active", color='white', fontweight='bold', fontsize=7.5, ha='center')
ax1.text(3.1, 2.4, "Wasted Reserved VRAM", color=RED, fontweight='bold', fontsize=7.5, ha='center')

# PagedAttention Virtual Memory
ax2.set_title("vLLM PagedAttention: Virtual Memory Block Table\n(Zero Memory Waste — 96%+ VRAM Utilization)",
              fontsize=10.5, fontweight='bold', color=TEAL)
ax2.set_xlim(0, 5); ax2.set_ylim(0, 5); ax2.axis('off')

# Block Table
ax2.text(1.0, 4.4, "Block Table (Logical -> Physical)", fontsize=8.5, fontweight='bold', color=NAVY)
table_data = [("Logical 0", "Phys Block 7"), ("Logical 1", "Phys Block 3"), ("Logical 2", "Phys Block 12")]
for idx, (log_b, phys_b) in enumerate(table_data):
    ax2.add_patch(patches.Rectangle((0.5, 3.6 - idx*0.6), 1.6, 0.5, fc=LIGHT_BG, ec=BORDER))
    ax2.text(1.3, 3.85 - idx*0.6, log_b, fontsize=7.5, ha='center')
    ax2.add_patch(patches.Rectangle((2.3, 3.6 - idx*0.6), 1.8, 0.5, fc=CYAN, ec=BLUE))
    ax2.text(3.2, 3.85 - idx*0.6, phys_b, fontsize=7.5, ha='center', fontweight='bold', color=NAVY)
    ax2.annotate("", xy=(2.3, 3.85 - idx*0.6), xytext=(2.1, 3.85 - idx*0.6), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

save_fig(fig, "paged_attention_diagram.png")

# -------------------------------------------------------------
# 17. Triton Inference Server Architecture (Chapter 6.4)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title("NVIDIA Triton Inference Server: Dynamic Batching & Concurrent Model Execution",
             fontsize=12, fontweight='bold', color=NAVY)

# Incoming clients
ax.text(1.0, 4.2, "Concurrent Client Requests\n(HTTP/2 & gRPC)", fontsize=8.5, fontweight='bold', color=NAVY, ha='center')
for i in range(3):
    ax.add_patch(patches.FancyBboxPatch((0.4, 3.0 - i*0.8), 1.2, 0.6, boxstyle="round,pad=0.05", fc=CYAN, ec=BLUE))
    ax.text(1.0, 3.3 - i*0.8, f"Req #{i+1}", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    ax.annotate("", xy=(2.6, 2.5), xytext=(1.6, 3.3 - i*0.8), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

# Dynamic Batcher
rect_batcher = patches.FancyBboxPatch((2.6, 1.2), 2.4, 2.6, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=TEAL, lw=2)
ax.add_patch(rect_batcher)
ax.text(3.8, 3.3, "Dynamic Batcher", color=TEAL, fontweight='bold', fontsize=9.5, ha='center')
ax.text(3.8, 2.4, "max_batch_size: 64\nmax_queue_delay: 5ms\nGroups incoming single\nrequests into optimal GEMM",
        ha='center', va='center', fontsize=7.8, color=NAVY)

# GPU Engine Execution
rect_gpu = patches.FancyBboxPatch((6.4, 1.2), 2.8, 2.6, boxstyle="round,pad=0.08", fc=NAVY, ec=BLUE, lw=2)
ax.add_patch(rect_gpu)
ax.text(7.8, 3.3, "NVIDIA GPU Workers", color='white', fontweight='bold', fontsize=9.5, ha='center')
ax.text(7.8, 2.3, "• TensorRT Engine Instances\n• ONNX Runtime Backend\n• PyTorch C++ LibTorch\n• Shared-Memory IPC (CUDA)",
        color=CYAN, fontsize=7.8, ha='center')

ax.annotate("", xy=(6.4, 2.5), xytext=(5.0, 2.5), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.5))

save_fig(fig, "triton_architecture_diagram.png")

# -------------------------------------------------------------
# 18. Two-Tower Recommendation Architecture (Chapter 7.1)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title(r"Two-Tower Neural Retrieval: $\langle \mathbf{u}, \mathbf{v} \rangle$ at Billion Scale",
             fontsize=12, fontweight='bold', color=NAVY)

# User Tower (left)
rect_u = patches.FancyBboxPatch((1.0, 1.5), 2.2, 2.2, boxstyle="round,pad=0.08", fc=BLUE, ec=NAVY, lw=2)
ax.add_patch(rect_u)
ax.text(2.1, 3.2, "User / Query Tower", color='white', fontweight='bold', fontsize=9, ha='center')
ax.text(2.1, 2.3, "User ID, Watch History,\nSearch query, Device, Geo\n\nDeep MLP / Transformer", color=CYAN, fontsize=7.5, ha='center')

# Item Tower (right)
rect_v = patches.FancyBboxPatch((6.8, 1.5), 2.2, 2.2, boxstyle="round,pad=0.08", fc=TEAL, ec=NAVY, lw=2)
ax.add_patch(rect_v)
ax.text(7.9, 3.2, "Candidate / Item Tower", color='white', fontweight='bold', fontsize=9, ha='center')
ax.text(7.9, 2.3, "Video ID, Title, Tags,\nVisual Embedding, Channel\n\nDeep MLP (Pre-computed)", color='#e0f2f1', fontsize=7.5, ha='center')

# Dot product & HNSW
circle_dot = patches.Circle((5.0, 2.6), 0.5, fc=GOLD, ec=NAVY, lw=2)
ax.add_patch(circle_dot)
ax.text(5.0, 2.6, r"$\langle \mathbf{u}, \mathbf{v} \rangle$", ha='center', va='center', fontsize=11, fontweight='bold', color=NAVY)

ax.annotate("", xy=(4.5, 2.6), xytext=(3.2, 2.6), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2))
ax.text(3.8, 2.85, r"$\mathbf{u} \in \mathbb{R}^d$", color=BLUE, fontweight='bold', fontsize=9)

ax.annotate("", xy=(5.5, 2.6), xytext=(6.8, 2.6), arrowprops=dict(arrowstyle="<-", color=TEAL, lw=2))
ax.text(5.9, 2.85, r"$\mathbf{v} \in \mathbb{R}^d$", color=TEAL, fontweight='bold', fontsize=9)

ax.text(5.0, 0.6, "Inference: Item tower embeddings are pre-computed offline & stored in HNSW index.\nOnly User Tower runs online in <10ms!",
        ha='center', fontsize=8.5, color=NAVY, bbox=dict(boxstyle="round,pad=0.3", fc=LIGHT_BG, ec=BORDER))

save_fig(fig, "two_tower_recsys_diagram.png")

# -------------------------------------------------------------
# 19. Uniform Affine Quantization Mapping (Chapter 7.3)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.0))
ax.set_xlim(-0.5, 9.5)
ax.set_ylim(-0.5, 4.5)
ax.axis('off')
ax.set_title(r"Uniform Affine Quantization: Real Range $[r_{\min}, r_{\max}]$ to INT8 $[q_{\min}, q_{\max}]$",
             fontsize=12, fontweight='bold', color=NAVY)

# Real float axis
ax.plot([1.0, 8.0], [3.2, 3.2], color=BLUE, lw=3)
ax.scatter([1.0, 8.0], [3.2, 3.2], color=BLUE, s=80, zorder=5)
ax.text(1.0, 3.6, r"$r_{\min} = -2.40$", ha='center', fontweight='bold', color=BLUE, fontsize=9)
ax.text(8.0, 3.6, r"$r_{\max} = +4.15$", ha='center', fontweight='bold', color=BLUE, fontsize=9)
ax.text(4.5, 3.8, "Continuous FP32 Real Axis (4 Bytes per weight)", ha='center', color=NAVY, fontsize=9, fontweight='bold')

# Integer quantized axis
ax.plot([1.0, 8.0], [1.2, 1.2], color=TEAL, lw=3)
int_ticks = np.linspace(1.0, 8.0, 9)
for idx, tick in enumerate(int_ticks):
    ax.plot([tick, tick], [1.0, 1.4], color=TEAL, lw=2)
    val = int(-128 + idx * 32)
    ax.text(tick, 0.6, str(val), ha='center', fontsize=7.5, color=TEAL, fontweight='bold')

ax.text(4.5, 0.1, "Discrete INT8 Grid [-128, 127] (1 Byte per weight — 75% VRAM Reduction!)",
        ha='center', color=TEAL, fontsize=9, fontweight='bold')

# Formulas in the middle
ax.text(4.5, 2.2, r"Scale $S = \frac{r_{\max} - r_{\min}}{q_{\max} - q_{\min}} = \frac{6.55}{255} \approx 0.02569$" + "\n" +
                  r"Zero-Point $Z = \mathrm{round}(-r_{\min}/S) + q_{\min} \rightarrow q = \mathrm{clamp}(\mathrm{round}(r/S) + Z)$",
        ha='center', va='center', fontsize=8.5, color=NAVY, bbox=dict(boxstyle="round,pad=0.4", fc=LIGHT_BG, ec=BORDER))

save_fig(fig, "quantization_mapping_diagram.png")

# -------------------------------------------------------------
# 20. Model Context Protocol (MCP) Architecture (Chapter 8.1)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title("Model Context Protocol (MCP): Open Universal Interface for AI Tools & Context",
             fontsize=12, fontweight='bold', color=NAVY)

# Host / Client
rect_host = patches.FancyBboxPatch((0.6, 1.5), 2.5, 2.2, boxstyle="round,pad=0.1", fc=NAVY, ec=BLUE, lw=2)
ax.add_patch(rect_host)
ax.text(1.85, 3.2, "MCP Host Application", color='white', fontweight='bold', fontsize=9, ha='center')
ax.text(1.85, 2.3, "Claude Desktop, Cursor,\nAntigravity IDE, Dev Containers\n\n(Houses MCP Client)", color=CYAN, fontsize=7.8, ha='center')

# Protocol Bus (JSON-RPC 2.0)
rect_bus = patches.Rectangle((3.8, 1.2), 1.8, 2.8, fc=LIGHT_BG, ec=BORDER, lw=1.5)
ax.add_patch(rect_bus)
ax.text(4.7, 3.4, "Standard Transport\nLayer", fontweight='bold', color=NAVY, fontsize=8.5, ha='center')
ax.text(4.7, 2.4, "• JSON-RPC 2.0\n• Stdio (Local)\n• SSE (Remote HTTP)\n• Auth & Security", fontsize=7.5, color='#444', ha='center')

# MCP Servers (right)
servers = [
    (7.8, 4.0, "Filesystem MCP Server", TEAL),
    (7.8, 3.0, "GitHub / Git MCP Server", BLUE),
    (7.8, 2.0, "PostgreSQL / DB MCP Server", ORANGE),
    (7.8, 1.0, "Web / Search MCP Server", GOLD)
]

for sx, sy, sname, scol in servers:
    rect = patches.FancyBboxPatch((sx-1.1, sy-0.35), 2.2, 0.7, boxstyle="round,pad=0.05", fc=scol, ec=NAVY, lw=1.2)
    ax.add_patch(rect)
    tcol = 'white' if scol not in [GOLD, CYAN] else NAVY
    ax.text(sx, sy, sname, ha='center', va='center', color=tcol, fontweight='bold', fontsize=7.8)

# Connectors
ax.annotate("", xy=(3.8, 2.6), xytext=(3.1, 2.6), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=2))
for _, sy, _, _ in servers:
    ax.annotate("", xy=(6.7, sy), xytext=(5.6, 2.6), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.5, ls="--"))

save_fig(fig, "mcp_topology_diagram.png")

print("\nAll 19 textbook diagrams successfully generated at high resolution!")
