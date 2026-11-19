/* 会員ページの割引設定（暗号化済み）。
   このファイルは data/members-lock.mjs が作ります。手で書き換えないでください。
   ログインコードを鍵にして暗号化してあり、正しいコードを入れた端末でだけ中身が戻ります。 */
(function runtime(g, LOCK) {
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
})(typeof window !== 'undefined' ? window : globalThis, {"v":1,"iter":150000,"salt":"qPubHcD+2i99HiNWiRzNrg==","items":[{"iv":"380II+XppdKq6op2","ct":"2BgmlNlSd2LkgW4JBww534SQfOFR3F0QrsWAvXWWMZerQsxHBZctnk93/WsoeSQ7WxpA+uOIIUJDpOzKLJB6eH1ujMKTLBEZzFzxVpJvrSuLHXGMNzV1D66nfatOHKNgLHak3oFEPctO7vgIN0yce9i3WA9WPyX2cQ26UWcRK5wPb4RZYjx/NEUDnA25mCweH2A4vPYj876i1MAZwcEH0EyD0G4M/7ijaJOtJZFSRYXIS58CkLnRnswhYjk9Go34m4oE4MPfQ1qdybVjeH/J68HrwgnirWkg31ZLk4+aJbHiTpL+I51NmbUc7ydYFWdcoByWU+HCWFaVts5FJc2fuMqDoT2YARa+5eY="}]});
