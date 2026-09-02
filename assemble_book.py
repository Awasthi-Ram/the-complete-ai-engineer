# assemble_book.py
import os

def assemble_manuscript():
    html_files = [
        'book_builder/frontmatter.html',
        'book_builder/part0.html',
        'book_builder/part1.html',
        'book_builder/part2.html',
        'book_builder/part3.html',
        'book_builder/part4.html',
        'book_builder/part5.html',
        'book_builder/part6.html',
        'book_builder/part7.html',
        'book_builder/part8.html',
        'book_builder/backmatter.html'
    ]
    
    parts = []
    for rel_path in html_files:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            parts.append(content)
            print(f"Loaded {rel_path} ({len(content):,} chars)")
            
    full_html = "\n\n".join(parts) + "\n"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'book.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    size_bytes = os.path.getsize(output_path)
    print(f"Master manuscript assembled into {output_path} ({size_bytes:,} bytes) successfully!")

if __name__ == "__main__":
    assemble_manuscript()
