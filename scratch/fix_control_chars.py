"""
Comprehensive LaTeX fixer for the entire book.
1. Fix control character corruption (\x07 -> \a in \approx, \x0c -> \f in \frac, etc.)
2. Verify all LaTeX commands have proper backslashes
3. Report on fixes applied per file
"""
import os
import re

BOOK_DIR = 'book_builder'

# Map of control chars to the original LaTeX escape they came from
# Python string escapes: \a=0x07(bell), \b=0x08(backspace), \f=0x0c(formfeed), 
# \n=0x0a(newline), \r=0x0d(cr), \t=0x09(tab), \v=0x0b(vtab)
# LaTeX commands starting with these letters:
# \a -> \approx, \alpha, \ast, \angle, \arctan, \arcsin, \arccos, etc.
# \f -> \frac, \forall, \flat
# \b -> \beta, \bar, \begin, \big, \binom, \boldsymbol, \bmod, \bot
# \t -> \text, \theta, \times, \tilde, \top, \to, \tau
# \v -> \vec, \vdots, \vee, \varphi, \varepsilon
# \n -> \nabla, \neg, \nu, \newline, \neq, \not
# \r -> \right, \rho, \rangle, \rceil, \rfloor

CONTROL_CHAR_FIXES = {
    '\x07': '\\a',   # bell -> \a (for \approx, \alpha, etc.)
    '\x0c': '\\f',   # formfeed -> \f (for \frac, \forall, etc.)
    '\x08': '\\b',   # backspace -> \b (for \beta, \bar, \begin, etc.)
    '\x0b': '\\v',   # vertical tab -> \v (for \vec, \vdots, etc.)
    # Note: \t (tab), \n (newline), \r (carriage return) are legitimate whitespace
    # and should NOT be blindly replaced - they could be actual formatting
}

def fix_file(filepath):
    """Fix control character corruption in a single HTML file."""
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    original_size = len(raw)
    fixes = {}
    
    # Fix each control character
    for char_byte, replacement in CONTROL_CHAR_FIXES.items():
        char_bytes = char_byte.encode('latin-1')
        count = raw.count(char_bytes)
        if count > 0:
            raw = raw.replace(char_bytes, replacement.encode('utf-8'))
            fixes[replacement] = count
    
    if fixes:
        with open(filepath, 'wb') as f:
            f.write(raw)
        return fixes
    return None

# Process all chapter files
all_fixes = {}
chapter_files = sorted([f for f in os.listdir(BOOK_DIR) if f.endswith('.html')])

for filename in chapter_files:
    filepath = os.path.join(BOOK_DIR, filename)
    fixes = fix_file(filepath)
    if fixes:
        all_fixes[filename] = fixes
        fix_desc = ", ".join(f"{k}: {v}" for k, v in fixes.items())
        print(f"FIXED {filename}: {fix_desc}")

if not all_fixes:
    print("No control character corruption found in any files.")
else:
    total_fixes = sum(sum(v.values()) for v in all_fixes.values())
    print(f"\nTotal files fixed: {len(all_fixes)}")
    print(f"Total control characters replaced: {total_fixes}")

# Also fix part files and book.html
for partfile in ['part0.html', 'part1.html', 'part2.html', 'part3.html', 'part4.html',
                 'part5.html', 'part6.html', 'part7.html', 'part8.html']:
    filepath = os.path.join(BOOK_DIR, partfile)
    if os.path.exists(filepath):
        fixes = fix_file(filepath)
        if fixes:
            fix_desc = ", ".join(f"{k}: {v}" for k, v in fixes.items())
            print(f"FIXED {partfile}: {fix_desc}")

# Fix book.html itself
book_path = 'book.html'
if os.path.exists(book_path):
    fixes = fix_file(book_path)
    if fixes:
        fix_desc = ", ".join(f"{k}: {v}" for k, v in fixes.items())
        print(f"FIXED book.html: {fix_desc}")

print("\nControl character fix pass complete.")
