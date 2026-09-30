/* Historiapp service worker: app shell cached on install; data and images cached as they are used. */
const VERSION = "historiapp-v45";
const SHELL = ["./", "./index.html", "./manifest.json", "./data/temas.json", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png", "./fonts/Carlito-Regular.woff2", "./fonts/Carlito-Bold.woff2", "./fonts/Carlito-Italic.woff2", "./fonts/Carlito-BoldItalic.woff2", "./icons/logo_oro.png", "./icons/emblema_blanco.png", "./icons/emblema_oro.png"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  // videos stream straight from the network (range requests), never cached on the phone
  if (/\.(mp4|m4a|mp3)$/.test(url.pathname)) return;
  const isData = url.pathname.endsWith(".json") || url.pathname.endsWith(".html") || url.pathname.endsWith("/");
  if (isData) {
    // network first, fall back to cache (so new content arrives as soon as it is published)
    e.respondWith(fetch(new Request(e.request.url, { cache: "no-cache", credentials: "same-origin" })).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request, { ignoreSearch: true })));
  } else {
    // cache first for images and static files
    e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r; })));
  }
});
