import os
import re

def verify_book():
    book_path = "book.html"
    with open(book_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Master Book size: {len(content):,} characters / {len(content.encode('utf-8')):,} bytes")
    print(f"Total lines: {len(content.splitlines()):,}")

    # Count problems
    problem_divs = re.findall(r'<div class="problem">', content)
    problem_numbers = re.findall(r'<span class="problem-number">([^<]+)</span>', content)
    print(f"\nTotal problem containers: {len(problem_divs)}")
    print(f"Total labeled problems: {len(problem_numbers)}")

    # Check Part breakdowns
    p0_problems = [p for p in problem_numbers if p.startswith("Problem 0.")]
    p1_problems = [p for p in problem_numbers if p.startswith("Problem 1.")]
    p2_problems = [p for p in problem_numbers if p.startswith("Problem 2.")]
    p3_problems = [p for p in problem_numbers if p.startswith("Problem 3.")]
    p4_problems = [p for p in problem_numbers if p.startswith("Problem 4.")]
    p5_problems = [p for p in problem_numbers if p.startswith("Problem 5.")]
    p6_problems = [p for p in problem_numbers if p.startswith("Problem 6.")]
    p7_problems = [p for p in problem_numbers if p.startswith("Problem 7.")]
    p8_problems = [p for p in problem_numbers if p.startswith("Problem 8.")]

    print(f"\n--- Problem Breakdown ---")
    print(f"Part 0 (Foundations): {len(p0_problems)} problems")
    print(f"Part 1 (Mathematics of AI): {len(p1_problems)} problems")
    print(f"Part 2 (Classical Machine Learning): {len(p2_problems)} problems")
    print(f"Part 3 (Neural Networks from Scratch): {len(p3_problems)} problems")
    print(f"Part 4 (Deep Learning Architectures): {len(p4_problems)} problems")
    print(f"Part 5 (Transformers, LLMs & Multi-Agent Systems): {len(p5_problems)} problems")
    print(f"Part 6 (MLOps & Systems): {len(p6_problems)} problems")
    print(f"Part 7 (Security, Ethics & Governance): {len(p7_problems)} problems")
    print(f"Part 8 (Emerging Frontiers): {len(p8_problems)} problems")
    print(f"\nGrand Total Problems in Manuscript: {len(problem_numbers)}")

    # Verify Math Delimiters
    dd_count = content.count("$$")
    print(f"\nMathJax '$$' delimiters: {dd_count} (Must be even: {dd_count % 2 == 0})")

    # Check HTML tag balances for major structures
    for tag in ['div class="problem"', 'div class="solution"', 'div class="chapter"']:
        opens = len(re.findall(f'<{tag}', content))
        print(f"Tag <{tag}>: {opens} instances")

    # Check code lab links and repo links
    repo_links = re.findall(r'href="(https://github.com/[^"]+)"', content)
    print(f"\nGitHub Solution repo links found: {len(repo_links)}")

if __name__ == "__main__":
    verify_book()
