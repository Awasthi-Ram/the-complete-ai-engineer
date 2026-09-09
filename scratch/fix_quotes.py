with open('scratch/expand_ch02.py', 'r', encoding='utf-8') as f:
    text = f.read()

# First replace start and end markers
prefix = 'ch02_content = """'
suffix = '"""\n\nwith open'

start_idx = text.find(prefix) + len(prefix)
end_idx = text.rfind(suffix)

html_part = text[start_idx:end_idx]
# replace triple quotes in html_part with '''
fixed_html = html_part.replace('"""', "'''")

new_script = text[:start_idx] + fixed_html + text[end_idx:]

with open('scratch/expand_ch02.py', 'w', encoding='utf-8') as f:
    f.write(new_script)

print("Fixed expand_ch02.py")
