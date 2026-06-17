# -*- coding: utf-8 -*-
"""最終調整スクリプト: index.html 医師表現修正・レビュー重複削除"""
import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

original = html

# ============================================================
# 【1-a】メタタグ・OGP・Twitter修正
# ============================================================
html = html.replace(
    '<title>医師推薦の韓国コスメセレクトショップ｜LUMINOVE</title>',
    '<title>六本木BMC院長が商品選定に携わる韓国コスメセレクトショップ｜LUMINOVE</title>'
)
html = html.replace(
    '美容医療専門医が成分を厳選。グルタチオン・PDRN・コラーゲンなど機能性成分にこだわった韓国コスメブランドを厳選してお届けする、医師推薦のセレクトショップLUMINOVE。',
    '美容医療の知見を持つ六本木BMC院長が代表を務め、成分・品質面を重視して選定した韓国コスメブランドをお届けするセレクトショップLUMINOVE。グルタチオン・PDRN・コラーゲン配合ブランドに特化。'
)
html = html.replace(
    '<meta property="og:title" content="医師推薦の韓国コスメセレクトショップ｜LUMINOVE" />',
    '<meta property="og:title" content="六本木BMC院長が商品選定に携わる韓国コスメセレクトショップ｜LUMINOVE" />'
)
html = html.replace(
    '<meta name="twitter:title" content="医師推薦の韓国コスメセレクトショップ｜LUMINOVE" />',
    '<meta name="twitter:title" content="六本木BMC院長が商品選定に携わる韓国コスメセレクトショップ｜LUMINOVE" />'
)

# ============================================================
# 【1-b】JSON-LD Organization description & reviewBody
# ============================================================
html = html.replace(
    '"description": "六本木美容医療クリニック（BMC）院長と共同創業した韓国コスメのセレクトショップ。エクソソームや美容点滴など最先端の美容医療の知見を持つ医師が、数ある韓国コスメの中から成分を徹底調査し、日本人の肌に本当に合うものだけを厳選・推薦。洗顔・スキンケアからヘアケア・ハンドケアまで幅広い製品を提供。"',
    '"description": "六本木美容医療クリニック（BMC）院長・大久保義徳が代表を務める株式会社ルミノーブが運営する韓国コスメのセレクトショップ。グルタチオン・PDRN・コラーゲン・RG3など機能性成分を配合した韓国ブランドを、品質面を重視して選定しお届けしています。洗顔・スキンケアからヘアケア・ハンドケアまで幅広い製品を提供。"'
)
html = html.replace(
    '"reviewBody": "エクソソームや美容点滴など細胞レベルの再生医療に精通した医師が、数ある韓国コスメの中から成分を徹底調査し、日本人の肌に本当に合う製品だけを厳選・推薦しています。"',
    '"reviewBody": "六本木美容医療クリニック（BMC）院長・大久保義徳が代表として、成分やブランドの品質面を重視してLUMINOVEの取り扱い商品を選定しています。商品の処方設計・製品開発は各韓国ブランドが行っています。"'
)

# ============================================================
# 【1-c】商品JSON-LD description & reviewBody（代表商品）
# ============================================================
html = html.replace(
    '"description": "グルタチオン・300Daコラーゲン高配合の韓国発クレンジングフォーム。六本木BMC院長推薦。"',
    '"description": "グルタチオン・300Daコラーゲン高配合の韓国発クレンジングフォーム。LUMINOVEが品質面を重視してセレクト。"'
)
html = html.replace(
    '"reviewBody": "細胞レベルの再生医療に精通した医師が成分を徹底評価。グルタチオン・300Daコラーゲンの肌バリアサポート効果に着目し推薦。"',
    '"reviewBody": "六本木美容医療クリニック（BMC）院長が代表を務めるLUMINOVEが、成分コンセプト・品質面を重視してセレクトしています。"'
)
html = html.replace(
    '"reviewBody": "細胞レベルの再生医療に精通した医師が成分を徹底評価。300Daコラーゲンの浸透力と乳酸菌発酵による基礎力サポートに着目し推薦。"',
    '"reviewBody": "六本木美容医療クリニック（BMC）院長が代表を務めるLUMINOVEが、成分コンセプト・品質面を重視してセレクトしています。"'
)
html = html.replace(
    '"reviewBody": "美容点滴で知られるグルタチオンを高濃度30,000ppm配合。細胞レベルのアプローチに詳しい医師が成分を徹底評価し推薦。"',
    '"reviewBody": "六本木美容医療クリニック（BMC）院長が代表を務めるLUMINOVEが、成分コンセプト・品質面を重視してセレクトしています。"'
)

# ============================================================
# 【1-d】クリニック構造化データのコメント・description修正
# ============================================================
html = html.replace(
    '<!-- 構造化データ：提携クリニック（共同創業・成分推薦元） -->',
    '<!-- 構造化データ：代表が院長を務めるクリニック -->'
)
html = html.replace(
    '"description": "エクソソーム（幹細胞培養上清液）治療や美容点滴（白玉点滴など）をはじめとする、細胞レベルの再生美容医療を専門とするクリニック。LUMINOVEの共同創業者である院長が在籍し、最先端の美容医療の知見をもとにLUMINOVE製品の成分を評価・推薦している。"',
    '"description": "美容医療を専門とするクリニック。代表取締役・大久保義徳が院長を務めており、LUMINOVEは同医師が代表を務める株式会社ルミノーブが運営するセレクトショップです。"'
)

# ============================================================
# 【1-e】CSS content '院長推薦' 修正
# ============================================================
html = html.replace("content: '院長推薦';", "content: '医師が選定';")

# ============================================================
# 【1-f】ヒーローサブコピー修正
# ============================================================
html = html.replace(
    '美容医療の現場で使われる成分"グルタチオン、PDRN、コラーゲン"を軸に、六本木美容医療クリニックの院長が韓国の優良ブランドを厳選したコスメセレクトショップ。透明感あふれる肌へ導くトータルスキンケアをお届けします。',
    '美容医療の現場で使われる成分"グルタチオン、PDRN、コラーゲン"を軸に、六本木美容医療クリニックの院長が商品選定に携わる韓国コスメセレクトショップ。透明感あふれる肌へ導くトータルスキンケアをお届けします。'
)

# ============================================================
# 【1-g】Brand Values セクション
# ============================================================
html = html.replace(
    '<p class="value-text">美容医療の専門医が、韓国の最新ブランドを成分レベルで審査。<br>日本人の肌に合うものだけをラインナップに加えます。</p>',
    '<p class="value-text">美容医療の知見を持つ六本木BMC院長が代表を務めるLUMINOVEが、成分コンセプトと品質面を重視して韓国ブランドを選定しています。</p>'
)

# ============================================================
# 【1-h】SUPERVISORセクション 全面修正
# ============================================================
html = html.replace(
    '<p class="section-tag">Medical Recommendation</p>\n        <h2 class="section-title">美容医療の専門医が<br><span class="align-right">成分を厳選</span></h2>',
    '<p class="section-tag">Brand Curation</p>\n        <h2 class="section-title">美容医療の知見を活かした<br><span class="align-right">商品選定</span></h2>'
)
html = html.replace(
    'LUMINOVEは、六本木美容医療クリニック（BMC）院長とともに立ち上げたブランドです。再生医療・美容医療の専門医として、日々「内側から美をつくる」治療と向き合ってきた院長だからこそ、スキンケアにも同じ哲学を持ちます。韓国産の美容成分が日本人の肌質・体質に本当に適合するかを一つひとつ医学的に確認し、肌の自己再生力を妨げない製品だけをLUMINOVEは取り扱っています。',
    'LUMINOVEは、六本木美容医療クリニック（BMC）院長・大久保義徳が代表を務める株式会社ルミノーブが運営するセレクトショップです。美容医療の知見を活かし、成分コンセプトやブランドの品質面を重視しながら取り扱い商品を選定しています。なお、取り扱い商品の処方設計・製品開発は各韓国ブランドが行っており、医師が商品を開発・監修したものではありません。'
)
html = html.replace(
    '<strong>再生医療の知見を成分選定に活かす</strong>\n              エクソソーム・再生医療を専門とする医師の視点で、肌の自己修復力を高める成分を評価・選定しています。',
    '<strong>美容医療の知見を商品選定に活かす</strong>\n              美容医療を専門とする代表の知見を活かし、成分コンセプトやブランドの品質面を重視して取り扱い商品を選定しています。'
)
html = html.replace(
    '<strong>日本人の体質・肌質への適合性を確認</strong>\n              韓国製コスメが日本人の肌環境・気候条件に合うかを医学的見地からひとつずつ確認しています。',
    '<strong>成分・ブランドコンセプトを重視した選定</strong>\n              グルタチオン・PDRN・RG3など機能性成分を配合し、ブランドコンセプトと品質管理体制が明確な韓国ブランドをLUMINOVEは選定しています。'
)
html = html.replace(
    '<strong>取り扱い製品の成分を院長が確認・推薦</strong>\n              洗顔・スキンケア・ヘアケア・ハンドケアまで、すべての取り扱い製品の成分を院長が確認し、安全性・適合性を認めたものだけをご提案しています。',
    '<strong>韓国ブランドが製造、LUMINOVEが選定して販売</strong>\n              取り扱い商品はすべて韓国の各ブランドが独自に製造しています。LUMINOVEは商品の処方設計・製品開発は行わず、品質面を重視したセレクトショップとして販売しています。'
)

# ============================================================
# 【1-i】ブランドセクション「医師が成分を確認し」
# ============================================================
html = html.replace(
    '医師が成分を確認し、セレクトした韓国コスメブランドをご紹介します。',
    '美容医療の知見を持つ代表が品質面を重視してセレクトした韓国コスメブランドをご紹介します。'
)

# ============================================================
# 【1-j】Brand Story セクション
# ============================================================
html = html.replace(
    '六本木美容医療クリニック（BMC）院長と立ち上げたこのセレクトショップは、一つのブランドを推すのではなく、「成分で選ぶ」という軸で韓国コスメを厳選しています。',
    '六本木美容医療クリニック（BMC）院長・大久保義徳が代表を務めるこのセレクトショップは、一つのブランドを推すのではなく、「成分で選ぶ」という軸で韓国コスメを選定しています。'
)
html = html.replace(
    '流行を追うのではなく、成分の根拠を確認し、日本人の肌に本当に合うものだけをお届けするのがLUMINOVEの役割です。',
    '流行を追うのではなく、成分コンセプトと品質管理体制を確認し、日本人の肌に届けたいものだけを選定するのがLUMINOVEの役割です。'
)

# stat labels
html = html.replace(
    '<div class="stat-label">院長確認済み製品数</div>',
    '<div class="stat-label">取扱製品数</div>'
)
html = html.replace(
    '<div class="stat-label">六本木BMC院長推薦</div>',
    '<div class="stat-label">六本木BMC院長が選定に関与</div>'
)

# ============================================================
# 【1-k】フッター・ナビ
# ============================================================
html = html.replace(
    '光と愛を纏う肌へ。六本木の美容医師が成分を確認・推薦する、医師推薦の韓国コスメセレクトショップ。',
    '光と愛を纏う肌へ。六本木BMC院長が代表を務め、品質面を重視して商品選定に携わる韓国コスメセレクトショップ。'
)
html = html.replace(
    '<li><a href="#supervisor">院長推薦・成分確認について</a></li>',
    '<li><a href="#supervisor">LUMINOVEの商品選定について</a></li>'
)
# Brand story h2
html = html.replace(
    '<h2 class="section-title brand-story-title">医師の目線で選ぶ、<br>韓国スキンケアの新基準</h2>',
    '<h2 class="section-title brand-story-title">成分コンセプトで選ぶ、<br>韓国スキンケアの新基準</h2>'
)

# ============================================================
# 【2】レビュー重複（ループ用コピー）削除
# ループ用コピーを削除し、CSSアニメーションを無効化して
# 代わりにグリッド表示に変更
# ============================================================

# ループ用コピーブロックを削除
loop_start = '        <!-- ループ用コピー -->\n        <div class="review-card">'
loop_end = '      </div>\n    </div>\n  </section>\n\n  <!-- STORES -->'

idx_start = html.find(loop_start)
idx_end   = html.find(loop_end)
if idx_start != -1 and idx_end != -1:
    html = html[:idx_start] + '      </div>\n    </div>\n  </section>\n\n  <!-- STORES -->' + html[idx_end + len(loop_end):]
    print('ループ用コピー削除: OK')
else:
    print('ループ用コピー: パターン不一致、手動確認要')

# reviews-track を grid に変更
html = html.replace(
    '.reviews-track {\n      display: flex;\n      animation: scroll 120s linear infinite;',
    '.reviews-track {\n      display: grid;\n      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));'
)
html = html.replace(
    '.reviews-track:hover { animation-play-state: paused; }',
    ''
)
html = html.replace(
    "@keyframes scroll {\n      from { transform: translateX(0); }\n      to { transform: translateX(-50%); }\n    }",
    ''
)

# ============================================================
# 【4】内部リンク強化：成分セクションに詳細ページリンク追加
# ============================================================
# 成分カードにリンクを追加
html = html.replace(
    '<h3 class="ingr-name">グルタチオン</h3>\n        <p class="ingr-text">「美白の王様」とも呼ばれる最強の抗酸化成分。メラニン生成を抑制し、透明感あふれる明るい肌へ導く。セラムには30,000ppmの高濃度配合。</p>',
    '<h3 class="ingr-name">グルタチオン</h3>\n        <p class="ingr-text">「美白の王様」とも呼ばれる最強の抗酸化成分。メラニン生成を抑制し、透明感あふれる明るい肌へ導く。セラムには30,000ppmの高濃度配合。</p>\n        <a href="/ingredients/glutathione.html" style="font-size:.78rem;color:var(--green-mid);letter-spacing:.05em;">詳しく見る →</a>'
)
html = html.replace(
    '<h3 class="ingr-name">300Da ナノコラーゲン</h3>\n        <p class="ingr-text">分子量300Daまで極限まで小さくしたナノサイズのコラーゲン。角層の奥まで浸透し、ふっくらとしたハリ感と深いうるおいをもたらす。</p>',
    '<h3 class="ingr-name">300Da ナノコラーゲン</h3>\n        <p class="ingr-text">分子量300Daまで極限まで小さくしたナノサイズのコラーゲン。角層の奥まで浸透し、ふっくらとしたハリ感と深いうるおいをもたらす。</p>\n        <a href="/ingredients/glutathione.html" style="font-size:.78rem;color:var(--green-mid);letter-spacing:.05em;">詳しく見る →</a>'
)

# SUPERVISORセクションにdoctor/リンクを追加（既存ボタンがあれば追加不要）
if '/doctor/' not in html[html.find('id="supervisor"'):html.find('id="supervisor"')+2000]:
    html = html.replace(
        '</div>\n      </div>\n    </div>\n  </section>\n\n  <!-- PRODUCTS -->',
        '        <a href="/doctor/" class="btn-outline" style="margin-top:1.5rem;display:inline-block">LUMINOVEの商品選定について →</a>\n      </div>\n    </div>\n  </section>\n\n  <!-- PRODUCTS -->'
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html 更新完了')

# 変更箇所の数を確認
changed = sum(1 for a, b in zip(original.splitlines(), html.splitlines()) if a != b)
print(f'変更行数: {changed}行')
