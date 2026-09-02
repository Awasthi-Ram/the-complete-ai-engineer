# book_builder/part0_foundations.py

PART0_HTML = """
<!-- ████████████████████████████████████████████████████████████████████████
     PART 0 — FOUNDATIONS BEFORE FOUNDATIONS
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 0</div>
  <div class="part-title">Foundations Before Foundations</div>
  <div class="part-subtitle">Setting up your mind, your Python toolchain, and your machine</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

<!-- ======================================================================
     CHAPTER 0.1 — HOW TO LEARN AI
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 0.1</span>
    <h2 class="chapter-title">How to Learn AI</h2>
    <span class="chapter-subtitle">Setting Up Your Mind and Your Machine</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"The expert in anything was once a beginner."</p>
    <p class="attribution">— Helen Hayes</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Before we write a single line of code, before we inspect a single equation, we must establish how to learn. Artificial intelligence is evolving at exponential velocity. New benchmark papers appear daily. Groundbreaking transformer variants and diffusion techniques drop weekly. The volume of noise is immense, and the temptation to chase every transient framework is intoxicating. But here is the foundational law separating engineers who thrive from those who drown: <strong>the fundamentals never change</strong>. Linear algebra, multivariable calculus, optimization, computational graphs, and systems engineering form an eternal foundation.</p>

    <div class="real-world-box">
      <h4>🏢 Real-World Problem Mapping: Why Depth Beats Tool-Chasing</h4>
      <p>In industry, the most expensive production outages occur when an engineer treats an AI model as a "magic black box." When a model starts hallucinating, suffers catastrophic forgetting during fine-tuning, or experiences severe latency regression under load, high-level API tutorials cannot save you. Diagnosing these failures requires understanding floating-point precision, gradient norms, memory bandwidth saturation, and loss surface geometry.</p>
    </div>

    <h3>The Learning Philosophy of This Book</h3>
    <p>This book is modeled after the legendary R.D. Sharma mathematics series that taught millions of engineers not merely how to memorize equations, but how to <em>think</em>:</p>
    <ol>
      <li><strong>Concept First:</strong> Physical intuition and mental imagery before mathematical formalism.</li>
      <li><strong>Why It Exists:</strong> Every algorithm was invented because an earlier approach broke in the real world. We examine that breakdown.</li>
      <li><strong>Rigorous Mathematics:</strong> Step-by-step derivations without skipped steps or "it can be shown that" hand-waving.</li>
      <li><strong>Complete Solved Problems:</strong> Fully worked interview problems from Google, Meta, OpenAI, and Amazon printed directly on the page. You do not need a computer to understand the complete solution.</li>
      <li><strong>Production Code Labs:</strong> Clean Python implementations with direct GitHub repository links.</li>
    </ol>

    <h3>Setting Up Your AI Machine</h3>
    <p>We recommend a standard Python 3.10+ virtual environment. For deep learning, an NVIDIA GPU with CUDA support or Google Colab T4/A100 is recommended.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 0.1 — Environment Verification Script</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part0_foundations/ch01_how_to_learn/verify_env.py" target="_blank">🔗 View in GitHub: part0_foundations/ch01_how_to_learn/verify_env.py</a></p>
<pre><code><span class="comment"># Environment Diagnostic & GPU Verification</span>
import sys, platform

def verify_environment():
    print(f"Python  : {sys.version.split()[0]} on {platform.system()}")
    try:
        import torch
        print(f"PyTorch : {torch.__version__} | CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU     : {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB VRAM)")
    except ImportError:
        print("PyTorch not installed. Run: pip install torch")

if __name__ == "__main__":
    verify_environment()</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 0.2 — PYTHON FOUNDATIONS FOR AI
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 0.2</span>
    <h2 class="chapter-title">Python Foundations</h2>
    <span class="chapter-subtitle">Object-Oriented AI Programming, Memory & Generators</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Simple is better than complex. Complex is better than complicated."</p>
    <p class="attribution">— The Zen of Python</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Python is the lingua franca of artificial intelligence. However, writing code for AI requires a fundamentally different mindset than writing standard web applications. In AI engineering, you deal with gigabytes of numeric tensors, parallel execution across GPU streams, memory reference cycles, and custom operator overloading.</p>

    <div class="real-world-box">
      <h4>🏢 Real-World Problem Mapping: The 100GB Out-of-Memory (OOM) Trap</h4>
      <p>A common disaster occurs when an engineer loads a 50GB dataset entirely into Python lists. Python objects carry substantial overhead: a standard 64-bit float in Python is a 24-byte heap-allocated object (`PyFloatObject`), whereas a raw C-float is only 4 or 8 bytes. Using standard lists blows up memory usage by 4x to 8x, crashing production training containers. Learning generators, buffer protocols, and memory profiling is mandatory.</p>
    </div>

    <h3>1. Object-Oriented AI Architecture</h3>
    <p>Modern deep learning frameworks like PyTorch represent neural layers as stateful objects that maintain internal weight matrices, bias vectors, and gradient accumulators. Understanding custom classes with operator overloading is critical:</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 0.2 — Dense Matrix with Operator Overloading</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part0_foundations/ch02_python_foundations/solutions.py" target="_blank">🔗 View in GitHub: part0_foundations/ch02_python_foundations/solutions.py</a></p>
<pre><code>class DenseMatrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def shape(self):
        return (self.rows, self.cols)

    def __add__(self, other):
        if self.shape() != other.shape():
            raise ValueError(f"Shape mismatch: {self.shape()} vs {other.shape()}")
        return DenseMatrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])</code></pre>
    </div>

    <h3>2. Memory-Efficient Batch Generators</h3>
    <p>When training models on millions of samples, you cannot materialize the full dataset in memory. Python generators (`yield`) yield one batch at a time into memory, enabling constant $O(1)$ RAM usage regardless of total dataset size:</p>

<pre><code>def batch_generator(data, batch_size=32):
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]</code></pre>

    <h3>FAANG Interview Problems — Python for AI</h3>

    <div class="problem">
      <div class="problem-header">
        <span class="problem-number">Problem 0.2.1</span>
        <span class="difficulty difficulty-medium">Medium</span>
        <span class="company-tag company-google">Google</span>
        <span class="company-tag company-meta">Meta</span>
      </div>
      <div class="problem-question">
        <p><strong>QUESTION:</strong> Explain why standard Python lists are unsuitable for large-scale matrix operations compared to contiguous memory arrays. Calculate the memory consumption of storing 10,000,000 floating-point numbers in a Python list versus a contiguous 64-bit float array.</p>
      </div>
      <div class="solution">
        <div class="solution-label">✓ Complete Step-by-Step Solution</div>
        <p class="step"><strong>Step 1: Understand Python List Memory Layout:</strong> A Python list is an array of <em>pointers</em> to arbitrary Python objects (`PyObject*`). Each element in a float list points to a distinct heap-allocated `PyFloatObject`. On a 64-bit machine:</p>
        <ul>
          <li>Each list pointer consumes 8 bytes.</li>
          <li>Each `PyFloatObject` contains an 8-byte reference count, an 8-byte type pointer, and an 8-byte double-precision C value = 24 bytes.</li>
          <li>Total per float = $8 + 24 = 32$ bytes minimum (excluding allocator fragmentation).</li>
        </ul>
        <p class="step"><strong>Step 2: Calculate List Memory:</strong> For $10^7$ floats, the list requires:
        $$\text{Memory}_{\text{list}} = 10^7 \times 32 \text{ bytes} \approx 320 \text{ MB}$$</p>
        <p class="step"><strong>Step 3: Contiguous Memory Layout (NumPy / C):</strong> A contiguous array stores raw binary floating-point numbers directly next to each other in RAM with zero pointer overhead. For 64-bit floats (8 bytes each):
        $$\text{Memory}_{\text{contiguous}} = 10^7 \times 8 \text{ bytes} = 80 \text{ MB}$$</p>
        <p class="step"><strong>Step 4: Cache Locality & Hardware Performance:</strong> Beyond saving 75% memory, contiguous arrays maximize CPU L1/L2 cache hits through sequential prefetching, whereas pointer dereferencing in lists causes constant cache misses. Furthermore, contiguous arrays enable SIMD (Single Instruction, Multiple Data) vectorization instructions (AVX-512) to process 8 floats per clock cycle.</p>
      </div>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 0.3 — THE AI TOOLCHAIN: NUMPY, PANDAS & PYTORCH
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 0.3</span>
    <h2 class="chapter-title">The AI Toolchain</h2>
    <span class="chapter-subtitle">NumPy Vectorization, Pandas & PyTorch GPU Tensors</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Give me a lever long enough and a fulcrum on which to place it, and I shall move the world."</p>
    <p class="attribution">— Archimedes</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Artificial intelligence is computationally intractable without specialized numeric libraries. In this prerequisite chapter, we master the holy trinity of AI engineering: <strong>NumPy</strong> (C-accelerated vectorization), <strong>Pandas</strong> (tabular feature manipulation), and <strong>PyTorch</strong> (GPU-accelerated tensors with automatic differentiation).</p>

    <div class="real-world-box">
      <h4>🏢 Real-World Problem Mapping: The 100x Speedup in Real-Time Latency</h4>
      <p>Suppose you work at an e-commerce giant serving 50,000 recommendations per second. Each request requires scoring a user vector against 10,000 product embeddings. In pure Python loops, computing 10,000 dot products takes ~25 milliseconds—violating your 5ms SLA and crashing the server. In vectorized NumPy (calling optimized BLAS/LAPACK routines), the exact same operation takes <strong>0.18 milliseconds</strong> (over 130x faster!). Vectorization is not a coding convenience; it is an architectural requirement.</p>
    </div>

    <h3>1. The Mechanics of Vectorization</h3>
    <p>When you execute a loop in pure Python, the Python interpreter checks types and handles reference counts on every single iteration:
    $$\text{for } i \text{ in range}(N): \quad c_i = a_i \times b_i$$
    In contrast, NumPy delegates the entire buffer to low-level compiled C/Fortran libraries (OpenBLAS, Intel MKL, or Apple Accelerate). The CPU registers load 256 or 512 bits simultaneously, multiplying 4 or 8 double-precision floats in a single clock cycle.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 0.3 — Vectorization Benchmark: 100x Acceleration</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part0_foundations/ch03_ai_toolchain/vectorization_benchmarks.py" target="_blank">🔗 View in GitHub: part0_foundations/ch03_ai_toolchain/vectorization_benchmarks.py</a></p>
<pre><code>import time, numpy as np

n = 1_000_000
a = [0.01 * i for i in range(n)]
b = [0.02 * i for i in range(n)]

# 1. Pure Python Loop
t0 = time.perf_counter()
dot_py = sum(x * y for x, y in zip(a, b))
t_py = time.perf_counter() - t0

# 2. NumPy BLAS
a_np = np.array(a, dtype=np.float64)
b_np = np.array(b, dtype=np.float64)
t0 = time.perf_counter()
dot_np = np.dot(a_np, b_np)
t_np = time.perf_counter() - t0

print(f"Python Loop : {t_py*1000:.2f} ms")
print(f"NumPy BLAS  : {t_np*1000:.2f} ms ({t_py/t_np:.1f}x speedup!)")</code></pre>
    </div>

    <h3>2. Broadcasting Rules in Multi-Dimensional Tensors</h3>
    <p>Broadcasting allows arithmetic operations between arrays of differing shapes without making unnecessary memory copies. Two dimensions are compatible when:
    <ol>
      <li>They are equal, OR</li>
      <li>One of them is 1.</li>
    </ol>
    Example: Adding a bias vector of shape $(1, D)$ to a batch matrix of shape $(B, D)$. The bias vector is virtually replicated along the batch dimension with zero memory allocation.</p>

    <h3>3. PyTorch Tensors vs NumPy Arrays</h3>
    <p>PyTorch Tensors share the same contiguous buffer concepts as NumPy, but provide two transformative superpowers:
    <ul>
      <li><strong>GPU Acceleration:</strong> Moving a tensor to CUDA (`tensor.to('cuda')`) unleashes thousands of streaming multiprocessors (SMs) performing parallel matrix multiplications at teraflops per second.</li>
      <li><strong>Autograd:</strong> Tensors track operations to build dynamic computational graphs, computing reverse-mode gradients automatically via `.backward()`.</li>
    </ul></p>

    <div class="problem">
      <div class="problem-header">
        <span class="problem-number">Problem 0.3.1</span>
        <span class="difficulty difficulty-hard">Hard</span>
        <span class="company-tag company-openai">OpenAI</span>
        <span class="company-tag company-meta">Meta</span>
      </div>
      <div class="problem-question">
        <p><strong>QUESTION:</strong> Determine whether the following array shapes can be broadcast together according to NumPy/PyTorch rules. If yes, state the resulting shape. If no, explain why:</p>
        <p>Case A: Array $A$ of shape $(8, 1, 64)$ and Array $B$ of shape $(8, 32, 1)$<br>
        Case B: Array $C$ of shape $(16, 256)$ and Array $D$ of shape $(256, 16)$<br>
        Case C: Array $E$ of shape $(4, 1, 128, 64)$ and Array $F$ of shape $(128, 1)$</p>
      </div>
      <div class="solution">
        <div class="solution-label">✓ Complete Step-by-Step Solution</div>
        <p class="step"><strong>Step 1: Rule of Alignment:</strong> Trailing dimensions are aligned from right to left. If one shape has fewer dimensions, it is prepended with 1s on the left.</p>
        <p class="step"><strong>Step 2: Evaluate Case A:</strong>
        $$A: (8, 1, 64) \quad \text{vs} \quad B: (8, 32, 1)$$
        Dim 3: $64$ and $1 \rightarrow$ Compatible (1 expands to 64)<br>
        Dim 2: $1$ and $32 \rightarrow$ Compatible (1 expands to 32)<br>
        Dim 1: $8$ and $8 \rightarrow$ Compatible (equal)<br>
        <strong>Result: Broadcastable to $(8, 32, 64)$.</strong></p>

        <p class="step"><strong>Step 3: Evaluate Case B:</strong>
        $$C: (16, 256) \quad \text{vs} \quad D: (256, 16)$$
        Dim 2: $256$ and $16 \rightarrow$ Incompatible (neither is 1, and $256 \ne 16$).<br>
        <strong>Result: Fails broadcasting error.</strong></p>

        <p class="step"><strong>Step 4: Evaluate Case C:</strong>
        $$E: (4, 1, 128, 64) \quad \text{vs} \quad F: (128, 1) \rightarrow \text{Prepend 1s: } (1, 1, 128, 1)$$
        Dim 4: $64$ and $1 \rightarrow$ Compatible (1 expands to 64)<br>
        Dim 3: $128$ and $128 \rightarrow$ Compatible (equal)<br>
        Dim 2: $1$ and $1 \rightarrow$ Compatible<br>
        Dim 1: $4$ and $1 \rightarrow$ Compatible (1 expands to 4)<br>
        <strong>Result: Broadcastable to $(4, 1, 128, 64)$.</strong></p>
      </div>
    </div>
  </div>
</div>

<!-- ======================================================================
     PROJECT 0 — BUILD YOUR AI DEVELOPMENT DASHBOARD
     ====================================================================== -->
<div class="project-section">
  <div class="project-header">
    <span class="project-tag">Hands-On Project 0</span>
    <h3 class="project-title">Build Your AI Development Dashboard & Training Monitor</h3>
    <p class="project-desc">Create a real-time training metric logger that monitors training loss, validation loss, generalization gap, learning rate decay, and automatically flags early overfitting risks.</p>
    <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part0_foundations/project0_dashboard/dashboard.py" target="_blank">🔗 Full Project Code: part0_foundations/project0_dashboard/dashboard.py</a></p>
  </div>
  <div class="project-body">
    <p><strong>Architecture Overview:</strong> In modern MLOps, silent training failures cost tens of thousands of dollars in wasted GPU cluster compute. Your dashboard tracks mini-batch training trajectories, computes exponential moving averages, and triggers automated alerts when the generalization gap $(L_{\text{val}} - L_{\text{train}})$ exceeds safety thresholds.</p>
  </div>
</div>
"""
