import os
import re

book_builder_dir = 'book_builder'
ch_files = sorted([f for f in os.listdir(book_builder_dir) if re.match(r'ch\d.*\.html', f)])

report = []

for ch in ch_files:
    p = os.path.join(book_builder_dir, ch)
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    c_title = re.findall(r'class="chapter-title">([^<]+)', content)
    c_num = re.findall(r'class="chapter-number">([^<]+)', content)
    c_sub = re.findall(r'class="chapter-subtitle">([^<]+)', content)
    
    title = c_title[0].strip() if c_title else ch
    num = c_num[0].strip() if c_num else "?"
    sub = c_sub[0].strip() if c_sub else ""
    
    h3s = [re.sub(r'\s+', ' ', h.strip()) for h in re.findall(r'<h3>([^<]+)</h3>', content)]
    h4s = [re.sub(r'\s+', ' ', h.strip()) for h in re.findall(r'<h4>([^<]+)</h4>', content)]
    
    # Practice problems questions and solutions
    questions = re.findall(r'<strong>QUESTION:?</strong>\s*([^<]+)', content)
    
    # Code labs
    code_labs = re.findall(r'class="code-lab-header">([^<]+)', content)
    
    # Text length
    text_only = re.sub(r'<[^>]+>', ' ', content)
    words = len(text_only.split())
    
    report.append({
        'file': ch,
        'num': num,
        'title': title,
        'sub': sub,
        'words': words,
        'h3s': h3s,
        'h4s': h4s[:6], # first 6
        'questions': questions,
        'code_labs': code_labs
    })

with open('scratch/chapter_deep_audit.txt', 'w', encoding='utf-8') as out:
    for r in report:
        out.write(f"================================================================================\n")
        out.write(f"[{r['num']}] {r['title']} ({r['words']} words)\n")
        out.write(f"Subtitle: {r['sub']}\n")
        out.write(f"File: {r['file']}\n")
        out.write(f"Sections (H3):\n")
        for h in r['h3s']:
            out.write(f"   - {h}\n")
        out.write(f"Subsections (H4 sample):\n")
        for h in r['h4s']:
            out.write(f"     * {h}\n")
        out.write(f"Practice Problems ({len(r['questions'])}):\n")
        for q in r['questions']:
            out.write(f"     ? {q[:120]}...\n")
        out.write(f"Code Labs ({len(r['code_labs'])}):\n")
        for cl in r['code_labs']:
            out.write(f"     [LAB] {cl}\n")
        out.write("\n")

print("Saved deep audit to scratch/chapter_deep_audit.txt")
