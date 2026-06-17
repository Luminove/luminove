# -*- coding: utf-8 -*-
"""
内部リンク強化 + ブログ記事3本作成
【1】index.html: PDRN/RG3/NMN 成分カード追加
【2】商品ページ → 成分ページ リンク追加
【3】成分ページ → 商品ページ 不足リンク補完
【4】ブログ記事3本作成
"""
import os, re

# ============================================================
# 【1】index.html: PDRN / RG3 / NMN 成分カード追加
# ============================================================
print('=== 【1】index.html 成分カード追加 ===')

with open('index.html', encoding='utf-8') as f:
    idx = f.read()

new_cards = '''      <div class="ingr-card reveal" style="transition-delay:.32s">
        <div class="ingr-icon" style="color:var(--green-mid)"><svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4"/></svg></div>
        <h3 class="ingr-name">PDRN</h3>
        <p class="ingr-text">サーモンのDNA由来成分。再生医療でも研究される注目成分で、肌のリズムを整える「28日ルーティンケア」成分として韓国コスメで急速に普及。</p>
        <a href="/ingredients/pdrn.html" style="font-size:.78rem;color:var(--green-mid);letter-spacing:.05em;">詳しく見る →</a>
      </div>
      <div class="ingr-card reveal" style="transition-delay:.40s">
        <div class="ingr-icon" style="color:var(--green-mid)"><svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2z"/><path d="M12 8v4l3 3"/></svg></div>
        <h3 class="ingr-name">RG3（高麗人参）</h3>
        <p class="ingr-text">高麗人参全体のわずか0.001%以下しか含まれない希少サポニン成分。エイジングケア・ハリ・透明感にアプローチするプレミアム成分。</p>
        <a href="/ingredients/rg3.html" style="font-size:.78rem;color:var(--green-mid);letter-spacing:.05em;">詳しく見る →</a>
      </div>
      <div class="ingr-card reveal" style="transition-delay:.48s">
        <div class="ingr-icon" style="color:var(--green-mid)"><svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3M12 18v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M3 12H6M18 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/></svg></div>
        <h3 class="ingr-name">NMN</h3>
        <p class="ingr-text">細胞エネルギー（NAD+）の前駆体として注目されるアンチエイジング成分。PDRNとの組み合わせで内側からのハリ・活力ケアに。</p>
        <a href="/ingredients/nmn.html" style="font-size:.78rem;color:var(--green-mid);letter-spacing:.05em;">詳しく見る →</a>
      </div>'''

# 洗顔にもコラーゲンカードの後に追加
target = '        <h3 class="ingr-name">洗顔にもコラーゲン</h3>\n        <p class="ingr-text">洗い流すクレンジングフォームにも5%のコラーゲンを高配合。洗顔後もうるおいが角層に残り、つっぱり感ゼロの心地よい洗い上がりを実現。</p>\n      </div>\n    </div>\n  </section>'

if target in idx:
    idx = idx.replace(
        target,
        '        <h3 class="ingr-name">洗顔にもコラーゲン</h3>\n        <p class="ingr-text">洗い流すクレンジングフォームにも5%のコラーゲンを高配合。洗顔後もうるおいが角層に残り、つっぱり感ゼロの心地よい洗い上がりを実現。</p>\n      </div>\n' + new_cards + '\n    </div>\n  </section>'
    )
    print('  成分カード3件追加: OK')
else:
    print('  ターゲット不一致')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

# ============================================================
# 【2】商品ページ → 成分ページ リンク追加
# 各商品の「よくある質問」の直前にリンクボックスを挿入
# ============================================================
print('\n=== 【2】商品ページ → 成分ページ リンク追加 ===')

# 商品 → 成分ページのマッピング
product_ingredient_map = {
    'glucola-serum.html':         [('グルタチオン', '/ingredients/glutathione.html')],
    'glucola-skin.html':          [('グルタチオン', '/ingredients/glutathione.html')],
    'glucola-cleansing-foam.html':[('グルタチオン', '/ingredients/glutathione.html')],
    'glucola-peeling-pack2.html': [('グルタチオン', '/ingredients/glutathione.html')],
    'glucola-suncream.html':      [('グルタチオン', '/ingredients/glutathione.html')],
    'rejun-pdrn-cream.html':      [('PDRN', '/ingredients/pdrn.html'), ('NMN', '/ingredients/nmn.html')],
    'rg3-vital-ampoule.html':     [('RG3（高麗人参）', '/ingredients/rg3.html')],
    'rg3-vital-cream.html':       [('RG3（高麗人参）', '/ingredients/rg3.html')],
    'celviv-bio-kit.html':        [('PDRN', '/ingredients/pdrn.html'), ('NMN', '/ingredients/nmn.html')],
    'curlyshyll-repair-ampoule.html': [],  # 成分ページなし
}

ingr_box_tpl = '''
  <div style="max-width:800px;margin:0 auto 1rem;padding:0 5%">
    <div style="background:var(--green-mist);border-radius:12px;padding:1.2rem 1.5rem">
      <p style="font-size:.78rem;color:var(--text-light);letter-spacing:.1em;margin-bottom:.6rem">この商品の主要成分をもっと詳しく</p>
      <div style="display:flex;flex-wrap:wrap;gap:.6rem">
{links}
      </div>
    </div>
  </div>
'''
ingr_link_tpl = '        <a href="{url}" style="display:inline-block;font-size:.82rem;font-weight:500;color:var(--green-deep);background:#fff;border:1px solid var(--green-pale);border-radius:50px;padding:.35rem 1rem;text-decoration:none;">{name}とは？ →</a>'

for fname, ingrs in product_ingredient_map.items():
    if not ingrs:
        continue
    path = 'products/' + fname
    if not os.path.isfile(path):
        print(f'  SKIP(not found): {fname}')
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()
    marker = '  <section class="faq-section">'
    if marker not in html:
        print(f'  SKIP(no faq marker): {fname}')
        continue
    # 既に追加済みならスキップ
    if 'この商品の主要成分をもっと詳しく' in html:
        print(f'  SKIP(already added): {fname}')
        continue
    links_html = '\n'.join(ingr_link_tpl.format(url=u, name=n) for n, u in ingrs)
    box = ingr_box_tpl.format(links=links_html)
    html = html.replace(marker, box + marker)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Updated: {fname}')

# ============================================================
# 【3】成分ページ → 商品ページ 不足リンク補完
# ============================================================
print('\n=== 【3】成分ページ → 商品ページ リンク補完 ===')

# glutathione: serum / skin / peeling-pack2 が未追加
# pdrn: 現状 rejun + celviv → OK、cleansing-foam は除く（グルタチオン配合でPDRN配合ではない）
# rg3: ampoule / cream が未追加
# nmn: rejun + celviv → 確認

ingr_product_fixes = {
    'ingredients/glutathione.html': {
        'old': '<a href="/products/glucola-cleansing-foam.html" class="related-card">',
        'add_before': '''      <a href="/products/glucola-serum.html" class="related-card">
        <img src="/images/product-serum.webp" alt="グルコラ セラム（美容液）" loading="lazy" />
        <p>グルコラ<br>セラム（美容液）</p>
      </a>
      <a href="/products/glucola-skin.html" class="related-card">
        <img src="/images/product-skin.webp" alt="グルコラ スキン（化粧水）" loading="lazy" />
        <p>グルコラ<br>スキン（化粧水）</p>
      </a>
      '''
    },
    'ingredients/rg3.html': {
        'find_related': True,
    },
}

# glutathione.html: セラム・スキンを related-grid に追加
path = 'ingredients/glutathione.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

if '/products/glucola-serum.html' not in html:
    old = '      <a href="/products/glucola-cleansing-foam.html" class="related-card">'
    new = '''      <a href="/products/glucola-serum.html" class="related-card">
        <img src="/images/product-serum.webp" alt="グルコラ セラム（美容液）" loading="lazy" />
        <p>グルコラ セラム<br>（美容液）</p>
      </a>
      <a href="/products/glucola-skin.html" class="related-card">
        <img src="/images/product-skin.webp" alt="グルコラ スキン（化粧水）" loading="lazy" />
        <p>グルコラ スキン<br>（化粧水）</p>
      </a>
      <a href="/products/glucola-cleansing-foam.html" class="related-card">'''
    if old in html:
        html = html.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  {path}: セラム・スキン追加 OK')
else:
    print(f'  {path}: 既に追加済み')

# rg3.html: ampoule / cream を追加
path = 'ingredients/rg3.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

if '/products/rg3-vital-ampoule.html' not in html:
    # related-grid を探して商品カードを追加
    # 既存の商品カードの前に挿入
    old_marker = '<div class="related-grid">'
    new_grid_content = '''<div class="related-grid">
      <a href="/products/rg3-vital-ampoule.html" class="related-card">
        <img src="/images/product-rg3-serum.webp" alt="クイーンズ RG3 モイスチャーセラム" loading="lazy" />
        <p>クイーンズ RG3<br>モイスチャーセラム</p>
      </a>
      <a href="/products/rg3-vital-cream.html" class="related-card">
        <img src="/images/product-rg4-cream.webp" alt="クイーンズ RG3 モイスチャークリーム" loading="lazy" />
        <p>クイーンズ RG3<br>モイスチャークリーム</p>
      </a>'''
    # 最初のrelated-gridだけ置換
    if old_marker in html:
        html = html.replace(old_marker, new_grid_content, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  {path}: ampoule・cream追加 OK')
else:
    print(f'  {path}: 既に追加済み')

# nmn.html: 確認のみ
path = 'ingredients/nmn.html'
with open(path, encoding='utf-8') as f:
    html = f.read()
prod_links = re.findall(r'products/[a-z-]+\.html', html)
print(f'  nmn.html 現在のリンク: {list(set(prod_links))}')

# pdrn.html: 確認のみ
path = 'ingredients/pdrn.html'
with open(path, encoding='utf-8') as f:
    html = f.read()
prod_links = re.findall(r'products/[a-z-]+\.html', html)
print(f'  pdrn.html 現在のリンク: {list(set(prod_links))}')

# ============================================================
# 【4】ブログ記事3本作成
# ============================================================
print('\n=== 【4】ブログ記事作成 ===')

os.makedirs('blog', exist_ok=True)

BLOG_CSS = '''
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --green-deep: #2d4a3e; --green-mid: #4a7c67; --green-light: #7db89a;
      --green-pale: #d4ede4; --green-mist: #f0f8f4; --cream: #faf8f3;
      --warm-white: #fff; --text-dark: #1a2a23; --text-mid: #4a5c54;
      --text-light: #8a9e96; --gold: #c8a96a;
      --font-serif: 'Cormorant Garamond','Hiragino Mincho ProN',serif;
      --font-sans: 'Noto Sans JP',sans-serif;
      --radius: 12px; --shadow: 0 8px 40px rgba(45,74,62,.10);
      --transition: .35s cubic-bezier(.4,0,.2,1);
    }
    html { scroll-behavior: smooth; }
    body { font-family: var(--font-sans); color: var(--text-dark); background: var(--cream); line-height: 1.8; overflow-x: hidden; }
    a { color: inherit; text-decoration: none; }
    img { display: block; width: 100%; }
    #header { position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; padding: 0 5%; display: flex; align-items: center; justify-content: space-between; height: 72px; background: rgba(250,248,243,.92); backdrop-filter: blur(8px); box-shadow: 0 1px 12px rgba(45,74,62,.06); }
    .logo { font-family: var(--font-serif); font-size: 1.75rem; font-weight: 500; letter-spacing: .2em; color: var(--green-deep); }
    .logo span { color: var(--green-mid); }
    nav { display: flex; gap: 2.5rem; align-items: center; }
    nav a { font-size: .8rem; letter-spacing: .15em; font-weight: 500; color: var(--text-mid); transition: color var(--transition); }
    nav a:hover { color: var(--green-deep); }
    .btn-nav { background: var(--green-deep); color: #fff !important; padding: .55rem 1.5rem; border-radius: 50px; font-size: .78rem; }
    .hamburger { display: none; cursor: pointer; flex-direction: column; gap: 5px; padding: 4px; }
    .hamburger span { display: block; width: 24px; height: 2px; background: var(--green-deep); border-radius: 2px; }
    .mobile-nav { display: none; position: fixed; inset: 0; z-index: 1001; background: var(--cream); flex-direction: column; align-items: center; justify-content: center; gap: 2.5rem; }
    .mobile-nav.open { display: flex; }
    .mobile-nav a { font-family: var(--font-serif); font-size: 1.75rem; color: var(--green-deep); }
    .close-btn { position: absolute; top: 1.5rem; right: 5%; font-size: 1.75rem; cursor: pointer; color: var(--green-deep); background: none; border: none; }
    .btn-primary { display: inline-block; background: var(--green-deep); color: #fff; padding: .9rem 2.4rem; border-radius: 50px; font-size: .85rem; letter-spacing: .12em; font-weight: 500; text-align: center; transition: background var(--transition), transform var(--transition); }
    .btn-primary:hover { background: var(--green-mid); transform: translateY(-2px); }
    .btn-outline { display: inline-block; border: 1.5px solid var(--green-deep); color: var(--green-deep); padding: .9rem 2.4rem; border-radius: 50px; font-size: .85rem; letter-spacing: .12em; font-weight: 500; text-align: center; transition: all var(--transition); }
    .btn-outline:hover { background: var(--green-pale); transform: translateY(-2px); }
    .breadcrumb { max-width: 860px; margin: 0 auto; padding: 100px 5% 0; font-size: .75rem; letter-spacing: .05em; color: var(--text-light); }
    .breadcrumb a { color: var(--text-mid); }
    .article-hero { max-width: 860px; margin: 0 auto; padding: 2rem 5% 3rem; }
    .article-tag { display: inline-block; font-size: .72rem; letter-spacing: .2em; font-weight: 500; color: var(--green-mid); background: var(--green-pale); padding: .4rem 1.2rem; border-radius: 50px; margin-bottom: 1.2rem; }
    .article-hero h1 { font-family: var(--font-serif); font-size: clamp(1.8rem,4vw,2.6rem); font-weight: 500; line-height: 1.4; color: var(--green-deep); margin-bottom: 1.2rem; }
    .article-meta { font-size: .78rem; color: var(--text-light); margin-bottom: 2rem; }
    .article-lead { font-size: .95rem; color: var(--text-mid); border-left: 3px solid var(--green-light); padding-left: 1.2rem; margin-bottom: 2rem; line-height: 2; }
    .toc { background: var(--green-mist); border-radius: var(--radius); padding: 1.5rem 1.8rem; margin-bottom: 2.5rem; }
    .toc h2 { font-size: .85rem; letter-spacing: .1em; color: var(--text-dark); margin-bottom: 1rem; }
    .toc ol { padding-left: 1.4rem; }
    .toc li { font-size: .85rem; color: var(--green-mid); margin-bottom: .4rem; }
    .toc a { color: var(--green-mid); text-decoration: underline; }
    .article-body { max-width: 720px; margin: 0 auto; padding: 0 5% 4rem; }
    .article-section { margin-bottom: 3rem; }
    .article-section h2 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 500; color: var(--green-deep); margin-bottom: 1rem; padding-bottom: .6rem; border-bottom: 1px solid var(--green-pale); }
    .article-section h3 { font-size: 1.05rem; font-weight: 600; color: var(--text-dark); margin: 1.5rem 0 .6rem; }
    .article-section p { font-size: .92rem; color: var(--text-mid); margin-bottom: 1rem; line-height: 1.9; }
    .article-section ul, .article-section ol { font-size: .92rem; color: var(--text-mid); margin: 0 0 1rem 1.4rem; line-height: 1.9; }
    .article-section li { margin-bottom: .4rem; }
    .article-section a { color: var(--green-mid); text-decoration: underline; }
    .quote-box { background: var(--green-mist); border-left: 4px solid var(--green-light); border-radius: var(--radius); padding: 1.5rem 1.8rem; margin: 1.5rem 0; }
    .quote-box p { color: var(--text-dark); font-size: .92rem; margin-bottom: 0; }
    .cta-box { text-align: center; background: var(--green-mist); border-radius: var(--radius); padding: 2rem 1.5rem; margin: 2rem 0; }
    .cta-box p { font-size: .92rem; color: var(--text-mid); margin-bottom: 1.2rem; }
    .related-section { max-width: 720px; margin: 0 auto 3rem; padding: 0 5%; }
    .related-section h2 { font-family: var(--font-serif); font-size: 1.4rem; color: var(--green-deep); margin-bottom: 1.5rem; padding-bottom: .5rem; border-bottom: 1px solid var(--green-pale); }
    .related-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; }
    .related-card { display: block; text-align: center; }
    .related-card img { border-radius: var(--radius); margin-bottom: .6rem; aspect-ratio: 1; object-fit: cover; }
    .related-card p { font-size: .82rem; color: var(--text-dark); font-weight: 500; }
    .back-link { text-align: center; margin: 2rem auto 4rem; }
    .faq-section { max-width: 720px; margin: 3rem auto; padding: 0 5%; }
    .faq-section h2 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 500; color: var(--green-deep); margin-bottom: 1.5rem; padding-bottom: .5rem; border-bottom: 1px solid var(--green-pale); }
    .faq-item { border-bottom: 1px solid var(--green-pale); }
    .faq-question { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; cursor: pointer; padding: 1.2rem 0; font-weight: 500; color: var(--text-dark); list-style: none; }
    .faq-question::marker, .faq-question::-webkit-details-marker { display: none; }
    .faq-icon { flex-shrink: 0; width: 24px; height: 24px; border: 1px solid var(--green-mid); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--green-mid); font-size: .9rem; transition: transform var(--transition); }
    details[open] .faq-icon { transform: rotate(45deg); }
    .faq-answer { padding: .25rem 0 1.2rem; color: var(--text-mid); line-height: 1.9; font-size: .92rem; }
    footer { background: var(--text-dark); color: rgba(255,255,255,.65); padding: 60px 5% 30px; }
    .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr 1.8fr; gap: 3rem; margin-bottom: 3rem; }
    .footer-brand .logo { color: #fff; margin-bottom: 1rem; }
    .footer-brand p { font-size: .83rem; line-height: 1.85; max-width: 260px; }
    .footer-col h4 { font-size: .78rem; letter-spacing: .18em; font-weight: 500; color: #fff; margin-bottom: 1.25rem; }
    .footer-col ul { list-style: none; display: flex; flex-direction: column; gap: .6rem; }
    .footer-col li a { font-size: .83rem; transition: color var(--transition); }
    .footer-col li a:hover { color: var(--green-light); }
    .footer-bottom { border-top: 1px solid rgba(255,255,255,.1); padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: .5rem; }
    .footer-bottom p, .footer-bottom a { font-size: .78rem; }
    .footer-bottom a { margin-left: 1.5rem; }
    @media (max-width: 1024px) { .footer-grid { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 768px) { nav { display: none; } .hamburger { display: flex; } .footer-grid { grid-template-columns: 1fr; gap: 2rem; } .related-grid { grid-template-columns: repeat(2,1fr); } .article-section h2 { font-size: 1.25rem; } }
'''

BLOG_HEADER = '''  <header id="header">
    <a href="/" class="logo">LUMI<span>NOVE</span></a>
    <nav>
      <a href="/#products">製品</a>
      <a href="/#brands">取扱ブランド</a>
      <a href="/#ingredients">成分</a>
      <a href="/#reviews">レビュー</a>
      <a href="https://luminove.stores.jp/" target="_blank" rel="noopener" class="btn-nav">SHOP NOW</a>
    </nav>
    <button class="hamburger" id="hamburger" aria-label="メニュー"><span></span><span></span><span></span></button>
  </header>
  <nav class="mobile-nav" id="mobileNav">
    <button class="close-btn" id="closeNav">✕</button>
    <a href="/" class="mobile-link">TOP</a>
    <a href="/#products" class="mobile-link">製品</a>
    <a href="/#ingredients" class="mobile-link">成分</a>
    <a href="https://luminove.stores.jp/" target="_blank" rel="noopener" class="btn-primary mobile-link">SHOP NOW</a>
  </nav>'''

BLOG_FOOTER = '''  <footer>
    <div class="footer-grid">
      <div class="footer-brand">
        <span class="logo">LUMI<span style="color:var(--green-light)">NOVE</span></span>
        <p>光と愛を纏う肌へ。六本木BMC院長が代表を務め、品質面を重視して商品選定に携わる韓国コスメセレクトショップ。</p>
      </div>
      <div class="footer-col">
        <h4>Products</h4>
        <ul>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">スキンケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">ヘアケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">ハンドケア</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/doctor/">LUMINOVEについて</a></li>
          <li><a href="mailto:info@luminove.online">お問い合わせ</a></li>
          <li><a href="https://luminove.stores.jp/tokushoho" target="_blank" rel="noopener">特定商取引法</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>会社概要</h4>
        <address style="font-style:normal;font-size:.78rem;line-height:2;color:rgba(255,255,255,.55)">
          <span style="display:block;color:rgba(255,255,255,.8);font-weight:500;margin-bottom:.25rem">株式会社ルミノーブ</span>
          〒102-0094 東京都千代田区紀尾井町4番1号<br>ニューオータニガーデンコート28階
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 LUMINOVE. All rights reserved.</p>
      <a href="https://luminove.stores.jp/privacy_policy" target="_blank" rel="noopener">プライバシーポリシー</a>
      <a href="https://luminove.stores.jp/tokushoho" target="_blank" rel="noopener">特定商取引法</a>
    </div>
  </footer>
  <script>
    document.getElementById('hamburger').addEventListener('click', () => { document.getElementById('mobileNav').classList.toggle('open'); });
    document.getElementById('closeNav').addEventListener('click', () => { document.getElementById('mobileNav').classList.remove('open'); });
    document.querySelectorAll('.mobile-link').forEach(el => { el.addEventListener('click', () => { document.getElementById('mobileNav').classList.remove('open'); }); });
  </script>'''

# ---- ブログ記事①: グルタチオンとは？ ----
blog1 = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ECTSQMJ4ME"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ECTSQMJ4ME');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <title>グルタチオンとは？美容点滴の主成分と韓国コスメでの活用法｜LUMINOVE</title>
  <meta name="description" content="グルタチオンとは何か、なぜ美容点滴（白玉注射）の主成分として注目されるのかを徹底解説。透明感・くすみ改善・抗酸化の仕組みと、韓国スキンケアでの高濃度配合の意味をわかりやすく紹介します。" />
  <link rel="canonical" href="https://www.luminove.online/blog/glutathione-what-is.html" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="グルタチオンとは？美容点滴の主成分と韓国コスメでの活用法｜LUMINOVE" />
  <meta property="og:description" content="グルタチオンとは何か、なぜ美容点滴（白玉注射）の主成分として注目されるのかを徹底解説。" />
  <meta property="og:url" content="https://www.luminove.online/blog/glutathione-what-is.html" />
  <meta property="og:image" content="https://www.luminove.online/images/product-serum.webp" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "グルタチオンとは？美容点滴の主成分と韓国コスメでの活用法",
    "description": "グルタチオンとは何か、なぜ美容点滴（白玉注射）の主成分として注目されるのかを徹底解説。",
    "url": "https://www.luminove.online/blog/glutathione-what-is.html",
    "publisher": {{"@type":"Organization","name":"LUMINOVE","url":"https://www.luminove.online"}},
    "datePublished": "2026-06-17",
    "dateModified": "2026-06-17"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"TOP","item":"https://www.luminove.online/"}},
      {{"@type":"ListItem","position":2,"name":"ブログ","item":"https://www.luminove.online/blog/"}},
      {{"@type":"ListItem","position":3,"name":"グルタチオンとは？","item":"https://www.luminove.online/blog/glutathione-what-is.html"}}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{"@type":"Question","name":"グルタチオンとは何ですか？","acceptedAnswer":{{"@type":"Answer","text":"グルタチオンはグルタミン酸・システイン・グリシンの3つのアミノ酸が結合したトリペプチドで、人体に自然に存在する成分です。強力な抗酸化作用を持ち、美容点滴（白玉注射）の主成分として広く知られています。"}}}},
      {{"@type":"Question","name":"グルタチオンはなぜ透明感に効果があるのですか？","acceptedAnswer":{{"@type":"Answer","text":"グルタチオンはメラニン生成に関わるチロシナーゼ酵素の活性を抑えることで、メラニン量の調整にアプローチします。また強力な抗酸化作用により活性酸素を除去し、くすみ原因のひとつである酸化ストレスを抑えます。"}}}},
      {{"@type":"Question","name":"グルタチオン配合のスキンケアは美容点滴と同じ効果がありますか？","acceptedAnswer":{{"@type":"Answer","text":"美容点滴（白玉注射）は静脈投与のため全身への即効性があります。スキンケアは経皮吸収での働きが主となりますが、毎日継続使用できる手軽さが強みです。どちらか一方ではなく補完的に活用することをおすすめします。"}}}},
      {{"@type":"Question","name":"グルタチオン配合スキンケアを選ぶ際のポイントは？","acceptedAnswer":{{"@type":"Answer","text":"配合濃度（ppm表記）を確認しましょう。一般的な配合量は100〜500ppm程度ですが、グルコラ セラムのような高機能製品は30,000ppm（3%）まで配合しているものもあります。配合濃度が高いほど成分量が多くなります。"}}}},
      {{"@type":"Question","name":"グルタチオンの副作用はありますか？","acceptedAnswer":{{"@type":"Answer","text":"グルタチオンは体内に自然に存在する成分で、スキンケアとして使用する場合は一般的に低刺激とされています。ただし高濃度配合製品は初回使用前にパッチテストを実施することをおすすめします。"}}}},
      {{"@type":"Question","name":"毎日使っても大丈夫ですか？","acceptedAnswer":{{"@type":"Answer","text":"はい、グルタチオン配合スキンケアは毎日の朝晩使用に対応した設計の製品がほとんどです。グルタチオンは継続使用により透明感・くすみ改善の実感が得やすくなります。28日間（肌のターンオーバー1サイクル）の継続使用をおすすめします。"}}}}
    ]
  }}
  </script>
  <style>{BLOG_CSS}</style>
</head>
<body>
{BLOG_HEADER}

  <nav class="breadcrumb">
    <a href="/">TOP</a> ＞ <a href="/blog/">ブログ</a> ＞ グルタチオンとは？
  </nav>

  <article class="article-hero">
    <span class="article-tag">成分解説 / グルタチオン</span>
    <h1>グルタチオンとは？<br>美容点滴の主成分と韓国コスメでの活用法</h1>
    <p class="article-meta">2026年6月17日 ｜ LUMINOVE編集部</p>
    <p class="article-lead">「白玉注射」とも呼ばれる美容点滴の主成分として知られるグルタチオン。近年、韓国コスメへの高濃度配合が進み、スキンケアでの日常的な活用が注目されています。本記事ではグルタチオンの仕組み・効果・選び方をわかりやすく解説します。</p>

    <div class="toc">
      <h2>目次</h2>
      <ol>
        <li><a href="#what">グルタチオンとは？基本情報</a></li>
        <li><a href="#how">透明感・くすみ改善の仕組み</a></li>
        <li><a href="#clinic">美容点滴（白玉注射）との関係</a></li>
        <li><a href="#skincare">韓国コスメでの活用 ─ ppm表記の読み方</a></li>
        <li><a href="#choose">グルタチオン配合スキンケアの選び方</a></li>
        <li><a href="#products">LUMINOVEのグルタチオン配合商品</a></li>
        <li><a href="#faq">よくある質問</a></li>
      </ol>
    </div>
  </article>

  <div class="article-body">

    <section class="article-section" id="what">
      <h2>グルタチオンとは？基本情報</h2>
      <p>グルタチオン（Glutathione）は、グルタミン酸・システイン・グリシンの3つのアミノ酸が結合した<strong>トリペプチド</strong>で、人体のほぼすべての細胞に自然に存在している成分です。肝臓で生成され、解毒・抗酸化の中心的な役割を担います。</p>
      <p>年齢とともに体内のグルタチオン量は減少するとされており、これがくすみ・シミ・肌の老化の一因と考えられています。美容の世界では「マスター抗酸化物質」とも呼ばれ、美容点滴（白玉注射）の主成分として広く知られています。</p>
      <div class="quote-box">
        <p>グルタチオンは食品（アスパラガス・アボカド・ほうれん草など）にも含まれていますが、経口摂取では消化酵素によって分解されることが多く、スキンケアや点滴での摂取が美容目的では主流です。</p>
      </div>
    </section>

    <section class="article-section" id="how">
      <h2>透明感・くすみ改善の仕組み</h2>
      <h3>① メラニン生成アプローチ</h3>
      <p>グルタチオンは<strong>チロシナーゼ酵素の活性を抑制</strong>することで、メラニン生成量の調整にアプローチします。メラニンは紫外線や炎症などの刺激で過剰生成されるとシミ・くすみの原因になります。グルタチオンがこの過程に介入することで、透明感のある肌へのアプローチが期待できます。</p>
      <h3>② 強力な抗酸化作用</h3>
      <p>活性酸素（フリーラジカル）は肌の酸化ストレスを引き起こし、くすみ・シミ・老化の促進につながります。グルタチオンは<strong>強力な抗酸化物質</strong>として活性酸素を中和し、酸化ストレスによる肌ダメージを抑えます。</p>
      <h3>③ ビタミンCとの相乗効果</h3>
      <p>グルタチオンはビタミンCの抗酸化作用を再生・強化する働きがあります。両者を組み合わせることで抗酸化・美白アプローチの相乗効果が期待できます。</p>
    </section>

    <section class="article-section" id="clinic">
      <h2>美容点滴（白玉注射）との関係</h2>
      <p>美容クリニックで行われる「白玉注射」は、グルタチオンを高濃度で静脈投与する美容点滴です。静脈投与は消化管を通さず直接血中に入るため、即効性と全身への作用が特徴です。</p>
      <ul>
        <li><strong>美容点滴（白玉注射）：</strong>静脈投与・即効性・全身作用・クリニックで施術</li>
        <li><strong>グルタチオン配合スキンケア：</strong>経皮吸収・毎日継続可能・自宅ケア</li>
      </ul>
      <p>両者は吸収経路が異なりますが、スキンケアは毎日継続できる手軽さが強みです。クリニック施術を補完する日常ケアとしての活用が一般的です。</p>
      <div class="quote-box">
        <p>LUMINOVEでは、美容医療の現場で注目されるグルタチオンを高濃度配合した韓国ブランドを選定しています。グルコラ セラムのグルタチオン30,000ppmは、一般的な配合量の数十倍以上の濃度です。</p>
      </div>
    </section>

    <section class="article-section" id="skincare">
      <h2>韓国コスメでの活用 ─ ppm表記の読み方</h2>
      <p>韓国コスメのグルタチオン配合量は<strong>ppm（parts per million：100万分の1）</strong>で表記されます。</p>
      <ul>
        <li>100ppm = 0.01%</li>
        <li>1,000ppm = 0.1%</li>
        <li>10,000ppm = 1%</li>
        <li>30,000ppm = 3% ← グルコラ セラムの配合量</li>
      </ul>
      <p>一般的な韓国コスメのグルタチオン配合量は100〜500ppm程度です。グルコラ シリーズのように30,000ppmという高濃度配合は、スキンケアにおいて特に高い部類に入ります。</p>
      <p>成分ページでグルタチオンの詳細な情報を確認できます：<a href="/ingredients/glutathione.html">グルタチオンの詳細解説ページ →</a></p>
    </section>

    <section class="article-section" id="choose">
      <h2>グルタチオン配合スキンケアの選び方</h2>
      <h3>① 配合濃度（ppm）を確認</h3>
      <p>配合濃度が高いほど成分量が多くなります。透明感改善を本格的に目指すなら10,000ppm以上を目安に選ぶとよいでしょう。</p>
      <h3>② 一緒に配合されている成分を確認</h3>
      <p>グルタチオン単独より、コラーゲン・ビタミンC誘導体・ナイアシンアミドなどと組み合わせた製品が相乗効果を期待できます。グルコラシリーズは300Daコラーゲン・乳酸菌発酵エキスとの組み合わせです。</p>
      <h3>③ 剤形（化粧水・美容液・クリーム）で選ぶ</h3>
      <p>美容液が最も高濃度に配合されることが多く、化粧水→美容液の順で重ねるとより効果的です。予算やルーティンに合わせて選びましょう。</p>
    </section>

    <section class="article-section" id="products">
      <h2>LUMINOVEのグルタチオン配合商品</h2>
      <p>LUMINOVEではグルコラシリーズ（from the skin）を中心に、グルタチオン配合の韓国スキンケアを取り扱っています。</p>
      <div class="cta-box">
        <p>グルタチオン30,000ppm配合の美容液でまず試したい方に</p>
        <a href="/products/glucola-serum.html" class="btn-primary">グルコラ セラム（美容液）を詳しく見る →</a>
      </div>
      <div class="cta-box" style="margin-top:1rem">
        <p>化粧水ステップからグルタチオンを取り入れたい方に</p>
        <a href="/products/glucola-skin.html" class="btn-primary">グルコラ スキン（化粧水）を詳しく見る →</a>
      </div>
    </section>

  </div>

  <section class="faq-section" id="faq">
    <h2>よくある質問</h2>
    <details class="faq-item">
      <summary class="faq-question">グルタチオンとは何ですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">グルタチオンはグルタミン酸・システイン・グリシンの3つのアミノ酸が結合したトリペプチドで、人体に自然に存在する成分です。強力な抗酸化作用を持ち、美容点滴（白玉注射）の主成分として広く知られています。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">グルタチオンはなぜ透明感に効果があるのですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">グルタチオンはメラニン生成に関わるチロシナーゼ酵素の活性を抑えることで、メラニン量の調整にアプローチします。また強力な抗酸化作用により活性酸素を除去し、くすみ原因のひとつである酸化ストレスを抑えます。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">美容点滴と同じ効果がありますか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">美容点滴（白玉注射）は静脈投与のため全身への即効性があります。スキンケアは経皮吸収での働きが主となりますが、毎日継続できる手軽さが強みです。補完的に活用することをおすすめします。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">グルタチオン配合スキンケアの選び方は？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">配合濃度（ppm）・組み合わせ成分・剤形の3点で選びましょう。透明感改善を本格的に目指すなら10,000ppm以上、コラーゲンやビタミンC誘導体との組み合わせ製品がおすすめです。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">毎日使っても大丈夫ですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">はい、毎日の朝晩使用に対応した設計の製品がほとんどです。グルタチオンは継続使用により透明感・くすみ改善の実感が得やすくなります。28日間（肌のターンオーバー1サイクル）の継続使用をおすすめします。</p>
    </details>
  </section>

  <section class="related-section">
    <h2>関連記事・ページ</h2>
    <div class="related-grid">
      <a href="/ingredients/glutathione.html" class="related-card">
        <img src="/images/product-serum.webp" alt="グルタチオン成分解説" loading="lazy" />
        <p>グルタチオン<br>成分詳細ページ</p>
      </a>
      <a href="/blog/pdrn-what-is.html" class="related-card">
        <img src="/images/product-rejun-cream.webp" alt="PDRNとは" loading="lazy" />
        <p>PDRNとは？<br>再生成分解説</p>
      </a>
      <a href="/products/glucola-serum.html" class="related-card">
        <img src="/images/product-serum.webp" alt="グルコラ セラム" loading="lazy" />
        <p>グルコラ セラム<br>（美容液）</p>
      </a>
    </div>
  </section>

  <div class="back-link">
    <a href="/" class="btn-outline">LUMINOVEトップへ →</a>
  </div>

{BLOG_FOOTER}
</body>
</html>'''

with open('blog/glutathione-what-is.html', 'w', encoding='utf-8') as f:
    f.write(blog1)
print('  Created: blog/glutathione-what-is.html')

# ---- ブログ記事②: PDRNとは？ ----
blog2 = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ECTSQMJ4ME"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ECTSQMJ4ME');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <title>PDRNとは？サーモン由来のDNA成分と韓国スキンケアでの使い方｜LUMINOVE</title>
  <meta name="description" content="PDRN（ポリデオキシリボヌクレオチド）とは何か、サーモン由来DNA成分の仕組み・再生医療との関係・韓国コスメでの活用法をわかりやすく解説します。リジュエヌ クリームなどPDRN配合商品も紹介。" />
  <link rel="canonical" href="https://www.luminove.online/blog/pdrn-what-is.html" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="PDRNとは？サーモン由来のDNA成分と韓国スキンケアでの使い方｜LUMINOVE" />
  <meta property="og:description" content="PDRN（ポリデオキシリボヌクレオチド）とは何か、サーモン由来DNA成分の仕組み・再生医療との関係・韓国コスメでの活用法を解説。" />
  <meta property="og:url" content="https://www.luminove.online/blog/pdrn-what-is.html" />
  <meta property="og:image" content="https://www.luminove.online/images/product-rejun-cream.webp" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "PDRNとは？サーモン由来のDNA成分と韓国スキンケアでの使い方",
    "description": "PDRN（ポリデオキシリボヌクレオチド）とは何か、サーモン由来DNA成分の仕組み・再生医療との関係・韓国コスメでの活用法を解説。",
    "url": "https://www.luminove.online/blog/pdrn-what-is.html",
    "publisher": {{"@type":"Organization","name":"LUMINOVE","url":"https://www.luminove.online"}},
    "datePublished": "2026-06-17",
    "dateModified": "2026-06-17"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"TOP","item":"https://www.luminove.online/"}},
      {{"@type":"ListItem","position":2,"name":"ブログ","item":"https://www.luminove.online/blog/"}},
      {{"@type":"ListItem","position":3,"name":"PDRNとは？","item":"https://www.luminove.online/blog/pdrn-what-is.html"}}
    ]
  }}
  </script>
  <style>{BLOG_CSS}</style>
</head>
<body>
{BLOG_HEADER}

  <nav class="breadcrumb">
    <a href="/">TOP</a> ＞ <a href="/blog/">ブログ</a> ＞ PDRNとは？
  </nav>

  <article class="article-hero">
    <span class="article-tag">成分解説 / PDRN</span>
    <h1>PDRNとは？<br>サーモン由来DNA成分の仕組みと韓国スキンケアでの活用法</h1>
    <p class="article-meta">2026年6月17日 ｜ LUMINOVE編集部</p>
    <p class="article-lead">「水光注射」などの再生美容医療で注目されるPDRN。韓国コスメへの高配合が急速に進み、美容施術後ケアや日常の肌再生ケアとして自宅でも使えるようになりました。本記事ではPDRNの基礎知識から韓国スキンケアでの活用法まで解説します。</p>

    <div class="toc">
      <h2>目次</h2>
      <ol>
        <li><a href="#what">PDRNとは？基本情報</a></li>
        <li><a href="#salmon">なぜサーモン由来？</a></li>
        <li><a href="#clinic">再生医療・水光注射との関係</a></li>
        <li><a href="#skincare">韓国コスメでの活用とppm表記</a></li>
        <li><a href="#nmn">NMNとの組み合わせ効果</a></li>
        <li><a href="#products">LUMINOVEのPDRN配合商品</a></li>
        <li><a href="#faq">よくある質問</a></li>
      </ol>
    </div>
  </article>

  <div class="article-body">

    <section class="article-section" id="what">
      <h2>PDRNとは？基本情報</h2>
      <p>PDRN（ポリデオキシリボヌクレオチド / Polydeoxyribonucleotide）は、<strong>DNAを構成するポリヌクレオチドの断片</strong>です。細胞の修復・再生に関わるDNAの構成要素として、医療・美容分野で研究が進んでいます。</p>
      <p>PDRNは肌の「A2A受容体」に結合することで、細胞の修復・活性化をサポートすると考えられており、美容医療の再生注射や水光注射として取り入れられてきました。近年は韓国コスメ業界でのスキンケア成分としての活用が急速に広まっています。</p>
    </section>

    <section class="article-section" id="salmon">
      <h2>なぜサーモン由来？</h2>
      <p>PDRNは主に<strong>サーモン（鮭）の精巣から抽出</strong>されます。サーモンのDNAは人間のDNAとの相同性が高く（約80%）、生体適合性が高いとされています。これがサーモンDNA由来のPDRNが美容成分として選ばれる主な理由です。</p>
      <p>「サーモン注射」「サーモンDNA注射」という名称で呼ばれる美容医療は、このPDRN（またはPNTX）を使用した施術を指します。</p>
      <div class="quote-box">
        <p>PDRNとPNTX（ポリヌクレオチド）は類似した成分ですが、分子量・精製方法に違いがあります。どちらもサーモン由来DNAを原料とする再生系成分として韓国コスメで広く使われています。</p>
      </div>
    </section>

    <section class="article-section" id="clinic">
      <h2>再生医療・水光注射との関係</h2>
      <p>水光注射（スキンブースター注射）は、PDRNやヒアルロン酸などを真皮層に直接注入することで、肌のハリ・うるおい・再生をサポートする美容医療施術です。直接注入のため即効性と高い効果が期待できますが、クリニックでの施術が必要です。</p>
      <p>スキンケアとして使用するPDRN配合コスメは、経皮吸収によるアプローチとなり、施術とは作用経路が異なります。ただし<strong>施術後のダウンタイムケア</strong>として使用することで、肌回復のサポートが期待できます。リジュエヌ クリームはこの施術後ケアを主目的として設計されています。</p>
    </section>

    <section class="article-section" id="skincare">
      <h2>韓国コスメでの活用とppm表記</h2>
      <p>韓国コスメのPDRN配合量もppm（100万分の1）で表記されます。リジュエヌ クリームに配合されているPDRN3000ppmは0.3%に相当し、韓国のPDRN配合コスメとして高濃度の部類に入ります。</p>
      <p>PDRN配合スキンケアは以下のようなケースで特に注目されています：</p>
      <ul>
        <li>美容施術（レーザー・ピーリング・注射）後のダウンタイムケア</li>
        <li>ニキビ跡・色素沈着の改善ケア</li>
        <li>肌荒れ・ゆらぎ肌のバリア強化</li>
        <li>28日間ルーティンによる肌リズム整え</li>
      </ul>
      <p>詳細は成分ページもご参照ください：<a href="/ingredients/pdrn.html">PDRNの詳細解説ページ →</a></p>
    </section>

    <section class="article-section" id="nmn">
      <h2>NMNとの組み合わせ効果</h2>
      <p>NMN（ニコチンアミドモノヌクレオチド）は細胞のエネルギー源であるNAD+の前駆体で、アンチエイジング研究で注目される成分です。PDRNとNMNを組み合わせることで：</p>
      <ul>
        <li>PDRN：細胞修復・再生のサポート</li>
        <li>NMN：細胞エネルギー（NAD+）の補充によるハリ・活力</li>
      </ul>
      <p>という相補的なアプローチが期待できます。リジュエヌ クリームはPDRN3000ppm×NMN1000ppmのデュアルフォーミュラを採用しています。</p>
      <p>NMNについて詳しくは：<a href="/ingredients/nmn.html">NMN成分解説ページ →</a></p>
    </section>

    <section class="article-section" id="products">
      <h2>LUMINOVEのPDRN配合商品</h2>
      <p>LUMINOVEではPDRN配合の韓国スキンケアとして「リジュエヌ クリーム」と「CEL:VIV バイオキット」を取り扱っています。</p>
      <div class="cta-box">
        <p>PDRN3000ppm×NMN1000ppm｜施術後ケア・ニキビ跡・28日ルーティン</p>
        <a href="/products/rejun-pdrn-cream.html" class="btn-primary">リジュエヌ クリームを詳しく見る →</a>
      </div>
    </section>

  </div>

  <section class="faq-section" id="faq">
    <h2>よくある質問</h2>
    <details class="faq-item">
      <summary class="faq-question">PDRNとは何ですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">PDRN（ポリデオキシリボヌクレオチド）はサーモンのDNA由来の成分で、細胞の修復・再生に関わるDNA断片です。再生医療の水光注射や、韓国コスメのスキンケア成分として注目されています。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">なぜサーモン由来なのですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">サーモンのDNAは人間のDNAとの相同性が高く（約80%）、生体適合性が高いとされているためです。サーモンの精巣から抽出・精製されたPDRNが美容分野で広く活用されています。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">水光注射とスキンケアのPDRNは同じですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">同じPDRN成分ですが、作用経路が異なります。水光注射は真皮層への直接注入のため即効性が高く、スキンケアは経皮吸収での働きが主となります。スキンケアは毎日継続できる点が強みです。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">美容施術後に使えますか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">PDRN配合スキンケアは施術後のダウンタイムケアとして活用できます。リジュエヌ クリームは施術後ケアを主目的とした低刺激・無香料処方です。ただし施術後のケアは担当医師の指示に従ってください。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">NMNとPDRNの違いは何ですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">PDRNはサーモン由来DNA断片で細胞修復・再生へのアプローチ、NMNは細胞エネルギー（NAD+）の前駆体でアンチエイジングアプローチです。両者は異なる仕組みで肌にアプローチするため、組み合わせることで相補的な効果が期待できます。</p>
    </details>
  </section>

  <section class="related-section">
    <h2>関連記事・ページ</h2>
    <div class="related-grid">
      <a href="/ingredients/pdrn.html" class="related-card">
        <img src="/images/product-rejun-cream.webp" alt="PDRN成分解説" loading="lazy" />
        <p>PDRN<br>成分詳細ページ</p>
      </a>
      <a href="/blog/glutathione-what-is.html" class="related-card">
        <img src="/images/product-serum.webp" alt="グルタチオンとは" loading="lazy" />
        <p>グルタチオンとは？<br>成分解説</p>
      </a>
      <a href="/products/rejun-pdrn-cream.html" class="related-card">
        <img src="/images/product-rejun-cream.webp" alt="リジュエヌ クリーム" loading="lazy" />
        <p>リジュエヌ クリーム<br>（PDRN×NMN）</p>
      </a>
    </div>
  </section>

  <div class="back-link">
    <a href="/" class="btn-outline">LUMINOVEトップへ →</a>
  </div>

{BLOG_FOOTER}
</body>
</html>'''

with open('blog/pdrn-what-is.html', 'w', encoding='utf-8') as f:
    f.write(blog2)
print('  Created: blog/pdrn-what-is.html')

# ---- ブログ記事③: 韓国スキンケアおすすめ ----
blog3 = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ECTSQMJ4ME"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ECTSQMJ4ME');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <title>韓国スキンケアおすすめ2026年版｜グルタチオン・PDRN・RG3成分で選ぶLUMINOVEセレクト｜LUMINOVE</title>
  <meta name="description" content="2026年版・韓国スキンケアおすすめ特集。グルタチオン・PDRN・RG3・NMNなど機能性成分から選ぶLUMINOVEセレクトブランド8選を肌悩み別に徹底紹介します。" />
  <link rel="canonical" href="https://www.luminove.online/blog/korean-skincare-recommended.html" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="韓国スキンケアおすすめ2026年版｜グルタチオン・PDRN・RG3成分で選ぶLUMINOVEセレクト" />
  <meta property="og:description" content="2026年版・韓国スキンケアおすすめ特集。グルタチオン・PDRN・RG3・NMNなど機能性成分から選ぶLUMINOVEセレクトブランドを肌悩み別に紹介。" />
  <meta property="og:url" content="https://www.luminove.online/blog/korean-skincare-recommended.html" />
  <meta property="og:image" content="https://www.luminove.online/images/hero-all.webp" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "韓国スキンケアおすすめ2026年版｜グルタチオン・PDRN・RG3成分で選ぶLUMINOVEセレクト",
    "description": "2026年版・韓国スキンケアおすすめ特集。グルタチオン・PDRN・RG3・NMNなど機能性成分から選ぶLUMINOVEセレクトブランド8選を肌悩み別に紹介。",
    "url": "https://www.luminove.online/blog/korean-skincare-recommended.html",
    "publisher": {{"@type":"Organization","name":"LUMINOVE","url":"https://www.luminove.online"}},
    "datePublished": "2026-06-17",
    "dateModified": "2026-06-17"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"TOP","item":"https://www.luminove.online/"}},
      {{"@type":"ListItem","position":2,"name":"ブログ","item":"https://www.luminove.online/blog/"}},
      {{"@type":"ListItem","position":3,"name":"韓国スキンケアおすすめ2026","item":"https://www.luminove.online/blog/korean-skincare-recommended.html"}}
    ]
  }}
  </script>
  <style>{BLOG_CSS}
    .recommend-card {{ background: var(--warm-white); border-radius: var(--radius); padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: var(--shadow); display: flex; gap: 1.5rem; align-items: flex-start; }}
    .recommend-card img {{ width: 100px; height: 100px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }}
    .recommend-card-body h3 {{ font-size: 1rem; color: var(--green-deep); margin-bottom: .4rem; }}
    .recommend-card-body p {{ font-size: .85rem; color: var(--text-mid); margin-bottom: .6rem; line-height: 1.7; }}
    .recommend-card-body a {{ font-size: .8rem; color: var(--green-mid); font-weight: 500; text-decoration: underline; }}
    .trouble-table {{ width: 100%; border-collapse: collapse; font-size: .88rem; margin-bottom: 1.5rem; }}
    .trouble-table th {{ background: var(--green-pale); color: var(--green-deep); padding: .7rem 1rem; text-align: left; font-weight: 600; }}
    .trouble-table td {{ padding: .7rem 1rem; border-bottom: 1px solid var(--green-pale); color: var(--text-mid); }}
    @media (max-width: 600px) {{ .recommend-card {{ flex-direction: column; }} .recommend-card img {{ width: 80px; height: 80px; }} }}
  </style>
</head>
<body>
{BLOG_HEADER}

  <nav class="breadcrumb">
    <a href="/">TOP</a> ＞ <a href="/blog/">ブログ</a> ＞ 韓国スキンケアおすすめ2026
  </nav>

  <article class="article-hero">
    <span class="article-tag">韓国コスメ / セレクトガイド</span>
    <h1>韓国スキンケアおすすめ2026年版<br>グルタチオン・PDRN・RG3成分で選ぶLUMINOVEセレクト</h1>
    <p class="article-meta">2026年6月17日 ｜ LUMINOVE編集部</p>
    <p class="article-lead">流行だけで選ぶのではなく、「成分コンセプト」で選ぶ韓国スキンケア。LUMINOVEが取り扱うグルタチオン・PDRN・RG3・NMN配合の韓国ブランドを、肌悩み別におすすめ商品とともに紹介します。</p>

    <div class="toc">
      <h2>目次</h2>
      <ol>
        <li><a href="#policy">LUMINOVEのセレクト基準</a></li>
        <li><a href="#glutathione">透明感・くすみ改善 ─ グルタチオン配合</a></li>
        <li><a href="#pdrn">施術後ケア・再生 ─ PDRN配合</a></li>
        <li><a href="#rg3">エイジングケア ─ RG3配合</a></li>
        <li><a href="#table">肌悩み別おすすめ早見表</a></li>
        <li><a href="#faq">よくある質問</a></li>
      </ol>
    </div>
  </article>

  <div class="article-body">

    <section class="article-section" id="policy">
      <h2>LUMINOVEのセレクト基準</h2>
      <p>LUMINOVEは、六本木美容医療クリニック（BMC）院長・大久保義徳が代表を務める株式会社ルミノーブが運営するセレクトショップです。商品選定の基準は以下の通りです：</p>
      <ul>
        <li><strong>成分コンセプトの明確さ</strong>：配合成分の目的・濃度が明確であること</li>
        <li><strong>ブランドの品質管理体制</strong>：韓国での実績と製造管理体制が信頼できること</li>
        <li><strong>機能性成分への特化</strong>：グルタチオン・PDRN・RG3・NMNなど美容医療でも注目される成分を配合していること</li>
        <li><strong>日本市場への適合性</strong>：日本人の肌・ライフスタイルに合う商品であること</li>
      </ul>
      <p>取り扱い商品の処方設計・製品開発は各韓国ブランドが行っており、LUMINOVEは選定・販売を担うセレクトショップです。</p>
    </section>

    <section class="article-section" id="glutathione">
      <h2>透明感・くすみ改善 ─ グルタチオン配合ブランド</h2>
      <p>グルタチオンは美容点滴（白玉注射）の主成分。透明感・くすみ改善・抗酸化を目的に韓国コスメへの高配合が進んでいます。<a href="/blog/glutathione-what-is.html">グルタチオンとは？詳しく読む →</a></p>

      <div class="recommend-card">
        <img src="/images/product-serum.webp" alt="グルコラ セラム" loading="lazy" />
        <div class="recommend-card-body">
          <h3>グルコラ セラム（美容液）｜from the skin</h3>
          <p>グルタチオン30,000ppm（3%）×300Daコラーゲン×ボルフィリン配合。グルタチオン配合コスメで最高峰レベルの濃度。透明感・ハリ・うるおいをトータルケア。</p>
          <a href="/products/glucola-serum.html">詳しく見る →</a>
        </div>
      </div>
      <div class="recommend-card">
        <img src="/images/product-skin.webp" alt="グルコラ スキン" loading="lazy" />
        <div class="recommend-card-body">
          <h3>グルコラ スキン（化粧水）｜from the skin</h3>
          <p>グルタチオン×300Daコラーゲン×乳酸菌発酵エキス配合のブライトニング化粧水。化粧水ステップからグルタチオンケアを取り入れたい方に。</p>
          <a href="/products/glucola-skin.html">詳しく見る →</a>
        </div>
      </div>
      <div class="recommend-card">
        <img src="/images/product-cleanser.webp" alt="グルコラ クレンジングフォーム" loading="lazy" />
        <div class="recommend-card-body">
          <h3>グルコラ クレンジングフォーム｜from the skin</h3>
          <p>洗顔にもグルタチオン・300Daコラーゲンを配合。落とすだけじゃない"与える"洗顔。クレンジング・洗顔・シェービングのマルチ対応。</p>
          <a href="/products/glucola-cleansing-foam.html">詳しく見る →</a>
        </div>
      </div>
    </section>

    <section class="article-section" id="pdrn">
      <h2>施術後ケア・再生 ─ PDRN配合ブランド</h2>
      <p>PDRNはサーモン由来DNA成分。再生医療・水光注射でも使われる注目成分を配合した韓国コスメです。<a href="/blog/pdrn-what-is.html">PDRNとは？詳しく読む →</a></p>

      <div class="recommend-card">
        <img src="/images/product-rejun-cream.webp" alt="リジュエヌ クリーム" loading="lazy" />
        <div class="recommend-card-body">
          <h3>リジュエヌ クリーム（Reju:N）</h3>
          <p>PDRN3000ppm×NMN1000ppmのデュアルフォーミュラ。EGF・セラミドNP・ツボクサエキスを複合配合。美容施術後ケア・ニキビ跡・色素沈着に特化した低刺激・無香料クリーム。</p>
          <a href="/products/rejun-pdrn-cream.html">詳しく見る →</a>
        </div>
      </div>
    </section>

    <section class="article-section" id="rg3">
      <h2>エイジングケア ─ RG3（高麗人参）配合ブランド</h2>
      <p>RG3は高麗人参のわずか0.001%以下しか含まれない希少サポニン。エイジングケア・ハリ・透明感にアプローチするプレミアム成分です。<a href="/ingredients/rg3.html">RG3成分詳細ページ →</a></p>

      <div class="recommend-card">
        <img src="/images/product-rg3-serum.webp" alt="クイーンズ RG3 モイスチャーセラム" loading="lazy" />
        <div class="recommend-card-body">
          <h3>クイーンズ RG3 モイスチャーセラム（QUEEN'S GINSENOSIDE RG3）</h3>
          <p>高麗人参由来RG3×韓国特許取得成分DERMA-CLERA配合のブースターアンプル。ハリ・透明感・肌荒れケアを次のスキンケアへの導入ステップとして。80ml</p>
          <a href="/products/rg3-vital-ampoule.html">詳しく見る →</a>
        </div>
      </div>
      <div class="recommend-card">
        <img src="/images/product-rg4-cream.webp" alt="クイーンズ RG3 モイスチャークリーム" loading="lazy" />
        <div class="recommend-card-body">
          <h3>クイーンズ RG3 モイスチャークリーム（QUEEN'S GINSENOSIDE RG3）</h3>
          <p>RG3×コラーゲン×ヒアルロン酸配合の弾力保湿ナイトクリーム。DERMA-CLERAが肌バリアを整え、睡眠中にうるおいを閉じ込める。50ml</p>
          <a href="/products/rg3-vital-cream.html">詳しく見る →</a>
        </div>
      </div>
    </section>

    <section class="article-section" id="table">
      <h2>肌悩み別おすすめ早見表</h2>
      <table class="trouble-table">
        <tr><th>肌悩み</th><th>おすすめ成分</th><th>商品</th></tr>
        <tr><td>透明感・くすみ改善</td><td>グルタチオン</td><td><a href="/products/glucola-serum.html">グルコラ セラム</a>・<a href="/products/glucola-skin.html">スキン</a></td></tr>
        <tr><td>毛穴・洗顔ケア</td><td>グルタチオン＋コラーゲン</td><td><a href="/products/glucola-cleansing-foam.html">グルコラ クレンジングフォーム</a></td></tr>
        <tr><td>ニキビ跡・色素沈着</td><td>PDRN＋NMN</td><td><a href="/products/rejun-pdrn-cream.html">リジュエヌ クリーム</a></td></tr>
        <tr><td>施術後ダウンタイムケア</td><td>PDRN（低刺激）</td><td><a href="/products/rejun-pdrn-cream.html">リジュエヌ クリーム</a></td></tr>
        <tr><td>ファーストエイジングケア</td><td>RG3＋DERMA-CLERA</td><td><a href="/products/rg3-vital-ampoule.html">RG3 セラム</a>・<a href="/products/rg3-vital-cream.html">クリーム</a></td></tr>
        <tr><td>ヘアダメージ・サロン帰り感</td><td>補修成分配合ヘアアンプル</td><td><a href="/products/curlyshyll-repair-ampoule.html">Curly Shyllアンプル</a></td></tr>
      </table>
    </section>

  </div>

  <section class="faq-section" id="faq">
    <h2>よくある質問</h2>
    <details class="faq-item">
      <summary class="faq-question">韓国スキンケアはどう選べばいいですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">肌悩みと配合成分を軸に選ぶのがおすすめです。透明感・くすみにはグルタチオン、施術後ケア・ニキビ跡にはPDRN、エイジングケアにはRG3というように、目的に合った成分を配合したブランドを選びましょう。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">グルタチオンとPDRNを同時に使っても大丈夫ですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">はい、異なる仕組みでアプローチする成分なので組み合わせて使用できます。例えばグルコラシリーズ（グルタチオン）で洗顔・化粧水・美容液を行い、リジュエヌ クリームを保湿ステップで使用するルーティンが人気です。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">LUMINOVEはどこで購入できますか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">LUMINOVEの公式STORESショップ（luminove.stores.jp）でお買い求めいただけます。各商品ページの「STORESで購入する」ボタンからご購入いただけます。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">初めての韓国コスメにおすすめは何ですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">まずはグルコラ クレンジングフォーム（¥3,500）からお試しください。洗顔ステップで毎日グルタチオン・コラーゲンケアができ、使い続けやすい価格帯です。化粧水・美容液と順次ステップアップすることをおすすめします。</p>
    </details>
  </section>

  <section class="related-section">
    <h2>成分をもっと詳しく知る</h2>
    <div class="related-grid">
      <a href="/blog/glutathione-what-is.html" class="related-card">
        <img src="/images/product-serum.webp" alt="グルタチオンとは" loading="lazy" />
        <p>グルタチオンとは？<br>成分解説</p>
      </a>
      <a href="/blog/pdrn-what-is.html" class="related-card">
        <img src="/images/product-rejun-cream.webp" alt="PDRNとは" loading="lazy" />
        <p>PDRNとは？<br>成分解説</p>
      </a>
      <a href="/ingredients/rg3.html" class="related-card">
        <img src="/images/product-rg3-serum.webp" alt="RG3成分" loading="lazy" />
        <p>RG3（高麗人参）<br>成分詳細</p>
      </a>
    </div>
  </section>

  <div class="back-link">
    <a href="/" class="btn-outline">LUMINOVEトップへ →</a>
  </div>

{BLOG_FOOTER}
</body>
</html>'''

with open('blog/korean-skincare-recommended.html', 'w', encoding='utf-8') as f:
    f.write(blog3)
print('  Created: blog/korean-skincare-recommended.html')

# sitemap 更新
print('\n=== sitemap.xml 更新 ===')
with open('sitemap.xml', encoding='utf-8') as f:
    sm = f.read()

new_urls = ''
for slug in ['glutathione-what-is', 'pdrn-what-is', 'korean-skincare-recommended']:
    url = f'https://www.luminove.online/blog/{slug}.html'
    if url not in sm:
        new_urls += f'''  <url>
    <loc>{url}</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
if new_urls:
    sm = sm.replace('</urlset>', new_urls + '</urlset>')
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sm)
    print('  sitemap.xml: ブログ3件追加 OK')

print('\n=== 全処理完了 ===')
