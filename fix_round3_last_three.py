# -*- coding: utf-8 -*-

# pdrn-nmn-cream.html: 「相乗効果を解説」を全箇所で統一変更
path = "blog/pdrn-nmn-cream.html"
with open(path, encoding='utf-8') as f:
    text = f.read()
count = text.count("相乗効果を解説")
text = text.replace("相乗効果を解説", "組み合わせの理由を解説")
with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print(f'pdrn-nmn-cream.html: {count}件置換')

# blog/index.html: カード見出しも合わせて変更
path = "blog/index.html"
with open(path, encoding='utf-8') as f:
    text = f.read()
old = '<h2>PDRN×NMNクリームとは？相乗効果を解説</h2>'
new = '<h2>PDRN×NMNクリームとは？組み合わせの理由を解説</h2>'
if old in text:
    text = text.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('blog/index.html: 置換OK')
else:
    print('blog/index.html: NOT FOUND')

# korean-skincare-recommended.html
path = "blog/korean-skincare-recommended.html"
with open(path, encoding='utf-8') as f:
    text = f.read()

REPLACEMENTS = [
    ('<li><a href="#glutathione">透明感・くすみ改善 ─ グルタチオン配合</a></li>',
     '<li><a href="#glutathione">透明感ケア・くすみが気になる肌のケア ─ グルタチオン配合</a></li>'),
    ('<h2>透明感・くすみ改善 ─ グルタチオン配合ブランド</h2>',
     '<h2>透明感ケア・くすみが気になる肌のケア ─ グルタチオン配合ブランド</h2>'),
    ('グルタチオンは美容点滴（白玉注射）の主成分。透明感・くすみ改善・抗酸化を目的に韓国コスメへの高配合が進んでいます。',
     'グルタチオンは美容点滴（白玉注射）の主成分。透明感ケア・くすみが気になる肌のケア・抗酸化ケアを目的に韓国コスメへの高配合が進んでいます。'),
    ('<p>PDRN3000ppm×NMN1000ppmのデュアルフォーミュラ。EGF・セラミドNP・ツボクサエキスを複合配合。美容施術後ケア・ニキビ跡・色素沈着に特化した低刺激・無香料クリーム。</p>',
     '<p>PDRN3000ppm×NMN1000ppmのデュアルフォーミュラ。EGF・セラミドNP・ツボクサエキスを複合配合。美容施術後のデリケートな肌の保湿ケア・ニキビ跡やくすみが気になる肌のケアに特化した低刺激・無香料クリーム。</p>'),
    ('<tr><td>透明感・くすみ改善</td><td>グルタチオン</td><td><a href="/products/glucola-serum.html">グルコラ セラム</a>・<a href="/products/glucola-skin.html">スキン</a></td></tr>',
     '<tr><td>透明感ケア・くすみが気になる肌</td><td>グルタチオン</td><td><a href="/products/glucola-serum.html">グルコラ セラム</a>・<a href="/products/glucola-skin.html">スキン</a></td></tr>'),
    ('<tr><td>ニキビ跡・色素沈着</td><td>PDRN＋NMN</td><td><a href="/products/rejun-pdrn-cream.html">リジュエヌ クリーム</a></td></tr>',
     '<tr><td>ニキビ跡やくすみが気になる肌</td><td>PDRN＋NMN</td><td><a href="/products/rejun-pdrn-cream.html">リジュエヌ クリーム</a></td></tr>'),
]

errors = []
for old, new in REPLACEMENTS:
    if old not in text:
        errors.append(old[:50])
        continue
    text = text.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print(f'korean-skincare-recommended.html: エラー{len(errors)}件')
for e in errors:
    print(f'  NOT FOUND: {e}')
