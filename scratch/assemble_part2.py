import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 2 — CLASSICAL MACHINE LEARNING
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 2</div>
  <div class="part-title">Classical Machine Learning</div>
  <div class="part-subtitle">Regression, Classification, Ensembles, XGBoost, SVMs, Unsupervised Learning, Evaluation &amp; Reinforcement Learning</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

"""

CHAPTERS = [
    "book_builder/ch21_ml_paradigm.html",
    "book_builder/ch22_linear_regression.html",
    "book_builder/ch23_logistic_regression.html",
    "book_builder/ch24_decision_trees.html",
    "book_builder/ch25_random_forests.html",
    "book_builder/ch25b_gradient_boosting.html",
    "book_builder/ch26_svm.html",
    "book_builder/ch27_unsupervised_kmeans_pca.html",
    "book_builder/ch28_feature_engineering.html",
    "book_builder/ch29_model_evaluation.html",
    "book_builder/ch210_reinforcement_learning.html"
]

output_path = "book_builder/part2.html"

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

print(f"\nPart 2 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 2: {total_problems}")
