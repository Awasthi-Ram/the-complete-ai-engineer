"""
embed_all_diagrams.py — Embeds all 20 publication-grade diagrams into their corresponding
chapter files in book_builder/, ensuring proper styling, figure numbers, and descriptive captions.
"""
import os
import re

DIAGRAM_INSERTIONS = [
    {
        'file': 'book_builder/ch01_how_to_learn.html',
        'target': '<h4>The Roofline Model: Arithmetic Intensity</h4>',
        'position': 'after_block',
        'html': """
    <!-- DIAGRAM: ROOFLINE MODEL & GPU HIERARCHY -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="roofline_model_diagram.png" alt="The Roofline Model & GPU Memory Hierarchy" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 0.1.1:</em> The GPU memory hierarchy pyramid (left) and the Roofline Model performance ceiling (right). Memory-bandwidth bound operations (Softmax, LayerNorm, low-batch generation) lie to the left of the machine balance point $I^*$, while compute-bound operations (GEMM matrix multiplications) saturate peak Tensor Core FLOPs on the right.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch03_ai_toolchain.html',
        'target': '<h3>2. NumPy Vectorization &amp; C-Contiguous Memory Layout</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: NUMPY STRIDED ARRAYS -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="numpy_strides_diagram.png" alt="NumPy Strided Arrays & Memory Layout" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 0.3.1:</em> Physical contiguous RAM allocation versus multidimensional logical views in NumPy. A 1D array of bytes is indexed using shape $(2, 3)$ and strides $(12, 4)$ bytes. Matrix transposition simply swaps stride metadata, achieving instantaneous $\\mathcal{O}(1)$ zero-copy transformation.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch11_linear_algebra.html',
        'target': '<h3>3. Singular Value Decomposition (SVD)</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: SVD GEOMETRY -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="svd_geometry_diagram.png" alt="Geometric Interpretation of SVD" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 1.1.1:</em> The geometric action of Singular Value Decomposition ($\\mathbf{A} = \\mathbf{U} \\mathbf{\\Sigma} \\mathbf{V}^T$). Any real linear transformation decomposes into three fundamental operations: an initial orthogonal coordinate rotation ($\\mathbf{V}^T$), axis stretching by singular values $\\sigma_i$, and an orthogonal rotation ($\\mathbf{U}$) into the target space $\\mathbb{R}^m$.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch12_calculus_autograd.html',
        'target': '<h3>2. Computational Graphs &amp; Automatic Differentiation</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: AUTOGRAD DAG -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="autograd_dag_diagram.png" alt="Computational DAG & Reverse-Mode Autodiff" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 1.2.1:</em> Directed Acyclic Graph (DAG) for automatic differentiation. The forward pass computes intermediate activation values from inputs to the scalar loss $L$. The reverse pass traverses adjoints in reverse topological order via Vector-Jacobian Products (VJPs), calculating exact gradients for all parameters in a single pass.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch15_convex_optimization.html',
        'target': '<h3>2. Gradient Descent &amp; Condition Numbers</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: OPTIMIZATION RAVINE -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="optimization_ravine_diagram.png" alt="Optimization Dynamics in Ill-Conditioned Ravines" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 1.5.1:</em> Optimization trajectories on an ill-conditioned loss surface with high condition number $\\kappa \\gg 1$. Standard SGD oscillates wildly across steep ravine walls with slow longitudinal progress, whereas Momentum dampens orthogonal oscillations and accelerates directly toward the minimum.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch26_svm.html',
        'target': '<h3>1. The Maximum Margin Hyperplane</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: SVM MAXIMUM MARGIN & KERNEL TRICK -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="svm_margin_kernel_diagram.png" alt="SVM Maximum Margin & Kernel Trick" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 2.6.1:</em> Support Vector Machines. Left: The maximum margin separating hyperplane maximizing margin width $2/\\|\\mathbf{w}\\|_2$ bounded by support vectors. Right: The Kernel Trick implicitly projecting non-linearly separable circular data into higher-dimensional space where a linear hyperplane achieves complete separation.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch210_reinforcement_learning.html',
        'target': '<h3>1. The Reinforcement Learning Paradigm &amp; The Markov Decision Process (MDP)</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: RL AGENT ENVIRONMENT MDP -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="rl_agent_environment.jpg" alt="The Reinforcement Learning Agent-Environment Interaction Cycle" style="max-width: 92%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 2.10.1:</em> The canonical Reinforcement Learning interaction cycle. The agent observes current state $S_t$, takes action $A_t$ sampled from policy $\\pi$, and receives scalar reward $R_{t+1}$ and next state $S_{t+1}$ from the environment transition dynamics $\\mathcal{P}$.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch31_perceptron_xor.html',
        'target': '<h3>3. The XOR Barrier: Minsky &amp; Papert\'s Historic Critique</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: XOR LINEAR SEPARABILITY -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="xor_linear_separability_diagram.png" alt="The XOR Linear Separability Barrier & Manifold Folding" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 3.1.1:</em> The XOR linear separability barrier and hidden layer manifold folding. In the original 2D input space, no single linear decision boundary can separate XOR classes. A single hidden layer with non-linear activation warps the coordinate geometry, making the representations linearly separable.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch33_backprop_scratch.html',
        'target': '<h3>2. Matrix Dimension Tracing: The Golden Rule of Neural Backprop</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: BACKPROP MATRIX FLOW -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="backprop_matrix_flow_diagram.png" alt="2-Layer MLP Backpropagation Matrix Dimensions" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 3.3.1:</em> Exact tensor dimension flows and transposition rules in a 2-layer MLP. Notice how backward gradient propagation preserves matrix multiplication conformability: $\\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{W}_1} = \\mathbf{X}^T \\mathbf{\\delta}_1$ yields $[d_{\\text{in}} \\times d_h]$.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch35_normalization_regularization.html',
        'target': '<h3>1. The Internal Covariate Shift &amp; Normalization Zoo</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: NORMALIZATION CUBES -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="normalization_cubes_diagram.png" alt="Tensor Normalization Slicing: Batch, Layer, Instance, Group Norm" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 3.5.1:</em> Geometric tensor slicing in neural normalization layers across a 3D activation tensor $(N, C, L)$. Batch Normalization normalizes across batch elements $N$; Layer Normalization normalizes across channels $C$ and length $L$ per sample; Instance Normalization normalizes spatially per channel; Group Normalization normalizes across channel sub-groups.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch41_cnns_resnets.html',
        'target': '<h3>3. Deep Residual Networks (ResNets): The Identity Highway</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: RESNET BLOCK -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="resnet_block_diagram.png" alt="The ResNet Residual Block & Gradient Highway" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 4.1.1:</em> The canonical ResNet residual block. The identity shortcut connection creates an uninterrupted additive gradient highway $\\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{x}} = \\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{y}} \\cdot \\frac{\\partial \\mathcal{F}}{\\partial \\mathbf{x}} + \\frac{\\partial \\mathcal{L}}{\\partial \\mathbf{y}} \\cdot \\mathbf{I}$, preventing vanishing gradients even in networks exceeding 100+ layers.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch42_segmentation_unet.html',
        'target': '<h3>2. The U-Net Architecture: Contracting Path, Bottleneck &amp; Expansive Path</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: UNET ARCHITECTURE -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="unet_architecture_diagram.png" alt="The U-Net Medical Segmentation Architecture" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 4.2.1:</em> The U-Net encoder-decoder architecture. The contracting left path extracts high-level semantic context, the central bottleneck captures latent representations, and the expansive right path recovers spatial resolution, assisted by horizontal copy-and-crop skip connections.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch44_diffusion_models.html',
        'target': '<h3>1. The Generative Paradigm: From GANs to Diffusion</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: DIFFUSION PROCESS -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="diffusion_process_diagram.png" alt="Forward & Reverse Diffusion Process" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 4.4.1:</em> The continuous diffusion modeling framework. The forward Markov process progressively corrupts structured image data into pure isotropic Gaussian noise, while the reverse generative process trains a neural score estimator $\\boldsymbol{\\epsilon}_\\theta(\\mathbf{x}_t, t)$ to iteratively remove noise and synthesize sharp images.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch45_vit_mae.html',
        'target': '<h3>2. Vision Transformers (ViT): An Image is Worth 16x16 Words</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: VISION TRANSFORMER -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="vit_architecture_diagram.png" alt="Vision Transformer (ViT) Architecture" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 4.5.1:</em> The Vision Transformer (ViT) architecture. An input image is partitioned into non-overlapping $16 \\times 16$ patches, flattened into linear projections, prepended with a learnable [CLS] classification token, augmented with 1D learnable position embeddings, and processed through standard Transformer encoder blocks.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch55_lora_qlora.html',
        'target': '<h3>1. The Parameter Explosion Crisis: Why Full Fine-Tuning Fails at Scale</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: LORA ARCHITECTURE -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="lora_architecture_diagram.png" alt="LoRA & QLoRA Low-Rank Adaptation Architecture" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 5.5.1:</em> Parameter-Efficient Fine-Tuning with LoRA and QLoRA. The large pre-trained base weight $\\mathbf{W}_0$ is frozen (quantized to 4-bit NormalFloat in QLoRA). Only low-rank matrices $\\mathbf{A}$ and $\\mathbf{B}$ are trained, reducing trainable parameters and optimizer memory by over 99.8%.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch58_langgraph_agents.html',
        'target': '<h3>1. The Multi-Agent Architectural Shift</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: LANGGRAPH MULTI-AGENT SWARM -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="langgraph_swarm_diagram.png" alt="LangGraph Stateful Multi-Agent Swarm Architecture" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 5.8.1:</em> LangGraph multi-agent architecture with shared state graphs. A central typed state dictionary is coordinated by a supervisor orchestrator node dispatching tasks to specialized worker nodes (Coder, Reviewer, Researcher) with conditional routing cycles and human-in-the-loop checkpoints.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch510_llm_serving_vllm.html',
        'target': '<h3>1. The KV-Cache Memory Wall</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: PAGEDATTENTION VIRTUAL MEMORY -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="paged_attention_diagram.png" alt="PagedAttention Virtual Memory Architecture in vLLM" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 5.10.1:</em> Memory management in LLM serving. Traditional contiguous memory allocation wastes 60-80% of VRAM due to internal and external fragmentation. vLLM PagedAttention applies virtual memory paging to KV caches, dynamically allocating non-contiguous physical memory blocks with near-zero waste.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch64_triton_serving.html',
        'target': '<h3>1. The High-Throughput Serving Imperative</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: TRITON ARCHITECTURE -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="triton_architecture_diagram.png" alt="NVIDIA Triton Inference Server Dynamic Batching" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 6.4.1:</em> High-throughput inference server topology in NVIDIA Triton. A dynamic batching scheduler combines asynchronous single-client HTTP/gRPC requests within a microsecond latency window into dense GPU GEMM batches, executing across multi-instance TensorRT engines with zero-copy shared memory.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch71_recsys_twotower.html',
        'target': '<h3>1. The Recommendation Funnel: From Billions to Ten</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: TWO TOWER RECSYS -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="two_tower_recsys_diagram.png" alt="Two-Tower Deep Neural Retrieval Architecture" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 7.1.1:</em> Two-Tower deep retrieval architecture. The User/Query Tower and Item/Candidate Tower project disparate feature spaces into a shared $d$-dimensional embedding space, enabling sub-10ms candidate retrieval across billions of candidate items via Approximate Nearest Neighbor (HNSW) search.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch73_edge_ai_quantization.html',
        'target': '<h3>1. The Edge AI Constraint Landscape</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: QUANTIZATION MAPPING -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="quantization_mapping_diagram.png" alt="Uniform Affine Quantization Mapping" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 7.3.1:</em> Uniform affine quantization mapping continuous 32-bit floating-point weights into 8-bit integer grids. Calculating the optimal scale $S$ and zero-point $Z$ preserves network dynamic range while slashing memory bandwidth and VRAM requirements by 75%.
      </p>
    </div>
"""
    },
    {
        'file': 'book_builder/ch81_mcp_standard.html',
        'target': '<h3>1. The Tool-Integration Fragmentation Crisis</h3>',
        'position': 'after_heading',
        'html': """
    <!-- DIAGRAM: MCP TOPOLOGY -->
    <div class="diagram-figure" style="text-align: center; margin: 1.8em 0; page-break-inside: avoid;">
      <img src="mcp_topology_diagram.png" alt="Model Context Protocol (MCP) Topology" style="max-width: 95%; border-radius: 6px; border: 1.5px solid #1b4965; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
      <p style="font-family: var(--font-ui); font-size: 0.85em; color: #555; margin-top: 8px;">
        <em>Figure 8.1.1:</em> Model Context Protocol (MCP) architecture. MCP decouples tool development from model providers through a standard JSON-RPC 2.0 interface, allowing any host application (Claude Desktop, IDEs) to seamlessly communicate with decoupled local or remote tool servers.
      </p>
    </div>
"""
    }
]

inserted_count = 0
for entry in DIAGRAM_INSERTIONS:
    filepath = entry['file']
    target = entry['target']
    html_block = entry['html']
    
    if not os.path.exists(filepath):
        print(f"  [MISSING] File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if already inserted
    img_name = re.search(r'src="([^"]+)"', html_block).group(1)
    if img_name in content:
        print(f"  [EXISTS] Already embedded: {img_name} in {filepath}")
        continue
        
    if target in content:
        # Insert right after target heading
        idx = content.find(target) + len(target)
        new_content = content[:idx] + "\n" + html_block + "\n" + content[idx:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [EMBEDDED] {img_name} into {filepath}")
        inserted_count += 1
    else:
        # Fallback: find <h3> or chapter-body
        print(f"  [WARNING] Target heading not found in {filepath}: '{target}'")

print(f"\nSuccessfully embedded {inserted_count} new diagrams across book chapters!")
