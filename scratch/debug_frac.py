import re

with open('book_builder/ch01_how_to_learn.html', 'rb') as f:
    raw = f.read()

# Find all positions of 'rac{' in raw bytes
pos = 0
count = 0
while True:
    idx = raw.find(b'rac{', pos)
    if idx == -1:
        break
    # Check byte before
    if idx > 0:
        byte_before = raw[idx-1]
        if byte_before != 0x5c:  # not backslash
            # Also check if preceded by \f (0x5c 0x66)
            if idx >= 2 and raw[idx-2] == 0x5c and raw[idx-1] == 0x66:
                # This is \frac - correct!
                pass
            else:
                ctx = raw[max(0,idx-10):idx+15]
                byte_hex = hex(byte_before)
                print(f"Broken rac{{ at byte {idx}: preceding=0x{byte_before:02x} ({chr(byte_before) if byte_before > 31 else 'CTRL'})")
                print(f"  Context: {repr(ctx)}")
                count += 1
    pos = idx + 1

print(f"\nTotal broken rac{{ instances: {count}")
