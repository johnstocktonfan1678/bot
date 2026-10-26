// Caches all three apps (drills, table, painter) so it runs with no connection after the first visit.
const CACHE = "nl25-preflop-v2";
const APPS = ["", "table/", "painter/"];
const FILES = ["data.js"].concat(...APPS.map(a => [a || "./", a + "index.html", a + "manifest.webmanifest", a + "icon-180.png", a + "icon-512.png"]));

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
// Network first so chart updates arrive when online; cache when offline.
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    fetch(e.request).then(r => {
      const copy = r.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy));
      return r;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match(new URL("index.html", e.request.url).href)))
  );
});
