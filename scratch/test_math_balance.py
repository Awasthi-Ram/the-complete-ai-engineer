import re

with open('book.html', 'r', encoding='utf-8') as f:
    text = f.read()

delim = chr(36) + chr(36)
parts = text.split(delim)
total_eqs = (len(parts) - 1) // 2
print(f'Total equations: {total_eqs}')

brace_mismatches = 0
for i in range(1, len(parts), 2):
    eq = parts[i]
    # Remove escaped braces \{ and \}
    clean = re.sub(r'\\[\{\}]', '', eq)
    open_b = clean.count('{')
    close_b = clean.count('}')
    if open_b != close_b:
        print(f'Equation {i//2} brace mismatch: open={open_b}, close={close_b}')
        print(eq.strip()[:140])
        print('-'*40)
        brace_mismatches += 1

print(f'Done checking {total_eqs} equations. Found {brace_mismatches} brace mismatches.')
