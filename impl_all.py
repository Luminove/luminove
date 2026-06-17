# -*- coding: utf-8 -*-
"""
全タスク実装スクリプト
1. glucola-serum.html 新規作成
2. glucola-skin.html 新規作成
3. doctor/index.html 修正（表現修正）
4. AggregateRating を reviewCount:5 / ratingValue:4.8 に統一
5. 残存 JPG/PNG 参照を WebP 化（画像変換 + HTML更新）
"""
import os, re
from PIL import Image

# ======================================================
# TASK 5: 残存画像の WebP 変換
# ======================================================
print('=== TASK5: WebP変換 ===')
IMGDIR = 'images'
to_convert = ['product-cleanser.jpg','product-pack2.jpg','product-mgcream.jpg','product-serum.jpg','product-skin.jpg']
for fname in to_convert:
    src = os.path.join(IMGDIR, fname)
    if not os.path.isfile(src):
        print(f'  SKIP(not found): {src}')
        continue
    dst = os.path.join(IMGDIR, fname.rsplit('.',1)[0] + '.webp')
    if os.path.isfile(dst):
        print(f'  SKIP(exists): {dst}')
        continue
    img = Image.open(src).convert('RGB')
    img.save(dst, 'WEBP', quality=85)
    print(f'  OK: {src} ({os.path.getsize(src)//1024}KB) -> {dst} ({os.path.getsize(dst)//1024}KB)')

# HTML内のJPG/PNG参照をWebPへ更新
html_files = ['index.html']
for f in os.listdir('products'):
    if f.endswith('.html'): html_files.append('products/'+f)
for f in os.listdir('ingredients'):
    if f.endswith('.html'): html_files.append('ingredients/'+f)
html_files.append('doctor/index.html')

replace_map = {n: n.rsplit('.',1)[0]+'.webp' for n in to_convert}
for path in html_files:
    if not os.path.isfile(path): continue
    with open(path, encoding='utf-8') as f: html = f.read()
    changed = False
    for old, new in replace_map.items():
        for prefix in ['images/', '../images/']:
            if prefix+old in html:
                html = html.replace(prefix+old, prefix+new)
                changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f: f.write(html)
        print(f'  HTML updated: {path}')

# ======================================================
# TASK 4: AggregateRating を reviewCount:5 / ratingValue:4.8 に統一
# ======================================================
print('\n=== TASK4: AggregateRating修正 ===')
for fname in os.listdir('products'):
    if not fname.endswith('.html'): continue
    path = 'products/'+fname
    with open(path, encoding='utf-8') as f: html = f.read()
    # reviewCount を 5 に、ratingValue を 4.8 に統一
    html2 = re.sub(r'"reviewCount":\s*"\d+"', '"reviewCount": "5"', html)
    html2 = re.sub(r'"ratingValue":\s*"[\d.]+"', '"ratingValue": "4.8"', html2)
    if html2 != html:
        with open(path, 'w', encoding='utf-8') as f: f.write(html2)
        print(f'  Fixed: {fname}')

# ======================================================
# SHARED: 商品ページ HTML テンプレート
# ======================================================
def product_page(
    title, desc, canonical, breadcrumb3, og_image,
    product_name, brand, stores_url, price,
    review_body, article_tag_text,
    h1_html, lead_text, img_src, img_alt,
    sections_html, related_html,
    faqs
):
    faq_schema = ',\n    '.join(
        '{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'.format(q=q.replace('"','\\"'), a=a.replace('"','\\"'))
        for q, a in faqs
    )
    faq_html_items = '\n'.join(
        f'    <details class="faq-item">\n      <summary class="faq-question">{q}<span class="faq-icon">＋</span></summary>\n      <p class="faq-answer">{a}</p>\n    </details>'
        for q, a in faqs
    )
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ECTSQMJ4ME"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ECTSQMJ4ME');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#2d4a3e" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" /></noscript>

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://www.luminove.online{canonical}" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://www.luminove.online{canonical}" />
  <meta property="og:image" content="https://www.luminove.online{og_image}" />
  <meta property="og:locale" content="ja_JP" />
  <meta property="og:site_name" content="LUMINOVE" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://www.luminove.online{og_image}" />

  <!-- JSON-LD: Product -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{product_name}",
    "brand": {{ "@type": "Brand", "name": "{brand}" }},
    "description": "{desc}",
    "image": "https://www.luminove.online{og_image}",
    "url": "{stores_url}",
    "offers": {{
      "@type": "Offer",
      "url": "{stores_url}",
      "priceCurrency": "JPY",
      "price": "{price}",
      "availability": "https://schema.org/InStock"
    }},
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "reviewCount": "5",
      "bestRating": "5"
    }},
    "review": {{
      "@type": "Review",
      "author": {{
        "@type": "Organization",
        "name": "六本木美容医療クリニック（BMC）",
        "url": "https://bmc-roppongi.com/"
      }},
      "reviewBody": "{review_body}"
    }}
  }}
  </script>

  <!-- JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "TOP", "item": "https://www.luminove.online/" }},
      {{ "@type": "ListItem", "position": 2, "name": "製品", "item": "https://www.luminove.online/#products" }},
      {{ "@type": "ListItem", "position": 3, "name": "{breadcrumb3}", "item": "https://www.luminove.online{canonical}" }}
    ]
  }}
  </script>

  <!-- JSON-LD: FAQPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
    {faq_schema}
    ]
  }}
  </script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --green-deep:#2d4a3e; --green-mid:#4a7c67; --green-light:#7db89a;
      --green-pale:#d4ede4; --green-mist:#f0f8f4; --cream:#faf8f3;
      --warm-white:#ffffff; --text-dark:#1a2a23; --text-mid:#4a5c54;
      --text-light:#8a9e96; --gold:#c8a96a;
      --font-serif:'Cormorant Garamond','Hiragino Mincho ProN',serif,'Segoe UI Emoji','Noto Color Emoji','Apple Color Emoji';
      --font-sans:'Noto Sans JP',sans-serif,'Segoe UI Emoji','Noto Color Emoji','Apple Color Emoji';
      --radius:12px; --shadow:0 8px 40px rgba(45,74,62,.10);
      --shadow-hover:0 16px 56px rgba(45,74,62,.18);
      --transition:.35s cubic-bezier(.4,0,.2,1);
    }}
    html {{ scroll-behavior:smooth; }}
    body {{ font-family:var(--font-sans); color:var(--text-dark); background:var(--cream); line-height:1.8; overflow-x:hidden; }}
    a {{ color:inherit; text-decoration:none; }}
    img {{ display:block; width:100%; }}
    #header {{ position:fixed; top:0; left:0; width:100%; z-index:1000; padding:0 5%; display:flex; align-items:center; justify-content:space-between; height:72px; background:rgba(250,248,243,.82); backdrop-filter:blur(8px); box-shadow:0 1px 12px rgba(45,74,62,.06); transition:background var(--transition),box-shadow var(--transition); }}
    #header.scrolled {{ background:rgba(250,248,243,.97); box-shadow:0 2px 24px rgba(45,74,62,.10); }}
    .logo {{ font-family:var(--font-serif); font-size:1.75rem; font-weight:500; letter-spacing:.2em; color:var(--green-deep); }}
    .logo span {{ color:var(--green-mid); }}
    nav {{ display:flex; gap:2.5rem; align-items:center; }}
    nav a {{ font-size:.8rem; letter-spacing:.15em; font-weight:500; color:var(--text-mid); transition:color var(--transition); }}
    nav a:hover {{ color:var(--green-deep); }}
    .btn-nav {{ background:var(--green-deep); color:#fff !important; padding:.55rem 1.5rem; border-radius:50px; letter-spacing:.12em; font-size:.78rem; transition:background var(--transition),transform var(--transition) !important; }}
    .btn-nav:hover {{ background:var(--green-mid); transform:translateY(-1px); }}
    .hamburger {{ display:none; cursor:pointer; flex-direction:column; gap:5px; padding:4px; }}
    .hamburger span {{ display:block; width:24px; height:2px; background:var(--green-deep); border-radius:2px; transition:var(--transition); }}
    .mobile-nav {{ display:none; position:fixed; inset:0; z-index:1001; background:var(--cream); flex-direction:column; align-items:center; justify-content:center; gap:2.5rem; }}
    .mobile-nav.open {{ display:flex; }}
    .mobile-nav a {{ font-family:var(--font-serif); font-size:1.75rem; color:var(--green-deep); letter-spacing:.1em; }}
    .mobile-nav a.btn-primary {{ color:#fff; font-size:1.1rem; }}
    .close-btn {{ position:absolute; top:1.5rem; right:5%; font-size:1.75rem; cursor:pointer; color:var(--green-deep); background:none; border:none; }}
    .btn-primary {{ display:inline-block; background:var(--green-deep); color:#fff; padding:.9rem 2.4rem; border-radius:50px; font-size:.85rem; letter-spacing:.12em; font-weight:500; text-align:center; transition:background var(--transition),transform var(--transition),box-shadow var(--transition); box-shadow:0 4px 20px rgba(45,74,62,.25); }}
    .btn-primary:hover {{ background:var(--green-mid); transform:translateY(-2px); box-shadow:0 8px 30px rgba(45,74,62,.35); }}
    .btn-outline {{ display:inline-block; border:1.5px solid var(--green-deep); color:var(--green-deep); padding:.9rem 2.4rem; border-radius:50px; font-size:.85rem; letter-spacing:.12em; font-weight:500; text-align:center; transition:all var(--transition); }}
    .btn-outline:hover {{ background:var(--green-pale); transform:translateY(-2px); }}
    .breadcrumb {{ max-width:860px; margin:0 auto; padding:100px 5% 0; font-size:.75rem; letter-spacing:.05em; color:var(--text-light); }}
    .breadcrumb a {{ color:var(--text-mid); }}
    .breadcrumb a:hover {{ color:var(--green-deep); }}
    .article-hero {{ max-width:860px; margin:0 auto; padding:2rem 5% 3rem; text-align:center; }}
    .article-tag {{ display:inline-block; font-size:.72rem; letter-spacing:.2em; font-weight:500; color:var(--green-mid); background:var(--green-pale); padding:.4rem 1.2rem; border-radius:50px; margin-bottom:1.2rem; }}
    .article-hero h1 {{ font-family:var(--font-serif); font-size:clamp(1.8rem,4vw,2.8rem); font-weight:500; line-height:1.4; color:var(--green-deep); margin-bottom:1.2rem; }}
    .article-hero h1 .h1-sub {{ font-size:.6em; }}
    .br-mobile {{ display:none; }}
    .article-lead {{ font-size:.95rem; color:var(--text-mid); line-height:1.9; max-width:640px; margin:0 auto 2rem; }}
    .article-hero-img {{ max-width:320px; margin:0 auto 2rem; border-radius:var(--radius); overflow:hidden; box-shadow:var(--shadow); }}
    .article-body {{ max-width:720px; margin:0 auto; padding:0 5% 4rem; }}
    .article-section {{ margin-bottom:3rem; }}
    .article-section h2 {{ font-family:var(--font-serif); font-size:1.5rem; font-weight:500; color:var(--green-deep); margin-bottom:1rem; padding-bottom:.6rem; border-bottom:1px solid var(--green-pale); }}
    .article-section h3 {{ font-size:1.05rem; font-weight:600; color:var(--text-dark); margin:1.5rem 0 .6rem; }}
    .article-section p {{ font-size:.9rem; color:var(--text-mid); margin-bottom:1rem; }}
    .article-section ul,.article-section ol {{ font-size:.9rem; color:var(--text-mid); margin:0 0 1rem 1.4rem; line-height:1.9; }}
    .article-section li {{ margin-bottom:.4rem; }}
    .article-section p a {{ color:var(--green-mid); text-decoration:underline; }}
    .related-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }}
    .related-card {{ display:block; text-align:center; }}
    .related-card img {{ border-radius:var(--radius); margin-bottom:.6rem; aspect-ratio:1; object-fit:cover; }}
    .related-card p {{ font-size:.82rem; color:var(--text-dark); font-weight:500; }}
    .ingredient-card {{ background:var(--warm-white); border-radius:var(--radius); padding:1.5rem; margin-bottom:1.5rem; box-shadow:var(--shadow); }}
    .ingredient-card h3 {{ margin-top:0; color:var(--green-deep); }}
    .quote-box {{ background:var(--green-mist); border-left:4px solid var(--green-light); border-radius:var(--radius); padding:1.5rem 1.8rem; margin:1.5rem 0; }}
    .quote-box p {{ color:var(--text-dark); font-size:.92rem; margin-bottom:.8rem; }}
    .quote-box .quote-source {{ font-size:.78rem; color:var(--text-light); margin-bottom:0; }}
    .spec-table {{ width:100%; font-size:.88rem; color:var(--text-mid); margin-bottom:1.5rem; }}
    .spec-table tr {{ border-bottom:1px solid var(--green-pale); }}
    .spec-table th,.spec-table td {{ text-align:left; padding:.6rem 0; }}
    .spec-table th {{ width:8rem; color:var(--text-dark); font-weight:500; }}
    .cta-box {{ text-align:center; background:var(--green-mist); border-radius:var(--radius); padding:2.5rem 1.5rem; margin:2rem 0; }}
    .cta-box p {{ font-size:.92rem; color:var(--text-mid); margin-bottom:1.5rem; }}
    .cta-box .price {{ font-family:var(--font-serif); font-size:1.8rem; color:var(--green-deep); margin-bottom:.5rem; }}
    .cta-box .price span {{ font-size:.85rem; color:var(--text-light); margin-left:.4rem; }}
    .back-link {{ text-align:center; margin-bottom:4rem; }}
    .faq-section {{ max-width:800px; margin:4rem auto; padding:0 1.5rem; }}
    .faq-section h2 {{ font-family:var(--font-serif); font-size:1.6rem; font-weight:500; color:var(--green-deep); margin-bottom:2rem; padding-bottom:.75rem; border-bottom:1px solid var(--green-pale); }}
    .faq-item {{ border-bottom:1px solid var(--green-pale); }}
    .faq-question {{ display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; cursor:pointer; padding:1.2rem 0; font-weight:500; color:var(--text-dark); list-style:none; }}
    .faq-question::marker,.faq-question::-webkit-details-marker {{ display:none; }}
    .faq-icon {{ flex-shrink:0; width:24px; height:24px; border:1px solid var(--green-mid); border-radius:50%; display:flex; align-items:center; justify-content:center; color:var(--green-mid); font-size:.9rem; transition:transform var(--transition); }}
    details[open] .faq-icon {{ transform:rotate(45deg); }}
    .faq-answer {{ padding:.25rem 0 1.2rem; color:var(--text-mid); line-height:1.9; font-size:.95rem; }}
    footer {{ background:var(--text-dark); color:rgba(255,255,255,.65); padding:60px 5% 30px; }}
    .footer-grid {{ display:grid; grid-template-columns:1.5fr 1fr 1fr 1.8fr; gap:3rem; margin-bottom:3rem; }}
    .footer-brand .logo {{ color:#fff; margin-bottom:1rem; }}
    .footer-brand p {{ font-size:.83rem; line-height:1.85; max-width:260px; }}
    .footer-col h4 {{ font-size:.78rem; letter-spacing:.18em; font-weight:500; color:#fff; margin-bottom:1.25rem; text-transform:uppercase; }}
    .footer-col ul {{ list-style:none; display:flex; flex-direction:column; gap:.6rem; }}
    .footer-col li a {{ font-size:.83rem; transition:color var(--transition); }}
    .footer-col li a:hover {{ color:var(--green-light); }}
    .footer-bottom {{ border-top:1px solid rgba(255,255,255,.1); padding-top:1.5rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:.5rem; }}
    .footer-bottom p {{ font-size:.78rem; }}
    .footer-bottom a {{ font-size:.78rem; margin-left:1.5rem; transition:color var(--transition); }}
    .footer-bottom a:hover {{ color:var(--green-light); }}
    @media (max-width:1024px) {{ .footer-grid {{ grid-template-columns:1fr 1fr; }} }}
    @media (max-width:768px) {{
      nav {{ display:none; }} .hamburger {{ display:flex; }}
      .footer-grid {{ grid-template-columns:1fr; gap:2rem; }}
      .breadcrumb {{ padding-top:90px; }}
      .br-pc {{ display:none; }} .br-mobile {{ display:inline; }}
      .article-section h2 {{ font-size:1.25rem; }}
      .related-grid {{ grid-template-columns:repeat(2,1fr); }}
    }}
  </style>
</head>
<body>

  <header id="header">
    <a href="/" class="logo">LUMI<span>NOVE</span></a>
    <nav>
      <a href="/#products">製品</a>
      <a href="/#brands">取扱ブランド</a>
      <a href="/#ingredients">成分</a>
      <a href="/#reviews">レビュー</a>
      <a href="/#stores">取扱店</a>
      <a href="https://luminove.stores.jp/" target="_blank" rel="noopener" class="btn-nav">SHOP NOW</a>
    </nav>
    <button class="hamburger" id="hamburger" aria-label="メニュー">
      <span></span><span></span><span></span>
    </button>
  </header>

  <nav class="mobile-nav" id="mobileNav">
    <button class="close-btn" id="closeNav">✕</button>
    <a href="/" class="mobile-link">TOP</a>
    <a href="/#products" class="mobile-link">製品</a>
    <a href="/#brands" class="mobile-link">取扱ブランド</a>
    <a href="/#ingredients" class="mobile-link">成分</a>
    <a href="/#reviews" class="mobile-link">レビュー</a>
    <a href="https://luminove.stores.jp/" target="_blank" rel="noopener" class="btn-primary mobile-link">SHOP NOW</a>
  </nav>

  <nav class="breadcrumb" aria-label="breadcrumb">
    <a href="/">TOP</a> ＞ <a href="/#products">製品</a> ＞ {breadcrumb3}
  </nav>

  <section class="article-hero">
    <span class="article-tag">{article_tag_text}</span>
    {h1_html}
    <p class="article-lead">{lead_text}</p>
    <div class="article-hero-img">
      <img src="../images/{img_src}" alt="{img_alt}" fetchpriority="high" />
    </div>
    <a href="{stores_url}" target="_blank" rel="noopener" class="btn-primary">STORESで購入する →</a>
  </section>

  <div class="article-body">
{sections_html}
    <section class="article-section">
      <h2>関連商品</h2>
      <div class="related-grid">
{related_html}
      </div>
    </section>

    <div class="back-link">
      <a href="/#products" class="btn-outline">他の製品を見る →</a>
    </div>
  </div>

  <section class="faq-section">
    <h2>よくある質問</h2>
{faq_html_items}
  </section>

  <div class="back-link">
    <a href="/#products" class="btn-outline">他の製品を見る →</a>
  </div>

  <footer>
    <div class="footer-grid">
      <div class="footer-brand">
        <span class="logo">LUMI<span style="color:var(--green-light)">NOVE</span></span>
        <p>光と愛を纏う肌へ。六本木の美容医師が商品選定に携わる韓国コスメセレクトショップ。</p>
      </div>
      <div class="footer-col">
        <h4>Products</h4>
        <ul>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">スキンケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">ハンドケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">ヘアケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">アクネケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">プレミアム</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/#about">ブランドストーリー</a></li>
          <li><a href="/#ingredients">成分へのこだわり</a></li>
          <li><a href="/doctor/">LUMINOVEについて</a></li>
          <li><a href="mailto:info@luminove.online">お問い合わせ</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>会社概要</h4>
        <address style="font-style:normal;font-size:.78rem;line-height:2;color:rgba(255,255,255,.55)">
          <span style="display:block;color:rgba(255,255,255,.8);font-weight:500;margin-bottom:.25rem">株式会社ルミノーブ</span>
          〒102-0094<br>東京都千代田区紀尾井町4番1号<br>ニューオータニガーデンコート28階<br>
          <span style="display:block;margin-top:.4rem">設立：2025年2月</span>
          <span style="display:block">代表取締役：池田 宏貴　大久保 義徳</span>
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 LUMINOVE. All rights reserved.</p>
      <a href="https://luminove.stores.jp/privacy_policy" target="_blank" rel="noopener">プライバシーポリシー</a>
      <a href="https://luminove.stores.jp/tokushoho" target="_blank" rel="noopener">特定商取引法に基づく表示</a>
    </div>
  </footer>

  <script>
    const header = document.getElementById('header');
    window.addEventListener('scroll', () => {{ header.classList.toggle('scrolled', window.scrollY > 40); }});
    document.getElementById('hamburger').addEventListener('click', () => {{ document.getElementById('mobileNav').classList.toggle('open'); }});
    document.getElementById('closeNav').addEventListener('click', () => {{ document.getElementById('mobileNav').classList.remove('open'); }});
    document.querySelectorAll('.mobile-link').forEach(el => {{
      el.addEventListener('click', () => {{ document.getElementById('mobileNav').classList.remove('open'); }});
    }});
  </script>
</body>
</html>'''

# ======================================================
# TASK 1: glucola-serum.html
# ======================================================
print('\n=== TASK1: glucola-serum.html ===')

serum_sections = '''    <section class="article-section">
      <h2>グルコラ セラム（美容液）とは</h2>
      <p>「グルコラ セラム」は、韓国発スキンケアブランド「from the skin」のグルコラシリーズにおいて、最高濃度のグルタチオンを誇るフラッグシップ美容液です。グルタチオン30,000ppmという圧倒的な配合量に加え、コラーゲン・ボルフィリンを組み合わせ、透明感・ハリ・うるおいをトータルにケアします。</p>
      <p>美容液はスキンケアの中でも最も成分が濃縮されたステップ。化粧水（スキン）で肌を整えた後に使用することで、有効成分をより深く届けることができます。グルコラ セラムは、毎日のスキンケアに"本格的な美容成分の投資"を加えたい方に向けた、グルコラシリーズの中核製品です。</p>
      <div class="cta-box">
        <p class="price">¥7,200<span>（税込）</span></p>
        <a href="https://luminove.stores.jp/items/679c79bb4c088e04f7df3970" target="_blank" rel="noopener" class="btn-primary">STORESで購入する →</a>
      </div>
    </section>

    <section class="article-section">
      <h2>注目の3成分を徹底解説</h2>

      <div class="ingredient-card">
        <h3>①グルタチオン 30,000ppm<br>美容点滴の主成分を最高濃度で</h3>
        <p>グルタチオンは美容クリニックでの「白玉注射」（美容点滴）の主成分として知られるアミノ酸由来の成分です。グルコラ セラムには30,000ppm（3%）という高濃度で配合。一般的な韓国コスメのグルタチオン配合量（100〜500ppm）の数十倍以上の濃度です。</p>
        <p>グルタチオンの働きとして知られているのは、チロシナーゼ酵素の活性を抑えることによるメラニン生成への関与と、活性酸素を除去する抗酸化作用です。毎日の使用により、透明感やくすみ改善に継続的にアプローチします。</p>
      </div>

      <div class="ingredient-card">
        <h3>②300Daナノコラーゲン<br>肌の奥まで届く超低分子コラーゲン</h3>
        <p>コラーゲンの分子量は通常10万〜30万Daと大きく、皮膚表面への吸着が主となります。グルコラ セラムに配合される「300Daナノコラーゲン」は分子量を300Daまで低分子化した超低分子タイプ。角質層への浸透を考えて設計されており、ハリ・弾力・保湿に持続的にアプローチします。</p>
      </div>

      <div class="ingredient-card">
        <h3>③ボルフィリン<br>エイジングケアの新星成分</h3>
        <p>ボルフィリン（Volufiline）は、植物由来の美容成分で、肌のボリューム感やふっくら感にアプローチするとして注目されているエイジングケア成分です。グルタチオン・コラーゲンとの組み合わせで、外側からのハリと内側からのうるおいを同時にサポートします。</p>
      </div>
    </section>

    <section class="article-section">
      <h2>使用方法</h2>
      <table class="spec-table">
        <tr><th>使用タイミング</th><td>化粧水（スキン）の後、乳液（ローション）の前</td></tr>
        <tr><th>使用量</th><td>適量（パール粒大程度）を顔全体に</td></tr>
        <tr><th>頻度</th><td>毎朝晩（1日2回）</td></tr>
        <tr><th>組み合わせ</th><td>グルコラ スキン→グルコラ セラム→グルコラ ローションの順がおすすめ</td></tr>
      </table>
      <div class="quote-box">
        <p>🌿 グルコラシリーズはトータルケアとして設計されています。クレンジングフォーム→スキン（化粧水）→セラム（美容液）→ローション（乳液）の4ステップで、グルタチオン・コラーゲンを肌の隅々まで届けましょう。</p>
        <p class="quote-source">LUMINOVEおすすめの使い方</p>
      </div>
    </section>

    <section class="article-section">
      <h2>グルコラ スキン（化粧水）との違い</h2>
      <p>同シリーズのグルコラ スキン（化粧水）がグルタチオンと300Daコラーゲン・乳酸菌発酵エキスを配合した「水分補給・肌基盤強化」のステップであるのに対し、グルコラ セラムは<strong>グルタチオン30,000ppmという最高濃度の集中美容液</strong>です。</p>
      <ul>
        <li>グルコラ スキン：肌全体の水分バランスを整え、化粧水ステップとして使用</li>
        <li>グルコラ セラム：最高濃度のグルタチオンを浸透させる、美容液ステップとして使用</li>
      </ul>
      <p>2つを重ねて使うことで、グルタチオンケアの相乗効果が期待できます。</p>
    </section>

    <section class="article-section">
      <h2>こんな方におすすめ</h2>
      <ul>
        <li>透明感・くすみ改善を本格的にケアしたい方</li>
        <li>美容点滴（白玉注射）に興味があり、自宅でのスキンケアで代替・補完したい方</li>
        <li>シミ・色素沈着が気になり始めている方</li>
        <li>グルタチオンを高濃度で毎日継続して使いたい方</li>
        <li>エイジングサインが気になり始めた方</li>
      </ul>
    </section>'''

serum_related = '''        <a href="/products/glucola-cleansing-foam.html" class="related-card">
          <img src="../images/product-cleanser.webp" alt="グルコラ クレンジングフォーム" loading="lazy" />
          <p>グルコラ<br>クレンジングフォーム</p>
        </a>
        <a href="/products/glucola-peeling-pack2.html" class="related-card">
          <img src="../images/product-pack2.webp" alt="グルコラ ピリングパックⅡ" loading="lazy" />
          <p>グルコラ<br>ピリングパックⅡ</p>
        </a>
        <a href="/products/glucola-suncream.html" class="related-card">
          <img src="../images/product-suncream.webp" alt="グルコラ サンクリーム" loading="lazy" />
          <p>グルコラ<br>サンクリーム</p>
        </a>'''

serum_faqs = [
    ('グルタチオン30,000ppmとはどれほどの濃度ですか？', '30,000ppmは3%に相当します。韓国コスメのグルタチオン配合量の平均が100〜500ppm（0.01〜0.05%）であることを考えると、グルコラ セラムはその数十倍以上の濃度です。美容液として毎日使用することで、継続的に高濃度グルタチオンを肌へ届けられます。'),
    ('美容液はいつ使うのが正しいですか？', '化粧水（グルコラ スキンなど）で肌を整えた後、乳液（グルコラ ローション）の前のステップで使用します。化粧水で肌が柔らかくなった状態で美容液を重ねることで、成分が浸透しやすくなります。'),
    ('グルコラ スキン（化粧水）と両方使う必要がありますか？', '化粧水と美容液はそれぞれ異なる役割を持ちます。グルコラ スキンで肌の水分バランスを整えた後にグルコラ セラムを重ねることで、より高いグルタチオンケア効果が期待できます。予算や肌の状態に応じてセラム単品から始めることも可能です。'),
    ('敏感肌でも使えますか？', 'グルコラ セラムは成分の品質管理が厳格な韓国ブランドから選定した製品です。ただし高濃度成分配合のため、初回使用前にパッチテストを実施してください。肌に異常を感じた場合は使用を中止してください。'),
    ('毎日使用できますか？', 'はい、朝晩の美容液ステップとして毎日ご使用いただけます。グルタチオンは継続使用することで透明感・くすみ改善効果を実感しやすくなります。28日間（肌のターンオーバー1サイクル）継続することをおすすめします。'),
    ('白玉注射の代わりになりますか？', 'グルコラ セラムはあくまでスキンケアであり、美容点滴（白玉注射）とは吸収経路が異なります。注射は静脈投与のため全身への作用と高い即効性があります。一方、グルコラ セラムは毎日継続できる利便性が強みです。クリニック施術を補完する日常ケアとしての活用をおすすめします。'),
    ('どんな肌悩みに特に向いていますか？', '透明感が出にくい・くすみが気になる・シミ・色素沈着・肌のハリ不足・乾燥が気になる方に特におすすめです。グルタチオン（メラニンアプローチ）×コラーゲン（ハリ・保湿）×ボルフィリン（ボリューム感）のトリプルアプローチで、肌全体の底上げを目指します。'),
]

serum_html = product_page(
    title='グルコラ セラム（美容液）の効果とは？グルタチオン30,000ppm配合の韓国美容液｜LUMINOVE',
    desc='LUMINOVEが取り扱うグルコラ セラムを徹底解説。グルタチオン30,000ppm×300Daコラーゲン×ボルフィリン配合。透明感・くすみ改善・ハリを目指す韓国発フラッグシップ美容液。',
    canonical='/products/glucola-serum.html',
    breadcrumb3='グルコラ セラム（美容液）',
    og_image='/images/product-serum.webp',
    product_name='グルコラ セラム（美容液）',
    brand='LUMINOVE / from the skin',
    stores_url='https://luminove.stores.jp/items/679c79bb4c088e04f7df3970',
    price='7200',
    review_body='グルタチオン30,000ppmという高濃度配合と300Daコラーゲン・ボルフィリンとの組み合わせを評価。透明感・ハリ・うるおいへのトータルアプローチが期待できる製品として選定。',
    article_tag_text='from the skin / グルコラシリーズ',
    h1_html='<h1><span style="display:block;">グルコラ セラム</span><span class="h1-sub">グルタチオン30,000ppm×コラーゲン×ボルフィリン<br>透明感のための韓国発フラッグシップ美容液</span></h1>',
    lead_text='グルコラシリーズの中核を担う、最高濃度の美容液。グルタチオン30,000ppm（3%）に超低分子300Daコラーゲンとボルフィリンを組み合わせ、透明感・ハリ・うるおいを集中ケア。美容液に本格的な成分量を求める方のための、from the skinのフラッグシップモデルです。',
    img_src='product-serum.webp',
    img_alt='グルコラ セラム（美容液）',
    sections_html=serum_sections,
    related_html=serum_related,
    faqs=serum_faqs,
)

with open('products/glucola-serum.html', 'w', encoding='utf-8') as f:
    f.write(serum_html)
print('  Created: products/glucola-serum.html')

# ======================================================
# TASK 2: glucola-skin.html
# ======================================================
print('\n=== TASK2: glucola-skin.html ===')

skin_sections = '''    <section class="article-section">
      <h2>グルコラ スキン（化粧水）とは</h2>
      <p>「グルコラ スキン」は、韓国発スキンケアブランド「from the skin」が展開するグルコラシリーズの化粧水です。グルタチオン・300Daコラーゲン・ラクトバシラス発酵エキスの3成分を配合し、"うるおいを与えながら肌の土台を整える"ファーストステップとして設計されています。</p>
      <p>化粧水は洗顔後、最初に使用するスキンケアのステップ。グルコラ スキンは単なる保湿に留まらず、グルタチオンによる透明感アプローチと、乳酸菌発酵エキスによる肌バリアサポートを同時に行う、韓国コスメらしい多機能な化粧水です。</p>
      <div class="cta-box">
        <p class="price">¥3,500<span>（税込）</span></p>
        <a href="https://luminove.stores.jp/items/679c7a41be9f7e04f4d0f9f9" target="_blank" rel="noopener" class="btn-primary">STORESで購入する →</a>
      </div>
    </section>

    <section class="article-section">
      <h2>注目の3成分を徹底解説</h2>

      <div class="ingredient-card">
        <h3>①グルタチオン<br>透明感ケアの主役成分を化粧水に</h3>
        <p>グルタチオンは美容クリニックの美容点滴でも使用されるアミノ酸由来の成分です。チロシナーゼ酵素の活性を抑えることでメラニン生成にアプローチし、活性酸素を除去する抗酸化作用も持ちます。化粧水として毎日使用することで、継続的に透明感・くすみ改善をサポートします。</p>
        <p>グルコラ スキンは、化粧水という日常ケアのステップにグルタチオンを組み込むことで、特別な手間なく高機能な成分を毎日肌に届けることができます。</p>
      </div>

      <div class="ingredient-card">
        <h3>②300Daコラーゲン<br>角質層まで届く超低分子コラーゲン</h3>
        <p>コラーゲンは通常、分子量が大きく皮膚の奥まで届きにくいとされていますが、300Daまで低分子化した「300Daコラーゲン」は角質層への浸透を考えて設計されています。化粧水として使用することで、水分補給と同時にコラーゲン由来の保湿・ハリアップをサポートします。</p>
      </div>

      <div class="ingredient-card">
        <h3>③ラクトバシラス発酵エキス<br>乳酸菌発酵由来の肌バリアサポート</h3>
        <p>ラクトバシラス発酵エキスは乳酸菌発酵由来の成分で、肌のバリア機能を整え、外的刺激への耐性をサポートします。乾燥・肌荒れが気になる方の肌基盤を整える成分として、グルタチオン・コラーゲンと組み合わせた三位一体のアプローチを実現しています。</p>
      </div>
    </section>

    <section class="article-section">
      <h2>使用方法</h2>
      <table class="spec-table">
        <tr><th>使用タイミング</th><td>洗顔後、最初に使用するステップ（美容液・乳液の前）</td></tr>
        <tr><th>使用量</th><td>適量（500円玉大程度）をコットンまたは手に取り、顔全体へ</td></tr>
        <tr><th>頻度</th><td>毎朝晩（1日2回）</td></tr>
        <tr><th>組み合わせ</th><td>グルコラ スキン→グルコラ セラム→グルコラ ローションの順がおすすめ</td></tr>
      </table>
      <div class="quote-box">
        <p>🌿 グルコラ スキンはグルコラシリーズのファーストステップ。洗顔後すぐに使用し、水分と成分を肌に浸透させてから、次のセラム・ローションを重ねることで、全ステップの効果が高まります。</p>
        <p class="quote-source">LUMINOVEおすすめの使い方</p>
      </div>
    </section>

    <section class="article-section">
      <h2>グルコラ セラム（美容液）との違い</h2>
      <p>同シリーズのグルコラ セラムはグルタチオン30,000ppmという最高濃度の美容液ですが、グルコラ スキンは化粧水として肌全体に水分と成分を届けることを目的としています。</p>
      <ul>
        <li>グルコラ スキン：肌全体の水分補給・バリア機能強化・透明感ケアの「ファーストステップ」</li>
        <li>グルコラ セラム：より高濃度のグルタチオンを集中的に届ける「美容液ステップ」</li>
      </ul>
      <p>2つを組み合わせることで、グルタチオンを化粧水と美容液の両ステップで継続的に摂取でき、より高いケア効果が期待できます。まず化粧水（スキン）から始め、ステップアップとしてセラムを追加するのもおすすめです。</p>
    </section>

    <section class="article-section">
      <h2>こんな方におすすめ</h2>
      <ul>
        <li>韓国コスメでグルタチオンケアを日常に取り入れたい方</li>
        <li>透明感・くすみ改善を毎日のスキンケアで継続したい方</li>
        <li>乾燥や肌バリアの低下が気になる方</li>
        <li>シンプルなスキンケアルーティンに成分量を求める方</li>
        <li>美容点滴（白玉注射）のようなグルタチオン成分を日常ケアとして取り入れたい方</li>
      </ul>
    </section>'''

skin_related = '''        <a href="/products/glucola-serum.html" class="related-card">
          <img src="../images/product-serum.webp" alt="グルコラ セラム（美容液）" loading="lazy" />
          <p>グルコラ<br>セラム（美容液）</p>
        </a>
        <a href="/products/glucola-cleansing-foam.html" class="related-card">
          <img src="../images/product-cleanser.webp" alt="グルコラ クレンジングフォーム" loading="lazy" />
          <p>グルコラ<br>クレンジングフォーム</p>
        </a>
        <a href="/products/glucola-suncream.html" class="related-card">
          <img src="../images/product-suncream.webp" alt="グルコラ サンクリーム" loading="lazy" />
          <p>グルコラ<br>サンクリーム</p>
        </a>'''

skin_faqs = [
    ('グルコラ スキンは化粧水として単独でも使えますか？', 'はい、グルコラ スキン単独でも、毎日のスキンケアステップとして十分に活用できます。グルタチオン・300Daコラーゲン・乳酸菌発酵エキスが配合されており、化粧水だけでも透明感・うるおい・バリアサポートにアプローチできます。'),
    ('化粧水の使用量はどのくらいですか？', '一般的な化粧水と同様、500円玉大程度を目安にしてください。コットンに含ませてパッティングする方法と、手のひらで押し込む方法どちらでも使用できます。乾燥が強い場合は重ね付けすることをおすすめします。'),
    ('敏感肌でも使えますか？', 'グルコラ スキンは低刺激処方を心がけた設計です。乳酸菌発酵エキスによる肌バリアサポートも配合されているため、敏感肌の方にも多くご使用いただいています。ただし初回はパッチテストを実施し、問題がないことを確認してからお使いください。'),
    ('毎日使用できますか？', 'はい、毎朝晩の洗顔後に使用するスキンケアルーティンの一環としてご使用ください。グルタチオンは継続使用することで透明感・くすみ改善の効果を実感しやすくなります。'),
    ('グルコラ セラム（美容液）と一緒に使ったほうがいいですか？', 'グルコラ スキン（化粧水）の後にグルコラ セラム（美容液）を重ねることで、グルタチオンの継続的なケアをダブルで行えます。まずスキンから始めて、より集中したケアを求める方にセラムを追加することをおすすめします。'),
    ('コットンと手、どちらで使う方がいいですか？', 'どちらでも使用できます。コットンでのパッティングは角質をやわらかくしながら成分を浸透させるのに適しています。手のひらで温めながら押し込む方法は、体温で成分が浸透しやすくなる利点があります。肌の状態や好みに合わせて選んでください。'),
    ('どんな肌悩みに特に向いていますか？', '透明感が出にくい・くすみが気になる・肌のバリアが弱い・乾燥しやすい方に特におすすめです。グルタチオンによる透明感アプローチ、300Daコラーゲンによる保湿・ハリ、乳酸菌発酵エキスによるバリアサポートの3つが毎日の化粧水ステップで実現できます。'),
]

skin_html = product_page(
    title='グルコラ スキン（化粧水）の効果とは？グルタチオン×300Daコラーゲン配合の韓国化粧水｜LUMINOVE',
    desc='LUMINOVEが取り扱うグルコラ スキンを徹底解説。グルタチオン×300Daコラーゲン×乳酸菌発酵エキス配合。透明感・うるおい・肌バリアをトータルケアする韓国発ブライトニング化粧水。',
    canonical='/products/glucola-skin.html',
    breadcrumb3='グルコラ スキン（化粧水）',
    og_image='/images/product-skin.webp',
    product_name='グルコラ スキン（化粧水）',
    brand='LUMINOVE / from the skin',
    stores_url='https://luminove.stores.jp/items/679c7a41be9f7e04f4d0f9f9',
    price='3500',
    review_body='グルタチオン・300Daコラーゲン・乳酸菌発酵エキスの組み合わせによる透明感ケアと肌バリアサポートを評価。毎日の化粧水ステップで継続使用できる設計を選定。',
    article_tag_text='from the skin / グルコラシリーズ',
    h1_html='<h1><span style="display:block;">グルコラ スキン（化粧水）</span><span class="h1-sub">グルタチオン×300Daコラーゲン×乳酸菌発酵<br>透明感を育てる韓国発ブライトニング化粧水</span></h1>',
    lead_text='グルコラシリーズのファーストステップ。グルタチオン・300Daコラーゲン・ラクトバシラス発酵エキスを配合し、洗顔後すぐの肌に水分と美容成分を届けます。毎日の化粧水ルーティンで透明感・うるおい・肌バリアをトータルにケアしたい方のための、from the skinのブライトニング化粧水です。',
    img_src='product-skin.webp',
    img_alt='グルコラ スキン（化粧水）',
    sections_html=skin_sections,
    related_html=skin_related,
    faqs=skin_faqs,
)

with open('products/glucola-skin.html', 'w', encoding='utf-8') as f:
    f.write(skin_html)
print('  Created: products/glucola-skin.html')

# ======================================================
# TASK 3: doctor/index.html 修正
# ======================================================
print('\n=== TASK3: doctor/index.html修正 ===')

doctor_html = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ECTSQMJ4ME"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-ECTSQMJ4ME');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#2d4a3e" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" /></noscript>

  <title>LUMINOVEについて｜六本木BMC院長・大久保義徳が携わる韓国コスメセレクトショップ</title>
  <meta name="description" content="LUMINOVEは、六本木美容医療クリニック（BMC）院長・大久保義徳医師が代表を務める株式会社ルミノーブが運営する韓国コスメセレクトショップです。美容医療の知見を活かして商品選定に携わっています。" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://www.luminove.online/doctor/" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="LUMINOVEについて｜六本木BMC院長・大久保義徳が携わる韓国コスメセレクトショップ" />
  <meta property="og:description" content="LUMINOVEは、六本木美容医療クリニック（BMC）院長・大久保義徳医師が代表を務める株式会社ルミノーブが運営する韓国コスメセレクトショップです。美容医療の知見を活かして商品選定に携わっています。" />
  <meta property="og:url" content="https://www.luminove.online/doctor/" />
  <meta property="og:image" content="https://www.luminove.online/images/hero-all.webp" />
  <meta property="og:locale" content="ja_JP" />
  <meta property="og:site_name" content="LUMINOVE" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="LUMINOVEについて｜六本木BMC院長・大久保義徳が携わる韓国コスメセレクトショップ" />
  <meta name="twitter:description" content="LUMINOVEは、六本木美容医療クリニック（BMC）院長・大久保義徳医師が代表を務める株式会社ルミノーブが運営する韓国コスメセレクトショップです。" />
  <meta name="twitter:image" content="https://www.luminove.online/images/hero-all.webp" />

  <!-- JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type":"ListItem","position":1,"name":"TOP","item":"https://www.luminove.online/"},
      {"@type":"ListItem","position":2,"name":"LUMINOVEについて","item":"https://www.luminove.online/doctor/"}
    ]
  }
  </script>

  <!-- JSON-LD: Organization -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "株式会社ルミノーブ",
    "legalName": "株式会社ルミノーブ",
    "url": "https://www.luminove.online",
    "logo": "https://www.luminove.online/logo.png",
    "description": "六本木美容医療クリニック（BMC）院長・大久保義徳が代表を務める韓国コスメセレクトショップ。美容医療の知見を活かして、日本のお客様に届ける韓国スキンケアを選定しています。",
    "founder": {
      "@type": "Person",
      "name": "大久保 義徳",
      "jobTitle": "代表取締役・美容医療医師"
    }
  }
  </script>

  <!-- JSON-LD: FAQPage -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type":"Question","name":"LUMINOVEはどんなショップですか？","acceptedAnswer":{"@type":"Answer","text":"LUMINOVEは、株式会社ルミノーブが運営する韓国コスメのセレクトショップです。代表取締役の大久保義徳（六本木美容医療クリニック院長）が、美容医療の知見を活かして品質面を重視して商品を選定しています。"}},
      {"@type":"Question","name":"大久保義徳医師はどのような役割ですか？","acceptedAnswer":{"@type":"Answer","text":"大久保義徳医師は株式会社ルミノーブの代表取締役として、LUMINOVEのブランド運営に携わっています。また六本木美容医療クリニック（BMC）の院長として美容医療を専門とし、成分やブランドコンセプト・品質面を重視した商品選定に関わっています。なお、取り扱い商品の処方設計・製品開発は行っておりません。"}},
      {"@type":"Question","name":"取り扱い商品は医師が開発したものですか？","acceptedAnswer":{"@type":"Answer","text":"いいえ、LUMINOVEが取り扱う商品は韓国の各ブランドが独自に開発・製造しているものです。大久保義徳医師は商品の処方設計や製品開発には関わっておらず、美容医療の知見を活かして日本のお客様へ届ける商品を選定する役割を担っています。"}},
      {"@type":"Question","name":"六本木美容医療クリニック（BMC）とはどんなクリニックですか？","acceptedAnswer":{"@type":"Answer","text":"六本木美容医療クリニック（BMC）は東京・六本木に位置する美容医療専門クリニックです。美容医療を専門とし、大久保義徳医師が院長を務めています。LUMINOVEは同医師が代表を務める株式会社ルミノーブが運営しています。"}},
      {"@type":"Question","name":"商品選定の基準はどういうものですか？","acceptedAnswer":{"@type":"Answer","text":"LUMINOVEでは成分やブランドコンセプト・品質面を重視して商品を選定しています。グルタチオン・PDRN・NMN・RG3など、美容医療でも注目される成分を配合した韓国ブランドを中心にセレクトしています。"}}
    ]
  }
  </script>

  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --green-deep: #2d4a3e; --green-mid: #4a7c67; --green-light: #7db89a;
      --green-pale: #d4ede4; --green-mist: #f0f8f4; --cream: #faf8f3;
      --warm-white: #ffffff; --text-dark: #1a2a23; --text-mid: #4a5c54;
      --text-light: #8a9e96; --gold: #c8a96a;
      --font-serif: 'Cormorant Garamond','Hiragino Mincho ProN',serif;
      --font-sans: 'Noto Sans JP',sans-serif;
      --radius: 12px; --shadow: 0 8px 40px rgba(45,74,62,.10);
      --shadow-hover: 0 16px 56px rgba(45,74,62,.18);
      --transition: .35s cubic-bezier(.4,0,.2,1);
    }
    html { scroll-behavior: smooth; }
    body { font-family: var(--font-sans); color: var(--text-dark); background: var(--cream); line-height: 1.8; overflow-x: hidden; }
    a { color: inherit; text-decoration: none; }
    img { display: block; width: 100%; }
    #header { position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; padding: 0 5%; display: flex; align-items: center; justify-content: space-between; height: 72px; background: rgba(250,248,243,.82); backdrop-filter: blur(8px); box-shadow: 0 1px 12px rgba(45,74,62,.06); transition: background var(--transition), box-shadow var(--transition); }
    #header.scrolled { background: rgba(250,248,243,.97); box-shadow: 0 2px 24px rgba(45,74,62,.10); }
    .logo { font-family: var(--font-serif); font-size: 1.75rem; font-weight: 500; letter-spacing: .2em; color: var(--green-deep); }
    .logo span { color: var(--green-mid); }
    nav { display: flex; gap: 2.5rem; align-items: center; }
    nav a { font-size: .8rem; letter-spacing: .15em; font-weight: 500; color: var(--text-mid); transition: color var(--transition); }
    nav a:hover { color: var(--green-deep); }
    .btn-nav { background: var(--green-deep); color: #fff !important; padding: .55rem 1.5rem; border-radius: 50px; letter-spacing: .12em; font-size: .78rem; }
    .hamburger { display: none; cursor: pointer; flex-direction: column; gap: 5px; padding: 4px; }
    .hamburger span { display: block; width: 24px; height: 2px; background: var(--green-deep); border-radius: 2px; }
    .mobile-nav { display: none; position: fixed; inset: 0; z-index: 1001; background: var(--cream); flex-direction: column; align-items: center; justify-content: center; gap: 2.5rem; }
    .mobile-nav.open { display: flex; }
    .mobile-nav a { font-family: var(--font-serif); font-size: 1.75rem; color: var(--green-deep); letter-spacing: .1em; }
    .close-btn { position: absolute; top: 1.5rem; right: 5%; font-size: 1.75rem; cursor: pointer; color: var(--green-deep); background: none; border: none; }
    .btn-primary { display: inline-block; background: var(--green-deep); color: #fff; padding: .9rem 2.4rem; border-radius: 50px; font-size: .85rem; letter-spacing: .12em; font-weight: 500; text-align: center; transition: background var(--transition), transform var(--transition); }
    .btn-primary:hover { background: var(--green-mid); transform: translateY(-2px); }
    .btn-outline { display: inline-block; border: 1.5px solid var(--green-deep); color: var(--green-deep); padding: .9rem 2.4rem; border-radius: 50px; font-size: .85rem; letter-spacing: .12em; font-weight: 500; text-align: center; transition: all var(--transition); }
    .btn-outline:hover { background: var(--green-pale); transform: translateY(-2px); }

    .article-wrap { max-width: 860px; margin: 0 auto; padding: 110px 5% 4rem; }
    .article-tag { display: inline-block; font-size: .72rem; letter-spacing: .2em; font-weight: 500; color: var(--green-mid); background: var(--green-pale); padding: .4rem 1.2rem; border-radius: 50px; margin-bottom: 1.2rem; }
    h1.article-h1 { font-family: var(--font-serif); font-size: clamp(1.8rem,4vw,2.6rem); font-weight: 500; color: var(--green-deep); line-height: 1.4; margin-bottom: 1.2rem; }
    .article-lead { font-size: .95rem; color: var(--text-mid); border-left: 3px solid var(--green-light); padding-left: 1.2rem; margin-bottom: 3rem; line-height: 2; }
    .article-section { margin-bottom: 3rem; }
    .article-section h2 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 500; color: var(--green-deep); margin-bottom: 1rem; padding-bottom: .5rem; border-bottom: 1px solid var(--green-pale); }
    .article-section h3 { font-size: 1.05rem; font-weight: 600; color: var(--text-dark); margin: 1.5rem 0 .6rem; }
    .article-section p { color: var(--text-mid); margin-bottom: 1rem; line-height: 1.9; font-size: .92rem; }
    .article-section ul { padding-left: 1.5rem; color: var(--text-mid); line-height: 2; margin-bottom: 1rem; font-size: .92rem; }
    .profile-card { background: var(--warm-white); border-radius: var(--radius); padding: 2rem; box-shadow: var(--shadow); margin: 1.5rem 0; }
    .profile-card h3 { color: var(--green-deep); font-family: var(--font-serif); font-size: 1.3rem; margin-bottom: .5rem; }
    .profile-card .role { font-size: .82rem; color: var(--green-mid); letter-spacing: .1em; margin-bottom: 1.2rem; font-weight: 500; }
    .profile-card table { width: 100%; font-size: .88rem; color: var(--text-mid); }
    .profile-card tr { border-bottom: 1px solid var(--green-pale); }
    .profile-card th, .profile-card td { text-align: left; padding: .6rem 0; }
    .profile-card th { width: 9rem; color: var(--text-dark); font-weight: 500; }
    .notice-box { background: #fff8ec; border: 1px solid #e8d5a3; border-radius: var(--radius); padding: 1.2rem 1.5rem; margin: 1.5rem 0; }
    .notice-box p { font-size: .85rem; color: #7a5c2a; margin: 0; line-height: 1.9; }
    .notice-box strong { display: block; margin-bottom: .3rem; color: #5c4010; }
    .quote-box { background: var(--green-mist); border-left: 4px solid var(--green-light); border-radius: var(--radius); padding: 1.5rem 1.8rem; margin: 1.5rem 0; }
    .quote-box p { color: var(--text-dark); font-size: .92rem; margin-bottom: .8rem; }
    .quote-box .quote-source { font-size: .78rem; color: var(--text-light); margin-bottom: 0; }

    .related-section { max-width: 860px; margin: 0 auto 3rem; padding: 0 5%; }
    .related-section h2 { font-family: var(--font-serif); font-size: 1.4rem; color: var(--green-deep); margin-bottom: 1.5rem; padding-bottom: .5rem; border-bottom: 1px solid var(--green-pale); }
    .related-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; }
    .related-card { display: block; text-align: center; }
    .related-card img { border-radius: var(--radius); margin-bottom: .6rem; aspect-ratio: 1; object-fit: cover; }
    .related-card p { font-size: .82rem; color: var(--text-dark); font-weight: 500; }

    .faq-section { max-width: 860px; margin: 3rem auto; padding: 0 5%; }
    .faq-section h2 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 500; color: var(--green-deep); margin-bottom: 1.5rem; padding-bottom: .5rem; border-bottom: 1px solid var(--green-pale); }
    .faq-item { border-bottom: 1px solid var(--green-pale); }
    .faq-question { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; cursor: pointer; padding: 1.2rem 0; font-weight: 500; color: var(--text-dark); list-style: none; }
    .faq-question::marker, .faq-question::-webkit-details-marker { display: none; }
    .faq-icon { flex-shrink: 0; width: 24px; height: 24px; border: 1px solid var(--green-mid); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--green-mid); font-size: .9rem; transition: transform var(--transition); }
    details[open] .faq-icon { transform: rotate(45deg); }
    .faq-answer { padding: .25rem 0 1.2rem; color: var(--text-mid); line-height: 1.9; font-size: .92rem; }
    .back-link { text-align: center; margin: 3rem auto 5rem; }

    footer { background: var(--text-dark); color: rgba(255,255,255,.65); padding: 60px 5% 30px; }
    .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr 1.8fr; gap: 3rem; margin-bottom: 3rem; }
    .footer-brand .logo { color: #fff; margin-bottom: 1rem; }
    .footer-brand p { font-size: .83rem; line-height: 1.85; max-width: 260px; }
    .footer-col h4 { font-size: .78rem; letter-spacing: .18em; font-weight: 500; color: #fff; margin-bottom: 1.25rem; text-transform: uppercase; }
    .footer-col ul { list-style: none; display: flex; flex-direction: column; gap: .6rem; }
    .footer-col li a { font-size: .83rem; transition: color var(--transition); }
    .footer-col li a:hover { color: var(--green-light); }
    .footer-bottom { border-top: 1px solid rgba(255,255,255,.1); padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: .5rem; }
    .footer-bottom p, .footer-bottom a { font-size: .78rem; }
    .footer-bottom a { margin-left: 1.5rem; transition: color var(--transition); }
    .footer-bottom a:hover { color: var(--green-light); }
    @media (max-width: 1024px) { .footer-grid { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 768px) { nav { display: none; } .hamburger { display: flex; } .footer-grid { grid-template-columns: 1fr; gap: 2rem; } .related-grid { grid-template-columns: repeat(2,1fr); } .article-section h2 { font-size: 1.25rem; } }
  </style>
</head>
<body>

  <header id="header">
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
    <a href="/#brands" class="mobile-link">取扱ブランド</a>
    <a href="/#ingredients" class="mobile-link">成分</a>
    <a href="https://luminove.stores.jp/" target="_blank" rel="noopener" class="btn-primary mobile-link">SHOP NOW</a>
  </nav>

  <div class="article-wrap">
    <span class="article-tag">LUMINOVE / 運営について</span>
    <h1 class="article-h1">LUMINOVEについて<br>六本木BMC院長・大久保義徳が携わる韓国コスメセレクトショップ</h1>
    <p class="article-lead">LUMINOVEは、株式会社ルミノーブが運営する韓国コスメのセレクトショップです。代表取締役の大久保義徳（六本木美容医療クリニック院長）が、美容医療の知見を活かして品質面を重視した商品選定に携わっています。</p>

    <section class="article-section">
      <h2>代表取締役プロフィール</h2>
      <div class="profile-card">
        <h3>大久保 義徳（おおくぼ よしのり）</h3>
        <p class="role">株式会社ルミノーブ 代表取締役 ／ 六本木美容医療クリニック（BMC）院長</p>
        <table>
          <tr><th>所属クリニック</th><td>六本木美容医療クリニック（BMC）</td></tr>
          <tr><th>専門</th><td>美容医療</td></tr>
          <tr><th>役職</th><td>株式会社ルミノーブ 代表取締役</td></tr>
          <tr><th>クリニック公式</th><td><a href="https://bmc-roppongi.com/" target="_blank" rel="noopener" style="color:var(--green-mid);">bmc-roppongi.com</a></td></tr>
        </table>
      </div>

      <div class="notice-box">
        <strong>ご注意：LUMINOVEの商品について</strong>
        <p>LUMINOVEが取り扱う商品は、韓国の各ブランドが独自に開発・製造したものです。大久保義徳医師は商品の処方設計・製品開発・OEM開発には関わっておりません。美容医療の知見を活かして、日本のお客様へ届ける商品を選定する役割を担っています。</p>
      </div>
    </section>

    <section class="article-section">
      <h2>LUMINOVEの運営体制</h2>
      <p>LUMINOVEは2025年2月に設立された株式会社ルミノーブが運営する韓国コスメのセレクトショップです。代表取締役の大久保義徳が美容医療の専門家として、成分やブランドコンセプト・品質面を重視して取り扱い商品を選定しています。</p>
      <p>取り扱う韓国ブランドは、グルタチオン・PDRN・NMN・RG3など、美容医療でも注目される成分を配合したブランドを中心にセレクトしています。ブランドのコンセプトや品質管理体制、成分の配合方針などを確認した上で、日本のお客様に届ける商品として選定しています。</p>
    </section>

    <section class="article-section">
      <h2>商品選定のポリシー</h2>
      <p>LUMINOVEでは以下の観点で取り扱い商品を選定しています。</p>
      <ul>
        <li><strong>成分の妥当性</strong>：配合成分のコンセプトが明確であるか</li>
        <li><strong>配合濃度</strong>：主成分が実用的な濃度で配合されているか</li>
        <li><strong>ブランド品質</strong>：韓国での実績・製造管理体制が信頼できるか</li>
        <li><strong>日本への適合性</strong>：日本人の肌・ライフスタイルに合う商品か</li>
        <li><strong>ブランドコンセプト</strong>：LUMINOVEのセレクトショップとしての方向性と合致しているか</li>
      </ul>
      <div class="quote-box">
        <p>「美容医療の現場での知識を活かし、成分のコンセプトや品質面を大切にしながら、日本のお客様に本当に届けたい韓国スキンケアを選んでいます。」</p>
        <p class="quote-source">代表取締役 大久保義徳</p>
      </div>
    </section>

    <section class="article-section">
      <h2>六本木美容医療クリニック（BMC）について</h2>
      <p>六本木美容医療クリニック（BMC）は、東京・六本木に位置する美容医療専門クリニックです。大久保義徳医師が院長を務め、美容医療を提供しています。</p>
      <p>LUMINOVEは同医師が代表を務める株式会社ルミノーブが運営するセレクトショップです。クリニックとLUMINOVEは別組織ですが、代表が同一であることから、美容医療の知見がブランド運営の判断基準の一つとなっています。</p>
      <p><a href="https://bmc-roppongi.com/" target="_blank" rel="noopener" style="color:var(--green-mid);font-weight:500;">六本木美容医療クリニック（BMC）公式サイト →</a></p>
    </section>

    <section class="article-section">
      <h2>会社概要</h2>
      <div class="profile-card">
        <table>
          <tr><th>会社名</th><td>株式会社ルミノーブ</td></tr>
          <tr><th>代表取締役</th><td>池田 宏貴　大久保 義徳</td></tr>
          <tr><th>設立</th><td>2025年2月</td></tr>
          <tr><th>所在地</th><td>〒102-0094 東京都千代田区紀尾井町4番1号 ニューオータニガーデンコート28階</td></tr>
          <tr><th>事業内容</th><td>韓国コスメセレクトショップの運営・EC販売</td></tr>
          <tr><th>お問い合わせ</th><td><a href="mailto:info@luminove.online" style="color:var(--green-mid);">info@luminove.online</a></td></tr>
        </table>
      </div>
    </section>
  </div>

  <section class="related-section">
    <h2>LUMINOVEが選んだ商品を見る</h2>
    <div class="related-grid">
      <a href="/products/rejun-pdrn-cream.html" class="related-card">
        <img src="/images/product-rejun-cream.webp" alt="リジュエヌ クリーム" loading="lazy" />
        <p>リジュエヌ クリーム<br>PDRN×NMN</p>
      </a>
      <a href="/products/glucola-cleansing-foam.html" class="related-card">
        <img src="/images/product-cleanser.webp" alt="グルコラ クレンジングフォーム" loading="lazy" />
        <p>グルコラ<br>クレンジングフォーム</p>
      </a>
      <a href="/products/rg3-vital-ampoule.html" class="related-card">
        <img src="/images/product-rg3-serum.webp" alt="クイーンズ RG3 モイスチャーセラム" loading="lazy" />
        <p>クイーンズ RG3<br>モイスチャーセラム</p>
      </a>
    </div>
  </section>

  <section class="faq-section">
    <h2>よくある質問</h2>
    <details class="faq-item">
      <summary class="faq-question">LUMINOVEはどんなショップですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">LUMINOVEは、株式会社ルミノーブが運営する韓国コスメのセレクトショップです。代表取締役の大久保義徳（六本木美容医療クリニック院長）が、美容医療の知見を活かして品質面を重視して商品を選定しています。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">大久保義徳医師はどのような役割ですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">大久保義徳医師は株式会社ルミノーブの代表取締役として、LUMINOVEのブランド運営に携わっています。また六本木美容医療クリニック（BMC）の院長として美容医療を専門とし、成分やブランドコンセプト・品質面を重視した商品選定に関わっています。なお、取り扱い商品の処方設計・製品開発は行っておりません。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">取り扱い商品は医師が開発したものですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">いいえ、LUMINOVEが取り扱う商品は韓国の各ブランドが独自に開発・製造しているものです。大久保義徳医師は商品の処方設計や製品開発には関わっておらず、美容医療の知見を活かして日本のお客様へ届ける商品を選定する役割を担っています。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">六本木美容医療クリニック（BMC）とはどんなクリニックですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">六本木美容医療クリニック（BMC）は東京・六本木に位置する美容医療専門クリニックです。大久保義徳医師が院長を務めています。LUMINOVEは同医師が代表を務める株式会社ルミノーブが運営しています。</p>
    </details>
    <details class="faq-item">
      <summary class="faq-question">商品選定の基準はどういうものですか？<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">LUMINOVEでは成分のコンセプト・配合方針・ブランドの品質管理体制・日本人の肌への適合性などを確認した上で取り扱い商品を選定しています。グルタチオン・PDRN・NMN・RG3など、美容医療でも注目される成分を配合した韓国ブランドを中心にセレクトしています。</p>
    </details>
  </section>

  <div class="back-link">
    <a href="/" class="btn-outline">LUMINOVEトップへ →</a>
  </div>

  <footer>
    <div class="footer-grid">
      <div class="footer-brand">
        <span class="logo">LUMI<span style="color:var(--green-light)">NOVE</span></span>
        <p>光と愛を纏う肌へ。六本木の美容医師が商品選定に携わる韓国コスメセレクトショップ。</p>
      </div>
      <div class="footer-col">
        <h4>Products</h4>
        <ul>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">スキンケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">ハンドケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">ヘアケア</a></li>
          <li><a href="https://luminove.stores.jp/" target="_blank" rel="noopener">アクネケア</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/#about">ブランドストーリー</a></li>
          <li><a href="/doctor/">LUMINOVEについて</a></li>
          <li><a href="mailto:info@luminove.online">お問い合わせ</a></li>
          <li><a href="https://luminove.stores.jp/tokushoho" target="_blank" rel="noopener">特定商取引法</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>会社概要</h4>
        <address style="font-style:normal;font-size:.78rem;line-height:2;color:rgba(255,255,255,.55)">
          <span style="display:block;color:rgba(255,255,255,.8);font-weight:500;margin-bottom:.25rem">株式会社ルミノーブ</span>
          〒102-0094<br>東京都千代田区紀尾井町4番1号<br>ニューオータニガーデンコート28階<br>
          <span style="display:block;margin-top:.4rem">設立：2025年2月</span>
          <span style="display:block">代表取締役：池田 宏貴　大久保 義徳</span>
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 LUMINOVE. All rights reserved.</p>
      <a href="https://luminove.stores.jp/privacy_policy" target="_blank" rel="noopener">プライバシーポリシー</a>
      <a href="https://luminove.stores.jp/tokushoho" target="_blank" rel="noopener">特定商取引法に基づく表示</a>
    </div>
  </footer>

  <script>
    const header = document.getElementById('header');
    window.addEventListener('scroll', () => { header.classList.toggle('scrolled', window.scrollY > 40); });
    document.getElementById('hamburger').addEventListener('click', () => { document.getElementById('mobileNav').classList.toggle('open'); });
    document.getElementById('closeNav').addEventListener('click', () => { document.getElementById('mobileNav').classList.remove('open'); });
    document.querySelectorAll('.mobile-link').forEach(el => {
      el.addEventListener('click', () => { document.getElementById('mobileNav').classList.remove('open'); });
    });
  </script>
</body>
</html>'''

with open('doctor/index.html', 'w', encoding='utf-8') as f:
    f.write(doctor_html)
print('  Rewritten: doctor/index.html')

# sitemap 更新
print('\n=== sitemap.xml 更新 ===')
with open('sitemap.xml', encoding='utf-8') as f:
    sm = f.read()

new_entries = '''  <url>
    <loc>https://www.luminove.online/products/glucola-serum.html</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.luminove.online/products/glucola-skin.html</loc>
    <lastmod>2026-06-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''
if 'glucola-serum' not in sm:
    sm = sm.replace('</urlset>', new_entries + '</urlset>')
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sm)
    print('  sitemap.xml updated')

print('\n=== 全タスク完了 ===')
