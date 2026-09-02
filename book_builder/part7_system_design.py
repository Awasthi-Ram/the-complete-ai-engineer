# book_builder/part7_system_design.py

PART7_HTML = """
<!-- ████████████████████████████████████████████████████████████████████████
     PART 7 — SYSTEM DESIGN FOR AI ENGINEERS
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 7</div>
  <div class="part-title">System Design for AI Engineers</div>
  <div class="part-subtitle">The 7-Step Framework, Large-Scale Architectures, Ethics &amp; Explainability</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

<!-- ======================================================================
     CHAPTER 7.1 — AI SYSTEM DESIGN FRAMEWORK
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 7.1</span>
    <h2 class="chapter-title">AI System Design Framework</h2>
    <span class="chapter-subtitle">The 7-Step Blueprint &amp; Back-of-the-Envelope Capacity Estimation</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"System design is the art of making the right trade-offs under severe constraints."</p>
    <p class="attribution">— Systems Architect Principle</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Staff and Principal AI Engineer interviews at FAANG companies pivot around AI System Design. You are asked to design YouTube Recommendations, Google Search Autocomplete, or Uber Dynamic Surge Pricing. Success requires a structured 7-step blueprint that balances algorithmic precision with distributed systems realities.</p>

    <h3>1. The 7-Step AI System Design Blueprint</h3>
    <ol>
      <li><strong>Requirements Clarification:</strong> Functional scope, business KPIs, throughput (QPS), latency SLA (P99 < 50ms).</li>
      <li><strong>Back-of-the-Envelope Estimation:</strong> Daily active users, storage for feature tables, GPU memory bandwidth.</li>
      <li><strong>Data Pipeline & Feature Engineering:</strong> Ingestion, offline batch vs online streaming feature store.</li>
      <li><strong>Model Architecture Selection:</strong> Inductive bias, candidate generation vs heavy ranking.</li>
      <li><strong>Training & Evaluation Strategy:</strong> Loss formulation, offline AUC vs online A/B testing conversion lift.</li>
      <li><strong>Serving & High-Availability Deployment:</strong> Dynamic batching, caching, fallback heuristics.</li>
      <li><strong>Monitoring & Continuous Improvement:</strong> Feedback loops, position bias correction, drift alerting.</li>
    </ol>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 7.1 — Capacity & Hardware Sizing Estimator</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part7_ai_system_design/ch71_system_design_framework/capacity_estimator.py" target="_blank">🔗 View in GitHub: part7_ai_system_design/ch71_system_design_framework/capacity_estimator.py</a></p>
<pre><code>def estimate_capacity(dau=100_000_000, reqs_per_user=20, embed_dim=256):
    total_reqs = dau * reqs_per_user
    avg_qps = total_reqs / 86400
    peak_qps = avg_qps * 3
    ram_gb = (500_000_000 * embed_dim * 4) / (1024**3)
    return {"avg_qps": int(avg_qps), "peak_qps": int(peak_qps), "ram_gb": round(ram_gb, 1)}</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 7.2 — REAL-WORLD SYSTEM DESIGNS
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 7.2</span>
    <h2 class="chapter-title">Real-World System Designs</h2>
    <span class="chapter-subtitle">YouTube Recommendation Funnel, Search Autocomplete &amp; Fraud Scoring</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Complex systems that work are invariably found to have evolved from simple systems that worked."</p>
    <p class="attribution">— John Gall (Gall's Law)</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>At scale (1 billion+ videos, 100 million active users), scoring every video for every user on every page refresh requires $10^9 \times 10^8 = 10^{17}$ predictions per second—an impossibility. Real-world systems use a <strong>Multi-Stage Funnel Architecture</strong>.</p>

    <h3>1. The Two-Stage Funnel: Candidate Retrieval + Heavy Ranking</h3>
    <ul>
      <li><strong>Stage 1: Candidate Generation (Retrieval):</strong> Narrows the candidate universe from 1 billion items down to ~500 items in <10ms using fast two-tower embedding dot-products or approximate nearest neighbor (ANN) search.</li>
      <li><strong>Stage 2: Heavy Ranking:</strong> Takes the 500 candidates and passes them through a deep scoring network (Transformer/DLRM) evaluating hundreds of interaction features (user history, video age, device, time-of-day), sorting the final Top 10 feed.</li>
    </ul>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 7.2 — Two-Stage Recommendation Architecture</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part7_ai_system_design/ch72_real_world_architectures/two_stage_recommender.py" target="_blank">🔗 View in GitHub: part7_ai_system_design/ch72_real_world_architectures/two_stage_recommender.py</a></p>
<pre><code>import numpy as np

class TwoStageRecommender:
    def __init__(self, num_items=5000, dim=32):
        self.item_ids = [f"item_{i}" for i in range(num_items)]
        self.embeds = np.random.randn(num_items, dim)
        self.embeds /= np.linalg.norm(self.embeds, axis=1, keepdims=True)

    def retrieve_candidates(self, user_vec, k=50):
        scores = np.dot(self.embeds, user_vec)
        return [self.item_ids[i] for i in np.argsort(scores)[::-1][:k]]</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 7.3 — ETHICS, FAIRNESS & EXPLAINABILITY
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 7.3</span>
    <h2 class="chapter-title">Ethics, Fairness &amp; Explainability</h2>
    <span class="chapter-subtitle">SHAP Values, LIME &amp; The Mathematical Impossibility Theorem of Fairness</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Ethics is knowing the difference between what you have a right to do and what is right to do."</p>
    <p class="attribution">— Potter Stewart</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>As AI governs credit lending, hiring, medical diagnoses, and criminal sentencing, explaining <em>why</em> a model made a decision is legally and ethically mandatory (EU AI Act, GDPR Article 22).</p>

    <h3>1. SHAP (SHapley Additive exPlanations)</h3>
    <p>Lundberg and Lee (2017) unified feature attribution through cooperative game theory. The Shapley value $\phi_i$ assigns a unique payoff attribution to feature $i$ based on its marginal contribution across all possible feature coalitions $S \subseteq F \setminus \{i\}$:
    $$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]$$
    SHAP is the only feature attribution method guaranteed to satisfy efficiency, symmetry, dummy, and additivity axioms.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 7.3 — Permutation Feature Importance & Fairness Audit</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part7_ai_system_design/ch73_ethics_fairness_explainability/shap_values_permutation.py" target="_blank">🔗 View in GitHub: part7_ai_system_design/ch73_ethics_fairness_explainability/shap_values_permutation.py</a></p>
<pre><code>import numpy as np

def permutation_importance(predict_fn, X, y, metric):
    base_score = metric(y, predict_fn(X))
    imp = {}
    for j in range(X.shape[1]):
        X_p = X.copy()
        np.random.shuffle(X_p[:, j])
        imp[f"feat_{j}"] = base_score - metric(y, predict_fn(X_p))
    return imp</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     PROJECT 7 — TWO-STAGE RECOMMENDATION SYSTEM
     ====================================================================== -->
<div class="project-section">
  <div class="project-header">
    <span class="project-tag">Hands-On Project 7</span>
    <h3 class="project-title">Industrial Two-Stage Recommendation Engine Architecture</h3>
    <p class="project-desc">Architect and implement a candidate generation tower with approximate nearest neighbors (ANN) paired with a deep ranking model with real-time feature retrieval.</p>
    <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part7_ai_system_design/ch72_real_world_architectures/two_stage_recommender.py" target="_blank">🔗 Full Project Code: part7_ai_system_design/ch72_real_world_architectures/two_stage_recommender.py</a></p>
  </div>
  <div class="project-body">
    <p><strong>Architecture Overview:</strong> You will simulate a catalog of 1,000,000 items, build an HNSW index to retrieve top-100 candidates in under 3ms, evaluate contextual features through a ranker model, and output personalized Top-10 recommendations under a 15ms P99 SLA.</p>
  </div>
</div>
"""
