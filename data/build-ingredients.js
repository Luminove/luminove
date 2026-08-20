/**
 * 全成分セクションの生成・更新スクリプト
 *
 * 使い方:
 *   node data/build-ingredients.js          … 差分を表示するだけ（安全確認用）
 *   node data/build-ingredients.js --write  … 実際に商品ページへ反映
 *
 * 仕様:
 *   - data/ingredients.json の verified:true かつ ingredients が入っている商品だけを対象にする
 *   - 未確認（verified:false）の商品ページには何も追加しない（空欄の「準備中」を出さないため）
 *   - すでに全成分セクションがある場合は中身だけ差し替える（重複追加しない）
 *   - 挿入位置は「商品情報」セクションの直後
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const DATA = path.join(__dirname, "ingredients.json");
const WRITE = process.argv.includes("--write");

const START = "<!-- INGREDIENTS:START -->";
const END = "<!-- INGREDIENTS:END -->";

const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function buildSection(p) {
  return `${START}
    <section class="article-section" id="ingredients">
      <h2>全成分</h2>
      <p style="font-size:.82rem;color:var(--text-light);margin-bottom:.8rem">${esc(p.displayName)}${p.volume ? "（" + esc(p.volume) + "）" : ""}のパッケージ記載の全成分です。</p>
      <div class="table-scroll">
        <table class="spec-table">
          <tr><td style="font-size:.82rem;line-height:1.9">${esc(p.ingredients)}</td></tr>
        </table>
      </div>
      <p style="font-size:.78rem;color:var(--text-light)">※本表示はパッケージの記載に基づくものです。リニューアル等により変更となる場合がありますので、お手元の製品の表示もあわせてご確認ください。</p>
    </section>
    ${END}`;
}

const data = JSON.parse(fs.readFileSync(DATA, "utf8"));
const targets = data.products.filter(p => p.verified && p.ingredients && p.page);

let added = 0, updated = 0, skipped = 0, missing = 0;

targets.forEach(p => {
  const file = path.join(ROOT, p.page.replace(/^\//, ""));
  if (!fs.existsSync(file)) { console.log("  ページなし  " + p.page); missing++; return; }

  let html = fs.readFileSync(file, "utf8");
  const section = buildSection(p);

  if (html.includes(START)) {
    // 既存セクションを差し替え
    const re = new RegExp(START.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "[\\s\\S]*?" + END.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    const next = html.replace(re, section);
    if (next === html) { skipped++; return; }
    if (WRITE) fs.writeFileSync(file, next);
    console.log("  更新      " + p.page);
    updated++;
    return;
  }

  // 「商品情報」セクションの直後に挿入
  // ページによって見出しが「商品情報」「商品仕様」と揺れているため両対応
  const markers = ["<h2>商品情報</h2>", "<h2>商品仕様</h2>"];
  let mi = -1;
  for (const m of markers) { const i = html.indexOf(m); if (i >= 0) { mi = i; break; } }
  if (mi < 0) { console.log("  ⚠ 商品情報/商品仕様セクションが見つかりません  " + p.page); skipped++; return; }
  const endIdx = html.indexOf("</section>", mi);
  if (endIdx < 0) { console.log("  ⚠ セクション終端が見つかりません  " + p.page); skipped++; return; }
  const insertAt = endIdx + "</section>".length;

  const next = html.slice(0, insertAt) + "\n\n    " + section + html.slice(insertAt);
  if (WRITE) fs.writeFileSync(file, next);
  console.log("  追加      " + p.page);
  added++;
});

console.log("\n  追加 " + added + " / 更新 " + updated + " / スキップ " + skipped + " / ページなし " + missing);
console.log("  未確認のため対象外: " + data.products.filter(p => !p.verified).length + "件");
if (!WRITE) console.log("\n  ※ドライラン。実際に反映するには --write を付けて実行してください。");
