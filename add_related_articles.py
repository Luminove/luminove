# -*- coding: utf-8 -*-
"""
全商品ページに「関連記事」リンクボックスを追加
"""
import re

ARTICLE_MAP = {
    'glucola-serum.html': [
        ('/blog/glutathione-serum.html', 'グルタチオン美容液の選び方'),
        ('/blog/glutathione-what-is.html', 'グルタチオンとは？'),
    ],
    'glucola-skin.html': [
        ('/blog/glutathione-skincare.html', 'グルタチオン化粧品とは？'),
        ('/blog/nano-collagen.html', 'ナノコラーゲンとは？'),
    ],
    'glucola-cleansing-foam.html': [
        ('/blog/glutathione-skincare.html', 'グルタチオン化粧品とは？'),
        ('/blog/korean-skincare-routine.html', '韓国スキンケアの順番とは？'),
    ],
    'glucola-peeling-pack2.html': [
        ('/blog/peeling-pack-how-to-use.html', 'ピールオフパックの使い方'),
        ('/blog/glutathione-skincare.html', 'グルタチオン化粧品とは？'),
    ],
    'glucola-suncream.html': [
        ('/blog/korean-sunscreen.html', '韓国日焼け止めの選び方'),
    ],
    'rejun-pdrn-cream.html': [
        ('/blog/pdrn-skincare.html', 'PDRN化粧品とは？'),
        ('/blog/pdrn-nmn-cream.html', 'PDRN×NMNクリームとは？'),
        ('/blog/pdrn-what-is.html', 'PDRNとは？'),
    ],
    'rg3-vital-ampoule.html': [
        ('/blog/korean-skincare-recommended.html', '韓国スキンケアおすすめ2026'),
    ],
    'rg3-vital-cream.html': [
        ('/blog/korean-skincare-recommended.html', '韓国スキンケアおすすめ2026'),
    ],
    'celviv-bio-kit.html': [
        ('/blog/pdrn-skincare.html', 'PDRN化粧品とは？'),
    ],
    'curlyshyll-repair-ampoule.html': [
        ('/blog/korean-hair-ampoule.html', '韓国ヘアアンプルとは？'),
    ],
}

BOX_TPL = '''
  <div style="max-width:800px;margin:0 auto 2rem;padding:0 5%">
    <div style="background:var(--green-mist);border-radius:12px;padding:1.2rem 1.5rem">
      <p style="font-size:.78rem;color:var(--text-light);letter-spacing:.1em;margin-bottom:.6rem">関連記事</p>
      <div style="display:flex;flex-wrap:wrap;gap:.6rem">
{links}
      </div>
    </div>
  </div>
'''
LINK_TPL = '        <a href="{url}" style="display:inline-block;font-size:.82rem;font-weight:500;color:var(--green-deep);background:#fff;border:1px solid var(--green-pale);border-radius:50px;padding:.35rem 1rem;text-decoration:none;">{name} →</a>'

for fname, articles in ARTICLE_MAP.items():
    path = f'products/{fname}'
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if '関連記事' in html:
        print(f'  SKIP(already added): {fname}')
        continue

    links_html = '\n'.join(LINK_TPL.format(url=u, name=n) for u, n in articles)
    box = BOX_TPL.format(links=links_html)

    # 「この商品の主要成分をもっと詳しく」ボックスの直後 / なければFAQセクション直前に挿入
    marker_ingredient_box_end = re.search(r'(この商品の主要成分をもっと詳しく.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
    if marker_ingredient_box_end:
        insert_pos = marker_ingredient_box_end.end()
        html = html[:insert_pos] + box + html[insert_pos:]
    elif '<section class="faq-section">' in html:
        html = html.replace('<section class="faq-section">', box + '  <section class="faq-section">', 1)
    else:
        print(f'  WARN(no insertion point): {fname}')
        continue

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Updated: {fname}')

print('\n=== 完了 ===')
