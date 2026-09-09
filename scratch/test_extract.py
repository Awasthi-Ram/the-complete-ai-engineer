# scratch/test_extract.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

for p in [2, 3, 4, 5]:
    with open(f'book_builder/part{p}.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    first_ch = content.find('<div class="chapter"')
    header = content[:first_ch].strip()
    
    capstone_pos = content.rfind('<div class="project-section">')
    comment_pos = content.rfind('<!-- ===', 0, capstone_pos)
    if comment_pos != -1 and 'HANDS-ON' in content[comment_pos:capstone_pos]:
        capstone = content[comment_pos:].strip()
    else:
        capstone = content[capstone_pos:].strip()
        
    print(f"=== Part {p} ===")
    print(f"Header: {len(header)} chars")
    print(f"Capstone: {len(capstone)} chars")
    assert 'class="chapter"' not in capstone, f"Error: chapters inside capstone in part {p}!"
    print("  [OK] Clean capstone with zero chapter divs!")
