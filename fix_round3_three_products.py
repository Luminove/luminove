# -*- coding: utf-8 -*-

FIXES = {
    "products/glucola-suncream.html": [
        ('{"@type":"Question","name":"グルタチオンが日焼け止めに配合されている意味は何ですか？","acceptedAnswer":{"@type":"Answer","text":"グルタチオンはUV照射による酸化ストレスを抑える抗酸化作用を持ちます。紫外線を浴びながらもその影響を内側から緩和することで、より効果的な光老化対策ができます。"}},',
         '{"@type":"Question","name":"グルタチオンが日焼け止めに配合されている意味は何ですか？","acceptedAnswer":{"@type":"Answer","text":"グルタチオンはUV照射による酸化ストレスにアプローチする、抗酸化ケアで知られる成分です。紫外線を浴びながらもその影響に内側からアプローチすることで、より丁寧なUVケアにつながります。"}},'),
        ('<p class="faq-answer">グルタチオンはUV照射による酸化ストレスを抑える抗酸化作用を持ちます。紫外線を浴びながらもその影響を内側から緩和することで、より効果的な光老化対策ができます。</p>',
         '<p class="faq-answer">グルタチオンはUV照射による酸化ストレスにアプローチする、抗酸化ケアで知られる成分です。紫外線を浴びながらもその影響に内側からアプローチすることで、より丁寧なUVケアにつながります。</p>'),
    ],
    "products/rejun-pdrn-cream.html": [
        ('{"@type":"Question","name":"他のスキンケアと一緒に使えますか？","acceptedAnswer":{"@type":"Answer","text":"化粧水などで肌を整えた後に使用いただくと、成分が浸透しやすい状態になります。同じReju:Nラインの製品との組み合わせや、他の保湿アイテムとの併用も問題ありません。"}},',
         '{"@type":"Question","name":"他のスキンケアと一緒に使えますか？","acceptedAnswer":{"@type":"Answer","text":"化粧水などで肌を整えた後に使用いただくと、成分が肌になじみやすい状態になります。同じReju:Nラインの製品との組み合わせや、他の保湿アイテムとの併用も問題ありません。"}},'),
        ('<p class="faq-answer">化粧水などで肌を整えた後に使用いただくと、成分が浸透しやすい状態になります。同じReju:Nラインの製品との組み合わせや、他の保湿アイテムとの併用も問題ありません。</p>',
         '<p class="faq-answer">化粧水などで肌を整えた後に使用いただくと、成分が肌になじみやすい状態になります。同じReju:Nラインの製品との組み合わせや、他の保湿アイテムとの併用も問題ありません。</p>'),
    ],
    "products/curlyshyll-repair-ampoule.html": [
        ('{"@type":"Question","name":"どのくらいの頻度で使えばいいですか？","acceptedAnswer":{"@type":"Answer","text":"毎日の使用が推奨です。シャンプー後の濡れた髪に使用し、洗い流さずにそのまま乾かします。毎日続けることで高濃度タンパク質成分が髪に蓄積され、効果を実感しやすくなります。"}},',
         '{"@type":"Question","name":"どのくらいの頻度で使えばいいですか？","acceptedAnswer":{"@type":"Answer","text":"毎日の使用が推奨です。シャンプー後の濡れた髪に使用し、洗い流さずにそのまま乾かします。毎日続けることで高濃度タンパク質成分が髪に蓄積され、使用感を感じやすくなります。"}},'),
        ('<p class="faq-answer">毎日の使用が推奨です。シャンプー後の濡れた髪に使用し、洗い流さずにそのまま乾かします。毎日続けることで高濃度タンパク質成分が髪に蓄積され、効果を実感しやすくなります。</p>',
         '<p class="faq-answer">毎日の使用が推奨です。シャンプー後の濡れた髪に使用し、洗い流さずにそのまま乾かします。毎日続けることで高濃度タンパク質成分が髪に蓄積され、使用感を感じやすくなります。</p>'),
    ],
}

for path, pairs in FIXES.items():
    with open(path, encoding='utf-8') as f:
        text = f.read()
    errors = []
    for old, new in pairs:
        if old not in text:
            errors.append(old[:50])
            continue
        text = text.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'{path}: エラー{len(errors)}件')
    for e in errors:
        print(f'  NOT FOUND: {e}')
