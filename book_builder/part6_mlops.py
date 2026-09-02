# book_builder/part6_mlops.py

PART6_HTML = """
<!-- ████████████████████████████████████████████████████████████████████████
     PART 6 — MLOPS & PRODUCTION AI
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 6</div>
  <div class="part-title">MLOps &amp; Production AI</div>
  <div class="part-subtitle">Experiment Tracking, Low-Latency Serving, Drift Detection & Cloud Infrastructure</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

<!-- ======================================================================
     CHAPTER 6.1 — EXPERIMENT TRACKING
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 6.1</span>
    <h2 class="chapter-title">Experiment Tracking &amp; Versioning</h2>
    <span class="chapter-subtitle">The Scientific Discipline of Production Machine Learning</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Without data, you're just another person with an opinion."</p>
    <p class="attribution">— W. Edwards Deming</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>In classical software engineering, Git versions your code deterministically. In machine learning, code alone is insufficient: a model is the output of <strong>Code + Data + Hyperparameters + Hardware Environment</strong>. If you cannot reproduce a model down to the exact floating-point weights, it cannot be safely deployed to production.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 6.1 — Minimal Experiment Tracker & Artifact Logger</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part6_mlops_production/ch61_experiment_tracking/experiment_logger.py" target="_blank">🔗 View in GitHub: part6_mlops_production/ch61_experiment_tracking/experiment_logger.py</a></p>
<pre><code>import json, time

class MinimalExperimentTracker:
    def __init__(self, exp_name):
        self.exp_name, self.runs = exp_name, []

    def log_run(self, run_id, params, metrics, artifact):
        self.runs.append({
            "run_id": run_id, "params": params, "metrics": metrics,
            "artifact": artifact, "timestamp": time.time()
        })</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 6.2 — MODEL SERVING & DEPLOYMENT
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 6.2</span>
    <h2 class="chapter-title">Model Serving &amp; Deployment</h2>
    <span class="chapter-subtitle">FastAPI, ONNX Runtime, Triton Inference Server &amp; Dynamic Batching</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"A model that cannot be served in production is merely expensive academic art."</p>
    <p class="attribution">— Production Engineering Maxim</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Training a model in a Python notebook is only 20% of the engineering journey. Serving a model to handle 10,000 queries per second with a strict 20-millisecond P99 latency SLA requires compiled execution runtimes, asynchronous request queuing, and dynamic batching.</p>

    <h3>1. The Inference Latency Budget</h3>
    <p>A typical 50ms user request budget breaks down into:
    <ul>
      <li><strong>Network Round-Trip (TLS + CDN):</strong> 20–25 ms</li>
      <li><strong>API Gateway & Auth:</strong> 3–5 ms</li>
      <li><strong>Feature Store Lookup:</strong> 3–5 ms</li>
      <li><strong>Model Preprocessing & Tokenization:</strong> 2–4 ms</li>
      <li><strong>Model Forward Pass (GPU/ONNX):</strong> <strong>8–15 ms</strong></li>
    </ul></p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 6.2 — Low-Latency FastAPI Serving Endpoint with Pydantic</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part6_mlops_production/ch62_model_serving_fastapi/fastapi_inference_server.py" target="_blank">🔗 View in GitHub: part6_mlops_production/ch62_model_serving_fastapi/fastapi_inference_server.py</a></p>
<pre><code>from pydantic import BaseModel
import time

class InferenceRequest(BaseModel):
    features: list[float]

def predict_endpoint(req: InferenceRequest):
    t0 = time.perf_counter()
    prob = 1.0 / (1.0 + np.exp(-sum(req.features)))
    latency = (time.perf_counter() - t0) * 1000
    return {"prediction": int(prob >= 0.5), "prob": prob, "latency_ms": latency}</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 6.3 — MONITORING & DRIFT DETECTION
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 6.3</span>
    <h2 class="chapter-title">Monitoring &amp; Drift Detection</h2>
    <span class="chapter-subtitle">Covariate Shift, Concept Drift &amp; Population Stability Index (PSI)</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Everything flows, nothing stands still."</p>
    <p class="attribution">— Heraclitus</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Models degrade silently. Unlike standard software services that crash with an explicit HTTP 500 error, a decaying machine learning model continues returning HTTP 200 OK responses with high confidence while making completely erroneous business decisions.</p>

    <h3>1. The Taxonomy of Drift</h3>
    <ul>
      <li><strong>Covariate Shift (Data Drift):</strong> Input distribution $P(\mathbf{x})$ shifts while conditional target mapping $P(y|\mathbf{x})$ remains unchanged (e.g. mobile app updates change user demographics).</li>
      <li><strong>Concept Drift:</strong> The underlying relationship $P(y|\mathbf{x})$ shifts (e.g. macroeconomic inflation shifts user spending patterns).</li>
      <li><strong>Prior Probability Shift:</strong> Class prevalence $P(y)$ shifts (e.g. holiday seasonality increases conversion rates).</li>
    </ul>

    <h3>2. Population Stability Index (PSI)</h3>
    <p>PSI compares the quantile distribution of production inference features against training baselines:
    $$\text{PSI} = \sum_{b=1}^B \left( \% \text{Actual}_b - \% \text{Expected}_b \right) \times \ln\left( \frac{\% \text{Actual}_b}{\% \text{Expected}_b} \right)$$
    Industry benchmarks: $\text{PSI} < 0.1$: No change; $0.1 \le \text{PSI} < 0.2$: Moderate shift; $\text{PSI} \ge 0.2$: Significant drift requiring automated model retraining.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 6.3 — Population Stability Index (PSI) Drift Detector</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part6_mlops_production/ch63_drift_monitoring/drift_detector_psi_ks.py" target="_blank">🔗 View in GitHub: part6_mlops_production/ch63_drift_monitoring/drift_detector_psi_ks.py</a></p>
<pre><code>import numpy as np

def calculate_psi(expected, actual, num_buckets=10, eps=1e-4):
    bins = np.percentile(expected, np.linspace(0, 100, num_buckets + 1))
    exp_pct = np.histogram(expected, bins=bins)[0] / len(expected) + eps
    act_pct = np.histogram(actual, bins=bins)[0] / len(actual) + eps
    return np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct))</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 6.4 — DATA PIPELINES & FEATURE STORES
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 6.4</span>
    <h2 class="chapter-title">Data Pipelines &amp; Feature Stores</h2>
    <span class="chapter-subtitle">Online vs Offline Stores, Point-in-Time Correctness &amp; Schema Validation</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Data is the new oil, but only if it is refined."</p>
    <p class="attribution">— Clive Humby</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>A feature store serves as the unified data layer between training and inference, ensuring features are calculated identically offline in batch analytics (Snowflake/BigQuery) and online in real-time key-value stores (Redis/DynamoDB) with sub-5ms lookup latency.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 6.4 — Data Schema Validation Contract</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part6_mlops_production/ch64_data_feature_pipelines/schema_validator.py" target="_blank">🔗 View in GitHub: part6_mlops_production/ch64_data_feature_pipelines/schema_validator.py</a></p>
<pre><code>class DataValidator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, record):
        errors = []
        for field, rules in self.schema.items():
            if field in record and "min" in rules and record[field] < rules["min"]:
                errors.append(f"{field} under min threshold {rules['min']}")
        return errors</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 6.5 — CLOUD ML PLATFORMS
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 6.5</span>
    <h2 class="chapter-title">Cloud ML Platforms</h2>
    <span class="chapter-subtitle">AWS SageMaker, GCP Vertex AI, Spot Instance Sizing &amp; Cost Engineering</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Architecture is the art of how to waste space; engineering is the science of how to save money."</p>
    <p class="attribution">— Cloud Infrastructure Adage</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Running high-end GPU clusters (e.g. 8x NVIDIA H100 nodes at $30/hour per node) can burn hundreds of thousands of dollars in days. Cloud ML engineering involves choosing between managed platforms (AWS SageMaker, Google Cloud Vertex AI, Azure ML) and orchestrating spot instances with automated atomic checkpointing to slash compute expenditure by 60–70%.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 6.5 — Production Multi-Stage Dockerfile for AI Serving</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part6_mlops_production/ch65_cloud_deployment/Dockerfile" target="_blank">🔗 View in GitHub: part6_mlops_production/ch65_cloud_deployment/Dockerfile</a></p>
<pre><code>FROM python:3.11-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "fastapi_inference_server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     PROJECT 6 — END-TO-END MLOPS PIPELINE
     ====================================================================== -->
<div class="project-section">
  <div class="project-header">
    <span class="project-tag">Hands-On Project 6</span>
    <h3 class="project-title">End-to-End Production MLOps Pipeline</h3>
    <p class="project-desc">Containerize a production model inference service with FastAPI, Docker, Prometheus telemetry monitoring, automated PSI drift detection, and canary rollback routing.</p>
    <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part6_mlops_production/ch62_model_serving_fastapi/fastapi_inference_server.py" target="_blank">🔗 Full Project Code: part6_mlops_production/ch62_model_serving_fastapi/fastapi_inference_server.py</a></p>
  </div>
  <div class="project-body">
    <p><strong>Architecture Overview:</strong> You will build a Dockerized REST API that ingests customer records, executes model inference under a 15ms SLA, logs feature distributions to Prometheus, and triggers an automated alerting webhook when statistical drift is detected.</p>
  </div>
</div>
"""
