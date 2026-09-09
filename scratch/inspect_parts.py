# scratch/inspect_parts.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

for part_num in [2, 3, 4, 5]:
    with open(f'book_builder/part{part_num}.html', 'r', encoding='utf-8') as f:
        content = f.read()
    idx = content.find('<div class="chapter"')
    print(f'=== PART {part_num} ===')
    print(content[:idx].strip())
    # Check what chapters are in this file
    import re
    ch_nums = re.findall(r'<span class="chapter-number">([^<]+)</span>', content)
    print(f'Chapters in part{part_num}.html:', ch_nums)
