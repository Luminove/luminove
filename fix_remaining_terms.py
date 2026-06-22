# -*- coding: utf-8 -*-
"""
「ダウンタイムケア」「アンチエイジング」の残存箇所を統一表現に置換
"""

REPLACEMENTS = {
    "blog/korean-skincare-recommended.html": [
        ('<tr><td>施術後ダウンタイムケア</td><td>PDRN（低刺激）</td><td><a href="/products/rejun-pdrn-cream.html">リジュエヌ クリーム</a></td></tr>',
         '<tr><td>施術後の保湿ケア</td><td>PDRN（低刺激）</td><td><a href="/products/rejun-pdrn-cream.html">リジュエヌ クリーム</a></td></tr>'),
    ],
    "blog/pdrn-what-is.html": [
        ('ただし<strong>施術後のダウンタイムケア</strong>として使用することで、肌回復のサポートが期待できます。リジュエヌ クリームはこの施術後ケアを主目的として設計されています。',
         'ただし<strong>施術後のデリケートな肌の保湿ケア</strong>として使用することで、肌コンディションを整えるサポートが期待できます。リジュエヌ クリームはこの施術後ケアを主目的として設計されています。'),
        ('<li>美容施術（レーザー・ピーリング・注射）後のダウンタイムケア</li>',
         '<li>美容施術（レーザー・ピーリング・注射）後のデリケートな肌の保湿ケア</li>'),
        ('NMN（ニコチンアミドモノヌクレオチド）は細胞のエネルギー源であるNAD+の前駆体で、アンチエイジング研究で注目される成分です。',
         'NMN（ニコチンアミドモノヌクレオチド）は細胞のエネルギー源であるNAD+の前駆体で、エイジングケア分野の研究で注目される成分です。'),
    ],
    "index.html": [
        ('グルタチオン30,000ppm配合の"アンチエイジング・シンデレラクリーム"。',
         'グルタチオン30,000ppm配合の"エイジングケア・シンデレラクリーム"。'),
        ('<p class="brand-catch">美容施術後のダウンタイムケア</p>',
         '<p class="brand-catch">美容施術後の保湿ケア</p>'),
    ],
    "ingredients/pdrn.html": [
        ('{"@type":"Question","name":"美容施術後にPDRN配合のクリームを使ってもいいですか？","acceptedAnswer":{"@type":"Answer","text":"PDRNは美容施術後のダウンタイムケアとして設計されていますが、施術直後の使用については必ず施術を行ったクリニックに相談してください。施術内容によって推奨ケアが異なります。"}},',
         '{"@type":"Question","name":"美容施術後にPDRN配合のクリームを使ってもいいですか？","acceptedAnswer":{"@type":"Answer","text":"PDRNは美容施術後のデリケートな肌の保湿ケアとして設計されていますが、施術直後の使用については必ず施術を行ったクリニックに相談してください。施術内容によって推奨ケアが異なります。"}},'),
        ('肌のターンオーバーに合わせた28日ルーティンケアを実現します。美容施術後のダウンタイムケアとして特におすすめです。',
         '肌のリズムに合わせた28日ルーティンケアとして設計されています。美容施術後のデリケートな肌の保湿ケアとして特におすすめです。'),
        ('<p class="faq-answer">PDRNは美容施術後のダウンタイムケアとして設計されていますが、施術直後の使用については必ず施術を行ったクリニックに相談してください。施術内容によって推奨ケアが異なります。</p>',
         '<p class="faq-answer">PDRNは美容施術後のデリケートな肌の保湿ケアとして設計されていますが、施術直後の使用については必ず施術を行ったクリニックに相談してください。施術内容によって推奨ケアが異なります。</p>'),
    ],
    "products/celviv-bio-kit.html": [
        ('イタリア産のプレミアムキャビア成分を配合。肌の調子を整える高い保湿力、抗酸化作用に効果的なビタミン、アンチエイジングに効果があるとされるオメガ3系脂肪酸を含み、「血色の良い肌」へと導くことをコンセプトにしています。',
         'イタリア産のプレミアムキャビア成分を配合。肌の調子を整える保湿成分、抗酸化ケアに着目したビタミン、エイジングケアに着目したオメガ3系脂肪酸を含み、「血色の良い肌」へと導くことをコンセプトにしています。'),
    ],
}

total = 0
for path, pairs in REPLACEMENTS.items():
    with open(path, encoding='utf-8') as f:
        text = f.read()
    for old, new in pairs:
        count = text.count(old)
        if count == 0:
            print(f'  NOT FOUND in {path}: {old[:50]}')
            continue
        text = text.replace(old, new)
        total += count
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'  Updated: {path}')

print(f'\n合計置換: {total}件')

# 最終検証
print('\n=== 最終検証 ===')
import glob
NG_WORDS = ['ダウンタイムケア','アンチエイジング']
files = sorted(set(glob.glob('*.html') + glob.glob('ingredients/*.html') + glob.glob('products/*.html') + glob.glob('blog/*.html')))
remaining = False
for path in files:
    with open(path, encoding='utf-8') as f:
        html = f.read()
    for w in NG_WORDS:
        if w in html:
            print(f'  残存: {path} -> {w}')
            remaining = True
print('残存なし' if not remaining else '要確認')
