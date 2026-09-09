"""
Deep diagnostic: Check every LaTeX command in every chapter file.
Goal: Find all files that have broken LaTeX (single backslash interpreted as escape)
vs files with correct LaTeX (literal single backslash in HTML for MathJax).
"""
import re, os

chapter_files = sorted([f for f in os.listdir('book_builder') if f.startswith('ch') and f.endswith('.html')])

# For MathJax in HTML, we need single backslash: \frac, \text, \left, etc.
# The problem the user reports is that \frac shows as "rac{" -- meaning the backslash
# is being consumed/lost somewhere.

# Let's open a file in the browser and check what MathJax actually sees.
# But first, let's verify the raw file content character by character.

print("=== Checking ch01_how_to_learn.html (has bell and formfeed chars) ===")
with open('book_builder/ch01_how_to_learn.html', 'rb') as f:
    raw = f.read()

# Find bell character (0x07) contexts
bell_pos = []
idx = 0
while True:
    pos = raw.find(b'\x07', idx)
    if pos == -1:
        break
    bell_pos.append(pos)
    idx = pos + 1

print(f"Bell chars: {len(bell_pos)}")
for pos in bell_pos[:5]:
    ctx = raw[max(0,pos-15):pos+25]
    print(f"  pos {pos}: {repr(ctx)}")

# Find formfeed (0x0c) contexts  
ff_pos = []
idx = 0
while True:
    pos = raw.find(b'\x0c', idx)
    if pos == -1:
        break
    ff_pos.append(pos)
    idx = pos + 1

print(f"\nFormfeed chars: {len(ff_pos)}")
for pos in ff_pos[:5]:
    ctx = raw[max(0,pos-15):pos+25]
    print(f"  pos {pos}: {repr(ctx)}")

# Now check: is the problem that Python's write_to_file interpreted \a as bell and \f as formfeed?
# \a = 0x07 (bell), \f = 0x0c (formfeed), \t = 0x09 (tab), \n = 0x0a (newline)
# In LaTeX: \approx, \alpha, \frac, \forall, \text
# So \a in \approx -> bell+pprox, \f in \frac -> formfeed+rac
# BUT the byte check above shows ch11 has correct \frac (0x5c 66 = \f as literal chars)
# So the issue is only in ch01 and ch02 which have bell and formfeed chars!

print("\n=== Summary of files with control character corruption ===")
for ch in chapter_files:
    path = os.path.join('book_builder', ch)
    with open(path, 'rb') as f:
        raw = f.read()
    
    bell = raw.count(b'\x07')
    ff = raw.count(b'\x0c')
    tab = raw.count(b'\x09')
    
    if bell > 0 or ff > 0:
        print(f"  {ch}: bell(\\a)={bell}, formfeed(\\f)={ff}, tabs={tab}")

# So the real question: WHY does the user see "rac{" in the BROWSER?
# MathJax expects \frac in HTML. Let's check if the HTML has the right encoding.
print("\n=== Checking HTML charset declaration ===")
with open('book.html', 'r', encoding='utf-8') as f:
    head = f.read(2000)
print(head[:500])
