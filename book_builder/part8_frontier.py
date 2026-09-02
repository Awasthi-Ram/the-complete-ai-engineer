# book_builder/part8_frontier.py

PART8_HTML = """
<!-- ████████████████████████████████████████████████████████████████████████
     PART 8 — ADVANCED TOPICS & THE FRONTIER
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 8</div>
  <div class="part-title">Advanced Topics &amp; The Frontier</div>
  <div class="part-subtitle">Multimodal Intelligence, Reinforcement Learning, Model Optimization &amp; Your Career</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

<!-- ======================================================================
     CHAPTER 8.1 — MULTIMODAL AI
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 8.1</span>
    <h2 class="chapter-title">Multimodal AI</h2>
    <span class="chapter-subtitle">Vision Meets Language with Contrastive Learning (CLIP)</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Sight and sound and speech are not separate faculties; they are different windows onto the same reality."</p>
    <p class="attribution">— Cognitive Science Principle</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Human intelligence does not perceive language in an acoustic vacuum or vision without symbolic conceptual grounding. Multimodal AI bridges the sensory divide, projecting images, video, audio, and text into a unified semantic hypersphere.</p>

    <h3>1. Contrastive Language-Image Pre-training (CLIP)</h3>
    <p>Radford et al. (OpenAI, 2021) demonstrated that training an image encoder (ViT) and text encoder (Transformer) jointly using a symmetric contrastive loss over 400 million internet image-text pairs creates zero-shot classifiers that rival supervised ImageNet models. For a batch of $N$ image-text pairs, the model maximizes the cosine similarity of true $(I_i, T_i)$ pairs while penalizing all $N^2 - N$ incorrect pairings via symmetric InfoNCE loss:
    $$\mathcal{L}_{\text{InfoNCE}} = \frac{1}{2} \left( \mathcal{L}_{I \to T} + \mathcal{L}_{T \to I} \right)$$</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 8.1 — CLIP Contrastive InfoNCE Loss from Scratch</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part8_frontier/ch81_multimodal_clip/clip_zero_shot_classifier.py" target="_blank">🔗 View in GitHub: part8_frontier/ch81_multimodal_clip/clip_zero_shot_classifier.py</a></p>
<pre><code>import numpy as np

def clip_loss(img_emb, txt_emb, temp=0.07):
    I_n = img_emb / np.linalg.norm(img_emb, axis=1, keepdims=True)
    T_n = txt_emb / np.linalg.norm(txt_emb, axis=1, keepdims=True)
    logits = (I_n @ T_n.T) / temp
    N = len(img_emb)
    # Symmetric Cross Entropy
    exp_l = np.exp(logits - np.max(logits, axis=1, keepdims=True))
    probs = exp_l / np.sum(exp_l, axis=1, keepdims=True)
    return -np.mean(np.log(probs[np.arange(N), np.arange(N)] + 1e-12))</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 8.2 — REINFORCEMENT LEARNING
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 8.2</span>
    <h2 class="chapter-title">Reinforcement Learning</h2>
    <span class="chapter-subtitle">Markov Decision Processes, Bellman Optimality &amp; RLHF in LLMs</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"We are what we repeatedly do. Excellence, then, is not an act, but a habit."</p>
    <p class="attribution">— Will Durant</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>In supervised learning, the model is given correct ground-truth labels. In Reinforcement Learning (RL), an agent learns through trial and error, taking actions in an environment to maximize cumulative future rewards.</p>

    <h3>1. The Bellman Optimality Equation</h3>
    <p>In a Markov Decision Process $(S, A, P, R, \gamma)$, the optimal action-value function $Q^*(s, a)$ satisfies the fundamental recursive identity:
    $$Q^*(s, a) = R(s, a) + \gamma \sum_{s' \in S} P(s'|s, a) \max_{a'} Q^*(s', a')$$
    In model-free <strong>Q-Learning</strong>, the temporal difference (TD) update rule is:
    $$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 8.2 — Tabular Q-Learning on GridWorld</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part8_frontier/ch82_reinforcement_learning/q_learning_gridworld.py" target="_blank">🔗 View in GitHub: part8_frontier/ch82_reinforcement_learning/q_learning_gridworld.py</a></p>
<pre><code>class GridWorldQLearner:
    def __init__(self, states=16, actions=4, alpha=0.1, gamma=0.95):
        self.Q = np.zeros((states, actions))
        self.alpha, self.gamma = alpha, gamma

    def update(self, s, a, r, s_next):
        td_target = r + self.gamma * np.max(self.Q[s_next])
        self.Q[s, a] += self.alpha * (td_target - self.Q[s, a])</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 8.3 — MODEL OPTIMIZATION
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 8.3</span>
    <h2 class="chapter-title">Model Optimization</h2>
    <span class="chapter-subtitle">Post-Training Quantization (INT8/4-bit), Pruning &amp; Knowledge Distillation</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."</p>
    <p class="attribution">— Antoine de Saint-Exupéry</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Deploying state-of-the-art models to edge devices, smartphones, or cost-efficient cloud servers requires compressing neural parameters without sacrificing predictive accuracy.</p>

    <h3>1. Post-Training Quantization (PTQ): FP32 to INT8</h3>
    <p>Mapping 32-bit floating-point tensors onto 8-bit integers $[-128, 127]$ cuts memory consumption by 75% and activates high-throughput INT8 Tensor Cores. The affine quantization mapping is:
    $$q = \text{round}\left(\frac{x}{S}\right) + Z, \quad \text{where } S = \frac{\beta - \alpha}{q_{\max} - q_{\min}}, \quad Z = \text{round}\left(q_{\min} - \frac{\alpha}{S}\right)$$
    Where $[\alpha, \beta]$ is the dynamic range of real values.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 8.3 — INT8 Quantizer & Dequantizer from Scratch</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part8_frontier/ch83_model_quantization_pruning/int8_quantizer_from_scratch.py" target="_blank">🔗 View in GitHub: part8_frontier/ch83_model_quantization_pruning/int8_quantizer_from_scratch.py</a></p>
<pre><code>import numpy as np

def quantize_int8(x):
    alpha, beta = float(np.min(x)), float(np.max(x))
    scale = (beta - alpha) / 255.0
    zero_point = int(np.round(-128 - alpha / scale))
    q = np.clip(np.round(x / scale) + zero_point, -128, 127).astype(np.int8)
    return q, scale, zero_point</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 8.4 — YOUR CAREER AS AN AI ENGINEER
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 8.4</span>
    <h2 class="chapter-title">Your Career as an AI Engineer</h2>
    <span class="chapter-subtitle">Paper Reading Discipline, Portfolio Strategy &amp; The FAANG Interview Rubric</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"The future belongs to those who learn more skills and combine them in creative ways."</p>
    <p class="attribution">— Robert Greene</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>You have now completed the entire journey from Python foundations and school-level calculus to transformers, RAG pipelines, and cloud MLOps. But technical knowledge alone is inert without a disciplined career operating system.</p>

    <h3>1. The 3-Pass Method for Reading AI Research Papers</h3>
    <ol>
      <li><strong>Pass 1 (Bird's Eye, 10 mins):</strong> Read Title, Abstract, Introduction, and examine Figure 1 and Table 1 benchmarks. Decide whether the paper introduces a fundamentally new inductive bias or merely incremental parameter tuning.</li>
      <li><strong>Pass 2 (The Mechanics, 45 mins):</strong> Work through the problem formulation, loss function derivation, and architecture diagram. Note unfamiliar mathematical operators.</li>
      <li><strong>Pass 3 (Virtual Re-implementation, 2–3 hours):</strong> Mentally or programmatically recreate the core algorithm from raw math, comparing your implementation against the official open-source release.</li>
    </ol>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 8.4 — Production Go-Live Readiness Audit Tool</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part8_frontier/ch84_career_roadmap/production_ml_readiness_checklist.py" target="_blank">🔗 View in GitHub: part8_frontier/ch84_career_roadmap/production_ml_readiness_checklist.py</a></p>
<pre><code>def run_production_audit(meta):
    checks = {
        "Has Baseline Benchmark": "baseline" in meta,
        "Input Schema Validated": meta.get("schema_ok", False),
        "P99 Latency < 50ms": meta.get("p99_ms", 999) < 50,
        "Rollback Ready": meta.get("canary_ready", False)
    }
    return {"passed": all(checks.values()), "checks": checks}</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     PROJECT 8 — MULTIMODAL IMAGE SEARCH & CAPTIONING
     ====================================================================== -->
<div class="project-section">
  <div class="project-header">
    <span class="project-tag">Hands-On Project 8</span>
    <h3 class="project-title">Multimodal Zero-Shot Search & Caption Generator</h3>
    <p class="project-desc">Combine CLIP contrastive visual embeddings with an autoregressive language decoder to build a natural language image search engine and automatic image captioning system.</p>
    <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part8_frontier/ch81_multimodal_clip/clip_zero_shot_classifier.py" target="_blank">🔗 Full Project Code: part8_frontier/ch81_multimodal_clip/clip_zero_shot_classifier.py</a></p>
  </div>
  <div class="project-body">
    <p><strong>Architecture Overview:</strong> You will extract image embeddings across a collection of photographs, build an index, project natural language search queries into the same hypersphere, and generate descriptive textual captions using zero-shot semantic matching.</p>
  </div>
</div>
"""
