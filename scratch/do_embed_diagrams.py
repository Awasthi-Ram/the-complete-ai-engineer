"""
do_embed_diagrams.py — Accurately locates sections and embeds all 20 diagrams
into the corresponding book_builder chapters.
"""
import os
import re

INSERTIONS = [
    {
        'file': 'book_builder/ch03_ai_toolchain.html',
        'heading': 'Memory Layouts &amp; Strided Offset Formula',
        'img': 'numpy_strides_diagram.png',
        'fig': '0.3.1',
        'caption': 'Physical contiguous RAM allocation versus multidimensional logical views in NumPy. A 1D array of bytes is indexed using shape $(2, 3)$ and strides $(12, 4)$ bytes without data duplication. Transposing an array simply swaps stride metadata, enabling instant $\\mathcal{O}(1)$ zero-copy transformation.'
    },
    {
        'file': 'book_builder/ch11_linear_algebra.html',
        'heading': 'Singular Value Decomposition',
        'img': 'svd_geometry_diagram.png',
        'fig': '1.1.1',
        'caption': 'The geometric transformation of Singular Value Decomposition ($\\mathbf{A} = \\mathbf{U} \\mathbf{\\Sigma} \\mathbf{V}^T$). Any real linear map transforms a unit sphere through an orthogonal rotation ($\\mathbf{V}^T$), axis-aligned stretching by singular values $\\sigma_i$, and an orthogonal rotation ($\\mathbf{U}$) into an ellipsoid in $\\mathbb{R}^m$.'
    },
    {
        'file': 'book_builder/ch12_calculus_autograd.html',
        'heading': 'Automatic Differentiation',
        'img': 'autograd_dag_diagram.png',
        'fig': '1.2.1',
        'caption': 'Computational graph for automatic differentiation. The forward pass evaluates intermediate operations from inputs to scalar loss $L$. The reverse pass traverses adjoints in reverse topological order via Vector-Jacobian Products (VJPs), calculating exact gradients for all parameters simultaneously in a single sweep.'
    },
    {
        'file': 'book_builder/ch15_convex_optimization.html',
        'heading': 'Optimization with Projected Gradient Descent',
        'img': 'optimization_ravine_diagram.png',
        'fig': '1.5.1',
        'caption': 'Optimization dynamics on an ill-conditioned loss surface with high condition number $\\kappa \\gg 1$. Standard SGD oscillates wildly across the steep ravine walls with slow longitudinal progress, while Momentum dampens orthogonal oscillations and accelerates directly toward the minimum.'
    },
    {
        'file': 'book_builder/ch26_svm.html',
        'heading': 'The Maximum Margin Principle',
        'img': 'svm_margin_kernel_diagram.png',
        'fig': '2.6.1',
        'caption': 'Support Vector Machines. Left: The maximum margin separating hyperplane maximizing margin width $2/\\|\\mathbf{w}\\|_2$ bounded by support vectors. Right: The Kernel Trick implicitly projecting non-linearly separable circular data into higher-dimensional space where a linear hyperplane achieves complete separation.'
    },
    {
        'file': 'book_builder/ch210_reinforcement_learning.html',
        'heading': 'Markov Decision Processes',
        'img': 'rl_agent_environment.jpg',
        'fig': '2.10.1',
        'caption': 'The canonical Reinforcement Learning interaction cycle. The agent observes current state $S_t$, takes action $A_t$ sampled from policy $\\pi$, and receives scalar reward $R_{t+1}$ and next state $S_{t+1}$ from the environment transition dynamics $\\mathcal{P}$.'
    },
    {
        'file': 'book_builder/ch31_perceptron_xor.html',
        'heading': 'The XOR Barrier',
        'img': 'xor_linear_separability_diagram.png',
        'fig': '3.1.1',
        'caption': 'The XOR linear separability barrier and hidden layer manifold folding. In the original 2D input space, no single linear decision boundary can separate XOR classes. A single hidden layer with non-linear activation warps the coordinate geometry, making the representations linearly separable.'
    },
    {
        'file': 'book_builder/ch33_backprop_scratch.html',
        'heading': 'Analytical Backpropagation from Scratch',
        'img': 'backprop_matrix_flow_diagram.png',
        'fig': '3.3.1',
        'caption': 'Exact tensor dimension flows and transposition rules in a 2-layer MLP. Notice how backward gradient propagation preserves matrix multiplication conformability: $\\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{W}_1} = \\mathbf{X}^T \\mathbf{\\delta}_1$ yields $[d_{\\text{in}} \\times d_h]$.'
    },
    {
        'file': 'book_builder/ch35_normalization_regularization.html',
        'heading': 'BatchNorm to RMSNorm',
        'img': 'normalization_cubes_diagram.png',
        'fig': '3.5.1',
        'caption': 'Geometric tensor slicing in neural normalization layers across a 3D activation tensor $(N, C, L)$. Batch Normalization normalizes across batch elements $N$; Layer Normalization normalizes across channels $C$ and length $L$ per sample; Instance Normalization normalizes spatially per channel; Group Normalization normalizes across channel sub-groups.'
    },
    {
        'file': 'book_builder/ch41_cnns_resnets.html',
        'heading': 'Convolutional Neural Networks &amp; ResNets',
        'img': 'resnet_block_diagram.png',
        'fig': '4.1.1',
        'caption': 'The canonical ResNet residual block. The identity shortcut connection creates an uninterrupted additive gradient highway $\\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{x}} = \\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{y}} \\cdot \\frac{\\partial \\mathcal{F}}{\\partial \\mathbf{x}} + \\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{y}} \\cdot \\mathbf{I}$, preventing vanishing gradients even in networks exceeding 100+ layers.'
    },
    {
        'file': 'book_builder/ch42_segmentation_unet.html',
        'heading': 'Medical Image Segmentation &amp; U-Net',
        'img': 'unet_architecture_diagram.png',
        'fig': '4.2.1',
        'caption': 'The U-Net encoder-decoder architecture. The contracting left path extracts high-level semantic context, the central bottleneck captures latent representations, and the expansive right path recovers spatial resolution, assisted by horizontal copy-and-crop skip connections.'
    },
    {
        'file': 'book_builder/ch44_diffusion_models.html',
        'heading': 'Generative Visual Synthesis &amp; Diffusion Models',
        'img': 'diffusion_process_diagram.png',
        'fig': '4.4.1',
        'caption': 'The continuous diffusion modeling framework. The forward Markov process progressively corrupts structured image data into pure isotropic Gaussian noise, while the reverse generative process trains a neural score estimator $\\boldsymbol{\\epsilon}_\\theta(\\mathbf{x}_t, t)$ to iteratively remove noise and synthesize sharp images.'
    },
    {
        'file': 'book_builder/ch45_vit_mae.html',
        'heading': 'Vision Transformers &amp; Masked Autoencoders',
        'img': 'vit_architecture_diagram.png',
        'fig': '4.5.1',
        'caption': 'The Vision Transformer (ViT) architecture. An input image is partitioned into non-overlapping $16 \\times 16$ patches, flattened into linear projections, prepended with a learnable [CLS] classification token, augmented with 1D learnable position embeddings, and processed through standard Transformer encoder blocks.'
    },
    {
        'file': 'book_builder/ch55_lora_qlora.html',
        'heading': 'Parameter-Efficient Fine-Tuning: LoRA, QLoRA &amp; DoRA',
        'img': 'lora_architecture_diagram.png',
        'fig': '5.5.1',
        'caption': 'Parameter-Efficient Fine-Tuning with LoRA and QLoRA. The large pre-trained base weight $\\mathbf{W}_0$ is frozen (quantized to 4-bit NormalFloat in QLoRA). Only low-rank matrices $\\mathbf{A}$ and $\\mathbf{B}$ are trained, reducing trainable parameters and optimizer memory by over 99.8%.'
    },
    {
        'file': 'book_builder/ch58_langgraph_agents.html',
        'heading': 'LangGraph &amp; Stateful Multi-Agent Swarms',
        'img': 'langgraph_swarm_diagram.png',
        'fig': '5.8.1',
        'caption': 'LangGraph multi-agent architecture with shared state graphs. A central typed state dictionary is coordinated by a supervisor orchestrator node dispatching tasks to specialized worker nodes (Coder, Reviewer, Researcher) with conditional routing cycles and human-in-the-loop checkpoints.'
    },
    {
        'file': 'book_builder/ch510_llm_serving_vllm.html',
        'heading': 'PagedAttention: Virtual Memory for KV Caches',
        'img': 'paged_attention_diagram.png',
        'fig': '5.10.1',
        'caption': 'Memory management in LLM serving. Traditional contiguous memory allocation wastes 60-80% of VRAM due to internal and external fragmentation. vLLM PagedAttention applies virtual memory paging to KV caches, dynamically allocating non-contiguous physical memory blocks with near-zero waste.'
    },
    {
        'file': 'book_builder/ch64_triton_serving.html',
        'heading': 'High-Throughput Serving: Triton &amp; TensorRT',
        'img': 'triton_architecture_diagram.png',
        'fig': '6.4.1',
        'caption': 'High-throughput inference server topology in NVIDIA Triton. A dynamic batching scheduler combines asynchronous single-client HTTP/gRPC requests within a microsecond latency window into dense GPU GEMM batches, executing across multi-instance TensorRT engines with zero-copy shared memory.'
    },
    {
        'file': 'book_builder/ch71_recsys_twotower.html',
        'heading': 'Two-Tower Neural Networks',
        'img': 'two_tower_recsys_diagram.png',
        'fig': '7.1.1',
        'caption': 'Two-Tower deep retrieval architecture. The User/Query Tower and Item/Candidate Tower project disparate feature spaces into a shared $d$-dimensional embedding space, enabling sub-10ms candidate retrieval across billions of candidate items via Approximate Nearest Neighbor (HNSW) search.'
    },
    {
        'file': 'book_builder/ch73_edge_ai_quantization.html',
        'heading': 'Edge AI, Model Compression &amp; Quantization',
        'img': 'quantization_mapping_diagram.png',
        'fig': '7.3.1',
        'caption': 'Uniform affine quantization mapping continuous 32-bit floating-point weights into 8-bit integer grids. Calculating the optimal scale $S$ and zero-point $Z$ preserves network dynamic range while slashing memory bandwidth and VRAM requirements by 75%.'
    },
    {
        'file': 'book_builder/ch81_mcp_standard.html',
        'heading': 'The Model Context Protocol (MCP)',
        'img': 'mcp_topology_diagram.png',
        'fig': '8.1.1',
        'caption': 'Model Context Protocol (MCP) architecture. MCP decouples tool development from model providers through a standard JSON-RPC 2.0 interface, allowing any host application (Claude Desktop, IDEs) to seamlessly communicate with decoupled local or remote tool servers.'
    }
]

total_embedded = 0
for entry in INSERTIONS:
    filepath = entry['file']
    keyword = entry['heading']
    img = entry['img']
    fig_num = entry['fig']
    caption = entry['caption']
    
    if not os.path.exists(filepath):
        print(f"  [MISSING] {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if img in content:
        print(f"  [ALREADY PRESENT] {img} in {filepath}")
        continue
        
    # Find heading matching keyword
    m = re.search(rf'<h[234][^>]*>[^<]*?{re.escape(keyword)}[^<]*?</h[234]>', content, re.IGNORECASE)
    if not m:
        # Try looser match
        words = [w for w in keyword.split() if len(w) > 3]
        pattern = rf'<h[234][^>]*>.*?(?:{"|".join(words)}).*?</h[234]>'
        m = re.search(pattern, content, re.IGNORECASE)
        
    if m:
        # Find closing tag of heading or next paragraph
        h_end = m.end()
        # Look for end of the following </p> to place figure naturally after the introductory paragraph
        p_match = re.search(r'</p>', content[h_end:])
        if p_match:
            insert_pos = h_end + p_match.end()
        else:
            insert_pos = h_end
            
        figure_html = f"""

    <!-- FIGURE {fig_num}: {img} -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="{img}" alt="Figure {fig_num}: {img}" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure {fig_num}:</em> {caption}
      </p>
    </div>
"""
        new_content = content[:insert_pos] + figure_html + content[insert_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [SUCCESS] Embedded {img} into {filepath}")
        total_embedded += 1
    else:
        print(f"  [FAILED] Could not find heading for '{keyword}' in {filepath}")

print(f"\nAll done! Successfully embedded {total_embedded} diagrams.")
