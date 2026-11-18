// 会員ページの割引設定を、ログインコードを鍵にして暗号化し、members/lock.js を書き出す。
//
// 使い方:  node data/members-lock.mjs [設定ファイル]
//   設定ファイルの既定は data/members-campaigns.local.json 。
//   このファイルにはログインコードがそのまま入るので、.gitignore で除外してある。
//   リポジトリは公開なので、コードや割引率をこのスクリプトやほかの追跡ファイルに書かないこと。
//
// 設定ファイルの形:
//   {
//     "iterations": 150000,
//     "campaigns": [
//       { "code": "（コード）", "label": "メンバー割引（10%OFF）", "rate": 0.10,
//         "special": {}, "banner": "（注文ページ上部の案内。HTML可）",
//         "expires": "2026-08-31" }        // expires は期間限定のときだけ。この日まで有効
//     ]
//   }
//
// ページを見た人が読めるのは暗号文だけ。正しいコードを入れた端末でだけ、その割引設定が戻る。
// 短いコードは総当たりに弱いので、新しく決めるときは8文字以上がよい。

import { readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { isDeepStrictEqual } from 'node:util'
import path from 'node:path'

// ブラウザで動く部分。lock.js にはこの関数の中身がそのまま書き出される（古い端末でも動くよう ES5 で書く）。
function runtime(g, LOCK) {
  function normalize(code) {
    return String(code == null ? '' : code)
      .replace(/[Ａ-Ｚａ-ｚ０-９]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0xFEE0); })
      .replace(/　/g, ' ')
      .trim()
      .toUpperCase();
  }
  function bytes(s) {
    var b = atob(s), a = new Uint8Array(b.length);
    for (var i = 0; i < b.length; i++) a[i] = b.charCodeAt(i);
    return a;
  }
  function supported() {
    return !!(g.crypto && g.crypto.subtle && typeof TextEncoder !== 'undefined' && typeof TextDecoder !== 'undefined');
  }
  // 正しいコードならその割引設定（オブジェクト）、違えば null を返す Promise。
  function open(code) {
    code = normalize(code);
    if (!code || !LOCK || !supported()) return Promise.resolve(null);
    var subtle = g.crypto.subtle;
    return subtle.importKey('raw', new TextEncoder().encode(code), 'PBKDF2', false, ['deriveKey'])
      .then(function (base) {
        return subtle.deriveKey(
          { name: 'PBKDF2', salt: bytes(LOCK.salt), iterations: LOCK.iter, hash: 'SHA-256' },
          base, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      })
      .then(function (key) {
        var i = 0;
        function next() {
          if (i >= LOCK.items.length) return null;
          var it = LOCK.items[i++];
          return subtle.decrypt({ name: 'AES-GCM', iv: bytes(it.iv) }, key, bytes(it.ct))
            .then(function (buf) { return JSON.parse(new TextDecoder().decode(buf)); }, next);
        }
        return next();
      })
      .catch(function () { return null; });
  }
  g.LuminoveLock = { open: open, normalize: normalize, supported: supported };
}

const here = path.dirname(fileURLToPath(import.meta.url))
const src = process.argv[2] ? path.resolve(process.argv[2]) : path.join(here, 'members-campaigns.local.json')
const out = path.join(here, '..', 'members', 'lock.js')
const subtle = globalThis.crypto.subtle
const enc = new TextEncoder()
const b64 = u8 => Buffer.from(u8).toString('base64')

const probe = {}
runtime(probe, null)
const normalize = probe.LuminoveLock.normalize

const conf = JSON.parse(readFileSync(src, 'utf8'))
const iter = conf.iterations ?? 150000
if (!Array.isArray(conf.campaigns) || conf.campaigns.length === 0) throw new Error('campaigns が空です')

const salt = globalThis.crypto.getRandomValues(new Uint8Array(16))
const seen = new Set()
const items = []
const plains = []
let shortCodes = 0
for (const c of conf.campaigns) {
  const code = normalize(c.code)
  if (!code) throw new Error('コードが空の設定があります')
  if (seen.has(code)) throw new Error('同じコードが2回出てきます')
  seen.add(code)
  const { code: _drop, ...plain } = c
  plain.special = plain.special ?? {}
  if (typeof plain.rate !== 'number' || !(plain.rate >= 0 && plain.rate < 1)) throw new Error('rate は 0 以上 1 未満の数にしてください')
  if (!plain.label || !plain.banner) throw new Error('label と banner は必須です')
  if (plain.expires !== undefined && !/^\d{4}-\d{2}-\d{2}$/.test(plain.expires)) throw new Error('expires は YYYY-MM-DD で書いてください')
  if (code.length < 8) shortCodes++

  const base = await subtle.importKey('raw', enc.encode(code), 'PBKDF2', false, ['deriveKey'])
  const key = await subtle.deriveKey({ name: 'PBKDF2', salt, iterations: iter, hash: 'SHA-256' },
    base, { name: 'AES-GCM', length: 256 }, false, ['encrypt'])
  const iv = globalThis.crypto.getRandomValues(new Uint8Array(12))
  const ct = new Uint8Array(await subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(JSON.stringify(plain))))
  items.push({ iv: b64(iv), ct: b64(ct) })
  plains.push([code, plain])
}
// 並び順からどれがどのコードか推せないよう、順番を混ぜる
for (let i = items.length - 1; i > 0; i--) {
  const j = globalThis.crypto.getRandomValues(new Uint32Array(1))[0] % (i + 1);
  [items[i], items[j]] = [items[j], items[i]]
}

const lock = { v: 1, iter, salt: b64(salt), items }
const js = `/* 会員ページの割引設定（暗号化済み）。
   このファイルは data/members-lock.mjs が作ります。手で書き換えないでください。
   ログインコードを鍵にして暗号化してあり、正しいコードを入れた端末でだけ中身が戻ります。 */
(${runtime.toString()})(typeof window !== 'undefined' ? window : globalThis, ${JSON.stringify(lock)});
`
writeFileSync(out, js)

// 書き出したファイルを読み込んで、全部のコードで戻せるか・違うコードで戻らないかを確かめる
delete globalThis.LuminoveLock
await import(pathToFileURL(out).href + '?t=' + Date.now())
const L = globalThis.LuminoveLock
for (const [code, plain] of plains) {
  const got = await L.open(code.toLowerCase())
  if (!isDeepStrictEqual(got, plain)) throw new Error('書き出したファイルで戻せないコードがあります')
}
if (await L.open('NOT-A-REAL-CODE-' + b64(globalThis.crypto.getRandomValues(new Uint8Array(6)))) !== null) {
  throw new Error('違うコードで中身が戻ってしまいました')
}
if (shortCodes) console.warn(`注意: 8文字未満のコードが${shortCodes}件あります。新しく決めるときは8文字以上がおすすめです。`)
console.log(`members/lock.js を書き出しました（${items.length}件。全部のコードで戻ること、違うコードで戻らないことを確認済み）`)
