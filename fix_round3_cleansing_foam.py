# -*- coding: utf-8 -*-
path = "products/glucola-cleansing-foam.html"
with open(path, encoding='utf-8') as f:
    text = f.read()

REPLACEMENTS = [
    ('{"@type":"Question","name":"他のグルコラシリーズと一緒に使えますか？","acceptedAnswer":{"@type":"Answer","text":"グルコラシリーズはクレンジングフォーム→スキン（化粧水）→セラム（美容液）→ローション（乳液）という順番で重ねるトータルケアとして設計されています。シリーズで揃えることで相乗効果が期待できます。"}},',
     '{"@type":"Question","name":"他のグルコラシリーズと一緒に使えますか？","acceptedAnswer":{"@type":"Answer","text":"グルコラシリーズはクレンジングフォーム→スキン（化粧水）→セラム（美容液）→ローション（乳液）という順番で重ねるトータルケアとして設計されています。シリーズで揃えることで、組み合わせて使いやすい設計です。"}},'),
    ('{"@type":"Question","name":"どんな肌悩みに向いていますか？","acceptedAnswer":{"@type":"Answer","text":"透明感・くすみ改善・毛穴の黒ずみ・乾燥が気になる方に特におすすめです。グルタチオンの抗酸化作用とナノコラーゲン（300Da）の保湿作用が、洗うたびに肌の土台を整えます。"}},',
     '{"@type":"Question","name":"どんな肌悩みに向いていますか？","acceptedAnswer":{"@type":"Answer","text":"透明感のある肌印象・くすみが気になる肌・毛穴の黒ずみ・乾燥が気になる方に特におすすめです。グルタチオンの抗酸化ケアで知られる働きとナノコラーゲン（300Da）の保湿作用が、洗うたびに肌の土台を整えます。"}},'),
    ('<p class="faq-answer">グルコラシリーズはクレンジングフォーム→スキン（化粧水）→セラム（美容液）→ローション（乳液）という順番で重ねるトータルケアとして設計されています。シリーズで揃えることで相乗効果が期待できます。</p>',
     '<p class="faq-answer">グルコラシリーズはクレンジングフォーム→スキン（化粧水）→セラム（美容液）→ローション（乳液）という順番で重ねるトータルケアとして設計されています。シリーズで揃えることで、組み合わせて使いやすい設計です。</p>'),
    ('<p class="faq-answer">透明感・くすみ改善・毛穴の黒ずみ・乾燥が気になる方に特におすすめです。グルタチオンの抗酸化作用とナノコラーゲン（300Da）の保湿作用が、洗うたびに肌の土台を整えます。</p>',
     '<p class="faq-answer">透明感のある肌印象・くすみが気になる肌・毛穴の黒ずみ・乾燥が気になる方に特におすすめです。グルタチオンの抗酸化ケアで知られる働きとナノコラーゲン（300Da）の保湿作用が、洗うたびに肌の土台を整えます。</p>'),
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
