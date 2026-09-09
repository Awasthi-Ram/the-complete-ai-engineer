import re

# Check raw bytes to understand the exact corruption
with open('book_builder/ch11_linear_algebra.html', 'rb') as f:
    raw = f.read()

# Find first occurrence of 'rac{' that is NOT preceded by backslash byte (0x5c)
pos = 0
examples = 0
while examples < 5:
    idx = raw.find(b'rac{', pos)
    if idx == -1:
        break
    # Check byte before
    if idx > 0 and raw[idx-1:idx] != b'\\':
        preceding = raw[idx-1:idx]
        context = raw[max(0,idx-30):idx+40]
        print(f"Pos {idx}: preceding byte = 0x{raw[idx-1]:02x}")
        sep = " "
        print(f"  Hex context: {context.hex(sep)}")
        print(f"  Text (repr): {repr(context)}")
        print()
        examples += 1
    pos = idx + 1

# Also check what's happening with \left and \right
print("=== Checking \\left / \\right patterns ===")
for pattern, name in [(b'eft(', 'left('), (b'eft[', 'left['), (b'ight)', 'right)'), (b'ight]', 'right]')]:
    pos = 0
    count = 0
    while True:
        idx = raw.find(pattern, pos)
        if idx == -1:
            break
        if idx > 0 and raw[idx-1:idx] != b'\\':
            if count == 0:
                context = raw[max(0,idx-10):idx+20]
                print(f"  {name}: preceding byte = 0x{raw[idx-1]:02x}, context = {repr(context)}")
            count += 1
        pos = idx + 1
    if count > 0:
        print(f"  Total broken {name}: {count}")
