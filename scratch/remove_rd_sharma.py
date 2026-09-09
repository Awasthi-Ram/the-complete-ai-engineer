"""
remove_rd_sharma.py — Removes all references to 'R.D. Sharma' / 'RD Sharma'
across the book manuscript and replaces them with professional first-principles terminology.
Preserves scientific citation 'Archit Sharma' in Chapter 5.6.
"""
import os
import re
import glob

replacements = [
    (
        r'<!-- SECTION (\d+): THE RD SHARMA 4-TIER PRACTICE SUITE -->',
        r'<!-- SECTION \1: THE 4-TIER GRADED PRACTICE SUITE -->'
    ),
    (
        r'<h3>The R\.?D\.?\s*Sharma Practice Suite\s*([—\-\–\?]+)\s*(Chapter \d+\.\d+)</h3>',
        r'<h3>The 4-Tier Graded Practice Suite — \2</h3>'
    ),
    (
        r'Modeled after the beloved R\.?D\.?\s*Sharma mathematical textbooks,',
        r'Built from the ground up on first principles,'
    ),
    (
        r'Inspired by the classic Indian mathematics textbooks of R\.?D\.?\s*Sharma that emphasized thorough intuition, mathematical proof, and relentless problem-solving practice,',
        r'Emphasizing thorough first-principles intuition, exhaustive mathematical derivations, and relentless problem-solving practice,'
    ),
    (
        r'Inspired by the legendary R\.?D\.?\s*Sharma mathematics series, this book teaches artificial intelligence from first principles',
        r'Designed as an exhaustive, first-principles masterwork, this book teaches artificial intelligence from the ground up'
    ),
    (
        r'This book is modeled after the legendary R\.?D\.?\s*Sharma mathematics series that taught millions of engineers',
        r'This book is designed as an exhaustive, first-principles masterwork that teaches engineers'
    )
]

files_to_update = glob.glob('book_builder/ch*.html') + [
    'book_builder/frontmatter.html',
    'book_builder/backmatter.html',
    'book_builder/frontmatter.py',
    'book_builder/backmatter.py',
    'book_builder/part0_foundations.py'
]

print("Processing files to remove R.D. Sharma references...")
total_replaced = 0

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content
    for pattern, repl in replacements:
        content, count = re.subn(pattern, repl, content)
        if count > 0:
            print(f"  [{filepath}] Replaced {count} instance(s) of pattern: {pattern[:40]}...")
            total_replaced += count

    if content != orig_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [UPDATED] {filepath}")

print(f"\nTotal replacements made: {total_replaced}")
