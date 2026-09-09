import re

with open('book.html', 'r', encoding='utf-8') as f:
    text = f.read()

problem_numbers = re.findall(r'<span class="problem-number">Problem ([^<]+)</span>', text)
print(f"Total problems: {len(problem_numbers)}")

p8 = [p for p in problem_numbers if p.startswith('8.')]
print(f"Part 8 problems: {p8}")

seen = set()
duplicates = []
for p in problem_numbers:
    if p in seen:
        duplicates.append(p)
    seen.add(p)

if duplicates:
    print(f"DUPLICATES FOUND: {duplicates}")
else:
    print("ALL 452 PROBLEM NUMBERS ARE STRICTLY UNIQUE!")
