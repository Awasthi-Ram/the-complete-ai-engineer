"""
embed_remaining_diagrams.py — Injects the 31 newly generated diagrams into
their respective chapters in book_builder/ with proper figures and captions.
"""
import os
import re

DIAGRAM_SPECS = [
    {
        'file': 'book_builder/ch02_python_a_to_z.html',
        'img': 'python_memory_object_model.png',
        'fig': '0.2.1',
        'caption': 'CPython dynamic memory overhead versus NumPy contiguous buffer. A standard Python list allocates an array of 64-bit pointers pointing to disparate heap-allocated PyObject instances with refcount and type headers, resulting in cache misses and pointer-chasing. In contrast, NumPy allocates a single contiguous memory block with shape and stride metadata, enabling SIMD vectorization and hardware prefetching.'
    },
    {
        'file': 'book_builder/ch04_large_scale_data.html',
        'img': 'data_lakehouse_medallion.png',
        'fig': '0.4.1',
        'caption': 'The Medallion Lakehouse Architecture for Enterprise AI Pipelines. Raw telemetry streams and batch dumps enter the Bronze tier in append-only mode, pass through deduplication, validation, and schema enforcement into the Silver Parquet tier, and are aggregated into the Gold tier for feature stores, vector embeddings, and training-ready dataset splits.'
    },
    {
        'file': 'book_builder/ch13_probability_bayes.html',
        'img': 'bayesian_inference_update.png',
        'fig': '1.3.1',
        'caption': 'Bayesian updating under parameter estimation. The broad initial prior distribution $P(\\theta)$ expresses epistemic uncertainty. Conditioning on observed evidence through likelihood $P(D \\mid \\theta)$ sharpens belief into posterior distribution $P(\\theta \\mid D) \\propto P(D \\mid \\theta) P(\\theta)$, simultaneously reducing variance and shifting expectation toward empirical truth.'
    },
    {
        'file': 'book_builder/ch14_information_theory.html',
        'img': 'information_theory_venn.png',
        'fig': '1.4.1',
        'caption': 'Information-theoretic entropy Venn diagram. Illustrating the decomposition of joint entropy $H(X, Y)$ into marginal entropies $H(X)$ and $H(Y)$, conditional uncertainties $H(X \\mid Y)$ and $H(Y \\mid X)$, and mutual information $I(X; Y) = H(X) + H(Y) - H(X, Y)$, representing shared information content.'
    },
    {
        'file': 'book_builder/ch21_ml_paradigm.html',
        'img': 'bias_variance_tradeoff.png',
        'fig': '2.1.1',
        'caption': 'The Bias-Variance Decomposition and Generalization Bounds. As model capacity increases, squared bias monotonically decreases while variance rises. The optimal generalization sweet spot minimizes total test error. In modern overparameterized neural networks, double descent occurs beyond the interpolation threshold.'
    },
    {
        'file': 'book_builder/ch22_linear_regression.html',
        'img': 'lasso_vs_ridge_contours.png',
        'fig': '2.2.1',
        'caption': 'Geometric duality of Lasso ($\\ell_1$) versus Ridge ($\\ell_2$) regularization. The sharp diamond corners of the $\\ell_1$ norm ball align with coordinate axes, causing loss contour tangents to hit exact zeros (sparse feature selection). The smooth $\\ell_2$ circular ball shrinks weights uniformly without zeroing coefficients.'
    },
    {
        'file': 'book_builder/ch23_logistic_regression.html',
        'img': 'logistic_sigmoid_boundary.png',
        'fig': '2.3.1',
        'caption': 'The Logistic Sigmoid mapping and separating hyperplane. The linear combination $z = \\mathbf{w}^T \\mathbf{x} + b$ is squashed through non-linear activation $\\sigma(z) = 1/(1 + e^{-z})$ into calibrated posterior class probabilities $P(Y=1 \\mid \\mathbf{x})$. The threshold $p=0.5$ defines the orthogonal decision hyperplane.'
    },
    {
        'file': 'book_builder/ch24_decision_trees.html',
        'img': 'decision_tree_partitioning.png',
        'fig': '2.4.1',
        'caption': 'Decision tree binary splitting and feature space geometry. Left: The hierarchical recursive tree selects greedy splits maximizing Information Gain or Gini impurity reduction. Right: The corresponding axis-aligned orthogonal rectangular partitioning of the input feature space into homogeneous prediction regions.'
    },
    {
        'file': 'book_builder/ch25_random_forests.html',
        'img': 'random_forest_bagging.png',
        'fig': '2.5.1',
        'caption': 'Random Forest architecture: Bootstrap Aggregation (Bagging) combined with Random Feature Subspaces. Training $B$ deep, uncorrelated decision trees on independent bootstrap samples and aggregating via majority voting reduces variance by a factor of $1/B$ while preserving low bias.'
    },
    {
        'file': 'book_builder/ch25b_gradient_boosting.html',
        'img': 'gradient_boosting_residuals.png',
        'fig': '2.5b.1',
        'caption': 'Gradient Boosted Decision Trees (GBDT) sequential additive modeling. Rather than training independent trees in parallel, each consecutive tree $h_m(\\mathbf{x})$ is trained to predict the negative gradient (pseudo-residuals) of the loss with respect to previous ensemble predictions $F_{m-1}(\\mathbf{x})$, scaled by shrinkage factor $\\eta$.'
    },
    {
        'file': 'book_builder/ch27_unsupervised_kmeans_pca.html',
        'img': 'kmeans_pca_manifold.png',
        'fig': '2.7.1',
        'caption': 'Unsupervised Learning foundations. Left: K-Means clustering partitions space into convex Voronoi cells bounded by hyperplanes equidistant between cluster centroids $\\boldsymbol{\\mu}_k$. Right: Principal Component Analysis (PCA) identifies orthogonal eigenvectors maximizing projected variance $\\lambda_1 > \\lambda_2$.'
    },
    {
        'file': 'book_builder/ch28_feature_engineering.html',
        'img': 'data_leakage_temporal_split.png',
        'fig': '2.8.1',
        'caption': 'Feature engineering and temporal data leakage prevention. Scalers, encoders, and target statistics must be fit strictly on the historical training window $[0, T_{split}]$ and applied to test windows via transform-only semantics. Global preprocessing leaks future information into past training, causing catastrophic production failure.'
    },
    {
        'file': 'book_builder/ch29_model_evaluation.html',
        'img': 'roc_pr_calibration_curves.png',
        'fig': '2.9.1',
        'caption': 'Diagnostic classification evaluation curves. Left: The Receiver Operating Characteristic (ROC) curve plots True Positive Rate versus False Positive Rate across all decision thresholds, with Area Under the Curve (AUC) measuring rank discrimination. Right: The Precision-Recall (PR) curve reliably evaluates severely imbalanced datasets.'
    },
    {
        'file': 'book_builder/ch32_mlp_activations.html',
        'img': 'modern_activation_functions.png',
        'fig': '3.2.1',
        'caption': 'Comparison of modern neural activation functions. While standard ReLU suffers from dying neurons in negative saturation, modern activations like GELU and Swish/SiLU introduce smooth, non-monotonic curvature with non-zero negative gradients, stabilizing deep transformer and residual training.'
    },
    {
        'file': 'book_builder/ch34_deep_optimization.html',
        'img': 'deep_optimizers_trajectories.png',
        'fig': '3.4.1',
        'caption': 'Optimization dynamics in an ill-conditioned quadratic ravine. Standard SGD oscillates severely along high-curvature walls with negligible longitudinal progress. Momentum accelerates along the ravine axis by dampening cross-valley velocity, while AdamW rescales step sizes per-coordinate using exponential moving averages of squared gradients.'
    },
    {
        'file': 'book_builder/ch36_pytorch_production.html',
        'img': 'ddp_ring_allreduce.png',
        'fig': '3.6.1',
        'caption': 'PyTorch Distributed Data Parallel (DDP) Ring-AllReduce communication topology. $N$ GPUs pass gradient tensor slices in a logical ring across Scatter-Reduce and AllGather phases. Total network data transferred per GPU is exactly $2 \\cdot \\frac{N-1}{N} \\cdot S$, achieving bandwidth optimality independent of cluster size.'
    },
    {
        'file': 'book_builder/ch37_jax_functional_dl.html',
        'img': 'jax_primitives_pipeline.png',
        'fig': '3.7.1',
        'caption': 'The JAX functional transformation pipeline. Pure Python mathematical functions are transformed via reverse-mode auto-differentiation (`jax.grad`) and vectorization (`jax.vmap`), traced into high-level jaxpr IR, and just-in-time compiled (`jax.jit`) by XLA into fused hardware-optimized GPU/TPU machine kernels.'
    },
    {
        'file': 'book_builder/ch43_vaes_gans.html',
        'img': 'vae_gan_architectures.png',
        'fig': '4.3.1',
        'caption': 'Generative modeling paradigms. Top: Variational Autoencoders (VAEs) map inputs to distribution parameters $(\\boldsymbol{\\mu}, \\boldsymbol{\\sigma})$ and apply the reparameterization trick $\\mathbf{z} = \\boldsymbol{\\mu} + \\boldsymbol{\\sigma} \\odot \\boldsymbol{\\epsilon}$ to backpropagate through stochastic latents. Bottom: Generative Adversarial Networks (GANs) pit Generator $G(\\mathbf{z})$ against Discriminator $D(\\mathbf{x})$ in a zero-sum minimax game.'
    },
    {
        'file': 'book_builder/ch46_audio_whisper.html',
        'img': 'whisper_audio_pipeline.png',
        'fig': '4.6.1',
        'caption': 'The Whisper multilingual speech recognition architecture. Continuous 16 kHz audio waveforms are converted into 80-channel log-mel filterbank spectrograms, downsampled via 1D convolutions with stride 2, and processed by an encoder-decoder transformer emitting language identification, timestamps, and transcribed text tokens.'
    },
    {
        'file': 'book_builder/ch52_tokenization_huggingface.html',
        'img': 'bpe_tokenization_flow.png',
        'fig': '5.2.1',
        'caption': 'Byte-Pair Encoding (BPE) iterative subword merge hierarchy. Starting from raw character bytes, the tokenizer greedily merges the highest-frequency adjacent bigrams into subwords, balancing fixed vocabulary size against out-of-vocabulary representation and compact sequence lengths.'
    },
    {
        'file': 'book_builder/ch54_llamaindex_graphrag.html',
        'img': 'graphrag_hybrid_retrieval.png',
        'fig': '5.4.1',
        'caption': 'GraphRAG hybrid retrieval architecture. Unstructured text is indexed into both dense vector chunk embeddings and a knowledge graph with extracted entities and relations. Incoming user queries retrieve relevant semantic passages and traverse structural graph communities before passing through hybrid rerankers for LLM generation.'
    },
    {
        'file': 'book_builder/ch56_alignment_rlhf_dpo.html',
        'img': 'alignment_rlhf_vs_dpo.png',
        'fig': '5.6.1',
        'caption': 'LLM preference alignment paradigms. Left: Classical 3-stage RLHF trains a separate reward model on pairwise human ratings and optimizes the policy via PPO actor-critic with KL penalties. Right: Direct Preference Optimization (DPO) derives an exact closed-form implicit reward, optimizing policy weights directly on preference pairs without reinforcement learning instabilities.'
    },
    {
        'file': 'book_builder/ch57_langchain_lcel.html',
        'img': 'lcel_runnable_dag.png',
        'fig': '5.7.1',
        'caption': 'LangChain Expression Language (LCEL) streaming DAG execution. Declarative pipe composition (`prompt | model | parser`) compiles into an asynchronous streaming generator supporting parallel branches, fallbacks, and typed Pydantic validation.'
    },
    {
        'file': 'book_builder/ch59_coding_agents.html',
        'img': 'react_coding_agent_loop.png',
        'fig': '5.9.1',
        'caption': 'Autonomous Software Engineering Agent ReAct Execution Cycle. The agent iteratively reasons over workspace state (Thought), executes shell/code actions (Action), observes stdout/compiler feedback (Observation), and self-corrects syntax and test regressions until verification succeeds.'
    },
    {
        'file': 'book_builder/ch61_experiment_tracking.html',
        'img': 'mlops_experiment_registry.png',
        'fig': '6.1.1',
        'caption': 'Production MLOps lifecycle from experiment tracking to model governance. Training runs capture hyperparameter dictionaries, evaluation metric series, and artifact weights. Validated models are registered centrally, progressing through Staging, Canary, and Production stages.'
    },
    {
        'file': 'book_builder/ch62_feature_stores.html',
        'img': 'feature_store_architecture.png',
        'fig': '6.2.1',
        'caption': 'Enterprise Feature Store dual-storage topology. Batch and streaming ingestion pipelines write to an immutable offline Parquet lakehouse for point-in-time correct training splits, while syncing to an online key-value store (Redis) for sub-5 millisecond real-time inference lookups.'
    },
    {
        'file': 'book_builder/ch63_containerization_docker.html',
        'img': 'docker_multistage_cuda.png',
        'fig': '6.3.1',
        'caption': 'Multi-stage Docker builds for production AI. Stage 1 compiles C++ extensions and wheels inside a heavy CUDA development image (~18 GB). Stage 2 copies only compiled artifacts and Python virtualenvs into a slim runtime image (~2.1 GB), eliminating 88% of container bloat and hardening security.'
    },
    {
        'file': 'book_builder/ch65_drift_observability.html',
        'img': 'drift_observability_pipeline.png',
        'fig': '6.5.1',
        'caption': 'Continuous model observability and automated retraining loop. Live production feature distributions and prediction outputs are continuously compared against baseline distributions using Population Stability Index (PSI) and Kolmogorov-Smirnov tests, triggering automated retraining pipelines upon significant drift.'
    },
    {
        'file': 'book_builder/ch72_vector_search_scale.html',
        'img': 'hnsw_hierarchical_graph.png',
        'fig': '7.2.1',
        'caption': 'Hierarchical Navigable Small World (HNSW) vector search. The multi-layer proximity graph executes coarse greedy routing across sparse top layers before descending into dense base layers, locating approximate $k$-nearest neighbors in $\\mathcal{O}(\\log N)$ time with high recall.'
    },
    {
        'file': 'book_builder/ch82_test_time_compute.html',
        'img': 'test_time_search_trees.png',
        'fig': '8.2.1',
        'caption': 'Test-Time Compute scaling and reasoning search trees. Rather than relying on single greedy Chain-of-Thought paths that compound errors, test-time scaling explores trees of thoughts via Monte Carlo Tree Search (MCTS), evaluated at each intermediate token step by Process Reward Models (PRMs).'
    },
    {
        'file': 'book_builder/ch83_energy_hardware_limits.html',
        'img': 'ai_datacenter_energy_limits.png',
        'fig': '8.3.1',
        'caption': 'The physical thermodynamic and power scaling hierarchy of AI compute. Heat dissipation escalates from silicon die thermal design power (700W–1000W) to high-density liquid CDU racks (120 kW) and gigawatt data center substations, constrained by wire resistance and Landauer\'s thermodynamic limit.'
    }
]

print("Injecting diagrams into book_builder chapter HTML files...")
embedded_count = 0

for item in DIAGRAM_SPECS:
    filepath = item['file']
    if not os.path.exists(filepath):
        print(f"  [ERROR] File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as fp:
        content = fp.read()
        
    img_name = item['img']
    if img_name in content:
        print(f"  [SKIPPED] {img_name} already present in {filepath}")
        continue
        
    fig_html = f'''
    <div class="diagram-figure">
        <img src="{img_name}" alt="Figure {item['fig']}: {item['img'].replace('_', ' ').replace('.png', '')}">
        <div class="diagram-caption"><strong>Figure {item['fig']}:</strong> {item['caption']}</div>
    </div>
'''

    # Find the first <h2> or <h3> tag or top of chapter after <h1>
    # Best location: after the first <h2> and its following paragraph <p>...</p>
    h2_match = re.search(r'(<h2[^>]*>.*?</h2>\s*<p>.*?</p>)', content, re.DOTALL)
    if h2_match:
        target = h2_match.group(1)
        new_content = content.replace(target, target + '\n' + fig_html, 1)
    else:
        # Fallback: after the first <h1> and its following <p>
        h1_match = re.search(r'(<h1[^>]*>.*?</h1>\s*(?:<p>.*?</p>)?)', content, re.DOTALL)
        if h1_match:
            target = h1_match.group(1)
            new_content = content.replace(target, target + '\n' + fig_html, 1)
        else:
            # Fallback: insert near top
            new_content = fig_html + '\n' + content
            
    with open(filepath, 'w', encoding='utf-8') as fp:
        fp.write(new_content)
        
    print(f"  [EMBEDDED] {img_name} -> {filepath}")
    embedded_count += 1

print(f"\nEmbedding complete! Successfully embedded {embedded_count} diagrams.")
