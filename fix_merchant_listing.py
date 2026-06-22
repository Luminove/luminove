# -*- coding: utf-8 -*-
"""
Google Search Console「販売者のリスティング」警告対応
全Offerに shippingDetails / hasMerchantReturnPolicy を追加

配送料: 900円（10,000円以上で送料無料）
※北海道・沖縄は1,400円だが、schema.orgには地域別条件分岐の標準プロパティがないため
  基本配送料(900円)+全国一律フラグで表現。実際の地域差は決済画面に依存。
返品: 未開封・不良品のみ返品可
"""
import json, re, os, glob

SHIPPING_DETAILS = {
    "@type": "OfferShippingDetails",
    "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "900",
        "currency": "JPY"
    },
    "shippingDestination": {
        "@type": "DefinedRegion",
        "addressCountry": "JP"
    },
    "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {
            "@type": "QuantitativeValue",
            "minValue": 1,
            "maxValue": 3,
            "unitCode": "DAY"
        },
        "transitTime": {
            "@type": "QuantitativeValue",
            "minValue": 1,
            "maxValue": 4,
            "unitCode": "DAY"
        }
    }
}

RETURN_POLICY = {
    "@type": "MerchantReturnPolicy",
    "applicableCountry": "JP",
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 8,
    "returnMethod": "https://schema.org/ReturnByMail",
    "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
    "returnPolicySeasonalOverride": []
}
# returnPolicySeasonalOverride不要なので削除
del RETURN_POLICY["returnPolicySeasonalOverride"]


def patch_offer(offer):
    """Offerオブジェクトに shippingDetails / hasMerchantReturnPolicy を追加"""
    if isinstance(offer, list):
        for o in offer:
            patch_offer(o)
        return
    if not isinstance(offer, dict):
        return
    if offer.get('@type') == 'Offer':
        if 'shippingDetails' not in offer:
            offer['shippingDetails'] = SHIPPING_DETAILS
        if 'hasMerchantReturnPolicy' not in offer:
            offer['hasMerchantReturnPolicy'] = RETURN_POLICY


def walk_and_patch(node):
    """JSONツリーを再帰的に走査し、offersキーを見つけて修正"""
    changed = False
    if isinstance(node, dict):
        if 'offers' in node:
            before = json.dumps(node['offers'], sort_keys=True)
            patch_offer(node['offers'])
            after = json.dumps(node['offers'], sort_keys=True)
            if before != after:
                changed = True
        for v in node.values():
            if walk_and_patch(v):
                changed = True
    elif isinstance(node, list):
        for item in node:
            if walk_and_patch(item):
                changed = True
    return changed


def process_file(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL))
    new_html = html
    total_changed = 0

    for m in scripts:
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue

        if walk_and_patch(data):
            total_changed += 1
            new_json = json.dumps(data, ensure_ascii=False, indent=2)
            new_script = f'<script type="application/ld+json">\n  {new_json}\n  </script>'
            new_html = new_html.replace(m.group(0), new_script, 1)

    if total_changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
    return total_changed


# ============================================================
print('=== index.html ===')
n = process_file('index.html')
print(f'  修正ブロック数: {n}')

print('\n=== products/*.html ===')
for path in sorted(glob.glob('products/*.html')):
    n = process_file(path)
    print(f'  {os.path.basename(path)}: 修正ブロック数={n}')

# ============================================================
# 検証
# ============================================================
print('\n=== 検証 ===')

def count_offers(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    total, with_ship, with_return = 0, 0, 0

    def scan(node):
        nonlocal total, with_ship, with_return
        if isinstance(node, dict):
            if node.get('@type') == 'Offer':
                total += 1
                if 'shippingDetails' in node:
                    with_ship += 1
                if 'hasMerchantReturnPolicy' in node:
                    with_return += 1
            for v in node.values():
                scan(v)
        elif isinstance(node, list):
            for item in node:
                scan(item)

    for s in scripts:
        try:
            d = json.loads(s)
        except:
            continue
        scan(d)
    return total, with_ship, with_return

total_all, ship_all, return_all = 0, 0, 0
for path in ['index.html'] + sorted(glob.glob('products/*.html')):
    t, s, r = count_offers(path)
    total_all += t
    ship_all += s
    return_all += r
    print(f'  {path}: Offer={t}, shippingDetails={s}, hasMerchantReturnPolicy={r}')

print(f'\n合計: Offer={total_all}, shippingDetails={ship_all}, hasMerchantReturnPolicy={return_all}')
print('\n=== 完了 ===')
