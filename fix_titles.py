# -*- coding: utf-8 -*-
"""
商品ページのtitle/og:title/twitter:titleを自然な形式に統一
「○○の効果とは？」形式を排除
"""

REPLACEMENTS = {
    "products/curlyshyll-repair-ampoule.html": [
        ('<title>アフターサロンケア リペア ヘアアンプルの効果｜LUMINOVE</title>',
         '<title>アフターサロンケア リペア ヘアアンプル｜高濃度タンパク質配合の韓国ヘアケア｜LUMINOVE</title>'),
        ('content="アフターサロンケア リペア ヘアアンプルの効果とは？高濃度タンパク質×5種マリン成分のサロン発想ヘアケア｜LUMINOVE"',
         'content="アフターサロンケア リペア ヘアアンプル｜高濃度タンパク質×5種マリン成分のサロン発想ヘアケア｜LUMINOVE"'),
    ],
    "products/glucola-cleansing-foam.html": [
        ('<title>グルコラ クレンジングフォームの効果とは？グルタチオン×ナノコラーゲン（300Da）配合洗顔｜LUMINOVE</title>',
         '<title>グルコラ クレンジングフォーム｜グルタチオン×ナノコラーゲン配合洗顔｜LUMINOVE</title>'),
        ('content="グルコラ クレンジングフォームの効果とは？グルタチオン×ナノコラーゲン（300Da）配合洗顔｜LUMINOVE"',
         'content="グルコラ クレンジングフォーム｜グルタチオン×ナノコラーゲン配合洗顔｜LUMINOVE"'),
    ],
    "products/glucola-serum.html": [
        ('<title>グルコラ セラム（美容液）の効果とは？グルタチオン30,000ppm配合の韓国美容液｜LUMINOVE</title>',
         '<title>グルコラ セラム（美容液）｜グルタチオン30,000ppm配合の韓国美容液｜LUMINOVE</title>'),
        ('content="グルコラ セラム（美容液）の効果とは？グルタチオン30,000ppm配合の韓国美容液｜LUMINOVE"',
         'content="グルコラ セラム（美容液）｜グルタチオン30,000ppm配合の韓国美容液｜LUMINOVE"'),
    ],
    "products/glucola-skin.html": [
        ('<title>グルコラ スキン（化粧水）の効果とは？グルタチオン×ナノコラーゲン（300Da）配合の韓国化粧水｜LUMINOVE</title>',
         '<title>グルコラ スキン（化粧水）｜グルタチオン×ナノコラーゲン配合の韓国化粧水｜LUMINOVE</title>'),
        ('content="グルコラ スキン（化粧水）の効果とは？グルタチオン×ナノコラーゲン（300Da）配合の韓国化粧水｜LUMINOVE"',
         'content="グルコラ スキン（化粧水）｜グルタチオン×ナノコラーゲン配合の韓国化粧水｜LUMINOVE"'),
    ],
    "products/rg3-vital-ampoule.html": [
        ('<title>クイーンズ RG3 モイスチャーセラムの効果｜LUMINOVE</title>',
         '<title>クイーンズ RG3 モイスチャーセラム｜高麗人参由来RG3配合の韓国美容液｜LUMINOVE</title>'),
        ('content="クイーンズ RG3 モイスチャーセラムの効果とは？高麗人参由来RG3配合のブースターアンプル｜LUMINOVE"',
         'content="クイーンズ RG3 モイスチャーセラム｜高麗人参由来RG3配合のブースターアンプル｜LUMINOVE"'),
    ],
    "products/rg3-vital-cream.html": [
        ('<title>クイーンズ RG3 モイスチャークリームの効果｜LUMINOVE</title>',
         '<title>クイーンズ RG3 モイスチャークリーム｜高麗人参由来RG3配合の韓国クリーム｜LUMINOVE</title>'),
        ('content="クイーンズ RG3 モイスチャークリームの効果とは？高麗人参由来RG3配合の弾力保湿ナイトクリーム｜LUMINOVE"',
         'content="クイーンズ RG3 モイスチャークリーム｜高麗人参由来RG3配合の弾力保湿ナイトクリーム｜LUMINOVE"'),
    ],
}

total = 0
for path, pairs in REPLACEMENTS.items():
    with open(path, encoding='utf-8') as f:
        text = f.read()
    for old, new in pairs:
        count = text.count(old)
        if count == 0:
            print(f'  NOT FOUND in {path}: {old[:60]}')
            continue
        text = text.replace(old, new)
        total += count
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'  Updated: {path}')

print(f'\n合計置換: {total}件')

# 検証
print('\n=== 検証(残存「効果とは？」「の効果」チェック) ===')
import glob
for path in glob.glob('products/*.html'):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    title_line = [l for l in text.split('\n') if '<title>' in l]
    if title_line and ('効果とは' in title_line[0] or 'の効果｜' in title_line[0] or 'の効果<' in title_line[0]):
        print(f'  残存: {path} -> {title_line[0].strip()}')
print('チェック完了')
