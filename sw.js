/* Historiapp service worker (12-10-2026): instalación ligera y respuestas que no se quedan esperando a la red. */
const VERSION = "historiapp-v121";
// solo lo imprescindible para abrir la app; juegos, atlas, temas e imágenes se guardan la primera vez que se usan
const SHELL = ["./", "./index.html", "./manifest.json", "./data/temas.json", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png", "./fonts/Carlito-Regular.woff2", "./fonts/Carlito-Bold.woff2", "./fonts/Carlito-Italic.woff2", "./fonts/Carlito-BoldItalic.woff2", "./icons/logo_oro.png", "./icons/emblema_blanco.png", "./icons/emblema_oro.png"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  // se conservan los archivos ya guardados de la versión anterior (juegos, temas) para no volver a descargarlos
  e.waitUntil(caches.keys().then(async keys => {
    const cur = await caches.open(VERSION);
    for (const k of keys) {
      if (k === VERSION) continue;
      if (k.startsWith("historiapp-")) {
        const old = await caches.open(k);
        for (const req of await old.keys()) { if (!(await cur.match(req))) { const r = await old.match(req); if (r) await cur.put(req, r); } }
      }
      await caches.delete(k);
    }
  }).then(() => self.clients.claim()));
});
const put = (req, res) => { if (res && res.ok && res.status === 200) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); } return res; };
const fromNet = req => fetch(new Request(req.url, { cache: "no-cache", credentials: "same-origin" })).then(r => put(req, r));
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  if (/\.(mp4|m4a|mp3)$/.test(url.pathname)) return;   // vídeo y audio, siempre de la red
  const p = url.pathname;
  const heavy = /\/atlas\/|enciclopedia\.json$|efemerides\.json$|curiosidades\.json$|atlas(_mapa)?\.json$/.test(p);
  const game = /\/juegos\//.test(p);
  const isData = p.endsWith(".json") || p.endsWith(".html") || p.endsWith("/");
  if (game) {
    // juegos (13-10-2026): la red primero, para que al publicar una versión nueva la vean ya al abrir el juego
    // (la petición es condicional y, si no ha cambiado, apenas gasta datos); sin red o si tarda más de 4 s, la copia guardada
    e.respondWith(caches.match(req, { ignoreSearch: true }).then(hit => {
      const net = fromNet(req);
      if (!hit) return net;
      const late = new Promise(res => setTimeout(() => res(hit), 4000));
      return Promise.race([net.catch(() => hit), late]);
    }));
  } else if (heavy) {
    // archivos grandes: se abre al momento la copia guardada y se actualiza por detrás
    e.respondWith(caches.match(req, { ignoreSearch: true }).then(hit => {
      const net = fromNet(req).catch(() => hit);
      if (hit) { e.waitUntil(net.catch(() => {})); return hit; }
      return net;
    }));
  } else if (isData) {
    // la red primero, pero si tarda más de 3,5 s se usa la copia guardada
    e.respondWith(caches.match(req, { ignoreSearch: true }).then(hit => {
      const net = fromNet(req);
      if (!hit) return net;
      const late = new Promise(res => setTimeout(() => res(hit), 3500));
      return Promise.race([net.catch(() => hit), late]);
    }));
  } else {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => put(req, r))));
  }
});
