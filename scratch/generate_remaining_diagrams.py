"""
generate_remaining_diagrams.py — Generates 31 publication-grade architectural,
mathematical, and systems diagrams for 'The Complete AI Engineer' textbook.
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Typography & styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['mathtext.fontset'] = 'dejavusans'

# Cohesive Textbook Technical Palette
NAVY = '#0d1b2a'
BLUE = '#1b4965'
CYAN = '#5fa8d3'
LIGHT_BG = '#f8f9fa'
TEAL = '#2a9d8f'
ORANGE = '#e76f51'
RED = '#e63946'
GOLD = '#e9c46a'
PURPLE = '#7209b7'
BORDER = '#d0d7de'
GRAY = '#6c757d'

def save_fig(fig, filename):
    filepath = os.path.join('.', filename)
    fig.savefig(filepath, dpi=250, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"[SAVED] {filename}")

print("Generating 31 publication-grade diagrams for remaining textbook chapters...")

# =====================================================================
# 1. Ch 0.2: Python Object Model vs NumPy Buffer (ch02_python_a_to_z.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={'width_ratios': [1.1, 1]})
    ax1.set_xlim(-0.5, 6.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.axis('off')
    ax1.set_title("CPython Standard List: Boxed PyObject* Pointers", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Python list array of pointers
    ax1.text(0.5, 3.8, "PyListObject (Pointer Array)", fontsize=9, fontweight='bold', color=BLUE)
    for i in range(3):
        box = patches.FancyBboxPatch((i*1.8, 2.6), 1.5, 0.8, boxstyle="round,pad=0.03", fc=CYAN, ec=BLUE, lw=1.5, alpha=0.3)
        ax1.add_patch(box)
        ax1.text(i*1.8 + 0.75, 3.0, f"item[{i}]\n(64-bit ptr)", ha='center', va='center', fontsize=8, color=NAVY)
        
        # Arrow down to heap PyObject
        ax1.annotate('', xy=(i*1.8 + 0.75, 1.8), xytext=(i*1.8 + 0.75, 2.6),
                     arrowprops=dict(arrowstyle="->", lw=1.5, color=ORANGE))
        
        # Heap PyObject
        heap_box = patches.FancyBboxPatch((i*1.8 - 0.2, 0.2), 1.9, 1.5, boxstyle="round,pad=0.03", fc='white', ec=BORDER, lw=1.5)
        ax1.add_patch(heap_box)
        ax1.text(i*1.8 + 0.75, 1.4, f"PyLongObject {i+1}", ha='center', va='center', fontsize=8, fontweight='bold', color=BLUE)
        ax1.text(i*1.8 + 0.75, 1.0, "ob_refcnt: 8B\nob_type: 8B", ha='center', va='center', fontsize=7, color=GRAY)
        ax1.text(i*1.8 + 0.75, 0.5, f"ob_digit: {i+1} (8B)", ha='center', va='center', fontsize=7.5, fontweight='bold', color=NAVY)
    
    # NumPy Contiguous buffer
    ax2.set_xlim(-0.5, 6.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.axis('off')
    ax2.set_title("NumPy Contiguous C-Buffer: Zero Overhead", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # PyArrayObject Header
    header = patches.FancyBboxPatch((0.5, 3.0), 5.0, 1.1, boxstyle="round,pad=0.03", fc='#e0f2fe', ec=BLUE, lw=1.5)
    ax2.add_patch(header)
    ax2.text(3.0, 3.7, "PyArrayObject Header (24 Bytes Metadata)", ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)
    ax2.text(3.0, 3.3, "data_ptr | dtype: float64 | shape: (3,) | strides: (8,)", ha='center', va='center', fontsize=7.5, color=BLUE)
    
    # Arrow to data buffer
    ax2.annotate('', xy=(3.0, 2.0), xytext=(3.0, 3.0),
                 arrowprops=dict(arrowstyle="->", lw=2, color=TEAL))
    
    # Continuous memory block
    ax2.text(3.0, 2.2, "Single Continuous Virtual Memory Block (Cache-Line Friendly)", ha='center', va='center', fontsize=8, color=TEAL, fontweight='bold')
    for i in range(3):
        cbox = patches.Rectangle((0.8 + i*1.6, 0.8), 1.6, 1.0, fc='#dcfce7', ec=TEAL, lw=1.8)
        ax2.add_patch(cbox)
        ax2.text(0.8 + i*1.6 + 0.8, 1.4, f"data[{i}]", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
        ax2.text(0.8 + i*1.6 + 0.8, 1.05, f"{(i+1)*1.0:.1f} (8 Bytes)", ha='center', va='center', fontsize=7.5, color=BLUE)
    
    ax2.text(3.0, 0.2, "SIMD Vectorized | Zero Boxing | Cache Prefetch Optimal", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY,
             bbox=dict(boxstyle="round,pad=0.2", fc='#fef3c7', ec=GOLD))
    
    save_fig(fig, "python_memory_object_model.png")
except Exception as e:
    print(f"Error in 1: {e}")

# =====================================================================
# 2. Ch 0.4: Data Lakehouse Medallion Architecture (ch04_large_scale_data.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title("The Medallion Lakehouse Architecture for Enterprise AI Pipelines", fontsize=12, fontweight='bold', color=NAVY, pad=12)
    
    # Bronze Tier
    bronze = patches.FancyBboxPatch((0.2, 0.8), 2.8, 3.0, boxstyle="round,pad=0.05", fc='#fed7aa', ec='#c2410c', lw=2)
    ax.add_patch(bronze)
    ax.text(1.6, 3.4, "BRONZE TIER\nRaw Data Ingestion", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#9a3412')
    ax.text(1.6, 2.2, "• Kafka & Kinesis streams\n• Raw API JSON dumps\n• Unstructured logs & text\n• Append-only schema\n• High-throughput storage", ha='center', va='center', fontsize=8, color=NAVY, linespacing=1.4)
    
    # Arrow 1
    ax.annotate('', xy=(3.8, 2.3), xytext=(3.0, 2.3),
                arrowprops=dict(arrowstyle="->", lw=2.5, color=NAVY))
    ax.text(3.4, 2.7, "ETL Clean\nDe-dup", ha='center', va='center', fontsize=7.5, color=BLUE, fontweight='bold')
    
    # Silver Tier
    silver = patches.FancyBboxPatch((4.0, 0.8), 2.8, 3.0, boxstyle="round,pad=0.05", fc='#e2e8f0', ec='#475569', lw=2)
    ax.add_patch(silver)
    ax.text(5.4, 3.4, "SILVER TIER\nCleansed & Enriched", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e293b')
    ax.text(5.4, 2.2, "• Schema enforcement\n• Parquet / Delta Lake\n• Data quality validation\n• Missing value imputation\n• Conformed dimensions", ha='center', va='center', fontsize=8, color=NAVY, linespacing=1.4)
    
    # Arrow 2
    ax.annotate('', xy=(7.6, 2.3), xytext=(6.8, 2.3),
                arrowprops=dict(arrowstyle="->", lw=2.5, color=NAVY))
    ax.text(7.2, 2.7, "Aggregate\nEmbed", ha='center', va='center', fontsize=7.5, color=BLUE, fontweight='bold')
    
    # Gold Tier
    gold = patches.FancyBboxPatch((7.8, 0.8), 2.5, 3.0, boxstyle="round,pad=0.05", fc='#fef08a', ec='#ca8a04', lw=2)
    ax.add_patch(gold)
    ax.text(9.05, 3.4, "GOLD TIER\nAI & Feature Store", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#854d0e')
    ax.text(9.05, 2.2, "• Pre-computed features\n• Vector embeddings\n• Train/Val/Test splits\n• Low-latency online KV\n• BI & ML consumption", ha='center', va='center', fontsize=8, color=NAVY, linespacing=1.4)
    
    save_fig(fig, "data_lakehouse_medallion.png")
except Exception as e:
    print(f"Error in 2: {e}")

# =====================================================================
# 3. Ch 1.3: Bayesian Inference Update (ch13_probability_bayes.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    theta = np.linspace(0, 1, 300)
    
    # Prior Beta(3, 3)
    prior = theta**2 * (1 - theta)**2
    prior = prior / np.trapz(prior, theta)
    
    # Likelihood Binomial n=10, k=8 -> theta^8 (1-theta)^2
    likelihood = theta**8 * (1 - theta)**2
    likelihood = likelihood / np.trapz(likelihood, theta)
    
    # Posterior Beta(11, 5)
    posterior = theta**10 * (1 - theta)**4
    posterior = posterior / np.trapz(posterior, theta)
    
    ax.plot(theta, prior, color=CYAN, lw=2.2, linestyle='--', label=r"Prior $P(\theta)$: Initial Belief")
    ax.plot(theta, likelihood, color=ORANGE, lw=2.2, linestyle=':', label=r"Likelihood $P(D \mid \theta)$: Observed Evidence")
    ax.plot(theta, posterior, color=BLUE, lw=3.0, label=r"Posterior $P(\theta \mid D) \propto P(D \mid \theta) P(\theta)$")
    ax.fill_between(theta, 0, posterior, color=BLUE, alpha=0.15)
    
    ax.set_title("Bayesian Updating: Shift from Prior to Sharpened Posterior", fontsize=11, fontweight='bold', color=NAVY, pad=12)
    ax.set_xlabel(r"Parameter $\theta$", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylabel("Probability Density", fontsize=10, fontweight='bold', color=NAVY)
    ax.grid(True, linestyle='--', alpha=0.5, color=BORDER)
    ax.legend(framealpha=0.9, fontsize=9)
    
    save_fig(fig, "bayesian_inference_update.png")
except Exception as e:
    print(f"Error in 3: {e}")

# =====================================================================
# 4. Ch 1.4: Information Theory Venn Diagram (ch14_information_theory.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2.2)
    ax.axis('off')
    ax.set_title("Information Theory: Venn Decomposition of Entropy & Mutual Information", fontsize=11, fontweight='bold', color=NAVY, pad=12)
    
    # Circle X
    circ_x = patches.Circle((-0.8, 0), 1.5, fc=CYAN, ec=BLUE, lw=2, alpha=0.35)
    ax.add_patch(circ_x)
    
    # Circle Y
    circ_y = patches.Circle((0.8, 0), 1.5, fc=TEAL, ec=BLUE, lw=2, alpha=0.35)
    ax.add_patch(circ_y)
    
    # Labels
    ax.text(-1.6, 0, "Conditional\nEntropy\n$H(X \\mid Y)$", ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY)
    ax.text(1.6, 0, "Conditional\nEntropy\n$H(Y \\mid X)$", ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY)
    ax.text(0, 0, "Mutual\nInformation\n$I(X; Y)$", ha='center', va='center', fontsize=9.5, fontweight='bold', color=RED)
    
    ax.text(-1.4, 1.7, "Variable $X$ Entropy: $H(X)$", fontsize=9, fontweight='bold', color=BLUE)
    ax.text(0.6, 1.7, "Variable $Y$ Entropy: $H(Y)$", fontsize=9, fontweight='bold', color=TEAL)
    
    # Bottom formula box
    box = patches.FancyBboxPatch((-2.8, -1.8), 5.6, 0.7, boxstyle="round,pad=0.04", fc='#f8f9fa', ec=BORDER, lw=1.2)
    ax.add_patch(box)
    ax.text(0, -1.45, "Total Union = Joint Entropy $H(X, Y) = H(X) + H(Y) - I(X; Y)$", ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY)
    
    save_fig(fig, "information_theory_venn.png")
except Exception as e:
    print(f"Error in 4: {e}")

# =====================================================================
# 5. Ch 2.1: Bias-Variance Tradeoff & Double Descent (ch21_ml_paradigm.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    x = np.linspace(0.5, 8, 300)
    
    bias_sq = 4.0 / (x**0.8)
    variance = 0.08 * (x**1.8)
    irreducible = 0.8
    total_error = bias_sq + variance + irreducible
    
    ax.plot(x, bias_sq, color=BLUE, lw=2.2, linestyle='--', label=r"$\mathrm{Bias}^2$ (Underfitting Risk)")
    ax.plot(x, variance, color=ORANGE, lw=2.2, linestyle='-.', label=r"$\mathrm{Variance}$ (Overfitting Risk)")
    ax.axhline(irreducible, color=GRAY, lw=1.5, linestyle=':', label=r"Irreducible Noise $\sigma^2$")
    ax.plot(x, total_error, color=RED, lw=3.0, label="Total Generalization Error")
    
    # Optimum marker
    opt_idx = np.argmin(total_error)
    ax.axvline(x[opt_idx], color=TEAL, linestyle='--', lw=1.8)
    ax.scatter([x[opt_idx]], [total_error[opt_idx]], color=TEAL, s=80, zorder=5)
    ax.text(x[opt_idx], total_error[opt_idx] + 0.4, "Optimal Capacity\nSweet Spot", ha='center', fontsize=8.5, fontweight='bold', color=TEAL)
    
    ax.text(1.2, 4.5, "High Bias\n(Underfitting)", ha='center', fontsize=8.5, color=BLUE, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc='#e0f2fe', ec=BLUE))
    ax.text(6.8, 4.5, "High Variance\n(Overfitting)", ha='center', fontsize=8.5, color=ORANGE, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc='#ffedd5', ec=ORANGE))
    
    ax.set_title("The Bias-Variance Tradeoff & Generalization Error Bounds", fontsize=11, fontweight='bold', color=NAVY, pad=12)
    ax.set_xlabel("Model Capacity / Hypothesis Complexity", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylabel("Expected Test Error", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylim(0, 6)
    ax.grid(True, linestyle='--', alpha=0.5, color=BORDER)
    ax.legend(framealpha=0.9, fontsize=8.5, loc='upper center')
    
    save_fig(fig, "bias_variance_tradeoff.png")
except Exception as e:
    print(f"Error in 5: {e}")

# =====================================================================
# 6. Ch 2.2: Lasso vs Ridge Regularization Geometry (ch22_linear_regression.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.6))
    
    # Loss contours
    b1, b2 = np.meshgrid(np.linspace(-2, 3, 200), np.linspace(-2, 3, 200))
    loss = (b1 - 1.8)**2 + 2.0*(b2 - 1.5)**2
    
    # Left: L1 Lasso Diamond
    ax1.contour(b1, b2, loss, levels=[0.5, 1.5, 3.0, 5.0, 8.0], colors=BLUE, alpha=0.7)
    diamond = patches.Polygon([[-1, 0], [0, 1], [1, 0], [0, -1]], closed=True, fc='#fed7aa', ec=ORANGE, lw=2.5, alpha=0.5)
    ax1.add_patch(diamond)
    ax1.scatter([0], [1], color=RED, s=90, zorder=6, label=r"Corner Hit $\rightarrow \beta_1 = 0$ (Sparse)")
    ax1.axhline(0, color=BORDER, lw=1)
    ax1.axvline(0, color=BORDER, lw=1)
    ax1.set_title(r"L1 Lasso ($\ell_1$): Diamond Constraint", fontsize=10.5, fontweight='bold', color=NAVY)
    ax1.set_xlabel(r"$\beta_1$", fontsize=10, fontweight='bold')
    ax1.set_ylabel(r"$\beta_2$", fontsize=10, fontweight='bold')
    ax1.legend(loc='lower left', fontsize=8)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # Right: L2 Ridge Circle
    ax2.contour(b1, b2, loss, levels=[0.5, 1.5, 3.0, 5.0, 8.0], colors=BLUE, alpha=0.7)
    circle = patches.Circle((0, 0), 1.0, fc='#bfdbfe', ec=CYAN, lw=2.5, alpha=0.5)
    ax2.add_patch(circle)
    ax2.scatter([0.55], [0.83], color=TEAL, s=90, zorder=6, label=r"Smooth Tangency ($\beta_1, \beta_2 \neq 0$)")
    ax2.axhline(0, color=BORDER, lw=1)
    ax2.axvline(0, color=BORDER, lw=1)
    ax2.set_title(r"L2 Ridge ($\ell_2$): Circular Constraint", fontsize=10.5, fontweight='bold', color=NAVY)
    ax2.set_xlabel(r"$\beta_1$", fontsize=10, fontweight='bold')
    ax2.set_ylabel(r"$\beta_2$", fontsize=10, fontweight='bold')
    ax2.legend(loc='lower left', fontsize=8)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    save_fig(fig, "lasso_vs_ridge_contours.png")
except Exception as e:
    print(f"Error in 6: {e}")

# =====================================================================
# 7. Ch 2.3: Logistic Sigmoid & Decision Boundary (ch23_logistic_regression.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.4))
    
    # Left: Sigmoid curve
    z = np.linspace(-6, 6, 200)
    sig = 1.0 / (1.0 + np.exp(-z))
    ax1.plot(z, sig, color=BLUE, lw=3)
    ax1.axhline(0.5, color=ORANGE, linestyle='--', lw=1.5, label="Decision Threshold $p = 0.5$")
    ax1.axvline(0, color=GRAY, linestyle=':', lw=1.2)
    ax1.scatter([0], [0.5], color=RED, s=70, zorder=5)
    ax1.set_title(r"The Logistic Sigmoid $\sigma(z) = \frac{1}{1 + e^{-z}}$", fontsize=10.5, fontweight='bold', color=NAVY)
    ax1.set_xlabel(r"Logit $z = w^T x + b$", fontsize=10, fontweight='bold')
    ax1.set_ylabel(r"Class Probability $P(Y=1 \mid x)$", fontsize=10, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(loc='upper left', fontsize=8.5)
    
    # Right: 2D Decision Boundary
    np.random.seed(42)
    c0 = np.random.randn(25, 2) * 0.6 + [1.5, 1.5]
    c1 = np.random.randn(25, 2) * 0.6 + [3.5, 3.5]
    ax2.scatter(c0[:, 0], c0[:, 1], color=BLUE, s=40, label="Class 0 ($y=0$)", alpha=0.8)
    ax2.scatter(c1[:, 0], c1[:, 1], color=ORANGE, s=40, label="Class 1 ($y=1$)", marker='^', alpha=0.8)
    
    bx = np.linspace(0.5, 4.5, 100)
    by = -bx + 5.0 # w1*x1 + w2*x2 + b = 0
    ax2.plot(bx, by, color=TEAL, lw=2.5, label=r"Boundary: $w^T x + b = 0$")
    ax2.set_title("Hyperplane Linear Decision Boundary", fontsize=10.5, fontweight='bold', color=NAVY)
    ax2.set_xlabel(r"Feature $x_1$", fontsize=10, fontweight='bold')
    ax2.set_ylabel(r"Feature $x_2$", fontsize=10, fontweight='bold')
    ax2.legend(loc='lower left', fontsize=8)
    ax2.grid(True, linestyle='--', alpha=0.4)
    
    save_fig(fig, "logistic_sigmoid_boundary.png")
except Exception as e:
    print(f"Error in 7: {e}")

# =====================================================================
# 8. Ch 2.4: Decision Tree Partitioning (ch24_decision_trees.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    
    # Left: Tree Hierarchy
    ax1.set_xlim(-0.5, 6.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.axis('off')
    ax1.set_title("Hierarchical Binary Splits", fontsize=11, fontweight='bold', color=NAVY)
    
    # Nodes
    def draw_node(ax, x, y, text, col='#dbeafe', ec=BLUE):
        box = patches.FancyBboxPatch((x-0.9, y-0.35), 1.8, 0.7, boxstyle="round,pad=0.03", fc=col, ec=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    draw_node(ax1, 3.0, 4.0, "Root: $x_1 \leq 3.5$")
    draw_node(ax1, 1.5, 2.5, "$x_2 \leq 4.0$")
    draw_node(ax1, 4.5, 2.5, "Leaf: Class B\n(Region $R_3$)", col='#fef3c7', ec=GOLD)
    draw_node(ax1, 0.6, 1.0, "Leaf: Class A\n(Region $R_1$)", col='#dcfce7', ec=TEAL)
    draw_node(ax1, 2.4, 1.0, "Leaf: Class B\n(Region $R_2$)", col='#fef3c7', ec=GOLD)
    
    # Arrows
    ax1.annotate('', xy=(1.5, 2.85), xytext=(2.6, 3.65), arrowprops=dict(arrowstyle="->", lw=1.5, color=BLUE))
    ax1.text(1.8, 3.4, "Yes", fontsize=7.5, fontweight='bold', color=BLUE)
    ax1.annotate('', xy=(4.5, 2.85), xytext=(3.4, 3.65), arrowprops=dict(arrowstyle="->", lw=1.5, color=BLUE))
    ax1.text(4.1, 3.4, "No", fontsize=7.5, fontweight='bold', color=BLUE)
    ax1.annotate('', xy=(0.6, 1.35), xytext=(1.2, 2.15), arrowprops=dict(arrowstyle="->", lw=1.5, color=BLUE))
    ax1.text(0.7, 1.9, "Yes", fontsize=7.5, fontweight='bold', color=BLUE)
    ax1.annotate('', xy=(2.4, 1.35), xytext=(1.8, 2.15), arrowprops=dict(arrowstyle="->", lw=1.5, color=BLUE))
    ax1.text(2.2, 1.9, "No", fontsize=7.5, fontweight='bold', color=BLUE)
    
    # Right: 2D Partitioning
    ax2.set_xlim(0, 6)
    ax2.set_ylim(0, 6)
    ax2.axvline(3.5, color=RED, lw=2.2, linestyle='--', label=r"Split 1: $x_1 = 3.5$")
    ax2.plot([0, 3.5], [4.0, 4.0], color=ORANGE, lw=2.2, linestyle='-.', label=r"Split 2: $x_2 = 4.0$")
    
    # Fill regions
    ax2.fill_between([0, 3.5], 0, 4.0, color='#dcfce7', alpha=0.5)
    ax2.text(1.75, 2.0, "Region $R_1$\n(Class A)", ha='center', va='center', fontsize=9, fontweight='bold', color=TEAL)
    
    ax2.fill_between([0, 3.5], 4.0, 6.0, color='#fef3c7', alpha=0.5)
    ax2.text(1.75, 5.0, "Region $R_2$\n(Class B)", ha='center', va='center', fontsize=9, fontweight='bold', color='#b45309')
    
    ax2.fill_between([3.5, 6.0], 0, 6.0, color='#fed7aa', alpha=0.4)
    ax2.text(4.75, 3.0, "Region $R_3$\n(Class B)", ha='center', va='center', fontsize=9, fontweight='bold', color='#c2410c')
    
    ax2.set_title("Orthogonal Feature Space Partitioning", fontsize=11, fontweight='bold', color=NAVY)
    ax2.set_xlabel(r"Feature $x_1$", fontsize=10, fontweight='bold')
    ax2.set_ylabel(r"Feature $x_2$", fontsize=10, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=8)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    save_fig(fig, "decision_tree_partitioning.png")
except Exception as e:
    print(f"Error in 8: {e}")

# =====================================================================
# 9. Ch 2.5: Random Forest & Bagging (ch25_random_forests.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title("Random Forest: Bootstrap Aggregation (Bagging) & Random Subspace Voting", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Original Dataset
    d_box = patches.FancyBboxPatch((4.0, 3.6), 2.0, 0.7, boxstyle="round,pad=0.03", fc='#e0f2fe', ec=BLUE, lw=2)
    ax.add_patch(d_box)
    ax.text(5.0, 3.95, "Dataset $D$ ($N$ samples, $P$ feats)", ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)
    
    trees = ["Tree 1", "Tree 2", "Tree 3", "Tree B"]
    xs = [1.2, 3.7, 6.3, 8.8]
    
    for i, (tname, tx) in enumerate(zip(trees, xs)):
        # Arrow down
        ax.annotate('', xy=(tx, 2.6), xytext=(5.0, 3.6), arrowprops=dict(arrowstyle="->", lw=1.2, color=GRAY))
        
        # Bootstrap sample
        b_box = patches.FancyBboxPatch((tx-1.0, 2.0), 2.0, 0.6, boxstyle="round,pad=0.02", fc='#fef3c7', ec=GOLD, lw=1.2)
        ax.add_patch(b_box)
        ax.text(tx, 2.3, f"Bootstrap $D_{i+1}$\n(Subspace $\\sqrt{{P}}$)", ha='center', va='center', fontsize=7.5, color=NAVY)
        
        # Tree box
        t_box = patches.FancyBboxPatch((tx-0.9, 0.9), 1.8, 0.8, boxstyle="round,pad=0.02", fc='#dcfce7', ec=TEAL, lw=1.5)
        ax.add_patch(t_box)
        ax.text(tx, 1.3, f"{tname}\n(Unpruned Tree)", ha='center', va='center', fontsize=8, fontweight='bold', color=TEAL)
        
        # Arrow down to ensemble
        ax.annotate('', xy=(5.0, 0.3), xytext=(tx, 0.9), arrowprops=dict(arrowstyle="->", lw=1.2, color=GRAY))
    
    # Majority Voting Box
    v_box = patches.FancyBboxPatch((3.2, -0.4), 3.6, 0.6, boxstyle="round,pad=0.03", fc='#fed7aa', ec=ORANGE, lw=2)
    ax.add_patch(v_box)
    ax.text(5.0, -0.1, "Ensemble Aggregation: Majority Vote / Mean", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#9a3412')
    
    save_fig(fig, "random_forest_bagging.png")
except Exception as e:
    print(f"Error in 9: {e}")

# =====================================================================
# 10. Ch 2.5b: Gradient Boosted Decision Trees (ch25b_gradient_boosting.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.0)
    ax.axis('off')
    ax.set_title("Gradient Boosting (GBDT): Sequential Residual Fitting", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Step 0
    box0 = patches.FancyBboxPatch((0.2, 1.2), 2.2, 1.8, boxstyle="round,pad=0.03", fc='#e0f2fe', ec=BLUE, lw=1.8)
    ax.add_patch(box0)
    ax.text(1.3, 2.5, "Iteration $m=0$", ha='center', fontsize=9, fontweight='bold', color=BLUE)
    ax.text(1.3, 1.8, "$F_0(x) = \\bar{y}$\n(Base constant)\nResiduals:\n$r_{i,1} = y_i - F_0(x_i)$", ha='center', fontsize=8, color=NAVY)
    
    # Arrow 1
    ax.annotate('', xy=(3.0, 2.1), xytext=(2.4, 2.1), arrowprops=dict(arrowstyle="->", lw=2, color=ORANGE))
    
    # Step 1
    box1 = patches.FancyBboxPatch((3.2, 1.2), 2.8, 1.8, boxstyle="round,pad=0.03", fc='#dcfce7', ec=TEAL, lw=1.8)
    ax.add_patch(box1)
    ax.text(4.6, 2.5, "Iteration $m=1$", ha='center', fontsize=9, fontweight='bold', color=TEAL)
    ax.text(4.6, 1.8, "Fit weak tree $h_1(x)$ to $r_{i,1}$\n$F_1(x) = F_0(x) + \\eta h_1(x)$\nNew smaller residuals:\n$r_{i,2} = y_i - F_1(x_i)$", ha='center', fontsize=8, color=NAVY)
    
    # Arrow 2
    ax.annotate('', xy=(6.6, 2.1), xytext=(6.0, 2.1), arrowprops=dict(arrowstyle="->", lw=2, color=ORANGE))
    
    # Step M
    box2 = patches.FancyBboxPatch((6.8, 1.2), 3.2, 1.8, boxstyle="round,pad=0.03", fc='#fef3c7', ec=GOLD, lw=1.8)
    ax.add_patch(box2)
    ax.text(8.4, 2.5, "Converged Model $M$", ha='center', fontsize=9, fontweight='bold', color='#b45309')
    ax.text(8.4, 1.8, "Final Strong Predictor:\n$F_M(x) = F_0(x) + \\sum_{m=1}^M \\eta h_m(x)$\nMinimal Pseudo-Residuals\nHigh Accuracy & Robust", ha='center', fontsize=8, color=NAVY)
    
    save_fig(fig, "gradient_boosting_residuals.png")
except Exception as e:
    print(f"Error in 10: {e}")

# =====================================================================
# 11. Ch 2.7: K-Means & PCA (ch27_unsupervised_kmeans_pca.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.4))
    
    # Left: K-Means Voronoi
    np.random.seed(10)
    c1 = np.random.randn(20, 2)*0.4 + [1, 2]
    c2 = np.random.randn(20, 2)*0.4 + [3, 4]
    c3 = np.random.randn(20, 2)*0.4 + [4, 1.5]
    ax1.scatter(c1[:,0], c1[:,1], color=CYAN, s=30, alpha=0.8)
    ax1.scatter(c2[:,0], c2[:,1], color=ORANGE, s=30, alpha=0.8)
    ax1.scatter(c3[:,0], c3[:,1], color=TEAL, s=30, alpha=0.8)
    ax1.scatter([1, 3, 4], [2, 4, 1.5], color=RED, marker='*', s=140, label="Centroids $\\mu_k$", zorder=5)
    ax1.set_title("K-Means: Centroid Partitioning", fontsize=10.5, fontweight='bold', color=NAVY)
    ax1.grid(True, linestyle='--', alpha=0.3)
    ax1.legend(loc='lower right', fontsize=8)
    
    # Right: PCA orthogonal axes
    data = np.random.randn(80, 2)
    data[:, 1] = 0.8 * data[:, 0] + np.random.randn(80)*0.3
    ax2.scatter(data[:,0], data[:,1], color=BLUE, s=25, alpha=0.6)
    
    # PCA vectors
    ax2.annotate('', xy=(1.8, 1.44), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", lw=3, color=RED))
    ax2.text(1.9, 1.3, "PC1 (Max Var $\\lambda_1$)", fontsize=8.5, fontweight='bold', color=RED)
    ax2.annotate('', xy=(-0.6, 0.75), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", lw=2, color=TEAL))
    ax2.text(-1.4, 0.9, "PC2 ($\\lambda_2$)", fontsize=8.5, fontweight='bold', color=TEAL)
    ax2.set_title("PCA: Principal Axes of Variance", fontsize=10.5, fontweight='bold', color=NAVY)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    save_fig(fig, "kmeans_pca_manifold.png")
except Exception as e:
    print(f"Error in 11: {e}")

# =====================================================================
# 12. Ch 2.8: Temporal Split vs Data Leakage (ch28_feature_engineering.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 4.4))
    
    # Subplot 1: Correct Temporal Split
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 2)
    ax1.axis('off')
    ax1.set_title("Correct Production Workflow: Temporal Train / Test Split (Zero Leakage)", fontsize=10, fontweight='bold', color=NAVY)
    
    t_train = patches.Rectangle((0.5, 0.5), 5.5, 0.8, fc='#dbeafe', ec=BLUE, lw=1.5)
    ax1.add_patch(t_train)
    ax1.text(3.25, 0.9, "Historical Training Window [0, T_split]\nFit Scalers & Imputers ONLY here", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    t_test = patches.Rectangle((6.2, 0.5), 3.0, 0.8, fc='#dcfce7', ec=TEAL, lw=1.5)
    ax1.add_patch(t_test)
    ax1.text(7.7, 0.9, "Future Test Window [T_split, T_end]\nTransform ONLY (.transform)", ha='center', va='center', fontsize=8, fontweight='bold', color=TEAL)
    
    # Subplot 2: Data Leakage Hazard
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 2)
    ax2.axis('off')
    ax2.set_title("Catastrophic Data Leakage: Random K-Fold Shuffling / Global Preprocessing", fontsize=10, fontweight='bold', color=RED)
    
    leak_box = patches.Rectangle((0.5, 0.5), 8.7, 0.8, fc='#fee2e2', ec=RED, lw=1.5, linestyle='--')
    ax2.add_patch(leak_box)
    ax2.text(4.85, 0.9, "Global Fit: Future Information Leaks into Past Training\nArtificially Overoptimistic Test Metrics -> Silent Production Failure!", ha='center', va='center', fontsize=8, fontweight='bold', color=RED)
    
    save_fig(fig, "data_leakage_temporal_split.png")
except Exception as e:
    print(f"Error in 12: {e}")

# =====================================================================
# 13. Ch 2.9: ROC-AUC & Precision-Recall Curves (ch29_model_evaluation.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.4))
    
    # Left: ROC
    fpr = np.linspace(0, 1, 100)
    tpr = 1 - (1 - fpr)**2.5
    ax1.plot(fpr, tpr, color=BLUE, lw=2.5, label="Model ROC (AUC = 0.91)")
    ax1.plot([0, 1], [0, 1], color=GRAY, linestyle='--', label="Random Guess (AUC = 0.50)")
    ax1.fill_between(fpr, 0, tpr, color=BLUE, alpha=0.15)
    ax1.set_title("Receiver Operating Characteristic (ROC)", fontsize=10.5, fontweight='bold', color=NAVY)
    ax1.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=9, fontweight='bold')
    ax1.set_ylabel("True Positive Rate (Recall)", fontsize=9, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(loc='lower right', fontsize=8.5)
    
    # Right: PR
    recall = np.linspace(0, 1, 100)
    precision = 0.95 / (1.0 + 3.0 * recall**2)
    ax2.plot(recall, precision, color=TEAL, lw=2.5, label="Model PR Curve")
    ax2.axhline(0.1, color=ORANGE, linestyle='--', label="Base Prevalence (10%)")
    ax2.fill_between(recall, 0, precision, color=TEAL, alpha=0.15)
    ax2.set_title("Precision-Recall Curve (Imbalanced Data)", fontsize=10.5, fontweight='bold', color=NAVY)
    ax2.set_xlabel("Recall (Coverage)", fontsize=9, fontweight='bold')
    ax2.set_ylabel("Precision (Purity)", fontsize=9, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.4)
    ax2.legend(loc='upper right', fontsize=8.5)
    
    save_fig(fig, "roc_pr_calibration_curves.png")
except Exception as e:
    print(f"Error in 13: {e}")

# =====================================================================
# 14. Ch 3.2: Modern Activation Functions (ch32_mlp_activations.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    x = np.linspace(-3, 3, 300)
    
    relu = np.maximum(0, x)
    lrelu = np.where(x > 0, x, 0.1 * x)
    # GELU approx: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
    gelu = 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))
    silu = x / (1 + np.exp(-x))
    
    ax.plot(x, relu, label="ReLU: max(0, x)", color=GRAY, lw=1.8, linestyle=':')
    ax.plot(x, lrelu, label="Leaky ReLU (alpha=0.1)", color=ORANGE, lw=1.8, linestyle='--')
    ax.plot(x, gelu, label="GELU (Transformers / BERT)", color=BLUE, lw=2.5)
    ax.plot(x, silu, label="Swish / SiLU (LLaMA)", color=TEAL, lw=2.5)
    
    ax.axhline(0, color=BORDER, lw=1)
    ax.axvline(0, color=BORDER, lw=1)
    ax.set_title("Modern Non-Linear Activations: Smoothness & Non-Monotonicity", fontsize=11, fontweight='bold', color=NAVY, pad=12)
    ax.set_xlabel("Input $x$", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylabel(r"Output $f(x)$", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylim(-0.8, 3.2)
    ax.grid(True, linestyle='--', alpha=0.4, color=BORDER)
    ax.legend(framealpha=0.9, fontsize=8.5, loc='upper left')
    
    save_fig(fig, "modern_activation_functions.png")
except Exception as e:
    print(f"Error in 14: {e}")

# =====================================================================
# 15. Ch 3.4: Deep Optimizers Trajectories (ch34_deep_optimization.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-2, 2, 200))
    z = 0.1 * x**2 + 1.5 * y**2 # Anisotropic ravine
    
    ax.contour(x, y, z, levels=[0.2, 0.6, 1.2, 2.2, 3.5, 5.5], colors=BORDER)
    
    # SGD trajectory (oscillatory)
    sgd_x = [-2.5, -2.2, -1.8, -1.4, -0.9, -0.5, -0.2, 0]
    sgd_y = [1.5, -1.3, 1.0, -0.8, 0.6, -0.4, 0.2, 0]
    ax.plot(sgd_x, sgd_y, color=RED, marker='o', markersize=4, lw=1.8, label="Standard SGD (Wild Oscillations)")
    
    # Momentum (dampened)
    mom_x = [-2.5, -2.1, -1.6, -1.0, -0.5, 0]
    mom_y = [1.5, 0.2, -0.3, 0.1, -0.05, 0]
    ax.plot(mom_x, mom_y, color=ORANGE, marker='s', markersize=4, lw=2.2, label="SGD + Momentum (Dampened)")
    
    # Adam / AdamW (direct)
    adam_x = [-2.5, -1.8, -1.0, -0.4, 0]
    adam_y = [1.5, 0.5, 0.1, 0.02, 0]
    ax.plot(adam_x, adam_y, color=TEAL, marker='^', markersize=5, lw=2.8, label="AdamW (Adaptive Per-Coordinate Scaling)")
    
    ax.scatter([0], [0], color=GOLD, marker='*', s=160, zorder=6, label="Global Minimum")
    ax.set_title("Optimization Trajectories Across an Ill-Conditioned Ravine", fontsize=11, fontweight='bold', color=NAVY, pad=12)
    ax.set_xlabel("Parameter $\\theta_1$ (Low Curvature)", fontsize=9.5, fontweight='bold')
    ax.set_ylabel("Parameter $\\theta_2$ (High Curvature)", fontsize=9.5, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(framealpha=0.9, fontsize=8.5, loc='upper right')
    
    save_fig(fig, "deep_optimizers_trajectories.png")
except Exception as e:
    print(f"Error in 15: {e}")

# =====================================================================
# 16. Ch 3.6: PyTorch DDP Ring-AllReduce (ch36_pytorch_production.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.axis('off')
    ax.set_title("PyTorch Distributed Data Parallel (DDP): Ring-AllReduce Topology", fontsize=11, fontweight='bold', color=NAVY, pad=12)
    
    gpos = [(-1.2, 1.2), (1.2, 1.2), (1.2, -1.2), (-1.2, -1.2)]
    gnames = ["GPU 0\nRank 0", "GPU 1\nRank 1", "GPU 2\nRank 2", "GPU 3\nRank 3"]
    
    for (gx, gy), name in zip(gpos, gnames):
        gbox = patches.FancyBboxPatch((gx-0.6, gy-0.45), 1.2, 0.9, boxstyle="round,pad=0.04", fc='#e0f2fe', ec=BLUE, lw=2)
        ax.add_patch(gbox)
        ax.text(gx, gy, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)
    
    # Ring arrows
    def draw_ring_arrow(ax, p1, p2, col=TEAL):
        ax.annotate('', xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="-|>", lw=2.5, color=col, mutation_scale=15))
    
    draw_ring_arrow(ax, (-0.5, 1.2), (0.5, 1.2))
    draw_ring_arrow(ax, (1.2, 0.65), (1.2, -0.65))
    draw_ring_arrow(ax, (0.5, -1.2), (-0.5, -1.2))
    draw_ring_arrow(ax, (-1.2, -0.65), (-1.2, 0.65))
    
    # Center text
    cbox = patches.FancyBboxPatch((-0.9, -0.4), 1.8, 0.8, boxstyle="round,pad=0.03", fc='#fef3c7', ec=GOLD, lw=1.5)
    ax.add_patch(cbox)
    ax.text(0, 0.1, "Bandwidth-Optimal Ring", ha='center', va='center', fontsize=8, fontweight='bold', color='#9a3412')
    ax.text(0, -0.2, r"Total Transfer: $2 \cdot \frac{N-1}{N} \cdot S$", ha='center', va='center', fontsize=7.5, color=NAVY)
    
    save_fig(fig, "ddp_ring_allreduce.png")
except Exception as e:
    print(f"Error in 16: {e}")

# =====================================================================
# 17. Ch 3.7: JAX Transformation Pipeline (ch37_jax_functional_dl.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    ax.set_title("JAX Functional Transformation Pipeline: From Python to Accelerated XLA HLO", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    steps = [
        ("Pure Python\nFunction f(x)", "#e2e8f0", BLUE),
        ("jax.grad\n(Auto-Diff AD)", "#fed7aa", ORANGE),
        ("jax.vmap\n(Auto-Batching)", "#dbeafe", CYAN),
        ("jax.jit\n(XLA Compiler)", "#dcfce7", TEAL),
        ("Fused GPU / TPU\nKernel Execution", "#fef3c7", GOLD)
    ]
    
    for i, (text, fc, ec) in enumerate(steps):
        bx = patches.FancyBboxPatch((i*2.1 + 0.2, 0.8), 1.8, 1.8, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=1.8)
        ax.add_patch(bx)
        ax.text(i*2.1 + 1.1, 1.7, text, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
        
        if i < len(steps) - 1:
            ax.annotate('', xy=(i*2.1 + 2.1, 1.7), xytext=(i*2.1 + 1.9, 1.7),
                        arrowprops=dict(arrowstyle="->", lw=2.2, color=NAVY))
    
    save_fig(fig, "jax_primitives_pipeline.png")
except Exception as e:
    print(f"Error in 17: {e}")

# =====================================================================
# 18. Ch 4.3: VAE vs GAN Architectures (ch43_vaes_gans.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 4.6))
    
    # VAE
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 2)
    ax1.axis('off')
    ax1.set_title("Variational Autoencoder (VAE): Latent Reparameterization Trick", fontsize=10, fontweight='bold', color=NAVY)
    
    def draw_box(ax, x, y, w, h, text, fc='#e0f2fe', ec=BLUE):
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=7.5, fontweight='bold', color=NAVY)
    
    draw_box(ax1, 0.5, 0.5, 1.2, 1.0, "Input x")
    ax1.annotate('', xy=(2.2, 1.0), xytext=(1.7, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    draw_box(ax1, 2.2, 0.5, 1.8, 1.0, "Encoder\nq(z|x)")
    ax1.annotate('', xy=(4.5, 1.0), xytext=(4.0, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    draw_box(ax1, 4.5, 0.5, 2.2, 1.0, r"z = \mu + \sigma \odot \epsilon" + "\n(\\epsilon ~ N(0, I))", fc='#fef3c7', ec=GOLD)
    ax1.annotate('', xy=(7.2, 1.0), xytext=(6.7, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    draw_box(ax1, 7.2, 0.5, 1.8, 1.0, "Decoder\np(x|z)")
    ax1.annotate('', xy=(9.5, 1.0), xytext=(9.0, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    draw_box(ax1, 9.5, 0.5, 1.0, 1.0, "Recon x'")
    
    # GAN
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 2)
    ax2.axis('off')
    ax2.set_title("Generative Adversarial Network (GAN): Minimax Adversarial Game", fontsize=10, fontweight='bold', color=NAVY)
    
    draw_box(ax2, 0.5, 0.5, 1.5, 1.0, "Noise z\n~ N(0, I)")
    ax2.annotate('', xy=(2.5, 1.0), xytext=(2.0, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    draw_box(ax2, 2.5, 0.5, 2.0, 1.0, "Generator G(z)", fc='#fed7aa', ec=ORANGE)
    ax2.annotate('', xy=(5.2, 1.0), xytext=(4.5, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    draw_box(ax2, 5.2, 0.5, 2.4, 1.0, "Discriminator D\n(Real vs Fake)", fc='#dcfce7', ec=TEAL)
    ax2.annotate('', xy=(8.3, 1.0), xytext=(7.6, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    draw_box(ax2, 8.3, 0.5, 1.4, 1.0, "Probability\nP(Real)")
    
    save_fig(fig, "vae_gan_architectures.png")
except Exception as e:
    print(f"Error in 18: {e}")

# =====================================================================
# 19. Ch 4.6: Whisper Audio Intelligence Pipeline (ch46_audio_whisper.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.0)
    ax.axis('off')
    ax.set_title("Whisper Architecture: From Raw Audio Waveform to Multilingual Tokens", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    modules = [
        ("Raw Audio\n16 kHz Waveform", "#e2e8f0", BLUE),
        ("80-Channel\nLog-Mel Spectrogram", "#fed7aa", ORANGE),
        ("2x 1D Conv\nStride 2 Stem", "#dbeafe", CYAN),
        ("Audio Transformer\nEncoder Blocks", "#dcfce7", TEAL),
        ("Cross-Attention\nText Decoder", "#fef3c7", GOLD)
    ]
    
    for i, (text, fc, ec) in enumerate(modules):
        bx = patches.FancyBboxPatch((i*2.1 + 0.2, 1.0), 1.8, 1.8, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=1.8)
        ax.add_patch(bx)
        ax.text(i*2.1 + 1.1, 1.9, text, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
        
        if i < len(modules) - 1:
            ax.annotate('', xy=(i*2.1 + 2.1, 1.9), xytext=(i*2.1 + 1.9, 1.9),
                        arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
            
    ax.text(5.25, 0.2, "Autoregressive Emission: Timestamp Tokens | Language ID | Transcribed Text", ha='center', va='center', fontsize=8.5, fontweight='bold', color=BLUE,
            bbox=dict(boxstyle="round,pad=0.2", fc='white', ec=BORDER))
    
    save_fig(fig, "whisper_audio_pipeline.png")
except Exception as e:
    print(f"Error in 19: {e}")

# =====================================================================
# 20. Ch 5.2: BPE Tokenization Flow (ch52_tokenization_huggingface.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title("Byte-Pair Encoding (BPE): Subword Merging & Token Vocabulary", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Step 1: Characters
    ax.text(1.5, 3.8, "1. Initial Raw Character Tokens", fontsize=9, fontweight='bold', color=BLUE)
    tokens_c = ["l", "o", "w", "e", "s", "t"]
    for i, c in enumerate(tokens_c):
        b = patches.Rectangle((0.5 + i*0.8, 2.9), 0.7, 0.6, fc='#f1f5f9', ec=BORDER, lw=1.2)
        ax.add_patch(b)
        ax.text(0.5 + i*0.8 + 0.35, 3.2, f"'{c}'", ha='center', va='center', fontsize=8.5, color=NAVY)
        
    # Step 2: Merge 1
    ax.text(1.5, 2.3, "2. Most Frequent Pair ('e', 's') -> 'es'", fontsize=9, fontweight='bold', color=TEAL)
    t2 = ["l", "o", "w", "es", "t"]
    for i, c in enumerate(t2):
        col = '#dcfce7' if c == 'es' else '#f1f5f9'
        b = patches.Rectangle((0.5 + i*0.9, 1.4), 0.8, 0.6, fc=col, ec=TEAL if c=='es' else BORDER, lw=1.5)
        ax.add_patch(b)
        ax.text(0.5 + i*0.9 + 0.4, 1.7, f"'{c}'", ha='center', va='center', fontsize=8.5, color=NAVY)
        
    # Step 3: Merge 2
    ax.text(1.5, 0.8, "3. Iterative Subword Token ('es', 't') -> 'est'", fontsize=9, fontweight='bold', color=ORANGE)
    t3 = ["l", "o", "w", "est"]
    for i, c in enumerate(t3):
        col = '#fed7aa' if c == 'est' else '#f1f5f9'
        b = patches.Rectangle((0.5 + i*1.0, -0.1), 0.9, 0.6, fc=col, ec=ORANGE if c=='est' else BORDER, lw=1.5)
        ax.add_patch(b)
        ax.text(0.5 + i*1.0 + 0.45, 0.2, f"'{c}'", ha='center', va='center', fontsize=8.5, color=NAVY)
        
    # Right side: Vocab & ID lookup
    v_box = patches.FancyBboxPatch((6.0, 0.3), 3.2, 3.5, boxstyle="round,pad=0.03", fc='#fef3c7', ec=GOLD, lw=1.8)
    ax.add_patch(v_box)
    ax.text(7.6, 3.4, "Vocabulary ID Lookup", ha='center', va='center', fontsize=9, fontweight='bold', color='#854d0e')
    ax.text(7.6, 2.2, "'low' -> ID 4501\n'est' -> ID 1289\n'transformer' -> ID 38102\n\nVector Embedding Matrix\nLookup: E[ID, :]", ha='center', va='center', fontsize=8, color=NAVY, linespacing=1.3)
    
    save_fig(fig, "bpe_tokenization_flow.png")
except Exception as e:
    print(f"Error in 20: {e}")

# =====================================================================
# 21. Ch 5.4: GraphRAG Hybrid Retrieval (ch54_llamaindex_graphrag.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title("GraphRAG: Knowledge Graph Entities & Dense Vector Fusion", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Query box
    qbox = patches.FancyBboxPatch((0.2, 1.8), 2.0, 1.0, boxstyle="round,pad=0.03", fc='#e0f2fe', ec=BLUE, lw=2)
    ax.add_patch(qbox)
    ax.text(1.2, 2.3, "User Query\n& Concept Extractor", ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)
    
    # Dense Vector Branch (Top)
    ax.annotate('', xy=(3.2, 3.2), xytext=(2.2, 2.5), arrowprops=dict(arrowstyle="->", lw=2, color=CYAN))
    vbox = patches.FancyBboxPatch((3.2, 2.7), 2.8, 1.1, boxstyle="round,pad=0.03", fc='#dbeafe', ec=CYAN, lw=1.8)
    ax.add_patch(vbox)
    ax.text(4.6, 3.25, "Dense Semantic Retrieval\n(k-NN Chunk Similarity)", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    # Knowledge Graph Branch (Bottom)
    ax.annotate('', xy=(3.2, 1.2), xytext=(2.2, 2.1), arrowprops=dict(arrowstyle="->", lw=2, color=TEAL))
    gbox = patches.FancyBboxPatch((3.2, 0.7), 2.8, 1.1, boxstyle="round,pad=0.03", fc='#dcfce7', ec=TEAL, lw=1.8)
    ax.add_patch(gbox)
    ax.text(4.6, 1.25, "Graph Subgraph Traversal\n(Entities, Relations, Communities)", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    # Fusion & Reranking
    ax.annotate('', xy=(7.0, 2.3), xytext=(6.0, 3.1), arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
    ax.annotate('', xy=(7.0, 2.3), xytext=(6.0, 1.4), arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
    
    fbox = patches.FancyBboxPatch((7.0, 1.5), 3.0, 1.6, boxstyle="round,pad=0.03", fc='#fef3c7', ec=GOLD, lw=2)
    ax.add_patch(fbox)
    ax.text(8.5, 2.5, "Hybrid Context Reranker", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#854d0e')
    ax.text(8.5, 1.9, "Entity graph facts +\nDense text evidence ->\nSynthesized Answer", ha='center', va='center', fontsize=7.5, color=NAVY)
    
    save_fig(fig, "graphrag_hybrid_retrieval.png")
except Exception as e:
    print(f"Error in 21: {e}")

# =====================================================================
# 22. Ch 5.6: RLHF vs DPO Alignment (ch56_alignment_rlhf_dpo.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    
    # Left: 3-Stage RLHF
    ax1.set_xlim(-0.5, 5.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.axis('off')
    ax1.set_title("Classic 3-Stage RLHF (PPO)", fontsize=10.5, fontweight='bold', color=NAVY)
    
    b1 = patches.FancyBboxPatch((0.5, 3.4), 4.2, 0.7, boxstyle="round,pad=0.02", fc='#e0f2fe', ec=BLUE, lw=1.5)
    ax1.add_patch(b1)
    ax1.text(2.6, 3.75, "Stage 1: Supervised Fine-Tuning (SFT)", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    ax1.annotate('', xy=(2.6, 2.6), xytext=(2.6, 3.4), arrowprops=dict(arrowstyle="->", lw=1.8, color=GRAY))
    
    b2 = patches.FancyBboxPatch((0.5, 1.9), 4.2, 0.7, boxstyle="round,pad=0.02", fc='#fed7aa', ec=ORANGE, lw=1.5)
    ax1.add_patch(b2)
    ax1.text(2.6, 2.25, "Stage 2: Reward Model Training r(x, y)", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    ax1.annotate('', xy=(2.6, 1.1), xytext=(2.6, 1.9), arrowprops=dict(arrowstyle="->", lw=1.8, color=GRAY))
    
    b3 = patches.FancyBboxPatch((0.5, 0.4), 4.2, 0.7, boxstyle="round,pad=0.02", fc='#dcfce7', ec=TEAL, lw=1.5)
    ax1.add_patch(b3)
    ax1.text(2.6, 0.75, "Stage 3: PPO Actor-Critic + KL Penalty", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    # Right: Direct Preference Optimization (DPO)
    ax2.set_xlim(-0.5, 5.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.axis('off')
    ax2.set_title("Direct Preference Optimization (DPO)", fontsize=10.5, fontweight='bold', color=NAVY)
    
    dpobox = patches.FancyBboxPatch((0.5, 1.2), 4.2, 2.2, boxstyle="round,pad=0.03", fc='#fef3c7', ec=GOLD, lw=2)
    ax2.add_patch(dpobox)
    ax2.text(2.6, 3.0, "Direct Loss: No Reward Model Needed!", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#854d0e')
    ax2.text(2.6, 2.1, r"$\mathcal{L}_{DPO} = -\mathbb{E} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} \right.\right.$" + "\n" +
             r"$\left.\left. - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)} \right) \right]$", ha='center', va='center', fontsize=7.5, color=NAVY)
    ax2.text(2.6, 1.5, "Closed-form exact implicit reward\nUltra-stable training & lower VRAM", ha='center', va='center', fontsize=7.5, color=TEAL, fontweight='bold')
    
    save_fig(fig, "alignment_rlhf_vs_dpo.png")
except Exception as e:
    print(f"Error in 22: {e}")

# =====================================================================
# 23. Ch 5.7: LCEL Streaming DAG (ch57_langchain_lcel.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.0))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    ax.set_title("LangChain Expression Language (LCEL): Declarative Streaming Pipeline", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    lcel_steps = [
        ("Input Prompt\nDict / Message", "#e2e8f0", BLUE),
        ("ChatPromptTemplate\n(Formatted Text)", "#dbeafe", CYAN),
        ("ChatModel (LLM)\nAsync Token Stream", "#fed7aa", ORANGE),
        ("OutputParser\n(Pydantic Schema)", "#dcfce7", TEAL),
        ("Final Verified\nStructured Output", "#fef3c7", GOLD)
    ]
    
    for i, (text, fc, ec) in enumerate(lcel_steps):
        bx = patches.FancyBboxPatch((i*2.1 + 0.2, 0.8), 1.8, 1.8, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=1.8)
        ax.add_patch(bx)
        ax.text(i*2.1 + 1.1, 1.7, text, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
        
        if i < len(lcel_steps) - 1:
            ax.annotate('', xy=(i*2.1 + 2.1, 1.7), xytext=(i*2.1 + 1.9, 1.7),
                        arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
            ax.text(i*2.1 + 2.0, 2.0, "|", ha='center', fontsize=12, fontweight='bold', color=BLUE)
            
    save_fig(fig, "lcel_runnable_dag.png")
except Exception as e:
    print(f"Error in 23: {e}")

# =====================================================================
# 24. Ch 5.9: Autonomous Coding Agent ReAct Loop (ch59_coding_agents.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.axis('off')
    ax.set_title("Autonomous Coding Agent: ReAct Self-Correction Loop", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    nodes = [
        (0, 1.5, "THOUGHT\nReason about test failure\n& formulate patch", "#dbeafe", BLUE),
        (1.5, 0, "ACTION\nExecute Tool:\nEdit file / Run bash", "#fed7aa", ORANGE),
        (0, -1.5, "OBSERVATION\nInspect stdout, exit code\n& syntax linter", "#dcfce7", TEAL),
        (-1.5, 0, "REFLECTION\nDid the test pass?\nSelf-correct if error", "#fef3c7", GOLD)
    ]
    
    for x, y, text, fc, ec in nodes:
        bx = patches.FancyBboxPatch((x-0.7, y-0.45), 1.4, 0.9, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=1.8)
        ax.add_patch(bx)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5, fontweight='bold', color=NAVY)
        
    # Directed circular arrows
    ax.annotate('', xy=(1.0, 0.6), xytext=(0.6, 1.2), arrowprops=dict(arrowstyle="->", lw=2.2, color=NAVY))
    ax.annotate('', xy=(0.6, -1.2), xytext=(1.2, -0.6), arrowprops=dict(arrowstyle="->", lw=2.2, color=NAVY))
    ax.annotate('', xy=(-1.0, -0.6), xytext=(-0.6, -1.2), arrowprops=dict(arrowstyle="->", lw=2.2, color=NAVY))
    ax.annotate('', xy=(-0.6, 1.2), xytext=(-1.2, 0.6), arrowprops=dict(arrowstyle="->", lw=2.2, color=NAVY))
    
    save_fig(fig, "react_coding_agent_loop.png")
except Exception as e:
    print(f"Error in 24: {e}")

# =====================================================================
# 25. Ch 6.1: MLOps Experiment Tracking & Model Registry (ch61_experiment_tracking.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.2)
    ax.axis('off')
    ax.set_title("MLOps Lifecycle: From Experiment Tracking to Staged Model Registry", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Tracking
    tbox = patches.FancyBboxPatch((0.2, 0.8), 3.4, 3.0, boxstyle="round,pad=0.04", fc='#e0f2fe', ec=BLUE, lw=2)
    ax.add_patch(tbox)
    ax.text(1.9, 3.4, "Experiment Tracking (Runs)", ha='center', fontsize=9.5, fontweight='bold', color=BLUE)
    ax.text(1.9, 2.1, "• Hyperparameters & Configs\n• Loss & Accuracy Curves\n• Git Commit SHA & Seeds\n• Weights Checkpoint Artifacts\n• System GPU / RAM metrics", ha='center', fontsize=8, color=NAVY, linespacing=1.3)
    
    # Arrow to Registry
    ax.annotate('', xy=(4.6, 2.3), xytext=(3.8, 2.3), arrowprops=dict(arrowstyle="->", lw=2.5, color=NAVY))
    
    # Model Registry
    rbox = patches.FancyBboxPatch((4.8, 0.8), 5.2, 3.0, boxstyle="round,pad=0.04", fc='#f8fafc', ec=TEAL, lw=2)
    ax.add_patch(rbox)
    ax.text(7.4, 3.4, "Central Model Registry Stages", ha='center', fontsize=9.5, fontweight='bold', color=TEAL)
    
    stages = [
        ("v1.0 (Archived)", "#f1f5f9", GRAY),
        ("v2.0 (Production Live)", "#dcfce7", TEAL),
        ("v2.1 (Staging / Canary)", "#fef3c7", GOLD)
    ]
    for j, (sname, sfc, sec) in enumerate(stages):
        sb = patches.FancyBboxPatch((5.2, 2.3 - j*0.7), 4.4, 0.55, boxstyle="round,pad=0.02", fc=sfc, ec=sec, lw=1.5)
        ax.add_patch(sb)
        ax.text(7.4, 2.55 - j*0.7, sname, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
        
    save_fig(fig, "mlops_experiment_registry.png")
except Exception as e:
    print(f"Error in 25: {e}")

# =====================================================================
# 26. Ch 6.2: Feature Store Architecture (ch62_feature_stores.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title("Enterprise Feature Store: Dual Storage for Training & Inference Consistency", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Sources
    sbox = patches.FancyBboxPatch((0.2, 1.2), 2.2, 2.0, boxstyle="round,pad=0.03", fc='#f1f5f9', ec=BORDER, lw=1.8)
    ax.add_patch(sbox)
    ax.text(1.3, 2.5, "Data Sources", ha='center', fontsize=9, fontweight='bold', color=NAVY)
    ax.text(1.3, 1.8, "Batch Lakehouse\n+\nStreaming Kafka", ha='center', fontsize=8, color=BLUE)
    
    # Dual store branches
    ax.annotate('', xy=(3.4, 3.2), xytext=(2.4, 2.5), arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
    ax.annotate('', xy=(3.4, 1.2), xytext=(2.4, 1.9), arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
    
    # Offline
    offbox = patches.FancyBboxPatch((3.4, 2.5), 3.2, 1.5, boxstyle="round,pad=0.03", fc='#dbeafe', ec=BLUE, lw=1.8)
    ax.add_patch(offbox)
    ax.text(5.0, 3.6, "OFFLINE STORE (Parquet)", ha='center', fontsize=8.5, fontweight='bold', color=BLUE)
    ax.text(5.0, 3.0, "Point-in-time correct joins\nZero data leakage for training", ha='center', fontsize=7.5, color=NAVY)
    
    # Online
    onbox = patches.FancyBboxPatch((3.4, 0.5), 3.2, 1.5, boxstyle="round,pad=0.03", fc='#dcfce7', ec=TEAL, lw=1.8)
    ax.add_patch(onbox)
    ax.text(5.0, 1.6, "ONLINE STORE (Redis)", ha='center', fontsize=8.5, fontweight='bold', color=TEAL)
    ax.text(5.0, 1.0, "Sub-millisecond KV lookups\nReal-time inference serving", ha='center', fontsize=7.5, color=NAVY)
    
    # Consumers
    ax.annotate('', xy=(7.2, 3.2), xytext=(6.6, 3.2), arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
    ax.text(8.2, 3.2, "Model Training\n(PyTorch / XGBoost)", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    ax.annotate('', xy=(7.2, 1.2), xytext=(6.6, 1.2), arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
    ax.text(8.2, 1.2, "Real-Time API\n(FastAPI / Triton)", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    save_fig(fig, "feature_store_architecture.png")
except Exception as e:
    print(f"Error in 26: {e}")

# =====================================================================
# 27. Ch 6.3: Multi-Stage Docker Builds for AI (ch63_containerization_docker.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.4))
    
    # Left: Builder Stage
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.axis('off')
    ax1.set_title("Stage 1: Build Image (Heavy)", fontsize=10.5, fontweight='bold', color=NAVY)
    
    b1 = patches.FancyBboxPatch((0.2, 0.4), 4.0, 3.6, boxstyle="round,pad=0.04", fc='#fee2e2', ec=RED, lw=2)
    ax1.add_patch(b1)
    ax1.text(2.2, 3.5, "nvidia/cuda:12.4-devel (~18 GB)", ha='center', fontsize=9, fontweight='bold', color=RED)
    ax1.text(2.2, 2.0, "• Complete CUDA compiler (nvcc)\n• C++ headers & build tools (gcc)\n• pip build wheel dependencies\n• Compiled binary artifacts\n• Not needed in production!", ha='center', fontsize=8, color=NAVY, linespacing=1.3)
    
    # Right: Production Runtime
    ax2.set_xlim(-0.5, 4.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.axis('off')
    ax2.set_title("Stage 2: Slim Production Image", fontsize=10.5, fontweight='bold', color=NAVY)
    
    b2 = patches.FancyBboxPatch((0.2, 0.4), 4.0, 3.6, boxstyle="round,pad=0.04", fc='#dcfce7', ec=TEAL, lw=2)
    ax2.add_patch(b2)
    ax2.text(2.2, 3.5, "python:3.11-slim (~2.1 GB)", ha='center', fontsize=9, fontweight='bold', color=TEAL)
    ax2.text(2.2, 2.0, "• COPY --from=builder /opt/venv\n• Stripped shared libraries (.so)\n• Application inference code\n• 88% image size reduction!\n• Minimal security attack surface", ha='center', fontsize=8, color=NAVY, linespacing=1.3)
    
    save_fig(fig, "docker_multistage_cuda.png")
except Exception as e:
    print(f"Error in 27: {e}")

# =====================================================================
# 28. Ch 6.5: Drift Observability Pipeline (ch65_drift_observability.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.0)
    ax.axis('off')
    ax.set_title("Model Drift Observability: Detection & Automated Retraining Loop", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    d_steps = [
        ("Live Production\nTelemetry (X, y)", "#e2e8f0", BLUE),
        ("Statistical Drift Engine\n(PSI > 0.2, KS-Test)", "#fed7aa", ORANGE),
        ("Threshold Alerting\nTrigger Retrain Job", "#fee2e2", RED),
        ("Automated CI/CD\nRetraining Pipeline", "#dbeafe", CYAN),
        ("Canary Rollout\n& Shadow Testing", "#dcfce7", TEAL)
    ]
    
    for i, (text, fc, ec) in enumerate(d_steps):
        bx = patches.FancyBboxPatch((i*2.1 + 0.2, 1.0), 1.8, 1.8, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=1.8)
        ax.add_patch(bx)
        ax.text(i*2.1 + 1.1, 1.9, text, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
        
        if i < len(d_steps) - 1:
            ax.annotate('', xy=(i*2.1 + 2.1, 1.9), xytext=(i*2.1 + 1.9, 1.9),
                        arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))
            
    # Feedback loop arrow
    ax.annotate('', xy=(1.1, 0.8), xytext=(9.5, 0.8),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=TEAL, connectionstyle="arc3,rad=-0.15"))
    ax.text(5.3, 0.2, "Continuous Feedback: Deployed Model Returns to Monitoring Loop", ha='center', fontsize=8, fontweight='bold', color=TEAL)
    
    save_fig(fig, "drift_observability_pipeline.png")
except Exception as e:
    print(f"Error in 28: {e}")

# =====================================================================
# 29. Ch 7.2: HNSW Hierarchical Vector Graph (ch72_vector_search_scale.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title("Hierarchical Navigable Small World (HNSW) Vector Search", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    # Layer 2 (Top, sparse)
    ax.text(0.5, 3.8, "Layer 2 (Coarse Skip List): Fast Greedy Jump", fontsize=8.5, fontweight='bold', color=RED)
    ax.plot([2, 7], [3.3, 3.3], color=RED, lw=2, marker='o', markersize=6)
    
    # Layer 1 (Medium)
    ax.text(0.5, 2.5, "Layer 1 (Intermediate): Neighborhood Exploration", fontsize=8.5, fontweight='bold', color=ORANGE)
    ax.plot([1.5, 3.5, 5.5, 7.5], [2.0, 2.0, 2.0, 2.0], color=ORANGE, lw=1.8, marker='o', markersize=5)
    
    # Layer 0 (Dense)
    ax.text(0.5, 1.2, "Layer 0 (Full Proximity Graph): Exact k-NN Search", fontsize=8.5, fontweight='bold', color=TEAL)
    pts = np.linspace(1, 8.5, 8)
    ax.plot(pts, np.ones_like(pts)*0.7, color=TEAL, lw=1.5, marker='o', markersize=4)
    
    # Downward search path
    ax.annotate('', xy=(3.5, 2.1), xytext=(2.0, 3.2), arrowprops=dict(arrowstyle="->", lw=2, color=BLUE, linestyle='--'))
    ax.annotate('', xy=(4.2, 0.8), xytext=(3.5, 1.9), arrowprops=dict(arrowstyle="->", lw=2, color=BLUE, linestyle='--'))
    
    ax.text(5.0, -0.2, "O(log N) Search Complexity: Top-down hierarchical zoom from coarse to fine", ha='center', fontsize=8, fontweight='bold', color=NAVY,
            bbox=dict(boxstyle="round,pad=0.2", fc='#f1f5f9', ec=BORDER))
    
    save_fig(fig, "hnsw_hierarchical_graph.png")
except Exception as e:
    print(f"Error in 29: {e}")

# =====================================================================
# 30. Ch 8.2: Test-Time Compute & Search Trees (ch82_test_time_compute.html)
# =====================================================================
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.4))
    
    # Left: Linear Chain-of-Thought
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(-0.5, 4.5)
    ax1.axis('off')
    ax1.set_title("Greedy Chain-of-Thought", fontsize=10.5, fontweight='bold', color=NAVY)
    
    for i in range(4):
        b = patches.FancyBboxPatch((1.0, 3.4 - i*1.0), 2.2, 0.6, boxstyle="round,pad=0.02", fc='#e0f2fe', ec=BLUE, lw=1.5)
        ax1.add_patch(b)
        ax1.text(2.1, 3.7 - i*1.0, f"Reasoning Step {i+1}", ha='center', va='center', fontsize=8, color=NAVY)
        if i < 3:
            ax1.annotate('', xy=(2.1, 3.4 - (i+1)*1.0 + 0.6), xytext=(2.1, 3.4 - i*1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax1.text(2.1, -0.2, "Single path: Errors compound", ha='center', fontsize=7.5, color=RED, fontweight='bold')
    
    # Right: Tree of Thoughts / MCTS with PRM
    ax2.set_xlim(-0.5, 5.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.axis('off')
    ax2.set_title("Tree Search + Process Reward Model (PRM)", fontsize=10.5, fontweight='bold', color=NAVY)
    
    # Root
    b_root = patches.FancyBboxPatch((1.8, 3.6), 1.8, 0.6, boxstyle="round,pad=0.02", fc='#e0f2fe', ec=BLUE, lw=1.5)
    ax2.add_patch(b_root)
    ax2.text(2.7, 3.9, "Problem State", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    
    # Level 1 branches
    b_left = patches.FancyBboxPatch((0.5, 2.2), 1.6, 0.6, boxstyle="round,pad=0.02", fc='#fee2e2', ec=RED, lw=1.5)
    ax2.add_patch(b_left)
    ax2.text(1.3, 2.5, "Path A (PRM: 0.1)\n[Pruned]", ha='center', va='center', fontsize=7, color=RED)
    
    b_right = patches.FancyBboxPatch((3.0, 2.2), 1.6, 0.6, boxstyle="round,pad=0.02", fc='#dcfce7', ec=TEAL, lw=1.5)
    ax2.add_patch(b_right)
    ax2.text(3.8, 2.5, "Path B (PRM: 0.95)\n[Expanded]", ha='center', va='center', fontsize=7, color=TEAL)
    
    ax2.annotate('', xy=(1.3, 2.8), xytext=(2.2, 3.6), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax2.annotate('', xy=(3.8, 2.8), xytext=(3.2, 3.6), arrowprops=dict(arrowstyle="->", lw=1.5))
    
    # Level 2 leaves
    b_leaf = patches.FancyBboxPatch((3.0, 0.8), 1.6, 0.6, boxstyle="round,pad=0.02", fc='#fef3c7', ec=GOLD, lw=1.5)
    ax2.add_patch(b_leaf)
    ax2.text(3.8, 1.1, "Verified Solution\n(Self-Consistency)", ha='center', va='center', fontsize=7, fontweight='bold', color=NAVY)
    ax2.annotate('', xy=(3.8, 1.4), xytext=(3.8, 2.2), arrowprops=dict(arrowstyle="->", lw=1.5))
    
    ax2.text(2.7, -0.2, "Test-Time Scaling: Compute scales with search depth", ha='center', fontsize=7.5, color=TEAL, fontweight='bold')
    
    save_fig(fig, "test_time_search_trees.png")
except Exception as e:
    print(f"Error in 30: {e}")

# =====================================================================
# 31. Ch 8.3: Datacenter Energy & Hardware Limits (ch83_energy_hardware_limits.html)
# =====================================================================
try:
    fig, ax = plt.subplots(figsize=(10, 4.4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.5)
    ax.axis('off')
    ax.set_title("The Physical Energy & Hardware Scaling Hierarchy of AI Compute", fontsize=11, fontweight='bold', color=NAVY, pad=10)
    
    scales = [
        ("Silicon Chip TDP\n700W - 1000W\n(Thermal Flux Limit)", 0.8, '#fee2e2', RED),
        ("Server Rack Density\n40 kW - 120 kW\n(Direct Liquid CDU)", 3.2, '#fed7aa', ORANGE),
        ("Data Center Facility\n100 MW - 1 GW\n(PUE ~ 1.15 Target)", 5.6, '#dbeafe', BLUE),
        ("Thermodynamic Limit\nLandauer Boundary\nk_B * T * ln(2)", 8.0, '#fef3c7', GOLD)
    ]
    
    for text, sx, fc, ec in scales:
        bx = patches.FancyBboxPatch((sx, 1.0), 2.1, 2.4, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=2)
        ax.add_patch(bx)
        ax.text(sx + 1.05, 2.2, text, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY, linespacing=1.3)
        
    for i in range(3):
        ax.annotate('', xy=(scales[i+1][1], 2.2), xytext=(scales[i][1] + 2.1, 2.2),
                    arrowprops=dict(arrowstyle="->", lw=2.2, color=NAVY))
        
    save_fig(fig, "ai_datacenter_energy_limits.png")
except Exception as e:
    print(f"Error in 31: {e}")

print("\nAll 31 diagram generation functions completed!")
