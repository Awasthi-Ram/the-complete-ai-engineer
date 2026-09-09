import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 3 — NEURAL NETWORKS FROM SCRATCH
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 3</div>
  <div class="part-title">Neural Networks from Scratch</div>
  <div class="part-subtitle">The Perceptron, Universal Approximation, Analytical Backpropagation, Deep Optimizers, Normalization, Production PyTorch, JAX &amp; Recurrence</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

"""

CHAPTERS = [
    "book_builder/ch31_perceptron_xor.html",
    "book_builder/ch32_mlp_activations.html",
    "book_builder/ch33_backprop_scratch.html",
    "book_builder/ch34_deep_optimization.html",
    "book_builder/ch35_normalization_regularization.html",
    "book_builder/ch36_pytorch_production.html",
    "book_builder/ch37_jax_functional_dl.html",
    "book_builder/ch38_rnns_lstms.html"
]

output_path = "book_builder/part3.html"

contents = [HEADER]
total_problems = 0

for ch in CHAPTERS:
    with open(ch, "r", encoding="utf-8") as f:
        text = f.read()
    problems = re.findall(r'<div class="problem">', text)
    total_problems += len(problems)
    contents.append(text)
    print(f"Loaded {ch}: {len(text)} bytes, {len(problems)} problems")

combined = "\n\n".join(contents)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(combined)

print(f"\nPart 3 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 3: {total_problems}")
