# -*- coding: utf-8 -*-
"""
SEO記事10本を /blog/ に生成
各記事に reel_title/hook/script/caption/hashtags のJSONを埋め込み(AI記事自動生成/Instagramリール生成用)
"""
import json, os

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
    .article-body { max-width: 720px; margin: 0 auto; padding: 0 5% 4rem; }
    .article-section { margin-bottom: 3rem; }
    .article-section h2 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 500; color: var(--green-deep); margin-bottom: 1rem; padding-bottom: .6rem; border-bottom: 1px solid var(--green-pale); }
    .article-section h3 { font-size: 1.05rem; font-weight: 600; color: var(--text-dark); margin: 1.5rem 0 .6rem; }
    .article-section p { font-size: .92rem; color: var(--text-mid); margin-bottom: 1rem; line-height: 1.9; }
    .article-section ul, .article-section ol { font-size: .92rem; color: var(--text-mid); margin: 0 0 1rem 1.4rem; line-height: 1.9; }
    .article-section li { margin-bottom: .4rem; }
    .article-section a { color: var(--green-mid); text-decoration: underline; }
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
        <h4>成分解説</h4>
        <ul>
          <li><a href="/ingredients/glutathione.html">グルタチオン</a></li>
          <li><a href="/ingredients/nano-collagen.html">ナノコラーゲン（300Da）</a></li>
          <li><a href="/ingredients/pdrn.html">PDRN</a></li>
          <li><a href="/ingredients/rg3.html">RG3</a></li>
          <li><a href="/ingredients/nmn.html">NMN</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/blog/">ブログ</a></li>
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


def render_article(a):
    """a: dict with slug,title,meta_desc,tag,h1,lead,sections(list of (h2,html)),faq(list of (q,a)),
           related(list of (url,img,name)),reel(dict)"""
    faq_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
            for q, ans in a['faq']
        ]
    }, ensure_ascii=False)

    breadcrumb_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TOP", "item": "https://www.luminove.online/"},
            {"@type": "ListItem", "position": 2, "name": "ブログ", "item": "https://www.luminove.online/blog/"},
            {"@type": "ListItem", "position": 3, "name": a['h1_plain'], "item": f"https://www.luminove.online/blog/{a['slug']}.html"}
        ]
    }, ensure_ascii=False)

    article_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a['h1_plain'],
        "description": a['meta_desc'],
        "url": f"https://www.luminove.online/blog/{a['slug']}.html",
        "image": a['image'],
        "publisher": {"@type": "Organization", "name": "LUMINOVE", "url": "https://www.luminove.online"},
        "datePublished": "2026-06-22",
        "dateModified": "2026-06-22"
    }, ensure_ascii=False)

    # AI記事自動生成/リール生成用データ
    reel_jsonld = json.dumps({"reel": a['reel']}, ensure_ascii=False, indent=2)

    sections_html = ''
    for h2, body in a['sections']:
        sections_html += f'''
    <section class="article-section">
      <h2>{h2}</h2>
{body}
    </section>
'''

    faq_html = ''
    for q, ans in a['faq']:
        faq_html += f'''    <details class="faq-item">
      <summary class="faq-question">{q}<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">{ans}</p>
    </details>
'''

    related_html = ''
    for url, img, name in a['related']:
        related_html += f'''      <a href="{url}" class="related-card">
        <img src="{img}" alt="{name}" loading="lazy" />
        <p>{name}</p>
      </a>
'''

    toc_html = ''
    for i, (h2, _) in enumerate(a['sections']):
        anchor = f"sec{i+1}"
        toc_html += f'        <li><a href="#{anchor}">{h2}</a></li>\n'

    # アンカーID付与
    sections_html2 = ''
    for i, (h2, body) in enumerate(a['sections']):
        anchor = f"sec{i+1}"
        sections_html2 += f'''
    <section class="article-section" id="{anchor}">
      <h2>{h2}</h2>
{body}
    </section>
'''

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ECTSQMJ4ME"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-ECTSQMJ4ME');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <title>{a['title']}</title>
  <meta name="description" content="{a['meta_desc']}" />
  <link rel="canonical" href="https://www.luminove.online/blog/{a['slug']}.html" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{a['title']}" />
  <meta property="og:description" content="{a['meta_desc']}" />
  <meta property="og:url" content="https://www.luminove.online/blog/{a['slug']}.html" />
  <meta property="og:image" content="{a['image']}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
  {article_jsonld}
  </script>
  <script type="application/ld+json">
  {breadcrumb_jsonld}
  </script>
  <script type="application/ld+json">
  {faq_jsonld}
  </script>
  <!-- AI記事自動生成 / Instagramリール生成用データ -->
  <script type="application/json" id="reel-data">
  {reel_jsonld}
  </script>
  <style>{BLOG_CSS}</style>
</head>
<body>
{BLOG_HEADER}

  <nav class="breadcrumb">
    <a href="/">TOP</a> ＞ <a href="/blog/">ブログ</a> ＞ {a['h1_plain']}
  </nav>

  <article class="article-hero">
    <span class="article-tag">{a['tag']}</span>
    <h1>{a['h1']}</h1>
    <p class="article-meta">2026年6月22日 ｜ LUMINOVE編集部</p>
    <p class="article-lead">{a['lead']}</p>
  </article>

  <div class="article-body">
{sections_html2}
  </div>

  <section class="faq-section" id="faq">
    <h2>よくある質問</h2>
{faq_html}  </section>

  <section class="related-section">
    <h2>関連記事・ページ</h2>
    <div class="related-grid">
{related_html}    </div>
  </section>

  <div class="back-link">
    <a href="/" class="btn-outline">LUMINOVEトップへ →</a>
  </div>

{BLOG_FOOTER}
</body>
</html>'''
    return html


ARTICLES = [
    dict(
        slug="glutathione-skincare",
        title="グルタチオン化粧品とは？韓国スキンケアで人気の理由｜LUMINOVE",
        meta_desc="グルタチオン化粧品とは何か、韓国スキンケアでなぜ人気なのかを解説。美容点滴の主成分が日常ケアに広がった理由とLUMINOVEの取り扱い商品を紹介します。",
        tag="成分コラム / グルタチオン",
        h1="グルタチオン化粧品とは？<br>韓国スキンケアで人気の理由",
        h1_plain="グルタチオン化粧品とは？韓国スキンケアで人気の理由",
        image="https://www.luminove.online/images/product-serum.webp",
        lead="美容点滴（白玉注射）の主成分として知られるグルタチオン。韓国コスメ業界ではこの成分を化粧品に高濃度配合する技術が進み、人気の美容成分として定着しました。なぜグルタチオン化粧品が選ばれているのか、その理由を解説します。",
        sections=[
            ("グルタチオン化粧品とは", "      <p>グルタチオンは、グルタミン酸・システイン・グリシンの3つのアミノ酸からなるトリペプチドで、強力な抗酸化作用を持つ成分です。美容クリニックの点滴施術として知られていましたが、近年は化粧品への配合技術が進み、化粧水・美容液・洗顔料など幅広いアイテムに採用されています。</p>"),
            ("韓国スキンケアで人気の理由", "      <p>韓国コスメブランドは機能性成分の高濃度配合に積極的で、グルタチオンも数千〜数万ppmという高濃度で配合する製品が登場しています。一般的な化粧品の配合量を大きく上回ることが、韓国グルタチオン化粧品の特徴です。</p><ul><li>抗酸化ケアへの注目度の高さ</li><li>高濃度配合技術の進歩</li><li>美容医療との親和性の高さ</li></ul>"),
            ("選び方のポイント", "      <p>配合量（ppm表記）と、組み合わせる成分（コラーゲン・ビタミンC誘導体など）を確認しましょう。詳しい仕組みは<a href=\"/ingredients/glutathione.html\">グルタチオン成分解説ページ</a>で解説しています。</p><div class=\"cta-box\"><p>グルタチオン30,000ppm配合の美容液</p><a href=\"/products/glucola-serum.html\" class=\"btn-primary\">グルコラ セラムを見る →</a></div>"),
        ],
        faq=[
            ("グルタチオン化粧品は誰でも使えますか？", "体内にも存在する成分のため低刺激とされていますが、配合される他成分により異なります。初回はパッチテストをおすすめします。"),
            ("どのくらいの期間で実感できますか？", "肌のターンオーバー周期である28日間を目安に、継続使用することをおすすめします。"),
            ("美容点滴と併用しても良いですか？", "はい、点滴施術を補完するホームケアとして併用される方が多くいらっしゃいます。"),
        ],
        related=[
            ("/ingredients/glutathione.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオン<br>成分詳細ページ"),
            ("/blog/glutathione-what-is.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオンとは？<br>成分解説"),
            ("/products/glucola-serum.html", "https://www.luminove.online/images/product-serum.webp", "グルコラ セラム<br>（美容液）"),
        ],
        reel=dict(
            reel_title="韓国で話題！グルタチオン化粧品って何？",
            hook="美容点滴の主成分が、まさかスキンケアに使えるって知ってた？",
            script="グルタチオンって聞いたことある？美容点滴の主成分なんだけど、韓国コスメでは高濃度で化粧品に配合されてるの。抗酸化ケアに注目の成分で、毎日のスキンケアに取り入れられるのが魅力。気になる人は概要欄から成分解説をチェックしてみて。",
            caption="美容点滴の主成分「グルタチオン」がスキンケアに。韓国コスメの高濃度配合技術で毎日のケアに取り入れやすくなりました✨ #グルタチオン #韓国コスメ",
            hashtags=["#グルタチオン", "#韓国コスメ", "#美容成分", "#スキンケア", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="nano-collagen",
        title="ナノコラーゲンとは？低分子コラーゲンが注目される理由｜LUMINOVE",
        meta_desc="ナノコラーゲンとは何か、低分子化されたコラーゲンが韓国スキンケアで注目される理由を解説。一般的なコラーゲンとの違いもわかりやすく紹介します。",
        tag="成分コラム / ナノコラーゲン",
        h1="ナノコラーゲンとは？<br>低分子コラーゲンが注目される理由",
        h1_plain="ナノコラーゲンとは？低分子コラーゲンが注目される理由",
        image="https://www.luminove.online/images/product-skin.webp",
        lead="「ナノコラーゲン」という言葉を韓国コスメでよく見かけるようになりました。通常のコラーゲンとどう違うのか、なぜ注目されているのかを解説します。",
        sections=[
            ("ナノコラーゲンとは", "      <p>ナノコラーゲンとは、分子量を大幅に小さくした低分子コラーゲンのことです。代表的な指標として「300Da（ダルトン）」という分子量が使われ、通常のコラーゲン（数千〜数万Da）と比較して極めて小さいサイズです。</p>"),
            ("注目される理由", "      <p>分子サイズが小さいほど、肌表面の角質層まで届きやすいとされています。韓国コスメブランドはこの低分子化技術を競って導入し、化粧水・美容液・洗顔料にまでナノコラーゲンを配合する製品が増えています。</p>"),
            ("一般的なコラーゲンとの違い", "      <p>一般的なコラーゲンは肌表面に保湿膜を作る働きが中心ですが、ナノコラーゲンは角質層までうるおいを届けやすい設計です。詳しくは<a href=\"/ingredients/nano-collagen.html\">ナノコラーゲン成分解説ページ</a>をご覧ください。</p><div class=\"cta-box\"><p>ナノコラーゲン×グルタチオン配合の化粧水</p><a href=\"/products/glucola-skin.html\" class=\"btn-primary\">グルコラ スキンを見る →</a></div>"),
        ],
        faq=[
            ("ナノコラーゲンは安全ですか？", "コラーゲン自体は比較的低刺激な成分です。敏感肌の方は初回使用前にパッチテストをおすすめします。"),
            ("どんな製品に配合されていますか？", "化粧水・美容液・クリーム・洗顔料など幅広いアイテムに配合されています。"),
            ("グルタチオンと併用できますか？", "はい、グルコラシリーズのように両成分を組み合わせた製品が人気です。"),
        ],
        related=[
            ("/ingredients/nano-collagen.html", "https://www.luminove.online/images/product-skin.webp", "ナノコラーゲン<br>成分詳細ページ"),
            ("/ingredients/glutathione.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオン<br>成分詳細ページ"),
            ("/products/glucola-skin.html", "https://www.luminove.online/images/product-skin.webp", "グルコラ スキン<br>（化粧水）"),
        ],
        reel=dict(
            reel_title="ナノコラーゲンって普通のコラーゲンと違うの？",
            hook="コラーゲンを「ナノ化」するとどう変わるか知ってる？",
            script="韓国コスメでよく見る「ナノコラーゲン」。実は分子サイズをめちゃ小さくしたコラーゲンのことなの。普通のコラーゲンより角質層まで届きやすい設計が特徴。うるおい重視派は要チェック。",
            caption="韓国コスメで話題の「ナノコラーゲン」。300Daまで低分子化された注目成分です💧 #ナノコラーゲン #韓国コスメ",
            hashtags=["#ナノコラーゲン", "#コラーゲン", "#韓国コスメ", "#美容成分", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="pdrn-skincare",
        title="PDRN化粧品とは？韓国コスメで注目される理由｜LUMINOVE",
        meta_desc="PDRN化粧品とは何か、韓国コスメでなぜ注目されるのかを解説。サーモン由来DNA成分の特徴とLUMINOVEの取り扱い商品を紹介します。",
        tag="成分コラム / PDRN",
        h1="PDRN化粧品とは？<br>韓国コスメで注目される理由",
        h1_plain="PDRN化粧品とは？韓国コスメで注目される理由",
        image="https://www.luminove.online/images/product-rejun-cream.webp",
        lead="再生医療の分野で研究されるPDRN。韓国コスメでは「水光注射成分」として知られるこの成分をスキンケアに応用する技術が進んでいます。注目される理由を解説します。",
        sections=[
            ("PDRN化粧品とは", "      <p>PDRN（ポリデオキシリボヌクレオチド）は、サーモン由来のDNA断片です。美容医療の水光注射として知られていましたが、韓国コスメではこの成分を化粧品に配合する技術が進んでいます。</p>"),
            ("注目される理由", "      <p>美容施術後のダウンタイムケアや、肌のリズムを整えるケア成分として注目されています。「28日ルーティンケア」という言葉とともに、韓国コスメ市場で急速に普及しました。</p>"),
            ("LUMINOVEのPDRN配合商品", "      <p>詳しい仕組みは<a href=\"/ingredients/pdrn.html\">PDRN成分解説ページ</a>をご覧ください。</p><div class=\"cta-box\"><p>PDRN×NMNのデュアルフォーミュラ</p><a href=\"/products/rejun-pdrn-cream.html\" class=\"btn-primary\">リジュエヌ クリームを見る →</a></div>"),
        ],
        faq=[
            ("PDRNは安全な成分ですか？", "サーモン由来の成分で、医療分野でも研究が進む成分です。敏感肌の方はパッチテストをおすすめします。"),
            ("どんな肌悩みに向いていますか？", "施術後のダウンタイムケア、肌のコンディション調整を目的とした製品が多くあります。"),
            ("毎日使用できますか？", "製品によって設計は異なりますが、毎日のケアに使用できる設計のものが多くあります。"),
        ],
        related=[
            ("/ingredients/pdrn.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRN<br>成分詳細ページ"),
            ("/blog/pdrn-what-is.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRNとは？<br>成分解説"),
            ("/products/rejun-pdrn-cream.html", "https://www.luminove.online/images/product-rejun-cream.webp", "リジュエヌ クリーム<br>（PDRN×NMN）"),
        ],
        reel=dict(
            reel_title="水光注射の成分がスキンケアに？PDRNとは",
            hook="サーモンのDNAが美容成分になるって知ってた？",
            script="PDRNって聞いたことある？サーモン由来のDNA断片で、水光注射でも使われる成分なの。韓国コスメではこれをクリームに配合した製品が人気。施術後ケアにもおすすめなんだって。",
            caption="水光注射でも使われる「PDRN」がスキンケアに。サーモン由来のDNA成分が韓国コスメで話題です🧬 #PDRN #韓国コスメ",
            hashtags=["#PDRN", "#韓国コスメ", "#美容成分", "#スキンケア", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="korean-skincare-routine",
        title="韓国スキンケアの順番とは？基本ステップを解説｜LUMINOVE",
        meta_desc="韓国スキンケアの正しい順番とは？クレンジングから保湿までの基本ステップと、各ステップで使いたい成分をわかりやすく解説します。",
        tag="ルーティン / 韓国スキンケア",
        h1="韓国スキンケアの順番とは？<br>基本ステップを解説",
        h1_plain="韓国スキンケアの順番とは？基本ステップを解説",
        image="https://www.luminove.online/images/product-cleanser.webp",
        lead="韓国スキンケアは多層的なケアが特徴と言われますが、基本となる順番を押さえれば毎日のルーティンは難しくありません。基本ステップを解説します。",
        sections=[
            ("基本の順番", "      <ol><li>クレンジング・洗顔</li><li>化粧水（スキン）</li><li>美容液（セラム）</li><li>乳液・クリーム</li><li>日焼け止め（朝のみ）</li></ol><p>「水分の多いものから少ないものへ」が基本の考え方です。</p>"),
            ("各ステップで意識したいこと", "      <p>洗顔ではうるおいを取りすぎないこと、化粧水では肌を柔らかくしてから美容液を重ねること、保湿ステップでは成分を逃さず閉じ込めることがポイントです。</p>"),
            ("成分で選ぶルーティン例", "      <p>グルタチオン×ナノコラーゲンのグルコラシリーズなら、洗顔から日焼け止めまで同じ成分軸で揃えられます。</p><div class=\"cta-box\"><p>グルタチオン×ナノコラーゲンで揃えるルーティン</p><a href=\"/#products\" class=\"btn-primary\">グルコラシリーズを見る →</a></div>"),
        ],
        faq=[
            ("ステップは多いほど良いですか？", "必ずしも多いほど良いわけではありません。肌の状態や時間に合わせて、無理なく続けられる数に調整することが大切です。"),
            ("朝と夜でステップは変えるべきですか？", "朝は日焼け止めを追加し、夜はクレンジングを重視するなど、目的に応じて調整するのが一般的です。"),
            ("初心者はどこから始めるべきですか？", "まずは洗顔と化粧水の2ステップから始め、徐々に美容液・保湿を追加していくのがおすすめです。"),
        ],
        related=[
            ("/products/glucola-cleansing-foam.html", "https://www.luminove.online/images/product-cleanser.webp", "グルコラ<br>クレンジングフォーム"),
            ("/products/glucola-skin.html", "https://www.luminove.online/images/product-skin.webp", "グルコラ スキン<br>（化粧水）"),
            ("/products/glucola-serum.html", "https://www.luminove.online/images/product-serum.webp", "グルコラ セラム<br>（美容液）"),
        ],
        reel=dict(
            reel_title="韓国スキンケアの正しい順番、知ってる？",
            hook="その順番、実は間違ってるかも？",
            script="韓国スキンケアの基本は「水分の多いものから少ないものへ」。クレンジング→化粧水→美容液→乳液の順が基本。難しく考えずに、この順番だけ覚えればOK。",
            caption="韓国スキンケアの基本ステップをおさらい。水分量の多い順に重ねるのがポイントです✨ #韓国スキンケア #スキンケアルーティン",
            hashtags=["#韓国スキンケア", "#スキンケアルーティン", "#美容", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="glutathione-serum",
        title="グルタチオン美容液の選び方｜LUMINOVE",
        meta_desc="グルタチオン美容液の選び方を解説。配合濃度（ppm）の見方や、組み合わせ成分のチェックポイントをわかりやすく紹介します。",
        tag="選び方ガイド / グルタチオン美容液",
        h1="グルタチオン美容液の選び方",
        h1_plain="グルタチオン美容液の選び方",
        image="https://www.luminove.online/images/product-serum.webp",
        lead="グルタチオン美容液は配合濃度や組み合わせ成分によって特徴が大きく異なります。失敗しない選び方のポイントを解説します。",
        sections=[
            ("配合濃度（ppm）を確認する", "      <p>グルタチオンの配合量はppm表記が一般的です。10,000ppm以上であれば高濃度の部類に入ります。LUMINOVEのグルコラ セラムは30,000ppm（3%）配合です。</p>"),
            ("組み合わせ成分を確認する", "      <p>グルタチオン単体よりも、コラーゲンやビタミンC誘導体などと組み合わせた製品の方が相乗効果が期待できます。グルコラ セラムは300Daコラーゲン・ボルフィリンとの組み合わせです。</p>"),
            ("テクスチャーと使うタイミング", "      <p>化粧水のあと、乳液の前のステップで使用するのが基本です。詳しくは<a href=\"/ingredients/glutathione.html\">グルタチオン成分解説ページ</a>をご覧ください。</p><div class=\"cta-box\"><p>グルタチオン30,000ppm配合の美容液</p><a href=\"/products/glucola-serum.html\" class=\"btn-primary\">グルコラ セラムを見る →</a></div>"),
        ],
        faq=[
            ("ppmが高いほど良いのですか？", "高濃度であるほど成分量は多くなりますが、肌質や他の配合成分との相性も重要です。"),
            ("どのくらいの期間で使い切るのが理想ですか？", "開封後は品質保持の観点から、3〜6ヶ月程度を目安に使い切ることをおすすめします。"),
            ("乾燥肌でも使えますか？", "保湿成分と組み合わされた製品であれば、乾燥肌の方にも使いやすい設計です。"),
        ],
        related=[
            ("/ingredients/glutathione.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオン<br>成分詳細ページ"),
            ("/products/glucola-serum.html", "https://www.luminove.online/images/product-serum.webp", "グルコラ セラム<br>（美容液）"),
            ("/products/glucola-skin.html", "https://www.luminove.online/images/product-skin.webp", "グルコラ スキン<br>（化粧水）"),
        ],
        reel=dict(
            reel_title="グルタチオン美容液、選び方のコツ",
            hook="その美容液、配合量ちゃんと見てる？",
            script="グルタチオン美容液選びで大事なのはppm表記。1万ppm以上なら高濃度の部類。あとはコラーゲンとかと組み合わさってるかも要チェック。",
            caption="グルタチオン美容液は配合濃度（ppm）と組み合わせ成分をチェックするのがポイントです✨ #グルタチオン美容液 #韓国コスメ",
            hashtags=["#グルタチオン", "#美容液", "#韓国コスメ", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="pdrn-nmn-cream",
        title="PDRN×NMNクリームとは？相乗効果を解説｜LUMINOVE",
        meta_desc="PDRN×NMNクリームとは何か、2つの成分を組み合わせる意味と相乗効果を解説。LUMINOVEのリジュエヌ クリームの特徴も紹介します。",
        tag="成分コラム / PDRN×NMN",
        h1="PDRN×NMNクリームとは？<br>相乗効果を解説",
        h1_plain="PDRN×NMNクリームとは？相乗効果を解説",
        image="https://www.luminove.online/images/product-rejun-cream.webp",
        lead="韓国コスメで見かける「PDRN×NMN」配合クリーム。それぞれ異なるアプローチを持つ2成分を組み合わせる理由を解説します。",
        sections=[
            ("PDRNとNMN、それぞれの特徴", "      <p>PDRNはサーモン由来のDNA断片で、細胞の修復・再生に関わる成分です。NMNは細胞エネルギー（NAD+）の前駆体で、アンチエイジング研究で注目される成分です。</p>"),
            ("組み合わせる理由", "      <p>PDRNが肌コンディションへのアプローチ、NMNが内側からのハリ・活力ケアへのアプローチと役割が異なるため、組み合わせることで相補的な効果が期待できます。</p>"),
            ("LUMINOVEのPDRN×NMNクリーム", "      <p>リジュエヌ クリームはPDRN3000ppm×NMN1000ppmのデュアルフォーミュラを採用しています。詳しくは<a href=\"/ingredients/nmn.html\">NMN成分解説ページ</a>もご覧ください。</p><div class=\"cta-box\"><p>PDRN×NMNのデュアルフォーミュラ</p><a href=\"/products/rejun-pdrn-cream.html\" class=\"btn-primary\">リジュエヌ クリームを見る →</a></div>"),
        ],
        faq=[
            ("PDRNとNMNは併用しても安全ですか？", "それぞれ異なる作用を持つ成分で、併用されることを前提に設計された製品が多くあります。"),
            ("どんな肌悩みに向いていますか？", "施術後のダウンタイムケアやニキビ跡、肌コンディションが気になる方に向いています。"),
            ("毎日使用できますか？", "製品設計によりますが、リジュエヌ クリームは毎日のケアに使用できる低刺激処方です。"),
        ],
        related=[
            ("/ingredients/pdrn.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRN<br>成分詳細ページ"),
            ("/ingredients/nmn.html", "https://www.luminove.online/images/product-rejun-cream.webp", "NMN<br>成分詳細ページ"),
            ("/products/rejun-pdrn-cream.html", "https://www.luminove.online/images/product-rejun-cream.webp", "リジュエヌ クリーム<br>（PDRN×NMN）"),
        ],
        reel=dict(
            reel_title="PDRNとNMN、一緒に使うとどうなる？",
            hook="2つの成分を組み合わせる理由、知ってる？",
            script="PDRNは細胞修復系、NMNはエネルギー系のアプローチ。役割が違うから組み合わせると相補的な効果が期待できるの。韓国コスメではこの2つを配合したクリームが人気。",
            caption="PDRN×NMNの組み合わせで、異なるアプローチを同時にケア。リジュエヌ クリームで採用されています🧬 #PDRN #NMN #韓国コスメ",
            hashtags=["#PDRN", "#NMN", "#韓国コスメ", "#美容成分", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="korean-sunscreen",
        title="韓国日焼け止めの選び方｜LUMINOVE",
        meta_desc="韓国日焼け止めの選び方を解説。SPF・PA値の見方や、機能性化粧品認証の意味、テクスチャーの違いをわかりやすく紹介します。",
        tag="選び方ガイド / 韓国日焼け止め",
        h1="韓国日焼け止めの選び方",
        h1_plain="韓国日焼け止めの選び方",
        image="https://www.luminove.online/images/product-suncream.webp",
        lead="韓国日焼け止めは機能性・使用感ともに進化が著しいカテゴリーです。選び方のポイントをわかりやすく解説します。",
        sections=[
            ("SPF・PA値の見方", "      <p>SPFは紫外線B波（UVB）への防御力、PAは紫外線A波（UVA）への防御力を示す指標です。日常使いならSPF30〜50、屋外活動が多い日はSPF50+ PA++++が目安です。</p>"),
            ("機能性化粧品認証について", "      <p>韓国では「シワ改善」「美白」などの機能性化粧品認証制度があります。認証を取得した日焼け止めは、UVカットに加えてこれらの機能性も兼ね備えていることが特徴です。</p>"),
            ("テクスチャーで選ぶ", "      <p>白浮きしにくい韓国日焼け止めは、メイク前の使用にも適しています。詳しくは商品ページをご覧ください。</p><div class=\"cta-box\"><p>UVカット×シワ改善×美白の3機能性</p><a href=\"/products/glucola-suncream.html\" class=\"btn-primary\">グルコラ サンクリームを見る →</a></div>"),
        ],
        faq=[
            ("日焼け止めだけでスキンケアになりますか？", "機能性化粧品認証を取得した製品であれば、UVケアと同時にエイジングケア・トーンケアも行えます。"),
            ("毎日塗り直しは必要ですか？", "屋外での活動時間が長い場合は、2〜3時間ごとの塗り直しをおすすめします。"),
            ("敏感肌でも使えますか？", "製品によって配合成分が異なるため、初回使用前にパッチテストをおすすめします。"),
        ],
        related=[
            ("/products/glucola-suncream.html", "https://www.luminove.online/images/product-suncream.webp", "グルコラ<br>サンクリーム"),
            ("/ingredients/glutathione.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオン<br>成分詳細ページ"),
            ("/ingredients/nano-collagen.html", "https://www.luminove.online/images/product-skin.webp", "ナノコラーゲン<br>成分詳細ページ"),
        ],
        reel=dict(
            reel_title="韓国日焼け止め、選び方のポイント3つ",
            hook="その日焼け止め、本当に合ってる？",
            script="韓国日焼け止め選びはSPF・PA値、機能性認証、テクスチャーの3つを見るのがコツ。白浮きしにくいものはメイク前にも使いやすいよ。",
            caption="韓国日焼け止めはSPF/PA値・機能性認証・テクスチャーの3つをチェック☀️ #韓国日焼け止め #UVケア",
            hashtags=["#韓国日焼け止め", "#UVケア", "#韓国コスメ", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="peeling-pack-how-to-use",
        title="ピールオフパックの使い方｜LUMINOVE",
        meta_desc="ピールオフパックの正しい使い方を解説。塗布から剥がすタイミングまでのステップと、使用頻度の目安をわかりやすく紹介します。",
        tag="使い方ガイド / ピールオフパック",
        h1="ピールオフパックの使い方",
        h1_plain="ピールオフパックの使い方",
        image="https://www.luminove.online/images/product-pack2.webp",
        lead="塗って剥がすピールオフパックは、正しい使い方を知ることでより心地よく使えます。基本ステップと使用頻度の目安を解説します。",
        sections=[
            ("基本の使い方", "      <ol><li>洗顔後、化粧水で肌を整える</li><li>目元・口元を避けて顔全体に薄くムラなく塗布</li><li>表示時間（目安15〜20分）乾かす</li><li>端からゆっくり剥がす</li><li>残った微量を優しくなじませる</li></ol>"),
            ("使用頻度の目安", "      <p>週1〜2回程度の使用が一般的です。肌の状態を見ながら頻度を調整してください。</p>"),
            ("剥がすときのポイント", "      <p>乾燥しすぎる前、表示時間内に剥がすのがポイントです。詳しくは商品ページをご覧ください。</p><div class=\"cta-box\"><p>高濃度グルタチオン×300Daコラーゲン配合</p><a href=\"/products/glucola-peeling-pack2.html\" class=\"btn-primary\">グルコラ ピリングパックⅡを見る →</a></div>"),
        ],
        faq=[
            ("毎日使っても良いですか？", "ピールオフパックは週1〜2回程度の使用が一般的です。毎日の使用は推奨されません。"),
            ("剥がしにくい場合はどうすれば良いですか？", "完全に乾燥しすぎると剥がしにくくなることがあります。表示時間を目安に、端から優しく剥がしてください。"),
            ("敏感肌でも使えますか？", "肌に直接密着するアイテムのため、敏感肌の方は初回使用前にパッチテストをおすすめします。"),
        ],
        related=[
            ("/products/glucola-peeling-pack2.html", "https://www.luminove.online/images/product-pack2.webp", "グルコラ<br>ピリングパックⅡ"),
            ("/ingredients/glutathione.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオン<br>成分詳細ページ"),
            ("/ingredients/nano-collagen.html", "https://www.luminove.online/images/product-skin.webp", "ナノコラーゲン<br>成分詳細ページ"),
        ],
        reel=dict(
            reel_title="ピールオフパック、正しい使い方教えます",
            hook="塗って剥がすだけ…じゃもったいない！",
            script="ピールオフパックは塗布→乾かす→剥がすの3ステップ。表示時間を守って、端からゆっくり剥がすのがコツ。週1〜2回の使用がおすすめだよ。",
            caption="ピールオフパックは正しい使い方でより気持ちよく。週1〜2回のスペシャルケアに✨ #ピールオフパック #韓国コスメ",
            hashtags=["#ピールオフパック", "#韓国コスメ", "#スペシャルケア", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="korean-hair-ampoule",
        title="韓国ヘアアンプルとは？使い方と選び方｜LUMINOVE",
        meta_desc="韓国ヘアアンプルとは何か、使い方と選び方を解説。サロン帰りのような仕上がりを目指すホームケアアイテムの魅力を紹介します。",
        tag="ヘアケア / 韓国ヘアアンプル",
        h1="韓国ヘアアンプルとは？<br>使い方と選び方",
        h1_plain="韓国ヘアアンプルとは？使い方と選び方",
        image="https://www.luminove.online/images/product-hairampoule-repair.webp",
        lead="韓国で人気の「ヘアアンプル」は、サロン帰りのような質感を自宅で目指せるホームケアアイテムです。使い方と選び方を解説します。",
        sections=[
            ("ヘアアンプルとは", "      <p>ヘアアンプルは、高濃度の美容成分を配合した集中ケア用のヘアケアアイテムです。タンパク質や保湿成分を高濃度配合し、ダメージ補修にアプローチします。</p>"),
            ("使い方", "      <p>タオルドライ後、ドライヤー前に少量を毛先中心に馴染ませるのが基本の使い方です。洗い流し不要のアイテムが多く、毎日のケアに取り入れやすい設計です。</p>"),
            ("選び方のポイント", "      <p>配合成分の濃度や、自分の髪質（乾燥・ダメージ・くせ毛など）に合った処方を選びましょう。</p><div class=\"cta-box\"><p>高濃度タンパク質×5種マリン由来成分配合</p><a href=\"/#products\" class=\"btn-primary\">アフターサロンケア リペアを見る →</a></div>"),
        ],
        faq=[
            ("毎日使用できますか？", "多くのヘアアンプルは洗い流し不要で、毎日のドライヤー前ケアに使用できる設計です。"),
            ("どんな髪質の人に向いていますか？", "ダメージヘア・乾燥が気になる髪質の方に特に向いています。"),
            ("頭皮にもつけて良いですか？", "製品によって設計が異なります。基本的には毛先〜中間を中心に使用することをおすすめします。"),
        ],
        related=[
            ("/#products", "https://www.luminove.online/images/product-hairampoule-repair.webp", "アフターサロンケア<br>リペア ヘアアンプル"),
            ("/#products", "https://www.luminove.online/images/product-oilserum-whitelily.webp", "ホワイトリリー<br>シルキーオイルセラム"),
            ("/blog/korean-skincare-recommended.html", "https://www.luminove.online/images/hero-all.webp", "韓国スキンケア<br>おすすめ2026"),
        ],
        reel=dict(
            reel_title="韓国ヘアアンプル、使ったことある？",
            hook="サロン帰りの質感、家で作れるって知ってた？",
            script="韓国ヘアアンプルはタオルドライ後、ドライヤー前に毛先に馴染ませるだけ。高濃度のタンパク質や保湿成分でダメージ補修にアプローチ。洗い流し不要だから続けやすいよ。",
            caption="韓国ヘアアンプルで毎日のドライヤー前ケアを格上げ。サロン帰りのような質感を目指して✨ #韓国ヘアアンプル #ヘアケア",
            hashtags=["#韓国ヘアアンプル", "#ヘアケア", "#韓国コスメ", "#LUMINOVE"]
        ),
    ),
    dict(
        slug="hand-balm-gift",
        title="香りで選ぶ韓国ハンドバーム｜LUMINOVE",
        meta_desc="韓国ハンドバームを香りで選ぶポイントを解説。プレゼントにも人気のハンドケアアイテムの選び方を紹介します。",
        tag="ギフトガイド / ハンドバーム",
        h1="香りで選ぶ韓国ハンドバーム",
        h1_plain="香りで選ぶ韓国ハンドバーム",
        image="https://www.luminove.online/images/product-handbalm-mev.webp",
        lead="ハンドバームはちょっとしたプレゼントにも人気のアイテムです。香りで選ぶときのポイントと、おすすめのシーンを紹介します。",
        sections=[
            ("香りで選ぶ楽しさ", "      <p>ハンドバームは保湿効果だけでなく、香りも楽しめるアイテムです。マリン系・ウッディ系・フローラル系など、好みやシーンに合わせて選べます。</p>"),
            ("シーン別のおすすめ", "      <p>お出かけ用にはリフレッシュ感のあるマリン系、就寝前にはリラックスできるウッディ系など、シーンに合わせた使い分けもおすすめです。</p>"),
            ("ギフトとしての魅力", "      <p>シアバターベースの上質な仕上がりと香りの楽しさから、ちょっとしたギフトにも適しています。</p><div class=\"cta-box\"><p>体温でとろけるシアバターベースのハンドバーム</p><a href=\"/#products\" class=\"btn-primary\">ヴィーガン ハンドバームを見る →</a></div>"),
        ],
        faq=[
            ("どんな人へのプレゼントに向いていますか？", "香りを楽しみたい方、ハンドケアを習慣にしたい方へのちょっとしたプレゼントに向いています。"),
            ("ベタつきは気になりますか？", "体温でとろけるテクスチャーの製品が多く、馴染みやすい使用感です。"),
            ("複数の香りを使い分けても良いですか？", "はい、シーンや気分に合わせて使い分ける方が多くいらっしゃいます。"),
        ],
        related=[
            ("/#products", "https://www.luminove.online/images/product-handbalm-mev.webp", "ヴィーガン<br>ハンドバーム"),
            ("/blog/korean-skincare-recommended.html", "https://www.luminove.online/images/hero-all.webp", "韓国スキンケア<br>おすすめ2026"),
            ("/#products", "https://www.luminove.online/images/product-oilserum-whitelily.webp", "ホワイトリリー<br>シルキーオイルセラム"),
        ],
        reel=dict(
            reel_title="香りで選ぶハンドバーム、どれが好き？",
            hook="ハンドケアって、香りも選べるって知ってた？",
            script="ハンドバームはマリン系、ウッディ系、フローラル系と香りで選べるのが楽しい。シアバターベースで体温でとろけるテクスチャーだから、ベタつかず使いやすいよ。",
            caption="香りで選ぶハンドバーム。シーンや気分に合わせて使い分けるのも楽しい🤍 #ハンドバーム #韓国コスメ",
            hashtags=["#ハンドバーム", "#ハンドケア", "#韓国コスメ", "#LUMINOVE"]
        ),
    ),
]


os.makedirs('blog', exist_ok=True)
print('=== ブログ記事10本生成 ===')
for a in ARTICLES:
    html = render_article(a)
    path = f"blog/{a['slug']}.html"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Created: {path}')

print('\n=== 完了 ===')
