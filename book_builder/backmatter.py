# book_builder/backmatter.py

BACKMATTER_HTML = """
<!-- ======================================================================
     APPENDIX A — GLOSSARY & NOTATION
     ====================================================================== -->
<div class="chapter glossary">
  <div class="chapter-header">
    <span class="chapter-number">Appendix A</span>
    <h2 class="chapter-title">Mathematical Notation &amp; Glossary</h2>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="chapter-body">
    <h3>Standard Mathematical Notation</h3>
    <table>
      <tr><th>Symbol</th><th>Meaning</th><th>Example</th></tr>
      <tr><td>$x \in \mathbb{R}$</td><td>Real scalar</td><td>$x = 3.1415$</td></tr>
      <tr><td>$\mathbf{x} \in \mathbb{R}^d$</td><td>Column vector of dimension $d$</td><td>$\mathbf{x} = [x_1, x_2, \dots, x_d]^T$</td></tr>
      <tr><td>$X \in \mathbb{R}^{N \times d}$</td><td>Matrix of $N$ samples and $d$ features</td><td>$X_{ij}$ is row $i$, column $j$</td></tr>
      <tr><td>$T \in \mathbb{R}^{B \times S \times D}$</td><td>3D Tensor</td><td>Batch $B$, Sequence $S$, Hidden $D$</td></tr>
      <tr><td>$\|\mathbf{x}\|_2$</td><td>$L_2$ Euclidean vector norm</td><td>$\sqrt{\sum x_i^2}$</td></tr>
      <tr><td>$\nabla_{\mathbf{w}} \mathcal{L}$</td><td>Gradient vector of loss $\mathcal{L}$ w.r.t $\mathbf{w}$</td><td>Direction of steepest ascent</td></tr>
      <tr><td>$\sigma(z)$</td><td>Sigmoid activation function</td><td>$\frac{1}{1 + e^{-z}}$</td></tr>
      <tr><td>$D_{\text{KL}}(P \parallel Q)$</td><td>Kullback-Leibler Divergence</td><td>Statistical distance between $P$ and $Q$</td></tr>
    </table>

    <h3>Essential AI Engineering Terms</h3>
    <ul>
      <li><strong>Autograd:</strong> Reverse-mode automatic differentiation tracking operations on tensors to compute exact gradients via the chain rule.</li>
      <li><strong>Backpropagation:</strong> The efficient computational graph algorithm for calculating partial derivatives $\frac{\partial \mathcal{L}}{\partial W^{[l]}}$.</li>
      <li><strong>BPE (Byte-Pair Encoding):</strong> Subword tokenization algorithm that iteratively merges the most frequent adjacent character pairs into single tokens.</li>
      <li><strong>Data Leakage:</strong> An evaluation catastrophe where information from the test or target dataset contaminates the training feature pipeline.</li>
      <li><strong>Inductive Bias:</strong> The set of architectural assumptions a learning algorithm uses to predict outputs for unseen inputs.</li>
      <li><strong>KV Cache:</strong> An inference optimization that stores Key and Value tensors in GPU memory to prevent redundant quadratic compute during autoregressive generation.</li>
      <li><strong>LoRA:</strong> Low-Rank Adaptation, freezing base weights $W_0$ and updating parameters through factorized low-rank matrices $B \times A$.</li>
      <li><strong>PSI (Population Stability Index):</strong> Statistical metric measuring divergence between baseline training feature distributions and production inference traffic.</li>
      <li><strong>RAG (Retrieval-Augmented Generation):</strong> Augmenting LLM prompts with semantically retrieved context chunks from non-parametric vector databases.</li>
      <li><strong>ReAct:</strong> An agent framework interleaving Reasoning (Thought) and Acting (Tool execution).</li>
      <li><strong>SVD (Singular Value Decomposition):</strong> Factorization of matrix $A$ into $U \Sigma V^T$, providing the mathematically optimal low-rank matrix approximation.</li>
    </ul>
  </div>
</div>

<!-- ======================================================================
     APPENDIX B — ABOUT THE AUTHOR
     ====================================================================== -->
<div class="chapter about-author">
  <div class="chapter-header">
    <span class="chapter-number">Appendix B</span>
    <h2 class="chapter-title">About the Author</h2>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="chapter-body">
    <p><strong>Ram Awasthi</strong> is an AI engineer, systems researcher, and educator passionate about demystifying artificial intelligence from first principles. With deep expertise across deep learning, large language models, high-performance computing, and production MLOps, Ram has dedicated himself to creating comprehensive, rigorous, and accessible educational resources that empower engineers worldwide to build real-world intelligent systems.</p>
    <p>Inspired by the classic Indian mathematics textbooks of R.D. Sharma that emphasized thorough intuition, mathematical proof, and relentless problem-solving practice, Ram authored <em>The Complete AI Engineer</em> to bridge the gap between academic theory and production reality.</p>
  </div>
</div>

<!-- ======================================================================
     APPENDIX C — OFFICIAL GITHUB REPOSITORY & QR CODE ACCESS
     ====================================================================== -->
<div class="chapter github-repo-guide">
  <div class="chapter-header">
    <span class="chapter-number">Appendix C</span>
    <h2 class="chapter-title">Official Companion Code Repository</h2>
    <span class="chapter-subtitle">Run Every Problem, Code Lab &amp; Project On Your System</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="chapter-body">
    <p>While every mathematical proof, step-by-step calculation, and code implementation is printed in full directly in this book, we have published the complete, open-source, runnable repository for hands-on experimentation, benchmark replication, and production deployment.</p>

    <div class="qr-container">
      <h3>Scan to Access the Complete Code Repository</h3>
      <img src="github_repo_qr.png" alt="QR Code — The Complete AI Engineer Solutions Repository">
      <p><strong>Official Repository URL:</strong><br>
      <a href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions" target="_blank" style="color: #0077b6; font-family: monospace; font-size: 1.1em; font-weight: bold;">
        https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions
      </a></p>
      <p style="color: #666; font-size: 0.9em; margin-top: 8px;">Scan with your smartphone camera or click the link above on your e-reader.</p>
    </div>

    <h3>How to Run the Code on Your Computer</h3>

    <h4>1. Clone the Code Repository</h4>
<pre><code>git clone https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions.git
cd the-complete-ai-engineer-solutions</code></pre>

    <h4>2. Set Up Your Python Environment</h4>
<pre><code># Option A: Conda (Recommended)
conda create -n ai-engineer python=3.11 -y
conda activate ai-engineer
pip install -r requirements.txt

# Option B: Python Virtual Environment
python -m venv venv
# On Windows: .\\venv\\Scripts\\activate
# On macOS/Linux: source venv/bin/activate
pip install -r requirements.txt</code></pre>

    <h4>3. Verify Environment Health</h4>
<pre><code>python setup_env.py</code></pre>

    <h4>4. Run Code Labs & Projects Chapter by Chapter</h4>
    <p>The repository mirrors the exact chapter structure of this book:</p>
    <ul>
      <li><code>part0_foundations/</code> — Vectorization benchmarks & AI development dashboard</li>
      <li><code>part1_mathematics/</code> — SVD low-rank compression & autograd engine</li>
      <li><code>part2_classical_ml/</code> — OLS vs SGD, Decision Trees, SVM & ROC-AUC</li>
      <li><code>part3_neural_networks/</code> — Analytical backprop, AdamW & PyTorch loops</li>
      <li><code>part4_deep_learning/</code> — Conv2D, LSTM, Transformers & Diffusion</li>
      <li><code>part5_llms_and_agents/</code> — BPE Tokenizer, KV Cache, LoRA & ReAct Agent</li>
      <li><code>part6_mlops_production/</code> — FastAPI serving, PSI drift detector & Docker</li>
      <li><code>part7_ai_system_design/</code> — Industrial two-stage recommendation architecture</li>
      <li><code>part8_frontier/</code> — Multimodal CLIP search, Q-Learning & INT8 quantization</li>
    </ul>
  </div>
</div>

<!-- ====================================================================
     BACK COVER
     ==================================================================== -->
<div class="back-cover-page">
  <div class="back-cover-overlay">
    <h2 style="font-size: 1.8em; color: #5fa8d3; margin-bottom: 0.2em; font-family: 'Playfair Display', serif;">The Complete AI Engineer</h2>
    <h3 style="font-size: 1.1em; color: #e0e1dd; font-weight: 300; margin-bottom: 1.5em;">From Absolute Beginner to Production-Ready Engineer</h3>

    <p style="font-size: 0.9em; line-height: 1.6; margin-bottom: 1.2em; color: #cdd5e0;">
      Every concept taught the way a great teacher explains it. Inspired by the legendary R.D. Sharma mathematics series, this book teaches artificial intelligence from first principles — moving from mental intuition and rigorous mathematical derivations to solved FAANG interview problems and production-grade engineering code.
    </p>

    <div style="background: rgba(255,255,255,0.08); padding: 12px 16px; border-left: 3px solid #5fa8d3; margin-bottom: 1.5em; border-radius: 4px;">
      <p style="font-size: 0.85em; font-style: italic; color: #e0e1dd; margin: 0;">
        "You do not need to open a computer to read this book. Every single mathematical derivation, matrix step, and algorithm trace is written in full directly on the page."
      </p>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.8em; color: #a0aec0; margin-bottom: 1.5em;">
      <div>✓ Complete Python & Math Foundations</div>
      <div>✓ Classical Machine Learning from Scratch</div>
      <div>✓ Analytical Backprop & Neural Networks</div>
      <div>✓ Modern Transformers & Attention</div>
      <div>✓ LLMs, Tokenizers, LoRA & Agents</div>
      <div>✓ Enterprise MLOps & High-Scale Systems</div>
      <div>✓ 100+ Top FAANG Interview Problems</div>
      <div>✓ Official Companion GitHub Repository</div>
    </div>

    <div style="margin-top: auto; padding-top: 1em; border-top: 1px solid rgba(255,255,255,0.15); display: flex; justify-content: space-between; align-items: center;">
      <div>
        <p style="font-size: 0.85em; color: #ffffff; margin: 0; font-weight: bold;">Ram Awasthi</p>
        <p style="font-size: 0.75em; color: #718096; margin: 0;">AI Systems Researcher &amp; Engineer</p>
      </div>
      <div style="font-family: monospace; font-size: 0.8em; color: #5fa8d3;">
        github.com/Awasthi-Ram
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""
