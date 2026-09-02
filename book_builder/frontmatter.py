# book_builder/frontmatter.py

FRONTMATTER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Complete AI Engineer — From Absolute Beginner to Production-Ready Engineer</title>
  <link rel="stylesheet" href="styles.css">
  <style>
    /* Cover-specific styles (full-bleed, no margins) */
    .cover-page { page-break-after: always; margin: 0; padding: 0; width: 6in; height: 9in; overflow: hidden; }
    .cover-page img { width: 100%; height: 100%; object-fit: contain; display: block; }
    .back-cover-page { break-before: right; margin: 0; padding: 0; width: 6in; height: 9in; overflow: hidden; background: linear-gradient(135deg, #050a15, #0a1128, #0d1b2a, #050a15); }
    .back-cover-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; padding: 1in 0.8in; display: flex; flex-direction: column; justify-content: center; color: white; }
    .repo-link-badge { display: inline-block; background: #0d1b2a; color: #5fa8d3; padding: 4px 10px; border-radius: 4px; font-family: monospace; font-size: 0.85em; text-decoration: none; margin: 6px 0; border: 1px solid #1b4965; }
    .repo-link-badge:hover { background: #1b4965; color: #ffffff; }
    .real-world-box { background: #f0f7ff; border-left: 4px solid #0077b6; padding: 12px 16px; margin: 1.2em 0; border-radius: 0 4px 4px 0; }
    .real-world-box h4 { margin: 0 0 6px 0; color: #0077b6; font-size: 1.05em; }
    .qr-container { text-align: center; margin: 2em 0; padding: 20px; background: #ffffff; border: 2px solid #0d1b2a; border-radius: 8px; }
    .qr-container img { width: 220px; height: 220px; display: block; margin: 0 auto 12px auto; }
  </style>
</head>
<body>

<!-- ====================================================================
     FRONT COVER
     ==================================================================== -->
<div class="cover-page"><img src="front_cover.png" alt="The Complete AI Engineer — Book Cover"></div>

<!-- ====================================================================
     TITLE PAGE
     ==================================================================== -->
<div class="title-page">
  <div class="book-title">The Complete<br>AI Engineer</div>
  <div class="book-subtitle">From Absolute Beginner to Production-Ready Engineer</div>
  <div class="ornament">✦ ✦ ✦</div>
  <div class="author-name">Ram Awasthi</div>
</div>

<!-- ====================================================================
     COPYRIGHT PAGE
     ==================================================================== -->
<div class="copyright-page">
  <p><strong>The Complete AI Engineer: From Absolute Beginner to Production-Ready Engineer</strong></p>
  <p>Copyright © 2026 Ram Awasthi</p>
  <p>All rights reserved. No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other non-commercial uses permitted by copyright law.</p>
  <p>First Edition, 2026</p>
  <p>ISBN: To be assigned</p>
  <p style="margin-top: 1em;">Every effort has been made to ensure the accuracy of the information presented in this book. However, the information contained in this book is sold without warranty, either express or implied. The author and publisher will not be held liable for any damages caused or alleged to be caused directly or indirectly by this book.</p>
  <p><strong>Companion Code Repository:</strong><br>
  All runnable code solutions, Jupyter notebooks, unit tests, and production project assets are hosted open-source at:<br>
  <code>https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions</code></p>
  <p style="margin-top: 1em;">Typeset in Merriweather, Playfair Display, and Source Code Pro.</p>
</div>

<!-- ====================================================================
     A MESSAGE FROM THE BOOK
     ==================================================================== -->
<div class="message-page">
  <h2>A Message From the Book</h2>
  
  <h3>Who This Book Is For</h3>
  <p>This book is for anyone who wants to become an AI engineer. Not someone who merely invokes API calls or memorizes high-level library syntax — but an engineer who deeply understands how models learn, why loss landscapes curve, how computational graphs propagate gradients, and how to scale and deploy robust intelligence to millions of users. You do not need a PhD. You do not need to have studied at MIT. You need dedication, a willingness to work through the mathematics, and this book.</p>

  <h3>The Core Philosophy: You Don't Even Need a Computer</h3>
  <p>A core design tenet of this textbook is complete self-containment. Modeled after the beloved R.D. Sharma mathematical textbooks, <em>every single derivation, equation step, and worked problem is solved in full directly on the page</em>. You can read this book on a train, on an airplane, or in a library without opening a laptop. Every step of algebra, every matrix dimension check, and every algorithm trace is printed before your eyes.</p>
  <p>For those who wish to execute, benchmark, and deploy the code, every problem and lab is accompanied by a direct link to the official open-source GitHub repository: <code>https://github.com/Awasthi-Ram/the-complete-ai-engineer-solutions</code>.</p>

  <h3>Real-World Problem Mapping & FAANG Interview Rigor</h3>
  <p>Every concept is introduced through two rigorous lenses:
  <ol>
    <li><strong>Real-World Industry Problem Mapping:</strong> What production disaster, latency bottleneck, or product challenge does this technique solve in industry?</li>
    <li><strong>Top-Tier FAANG AI Interview Problems:</strong> Exact questions asked at Google, Meta, Amazon, OpenAI, DeepMind, Apple, Netflix, and Microsoft — complete with difficulty badges, company tags, and step-by-step solutions.</li>
  </ol></p>
</div>

<!-- ====================================================================
     TABLE OF CONTENTS
     ==================================================================== -->
<div class="toc">
  <h2>Contents</h2>

  <!-- Part 0 -->
  <div class="toc-part">Part 0 — Foundations Before Foundations</div>
  <div class="toc-entry"><span class="toc-chapter-num">0.1</span><span class="toc-chapter-title">How to Learn AI — Setting Up Your Mind and Machine</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">0.2</span><span class="toc-chapter-title">Python Foundations — Object-Oriented AI Programming & Memory</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">0.3</span><span class="toc-chapter-title">The AI Toolchain — NumPy Vectorization, Pandas & PyTorch Tensors</span></div>
  <div class="toc-project">Project: Build Your AI Development Dashboard</div>

  <!-- Part 1 -->
  <div class="toc-part">Part 1 — The Mathematics of AI</div>
  <div class="toc-entry"><span class="toc-chapter-num">1.1</span><span class="toc-chapter-title">Linear Algebra — The Language Machines Think In</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">1.2</span><span class="toc-chapter-title">Calculus — The Engine of Learning & Automatic Differentiation</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">1.3</span><span class="toc-chapter-title">Probability &amp; Statistics — Thinking in Uncertainty</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">1.4</span><span class="toc-chapter-title">Information Theory — Entropy, Cross-Entropy & KL Divergence</span></div>
  <div class="toc-project">Project: Image Transformation Engine & SVD Compression</div>

  <!-- Part 2 -->
  <div class="toc-part">Part 2 — Classical Machine Learning</div>
  <div class="toc-entry"><span class="toc-chapter-num">2.1</span><span class="toc-chapter-title">What Is Machine Learning? — The Paradigm Shift</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">2.2</span><span class="toc-chapter-title">Linear Regression — OLS Normal Equation & Gradient Descent</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">2.3</span><span class="toc-chapter-title">Logistic Regression — Sigmoid, Odds Ratios & Cross-Entropy</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">2.4</span><span class="toc-chapter-title">Decision Trees & Ensembles — CART, Gini Impurity & Random Forests</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">2.5</span><span class="toc-chapter-title">KNN &amp; SVMs — Margins, Slack Variables & Kernel Trick</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">2.6</span><span class="toc-chapter-title">Unsupervised Learning — K-Means++, Hierarchical & PCA</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">2.7</span><span class="toc-chapter-title">Feature Engineering — Outliers, Imputation & Leakage Prevention</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">2.8</span><span class="toc-chapter-title">Model Evaluation — Confusion Matrix, ROC-AUC & Calibration</span></div>
  <div class="toc-project">Project: House Price Predictor from Scratch</div>

  <!-- Part 3 -->
  <div class="toc-part">Part 3 — Neural Networks from Scratch</div>
  <div class="toc-entry"><span class="toc-chapter-num">3.1</span><span class="toc-chapter-title">The Neuron &amp; Perceptron — Where It All Began & XOR Limitation</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">3.2</span><span class="toc-chapter-title">Feedforward Networks — Layers of Intelligence & Universal Approximation</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">3.3</span><span class="toc-chapter-title">Backpropagation — Computational Graphs & Vector-Jacobian Products</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">3.4</span><span class="toc-chapter-title">Optimization — SGD, Momentum, RMSprop, Adam & AdamW</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">3.5</span><span class="toc-chapter-title">Regularization — Dropout, Batch Normalization & Layer Normalization</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">3.6</span><span class="toc-chapter-title">Training in Practice — PyTorch Loops, AMP FP16 & Checkpointing</span></div>
  <div class="toc-project">Project: Handwritten Digit Classifier from Scratch</div>

  <!-- Part 4 -->
  <div class="toc-part">Part 4 — Deep Learning Architectures</div>
  <div class="toc-entry"><span class="toc-chapter-num">4.1</span><span class="toc-chapter-title">CNNs — Convolutions, Strides, Receptive Fields & ResNet</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">4.2</span><span class="toc-chapter-title">RNNs &amp; LSTMs — Vanishing Gradients & The Constant Error Carousel</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">4.3</span><span class="toc-chapter-title">Attention &amp; Seq2Seq — Eliminating the Bottleneck Vector</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">4.4</span><span class="toc-chapter-title">Transformers — Multi-Head Self-Attention & Modern Decoder LLMs</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">4.5</span><span class="toc-chapter-title">Generative Models — VAEs, GANs & Denoising Diffusion (DDPM)</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">4.6</span><span class="toc-chapter-title">Audio &amp; Speech — STFT Spectrograms, Mel-Filterbanks & Whisper</span></div>
  <div class="toc-project">Project: Real-Time Image Classifier</div>

  <!-- Part 5 -->
  <div class="toc-part">Part 5 — Large Language Models (LLMs) & Agents</div>
  <div class="toc-entry"><span class="toc-chapter-num">5.1</span><span class="toc-chapter-title">Text to Numbers — NLP Foundations, Word2Vec & N-Grams</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">5.2</span><span class="toc-chapter-title">The LLM Revolution — BPE Tokenization, Scaling Laws & KV Cache</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">5.3</span><span class="toc-chapter-title">Prompt Engineering — In-Context Reasoning, CoT & Structured Outputs</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">5.4</span><span class="toc-chapter-title">Fine-Tuning LLMs — LoRA, QLoRA 4-bit, SFT & DPO</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">5.5</span><span class="toc-chapter-title">RAG — Chunking, Vector Databases, HNSW & Hybrid Search</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">5.6</span><span class="toc-chapter-title">AI Agents — The ReAct Paradigm, Tool Calling & Episodic Memory</span></div>
  <div class="toc-project">Project: Production RAG & Sentiment Analysis Engine</div>

  <!-- Part 6 -->
  <div class="toc-part">Part 6 — MLOps &amp; Production AI</div>
  <div class="toc-entry"><span class="toc-chapter-num">6.1</span><span class="toc-chapter-title">Experiment Tracking &amp; Versioning — The Science of ML</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">6.2</span><span class="toc-chapter-title">Model Serving &amp; Deployment — FastAPI, Triton & Dynamic Batching</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">6.3</span><span class="toc-chapter-title">Monitoring &amp; Drift Detection — Population Stability Index (PSI)</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">6.4</span><span class="toc-chapter-title">Data Pipelines &amp; Feature Stores — Online/Offline Sync & Point-in-Time Joins</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">6.5</span><span class="toc-chapter-title">Cloud ML Platforms — AWS SageMaker, GCP Vertex AI & Spot Clusters</span></div>
  <div class="toc-project">Project: End-to-End MLOps Pipeline with Docker & Monitoring</div>

  <!-- Part 7 -->
  <div class="toc-part">Part 7 — System Design for AI Engineers</div>
  <div class="toc-entry"><span class="toc-chapter-num">7.1</span><span class="toc-chapter-title">AI System Design Framework — 7-Step Blueprint & Capacity Sizing</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">7.2</span><span class="toc-chapter-title">Real-World System Designs — YouTube Recs, Search & Fraud Detection</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">7.3</span><span class="toc-chapter-title">Ethics, Fairness & Explainability — SHAP Values, LIME & Bias Auditing</span></div>
  <div class="toc-project">Project: Two-Stage Recommendation Engine Architecture</div>

  <!-- Part 8 -->
  <div class="toc-part">Part 8 — Advanced Topics &amp; The Frontier</div>
  <div class="toc-entry"><span class="toc-chapter-num">8.1</span><span class="toc-chapter-title">Multimodal AI — Vision Meets Language with Contrastive CLIP</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">8.2</span><span class="toc-chapter-title">Reinforcement Learning — Bellman Optimality, Q-Learning & RLHF</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">8.3</span><span class="toc-chapter-title">Model Optimization — INT8 Quantization, Pruning & Distillation</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">8.4</span><span class="toc-chapter-title">Your Career as an AI Engineer — Paper Reading & FAANG Interview Rubric</span></div>
  <div class="toc-project">Project: Multimodal CLIP Image Search & Captioning</div>

  <!-- Back matter -->
  <div class="toc-part">Appendices</div>
  <div class="toc-entry"><span class="toc-chapter-num">A</span><span class="toc-chapter-title">Mathematical Notation & Glossary</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">B</span><span class="toc-chapter-title">About the Author</span></div>
  <div class="toc-entry"><span class="toc-chapter-num">C</span><span class="toc-chapter-title">Official GitHub Solutions Repository & QR Code Access</span></div>
</div>
"""
