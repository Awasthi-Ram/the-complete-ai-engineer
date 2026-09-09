import os

part0_header = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 0 — FOUNDATIONS BEFORE FOUNDATIONS
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 0</div>
  <div class="part-title">Foundations Before Foundations</div>
  <div class="part-subtitle">The AI Engineer Operating System, Python from A to Z, C-BLAS Vectorization &amp; Large-Scale Data Systems</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>
"""

chapters = [
    'book_builder/ch01_how_to_learn.html',
    'book_builder/ch02_python_a_to_z.html',
    'book_builder/ch03_ai_toolchain.html',
    'book_builder/ch04_large_scale_data.html'
]

contents = [part0_header.strip()]
for ch in chapters:
    with open(ch, 'r', encoding='utf-8') as f:
        contents.append(f.read().strip())

full_part0 = "\n\n".join(contents) + "\n"

with open('book_builder/part0.html', 'w', encoding='utf-8') as f:
    f.write(full_part0)

size_bytes = os.path.getsize('book_builder/part0.html')
print(f"Assembled part0.html successfully! ({size_bytes:,} bytes)")
