// 九星気学盤: オフライン用サービスワーカー
// ファイルを更新したときは、下の VERSION を変えると、端末のキャッシュが入れ替わります。
const VERSION = 'kigaku-v5';
const CORE = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', (e) => {
  // 公開サーバーの一時保存を使わず、常に最新のファイルを取り込みます。
  e.waitUntil(
    caches.open(VERSION)
      .then((c) => Promise.all(CORE.map((u) => fetch(u, { cache: 'reload' }).then((r) => { if (r.ok) return c.put(u, r); }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;
  const fonts = url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (!sameOrigin && !fonts) return;

  const isPage = sameOrigin && (req.mode === 'navigate' || url.pathname.endsWith('/') ||
    url.pathname.endsWith('.html') || url.pathname.endsWith('.webmanifest'));

  if (isPage) {
    // 画面本体は、電波があれば常に最新を取得し、電波がないときだけ保存したものを使います。
    e.respondWith(
      fetch(url.href, { cache: 'no-cache' })
        .then((res) => {
          if (res && res.ok) { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); }
          return res;
        })
        .catch(() => caches.match(req, { ignoreSearch: true }).then((hit) => hit || caches.match('./index.html')))
    );
    return;
  }

  // アイコンやフォントは、保存したものを先に使い、裏で更新します。
  e.respondWith(
    caches.open(VERSION).then((cache) =>
      cache.match(req, { ignoreSearch: true }).then((hit) => {
        const net = fetch(req)
          .then((res) => { if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()); return res; })
          .catch(() => hit);
        return hit || net;
      })
    )
  );
});
