import os
import glob
import re
from collections import defaultdict

book_builder_dir = 'book_builder'
ch_files = sorted([f for f in os.listdir(book_builder_dir) if re.match(r'ch\d.*\.html', f)])

print(f"Total individual chapter files: {len(ch_files)}")

stats = []
all_div_classes = set()

for ch in ch_files:
    p = os.path.join(book_builder_dir, ch)
    size = os.path.getsize(p)
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for m in re.finditer(r'class="([^"]+)"', content):
        for c in m.group(1).split():
            all_div_classes.add(c)
            
    c_title = re.findall(r'class="chapter-title">([^<]+)', content)
    c_num = re.findall(r'class="chapter-number">([^<]+)', content)
    c_sub = re.findall(r'class="chapter-subtitle">([^<]+)', content)
    
    # Check problem structures
    # Let's search for interview problems / practice problems
    interview_probs = len(re.findall(r'class="interview-problem"', content))
    prob_cards = len(re.findall(r'class="problem-card"', content))
    prob_questions = len(re.findall(r'class="problem-question"', content))
    solutions = len(re.findall(r'class="solution"', content))
    code_labs = len(re.findall(r'class="code-lab"', content))
    projects = len(re.findall(r'class="project-section"', content))
    key_insights = len(re.findall(r'class="key-insight"', content))
    real_world_boxes = len(re.findall(r'class="real-world-box"', content))
    
    # H3 headings (main concepts)
    h3s = [h.strip() for h in re.findall(r'<h3>([^<]+)</h3>', content)]
    
    # Math equations ($$ or $)
    latex_blocks = len(re.findall(r'\$\$', content)) // 2
    latex_inline = len(re.findall(r'\$[^\$]+\$', content))
    
    # Word count
    text_only = re.sub(r'<[^>]+>', ' ', content)
    words = len(text_only.split())
    
    title = c_title[0].strip() if c_title else ch
    num = c_num[0].strip() if c_num else "?"
    sub = c_sub[0].strip() if c_sub else ""
    
    stats.append({
        'file': ch,
        'num': num,
        'title': title,
        'sub': sub,
        'size': size,
        'words': words,
        'problems': max(interview_probs, prob_cards, prob_questions),
        'solutions': solutions,
        'code_labs': code_labs,
        'projects': projects,
        'latex_blocks': latex_blocks,
        'latex_inline': latex_inline,
        'h3s': h3s
    })

print(f"{'Num':<12} | {'Title':<35} | {'Words':<6} | {'Probs':<5} | {'Labs':<4} | {'H3 Count':<8} | {'Math Blk':<8}")
print("-" * 90)
for s in stats:
    print(f"{s['num']:<12} | {s['title'][:35]:<35} | {s['words']:<6} | {s['problems']:<5} | {s['code_labs']:<4} | {len(s['h3s']):<8} | {s['latex_blocks']:<8}")

total_words = sum(s['words'] for s in stats)
total_probs = sum(s['problems'] for s in stats)
total_labs = sum(s['code_labs'] for s in stats)
total_projects = sum(s['projects'] for s in stats)
total_math = sum(s['latex_blocks'] for s in stats)

print("=" * 90)
print(f"Total Chapters: {len(stats)}")
print(f"Total Words   : {total_words:,}")
print(f"Total Problems: {total_probs}")
print(f"Total CodeLabs: {total_labs}")
print(f"Total Projects: {total_projects}")
print(f"Total Math Blk: {total_math}")

print("\nSample problem-related CSS classes found in HTML:")
print([c for c in sorted(all_div_classes) if 'prob' in c or 'sol' in c or 'quest' in c or 'tag' in c or 'exer' in c])

