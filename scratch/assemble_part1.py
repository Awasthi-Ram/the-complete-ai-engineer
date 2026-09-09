import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 1 — THE MATHEMATICS OF AI
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 1</div>
  <div class="part-title">The Mathematics of AI</div>
  <div class="part-subtitle">Linear Algebra, SVD, Multivariable Autograd, Bayesian Probability &amp; Convex Duality</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

"""

CHAPTERS = [
    "book_builder/ch11_linear_algebra.html",
    "book_builder/ch12_calculus_autograd.html",
    "book_builder/ch13_probability_bayes.html",
    "book_builder/ch14_information_theory.html",
    "book_builder/ch15_convex_optimization.html"
]

output_path = "book_builder/part1.html"

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

print(f"\nPart 1 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 1: {total_problems}")
