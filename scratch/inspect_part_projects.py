# scratch/inspect_part_projects.py
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for part_num in range(9):
    with open(f'book_builder/part{part_num}.html', 'r', encoding='utf-8') as f:
        content = f.read()
    projs = re.findall(r'<div class="project-(?:section|header)">[\s\S]*?<h3 class="project-title">([^<]+)</h3>', content)
    print(f'Part {part_num} project titles found in part{part_num}.html: {projs}')
