import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 6 — MLOPS, OBSERVABILITY & PRODUCTION MODEL DEPLOYMENT
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 6</div>
  <div class="part-title">MLOps &amp; Production Engineering</div>
  <div class="part-subtitle">Experiment Registries, Dual Feature Stores, Rootless Docker, Triton High-Throughput Serving &amp; Drift Sentinels</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

"""

CHAPTERS = [
    "book_builder/ch61_experiment_tracking.html",
    "book_builder/ch62_feature_stores.html",
    "book_builder/ch63_containerization_docker.html",
    "book_builder/ch64_triton_serving.html",
    "book_builder/ch65_drift_observability.html"
]

output_path = "book_builder/part6.html"

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

print(f"\nPart 6 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 6: {total_problems}")
