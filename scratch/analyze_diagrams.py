import glob
import os
import re

files = sorted(glob.glob('book_builder/ch*.html'))
print(f"Total chapter files: {len(files)}")

with_diagrams = []
without_diagrams = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    title_m = re.search(r'<h[12][^>]*>(.*?)</h[12]>', content)
    title = title_m.group(1).strip() if title_m else os.path.basename(f)
    title = re.sub(r'<[^>]+>', '', title)
    
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content)
    if imgs:
        with_diagrams.append((os.path.basename(f), title, imgs))
    else:
        without_diagrams.append((os.path.basename(f), title))

print(f"\n--- Chapters WITH diagrams ({len(with_diagrams)}): ---")
for fname, title, imgs in with_diagrams:
    print(f"  [IMG] {fname}: {title} -> {imgs}")

print(f"\n--- Chapters WITHOUT diagrams ({len(without_diagrams)}): ---")
for fname, title in without_diagrams:
    print(f"  [NO IMG] {fname}: {title}")
