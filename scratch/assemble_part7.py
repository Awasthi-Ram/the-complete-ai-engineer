import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 7 — AI SYSTEM DESIGN & ARCHITECTURE AT SCALE
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 7</div>
  <div class="part-title">AI System Design at Scale</div>
  <div class="part-subtitle">Billion-Item Recommendation Systems, Distributed Vector Search, HNSW, IVF-PQ &amp; Edge AI Quantization</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

"""

CHAPTERS = [
    "book_builder/ch71_recsys_twotower.html",
    "book_builder/ch72_vector_search_scale.html",
    "book_builder/ch73_edge_ai_quantization.html"
]

output_path = "book_builder/part7.html"

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

print(f"\nPart 7 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 7: {total_problems}")
