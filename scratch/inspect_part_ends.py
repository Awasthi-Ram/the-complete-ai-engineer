# scratch/inspect_part_ends.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

for part_num in [2, 3, 4, 5]:
    with open(f'book_builder/part{part_num}.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f'=== End of part{part_num}.html ({len(lines)} lines) ===')
    print(''.join(lines[-25:]))
