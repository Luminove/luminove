# -*- coding: utf-8 -*-
"""
ナノコラーゲン表記統一
表示名: ナノコラーゲン（300Da）
説明文: 300Da低分子コラーゲン
"""
import glob, re

# 個別修正(見出し内の重複表現)
SPECIFIC = {
    "products/glucola-cleansing-foam.html": [
        ('<h3>②300Daコラーゲン<br>角質層まで届く低分子設計</h3>',
         '<h3>②ナノコラーゲン（300Da）<br>角質層までうるおいを届ける低分子設計</h3>'),
        ('グルコラ クレンジングフォームに配合されている「300Daコラーゲン」は、一般的なコラーゲンよりも分子量を小さく設計した低分子タイプ。洗顔中の短い接触時間でも角質層まで浸透しやすく、洗い流すタイプの処方でも"うるおいを置いていく"洗顔を実現しています。',
         'グルコラ クレンジングフォームに配合されている「ナノコラーゲン（300Da）」は、一般的なコラーゲンよりも分子量を小さく設計した低分子タイプ。洗顔中の短い接触時間でも角質層までうるおいを届けやすく、洗い流すタイプの処方でも"うるおいを置いていく"洗顔を実現しています。'),
        ('洗うたびに「乾燥して肌がつっぱる」という悩みを抱えている方ほど、この300Daコラーゲンの恩恵を実感しやすいといわれています。',
         '洗うたびに「乾燥して肌がつっぱる」という悩みを抱えている方ほど、このナノコラーゲン（300Da）の恩恵を実感しやすいといわれています。'),
    ],
    "products/glucola-skin.html": [
        ('<h3>②300Daコラーゲン<br>角質層まで届く超低分子コラーゲン</h3>',
         '<h3>②ナノコラーゲン（300Da）<br>角質層までうるおいを届ける低分子コラーゲン</h3>'),
        ('コラーゲンは通常、分子量が大きく皮膚の奥まで届きにくいとされていますが、300Daまで低分子化した「300Daコラーゲン」は角質層への浸透を考えて設計されています。',
         'コラーゲンは通常、分子量が大きく皮膚の奥まで届きにくいとされていますが、300Daまで低分子化した「ナノコラーゲン（300Da）」は角質層までうるおいを届けることを考えて設計されています。'),
    ],
}

for path, pairs in SPECIFIC.items():
    with open(path, encoding='utf-8') as f:
        text = f.read()
    for old, new in pairs:
        if old not in text:
            print(f'  NOT FOUND in {path}: {old[:50]}...')
            continue
        text = text.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'  Specific fix applied: {path}')

# 一括置換: 残った bare "300Daコラーゲン" を "ナノコラーゲン（300Da）" に統一
files = sorted(set(glob.glob('*.html') + glob.glob('ingredients/*.html') +
                    glob.glob('products/*.html') + glob.glob('blog/*.html') +
                    glob.glob('doctor/*.html')))

total = 0
for path in files:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    original = text
    # "300Daコラーゲン" -> "ナノコラーゲン（300Da）" (前後に既に「ナノコラーゲン」等が無い場合のみ)
    new_text, count = re.subn(r'300Daコラーゲン(?!エキス)', 'ナノコラーゲン（300Da）', text)
    if count:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        total += count
        print(f'  {path}: 一括置換 {count}件')

print(f'\n合計一括置換: {total}件')

# 検証
print('\n=== 検証 ===')
remaining = []
for path in files:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    for pattern in ['300Daナノコラーゲン', '300Da コラーゲン', '300Da超低分子コラーゲン',
                    '浸透力を極めたナノコラーゲン', '300Daコラーゲン']:
        if pattern in text:
            remaining.append((path, pattern))

if remaining:
    for p, pat in remaining:
        print(f'  残存: {p} -> {pat}')
else:
    print('  残存なし：表記統一完了')
