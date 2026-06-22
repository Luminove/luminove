# -*- coding: utf-8 -*-
"""
優先記事6本に以下を追加:
- 冒頭: この記事でわかること + おすすめ商品導線 + 関連成分導線
- 末尾: Instagramリール30秒台本(可視) + STORES購入ボタン
- reel-data JSONを新形式(script配列)+指定テーマに更新
"""
import json, re

DATA = {
    "blog/glutathione-serum.html": dict(
        anchor_lead='<p class="article-lead">グルタチオン美容液は配合濃度や組み合わせ成分によって特徴が大きく異なります。初めて選ぶ方にもわかりやすく、失敗しない選び方のポイントを解説します。</p>',
        whatyouknow=[
            "グルタチオン美容液の選び方の基準（配合濃度・組み合わせ成分）",
            "美容液をいつ・どう使うか",
            "向いている人と使用時の注意点",
        ],
        product_url="https://luminove.stores.jp/items/679c79bb4c088e04f7df3970",
        product_name="グルコラ セラム（美容液）",
        ingredient_url="/ingredients/glutathione.html",
        ingredient_name="グルタチオン",
        reel_title="グルタチオン美容液って何が違う？",
        hook="その美容液、何が違うか説明できる？",
        script=[
            "「グルタチオン美容液、いろいろあるけど何が違うの？」",
            "選ぶポイントは配合濃度（ppm）と組み合わせ成分の2つ。",
            "1万ppm以上なら高濃度の部類。コラーゲンと組み合わせた製品なら、うるおいケアも一緒に。",
            "詳しい選び方はプロフィールのリンクからチェックしてね。",
        ],
        caption="グルタチオン美容液は配合濃度（ppm）と組み合わせ成分をチェックするのがポイントです✨ #グルタチオン美容液 #韓国コスメ",
        hashtags=["#グルタチオン", "#美容液", "#韓国コスメ", "#LUMINOVE"],
    ),
    "blog/pdrn-cream-how-to-choose.html": dict(
        anchor_lead='<p class="article-lead">韓国スキンケアで急速に普及したPDRNクリーム。種類が増えてきた今、どこを見て選べば良いのか迷う方も多いはず。初心者の方にもわかりやすく選び方のポイントを解説します。</p>',
        whatyouknow=[
            "PDRNクリームを選ぶときに確認したい3つのポイント",
            "配合濃度・組み合わせ成分・低刺激処方の見方",
            "施術後ケアに使う場合の注意点",
        ],
        product_url="https://luminove.stores.jp/?category_id=69b20f03c7a87210bb19aecc",
        product_name="リジュエヌ クリーム",
        ingredient_url="/ingredients/pdrn.html",
        ingredient_name="PDRN",
        reel_title="PDRNクリームを選ぶ時の3つのポイント",
        hook="PDRNクリーム、何を基準に選んでる？",
        script=[
            "PDRNクリーム選びで見るべきポイントは3つ。",
            "①配合濃度（ppm）②組み合わせ成分③低刺激処方かどうか。",
            "施術後のケアに使いたい人は、低刺激・無香料処方を必ず確認して。",
            "詳しくはプロフィールのリンクから読んでみてね。",
        ],
        caption="PDRNクリームは配合濃度・組み合わせ成分・処方の3点で選ぶのがコツです🧬 #PDRN #韓国スキンケア",
        hashtags=["#PDRN", "#韓国スキンケア", "#韓国コスメ", "#LUMINOVE"],
    ),
    "blog/nano-collagen.html": dict(
        anchor_lead='<p class="article-lead">「ナノコラーゲン」という言葉を韓国コスメでよく見かけるようになりました。通常のコラーゲンとどう違うのか、なぜ注目されているのかを初心者の方にもわかりやすく解説します。</p>',
        whatyouknow=[
            "ナノコラーゲン（300Da）が一般的なコラーゲンと違う理由",
            "選び方と使い方のポイント",
            "グルタチオンと組み合わせるメリット",
        ],
        product_url="https://luminove.stores.jp/items/679c7a41be9f7e04f4d0f9f9",
        product_name="グルコラ スキン（化粧水）",
        ingredient_url="/ingredients/nano-collagen.html",
        ingredient_name="ナノコラーゲン（300Da）",
        reel_title="ナノコラーゲン（300Da）とは？",
        hook="コラーゲンを「ナノ化」するとどう変わるか知ってる？",
        script=[
            "「ナノコラーゲン」って聞いたことある？",
            "分子サイズを300Daまで小さくした低分子コラーゲンのことなの。",
            "普通のコラーゲンより角質層までうるおいを届けやすい設計が特徴。",
            "詳しくはプロフィールのリンクから見てみて。",
        ],
        caption="韓国コスメで話題の「ナノコラーゲン（300Da）」。低分子化された注目成分です💧 #ナノコラーゲン #韓国コスメ",
        hashtags=["#ナノコラーゲン", "#コラーゲン", "#韓国コスメ", "#LUMINOVE"],
    ),
    "blog/korean-skincare-routine.html": dict(
        anchor_lead='<p class="article-lead">韓国スキンケアは多層的なケアが特徴と言われますが、基本となる順番を押さえれば毎日のルーティンは難しくありません。基本ステップを解説します。</p>',
        whatyouknow=[
            "韓国スキンケアの基本の順番",
            "各ステップで意識したいポイント",
            "成分で選ぶルーティン例",
        ],
        product_url="https://luminove.stores.jp/items/679c1f75d944440bead08a2d",
        product_name="グルコラ クレンジングフォーム",
        ingredient_url="/ingredients/glutathione.html",
        ingredient_name="グルタチオン",
        reel_title="韓国スキンケアの順番",
        hook="その順番、実は間違ってるかも？",
        script=[
            "韓国スキンケアの基本は「水分の多いものから少ないものへ」。",
            "クレンジング→化粧水→美容液→乳液の順が基本。",
            "難しく考えずに、この順番だけ覚えればOK。",
            "詳しくはプロフィールのリンクから見てみて。",
        ],
        caption="韓国スキンケアの基本ステップをおさらい。水分量の多い順に重ねるのがポイントです✨ #韓国スキンケア #スキンケアルーティン",
        hashtags=["#韓国スキンケア", "#スキンケアルーティン", "#美容", "#LUMINOVE"],
    ),
    "blog/korean-skincare-for-40s.html": dict(
        anchor_lead='<p class="article-lead">40代になると、20〜30代の頃とは違う肌の変化を感じる方も多いはず。ハリ感やうるおいを重視した韓国スキンケアの選び方を、初心者の方にもわかりやすく解説します。</p>',
        whatyouknow=[
            "40代の肌で意識したい3つのポイント",
            "高濃度処方・ハリ感成分の選び方",
            "向いている人と注意点",
        ],
        product_url="https://luminove.stores.jp/items/679c79bb4c088e04f7df3970",
        product_name="グルコラ セラム（美容液）",
        ingredient_url="/ingredients/glutathione.html",
        ingredient_name="グルタチオン",
        reel_title="40代からの韓国スキンケア",
        hook="40代から変えたいスキンケアのポイント",
        script=[
            "40代からはハリ感・うるおい・透明感の3つにアプローチする成分を意識するのがおすすめ。",
            "グルタチオン・ナノコラーゲン・RG3を組み合わせて使う人も増えてるよ。",
            "高濃度処方を選ぶのもポイント。",
            "詳しくはプロフィールのリンクから見てみて。",
        ],
        caption="40代からの韓国スキンケアはハリ感・うるおい・透明感を意識して選ぶのがポイント✨ #韓国スキンケア #40代スキンケア",
        hashtags=["#韓国スキンケア", "#40代スキンケア", "#エイジングケア", "#LUMINOVE"],
    ),
    "blog/korean-skincare-for-men.html": dict(
        anchor_lead='<p class="article-lead">韓国スキンケアは男性にも取り入れやすいアイテムが増えています。何から始めれば良いかわからない方にもわかりやすく、基本のステップと選び方を解説します。</p>',
        whatyouknow=[
            "男性のスキンケアで意識したいポイント",
            "洗顔・保湿・UVケアの基本ステップ",
            "シンプルに続けられるルーティン例",
        ],
        product_url="https://luminove.stores.jp/items/679c1f75d944440bead08a2d",
        product_name="グルコラ クレンジングフォーム",
        ingredient_url="/ingredients/glutathione.html",
        ingredient_name="グルタチオン",
        reel_title="男性にも使いやすい韓国スキンケア",
        hook="スキンケアって何からやればいいの？",
        script=[
            "男性のスキンケアは洗顔・保湿・UVケアの3ステップから始めるのがおすすめ。",
            "多機能なアイテムを選べばシンプルに続けられるよ。",
            "まずは洗顔だけでも変えてみて。",
            "詳しくはプロフィールのリンクから見てみて。",
        ],
        caption="男性にも使いやすい韓国スキンケア。洗顔・保湿・UVケアの基本ステップから始めよう✨ #韓国スキンケア #メンズスキンケア",
        hashtags=["#韓国スキンケア", "#メンズスキンケア", "#韓国コスメ", "#LUMINOVE"],
    ),
}

for path, d in DATA.items():
    with open(path, encoding='utf-8') as f:
        text = f.read()
    original = text

    # 1. reel-data JSON更新(配列形式)
    reel_json = json.dumps({
        "reel": {
            "reel_title": d["reel_title"],
            "hook": d["hook"],
            "script": d["script"],
            "caption": d["caption"],
            "hashtags": d["hashtags"],
        }
    }, ensure_ascii=False, indent=2)
    text = re.sub(
        r'<script type="application/json" id="reel-data">\s*\{.*?\}\s*</script>',
        f'<script type="application/json" id="reel-data">\n  {reel_json}\n  </script>',
        text, count=1, flags=re.DOTALL
    )

    # 2. 冒頭に「この記事でわかること」+ 導線 を挿入
    whatyouknow_li = ''.join(f'<li>{w}</li>' for w in d['whatyouknow'])
    intro_block = f'''
  <div style="max-width:720px;margin:0 auto 2rem;padding:0 5%">
    <div style="background:var(--green-mist);border-radius:12px;padding:1.5rem 1.8rem">
      <h2 style="font-size:.95rem;color:var(--green-deep);margin-bottom:.8rem;font-weight:600">この記事でわかること</h2>
      <ul style="font-size:.88rem;color:var(--text-mid);line-height:1.9;margin:0 0 1rem 1.2rem">{whatyouknow_li}</ul>
      <div style="display:flex;flex-wrap:wrap;gap:.6rem">
        <a href="{d['product_url']}" target="_blank" rel="noopener" style="display:inline-block;font-size:.82rem;font-weight:500;color:#fff;background:var(--green-deep);border-radius:50px;padding:.5rem 1.2rem;text-decoration:none">おすすめ商品：{d['product_name']} →</a>
        <a href="{d['ingredient_url']}" style="display:inline-block;font-size:.82rem;font-weight:500;color:var(--green-deep);background:#fff;border:1px solid var(--green-pale);border-radius:50px;padding:.5rem 1.2rem;text-decoration:none">関連成分：{d['ingredient_name']}とは？ →</a>
      </div>
    </div>
  </div>
'''
    if d['anchor_lead'] not in text:
        print(f'  WARN anchor_lead not found in {path}')
    else:
        # article-lead を含む </article> の直後に挿入
        idx = text.find(d['anchor_lead'])
        end_article = text.find('</article>', idx)
        if end_article == -1:
            print(f'  WARN </article> not found after lead in {path}')
        else:
            insert_pos = end_article + len('</article>')
            text = text[:insert_pos] + '\n' + intro_block + text[insert_pos:]

    # 3. 末尾(フッター直前)にInstagramリール台本+STORES購入ボタンを追加
    script_li = ''.join(f'<li>{s}</li>' for s in d['script'])
    outro_block = f'''
  <section style="max-width:720px;margin:0 auto 3rem;padding:0 5%">
    <div style="background:var(--green-mist);border-radius:12px;padding:1.5rem 1.8rem">
      <h2 style="font-size:1rem;color:var(--green-deep);margin-bottom:.8rem;font-weight:600">Instagramリール台本（30秒）</h2>
      <ol style="font-size:.88rem;color:var(--text-mid);line-height:1.9;margin:0 0 1rem 1.2rem">{script_li}</ol>
      <p style="font-size:.78rem;color:var(--text-light);margin:0">フック：{d['hook']}</p>
    </div>
  </section>
  <div style="text-align:center;margin:0 auto 3rem">
    <a href="{d['product_url']}" target="_blank" rel="noopener" class="btn-primary">{d['product_name']}をSTORESで購入する →</a>
  </div>
'''
    footer_idx = text.find('  <footer>')
    if footer_idx == -1:
        print(f'  WARN <footer> not found in {path}')
    else:
        text = text[:footer_idx] + outro_block + '\n' + text[footer_idx:]

    if text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'  Updated: {path}')
    else:
        print(f'  NO CHANGE: {path}')

print('\n=== 完了 ===')
