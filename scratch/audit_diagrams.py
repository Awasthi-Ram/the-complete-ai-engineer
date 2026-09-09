import re

with open('book.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all chapters
chapter_matches = list(re.finditer(r'<div class="chapter"[^>]*id="([^"]+)"[^>]*>.*?<h2 class="chapter-title">([^<]+)</h2>', text, re.DOTALL))
print(f"Total chapters identified: {len(chapter_matches)}")

has_diagrams = []
needs_diagrams = []

for i, match in enumerate(chapter_matches):
    cid = match.group(1)
    ctitle = match.group(2).strip()
    start_pos = match.start()
    end_pos = chapter_matches[i+1].start() if i + 1 < len(chapter_matches) else len(text)
    
    chapter_content = text[start_pos:end_pos]
    
    img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', chapter_content)
    svg_tags = len(re.findall(r'<svg\b', chapter_content))
    
    if img_tags or svg_tags:
        has_diagrams.append((cid, ctitle, img_tags, svg_tags))
    else:
        needs_diagrams.append((cid, ctitle))

print(f"\n--- Chapters WITH Diagrams ({len(has_diagrams)}) ---")
for cid, ctitle, imgs, svgs in has_diagrams:
    print(f"  [YES] {cid}: {ctitle} (imgs={imgs}, svgs={svgs})")

print(f"\n--- Chapters NEEDING Diagrams ({len(needs_diagrams)}) ---")
for cid, ctitle in needs_diagrams:
    print(f"  [NO ] {cid}: {ctitle}")
