import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 4 — DEEP LEARNING ARCHITECTURES: VISION, AUDIO & GENERATION
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 4</div>
  <div class="part-title">Deep Learning Architectures</div>
  <div class="part-subtitle">Convolutional Networks, ResNets, Medical U-Net, VAEs, Diffusion Models, ViTs, Whisper Audio &amp; Dense NLP Embeddings</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

"""

CHAPTERS = [
    "book_builder/ch41_cnns_resnets.html",
    "book_builder/ch42_segmentation_unet.html",
    "book_builder/ch43_vaes_gans.html",
    "book_builder/ch44_diffusion_models.html",
    "book_builder/ch45_vit_mae.html",
    "book_builder/ch46_audio_whisper.html",
    "book_builder/ch47_nlp_embeddings.html"
]

output_path = "book_builder/part4.html"

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

print(f"\nPart 4 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 4: {total_problems}")
