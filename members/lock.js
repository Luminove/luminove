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
})(typeof window !== 'undefined' ? window : globalThis, {"v":1,"iter":150000,"salt":"CGlnWjNBMec9Ojcxg9NcFA==","items":[{"iv":"+zwzVqDlCqFgGpl8","ct":"SNZ88sAcy/3yipugRollBFUg/14Yee2xMhveTN/DdhYiWYshOX8vENcr6mbm/P2+QZA91iGXC4V61Zy4UEOBZ2x6b9a6zEzxnidVkY3Qd/0tGNAzztrxkPGqx69zdtXt4sPeALEFMUXrkJO40IzIub6RvTmjh07a6UbOoA6hNTIMi4ipopBdMMIiPa/Z0ThPtUj7w5Z2R+dCnpSnS7lh4phjE7i6BWfMlub0d8Rnmzk77T4fjA0ve/TzrnreY5OQJrpI8FCZHMoivO5GZOxENFErNqwQGcsVJmpNHbXGljmoU9+97yI4DtxoHk29a1IwzUTJ6BG60yo6NRbJLoLyUu0v9wiLlDjuHi2l/xnUqhFNNBpnMBzqowk/ZG7iYhc21xF7z4ELMc6voN2Z+E1WMkuVov6K5cE0Up1ao8s5uX6TUC1bN2oz"},{"iv":"eYLJsM/V+ccR0ElO","ct":"5lESgtXbiGEMWiL8eZTeQWdm8RGzVD6SVYqgLPHgoYs/qWPpsLa34ZWBwY1JpwR4kEiDq7J87rI4nsfmIw8JSsz1SlqvgOG0nhBgQYfSCFsLZwD1nN36WruBYyPDvHo4Aeci4jkmVKcsZpQZXu2jouqTmWL19DRvePUf9rdChDqw2b0xUtzwwDQXTtsWCS7JC6+T8Vc6VrWUwxPc8W7DoIbLwr5ZQ9jnspFi1LYypm4lMMPmIY/tbGgslC2MhI8MKN1FBBhD78iSZTAI487roTFN45+i+BE2PtjW/8XNgIMeHFLZndcziy1sl3FmPbzyR2fkUDSQ4j9M8mYQnnRRB0b8DwgOatVA9HE="}]});
