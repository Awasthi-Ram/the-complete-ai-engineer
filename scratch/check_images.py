import re
import os

with open('book.html', 'r', encoding='utf-8') as f:
    text = f.read()

imgs = set(re.findall(r'src=["\']([^"\']+\.(?:png|jpg|jpeg|svg|webp))["\']', text))
print(f'Found {len(imgs)} unique images:')
for img in sorted(imgs):
    print(f'  {img}: exists = {os.path.exists(img)}')
