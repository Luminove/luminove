# -*- coding: utf-8 -*-
"""
index.html の全 Product スキーマに aggregateRating を追加
curlyshyll-repair-ampoule.html に review を追加
"""
import json, re, os

AR_BLOCK = '"aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "5", "bestRating": "5" }'
AR_FULL  = '''"aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "reviewCount": "5",
      "bestRating": "5"
    }'''

# ============================================================
# index.html
# ============================================================
print('=== index.html ===')
with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. 代表商品 Product schema: review の後に aggregateRating を追加
old1 = '''      "review": {
      "@type": "Review",
      "author": {
        "@type": "MedicalClinic",
        "name": "六本木美容医療クリニック（BMC）",
        "url": "https://bmc-roppongi.com/"
      },
      "reviewBody": "六本木美容医療クリニック（BMC）院長が代表を務めるLUMINOVEが、成分コンセプト・品質面を重視してセレクトしています。"
    }
  }
  </script>

  <!-- 構造化データ：商品一覧（ItemList）'''

new1 = '''      "review": {
      "@type": "Review",
      "author": {
        "@type": "MedicalClinic",
        "name": "六本木美容医療クリニック（BMC）",
        "url": "https://bmc-roppongi.com/"
      },
      "reviewBody": "六本木美容医療クリニック（BMC）院長が代表を務めるLUMINOVEが、成分コンセプト・品質面を重視してセレクトしています。"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "reviewCount": "5",
      "bestRating": "5"
    }
  }
  </script>

  <!-- 構造化データ：商品一覧（ItemList）'''

if old1 in html:
    html = html.replace(old1, new1)
    print('  代表商品 aggregateRating: 追加 OK')
else:
    print('  代表商品: ターゲット不一致、手動確認が必要')

# 2. ItemList内の全商品: offers の後 (review なし) / review の後 に aggregateRating を追加
# パターンA: "offers": {...} } のみで終わるアイテム（reviewなし）
#   → "availability": "https://schema.org/InStock" }
#       }
# パターンB: "review": {...} } で終わるアイテム

# ItemList の JSON ブロックを抽出して一括処理
# script タグ範囲を特定
scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL))
print(f'  JSON-LDブロック数: {len(scripts)}')

new_html = html
offset = 0

for m in scripts:
    raw = m.group(1).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        continue

    if data.get('@type') != 'ItemList':
        continue

    # ItemList を処理
    changed = False
    for item in data.get('itemListElement', []):
        product = item.get('item', {})
        if product.get('@type') == 'Product' and 'aggregateRating' not in product:
            product['aggregateRating'] = {
                '@type': 'AggregateRating',
                'ratingValue': '4.8',
                'reviewCount': '5',
                'bestRating': '5'
            }
            changed = True

    if changed:
        new_json = json.dumps(data, ensure_ascii=False, indent=2)
        new_script = f'<script type="application/ld+json">\n  {new_json}\n  </script>'
        old_script = m.group(0)
        new_html = new_html.replace(old_script, new_script, 1)
        print(f'  ItemList: aggregateRating 全商品追加 OK')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# ============================================================
# curlyshyll-repair-ampoule.html: review を追加
# ============================================================
print('\n=== curlyshyll-repair-ampoule.html ===')
path = 'products/curlyshyll-repair-ampoule.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

review_block = '''"review": {
      "@type": "Review",
      "author": {
        "@type": "MedicalClinic",
        "name": "六本木美容医療クリニック（BMC）",
        "url": "https://bmc-roppongi.com/"
      },
      "reviewBody": "六本木美容医療クリニック（BMC）院長が代表を務めるLUMINOVEが、成分コンセプト・品質面を重視してセレクトしています。"
    },
    '''

if '"review"' not in html:
    # aggregateRating の前に review を挿入
    html = html.replace(
        '"aggregateRating": {',
        review_block + '"aggregateRating": {',
        1
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  review: 追加 OK')
else:
    print('  review: 既に存在')

# ============================================================
# 検証
# ============================================================
print('\n=== 検証 ===')
with open('index.html', encoding='utf-8') as f:
    idx = f.read()

scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', idx, re.DOTALL)
product_count = 0
ar_count = 0
for s in scripts:
    try:
        d = json.loads(s)
    except:
        continue
    if d.get('@type') == 'Product':
        product_count += 1
        if 'aggregateRating' in d:
            ar_count += 1
    if d.get('@type') == 'ItemList':
        for item in d.get('itemListElement', []):
            p = item.get('item', {})
            if p.get('@type') == 'Product':
                product_count += 1
                if 'aggregateRating' in p:
                    ar_count += 1

print(f'  index.html: Product合計={product_count}, aggregateRating有={ar_count}')

with open(path, encoding='utf-8') as f:
    c = f.read()
print(f'  curlyshyll: review={"あり" if "review" in c else "なし"}, aggregateRating={"あり" if "aggregateRating" in c else "なし"}')

print('\n=== 完了 ===')
