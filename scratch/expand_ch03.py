import os

ch03_content = """<!-- ======================================================================
     CHAPTER 0.3 — THE AI TOOLCHAIN: NUMPY, PANDAS & PYTORCH TENSORS
     ====================================================================== -->
<div class="chapter" id="chapter-0-3">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 0.3</span>
    <h2 class="chapter-title">The AI Toolchain</h2>
    <span class="chapter-subtitle">NumPy SIMD Vectorization, Pandas Data Wrangling &amp; PyTorch GPU Tensors</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Vectors are not just rows of numbers; they are directions in high-dimensional thought."</p>
    <p class="attribution">— Mathematical Machine Learning Principle</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation • Core Pillar</span>

    <!-- SECTION 1: NUMPY & C-BLAS -->
    <h3>1. NumPy &amp; C-BLAS Under the Hood</h3>
    <p>Every modern machine learning framework—from PyTorch and TensorFlow to JAX, Triton, and ONNX—traces its architectural lineage directly to NumPy. At its core, NumPy solves the fundamental limitation of Python: <strong>eliminating the interpreter loop overhead</strong> by delegating heavy mathematical calculations to compiled C, C++, and Fortran libraries (such as OpenBLAS, Intel MKL, or Apple Accelerate).</p>

    <h4>The Anatomy of an <code>ndarray</code></h4>
    <p>A NumPy array (<code>np.ndarray</code>) consists of two distinct components:</p>
    <ol>
      <li><strong>The Data Buffer:</strong> A single, contiguous block of raw binary memory storing elements of a uniform primitive type (e.g. <code>float32</code> or <code>int64</code>).</li>
      <li><strong>The Array Metadata:</strong> A lightweight Python descriptor object containing:
        <ul>
          <li><code>dtype</code>: The data type (e.g., 4 bytes for <code>np.float32</code>).</li>
          <li><code>shape</code>: A tuple defining the dimensions (e.g. <code>(1000, 768)</code>).</li>
          <li><code>strides</code>: A tuple defining the exact number of bytes to step in physical memory to advance by one element along each dimension.</li>
        </ul>
      </li>
    </ol>

    <h4>Memory Layouts &amp; Strided Offset Formula</h4>
    <p>For an $N$-dimensional array with shape $(d_0, d_1, \dots, d_{N-1})$ and strides $(s_0, s_1, \dots, s_{N-1})$, the exact byte offset from the buffer start to element $(i_0, i_1, \dots, i_{N-1})$ is given by the linear affine equation:</p>
    $$\text{Byte Offset}(\mathbf{i}) = \text{base\_offset} + \sum_{k=0}^{N-1} i_k \times s_k$$
    <p>In <strong>Row-Major (C-contiguous) Order</strong>, the last dimension changes fastest in memory: $s_{N-1} = \text{itemsize}$, and $s_k = s_{k+1} \times d_{k+1}$. Because modern CPUs read memory in 64-byte cache lines, traversing an array along its contiguous stride achieves peak throughput. Traversing against the stride causes constant CPU cache misses!</p>

    <div class="key-insight">
      <p><strong>Zero-Copy Array Manipulations:</strong> Because NumPy and PyTorch decouple metadata from the raw memory buffer, operations like <code>reshape()</code>, <code>transpose()</code>, and slicing <code>arr[::2]</code> <strong>never allocate new memory or copy data</strong>! They simply instantiate a new lightweight metadata header with modified shape and strides pointing to the existing memory buffer. Slicing is $O(1)$ instantaneous!</p>
    </div>

    <!-- SECTION 2: BROADCASTING RULES -->
    <h3>2. The Universal Broadcasting Rules</h3>
    <p>Broadcasting is the mathematical mechanism for performing element-wise operations between arrays of different shapes without copying data. To determine compatibility, NumPy and PyTorch compare shapes element-wise, <strong>starting from the trailing (rightmost) dimensions and working backwards</strong>.</p>

    <div class="real-world-box">
      <h4>📐 The Three Immutable Rules of Broadcasting</h4>
      <ol>
        <li><strong>Prepend Dimensions:</strong> If the arrays have a different number of dimensions, prepend 1s to the shape of the shorter array on the left until both shapes have identical length.</li>
        <li><strong>Compatibility Check:</strong> Two dimensions are compatible if they are equal, or if one of them is exactly 1.</li>
        <li><strong>Zero-Stride Virtual Expansion:</strong> Dimensions of size 1 are stretched to match the other array by setting their internal <strong>stride to 0</strong>! The CPU/GPU reads the same single value repeatedly without allocating new memory!</li>
      </ol>
    </div>

    <!-- SECTION 3: PYTORCH GPU MEMORY & DMA -->
    <h3>3. PyTorch Tensor Mechanics &amp; GPU Memory Allocators</h3>
    <p>While NumPy executes SIMD vectorization on CPU registers, PyTorch extends this paradigm across thousands of GPU cores. However, naive data movement between CPU RAM and GPU VRAM introduces severe bottlenecks.</p>

    <h4>Host-to-Device Bottlenecks &amp; Page-Locked (Pinned) Memory</h4>
    <p>Standard operating system memory is <em>pageable</em>: the OS kernel can swap physical RAM pages to disk at any moment. Because the GPU cannot safely access pageable memory via Direct Memory Access (DMA), moving a standard tensor from CPU to GPU requires two copy operations:</p>
    $$\text{Pageable CPU Memory} \xrightarrow{\text{CPU Copy}} \text{Page-Locked Host Buffer} \xrightarrow{\text{PCIe Bus DMA}} \text{GPU VRAM}$$
    <p>By enabling <strong>Pinned Memory</strong> (<code>pin_memory=True</code> in your PyTorch DataLoader), you allocate page-locked host memory directly. This allows the GPU to stream data across the PCIe bus via DMA <strong>completely asynchronously without CPU intervention</strong>, saturating bus bandwidth!</p>

    <h4>The PyTorch Caching Allocator &amp; Fragmentation</h4>
    <p>Calling <code>cudaMalloc</code> directly on an NVIDIA GPU is an expensive operating system kernel syscall that stalls execution. To avoid this, PyTorch utilizes a custom <strong>Caching Memory Allocator</strong>. When a tensor is deleted (<code>del tensor</code>), the VRAM is not returned to the OS or NVIDIA driver; it is returned to PyTorch's internal free-block pool for instant reuse. Calling <code>torch.cuda.empty_cache()</code> only releases unused cached blocks to the OS—it does <em>not</em> free memory held by active tensors!</p>

    <!-- SECTION 4: THE RD SHARMA 4-TIER PRACTICE SUITE -->
    <div class="practice-set">
      <h3>The R.D. Sharma Practice Suite — Chapter 0.3</h3>
      <p class="section-intro">Master tensor memory geometry, stride calculations, broadcasting rules, and GPU DMA pipelines through graded analytical exercises.</p>

      <!-- ==================== TIER 1: FORMULA DRILLS ==================== -->
      <h4>Tier 1: Direct Formula &amp; Numerical Warm-Up Drills</h4>

      <div class="problem">
        <div class="problem-header">
          <span class="problem-number">Problem 0.3.1</span>
          <span class="difficulty difficulty-easy">Level 1: Formula Drill</span>
          <span class="company-tag company-google">Google</span>
        </div>
        <div class="problem-question">
          <p><strong>QUESTION:</strong> A 3D tensor $T$ has shape $(2, 3, 4)$ with data type FP32 (4 bytes per element) in standard C-contiguous (row-major) order.
          <ol>
            <li>Compute the stride tuple (in bytes) along each of the three dimensions.</li>
            <li>Compute the exact memory byte offset of the element located at index $(1, 2, 3)$ assuming base offset is 0.</li>
            <li>If you transpose dimensions 1 and 2 (<code>T.transpose(1, 2)</code>), what are the new shape and stride tuples? Does this operation copy any memory?</li>
          </ol></p>
        </div>
        <div class="solution">
          <div class="solution-label">✓ Complete Step-by-Step Solution</div>
          <p class="step"><strong>Step 1: Compute C-Contiguous Strides:</strong><br>
          Let shape be $(d_0, d_1, d_2) = (2, 3, 4)$ and itemsize $B = 4$ bytes.<br>
          - Stride for dimension 2 (last dimension): $s_2 = B = \mathbf{4 \text{ bytes}}$.<br>
          - Stride for dimension 1: $s_1 = d_2 \times s_2 = 4 \times 4 = \mathbf{16 \text{ bytes}}$.<br>
          - Stride for dimension 0: $s_0 = d_1 \times s_1 = 3 \times 16 = \mathbf{48 \text{ bytes}}$.<br>
          $$\text{Stride Tuple} = (48, 16, 4)$$</p>

          <p class="step"><strong>Step 2: Compute Byte Offset for $(1, 2, 3)$:</strong><br>
          $$\text{Offset} = (i_0 \times s_0) + (i_1 \times s_1) + (i_2 \times s_2)$$
          $$\text{Offset} = (1 \times 48) + (2 \times 16) + (3 \times 4) = 48 + 32 + 12 = \mathbf{92 \text{ bytes}}$$</p>

          <p class="step"><strong>Step 3: Transpose Dimensions 1 and 2:</strong><br>
          Transposing swaps the shape and stride entries for dimensions 1 and 2:<br>
          $$\text{New Shape} = (2, 4, 3)$$
          $$\text{New Strides} = (48, 4, 16)$$
          <strong>Memory Copy:</strong> <strong>Zero bytes copied!</strong> Only a new lightweight metadata header is created. The underlying memory buffer remains completely unchanged.</p>
        </div>
      </div>

      <div class="problem">
        <div class="problem-header">
          <span class="problem-number">Problem 0.3.2</span>
          <span class="difficulty difficulty-easy">Level 1: Formula Drill</span>
          <span class="company-tag company-amazon">Amazon</span>
        </div>
        <div class="problem-question">
          <p><strong>QUESTION:</strong> Determine whether each of the following pairs of tensor shapes is broadcast-compatible under standard NumPy/PyTorch rules. If compatible, state the resulting broadcasted output shape; if not, explain why:
          <ol>
            <li>$A: (64, 1, 128)$ and $B: (32, 128)$</li>
            <li>$A: (8, 3, 224, 224)$ and $B: (3, 1, 1)$</li>
            <li>$A: (16, 256)$ and $B: (16, 128)$</li>
            <li>$A: (5, 1, 4, 1)$ and $B: (3, 1, 7)$</li>
          </ol></p>
        </div>
        <div class="solution">
          <div class="solution-label">✓ Complete Step-by-Step Solution</div>
          <p class="step"><strong>Case 1: $A: (64, 1, 128)$ and $B: (32, 128)$</strong><br>
          - Prepend 1 to $B$: $(1, 32, 128)$.<br>
          - Dim 2: $128 == 128 \implies$ Match.<br>
          - Dim 1: $1$ vs $32 \implies$ Compatible (stretch 1 to 32).<br>
          - Dim 0: $64$ vs $1 \implies$ Compatible (stretch 1 to 64).<br>
          <strong>Result: Compatible &rarr; Output Shape: $(64, 32, 128)$.</strong></p>

          <p class="step"><strong>Case 2: $A: (8, 3, 224, 224)$ and $B: (3, 1, 1)$</strong><br>
          - Prepend 1 to $B$: $(1, 3, 1, 1)$.<br>
          - Dim 3: $224$ vs $1 \implies$ Match.<br>
          - Dim 2: $224$ vs $1 \implies$ Match.<br>
          - Dim 1: $3 == 3 \implies$ Match.<br>
          - Dim 0: $8$ vs $1 \implies$ Match.<br>
          <strong>Result: Compatible &rarr; Output Shape: $(8, 3, 224, 224)$.</strong> (Standard image per-channel normalization!).</p>

          <p class="step"><strong>Case 3: $A: (16, 256)$ and $B: (16, 128)$</strong><br>
          - Compare trailing Dim 1: $256 \neq 128$ and neither is 1.<br>
          <strong>Result: INCOMPATIBLE &rarr; Raises <code>ValueError</code>!</strong></p>

          <p class="step"><strong>Case 4: $A: (5, 1, 4, 1)$ and $B: (3, 1, 7)$</strong><br>
          - Prepend 1 to $B$: $(1, 3, 1, 7)$.<br>
          - Dim 3: $1$ vs $7 \implies 7$.<br>
          - Dim 2: $4$ vs $1 \implies 4$.<br>
          - Dim 1: $1$ vs $3 \implies 3$.<br>
          - Dim 0: $5$ vs $1 \implies 5$.<br>
          <strong>Result: Compatible &rarr; Output Shape: $(5, 3, 4, 7)$.</strong></p>
        </div>
      </div>

      <!-- ==================== TIER 2: APPLIED TRACES ==================== -->
      <h4>Tier 2: Applied Engineering &amp; Algorithmic Tracing</h4>

      <div class="problem">
        <div class="problem-header">
          <span class="problem-number">Problem 0.3.3</span>
          <span class="difficulty difficulty-medium">Level 2: Execution Trace</span>
          <span class="company-tag company-meta">Meta</span>
        </div>
        <div class="problem-question">
          <p><strong>QUESTION:</strong> An engineer creates a 2D tensor $X$ of shape $(3, 4)$, transposes it $Y = X.t()$, and attempts to flatten it using <code>Y.view(-1)</code>.
          <ol>
            <li>Why does PyTorch throw: <code>RuntimeError: view size is not compatible with input tensor's size and stride (must be contiguous)</code>?</li>
            <li>Trace the exact stride values of $X$ and $Y$ to explain what "contiguous" means mathematically.</li>
            <li>Explain what <code>Y.contiguous()</code> does physically to memory, and how <code>Y.reshape(-1)</code> handles this transparently.</li>
          </ol></p>
        </div>
        <div class="solution">
          <div class="solution-label">✓ Complete Step-by-Step Solution</div>
          <p class="step"><strong>Step 1: Mathematical Definition of Contiguity:</strong><br>
          A tensor is C-contiguous if its elements are laid out in linear physical memory such that moving to the next element in the last dimension steps forward by 1 item ($s_{D-1} = 1$), and each prior dimension steps by the product of all subsequent dimensions ($s_k = s_{k+1} \times d_{k+1}$).<br>
          For $X$ with shape $(3, 4)$:
          $$\text{Strides}(X) = (4, 1) \implies \text{C-Contiguous!}$$</p>

          <p class="step"><strong>Step 2: Trace Transposition $Y = X.t()$:</strong><br>
          Transposition swaps the shape and strides without copying memory:<br>
          $$\text{Shape}(Y) = (4, 3)$$
          $$\text{Strides}(Y) = (1, 4)$$
          Notice that to step to the next column in $Y$ (dimension 1), we must jump forward by 4 items, but to step to the next row (dimension 0), we jump by only 1 item! The memory layout is Fortran-ordered (column-major), <strong>NOT C-contiguous</strong>!</p>

          <p class="step"><strong>Step 3: Why <code>view()</code> Fails vs. <code>reshape()</code>:</strong><br>
          - <code>view()</code> requires the underlying tensor to be C-contiguous because it only modifies shape/stride metadata without reallocating data. Flattening non-contiguous strides $(1, 4)$ into a single 1D stride of 1 is mathematically impossible without rearranging the bytes!<br>
          - <code>Y.contiguous()</code> allocates a brand-new contiguous memory buffer and physically copies the elements into row-major order: strides become $(3, 1)$.<br>
          - <code>Y.reshape(-1)</code> inspects contiguity: if contiguous, it returns a zero-copy view; if non-contiguous, it automatically calls <code>contiguous()</code> behind the scenes.</p>
        </div>
      </div>

      <!-- ==================== TIER 3: FAANG INTERVIEWS ==================== -->
      <h4>Tier 3: FAANG &amp; Tier-1 AI Interview Challenges</h4>

      <div class="problem">
        <div class="problem-header">
          <span class="problem-number">Problem 0.3.4</span>
          <span class="difficulty difficulty-hard">Level 3: FAANG Challenge</span>
          <span class="company-tag company-google">Google</span>
          <span class="company-tag company-meta">Meta</span>
        </div>
        <div class="problem-question">
          <p><strong>QUESTION:</strong> You are given two matrices of embedding vectors: $X \in \mathbb{R}^{M \times D}$ and $Y \in \mathbb{R}^{N \times D}$. You must compute the pairwise squared Euclidean distance matrix $D \in \mathbb{R}^{M \times N}$, where $D_{ij} = \|X_i - Y_j\|_2^2$.</p>
          <ol>
            <li>Why does the naive broadcasting approach $(X[:, \text{None}, :] - Y[\text{None}, :, :])^2$ cause an immediate Out-Of-Memory (OOM) crash when $M = 50,000$, $N = 50,000$, and $D = 768$? Calculate the exact memory required.</li>
            <li>Derive the mathematically equivalent matrix expression using the binomial expansion of vector norms.</li>
            <li>Write the optimized, vectorized PyTorch implementation that executes in $O(M \times N)$ memory without allocating a 3D intermediate tensor.</li>
          </ol>
        </div>
        <div class="solution">
          <div class="solution-label">✓ Complete Step-by-Step Mathematical Solution</div>
          <p class="step"><strong>Step 1: Calculate Memory of Naive 3D Broadcasting:</strong><br>
          Expanding $X$ to $(M, 1, D)$ and $Y$ to $(1, N, D)$ creates an intermediate 3D subtraction tensor of shape $(M, N, D)$.<br>
          For $M = 50,000$, $N = 50,000$, and $D = 768$ under 32-bit floating point (4 bytes/element):
          $$\text{Total Elements} = 50,000 \times 50,000 \times 768 = 1.92 \times 10^{12} \text{ elements}$$
          $$\text{Memory Required} = 1.92 \times 10^{12} \times 4 \text{ bytes} \approx 7,680 \text{ Gigabytes} = 7.68 \text{ Terabytes of RAM!}$$
          This will instantaneously crash any server on Earth.</p>

          <p class="step"><strong>Step 2: Binomial Expansion Derivation:</strong><br>
          Recall the algebraic identity for the squared Euclidean distance between two vectors $\mathbf{x}$ and $\mathbf{y}$:
          $$\|\mathbf{x} - \mathbf{y}\|_2^2 = (\mathbf{x} - \mathbf{y})^T (\mathbf{x} - \mathbf{y}) = \mathbf{x}^T \mathbf{x} + \mathbf{y}^T \mathbf{y} - 2 \mathbf{x}^T \mathbf{y} = \|\mathbf{x}\|_2^2 + \|\mathbf{y}\|_2^2 - 2 (\mathbf{x} \cdot \mathbf{y})$$
          Generalize to matrices $X$ and $Y$:</p>
          <ul>
            <li>Let $\mathbf{r}_X \in \mathbb{R}^{M \times 1}$ be the row-wise squared norms: $(\mathbf{r}_X)_i = \sum_{k=1}^D X_{ik}^2$.</li>
            <li>Let $\mathbf{r}_Y \in \mathbb{R}^{1 \times N}$ be the row-wise squared norms: $(\mathbf{r}_Y)_j = \sum_{k=1}^D Y_{jk}^2$.</li>
            <li>Let $C = X Y^T \in \mathbb{R}^{M \times N}$ be the standard matrix multiplication dot-product.</li>
          </ul>
          $$D = \mathbf{r}_X + \mathbf{r}_Y - 2 (X Y^T)$$

          <p class="step"><strong>Step 3: Vectorized Implementation in PyTorch:</strong></p>
<pre><code>import torch

def pairwise_distance_squared(X: torch.Tensor, Y: torch.Tensor) -> torch.Tensor:
    # 1. Compute row-wise squared norms
    x_norm_sq = (X ** 2).sum(dim=1, keepdim=True) # Shape (M, 1)
    y_norm_sq = (Y ** 2).sum(dim=1, keepdim=True).t() # Shape (1, N)

    # 2. Compute cross term via GEMM (General Matrix Multiply)
    xy = torch.mm(X, Y.t()) # Shape (M, N)

    # 3. Combine via 2D broadcasting and clamp numerical epsilon
    dist_sq = x_norm_sq + y_norm_sq - 2.0 * xy
    return torch.clamp(dist_sq, min=0.0)</code></pre>
          <p><em>Memory Analysis:</em> The intermediate tensor size drops from <strong>7.68 Terabytes down to exactly 10 Gigabytes</strong> (the final $(M, N)$ output matrix), converting an impossible computation into a standard 15-millisecond GPU execution!</p>
        </div>
      </div>

      <!-- ==================== TIER 4: CONCEPTUAL MCQS ==================== -->
      <h4>Tier 4: Conceptual Trap MCQs &amp; Assertion-Reasoning</h4>

      <div class="problem">
        <div class="problem-header">
          <span class="problem-number">Problem 0.3.5</span>
          <span class="difficulty difficulty-medium">Level 4: Conceptual MCQ</span>
          <span class="company-tag company-apple">Apple</span>
        </div>
        <div class="problem-question">
          <p><strong>QUESTION:</strong> An engineer performs a 2D sliding window extraction on a 1D audio signal array of length $100,000$ using NumPy's <code>as_strided</code> utility. The resulting windowed matrix has shape $(99000, 1000)$. How much additional memory is allocated for the data buffer?</p>
          <ol type="A">
            <li>$99,000 \times 1000 \times 4 \text{ bytes} \approx 396 \text{ MB}$.</li>
            <li>Exactly zero bytes: only shape and stride metadata are created.</li>
            <li>$100,000 \times 4 \text{ bytes} = 400 \text{ KB}$.</li>
            <li>$1000 \times 4 \text{ bytes} = 4 \text{ KB}$.</li>
          </ol>
        </div>
        <div class="solution">
          <div class="solution-label">✓ Correct Answer: [B] &amp; Detailed Explanation</div>
          <p class="step"><strong>Analysis:</strong> <code>np.lib.stride_tricks.as_strided</code> creates a view into an existing array by altering only its shape and strides without copying memory. By manipulating the strides to advance by only 1 element between rows while sharing elements across windows, a $(99000, 1000)$ array is represented over the original 400KB buffer with <strong>zero additional data memory allocated</strong>.</p>
        </div>
      </div>

      <div class="problem">
        <div class="problem-header">
          <span class="problem-number">Problem 0.3.6</span>
          <span class="difficulty difficulty-medium">Level 4: Assertion-Reasoning</span>
          <span class="company-tag company-nvidia">NVIDIA</span>
        </div>
        <div class="problem-question">
          <p><strong>QUESTION:</strong> Read the following Assertion and Reason carefully, then choose the correct option:</p>
          <p><strong>Assertion (A):</strong> Calling <code>torch.cuda.empty_cache()</code> inside your PyTorch training loop immediately after <code>loss.backward()</code> will eliminate Out-Of-Memory (OOM) errors during training.</p>
          <p><strong>Reason (R):</strong> <code>torch.cuda.empty_cache()</code> frees active model weights and gradient buffers back to GPU VRAM.</p>
          <ol type="A">
            <li>Both (A) and (R) are true, and (R) is the correct explanation of (A).</li>
            <li>Both (A) and (R) are true, but (R) is NOT the correct explanation of (A).</li>
            <li>(A) is true, but (R) is false.</li>
            <li>Both (A) and (R) are false.</li>
          </ol>
        </div>
        <div class="solution">
          <div class="solution-label">✓ Correct Answer: [D] &amp; Detailed Explanation</div>
          <p class="step"><strong>Analysis:</strong> Both statements are completely false! (R) is false because <code>empty_cache()</code> only releases *cached, unreferenced* memory blocks from PyTorch's internal pool to the operating system; it cannot free active tensors (weights, gradients, activations). (A) is false because calling <code>empty_cache()</code> does not increase total available VRAM for active tensors, but drastically degrades training speed by forcing the GPU driver to perform expensive OS kernel re-allocations on every step.</p>
        </div>
      </div>

    </div>

    <!-- SECTION 5: CODE LAB -->
    <h3>4. Production Code Lab 0.3: SIMD Vectorization vs. Python Loops</h3>
    <p>To witness the physical reality of C-level SIMD vectorization, we benchmark naive Python iteration against optimized NumPy BLAS routines.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 0.3 — The 100x Speedup of Vectorization</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part0_foundations/ch03_the_ai_toolchain/vectorization_benchmarks.py" target="_blank">🔗 View in GitHub: part0_foundations/ch03_the_ai_toolchain/vectorization_benchmarks.py</a></p>
<pre><code>import time
import numpy as np

def benchmark_dot_product(N=10_000_000):
    a = np.random.randn(N).astype(np.float32)
    b = np.random.randn(N).astype(np.float32)

    # 1. Naive Python Loop
    t0 = time.perf_counter()
    dot_py = 0.0
    for i in range(1_000_000): # Run on 1M to avoid waiting forever
        dot_py += a[i] * b[i]
    t_py = (time.perf_counter() - t0) * 10 # Scale to 10M

    # 2. NumPy Vectorized BLAS Dot Product
    t0 = time.perf_counter()
    dot_np = np.dot(a, b)
    t_np = time.perf_counter() - t0

    print(f"Python Loop Time : {t_py*1000:.2f} ms")
    print(f"NumPy BLAS Time  : {t_np*1000:.2f} ms")
    print(f"Speedup Factor   : {t_py / t_np:.1f}x faster!")

if __name__ == "__main__":
    benchmark_dot_product()</code></pre>
    </div>

    <!-- SECTION 6: END OF CHAPTER PROJECT -->
    <div class="project-section">
      <div class="project-header">
        <span class="project-tag">Chapter 0.3 Dedicated Project &amp; Case Study</span>
        <h3 class="project-title">Project 0.3: High-Throughput In-Memory Vector Search Engine</h3>
        <p class="project-desc">Combine NumPy strided vectorization, broadcasting algebra, and PyTorch pinned memory to build a blazing-fast in-memory cosine similarity search engine capable of searching 1,000,000 embedding vectors in under 5 milliseconds.</p>
        <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part0_foundations/ch03_the_ai_toolchain/vectorization_benchmarks.py" target="_blank">🔗 Full Project Code: part0_foundations/ch03_the_ai_toolchain/vectorization_benchmarks.py</a></p>
      </div>
      <div class="project-body">
        <p><strong>Case Study Architecture:</strong> Before deploying complex vector databases like Milvus or Pinecone, production systems frequently require lightweight, in-memory embedding lookups inside real-time microservices. In this project, you construct a high-throughput vector ranker that normalizes query and catalog vectors using broadcasted L2 norms and executes fused matrix multiplications across millions of entries.</p>
      </div>
    </div>
  </div>
</div>
"""

with open('book_builder/ch03_ai_toolchain.html', 'w', encoding='utf-8') as f:
    f.write(ch03_content)
print("Updated ch03_ai_toolchain.html successfully!")
