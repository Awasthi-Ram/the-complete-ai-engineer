import re

with open('book.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

sharma_lines = []
for i, line in enumerate(lines):
    if re.search(r'sharma', line, re.IGNORECASE):
        sharma_lines.append((i+1, line.strip()))

print(f"Total lines with 'Sharma' in book.html: {len(sharma_lines)}")
for lno, text in sharma_lines:
    print(f"  Line {lno}: {text}")
