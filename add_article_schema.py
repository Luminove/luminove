# -*- coding: utf-8 -*-
"""
成分ページ5本にArticle構造化データを追加
"""
import re, json

PAGES = {
    "ingredients/glutathione.html": {
        "headline": "グルタチオンとは？美容点滴の主成分が韓国コスメに革命を起こす理由",
        "image": "https://www.luminove.online/images/product-cleanser.webp",
    },
    "ingredients/pdrn.html": {
        "headline": "PDRNとは？サーモンDNA由来成分がスキンケアにもたらす可能性",
        "image": "https://www.luminove.online/images/product-rejun-cream.webp",
    },
    "ingredients/rg3.html": {
        "headline": "RG3（ジンセノサイドRG3）とは？高麗人参の希少成分とエイジングケア",
        "image": "https://www.luminove.online/images/product-rg3-serum.webp",
    },
    "ingredients/nmn.html": {
        "headline": "NMNとは？年齢に応じたケアで注目される成分",
        "image": "https://www.luminove.online/images/product-rejun-cream.webp",
    },
    "ingredients/nano-collagen.html": {
        "headline": "ナノコラーゲン（300Da）とは？韓国スキンケアで注目の低分子コラーゲン",
        "image": "https://www.luminove.online/images/product-skin.webp",
    },
}

for path, info in PAGES.items():
    with open(path, encoding='utf-8') as f:
        text = f.read()

    # meta descriptionを取得
    m = re.search(r'<meta name="description" content="(.*?)" */?>', text)
    desc = m.group(1) if m else info['headline']

    # canonical URLを取得
    m2 = re.search(r'<link rel="canonical" href="(.*?)" */?>', text)
    url = m2.group(1) if m2 else f"https://www.luminove.online/{path}"

    article_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": info['headline'],
        "description": desc,
        "url": url,
        "image": info['image'],
        "publisher": {"@type": "Organization", "name": "LUMINOVE", "url": "https://www.luminove.online"},
        "datePublished": "2026-06-17",
        "dateModified": "2026-06-22"
    }, ensure_ascii=False, indent=2)

    marker = '  <!-- JSON-LD: BreadcrumbList -->'
    if marker not in text:
        print(f'  MARKER NOT FOUND: {path}')
        continue
    if '"@type": "Article"' in text or '"@type":"Article"' in text:
        print(f'  既にArticleあり: {path}')
        continue

    insertion = f'  <!-- JSON-LD: Article -->\n  <script type="application/ld+json">\n  {article_jsonld}\n  </script>\n\n{marker}'
    new_text = text.replace(marker, insertion, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f'  Article schema追加: {path}')

print('\n=== 検証 ===')
import glob
for path in sorted(glob.glob('ingredients/*.html')):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.DOTALL)
    types = []
    for s in scripts:
        try:
            d = json.loads(s)
            types.append(d.get('@type'))
        except Exception as e:
            print(f'  JSON ERROR {path}: {e}')
    print(f'  {path}: {types}')
