# -*- coding: utf-8 -*-
path = "products/glucola-peeling-pack2.html"
with open(path, encoding='utf-8') as f:
    text = f.read()

REPLACEMENTS = [
    ('{"@type":"Question","name":"グルタチオン1,400ppmとはどれほどの濃度ですか？","acceptedAnswer":{"@type":"Answer","text":"通常の韓国コスメに配合されるグルタチオンが100〜300ppm程度であるのに対し、本製品は1,400ppmを配合。美容点滴（白玉注射）の主成分を高濃度で配合した、セルフケアとしてはトップクラスの濃度です。"}},',
     '{"@type":"Question","name":"グルタチオン1,400ppmとはどれほどの濃度ですか？","acceptedAnswer":{"@type":"Answer","text":"通常の韓国コスメに配合されるグルタチオンが100〜300ppm程度であるのに対し、本製品は1,400ppmを配合。グルタチオンを高濃度で配合した、セルフケアとしては高濃度タイプです。"}},'),
    ('{"@type":"Question","name":"他のスキンケアと組み合わせて使えますか？","acceptedAnswer":{"@type":"Answer","text":"パック使用後は角質が除去されて美容成分が浸透しやすい状態になります。その後にグルコラ スキン（化粧水）やセラム（美容液）を重ねると、より高い効果が期待できます。"}},',
     '{"@type":"Question","name":"他のスキンケアと組み合わせて使えますか？","acceptedAnswer":{"@type":"Answer","text":"パック使用後は角質が除去されて、スキンケアが肌になじみやすい状態に整います。その後にグルコラ スキン（化粧水）やセラム（美容液）を重ねると、より丁寧な保湿ケアにつながります。"}},'),
    ('臨床試験では、使用後すぐに肌のツヤ・トーンアップを実感できることが確認されており、特別な日の前のスペシャルケアとしても選ばれています。',
     '試験データを参考に、使用直後のツヤ感や肌印象に着目して設計されています。特別な日の前のスペシャルケアとしても選ばれています。'),
    ('<p class="faq-answer">通常の韓国コスメに配合されるグルタチオンが100〜300ppm程度であるのに対し、本製品は1,400ppmを配合。美容点滴（白玉注射）の主成分を高濃度で配合した、セルフケアとしてはトップクラスの濃度です。</p>',
     '<p class="faq-answer">通常の韓国コスメに配合されるグルタチオンが100〜300ppm程度であるのに対し、本製品は1,400ppmを配合。グルタチオンを高濃度で配合した、セルフケアとしては高濃度タイプです。</p>'),
    ('<p class="faq-answer">パック使用後は角質が除去されて美容成分が浸透しやすい状態になります。その後にグルコラ スキン（化粧水）やセラム（美容液）を重ねると、より高い効果が期待できます。</p>',
     '<p class="faq-answer">パック使用後は角質が除去されて、スキンケアが肌になじみやすい状態に整います。その後にグルコラ スキン（化粧水）やセラム（美容液）を重ねると、より丁寧な保湿ケアにつながります。</p>'),
]

errors = []
for old, new in REPLACEMENTS:
    count = text.count(old)
    if count == 0:
        errors.append(old[:60])
        continue
    text = text.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'置換完了。エラー: {len(errors)}件')
for e in errors:
    print(f'  NOT FOUND: {e}')
