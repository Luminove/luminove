# -*- coding: utf-8 -*-
"""
既存ブログ記事9本の内容強化(1500文字以上)
結論/初心者向け説明/選び方/使い方/向いている人/注意点/関連成分/関連商品/FAQ5個以上/reel JSONを追加
薬機法NGワードは使用しない
"""
import json, os, re

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
    .conclusion-box { background: var(--green-mist); border-radius: var(--radius); padding: 1.5rem 1.8rem; margin: 0 auto 2.5rem; max-width: 720px; }
    .conclusion-box p { font-size: .92rem; color: var(--text-dark); margin: 0; line-height: 1.9; }
    .conclusion-box .label { display: block; font-size: .72rem; letter-spacing: .15em; color: var(--green-mid); font-weight: 600; margin-bottom: .5rem; }
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
    .note-box { background: #fff; border: 1px solid var(--green-pale); border-radius: var(--radius); padding: 1.2rem 1.5rem; margin: 1rem 0; }
    .note-box p { font-size: .85rem; color: var(--text-mid); margin: 0; line-height: 1.8; }
    .ingredient-links { display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1rem; }
    .ingredient-links a { display: inline-block; font-size: .82rem; font-weight: 500; color: var(--green-deep); background: var(--green-mist); border: 1px solid var(--green-pale); border-radius: 50px; padding: .45rem 1.1rem; text-decoration: none; }
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
    .footer-grid { display: grid; grid-template-columns: 1.3fr 1fr 1fr 1fr 1.6fr; gap: 2.4rem; margin-bottom: 3rem; }
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
        "datePublished": a.get('date_published', '2026-06-22'),
        "dateModified": "2026-06-22"
    }, ensure_ascii=False)

    reel_jsonld = json.dumps({"reel": a['reel']}, ensure_ascii=False, indent=2)

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

    ingredient_links_html = ''
    for url, name in a['ingredient_links']:
        ingredient_links_html += f'        <a href="{url}">{name} →</a>\n'

    sections_html = ''
    for i, (h2, body) in enumerate(a['sections']):
        anchor = f"sec{i+1}"
        sections_html += f'''
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

  <div class="conclusion-box">
    <span class="label">結論</span>
    <p>{a['conclusion']}</p>
  </div>

  <div class="article-body">
{sections_html}
    <section class="article-section">
      <h2>関連成分</h2>
      <p>{a['ingredient_intro']}</p>
      <div class="ingredient-links">
{ingredient_links_html}      </div>
    </section>
  </div>

  <section class="faq-section" id="faq">
    <h2>よくある質問</h2>
{faq_html}  </section>

  <section class="related-section">
    <h2>関連記事・関連商品</h2>
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

# ============================================================
# 1. glutathione-skincare.html
# ============================================================
dict(
    slug="glutathione-skincare",
    title="グルタチオン化粧品とは？韓国スキンケアで人気の理由｜LUMINOVE",
    meta_desc="グルタチオン化粧品とは何か、韓国スキンケアでなぜ人気なのかを解説。選び方・使い方・向いている人までわかりやすく紹介します。",
    tag="成分コラム / グルタチオン",
    h1="グルタチオン化粧品とは？<br>韓国スキンケアで人気の理由",
    h1_plain="グルタチオン化粧品とは？韓国スキンケアで人気の理由",
    image="https://www.luminove.online/images/product-serum.webp",
    lead="美容点滴（白玉注射）の主成分として知られるグルタチオン。韓国コスメ業界ではこの成分を化粧品に高濃度配合する技術が進み、人気の美容成分として定着しました。初心者の方にもわかりやすく、選び方から使い方まで解説します。",
    conclusion="グルタチオン化粧品は配合濃度（ppm）と組み合わせ成分を確認して選ぶのがポイント。継続使用が前提の成分なので、毎日のルーティンに組み込みやすいテクスチャーを選びましょう。",
    sections=[
        ("グルタチオン化粧品とは（初心者向け解説）", "      <p>グルタチオンは、グルタミン酸・システイン・グリシンの3つのアミノ酸からなるトリペプチドで、強力な抗酸化作用を持つ成分です。美容クリニックの点滴施術として知られていましたが、近年は化粧品への配合技術が進み、化粧水・美容液・洗顔料など幅広いアイテムに採用されています。</p><p>初めて聞く方は「美白成分」というイメージを持つかもしれませんが、正確には抗酸化ケアとメラニン生成に着目したアプローチを持つ成分で、透明感のある肌印象をサポートする目的で配合されています。</p>"),
        ("選び方", "      <p>選ぶときは以下の3点を確認しましょう。</p><ul><li><strong>配合濃度（ppm表記）：</strong>10,000ppm以上であれば高濃度の部類です</li><li><strong>組み合わせ成分：</strong>コラーゲンやビタミンC誘導体と組み合わせた製品は相乗効果が期待できます</li><li><strong>剤形：</strong>美容液が最も高濃度になりやすく、化粧水は毎日使いに適しています</li></ul>"),
        ("使い方", "      <p>洗顔後、化粧水→美容液→乳液の順で使用するのが基本です。グルタチオンは継続使用が前提の成分なので、肌のターンオーバー1サイクルにあたる28日間を目安に使い続けることをおすすめします。</p>"),
        ("こんな人におすすめ", "      <ul><li>透明感やくすみが気になる方</li><li>美容点滴に関心はあるが、まずは日常ケアから始めたい方</li><li>毎日続けやすい高濃度成分を探している方</li></ul>"),
        ("使用時の注意点", "      <p>体内にも存在する成分のため低刺激とされていますが、高濃度配合製品や他の配合成分によっては肌に合わないこともあります。初めて使用する際はパッチテストを行い、肌に異常を感じた場合はすぐに使用を中止してください。</p>"),
    ],
    ingredient_intro="グルタチオンと組み合わせて使われることが多いナノコラーゲン（300Da）についても、あわせてチェックしてみてください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("グルタチオン化粧品は誰でも使えますか？", "体内にも存在する成分のため低刺激とされていますが、配合される他成分により異なります。初回はパッチテストをおすすめします。"),
        ("どのくらいの期間で実感できますか？", "肌のターンオーバー周期である28日間を目安に、継続使用することをおすすめします。"),
        ("美容点滴と併用しても良いですか？", "はい、点滴施術を補完するホームケアとして併用される方が多くいらっしゃいます。"),
        ("配合濃度はどこを見ればわかりますか？", "パッケージや商品ページの成分表記にppm表示があります。LUMINOVEの商品ページでは配合量を明記しています。"),
        ("ナノコラーゲンと一緒に使うメリットは何ですか？", "グルタチオンが抗酸化ケア、ナノコラーゲンがうるおい・ハリ印象にアプローチするため、組み合わせることで透明感とハリ感の両方をケアしやすくなります。"),
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

# ============================================================
# 2. nano-collagen.html (blog)
# ============================================================
dict(
    slug="nano-collagen",
    title="ナノコラーゲンとは？低分子コラーゲンが注目される理由｜LUMINOVE",
    meta_desc="ナノコラーゲンとは何か、低分子化されたコラーゲンが韓国スキンケアで注目される理由を解説。選び方や使い方もわかりやすく紹介します。",
    tag="成分コラム / ナノコラーゲン",
    h1="ナノコラーゲンとは？<br>低分子コラーゲンが注目される理由",
    h1_plain="ナノコラーゲンとは？低分子コラーゲンが注目される理由",
    image="https://www.luminove.online/images/product-skin.webp",
    lead="「ナノコラーゲン」という言葉を韓国コスメでよく見かけるようになりました。通常のコラーゲンとどう違うのか、なぜ注目されているのかを初心者の方にもわかりやすく解説します。",
    conclusion="ナノコラーゲン（300Da）は分子量を小さくした低分子コラーゲンで、角質層までうるおいを届けやすい設計が特徴。配合濃度と組み合わせ成分を確認して選びましょう。",
    sections=[
        ("ナノコラーゲンとは（初心者向け解説）", "      <p>ナノコラーゲンとは、分子量を300Da（ダルトン）程度まで小さくした低分子コラーゲンのことです。通常のコラーゲンは分子サイズが大きく、肌表面に保湿膜を作る働きが中心ですが、ナノコラーゲンは低分子化により角質層までうるおいを届けやすい設計になっています。</p>"),
        ("選び方", "      <p>ナノコラーゲン配合の製品を選ぶときは、分子量の表記（300Daなど）と、一緒に配合されている成分を確認しましょう。グルタチオンなど抗酸化ケア成分と組み合わせた製品は、うるおいと透明感の両方にアプローチしやすくなります。</p>"),
        ("使い方", "      <p>化粧水・美容液・クリームなど幅広いアイテムに配合されているため、普段使っているスキンケアステップにそのまま取り入れられます。洗顔料に配合されたタイプは、洗い上がりのつっぱり感が気になる方に特におすすめです。</p>"),
        ("こんな人におすすめ", "      <ul><li>うるおい不足やハリ不足が気になる方</li><li>洗顔後のつっぱり感が気になる方</li><li>軽いテクスチャーのスキンケアを好む方</li></ul>"),
        ("使用時の注意点", "      <p>コラーゲン自体は比較的低刺激とされる成分ですが、製品によって配合される他の成分が異なります。敏感肌の方は初回使用前にパッチテストを実施することをおすすめします。</p>"),
    ],
    ingredient_intro="抗酸化ケアで知られるグルタチオンとの組み合わせもチェックしてみてください。",
    ingredient_links=[("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？"), ("/ingredients/glutathione.html", "グルタチオンとは？")],
    faq=[
        ("ナノコラーゲンは安全ですか？", "コラーゲン自体は比較的低刺激な成分です。敏感肌の方は初回使用前にパッチテストをおすすめします。"),
        ("どんな製品に配合されていますか？", "化粧水・美容液・クリーム・洗顔料など幅広いアイテムに配合されています。"),
        ("グルタチオンと併用できますか？", "はい、グルコラシリーズのように両成分を組み合わせた製品が人気です。"),
        ("一般的なコラーゲンと比べて何が違いますか？", "分子量が小さく低分子化されているため、肌表面に留まりやすい一般的なコラーゲンに比べ、角質層までうるおいを届けやすい設計です。"),
        ("毎日使っても問題ありませんか？", "多くの製品が毎日の朝晩のケアに使用できる設計です。製品の使用方法に従ってご使用ください。"),
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

# ============================================================
# 3. pdrn-skincare.html
# ============================================================
dict(
    slug="pdrn-skincare",
    title="PDRN化粧品とは？韓国コスメで注目される理由｜LUMINOVE",
    meta_desc="PDRN化粧品とは何か、韓国コスメでなぜ注目されるのかを解説。選び方・使い方・向いている人までわかりやすく紹介します。",
    tag="成分コラム / PDRN",
    h1="PDRN化粧品とは？<br>韓国コスメで注目される理由",
    h1_plain="PDRN化粧品とは？韓国コスメで注目される理由",
    image="https://www.luminove.online/images/product-rejun-cream.webp",
    lead="美容医療分野で研究されるPDRN。韓国コスメでは「水光注射成分」として知られるこの成分をスキンケアに応用する技術が進んでいます。初心者の方にもわかりやすく解説します。",
    conclusion="PDRN化粧品はサーモン由来DNA成分を配合したスキンケアで、肌コンディションを整えるケアや施術後の保湿ケアに取り入れられています。低刺激処方かどうかを確認して選びましょう。",
    sections=[
        ("PDRN化粧品とは（初心者向け解説）", "      <p>PDRN（ポリデオキシリボヌクレオチド）は、サーモン由来のDNA断片です。美容医療の水光注射として知られていましたが、韓国コスメではこの成分を化粧品に配合する技術が進んでいます。初めて聞く方には「再生医療の成分」という強いイメージがあるかもしれませんが、スキンケアでは肌コンディションを整える成分として穏やかに取り入れられています。</p>"),
        ("選び方", "      <p>PDRNの配合濃度（ppm表記）と、低刺激・無香料かどうかを確認しましょう。施術後のデリケートな肌を想定して設計された製品も多く、敏感肌の方にも選びやすい処方が増えています。</p>"),
        ("使い方", "      <p>化粧水や美容液で肌を整えた後、保湿クリームとして使用するのが基本です。「28日ルーティンケア」という言葉とともに、継続使用を前提に設計された製品が多くあります。</p>"),
        ("こんな人におすすめ", "      <ul><li>美容施術後のデリケートな肌のケアをしたい方</li><li>肌のコンディションが気になる方</li><li>低刺激処方のクリームを探している方</li></ul>"),
        ("使用時の注意点", "      <p>サーモン由来の成分のため、サーモンアレルギーがある方はご注意ください。敏感肌の方は初回使用前にパッチテストを実施し、施術直後に使用する場合は施術を行ったクリニックに確認することをおすすめします。</p>"),
    ],
    ingredient_intro="PDRNと組み合わせて配合されることが多いNMNについても確認してみてください。",
    ingredient_links=[("/ingredients/pdrn.html", "PDRNとは？"), ("/ingredients/nmn.html", "NMNとは？")],
    faq=[
        ("PDRN化粧品は誰でも使えますか？", "サーモン由来の成分で、医療分野でも研究が進む成分です。サーモンアレルギーがある方はご注意のうえ、敏感肌の方はパッチテストをおすすめします。"),
        ("どんな肌悩みに向いていますか？", "施術後のデリケートな肌の保湿ケア、肌コンディションの調整を目的とした製品が多くあります。"),
        ("毎日使用できますか？", "製品によって設計は異なりますが、毎日のケアに使用できる設計のものが多くあります。"),
        ("水光注射と同じ成分ですか？", "同じPDRNという成分ですが、注射は直接注入する施術であり、化粧品は経皮吸収による働きが主となるため作用経路が異なります。"),
        ("敏感肌でも使える製品はありますか？", "低刺激・無香料処方を採用した製品もあります。商品ページで処方の特徴を確認してから選ぶと安心です。"),
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

# ============================================================
# 4. glutathione-serum.html
# ============================================================
dict(
    slug="glutathione-serum",
    title="グルタチオン美容液の選び方｜LUMINOVE",
    meta_desc="グルタチオン美容液の選び方を解説。配合濃度（ppm）の見方や、使い方・向いている人・注意点までわかりやすく紹介します。",
    tag="選び方ガイド / グルタチオン美容液",
    h1="グルタチオン美容液の選び方",
    h1_plain="グルタチオン美容液の選び方",
    image="https://www.luminove.online/images/product-serum.webp",
    lead="グルタチオン美容液は配合濃度や組み合わせ成分によって特徴が大きく異なります。初めて選ぶ方にもわかりやすく、失敗しない選び方のポイントを解説します。",
    conclusion="グルタチオン美容液は配合濃度（ppm）・組み合わせ成分・テクスチャーの3点で選ぶのがポイント。透明感ケアを本格的に目指すなら10,000ppm以上を目安にしましょう。",
    sections=[
        ("グルタチオン美容液とは（初心者向け解説）", "      <p>グルタチオン美容液は、美容点滴の主成分として知られるグルタチオンを高濃度で配合した美容液です。化粧水よりも美容成分の配合量が多く、スキンケアの中でも「集中ケア」のステップとして使われます。</p>"),
        ("選び方", "      <p>配合濃度（ppm）を確認する：グルタチオンの配合量はppm表記が一般的です。10,000ppm以上であれば高濃度の部類に入ります。LUMINOVEのグルコラ セラムは30,000ppm（3%）配合です。</p><p>組み合わせ成分を確認する：グルタチオン単体よりも、コラーゲンやビタミンC誘導体などと組み合わせた製品の方が相乗効果が期待できます。</p>"),
        ("使い方", "      <p>化粧水のあと、乳液の前のステップで使用するのが基本です。毎日継続することで透明感・くすみのケア実感につながりやすくなります。</p>"),
        ("こんな人におすすめ", "      <ul><li>透明感やくすみが気になる方</li><li>化粧水だけでは満足できず、集中ケアを取り入れたい方</li><li>高濃度成分を毎日のスキンケアに取り入れたい方</li></ul>"),
        ("使用時の注意点", "      <p>高濃度配合のため、初めて使用する際はパッチテストを実施することをおすすめします。開封後は品質保持の観点から、3〜6ヶ月程度を目安に使い切ることをおすすめします。</p>"),
    ],
    ingredient_intro="グルタチオン美容液には、ナノコラーゲン（300Da）が組み合わせ配合されていることも多いので、あわせて確認してみてください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("ppmが高いほど良いのですか？", "高濃度であるほど成分量は多くなりますが、肌質や他の配合成分との相性も重要です。"),
        ("どのくらいの期間で使い切るのが理想ですか？", "開封後は品質保持の観点から、3〜6ヶ月程度を目安に使い切ることをおすすめします。"),
        ("乾燥肌でも使えますか？", "保湿成分と組み合わされた製品であれば、乾燥肌の方にも使いやすい設計です。"),
        ("化粧水と美容液はどちらを先に使いますか？", "化粧水で肌を整えてから美容液を重ねるのが基本の順番です。化粧水で肌が柔らかくなった状態だと、成分が浸透しやすくなります。"),
        ("毎日使っても問題ありませんか？", "はい、多くの製品は毎日の使用を前提に設計されています。継続使用することでケア実感につながりやすくなります。"),
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

# ============================================================
# 5. pdrn-nmn-cream.html
# ============================================================
dict(
    slug="pdrn-nmn-cream",
    title="PDRN×NMNクリームとは？相乗効果を解説｜LUMINOVE",
    meta_desc="PDRN×NMNクリームとは何か、2つの成分を組み合わせる意味を解説。選び方・使い方・向いている人までわかりやすく紹介します。",
    tag="成分コラム / PDRN×NMN",
    h1="PDRN×NMNクリームとは？<br>相乗効果を解説",
    h1_plain="PDRN×NMNクリームとは？相乗効果を解説",
    image="https://www.luminove.online/images/product-rejun-cream.webp",
    lead="韓国コスメで見かける「PDRN×NMN」配合クリーム。それぞれ異なるアプローチを持つ2成分を組み合わせる理由を、初心者の方にもわかりやすく解説します。",
    conclusion="PDRNは肌コンディションへのアプローチ、NMNは年齢に応じたハリ感ケアへのアプローチと役割が異なるため、組み合わせることで相補的なケアが期待できます。",
    sections=[
        ("PDRNとNMN、それぞれの特徴（初心者向け解説）", "      <p>PDRNはサーモン由来のDNA断片で、肌コンディションに着目したアプローチを持つ成分です。NMNは細胞エネルギー（NAD+）の前駆体として、年齢に応じたケアの分野で研究される成分です。</p>"),
        ("選び方", "      <p>PDRN・NMNそれぞれの配合濃度（ppm表記）を確認しましょう。LUMINOVEのリジュエヌ クリームはPDRN3000ppm×NMN1000ppmのデュアルフォーミュラを採用しています。低刺激・無香料処方かどうかも選ぶ際のポイントです。</p>"),
        ("使い方", "      <p>化粧水で肌を整えた後、保湿クリームとして使用します。施術後のデリケートな肌の保湿ケアとして使う場合は、施術を行ったクリニックの指示に従ってください。</p>"),
        ("こんな人におすすめ", "      <ul><li>美容施術後のデリケートな肌の保湿ケアをしたい方</li><li>ニキビ跡やくすみが気になる方</li><li>肌コンディションを整えるケアを探している方</li></ul>"),
        ("使用時の注意点", "      <p>サーモン由来の成分が含まれるため、サーモンアレルギーがある方はご注意ください。初めて使用する際はパッチテストをおすすめします。</p>"),
    ],
    ingredient_intro="PDRN・NMNそれぞれの成分解説ページもあわせてご覧ください。",
    ingredient_links=[("/ingredients/pdrn.html", "PDRNとは？"), ("/ingredients/nmn.html", "NMNとは？")],
    faq=[
        ("PDRNとNMNは併用しても安全ですか？", "それぞれ異なる作用を持つ成分で、併用されることを前提に設計された製品が多くあります。"),
        ("どんな肌悩みに向いていますか？", "施術後のデリケートな肌の保湿ケアや、肌コンディションが気になる方に向いています。"),
        ("毎日使用できますか？", "製品設計によりますが、リジュエヌ クリームは毎日のケアに使用できる低刺激処方です。"),
        ("NMNだけ、PDRNだけの製品とどちらが良いですか？", "目的によって選び方は異なります。両方のアプローチを同時に取り入れたい場合は、デュアルフォーミュラの製品がおすすめです。"),
        ("他のスキンケアと併用できますか？", "化粧水や日焼け止めとの組み合わせは問題ありません。同じシリーズの製品と組み合わせることで、ルーティンとして取り入れやすくなります。"),
    ],
    related=[
        ("/ingredients/pdrn.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRN<br>成分詳細ページ"),
        ("/ingredients/nmn.html", "https://www.luminove.online/images/product-rejun-cream.webp", "NMN<br>成分詳細ページ"),
        ("/products/rejun-pdrn-cream.html", "https://www.luminove.online/images/product-rejun-cream.webp", "リジュエヌ クリーム<br>（PDRN×NMN）"),
    ],
    reel=dict(
        reel_title="PDRNとNMN、一緒に使うとどうなる？",
        hook="2つの成分を組み合わせる理由、知ってる？",
        script="PDRNは肌コンディション系、NMNはエネルギー系のアプローチ。役割が違うから組み合わせると相補的なケアが期待できるの。韓国コスメではこの2つを配合したクリームが人気。",
        caption="PDRN×NMNの組み合わせで、異なるアプローチを同時にケア。リジュエヌ クリームで採用されています🧬 #PDRN #NMN #韓国コスメ",
        hashtags=["#PDRN", "#NMN", "#韓国コスメ", "#美容成分", "#LUMINOVE"]
    ),
),

# ============================================================
# 6. korean-sunscreen.html
# ============================================================
dict(
    slug="korean-sunscreen",
    title="韓国日焼け止めの選び方｜LUMINOVE",
    meta_desc="韓国日焼け止めの選び方を解説。SPF・PA値の見方や、機能性化粧品認証の意味、使い方・向いている人までわかりやすく紹介します。",
    tag="選び方ガイド / 韓国日焼け止め",
    h1="韓国日焼け止めの選び方",
    h1_plain="韓国日焼け止めの選び方",
    image="https://www.luminove.online/images/product-suncream.webp",
    lead="韓国日焼け止めは機能性・使用感ともに進化が著しいカテゴリーです。初めて選ぶ方にもわかりやすく、選び方のポイントを解説します。",
    conclusion="韓国日焼け止めはSPF・PA値、機能性化粧品認証の有無、テクスチャーの3点で選ぶのがポイント。日常使いと屋外活動で使い分けましょう。",
    sections=[
        ("韓国日焼け止めとは（初心者向け解説）", "      <p>韓国日焼け止めは、UVカット機能に加えてテクスチャーや機能性にこだわった製品が多いのが特徴です。白浮きしにくい処方や、スキンケア成分を配合した製品など、選択肢が豊富にあります。</p>"),
        ("選び方", "      <p>SPF・PA値の見方：SPFは紫外線B波（UVB）への防御力、PAは紫外線A波（UVA）への防御力を示す指標です。日常使いならSPF30〜50、屋外活動が多い日はSPF50+ PA++++が目安です。</p><p>機能性化粧品認証について：韓国では機能性化粧品認証制度があります。認証を取得した日焼け止めは、UVカットに加えてスキンケア成分も意識した処方であることが特徴です。</p>"),
        ("使い方", "      <p>スキンケアの最後のステップで、適量を顔・首・デコルテなどに塗布します。屋外での活動時間が長い場合は、2〜3時間ごとの塗り直しをおすすめします。</p>"),
        ("こんな人におすすめ", "      <ul><li>白浮きしにくい日焼け止めを探している方</li><li>日焼け止めと一緒にスキンケアも意識したい方</li><li>メイク前のベースとしても使いたい方</li></ul>"),
        ("使用時の注意点", "      <p>製品によって配合成分が異なるため、初回使用前にパッチテストをおすすめします。肌に異常を感じた場合はすぐに使用を中止してください。</p>"),
    ],
    ingredient_intro="グルタチオン・ナノコラーゲン（300Da）配合の日焼け止めも人気です。成分の詳細もあわせてご確認ください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("日焼け止めだけでスキンケアになりますか？", "機能性化粧品認証を取得した製品であれば、UVケアと一緒にスキンケアも意識した処方になっています。"),
        ("毎日塗り直しは必要ですか？", "屋外での活動時間が長い場合は、2〜3時間ごとの塗り直しをおすすめします。"),
        ("敏感肌でも使えますか？", "製品によって配合成分が異なるため、初回使用前にパッチテストをおすすめします。"),
        ("メイクの下地として使えますか？", "仕上がりがなめらかな処方の製品であれば、メイクの下地としても使用できます。"),
        ("室内でも日焼け止めは必要ですか？", "紫外線は室内でも窓から入ることがあるため、室内でも日常的に使用することをおすすめします。"),
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

# ============================================================
# 7. peeling-pack-how-to-use.html
# ============================================================
dict(
    slug="peeling-pack-how-to-use",
    title="ピールオフパックの使い方｜LUMINOVE",
    meta_desc="ピールオフパックの正しい使い方を解説。塗布から剥がすタイミング、使用頻度、向いている人や注意点までわかりやすく紹介します。",
    tag="使い方ガイド / ピールオフパック",
    h1="ピールオフパックの使い方",
    h1_plain="ピールオフパックの使い方",
    image="https://www.luminove.online/images/product-pack2.webp",
    lead="塗って剥がすピールオフパックは、正しい使い方を知ることでより心地よく使えます。初めて使う方にもわかりやすく、基本ステップから注意点まで解説します。",
    conclusion="ピールオフパックは週1〜2回程度のスペシャルケアとして取り入れるのがおすすめ。表示時間を守り、端から優しく剥がすのがポイントです。",
    sections=[
        ("ピールオフパックとは（初心者向け解説）", "      <p>ピールオフパックは、肌に塗布して乾かした後、フィルム状になったパックを剥がすタイプのスキンケアアイテムです。剥がす際に古い角質が一緒に取れることから、つるつる・もちもちの肌印象を目指すスペシャルケアとして人気です。</p>"),
        ("選び方", "      <p>配合成分とその濃度を確認しましょう。グルタチオンやコラーゲンなどの美容成分が高濃度に配合された製品は、剥がした直後の肌印象の変化を感じやすいとされています。</p>"),
        ("使い方", "      <ol><li>洗顔後、化粧水で肌を整える</li><li>目元・口元を避けて顔全体に薄くムラなく塗布</li><li>表示時間（目安15〜20分）乾かす</li><li>端からゆっくり剥がす</li><li>残った微量を優しくなじませる</li></ol>"),
        ("こんな人におすすめ", "      <ul><li>毛穴や肌のざらつきが気になる方</li><li>特別な日の前にスペシャルケアをしたい方</li><li>剥がすケアの爽快感が好きな方</li></ul>"),
        ("使用時の注意点", "      <p>肌に直接密着するアイテムのため、敏感肌の方は初回使用前にパッチテストをおすすめします。週1〜2回程度の使用が一般的で、毎日の使用は推奨されません。乾燥しすぎる前、表示時間内に剥がすようにしましょう。</p>"),
    ],
    ingredient_intro="グルタチオン・ナノコラーゲン（300Da）配合のピールオフパックについて、成分の詳細もご確認ください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("毎日使っても良いですか？", "ピールオフパックは週1〜2回程度の使用が一般的です。毎日の使用は推奨されません。"),
        ("剥がしにくい場合はどうすれば良いですか？", "完全に乾燥しすぎると剥がしにくくなることがあります。表示時間を目安に、端から優しく剥がしてください。"),
        ("敏感肌でも使えますか？", "肌に直接密着するアイテムのため、敏感肌の方は初回使用前にパッチテストをおすすめします。"),
        ("剥がした後のスキンケアはどうすれば良いですか？", "残った微量を優しくなじませた後、いつものスキンケアステップに進んで問題ありません。"),
        ("どんな効果を感じやすいですか？", "古い角質が一緒に取れることで、つるつる・もちもちとした肌印象を感じやすいとされています。個人差がありますので、まずは少量から試すことをおすすめします。"),
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

# ============================================================
# 8. korean-hair-ampoule.html
# ============================================================
dict(
    slug="korean-hair-ampoule",
    title="韓国ヘアアンプルとは？使い方と選び方｜LUMINOVE",
    meta_desc="韓国ヘアアンプルとは何か、使い方と選び方を解説。向いている人や注意点まで初心者にもわかりやすく紹介します。",
    tag="ヘアケア / 韓国ヘアアンプル",
    h1="韓国ヘアアンプルとは？<br>使い方と選び方",
    h1_plain="韓国ヘアアンプルとは？使い方と選び方",
    image="https://www.luminove.online/images/product-hairampoule-repair.webp",
    lead="韓国で人気の「ヘアアンプル」は、サロン帰りのような質感を自宅で目指せるホームケアアイテムです。初めて使う方にもわかりやすく、使い方と選び方を解説します。",
    conclusion="ヘアアンプルはタオルドライ後、ドライヤー前に使うのが基本。自分の髪質に合った配合成分の製品を選びましょう。",
    sections=[
        ("ヘアアンプルとは（初心者向け解説）", "      <p>ヘアアンプルは、高濃度の美容成分を配合した集中ケア用のヘアケアアイテムです。タンパク質や保湿成分を高濃度配合し、ダメージが気になる髪のなめらかさをサポートします。「アンプル」という名前から美容液のような印象を持つ方も多いですが、洗い流し不要で使いやすいのが特徴です。</p>"),
        ("選び方", "      <p>配合成分の種類と濃度を確認しましょう。加水分解シルク・ケラチン・コラーゲンなどのタンパク質や、海藻由来成分を配合した製品は、髪のコンディションを整える働きが期待されています。自分の髪質（乾燥・ダメージ・くせ毛など）に合った処方を選ぶことも大切です。</p>"),
        ("使い方", "      <p>タオルドライ後、ドライヤー前に少量を毛先中心に馴染ませるのが基本の使い方です。洗い流し不要のアイテムが多く、毎日のケアに取り入れやすい設計です。</p>"),
        ("こんな人におすすめ", "      <ul><li>ダメージヘア・乾燥が気になる髪質の方</li><li>サロン帰りのような質感を目指したい方</li><li>ドライヤー前のひと手間を取り入れたい方</li></ul>"),
        ("使用時の注意点", "      <p>製品によって配合成分が異なるため、頭皮につける場合は商品の使用方法を確認してください。基本的には毛先〜中間を中心に使用することをおすすめします。</p>"),
    ],
    ingredient_intro="ヘアケアと合わせて、スキンケアの注目成分もチェックしてみてください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("毎日使用できますか？", "多くのヘアアンプルは洗い流し不要で、毎日のドライヤー前ケアに使用できる設計です。"),
        ("どんな髪質の人に向いていますか？", "ダメージヘア・乾燥が気になる髪質の方に特に向いています。"),
        ("頭皮にもつけて良いですか？", "製品によって設計が異なります。基本的には毛先〜中間を中心に使用することをおすすめします。"),
        ("どのくらいの量を使えば良いですか？", "製品の使用方法に記載された目安量を確認してください。少量から試して、髪の長さや状態に応じて調整するのがおすすめです。"),
        ("カラーやパーマ施術後にも使えますか？", "サロン施術後のホームケアとして使われることが多く、施術後の髪のコンディションを整えるケアに取り入れやすい設計です。"),
    ],
    related=[
        ("/#products", "https://www.luminove.online/images/product-hairampoule-repair.webp", "アフターサロンケア<br>リペア ヘアアンプル"),
        ("/#products", "https://www.luminove.online/images/product-oilserum-whitelily.webp", "ホワイトリリー<br>シルキーオイルセラム"),
        ("/blog/korean-skincare-recommended.html", "https://www.luminove.online/images/hero-all.webp", "韓国スキンケア<br>おすすめ2026"),
    ],
    reel=dict(
        reel_title="韓国ヘアアンプル、使ったことある？",
        hook="サロン帰りの質感、家で作れるって知ってた？",
        script="韓国ヘアアンプルはタオルドライ後、ドライヤー前に毛先に馴染ませるだけ。高濃度のタンパク質や保湿成分でダメージが気になる髪のなめらかさをサポート。洗い流し不要だから続けやすいよ。",
        caption="韓国ヘアアンプルで毎日のドライヤー前ケアを格上げ。サロン帰りのような質感を目指して✨ #韓国ヘアアンプル #ヘアケア",
        hashtags=["#韓国ヘアアンプル", "#ヘアケア", "#韓国コスメ", "#LUMINOVE"]
    ),
),

# ============================================================
# 9. hand-balm-gift.html
# ============================================================
dict(
    slug="hand-balm-gift",
    title="香りで選ぶ韓国ハンドバーム｜LUMINOVE",
    meta_desc="韓国ハンドバームを香りで選ぶポイントを解説。使い方や向いている人、プレゼントに選ぶ際の注意点までわかりやすく紹介します。",
    tag="ギフトガイド / ハンドバーム",
    h1="香りで選ぶ韓国ハンドバーム",
    h1_plain="香りで選ぶ韓国ハンドバーム",
    image="https://www.luminove.online/images/product-handbalm-mev.webp",
    lead="ハンドバームはちょっとしたプレゼントにも人気のアイテムです。初めて選ぶ方にもわかりやすく、香りで選ぶときのポイントとおすすめのシーンを紹介します。",
    conclusion="ハンドバームは香りの系統とテクスチャーで選ぶのがポイント。シーンや贈る相手の好みに合わせて選ぶと失敗しにくくなります。",
    sections=[
        ("ハンドバームとは（初心者向け解説）", "      <p>ハンドバームは、シアバターなどの保湿成分をベースにした固形タイプのハンドケアアイテムです。クリームよりも濃厚なテクスチャーが多く、体温でとろけるように肌に伸びるのが特徴です。香りを楽しめる製品が多く、保湿とリラックスを同時に楽しめます。</p>"),
        ("選び方", "      <p>香りの系統で選ぶのがおすすめです。マリン系・ウッディ系・フローラル系など、好みやシーンに合わせて選べます。テクスチャーも製品によって異なるため、ベタつきが気になる方は伸びの良いタイプを選びましょう。</p>"),
        ("使い方", "      <p>適量を手に取り、体温で温めながら手肌全体に伸ばします。乾燥が気になる季節は、ハンドクリームの上に重ねて使うと保湿力がアップします。</p>"),
        ("こんな人におすすめ", "      <ul><li>香りを楽しみながらハンドケアをしたい方</li><li>ちょっとしたプレゼントを探している方</li><li>乾燥が気になる季節に集中保湿をしたい方</li></ul>"),
        ("プレゼントに選ぶ際の注意点", "      <p>香りの好みは人によって異なるため、贈る相手が好きな系統がわからない場合は、複数の香りを試せるセットを選ぶのもおすすめです。肌が敏感な方へ贈る場合は、無香料タイプの有無も確認しましょう。</p>"),
    ],
    ingredient_intro="ハンドケアと合わせて、スキンケアの注目成分もチェックしてみてください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("どんな人へのプレゼントに向いていますか？", "香りを楽しみたい方、ハンドケアを習慣にしたい方へのちょっとしたプレゼントに向いています。"),
        ("ベタつきは気になりますか？", "体温でとろけるテクスチャーの製品が多く、馴染みやすい使用感です。"),
        ("複数の香りを使い分けても良いですか？", "はい、シーンや気分に合わせて使い分ける方が多くいらっしゃいます。"),
        ("保管方法に注意点はありますか？", "シアバターベースの製品は高温で柔らかくなりやすいため、直射日光を避けて保管することをおすすめします。"),
        ("敏感肌でも使えますか？", "製品によって配合される香料や成分が異なります。敏感肌の方は無香料タイプや、成分表記を確認してから選ぶことをおすすめします。"),
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


print('=== ブログ記事9本を強化 ===')
for a in ARTICLES:
    html = render_article(a)
    path = f"blog/{a['slug']}.html"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    body_match = re.search(r'<body>(.*)</body>', html, re.DOTALL)
    body_text = body_match.group(1) if body_match else html
    body_text = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', body_text)
    text_only = re.sub(r'<[^>]+>', '', body_text)
    print(f'  Updated: {path} (本文文字数概算={len(text_only)})')

print('\n=== 完了 ===')
