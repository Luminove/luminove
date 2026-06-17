# -*- coding: utf-8 -*-
import re, os

files = ['index.html'] + ['products/'+f for f in os.listdir('products') if f.endswith('.html')]
files += ['ingredients/'+f for f in os.listdir('ingredients') if f.endswith('.html')]
files += ['doctor/index.html']

used = {}
for path in files:
    if not os.path.isfile(path):
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
    imgs = re.findall(r'src="((?:\.\./)?images/[^"]+)"', content)
    for img in imgs:
        if img not in used:
            used[img] = []
        used[img].append(path)

print('=== JPG/PNG still referenced (WebP exists = convertible) ===')
for img in sorted(used.keys()):
    ext = img.lower().rsplit('.',1)[-1]
    if ext in ('jpg','jpeg','png'):
        webp = img.rsplit('.',1)[0] + '.webp'
        actual = webp.replace('../','')
        exists = os.path.isfile(actual)
        print(('[webp OK] ' if exists else '[no webp] ') + img)

print()
print('=== All images in images/ folder NOT referenced in any HTML ===')
all_files = set()
for f in os.listdir('images'):
    full = os.path.join('images', f)
    if os.path.isfile(full):
        all_files.add('images/'+f)

all_referenced = set(img.replace('../','') for img in used.keys())
unused = all_files - all_referenced
for f in sorted(unused):
    sz = os.path.getsize(f)
    print(f'  {sz//1024}KB  {f}')
