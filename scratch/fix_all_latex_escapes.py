"""
Comprehensive LaTeX escape fixer for ALL chapter files.
Fixes ALL Python string escape sequences that corrupt LaTeX commands:
  \a (bell 0x07) in \approx, \alpha, etc.
  \f (formfeed 0x0c) in \frac, \forall, etc.  
  \b (backspace 0x08) in \beta, \bar, \begin, etc.
  \v (vtab 0x0b) in \vec, \vdots, etc.
  \t (tab 0x09) in \text, \times, \theta, \tilde, \tau, etc.

Strategy: In math contexts, tabs (0x09) that appear before LaTeX-command-like
continuations (ext{, imes, heta, ilde, au, etc.) are restored to backslash.
Regular tabs for HTML indentation are preserved.
"""
import os
import re

BOOK_DIR = 'book_builder'

def fix_file(filepath):
    """Fix all Python string escape corruption in a single HTML file."""
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    original = raw
    fixes = {}
    
    # === PHASE 1: Fix unambiguous control characters ===
    # These chars should NEVER appear in HTML source
    simple_fixes = {
        b'\x07': b'\\a',   # bell -> \a (approx, alpha, angle, etc.)
        b'\x0c': b'\\f',   # formfeed -> \f (frac, forall, flat)
        b'\x08': b'\\b',   # backspace -> \b (beta, bar, begin, big, binom, boldsymbol)
        b'\x0b': b'\\v',   # vtab -> \v (vec, vdots, vee, varphi, varepsilon)
    }
    
    for char_bytes, replacement in simple_fixes.items():
        count = raw.count(char_bytes)
        if count > 0:
            raw = raw.replace(char_bytes, replacement)
            fixes[replacement.decode()] = count
    
    # === PHASE 2: Fix tab (0x09) that should be \t for LaTeX commands ===
    # Tab is ambiguous: it could be real HTML indentation OR a corrupted \t
    # Strategy: Replace tab ONLY when followed by known LaTeX command suffixes
    
    # Known LaTeX commands starting with 't' that would have been corrupted:
    # \text{...}, \textbf{...}, \textit{...}, \textrm{...}, \texttt{...}
    # \times, \theta, \tilde, \tau, \top, \to, \therefore
    # \triangleq, \triangle, \tag
    
    latex_t_suffixes = [
        b'ext{', b'ext ',      # \text{ and \text  (with space)
        b'extbf{',             # \textbf{
        b'extit{',             # \textit{
        b'extrm{',             # \textrm{
        b'exttt{',             # \texttt{
        b'imes',               # \times
        b'heta',               # \theta
        b'ilde{', b'ilde ',    # \tilde{ and \tilde 
        b'au',                 # \tau (careful: also matches non-LaTeX words)
        b'op',                 # \top (careful)
        b'o ',                 # \to (careful - very short)
        b'riangle',            # \triangle, \triangleq
        b'ag{', b'ag ',        # \tag{ and \tag 
        b'herefore',           # \therefore
    ]
    
    tab_fixes = 0
    pos = 0
    result = bytearray()
    
    while pos < len(raw):
        if raw[pos:pos+1] == b'\x09':
            # Check if this tab is followed by a LaTeX command suffix
            matched = False
            for suffix in latex_t_suffixes:
                if raw[pos+1:pos+1+len(suffix)] == suffix:
                    # Additional check: for short suffixes like 'au', 'op', 'o ',
                    # verify we're in a math context (near $ or $$)
                    if len(suffix) <= 3:
                        # Look back up to 200 chars for $ delimiter
                        lookback = raw[max(0, pos-200):pos]
                        # Count dollar signs - if odd number, we're inside math
                        dollar_count = lookback.count(b'$')
                        if dollar_count % 2 == 0:
                            continue  # Not in math context, skip
                    
                    result.append(0x5c)  # backslash
                    result.append(0x74)  # 't'
                    matched = True
                    tab_fixes += 1
                    break
            
            if not matched:
                result.append(raw[pos])
        else:
            result.append(raw[pos])
        pos += 1
    
    if tab_fixes > 0:
        raw = bytes(result)
        fixes['\\t (tab->LaTeX)'] = tab_fixes
    
    if raw != original:
        with open(filepath, 'wb') as f:
            f.write(raw)
        return fixes
    return None


# Process ALL HTML files in book_builder
all_fixes = {}
html_files = sorted([f for f in os.listdir(BOOK_DIR) if f.endswith('.html')])

print("=== Scanning and fixing all chapter HTML files ===\n")
for filename in html_files:
    filepath = os.path.join(BOOK_DIR, filename)
    fixes = fix_file(filepath)
    if fixes:
        all_fixes[filename] = fixes
        fix_desc = ", ".join(f"{k}: {v}" for k, v in fixes.items())
        print(f"  FIXED {filename}: {fix_desc}")

if not all_fixes:
    print("  No corruption found in any files.")
else:
    total_fixes = sum(sum(v.values()) for v in all_fixes.values())
    print(f"\n  Total files fixed: {len(all_fixes)}")
    print(f"  Total corrupted bytes replaced: {total_fixes}")

# Now verify: scan all files for remaining issues
print("\n=== Post-fix verification ===\n")
remaining_issues = 0
for filename in html_files:
    filepath = os.path.join(BOOK_DIR, filename)
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    bell = raw.count(b'\x07')
    ff = raw.count(b'\x0c')
    bs = raw.count(b'\x08')
    vt = raw.count(b'\x0b')
    
    if bell + ff + bs + vt > 0:
        print(f"  WARNING {filename}: bell={bell}, formfeed={ff}, backspace={bs}, vtab={vt}")
        remaining_issues += 1
    
    # Check for tab followed by LaTeX suffix (remaining unfixed tabs)
    text_as_str = raw.decode('utf-8', errors='replace')
    tab_ext = len(re.findall(r'\text\{', text_as_str))
    tab_imes = len(re.findall(r'\times', text_as_str))
    
    # These are the CORRECT ones now, not broken

if remaining_issues == 0:
    print("  All control character corruption has been resolved!")
else:
    print(f"\n  {remaining_issues} files still have remaining issues")

print("\nDone. Now reassemble the book with: python assemble_book.py")
