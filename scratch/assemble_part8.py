import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 8 — FRONTIER AI & FUTURE HORIZONS
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 8</div>
  <div class="part-title">Frontier AI &amp; Future Horizons</div>
  <div class="part-subtitle">The Model Context Protocol (MCP), Test-Time Compute &amp; Reasoning Models, Thermodynamic Limits &amp; Photonic Compute</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>
"""

CHAPTERS = [
    "book_builder/ch81_mcp_standard.html",
    "book_builder/ch82_test_time_compute.html",
    "book_builder/ch83_energy_hardware_limits.html"
]

output_path = "book_builder/part8.html"

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

print(f"\nPart 8 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 8: {total_problems}")
