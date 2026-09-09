# scratch/validate_book.py
import re, os, ast, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('book.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Total HTML length: {len(html):,} characters")

# 1. Image reference verification
img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f"\n--- Checking {len(img_srcs)} Image References ---")
missing_images = []
for src in set(img_srcs):
    # Check in root and in book_builder
    found = os.path.exists(src) or os.path.exists(os.path.join('book_builder', src))
    if not found:
        missing_images.append(src)
    else:
        print(f"  [OK] Image exists: {src}")

if missing_images:
    print(f"  [ERROR] Missing images: {missing_images}")
else:
    print("  [SUCCESS] All images verified!")

# 2. Check Python code blocks with ast.parse
print("\n--- Checking Python Code Blocks ---")
code_blocks = re.findall(r'<code class="language-python">([\s\S]*?)</code>', html)
print(f"Found {len(code_blocks)} python code blocks.")

syntax_errors = []
for i, block in enumerate(code_blocks):
    # Unescape HTML entities if any
    cleaned = block.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
    try:
        ast.parse(cleaned)
    except SyntaxError as e:
        syntax_errors.append((i, str(e), cleaned[:80]))

if syntax_errors:
    print(f"  [WARNING] {len(syntax_errors)} Python syntax issues in code blocks:")
    for idx, err, snippet in syntax_errors:
        print(f"    Block #{idx}: {err} | Snippet: {snippet.strip()}...")
else:
    print("  [SUCCESS] All python code blocks passed ast.parse!")

# 3. MathJax delimiter parity check
print("\n--- Checking MathJax Delimiters ---")
double_dollars = html.count('$$')
print(f"  '$$' count: {double_dollars} ({'EVEN - OK' if double_dollars % 2 == 0 else 'ODD - WARNING!'})")

# 4. Check chapter count & list
chapters = re.findall(r'<span class="chapter-number">([^<]+)</span>', html)
print(f"\n--- Verified Chapters in Book ({len(chapters)} total) ---")
for ch in chapters:
    print(f"  - {ch}")
