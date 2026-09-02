# book_builder/part3_neural_networks.py

PART3_HTML = """
<!-- ████████████████████████████████████████████████████████████████████████
     PART 3 — NEURAL NETWORKS FROM SCRATCH
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 3</div>
  <div class="part-title">Neural Networks from Scratch</div>
  <div class="part-subtitle">The Perceptron, Multi-Layer Architectures, Analytical Backpropagation & Optimization</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

<!-- ======================================================================
     CHAPTER 3.1 — THE NEURON & PERCEPTRON
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 3.1</span>
    <h2 class="chapter-title">The Neuron &amp; Perceptron</h2>
    <span class="chapter-subtitle">Biological Inspiration to Mathematical Formulation &amp; The XOR Barrier</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"The perceptron may eventually be able to learn, make decisions, and translate languages."</p>
    <p class="attribution">— Frank Rosenblatt (1958)</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>In 1943, Warren McCulloch and Walter Pitts modeled the biological neuron as a simplified computational unit: inputs arrive through dendrites, weights represent synaptic strengths, the cell body sums incoming potentials, and if the total exceeds a threshold, an action potential fires down the axon. In 1958, Frank Rosenblatt created the <strong>Perceptron</strong>, introducing the first algorithmic learning rule.</p>

    <div class="real-world-box">
      <h4>🏢 Real-World Problem Mapping: The Historic AI Winter & The XOR Failure</h4>
      <p>In 1969, Marvin Minsky and Seymour Papert published their famous book <em>Perceptrons</em>, mathematically proving that a single-layer perceptron could not even compute the simple XOR (Exclusive OR) logical function. The inability to solve non-linearly separable problems led to the collapse of AI research funding for over a decade. Understanding how hidden layers bypass this linear barrier is the birth story of deep learning.</p>
    </div>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 3.1 — Perceptron Learning Rule & XOR Failure Proof</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part3_neural_networks/ch31_perceptron/perceptron_and_xor.py" target="_blank">🔗 View in GitHub: part3_neural_networks/ch31_perceptron/perceptron_and_xor.py</a></p>
<pre><code>import numpy as np

class Perceptron:
    def __init__(self, lr=0.1, epochs=20):
        self.lr, self.epochs = lr, epochs

    def fit(self, X, y):
        self.w, self.b = np.zeros(X.shape[1]), 0.0
        for _ in range(self.epochs):
            for i, x_i in enumerate(X):
                y_hat = 1 if np.dot(x_i, self.w) + self.b >= 0 else 0
                error = y[i] - y_hat
                self.w += self.lr * error * x_i
                self.b += self.lr * error</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 3.2 — FEEDFORWARD NETWORKS
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 3.2</span>
    <h2 class="chapter-title">Feedforward Networks</h2>
    <span class="chapter-subtitle">Multi-Layer Perceptrons, Activation Functions &amp; Universal Approximation</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Give me a non-linearity, and I will bend space itself."</p>
    <p class="attribution">— Deep Learning Folklore</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>A Multi-Layer Perceptron (MLP) stacks affine transformations interleaved with non-linear activation functions:
    $$\mathbf{z}^{[l]} = W^{[l]} \mathbf{a}^{[l-1]} + \mathbf{b}^{[l]}$$
    $$\mathbf{a}^{[l]} = \sigma(\mathbf{z}^{[l]})$$
    Without non-linear activations $\sigma(\cdot)$, any network of arbitrary depth collapses into a single trivial linear transformation: $W_3(W_2(W_1 \mathbf{x})) = (W_3 W_2 W_1)\mathbf{x} = W_{\text{eff}}\mathbf{x}$.</p>

    <h3>1. Modern Activation Functions</h3>
    <ul>
      <li><strong>ReLU (Rectified Linear Unit):</strong> $\text{ReLU}(z) = \max(0, z)$. Fast, non-saturating for $z > 0$, but suffers from the "Dying ReLU" problem when gradients permanently vanish for negative inputs.</li>
      <li><strong>GELU (Gaussian Error Linear Unit):</strong> $\text{GELU}(z) = z \cdot \Phi(z) \approx 0.5z(1 + \tanh(\sqrt{2/\pi}(z + 0.044715z^3)))$. Smooth, probabilistic gating; default in BERT, GPT-3, and ViT.</li>
      <li><strong>SwiGLU (Swish Gated Linear Unit):</strong> $\text{SwiGLU}(x) = (xW \cdot \text{Swish}(xV))W_2$. State-of-the-art activation used across LLaMA-2, LLaMA-3, and PaLM.</li>
    </ul>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 3.2 — Multi-Layer Perceptron Forward Pass from Scratch</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part3_neural_networks/ch32_feedforward_mlp/mlp_from_scratch.py" target="_blank">🔗 View in GitHub: part3_neural_networks/ch32_feedforward_mlp/mlp_from_scratch.py</a></p>
<pre><code>import numpy as np

class TwoLayerMLP:
    def __init__(self, in_d=2, h_d=4, out_d=1):
        self.W1 = np.random.randn(in_d, h_d) * np.sqrt(2.0 / in_d)
        self.b1 = np.zeros((1, h_d))
        self.W2 = np.random.randn(h_d, out_d) * np.sqrt(2.0 / h_d)
        self.b2 = np.zeros((1, out_d))

    def forward(self, X):
        self.A1 = np.maximum(0, X @ self.W1 + self.b1)
        return 1.0 / (1.0 + np.exp(-(self.A1 @ self.W2 + self.b2)))</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 3.3 — BACKPROPAGATION
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 3.3</span>
    <h2 class="chapter-title">Backpropagation</h2>
    <span class="chapter-subtitle">Computational Graphs &amp; Vector-Jacobian Products</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Nature does not make leaps, but algorithms do."</p>
    <p class="attribution">— Gottfried Wilhelm Leibniz</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Backpropagation is reverse-mode automatic differentiation applied to neural network computational graphs. It computes the exact gradient of the scalar loss $\mathcal{L}$ with respect to every weight tensor $W^{[l]}$ and bias vector $\mathbf{b}^{[l]}$ in a single backward sweep.</p>

    <h3>1. The Matrix Calculus Derivation</h3>
    <p>Let the error vector at layer $l$ be defined as $\boldsymbol{\delta}^{[l]} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{[l]}}$. By the chain rule:
    $$\boldsymbol{\delta}^{[l]} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{[l+1]}} \cdot \frac{\partial \mathbf{z}^{[l+1]}}{\partial \mathbf{a}^{[l]}} \cdot \frac{\partial \mathbf{a}^{[l]}}{\partial \mathbf{z}^{[l]}} = \left( (W^{[l+1]})^T \boldsymbol{\delta}^{[l+1]} \right) \odot \sigma'(\mathbf{z}^{[l]})$$
    The weight and bias gradients for a batch of $m$ samples are:
    $$\frac{\partial \mathcal{L}}{\partial W^{[l]}} = \frac{1}{m} (\mathbf{a}^{[l-1]})^T \boldsymbol{\delta}^{[l]}, \quad \frac{\partial \mathcal{L}}{\partial \mathbf{b}^{[l]}} = \frac{1}{m} \sum_{i=1}^m \boldsymbol{\delta}_i^{[l]}$$</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 3.3 — Analytical Backprop for Arbitrary Depth MLP</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part3_neural_networks/ch33_backpropagation/computational_graph_backprop.py" target="_blank">🔗 View in GitHub: part3_neural_networks/ch33_backpropagation/computational_graph_backprop.py</a></p>
<pre><code># Vectorized Backward Step in NumPy
dZ2 = A2 - y
dW2 = (1 / m) * (A1.T @ dZ2)
db2 = (1 / m) * np.sum(dZ2, axis=0, keepdims=True)

dA1 = dZ2 @ W2.T
dZ1 = dA1 * (1 - A1**2)  # tanh derivative
dW1 = (1 / m) * (X.T @ dZ1)
db1 = (1 / m) * np.sum(dZ1, axis=0, keepdims=True)</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 3.4 — OPTIMIZATION
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 3.4</span>
    <h2 class="chapter-title">Optimization Algorithms</h2>
    <span class="chapter-subtitle">SGD, Momentum, RMSprop, Adam &amp; AdamW Decoupled Weight Decay</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Speed is good, but direction is everything."</p>
    <p class="attribution">— Engineering Maxim</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Navigating the ravines, ill-conditioned curvature, and saddle points of non-convex neural network loss surfaces requires sophisticated adaptive optimizers.</p>

    <h3>1. AdamW: Why Decoupled Weight Decay Matters</h3>
    <p>Standard Adam couples weight decay with gradient scaling: $\mathbf{g}_t = \nabla \mathcal{L} + \lambda \boldsymbol{\theta}_t$. Because $\mathbf{g}_t$ is divided by $\sqrt{\mathbf{v}_t}$, weights with large historical gradients experience less regularization! <strong>AdamW</strong> (Loshchilov & Hutter, 2017) decouples weight decay, applying it directly to parameters outside the gradient accumulator:
    $$\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \alpha \lambda \boldsymbol{\theta}_t - \frac{\alpha}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \hat{\mathbf{m}}_t$$</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 3.4 — AdamW Optimizer Implementation</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part3_neural_networks/ch34_optimization_algorithms/optimizers_comparison.py" target="_blank">🔗 View in GitHub: part3_neural_networks/ch34_optimization_algorithms/optimizers_comparison.py</a></p>
<pre><code>class AdamW:
    def __init__(self, params, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8, wd=0.01):
        self.params, self.lr, self.b1, self.b2, self.eps, self.wd = params, lr, b1, b2, eps, wd
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, grads):
        self.t += 1
        for i, (p, g) in enumerate(zip(self.params, grads)):
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * (g**2)
            m_hat = self.m[i] / (1 - self.b1**self.t)
            v_hat = self.v[i] / (1 - self.b2**self.t)
            # Decoupled decay + update
            p -= self.lr * self.wd * p
            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 3.5 — REGULARIZATION
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 3.5</span>
    <h2 class="chapter-title">Regularization</h2>
    <span class="chapter-subtitle">Dropout, Batch Normalization &amp; Layer Normalization</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Constraints liberate."</p>
    <p class="attribution">— Architectural Principle</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Deep neural networks possess millions of free parameters, easily capable of brute-force memorizing random training noise. Regularization constrains the model hypothesis space to ensure robust out-of-distribution generalization.</p>

    <h3>1. Batch Normalization vs Layer Normalization</h3>
    <ul>
      <li><strong>Batch Normalization (Ioffe & Szegedy, 2015):</strong> Normalizes across the <em>batch dimension</em>: $\mu_B = \frac{1}{B}\sum_{i=1}^B x_{i, c, h, w}$. Requires large batch sizes; breaks on small batches or variable-length sequences.</li>
      <li><strong>Layer Normalization (Ba, Kiros, Hinton, 2016):</strong> Normalizes across the <em>feature channel dimension</em> independently for each individual sample: $\mu_L = \frac{1}{D}\sum_{j=1}^D x_{j}$. Essential for Transformers, RNNs, and online real-time inference.</li>
    </ul>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 3.5 — Inverted Dropout & LayerNorm from Scratch</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part3_neural_networks/ch35_regularization/dropout_and_batchnorm.py" target="_blank">🔗 View in GitHub: part3_neural_networks/ch35_regularization/dropout_and_batchnorm.py</a></p>
<pre><code>import numpy as np

class InvertedDropout:
    def __init__(self, p=0.5):
        self.p = p

    def forward(self, X, training=True):
        if not training or self.p == 0: return X
        keep_prob = 1.0 - self.p
        mask = (np.random.rand(*X.shape) < keep_prob) / keep_prob
        return X * mask</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     CHAPTER 3.6 — TRAINING IN PRACTICE
     ====================================================================== -->
<div class="chapter">
  <div class="chapter-header">
    <span class="chapter-number">Chapter 3.6</span>
    <h2 class="chapter-title">Training in Practice</h2>
    <span class="chapter-subtitle">PyTorch Production Loops, Mixed Precision (AMP) &amp; Checkpointing</span>
    <span class="chapter-ornament">✦</span>
  </div>

  <div class="epigraph">
    <p>"Theory is when you know everything but nothing works. Practice is when everything works but nobody knows why."</p>
    <p class="attribution">— Anonymous</p>
  </div>

  <div class="chapter-body">
    <span class="level-badge level-foundation">Foundation</span>

    <p>Moving from a toy Jupyter notebook to production model training requires disciplined engineering: Automatic Mixed Precision (FP16/BF16) to double throughput, gradient clipping to eliminate exploding gradients, gradient accumulation to simulate massive batch sizes, and atomic checkpointing to survive spot instance preemption.</p>

    <div class="code-lab">
      <div class="code-lab-header">Code Lab 3.6 — Production PyTorch Training Pipeline</div>
      <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part3_neural_networks/ch36_training_in_practice/production_training_loop.py" target="_blank">🔗 View in GitHub: part3_neural_networks/ch36_training_in_practice/production_training_loop.py</a></p>
<pre><code>import torch
import torch.nn as nn

# Production PyTorch training step with Gradient Clipping
optimizer.zero_grad()
preds = model(batch_x)
loss = criterion(preds, batch_y)
loss.backward()

# Production safeguard against exploding gradient spikes
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()</code></pre>
    </div>
  </div>
</div>

<!-- ======================================================================
     PROJECT 3 — HANDWRITTEN DIGIT CLASSIFIER FROM SCRATCH
     ====================================================================== -->
<div class="project-section">
  <div class="project-header">
    <span class="project-tag">Hands-On Project 3</span>
    <h3 class="project-title">Handwritten Digit Classifier from Scratch (MNIST)</h3>
    <p class="project-desc">Build and train a 3-layer deep neural network on MNIST using exclusively pure Python and NumPy — no PyTorch, no TensorFlow, no automatic differentiation.</p>
    <p><a class="repo-link-badge" href="https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions/blob/main/part3_neural_networks/ch33_backpropagation/computational_graph_backprop.py" target="_blank">🔗 Full Project Code: part3_neural_networks/ch33_backpropagation/computational_graph_backprop.py</a></p>
  </div>
  <div class="project-body">
    <p><strong>Architecture Overview:</strong> 784 input neurons $\to$ 128 hidden neurons (ReLU) $\to$ 64 hidden neurons (ReLU) $\to$ 10 output neurons (Softmax). You will code the forward pass, categorical cross-entropy loss, analytical backpropagation, and mini-batch gradient descent, achieving >97.5% test accuracy from raw math.</p>
  </div>
</div>
"""
