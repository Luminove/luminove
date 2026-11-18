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
})(typeof window !== 'undefined' ? window : globalThis, {"v":1,"iter":150000,"salt":"ncgDjRh0KygrYrEfZ14BwQ==","items":[{"iv":"vMV3lbg5Qh1wBm59","ct":"GTWQOQgOZRwVRszCzM6Kxqjsv3eC/FvMYV6r7jSzERAgu9JyqQvu+hiqOMj0IiXOxOJyZoQISO2YlfspHWPtVVAWFsQfx6BAfD3K5MusaXT7h+1T4/ZjBO54OFcFXALbDUMS0EzymtA7Llt7l/MDop+Oz8P0P5Tz8bMsC2x80IoIZCHZJuMvhM56Eef1VlsJF3iE5XxACIJhs0IviXzZ7FRi0dFsFA7mU0b7Jz3I7dzNLzXmyNpqw7Fj9ihazGwPheDNxKtbFTf3ba7oiEGhKwx3u9VN/81TeOYAELmq+vd9jCW1qTzBNcAP0I8wF8dd0OWpwUVv1TqkOadhGyK27WgdH1HGf+owdug="},{"iv":"9mU+5B9IHvjfRseF","ct":"AYHYVLbaVc+7rI/UH0slvrHsI2YYebdoZoyaZOsHJUtB+EC+KNMoz+ElXpVqDy60cZPSaK9/r6FzB3HvtSj8KWOwGgxpF1AmEWDOPzmUYOIwdk4YcSrkiDN8B0+9Ez0U544+aXtVFP9dxGVXRi22oIW6AKO1poMdOCjQqKl0UCfthny4umS709M1CkqFIR/cPL5rysklOKhtG5K5Ar/nejVuc0VtPGYk8I/J38fwR1XD6b0E3D6xjLzvkF6RNjbP394PZtUCJMCNEpc8AlcTCWdNeQue/V/+tWM9AsUBNnLkWvADpasxyQ1fmX6UJpAqiQZhFgjMN214JlvAh7WPItPxo9xNPg3O7ND6pzlURpxgFY9j2G8IVZFM3K/AvlWJ/IA3Pwb3XUISjJ9LtotYu+0Vpg48Z9kcdGjwm/gLnCGWjdJ0fMhj"}]});
