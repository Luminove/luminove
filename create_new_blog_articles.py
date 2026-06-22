# -*- coding: utf-8 -*-
"""
新規ブログ記事5本作成
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
    .article-section table { width: 100%; border-collapse: collapse; font-size: .88rem; margin-bottom: 1rem; }
    .article-section th, .article-section td { text-align: left; padding: .6rem .8rem; border-bottom: 1px solid var(--green-pale); }
    .article-section th { background: var(--green-pale); color: var(--green-deep); font-weight: 600; }
    .table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .cta-box { text-align: center; background: var(--green-mist); border-radius: var(--radius); padding: 2rem 1.5rem; margin: 2rem 0; }
    .cta-box p { font-size: .92rem; color: var(--text-mid); margin-bottom: 1.2rem; }
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
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a['faq']]
    }, ensure_ascii=False)
    breadcrumb_jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TOP", "item": "https://www.luminove.online/"},
            {"@type": "ListItem", "position": 2, "name": "ブログ", "item": "https://www.luminove.online/blog/"},
            {"@type": "ListItem", "position": 3, "name": a['h1_plain'], "item": f"https://www.luminove.online/blog/{a['slug']}.html"}
        ]
    }, ensure_ascii=False)
    article_jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": a['h1_plain'], "description": a['meta_desc'],
        "url": f"https://www.luminove.online/blog/{a['slug']}.html", "image": a['image'],
        "publisher": {"@type": "Organization", "name": "LUMINOVE", "url": "https://www.luminove.online"},
        "datePublished": "2026-06-22", "dateModified": "2026-06-22"
    }, ensure_ascii=False)
    reel_jsonld = json.dumps({"reel": a['reel']}, ensure_ascii=False, indent=2)

    faq_html = ''.join(f'''    <details class="faq-item">
      <summary class="faq-question">{q}<span class="faq-icon">＋</span></summary>
      <p class="faq-answer">{ans}</p>
    </details>
''' for q, ans in a['faq'])

    related_html = ''.join(f'''      <a href="{url}" class="related-card">
        <img src="{img}" alt="{name}" loading="lazy" />
        <p>{name}</p>
      </a>
''' for url, img, name in a['related'])

    ingredient_links_html = ''.join(f'        <a href="{url}">{name} →</a>\n' for url, name in a['ingredient_links'])

    sections_html = ''
    for i, (h2, body) in enumerate(a['sections']):
        sections_html += f'''
    <section class="article-section" id="sec{i+1}">
      <h2>{h2}</h2>
{body}
    </section>
'''

    return f'''<!DOCTYPE html>
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


ARTICLES = [

dict(
    slug="pdrn-cream-how-to-choose",
    title="PDRNクリームの選び方｜韓国スキンケアで注目される理由",
    meta_desc="PDRNクリームの選び方を解説。配合濃度の見方、低刺激処方の確認方法、向いている人や使い方までわかりやすく紹介します。",
    tag="選び方ガイド / PDRNクリーム",
    h1="PDRNクリームの選び方｜<br>韓国スキンケアで注目される理由",
    h1_plain="PDRNクリームの選び方｜韓国スキンケアで注目される理由",
    image="https://www.luminove.online/images/product-rejun-cream.webp",
    lead="韓国スキンケアで急速に普及したPDRNクリーム。種類が増えてきた今、どこを見て選べば良いのか迷う方も多いはず。初心者の方にもわかりやすく選び方のポイントを解説します。",
    conclusion="PDRNクリームは配合濃度（ppm）・組み合わせ成分・低刺激処方かどうかの3点で選ぶのがポイント。施術後のデリケートな肌を想定した処方かも確認しましょう。",
    sections=[
        ("PDRNクリームとは", "      <p>PDRNクリームは、サーモン由来のDNA断片であるPDRNを配合したクリームです。水光注射という美容医療施術の成分としても知られていますが、クリームとして経皮吸収で取り入れるタイプは、毎日のスキンケアに組み込みやすいのが特徴です。</p>"),
        ("選び方①：配合濃度を確認する", "      <p>PDRNの配合量はppm表記が一般的です。LUMINOVEで取り扱うリジュエヌ クリームはPDRN3000ppmを配合しています。配合量はパッケージや商品ページの成分表記で確認できます。</p>"),
        ("選び方②：組み合わせ成分を確認する", "      <p>PDRN単体よりも、NMNやEGF、セラミドNPなど他の美容成分と組み合わせた製品の方が、複数の角度からのケアが期待できます。自分の肌悩みに合わせて組み合わせ成分を確認しましょう。</p>"),
        ("選び方③：低刺激処方かどうか", "      <p>施術後のデリケートな肌を想定して、低刺激・無香料処方で設計された製品もあります。敏感肌の方や施術後のケアに使いたい方は、処方の特徴を商品ページで確認することをおすすめします。</p>"),
        ("使い方と向いている人", "      <p>化粧水で肌を整えた後、保湿クリームとして使用するのが基本です。施術後のデリケートな肌の保湿ケアをしたい方、ニキビ跡やくすみが気になる方、肌コンディションを整えるケアを探している方に向いています。</p>"),
        ("使用時の注意点", "      <p>サーモン由来の成分のため、サーモンアレルギーがある方はご注意ください。初めて使用する際はパッチテストをおすすめします。施術直後に使用する場合は、施術を行ったクリニックに確認すると安心です。</p>"),
    ],
    ingredient_intro="PDRNと組み合わせて配合されることが多いNMNについても、あわせてご覧ください。",
    ingredient_links=[("/ingredients/pdrn.html", "PDRNとは？"), ("/ingredients/nmn.html", "NMNとは？")],
    faq=[
        ("PDRNクリームはどのくらいの頻度で使えば良いですか？", "多くの製品が毎日の朝晩のケアに使用できる設計です。商品の使用方法に従ってご使用ください。"),
        ("水光注射の代わりになりますか？", "クリームと注射は吸収経路が異なります。注射は直接注入する施術、クリームは経皮吸収による働きが主となるため、補完的な日常ケアとして取り入れるのがおすすめです。"),
        ("どんな人が使っていますか？", "施術後のデリケートな肌のケアをしたい方、肌コンディションが気になる方に選ばれています。"),
        ("PDRNとPNTXは同じ成分ですか？", "どちらもサーモン由来DNAを原料とする成分ですが、分子量や精製方法に違いがあります。商品の成分表記で確認することをおすすめします。"),
        ("化粧水や日焼け止めと併用できますか？", "はい、化粧水で肌を整えた後にクリームを重ねる、日焼け止めと組み合わせるなど、通常のスキンケアステップに取り入れて問題ありません。"),
    ],
    related=[
        ("/ingredients/pdrn.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRN<br>成分詳細ページ"),
        ("/blog/pdrn-what-is.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRNとは？<br>成分解説"),
        ("/products/rejun-pdrn-cream.html", "https://www.luminove.online/images/product-rejun-cream.webp", "リジュエヌ クリーム<br>（PDRN×NMN）"),
    ],
    reel=dict(
        reel_title="PDRNクリーム、選び方で失敗しないコツ",
        hook="PDRNクリーム、何を基準に選んでる？",
        script="PDRNクリーム選びは配合濃度・組み合わせ成分・低刺激処方の3つがポイント。施術後のケアに使いたい人は、低刺激処方かどうかも要チェック。",
        caption="PDRNクリームは配合濃度・組み合わせ成分・処方の3点で選ぶのがコツです🧬 #PDRN #韓国スキンケア",
        hashtags=["#PDRN", "#韓国スキンケア", "#韓国コスメ", "#LUMINOVE"]
    ),
),

dict(
    slug="glutathione-vs-niacinamide",
    title="グルタチオンとナイアシンアミドの違い｜透明感ケアで選ぶなら？",
    meta_desc="グルタチオンとナイアシンアミドの違いを解説。それぞれの特徴・選び方・組み合わせ方まで初心者にもわかりやすく紹介します。",
    tag="成分比較 / グルタチオン×ナイアシンアミド",
    h1="グルタチオンとナイアシンアミドの違い｜<br>透明感ケアで選ぶなら？",
    h1_plain="グルタチオンとナイアシンアミドの違い｜透明感ケアで選ぶなら？",
    image="https://www.luminove.online/images/product-serum.webp",
    lead="透明感ケアの成分としてよく比較される「グルタチオン」と「ナイアシンアミド」。それぞれの特徴と違いを初心者の方にもわかりやすく解説し、選び方の参考になる情報をまとめました。",
    conclusion="グルタチオンは抗酸化ケア由来のアプローチ、ナイアシンアミドはビタミンB3由来のアプローチで、それぞれ異なる仕組みを持つ成分です。組み合わせて使うことも可能です。",
    sections=[
        ("グルタチオンとは", "      <p>グルタチオンは、グルタミン酸・システイン・グリシンの3つのアミノ酸からなるトリペプチドで、強力な抗酸化作用を持つ成分です。美容点滴（白玉注射）の主成分として知られ、近年は化粧品への高濃度配合が進んでいます。</p>"),
        ("ナイアシンアミドとは", "      <p>ナイアシンアミドはビタミンB3の一種で、韓国コスメだけでなく世界中のスキンケアで広く使われている成分です。肌のバリア機能サポートやキメを整えるケアに使われることが多く、比較的多くの製品に配合されています。</p>"),
        ("2つの違いを比較", "      <div class=\"table-scroll\"><table><tr><th>項目</th><th>グルタチオン</th><th>ナイアシンアミド</th></tr><tr><td>由来</td><td>アミノ酸由来のトリペプチド</td><td>ビタミンB3由来</td></tr><tr><td>主なアプローチ</td><td>抗酸化ケア・メラニン生成に着目したケア</td><td>肌のキメ・バリア機能に着目したケア</td></tr><tr><td>配合の広がり</td><td>韓国コスメで高濃度配合が進む</td><td>世界中のスキンケアで広く配合</td></tr></table></div>"),
        ("どちらを選ぶべきか", "      <p>透明感・くすみが気になる方はグルタチオン配合製品、キメや肌の質感を整えたい方はナイアシンアミド配合製品が選ばれる傾向にあります。両方を求める場合は、2成分を組み合わせた製品を選ぶのもひとつの方法です。</p>"),
        ("組み合わせて使う場合の注意点", "      <p>どちらも比較的低刺激とされる成分ですが、高濃度配合製品を併用する場合は、まず1つの製品でパッチテストを行い、肌の様子を見ながら徐々に追加することをおすすめします。</p>"),
    ],
    ingredient_intro="LUMINOVEで取り扱うグルタチオン配合商品の詳細もご覧ください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("グルタチオンとナイアシンアミドは併用できますか？", "はい、異なるアプローチを持つ成分のため併用される方が多くいらっしゃいます。まずは少量から試すことをおすすめします。"),
        ("どちらが透明感ケアに向いていますか？", "グルタチオンは抗酸化ケアとメラニン生成に着目したアプローチを持つ成分として、透明感ケアに選ばれることが多い成分です。"),
        ("敏感肌でも使えますか？", "どちらも比較的低刺激とされていますが、配合される他の成分によって異なります。初回はパッチテストをおすすめします。"),
        ("配合濃度はどう確認すれば良いですか？", "成分表記やppm表示で確認できます。LUMINOVEの商品ページでは配合量を明記しています。"),
        ("毎日両方使っても良いですか？", "多くの製品は毎日の使用を前提に設計されています。肌の状態を見ながら継続することをおすすめします。"),
    ],
    related=[
        ("/ingredients/glutathione.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオン<br>成分詳細ページ"),
        ("/products/glucola-serum.html", "https://www.luminove.online/images/product-serum.webp", "グルコラ セラム<br>（美容液）"),
        ("/blog/glutathione-what-is.html", "https://www.luminove.online/images/product-serum.webp", "グルタチオンとは？<br>成分解説"),
    ],
    reel=dict(
        reel_title="グルタチオン vs ナイアシンアミド、結局どっち？",
        hook="透明感ケア、どの成分を選ぶべき？",
        script="グルタチオンは抗酸化ケア由来、ナイアシンアミドはビタミンB3由来。それぞれ違うアプローチを持つ成分なの。組み合わせて使うのもアリだよ。",
        caption="グルタチオンとナイアシンアミドの違いを比較。それぞれの特徴を知って選ぼう✨ #グルタチオン #ナイアシンアミド #韓国コスメ",
        hashtags=["#グルタチオン", "#ナイアシンアミド", "#韓国コスメ", "#LUMINOVE"]
    ),
),

dict(
    slug="korean-skincare-for-40s",
    title="40代からの韓国スキンケア｜ハリ感とうるおいを重視する選び方",
    meta_desc="40代からの韓国スキンケアの選び方を解説。ハリ感とうるおいを重視した成分選びや使い方、注意点までわかりやすく紹介します。",
    tag="世代別ガイド / 40代スキンケア",
    h1="40代からの韓国スキンケア｜<br>ハリ感とうるおいを重視する選び方",
    h1_plain="40代からの韓国スキンケア｜ハリ感とうるおいを重視する選び方",
    image="https://www.luminove.online/images/product-serum.webp",
    lead="40代になると、20〜30代の頃とは違う肌の変化を感じる方も多いはず。ハリ感やうるおいを重視した韓国スキンケアの選び方を、初心者の方にもわかりやすく解説します。",
    conclusion="40代の韓国スキンケアは、ハリ感・うるおい・透明感の3点にアプローチする成分を重視して選ぶのがポイント。高濃度処方と組み合わせ成分を確認しましょう。",
    sections=[
        ("40代の肌で意識したいポイント（初心者向け解説）", "      <p>40代になると、うるおい不足やハリ不足を感じやすくなる方が増えてきます。スキンケアでは、抗酸化ケアにアプローチするグルタチオンや、うるおい・ハリ印象にアプローチするナノコラーゲン（300Da）など、複数の角度からケアする成分を組み合わせるのがおすすめです。</p>"),
        ("選び方：高濃度処方を確認する", "      <p>40代からのスキンケアは、配合濃度（ppm表記）を確認し、できれば高濃度の製品を選ぶと実感しやすいとされています。LUMINOVEのグルコラ セラムはグルタチオン30,000ppmという高濃度配合です。</p>"),
        ("選び方：ハリ感成分を組み合わせる", "      <p>RG3（高麗人参由来の希少サポニン）のようなハリ感・うるおい・キメを整える成分も、40代からのスキンケアで注目されています。グルタチオンやナノコラーゲンと組み合わせることで、複数の角度からケアできます。</p>"),
        ("使い方", "      <p>化粧水→美容液→クリームの順で重ねるのが基本です。集中ケアをしたい部位には、美容液を多めに重ねづけするのもおすすめです。継続使用が前提の成分が多いため、28日間を目安に使い続けてみましょう。</p>"),
        ("こんな人におすすめ", "      <ul><li>うるおい不足やハリ不足を感じ始めている方</li><li>これまでのスキンケアに高機能成分を取り入れたい方</li><li>透明感とハリ感を同時にケアしたい方</li></ul>"),
        ("注意点", "      <p>高濃度配合製品は、初めて使用する際にパッチテストを実施することをおすすめします。複数の高機能成分を一度に取り入れる場合は、1つずつ試しながら肌の状態を確認しましょう。</p>"),
    ],
    ingredient_intro="40代からのスキンケアで注目される成分をまとめてチェックできます。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？"), ("/ingredients/rg3.html", "RG3とは？")],
    faq=[
        ("40代から韓国スキンケアを始めるのは遅くないですか？", "いつから始めても問題ありません。まずは洗顔・化粧水・美容液の基本ステップから取り入れるのがおすすめです。"),
        ("高濃度処方は刺激が強いのですか？", "配合濃度が高いことと刺激の強さは必ずしも一致しません。ただし初めて使用する際はパッチテストをおすすめします。"),
        ("RG3とグルタチオンは一緒に使えますか？", "はい、異なるアプローチを持つ成分のため、組み合わせて使用される方が多くいらっしゃいます。"),
        ("どのくらいの期間で変化を感じやすいですか？", "肌のターンオーバー周期である28日間を目安に、継続使用することをおすすめします。"),
        ("乾燥が気になる場合はどうすれば良いですか？", "ナノコラーゲン（300Da）のような低分子保湿成分を配合した製品を選ぶと、うるおい感をサポートしやすくなります。"),
    ],
    related=[
        ("/products/glucola-serum.html", "https://www.luminove.online/images/product-serum.webp", "グルコラ セラム<br>（美容液）"),
        ("/products/rg3-vital-ampoule.html", "https://www.luminove.online/images/product-rg3-serum.webp", "クイーンズ RG3<br>モイスチャーセラム"),
        ("/blog/korean-skincare-recommended.html", "https://www.luminove.online/images/hero-all.webp", "韓国スキンケア<br>おすすめ2026"),
    ],
    reel=dict(
        reel_title="40代の韓国スキンケア、何を重視する？",
        hook="40代から変えたいスキンケアのポイント",
        script="40代からはハリ感・うるおい・透明感の3つにアプローチする成分を意識するのがおすすめ。グルタチオン・ナノコラーゲン・RG3を組み合わせて使う人も増えてるよ。",
        caption="40代からの韓国スキンケアはハリ感・うるおい・透明感を意識して選ぶのがポイント✨ #韓国スキンケア #40代スキンケア",
        hashtags=["#韓国スキンケア", "#40代スキンケア", "#エイジングケア", "#LUMINOVE"]
    ),
),

dict(
    slug="korean-skincare-for-men",
    title="男性にも使いやすい韓国スキンケア｜洗顔・保湿・UVケアの基本",
    meta_desc="男性にも使いやすい韓国スキンケアを解説。洗顔・保湿・UVケアの基本ステップと選び方をわかりやすく紹介します。",
    tag="男性向けガイド / 韓国スキンケア",
    h1="男性にも使いやすい韓国スキンケア｜<br>洗顔・保湿・UVケアの基本",
    h1_plain="男性にも使いやすい韓国スキンケア｜洗顔・保湿・UVケアの基本",
    image="https://www.luminove.online/images/product-cleanser.webp",
    lead="韓国スキンケアは男性にも取り入れやすいアイテムが増えています。何から始めれば良いかわからない方にもわかりやすく、基本のステップと選び方を解説します。",
    conclusion="男性のスキンケアは洗顔・保湿・UVケアの3ステップから始めるのがおすすめ。多機能なアイテムを選ぶことで、シンプルなルーティンでも続けやすくなります。",
    sections=[
        ("男性のスキンケアで意識したいポイント（初心者向け解説）", "      <p>男性の肌は皮脂量が多い傾向があるため、洗顔と保湿のバランスが大切です。洗いすぎると乾燥につながることがあるため、洗浄力と保湿成分のバランスが良いアイテムを選ぶのがポイントです。</p>"),
        ("選び方：まずは洗顔から", "      <p>クレンジング・洗顔・シェービングなど多機能に使える洗顔料は、スキンケアに時間をかけにくい方にもおすすめです。グルタチオンやナノコラーゲン（300Da）配合の洗顔料であれば、洗いながらうるおいケアもできます。</p>"),
        ("選び方：保湿は軽いテクスチャーから", "      <p>べたつきが気になる方は、とろみのある化粧水や軽めの乳液から試すのがおすすめです。乾燥が気になる季節は、美容液やクリームをプラスして保湿力を高めましょう。</p>"),
        ("選び方：UVケアも忘れずに", "      <p>日焼け止めは肌の状態に関わらず取り入れたいアイテムです。白浮きしにくいテクスチャーの製品を選べば、メイクをしない男性でも違和感なく使えます。</p>"),
        ("基本のルーティン", "      <ol><li>洗顔（朝晩）</li><li>化粧水で水分補給</li><li>気になる方は美容液を追加</li><li>乳液・クリームで保湿</li><li>日焼け止め（朝のみ）</li></ol>"),
        ("注意点", "      <p>髭剃り後は肌が敏感になりやすいため、刺激の少ない処方の製品を選ぶことをおすすめします。初めて使用する製品は、パッチテストを行うと安心です。</p>"),
    ],
    ingredient_intro="洗顔からUVケアまで使えるグルタチオン・ナノコラーゲン配合シリーズをチェックしてみてください。",
    ingredient_links=[("/ingredients/glutathione.html", "グルタチオンとは？"), ("/ingredients/nano-collagen.html", "ナノコラーゲン（300Da）とは？")],
    faq=[
        ("男性でも韓国スキンケアは使えますか？", "はい、性別に関わらず使用できる製品がほとんどです。多機能なアイテムから始めると取り入れやすくなります。"),
        ("スキンケアは何ステップから始めれば良いですか？", "まずは洗顔と保湿の2ステップから始め、慣れてきたら美容液や日焼け止めを追加するのがおすすめです。"),
        ("髭剃り後に使っても良いですか？", "刺激の少ない処方の製品であれば使用できますが、肌に異常を感じた場合は使用を中止してください。"),
        ("べたつきが気になる場合はどうすれば良いですか？", "とろみのある化粧水や軽めの乳液など、テクスチャーの軽い製品を選ぶとべたつきを抑えやすくなります。"),
        ("毎日続けられるシンプルなルーティンはありますか？", "洗顔・化粧水・日焼け止めの3ステップであれば、忙しい方でも続けやすいシンプルなルーティンになります。"),
    ],
    related=[
        ("/products/glucola-cleansing-foam.html", "https://www.luminove.online/images/product-cleanser.webp", "グルコラ<br>クレンジングフォーム"),
        ("/products/glucola-suncream.html", "https://www.luminove.online/images/product-suncream.webp", "グルコラ<br>サンクリーム"),
        ("/blog/korean-skincare-recommended.html", "https://www.luminove.online/images/hero-all.webp", "韓国スキンケア<br>おすすめ2026"),
    ],
    reel=dict(
        reel_title="男性向け韓国スキンケア、何から始める？",
        hook="スキンケアって何からやればいいの？",
        script="男性のスキンケアは洗顔・保湿・UVケアの3ステップから始めるのがおすすめ。多機能なアイテムを選べばシンプルに続けられるよ。",
        caption="男性にも使いやすい韓国スキンケア。洗顔・保湿・UVケアの基本ステップから始めよう✨ #韓国スキンケア #メンズスキンケア",
        hashtags=["#韓国スキンケア", "#メンズスキンケア", "#韓国コスメ", "#LUMINOVE"]
    ),
),

dict(
    slug="pdrn-after-treatment-skincare",
    title="美容施術後の保湿ケアに注目されるPDRNスキンケアとは？",
    meta_desc="美容施術後の保湿ケアに注目されるPDRNスキンケアを解説。選び方・使い方・注意点まで初心者にもわかりやすく紹介します。",
    tag="施術後ケア / PDRNスキンケア",
    h1="美容施術後の保湿ケアに注目される<br>PDRNスキンケアとは？",
    h1_plain="美容施術後の保湿ケアに注目されるPDRNスキンケアとは？",
    image="https://www.luminove.online/images/product-rejun-cream.webp",
    lead="美容施術を受けた後のデリケートな肌に、PDRN配合スキンケアを取り入れる方が増えています。初めての方にもわかりやすく、選び方や使い方を解説します。",
    conclusion="美容施術後の保湿ケアには、低刺激・無香料処方のPDRN配合スキンケアが選ばれる傾向にあります。使用前には施術を行ったクリニックへの確認をおすすめします。",
    sections=[
        ("施術後のデリケートな肌とPDRN（初心者向け解説）", "      <p>レーザーやピーリングなどの美容施術後は、肌がデリケートな状態になりやすいとされています。PDRN（ポリデオキシリボヌクレオチド）は、肌コンディションに着目したアプローチを持つ成分として、施術後のホームケアに取り入れられることが増えています。</p>"),
        ("選び方：低刺激・無香料処方を確認する", "      <p>施術後のデリケートな肌を想定して、低刺激・無香料処方で設計された製品を選びましょう。LUMINOVEのリジュエヌ クリームは、施術後の保湿ケアを主目的とした処方です。</p>"),
        ("選び方：配合成分の組み合わせを確認する", "      <p>PDRN単体ではなく、NMNやEGF、セラミドNPなど保湿・バリアサポート成分と組み合わせた製品を選ぶと、複数の角度からケアできます。</p>"),
        ("使い方", "      <p>施術後は、施術を行ったクリニックの指示に従って使用を開始してください。一般的には、洗顔・化粧水で肌を整えた後、保湿クリームとして使用します。</p>"),
        ("こんな人におすすめ", "      <ul><li>美容施術を控えている、または受けた直後の方</li><li>肌のコンディションが不安定になりやすい方</li><li>低刺激処方のスキンケアを探している方</li></ul>"),
        ("使用時の注意点", "      <p>サーモン由来の成分が含まれるため、サーモンアレルギーがある方はご注意ください。施術直後の使用については、自己判断せず施術を行ったクリニックに確認することを強くおすすめします。</p>"),
    ],
    ingredient_intro="PDRNと組み合わせて配合されることが多いNMNについてもご確認ください。",
    ingredient_links=[("/ingredients/pdrn.html", "PDRNとは？"), ("/ingredients/nmn.html", "NMNとは？")],
    faq=[
        ("施術後すぐに使用できますか？", "施術直後の使用については、自己判断せず施術を行ったクリニックに確認することをおすすめします。"),
        ("どんな施術後のケアに向いていますか？", "レーザー・ピーリング・注射系施術など、肌がデリケートな状態になりやすい施術後のケアを想定して設計された製品があります。"),
        ("毎日使用しても良いですか？", "低刺激・無香料処方の製品であれば、毎日のケアに使用できる設計のものが多くあります。"),
        ("施術を受けていなくても使えますか？", "はい、肌コンディションが気になる方であれば、施術の有無に関わらず日常のスキンケアとして使用できます。"),
        ("敏感肌の場合の注意点はありますか？", "サーモンアレルギーがある方はご注意ください。敏感肌の方は初回使用前にパッチテストを実施することをおすすめします。"),
    ],
    related=[
        ("/ingredients/pdrn.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRN<br>成分詳細ページ"),
        ("/products/rejun-pdrn-cream.html", "https://www.luminove.online/images/product-rejun-cream.webp", "リジュエヌ クリーム<br>（PDRN×NMN）"),
        ("/blog/pdrn-cream-how-to-choose.html", "https://www.luminove.online/images/product-rejun-cream.webp", "PDRNクリームの<br>選び方"),
    ],
    reel=dict(
        reel_title="施術後のケア、PDRNが選ばれる理由",
        hook="美容施術の後、どんなケアしてる？",
        script="美容施術後のデリケートな肌には、低刺激・無香料処方のPDRN配合クリームを選ぶ人が増えてるの。使用前には施術したクリニックに確認するのが安心だよ。",
        caption="美容施術後の保湿ケアにPDRN配合スキンケアが注目されています。低刺激処方かどうかを確認して選んで🧬 #PDRN #施術後ケア",
        hashtags=["#PDRN", "#施術後ケア", "#韓国コスメ", "#LUMINOVE"]
    ),
),

]

os.makedirs('blog', exist_ok=True)
print('=== 新規ブログ記事5本作成 ===')
for a in ARTICLES:
    html = render_article(a)
    path = f"blog/{a['slug']}.html"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    body_match = re.search(r'<body>(.*)</body>', html, re.DOTALL)
    body_text = body_match.group(1) if body_match else html
    body_text = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', body_text)
    text_only = re.sub(r'<[^>]+>', '', body_text)
    print(f'  Created: {path} (本文文字数概算={len(text_only)})')

print('\n=== 完了 ===')
