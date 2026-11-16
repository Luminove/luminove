/**
 * ブログ → Instagram の導線（記事末のカード・ブログ一覧の帯・ヘッダーのInstagramアイコンのPC表示）を生成・更新するスクリプト
 *
 * 使い方:
 *   node data/build-ig-follow.js                 … 差分を表示するだけ（安全確認用）
 *   node data/build-ig-follow.js --write         … 実際にブログの記事と一覧へ反映
 *   node data/build-ig-follow.js --only <slug>   … その記事（blog/<slug>.html）と一覧ページだけを対象にする（--write・--check と併用可）
 *                                                   slug は英小文字・数字・ハイフンだけ（.html は付けない。index は不可）。違えば終了コード2
 *   node data/build-ig-follow.js --check         … 調べるだけ。問題があれば終了コード1。見るのは次のとおり
 *                                                   ・記事の data-slug とファイル名の食い違い、ブロックの重複
 *                                                   ・投稿があるのに cover.webp がない
 *                                                   ・HTML が ig-posts.json と合っていない（未反映の記事、新しい投稿の未反映、一覧の帯の位置のずれ）
 *                                                   ・導線が使う画像（cover.webp など）が git に登録されていない（git add の後に実行する）
 *   node data/build-ig-follow.js --diff          … 差分表示のとき、変わる部分の中身も表示する
 *   ※ --write と差分表示は、飛ばした記事が1件でもあれば終了コード1を返す
 *
 * データ（data/ig-posts.json）の更新は、LUMINOVE_Instagram フォルダ（post_to_instagram.py と同じ場所）の
 * sync_ig_posts.py で行う（取得 → ig-posts.json → 足りない cover.webp を作成）。その後にこのスクリプトを --write
 *
 * 仕様:
 *   - data/ig-posts.json の投稿のうち、article（= blog/<slug>.html）があり、カルーセル（CAROUSEL_ALBUM）で
 *     show が false でないものを「その記事のまとめ投稿」とする（同じ記事に複数あれば新しいほう）
 *   - 記事末のカード: 投稿がある記事は「その投稿へ」＋「プロフィールへ」、ない記事は「プロフィールへ」だけ
 *     表紙は ig/<slug>/cover.webp（360×450）。ファイルがなければ表紙なしの文字だけのカードにする
 *     投稿がない記事の左のアイコンは images/ig-avatar.webp（160×160。apple-touch-icon.png の縮小版）。なければ apple-touch-icon.png
 *   - カードの位置: 商品CTA（<!-- CTA:END -->）があればその直後、なければ <section class="related-section"> の直前。
 *     どちらもない記事は警告して飛ばす
 *   - ブログ一覧（blog/index.html）の帯: 6枚目の記事カードのすぐ後に、横幅いっぱいで入れる。
 *     最近のまとめ投稿（表紙があるもの）3件の表紙と、プロフィールへのボタン
 *   - マーカー: <!-- IGFOLLOW:START --> 〜 <!-- IGFOLLOW:END -->（カード・帯）、/* IGFOLLOW:CSS:START *\/ 〜 /* IGFOLLOW:CSS:END *\/（CSS）
 *     すでにあれば中身だけ差し替える（重複追加しない）。一覧の帯は、6枚目の後からずれていれば位置も直す
 *   - CSS は各ページの <head> の <style> の最後に入れる（ヘッダーのInstagramアイコンをPCでも表示する指定もここに含む。
 *     幅769〜1159pxではメニューが詰まって折り返すため出さない。768px以下は既存の指定で表示）
 *   - CRLF のファイルは CRLF のまま書く
 *   - Instagram公式の埋め込み・外部スクリプト・計測用スクリプトは入れない。位置ごとの計測はクラス名で分ける
 *     （ig-cta-end-post／ig-cta-end-profile／ig-cta-index-band。GA4の拡張計測の外部リンククリックで見られる）
 */
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const BLOG = path.join(ROOT, "blog");
const DATA = path.join(__dirname, "ig-posts.json");

const args = process.argv.slice(2);
const WRITE = args.includes("--write");
const CHECK = args.includes("--check");
const SHOW_DIFF = args.includes("--diff");
const onlyIdx = args.indexOf("--only");
const ONLY = onlyIdx >= 0 ? args[onlyIdx + 1] : null;
if (onlyIdx >= 0 && (!ONLY || ONLY.startsWith("--"))) { console.error("--only のあとに記事の slug を指定してください"); process.exit(2); }
if (ONLY && (!/^[a-z0-9-]+$/.test(ONLY) || ONLY === "index")) {
  console.error(`--only には記事の slug を指定してください（英小文字・数字・ハイフンだけ。.html は付けない。index は不可）: ${ONLY}`);
  process.exit(2);
}

const START = "<!-- IGFOLLOW:START -->";
const END = "<!-- IGFOLLOW:END -->";
const CSS_START = "/* IGFOLLOW:CSS:START */";
const CSS_END = "/* IGFOLLOW:CSS:END */";
const INDEX_AFTER_N = 6; // 一覧の帯を入れる位置（何枚目のカードの後か）
const BAND_POSTS = 3;    // 一覧の帯に並べる表紙の数

const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const data = JSON.parse(fs.readFileSync(DATA, "utf8"));
const PROFILE = data.account && data.account.profile_url;
if (!PROFILE || !/^https:\/\/www\.instagram\.com\/[A-Za-z0-9._]+\/$/.test(PROFILE)) { console.error("ig-posts.json の account.profile_url が不正です"); process.exit(2); }

// 記事ごとのまとめ投稿（カルーセル・表示可・記事あり）。同じ記事に複数あれば新しいほう
const isPostLink = u => typeof u === "string" && /^https:\/\/www\.instagram\.com\/p\/[A-Za-z0-9_-]+\/$/.test(u);
const usable = (data.posts || [])
  .filter(p => p.article && p.show !== false && p.media_type === "CAROUSEL_ALBUM" && isPostLink(p.permalink))
  .sort((a, b) => String(b.posted_at).localeCompare(String(a.posted_at)));
const postByArticle = new Map();
for (const p of usable) if (!postByArticle.has(p.article)) postByArticle.set(p.article, p);

// 投稿予定の予告（data.upcoming: [{article, publish_at:"YYYY-MM-DD", label:"11月24日（火）", what:"この記事の7つのチェック"}]）
// まだ投稿がなく、予定日が今日以降の記事だけ「予告」のカードにする。予定日を過ぎたら通常の「投稿なし」カードに戻る
const pad2 = n => String(n).padStart(2, "0");
const _now = new Date();
const TODAY = `${_now.getFullYear()}-${pad2(_now.getMonth() + 1)}-${pad2(_now.getDate())}`;
const upcomingByArticle = new Map();
for (const u of (data.upcoming || [])) {
  if (u && /^[a-z0-9-]+$/.test(u.article || "") && /^\d{4}-\d{2}-\d{2}$/.test(u.publish_at || "") && u.label && u.publish_at >= TODAY)
    upcomingByArticle.set(u.article, u);
}

const coverFile = p => (p.cover && /^\/ig\/[a-z0-9-]+\/cover\.webp$/.test(p.cover)) ? path.join(ROOT, p.cover.replace(/^\//, "")) : null;
const hasCover = p => { const f = coverFile(p); return !!(f && fs.existsSync(f)); };

// 投稿がない記事のカードに出すアイコン（表示は64〜80px。2倍密度用に160pxの webp を使う）
const AVATAR = fs.existsSync(path.join(ROOT, "images", "ig-avatar.webp"))
  ? { src: "/images/ig-avatar.webp", size: 160 }
  : { src: "/apple-touch-icon.png", size: 180 };

// ---------------------------------------------------------------- 部品
const IG_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"></rect><circle cx="12" cy="12" r="4"></circle><circle cx="17.3" cy="6.7" r="0.9" fill="currentColor" stroke="none"></circle></svg>';
const EXT = '<span aria-hidden="true">↗</span>';
const NOTE = '<p class="ig-small">Instagram（アプリまたはWebサイト）が開きます。</p>';
const LINK = 'target="_blank" rel="noopener"';

// 記事末のカード（1行目のインデントは呼び出し側の行頭に任せる）
function buildCard(slug, p) {
  if (p) {
    const n = Number.isInteger(p.slide_count) && p.slide_count > 0 ? p.slide_count : null;
    const cover = hasCover(p);
    const alt = p.cover_title || "Instagramのまとめ投稿の表紙";
    return [
      START,
      `  <aside class="ig-card${cover ? "" : " ig-card--text"}" aria-labelledby="ig-card-title" data-slug="${esc(slug)}">`,
      `    <div class="ig-card-inner">`,
      ...(cover ? [
        `      <a class="ig-card-media ig-cta-end-post" href="${esc(p.permalink)}" ${LINK}>`,
        `        <img src="${esc(p.cover)}" width="360" height="450" alt="${esc(alt)}" loading="lazy" decoding="async" />`,
        `      </a>`,
      ] : []),
      `      <div class="ig-card-head">`,
      `        <p class="ig-label">${IG_SVG}Instagram</p>`,
      `        <h2 class="ig-card-title" id="ig-card-title">この記事の要点は、<wbr>Instagramでも</h2>`,
      `      </div>`,
      `      <p class="ig-card-desc">スライド${n ? n + "枚" : "数枚"}にまとめています。保存しておくと、あとで見返せます。フォローすると、新しいまとめがフィードに届きます。</p>`,
      `      <div class="ig-card-actions">`,
      `        <a class="ig-btn ig-btn-primary ig-cta-end-post" href="${esc(p.permalink)}" ${LINK}>${n ? n + "枚の" : ""}まとめを見る ${EXT}</a>`,
      `        <a class="ig-btn ig-btn-sub ig-cta-end-profile" href="${esc(PROFILE)}" ${LINK}>プロフィールを見る ${EXT}</a>`,
      `      </div>`,
      `      ${NOTE}`,
      `    </div>`,
      `  </aside>`,
      `  ${END}`,
    ].join("\n");
  }
  return [
    START,
    `  <aside class="ig-card ig-card--profile" aria-labelledby="ig-card-title" data-slug="${esc(slug)}">`,
    `    <div class="ig-card-inner">`,
    `      <a class="ig-card-media ig-card-avatar ig-cta-end-profile" href="${esc(PROFILE)}" ${LINK} tabindex="-1" aria-hidden="true">`,
    `        <img src="${AVATAR.src}" width="${AVATAR.size}" height="${AVATAR.size}" alt="" loading="lazy" decoding="async" />`,
    `      </a>`,
    `      <div class="ig-card-head">`,
    `        <p class="ig-label">${IG_SVG}Instagram</p>`,
    ...(upcomingByArticle.has(slug) ? [
      `        <h2 class="ig-card-title" id="ig-card-title">この記事の要点は、<wbr>Instagramでもお届けします</h2>`,
      `      </div>`,
      `      <p class="ig-card-desc">${esc(upcomingByArticle.get(slug).label)}に、${esc(upcomingByArticle.get(slug).what || "この記事の要点")}をスライドにまとめてInstagramに投稿します。フォローしておくと、投稿がフィードに届きます。</p>`,
    ] : [
      `        <h2 class="ig-card-title" id="ig-card-title">スキンケアの要点を、<wbr>Instagramでも</h2>`,
      `      </div>`,
      `      <p class="ig-card-desc">ブログで取り上げた成分やスキンケアの話を、スライド数枚にまとめて投稿しています。保存しておくと、あとで見返せます。フォローすると、新しいまとめがフィードに届きます。</p>`,
    ]),
    `      <div class="ig-card-actions">`,
    `        <a class="ig-btn ig-btn-primary ig-cta-end-profile" href="${esc(PROFILE)}" ${LINK}>Instagramで見る ${EXT}</a>`,
    `      </div>`,
    `      ${NOTE}`,
    `    </div>`,
    `  </aside>`,
    `  ${END}`,
  ].join("\n");
}

// 一覧の帯（1行目のインデントは呼び出し側の行頭に任せる）
function buildBand(posts) {
  const items = posts.map(p =>
    `        <li><a class="ig-cta-index-band" href="${esc(p.permalink)}" ${LINK}><img src="${esc(p.cover)}" width="360" height="450" alt="${esc(p.cover_title || "Instagramのまとめ投稿の表紙")}" loading="lazy" decoding="async" /></a></li>`);
  return [
    START,
    `    <section class="ig-band${items.length ? "" : " ig-band--text"}" aria-labelledby="ig-band-title">`,
    `      <div class="ig-band-head">`,
    `        <p class="ig-label">${IG_SVG}Instagram</p>`,
    `        <h2 id="ig-band-title">記事の要点を、<wbr>Instagramでも</h2>`,
    `        <p class="ig-band-desc">ブログの記事を、スライド数枚にまとめて投稿しています。${items.length ? "最近のまとめはこちらです。" : ""}フォローすると、新しいまとめがフィードに届きます。</p>`,
    `      </div>`,
    ...(items.length ? [
      `      <ul class="ig-band-list" aria-label="最近のまとめ投稿">`,
      ...items,
      `      </ul>`,
    ] : []),
    `      <div class="ig-band-actions">`,
    `        <a class="ig-btn ig-btn-primary ig-cta-index-band" href="${esc(PROFILE)}" ${LINK}>Instagramで見る ${EXT}</a>`,
    `        ${NOTE}`,
    `      </div>`,
    `    </section>`,
    `    ${END}`,
  ].join("\n");
}

// ---------------------------------------------------------------- CSS（各行は4スペースで字下げして入れる）
const CSS_COMMON = `
/* Instagram導線（data/build-ig-follow.js が管理。直すときはスクリプト側を直して --write） */
.mobile-instagram-link { transition: color var(--transition); }
.mobile-instagram-link:hover { color: var(--green-mid); }
@media (min-width: 1160px) { .mobile-instagram-link { display: inline-flex; } }
.ig-label { display: flex; align-items: center; gap: .4rem; font-size: .72rem; letter-spacing: .15em; font-weight: 600; color: var(--green-mid); margin-bottom: .35rem; line-height: 1.6; }
.ig-label svg { width: 15px; height: 15px; flex-shrink: 0; }
.ig-btn { display: inline-flex; align-items: center; justify-content: center; gap: .45rem; min-height: 44px; padding: .55rem 1.3rem; border-radius: 50px; font-size: .82rem; font-weight: 500; letter-spacing: .04em; line-height: 1.45; text-align: center; white-space: nowrap; transition: background var(--transition), transform var(--transition); }
.ig-btn-primary { background: var(--green-deep); color: #fff; }
.ig-btn-primary:hover { background: var(--green-mid); transform: translateY(-2px); }
.ig-btn-sub { background: #fff; color: var(--green-deep); border: 1px solid var(--green-light); }
.ig-btn-sub:hover { background: var(--green-mist); transform: translateY(-2px); }
.ig-small { font-size: .72rem; color: var(--text-light); line-height: 1.6; text-wrap: balance; line-break: strict; }`;

const CSS_ARTICLE = CSS_COMMON + `
.ig-card { max-width: 720px; margin: 0 auto 3rem; padding: 0 5%; }
.ig-card-inner { display: grid; grid-template-columns: 140px minmax(0,1fr); grid-template-rows: auto auto auto 1fr; grid-template-areas: "media head" "media desc" "media actions" "media note"; column-gap: 1.5rem; align-items: start; background: var(--warm-white); border: 1px solid var(--green-pale); border-radius: var(--radius); padding: 1.5rem; }
.ig-card-media { grid-area: media; display: block; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 18px rgba(45,74,62,.12); transition: transform var(--transition); }
.ig-card-media:hover { transform: translateY(-2px); }
.ig-card-media img { height: auto; aspect-ratio: 4 / 5; object-fit: cover; }
.ig-card-head { grid-area: head; }
.ig-card-title { font-family: var(--font-serif); font-size: 1.3rem; font-weight: 500; line-height: 1.5; color: var(--green-deep); word-break: keep-all; overflow-wrap: anywhere; }
.ig-card-desc { grid-area: desc; margin-top: .4rem; font-size: .85rem; color: var(--text-mid); line-height: 1.85; text-wrap: pretty; line-break: strict; }
@media (min-width: 561px) { .ig-card-desc { word-break: auto-phrase; } }
.ig-card-actions { grid-area: actions; display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1rem; }
.ig-card .ig-small { grid-area: note; margin-top: .7rem; }
.ig-card--profile .ig-card-inner { grid-template-columns: 80px minmax(0,1fr); }
.ig-card-avatar { width: 80px; height: 80px; border-radius: 50%; border: 1px solid var(--green-pale); box-shadow: none; }
.ig-card-avatar img { width: 100%; height: 100%; aspect-ratio: 1; }
.ig-card--text .ig-card-inner { grid-template-columns: minmax(0,1fr); grid-template-areas: "head" "desc" "actions" "note"; }
@media (max-width: 560px) {
  .ig-card-inner { grid-template-columns: 96px minmax(0,1fr); grid-template-rows: none; grid-template-areas: "head head" "media desc" "actions actions" "note note"; column-gap: 1rem; padding: 1.2rem 1.1rem; }
  .ig-card-head { margin-bottom: .8rem; }
  .ig-card-title { font-size: 1.12rem; }
  .ig-card-desc { margin-top: 0; align-self: center; font-size: .82rem; line-height: 1.8; text-wrap: balance; }
  .ig-card-actions { flex-direction: column; }
  .ig-card-actions .ig-btn { width: 100%; }
  .ig-card--profile .ig-card-inner { grid-template-columns: 64px minmax(0,1fr); }
  .ig-card-avatar { width: 64px; height: 64px; align-self: start; }
  .ig-card--text .ig-card-inner { grid-template-columns: minmax(0,1fr); grid-template-areas: "head" "desc" "actions" "note"; }
}`;

const CSS_INDEX = CSS_COMMON + `
.ig-band { grid-column: 1 / -1; display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1.3fr); grid-template-areas: "head list" "actions list"; column-gap: 2.4rem; row-gap: 1.2rem; align-items: center; background: var(--green-mist); border-radius: var(--radius); padding: 2rem 2.2rem; margin: .6rem 0; }
.ig-band--text { grid-template-columns: minmax(0,1fr); grid-template-areas: "head" "actions"; }
.ig-band-head { grid-area: head; align-self: end; }
.ig-band-head h2 { font-family: var(--font-serif); font-size: 1.45rem; font-weight: 500; line-height: 1.5; color: var(--green-deep); margin-bottom: .5rem; word-break: keep-all; overflow-wrap: anywhere; }
.ig-band-desc { font-size: .85rem; color: var(--text-mid); line-height: 1.85; text-wrap: pretty; line-break: strict; word-break: auto-phrase; }
.ig-band-list { grid-area: list; list-style: none; display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: .8rem; }
.ig-band-list a { display: block; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 18px rgba(45,74,62,.12); transition: transform var(--transition); }
.ig-band-list a:hover { transform: translateY(-3px); }
.ig-band-list img { height: auto; aspect-ratio: 4 / 5; object-fit: cover; }
.ig-band-actions { grid-area: actions; align-self: start; }
.ig-band-actions .ig-small { margin-top: .5rem; }
@media (max-width: 768px) {
  .ig-band { grid-template-columns: minmax(0,1fr); grid-template-areas: "head" "list" "actions"; padding: 1.5rem 1.2rem; row-gap: 1rem; }
  .ig-band--text { grid-template-areas: "head" "actions"; }
  .ig-band-head h2 { font-size: 1.2rem; }
  .ig-band-list { gap: .5rem; }
}
@media (max-width: 560px) {
  .ig-band-actions .ig-btn { width: 100%; }
}`;

function cssBlock(css, eol) {
  const lines = [CSS_START, ...css.replace(/^\n/, "").split("\n"), CSS_END];
  return lines.map(l => "    " + l).join(eol) + eol;
}

// ---------------------------------------------------------------- 差し込み
const toEol = (s, eol) => s.replace(/\r?\n/g, eol);
const lineStart = (html, i) => html.lastIndexOf("\n", i - 1) + 1;

function upsertCss(html, css, eol) {
  const block = cssBlock(css, eol);
  const re = new RegExp("[ \\t]*" + reEsc(CSS_START) + "[\\s\\S]*?" + reEsc(CSS_END) + "[ \\t]*\\r?\\n");
  if (re.test(html)) return { html: html.replace(re, () => block), op: "CSS" };
  const head = html.indexOf("</head>");
  const close = html.lastIndexOf("</style>", head < 0 ? html.length : head);
  if (close < 0) return { html, op: "CSS", warn: "<head> の </style> が見つかりません" };
  const at = lineStart(html, close);
  // </style> が行の途中にある（同じ行に CSS がある）場合は、その直前に改行を挟んで入れる
  const prefix = html.slice(at, close).trim() ? eol : "";
  const insertAt = prefix ? close : at;
  return { html: html.slice(0, insertAt) + prefix + block + html.slice(insertAt), op: "CSS" };
}

function upsertCard(html, slug, eol) {
  const block = toEol(buildCard(slug, postByArticle.get(slug)), eol);
  const re = new RegExp(reEsc(START) + "[\\s\\S]*?" + reEsc(END));
  // 置き場所は「よくある質問」のすぐ上（2026-11-16 池田さんの希望）。よくある質問がない記事は従来どおり
  const FAQ_TAG = '<section class="faq-section"';
  if (html.indexOf(FAQ_TAG) >= 0) {
    // 既存のブロックがあれば、前後の空行ごと取り除いてから入れ直す（同じ場所なら結果は変わらない）
    const m = re.exec(html);
    if (m) {
      const s = m.index, e = s + m[0].length, ls = lineStart(html, s), E2 = eol + eol;
      if (html.slice(e, e + E2.length) === E2) html = html.slice(0, ls) + html.slice(e + E2.length);
      else if (html.slice(ls - E2.length, ls) === E2) html = html.slice(0, ls - E2.length) + html.slice(e);
      else html = html.slice(0, ls) + html.slice(e);
    }
    const faq = html.indexOf(FAQ_TAG);
    const ls = lineStart(html, faq);
    const indent = html.slice(ls, faq);
    if (/^[ \t]*$/.test(indent)) return { html: html.slice(0, ls) + indent + block + eol + eol + html.slice(ls), where: "よくある質問の直前" };
    return { html: html.slice(0, faq) + block + eol + eol + indent.replace(/[^ \t]/g, " ") + html.slice(faq), where: "よくある質問の直前" };
  }
  if (re.test(html)) return { html: html.replace(re, () => block) };
  const cta = html.indexOf("<!-- CTA:END -->");
  if (cta >= 0) {
    const ls = lineStart(html, cta);
    const indent = html.slice(ls, cta).match(/^[ \t]*/)[0];
    const at = cta + "<!-- CTA:END -->".length;
    return { html: html.slice(0, at) + eol + eol + indent + block + html.slice(at), where: "商品CTAの直後" };
  }
  const rel = html.indexOf('<section class="related-section">');
  if (rel >= 0) {
    const ls = lineStart(html, rel);
    const indent = html.slice(ls, rel);
    if (/^[ \t]*$/.test(indent)) return { html: html.slice(0, ls) + indent + block + eol + eol + html.slice(ls), where: "関連記事の直前" };
    return { html: html.slice(0, rel) + block + eol + eol + indent.replace(/[^ \t]/g, " ") + html.slice(rel), where: "関連記事の直前" };
  }
  return { html, warn: "商品CTA（<!-- CTA:END -->）も <section class=\"related-section\"> も見つかりません" };
}

const CARD_RE = /[ \t]*<a href="\/blog\/[^"]+\.html" class="blog-card">[\s\S]*?<\/a>[ \t]*\r?\n/g;

function bandPosts() {
  const out = [];
  for (const p of usable) {
    if (out.length >= BAND_POSTS) break;
    if (out.some(o => o.article === p.article)) continue;
    if (hasCover(p) && fs.existsSync(path.join(BLOG, p.article + ".html"))) out.push(p);
  }
  return out;
}

function upsertBand(html, eol) {
  const block = toEol(buildBand(bandPosts()), eol);
  // いったん既存の帯を外してから、6枚目のカードの後に入れ直す（位置がずれていても直る。正しい位置なら結果は同じ）
  const re = new RegExp("[ \\t]*" + reEsc(START) + "[\\s\\S]*?" + reEsc(END) + "[ \\t]*\\r?\\n");
  const had = re.test(html);
  const base = had ? html.replace(re, "") : html;
  const grid = base.indexOf('<div class="blog-grid">');
  if (grid < 0) return { html, warn: '<div class="blog-grid"> が見つかりません', fatal: true };
  CARD_RE.lastIndex = grid;
  const cards = [];
  let m;
  while ((m = CARD_RE.exec(base)) && cards.length < INDEX_AFTER_N) cards.push(m);
  if (!cards.length) return { html, warn: "記事カードが見つかりません", fatal: true };
  const after = cards[cards.length - 1];
  const at = after.index + after[0].length;
  const indent = (after[0].match(/^[ \t]*/) || [""])[0];
  const next = base.slice(0, at) + indent + block + eol + base.slice(at);
  return { html: next, warn: cards.length < INDEX_AFTER_N ? `記事カードが${cards.length}枚しかないため、最後のカードの後に入れます` : null };
}

// ---------------------------------------------------------------- 実行
function articleFiles() {
  return fs.readdirSync(BLOG).filter(f => f.endsWith(".html") && f !== "index.html").sort();
}

// 行単位の差分（LCS）。変わったまとまりごとに { line, del, add } を返す
function lineDiff(a, b) {
  const A = a.split(/\r?\n/), B = b.split(/\r?\n/);
  let s = 0; while (s < A.length && s < B.length && A[s] === B[s]) s++;
  let e = 0; while (e < A.length - s && e < B.length - s && A[A.length - 1 - e] === B[B.length - 1 - e]) e++;
  const a2 = A.slice(s, A.length - e), b2 = B.slice(s, B.length - e);
  const n = a2.length, m = b2.length, W = m + 1;
  const L = new Int32Array((n + 1) * (m + 1));
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--)
    L[i * W + j] = a2[i] === b2[j] ? L[(i + 1) * W + j + 1] + 1 : Math.max(L[(i + 1) * W + j], L[i * W + j + 1]);
  const hunks = []; let cur = null, i = 0, j = 0;
  const flush = () => { if (cur) { hunks.push(cur); cur = null; } };
  while (i < n || j < m) {
    if (i < n && j < m && a2[i] === b2[j]) { flush(); i++; j++; }
    else if (j < m && (i >= n || L[i * W + j + 1] >= L[(i + 1) * W + j])) { (cur = cur || { line: s + i + 1, del: [], add: [] }).add.push(b2[j++]); }
    else { (cur = cur || { line: s + i + 1, del: [], add: [] }).del.push(a2[i++]); }
  }
  flush();
  return hunks;
}

function report(rel, before, after) {
  if (before === after) return false;
  const hunks = lineDiff(before, after);
  const del = hunks.reduce((t, h) => t + h.del.length, 0), add = hunks.reduce((t, h) => t + h.add.length, 0);
  console.log(`  ${WRITE ? "反映" : "変更予定"}  ${rel}  （${hunks.map(h => h.line + "行目").join("・")}　-${del}行 +${add}行）`);
  if (SHOW_DIFF) {
    for (const h of hunks) {
      console.log(`    @@ ${h.line}行目`);
      h.del.forEach(l => console.log("    - " + l));
      h.add.forEach(l => console.log("    + " + l));
    }
  }
  return true;
}

// ファイルごとの「今の中身」と「反映後の中身」を作る（書き込みはしない）
function planArticle(f) {
  const file = path.join(BLOG, f);
  const rel = "blog/" + f;
  if (!fs.existsSync(file)) return { rel, skip: "記事がありません" };
  const before = fs.readFileSync(file, "utf8");
  const eol = before.includes("\r\n") ? "\r\n" : "\n";
  const slug = f.replace(/\.html$/, "");
  const card = upsertCard(before, slug, eol);
  if (card.warn) return { rel, skip: card.warn };
  const css = upsertCss(card.html, CSS_ARTICLE, eol);
  if (css.warn) return { rel, skip: css.warn };
  return { file, rel, before, after: css.html };
}

function planIndex() {
  const file = path.join(BLOG, "index.html");
  const rel = "blog/index.html";
  if (!fs.existsSync(file)) return { rel, skip: "一覧ページがありません" };
  const before = fs.readFileSync(file, "utf8");
  const eol = before.includes("\r\n") ? "\r\n" : "\n";
  const band = upsertBand(before, eol);
  if (band.fatal) return { rel, skip: band.warn };
  const css = upsertCss(band.html, CSS_INDEX, eol);
  if (css.warn) return { rel, skip: css.warn };
  return { file, rel, before, after: css.html, warn: band.warn };
}

const targets = ONLY ? [ONLY + ".html"] : articleFiles();
const plans = [...targets.map(planArticle), planIndex()];

// 導線のブロックが使う画像（/ で始まるサイト内のパス）
function blockImages(html) {
  const out = [];
  const re = new RegExp(reEsc(START) + "[\\s\\S]*?" + reEsc(END), "g");
  for (const m of html.match(re) || []) for (const s of m.matchAll(/<img [^>]*src="(\/[^"]+)"/g)) out.push(s[1].slice(1));
  return out;
}

// git に登録されている（コミット済み、または git add 済み）ファイル。git が使えなければ null
function trackedFiles(paths) {
  if (!paths.length) return new Set();
  try {
    const out = execFileSync("git", ["-C", ROOT, "ls-files", "-z", "--", ...paths], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
    return new Set(out.split("\0").filter(Boolean));
  } catch (e) {
    return null;
  }
}

function runCheck() {
  const problems = [], notes = new Set();
  for (const f of targets) {
    const file = path.join(BLOG, f);
    if (!fs.existsSync(file)) continue; // 下の「反映の状態」で数える
    const html = fs.readFileSync(file, "utf8");
    const slug = f.replace(/\.html$/, "");
    const count = html.split(START).length - 1;
    if (count > 1) problems.push(`blog/${f}: 導線のブロックが${count}個あります`);
    const re = new RegExp(reEsc(START) + "[\\s\\S]*?" + reEsc(END), "g");
    for (const m of html.match(re) || []) {
      const ds = (m.match(/data-slug="([^"]*)"/) || [])[1];
      if (ds !== slug) problems.push(`blog/${f}: data-slug（${ds === undefined ? "なし" : ds}）とファイル名（${slug}）が食い違っています`);
    }
  }
  {
    const file = path.join(BLOG, "index.html");
    if (fs.existsSync(file)) {
      const count = fs.readFileSync(file, "utf8").split(START).length - 1;
      if (count > 1) problems.push(`blog/index.html: 導線のブロックが${count}個あります`);
    }
  }
  for (const p of usable) {
    if (ONLY && p.article !== ONLY) continue;
    if (!fs.existsSync(path.join(BLOG, p.article + ".html"))) continue;
    if (!hasCover(p)) problems.push(`投稿があるのに cover.webp がありません: ${p.article}（${p.cover || "cover 未設定"}）`);
  }
  // 反映の状態（ドライランで変更予定が出るものは、データと HTML がずれている）
  for (const p of plans) {
    if (p.skip) problems.push(`${p.rel}: ${p.skip}`);
    else if (p.before !== p.after) { problems.push(`${p.rel}: 未反映（--write で直ります）`); notes.add("※未反映＝HTML が ig-posts.json・このスクリプトの内容と合っていない（導線のない記事、新しい投稿の反映漏れ、一覧の帯の位置のずれなど）"); }
  }
  // 導線が使う画像が、ファイルとしてあり、git に登録されているか（登録し忘れると本番で画像が切れる）
  const imgs = [...new Set(plans.filter(p => !p.skip).flatMap(p => blockImages(p.after)))].sort();
  for (const rel of imgs) if (!fs.existsSync(path.join(ROOT, rel))) problems.push(`画像がありません: ${rel}`);
  const tracked = trackedFiles(imgs.filter(rel => fs.existsSync(path.join(ROOT, rel))));
  if (tracked === null) console.log("  （git で確かめられなかったため、画像が git に登録されているかは調べていません）");
  else for (const rel of imgs) if (fs.existsSync(path.join(ROOT, rel)) && !tracked.has(rel)) { problems.push(`git 未登録: ${rel}`); notes.add("※git 未登録＝導線が使う画像がコミットに入っていない（このままでは本番で画像が切れる）。git add してからもう一度 --check"); }

  if (problems.length) {
    problems.forEach(s => console.log("  ✗ " + s));
    notes.forEach(s => console.log("  " + s));
    console.log(`\n  問題 ${problems.length}件`);
    process.exit(1);
  }
  console.log(`  問題なし（対象 ${plans.length}ファイル・導線の画像 ${imgs.length}件）`);
}

if (CHECK) { runCheck(); process.exit(0); }

let changed = 0, same = 0, skipped = 0;
for (const p of plans) {
  if (p.skip) { console.log(`  ⚠ ${p.rel}: ${p.skip}（飛ばします）`); skipped++; continue; }
  if (p.warn) console.log(`  ⚠ ${p.rel}: ${p.warn}`);
  if (report(p.rel, p.before, p.after)) {
    changed++;
    if (WRITE) fs.writeFileSync(p.file, p.after);
  } else same++;
}

const withPost = targets.filter(f => postByArticle.has(f.replace(/\.html$/, ""))).length;
console.log(`\n  ${WRITE ? "反映" : "変更予定"} ${changed} / 変更なし ${same} / 飛ばした ${skipped}`);
console.log(`  対象の記事 ${targets.length}件（まとめ投稿あり ${withPost}件・なし ${targets.length - withPost}件）／一覧の帯の表紙: ${bandPosts().map(p => p.article).join(", ") || "なし"}`);
if (!WRITE) console.log("\n  ※ドライラン。実際に反映するには --write を付けて実行してください。");
if (skipped) { console.log(`\n  飛ばした対象が${skipped}件あります（終了コード1）`); process.exit(1); }
