// 会員ページの割引設定を、ログインコードを鍵にして暗号化し、members/lock.js を書き出す。
//
// 使い方:  node data/members-lock.mjs [設定ファイル] [--allow-short] [--allow-leaked]
//   設定ファイルの既定は data/members-campaigns.local.json 。
//   このファイルにはログインコードがそのまま入るので、.gitignore と .vercelignore で除外してある。
//   リポジトリは公開なので、コードや割引率をこのスクリプトやほかの追跡ファイルに書かないこと。
//
// 設定ファイルの形（値は例。本物の値はここに書かない）:
//   {
//     "iterations": 150000,
//     "campaigns": [
//       { "code": "（コード）", "label": "（注文ページに出す割引名）", "rate": 0.05,
//         "special": {}, "banner": "（注文ページ上部の案内。HTML可）",
//         "expires": "2099-12-31" }        // expires は期間限定のときだけ。この日まで有効
//     ]
//   }
//
// ページを見た人が読めるのは暗号文だけ。正しいコードを入れた端末でだけ、その割引設定が戻る。
// lock.js は誰でも取れて何度でも試せるので、コードの長さが守りの強さになる。
// 次のコードは止める（どうしても使うときだけ、理由をわかったうえで指定する）:
//   - 10文字未満のコード（--allow-short で通す）
//   - このリポジトリの履歴か、追跡しているファイルに出てくるコード（--allow-leaked で通す）
//     リポジトリは公開なので、一度でもコミットされたコードは誰でも読める。

import { readFileSync, writeFileSync, unlinkSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { isDeepStrictEqual } from 'node:util'
import { tmpdir } from 'node:os'
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
    var s = g.crypto && g.crypto.subtle;
    return !!(s && typeof s.importKey === 'function' && typeof s.deriveKey === 'function' &&
      typeof s.decrypt === 'function' && typeof TextEncoder !== 'undefined' &&
      typeof TextDecoder !== 'undefined' && typeof atob === 'function');
  }
  // 正しいコードならその割引設定（オブジェクト）、違うコードなら null で終わる Promise。
  // コード違い以外の失敗（暗号の処理そのものが動かない等）は reject にして、呼ぶ側で別の案内を出す。
  function open(code) {
    code = normalize(code);
    if (!code || !LOCK) return Promise.resolve(null);
    return new Promise(function (resolve) {
      var subtle = g.crypto.subtle;
      resolve(subtle.importKey('raw', new TextEncoder().encode(code), 'PBKDF2', false, ['deriveKey'])
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
        }));
    });
  }
  g.LuminoveLock = { open: open, normalize: normalize, supported: supported };
}

const args = process.argv.slice(2)
const allowShort = args.includes('--allow-short')
const allowLeaked = args.includes('--allow-leaked')
const fileArg = args.find(a => !a.startsWith('--'))

const here = path.dirname(fileURLToPath(import.meta.url))
const root = path.join(here, '..')
const src = fileArg ? path.resolve(fileArg) : path.join(here, 'members-campaigns.local.json')
const out = path.join(root, 'members', 'lock.js')
const subtle = globalThis.crypto.subtle
const enc = new TextEncoder()
const b64 = u8 => Buffer.from(u8).toString('base64')
const MIN_ITER = 150000
const MIN_LEN = 10

// コードがこのリポジトリの履歴か追跡ファイルに出てくるか（コードは画面に出さない）
function leaked(code) {
  const git = (...a) => execFileSync('git', a, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim()
  if (git('log', '--all', '--format=%h', '-S', code)) return true
  try { return git('grep', '-I', '-l', '-F', '-i', '-e', code) !== '' } catch { return false } // 見つからないと git grep は 1 で終わる
}

const probe = {}
runtime(probe, null)
const normalize = probe.LuminoveLock.normalize

const conf = JSON.parse(readFileSync(src, 'utf8'))
const iter = conf.iterations ?? MIN_ITER
if (!Number.isInteger(iter) || iter < MIN_ITER) throw new Error(`iterations は ${MIN_ITER} 以上にしてください`)
if (!Array.isArray(conf.campaigns) || conf.campaigns.length === 0) throw new Error('campaigns が空です')

const salt = globalThis.crypto.getRandomValues(new Uint8Array(16))
const seen = new Set()
const items = []
const plains = []
let n = 0
for (const c of conf.campaigns) {
  n++
  const code = normalize(c.code)
  if (!code) throw new Error(`${n}件目: コードが空です`)
  if (seen.has(code)) throw new Error(`${n}件目: 同じコードが前にも出てきます`)
  seen.add(code)
  if (code.length < MIN_LEN && !allowShort) throw new Error(`${n}件目: コードが${MIN_LEN}文字未満です（総当たりに弱い）。どうしても使うときは --allow-short`)
  if (!allowLeaked && leaked(code)) throw new Error(`${n}件目: このコードは公開リポジトリの履歴か追跡ファイルに出てきます。新しいコードにしてください（どうしても使うときは --allow-leaked）`)
  const { code: _drop, ...plain } = c
  plain.special = plain.special ?? {}
  if (typeof plain.rate !== 'number' || !(plain.rate >= 0 && plain.rate < 1)) throw new Error(`${n}件目: rate は 0 以上 1 未満の数にしてください`)
  if (!plain.label || !plain.banner) throw new Error(`${n}件目: label と banner は必須です`)
  if (plain.expires !== undefined && !/^\d{4}-\d{2}-\d{2}$/.test(plain.expires)) throw new Error(`${n}件目: expires は YYYY-MM-DD で書いてください`)

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

// まず一時ファイルに書いて確かめ、通ったときだけ members/lock.js を置き換える
const tmp = path.join(tmpdir(), `luminove-lock-${process.pid}-${b64(globalThis.crypto.getRandomValues(new Uint8Array(6))).replace(/[^A-Za-z0-9]/g, '')}.js`)
writeFileSync(tmp, js)
try {
  delete globalThis.LuminoveLock
  await import(pathToFileURL(tmp).href)
  const L = globalThis.LuminoveLock
  for (const [code, plain] of plains) {
    const got = await L.open(code.toLowerCase())
    if (!isDeepStrictEqual(got, plain)) throw new Error('作った暗号で戻せないコードがあります。lock.js は書き換えていません')
  }
  if (await L.open('NOT-A-REAL-CODE-' + b64(globalThis.crypto.getRandomValues(new Uint8Array(6)))) !== null) {
    throw new Error('違うコードで中身が戻ってしまいました。lock.js は書き換えていません')
  }
} finally {
  try { unlinkSync(tmp) } catch {}
}
writeFileSync(out, js)

const notes = []
if (allowShort) notes.push('短いコードを通しました')
if (allowLeaked) notes.push('公開済みのコードを通しました')
console.log(`members/lock.js を書き出しました（${items.length}件。全部のコードで戻ること、違うコードで戻らないことを確認済み）${notes.length ? '【注意】' + notes.join('・') : ''}`)
