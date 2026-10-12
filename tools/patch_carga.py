# Historiapp: arranque más ligero (12-10-2026). Idempotente.
import os,sys
H=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=os.path.join(H,'index.html'); s=open(P,encoding='utf-8').read()
if 'homeWait' in s: print('index ya parcheado')
else:
    def rep(a,b):
        global s
        assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
    # 1. los temas ya no se copian en localStorage (llenaba la cuota y bloqueaba el arranque); la copia sin conexión la guarda el service worker
    rep('let d; try{ d=await fetchJSON(meta.file); localStorage.setItem("historiapp.tema."+num,JSON.stringify(d)); }\n  catch(e){ d=load("historiapp.tema."+num,null); if(!d) throw e; }',
        'let d; try{ d=await fetchJSON(meta.file); try{ localStorage.removeItem("historiapp.tema."+num); }catch(_){} }\n  catch(e){ d=load("historiapp.tema."+num,null); if(!d) throw e; }')
    # 2. portada: lo pesado espera a que la pantalla esté pintada
    rep('async function renderHome(){','const homeWait=ms=>new Promise(r=>setTimeout(r,ms));\nasync function renderHome(){')
    rep('  // deporte del día\n  try{ const D=await getEnc(); const E=D.entries; if(E.length&&document.getElementById("hoy")===hoy){ const e=encDaily(E); const c=sDep;',
        '  // deporte del día (se guarda el de hoy para no leer la enciclopedia entera en cada arranque)\n  try{ let e=null; const ch=load("historiapp.encHoy",null); if(ch&&ch.d===todayKey()) e=ch.e; else { await homeWait(900); const D=await getEnc(); const E=D.entries; if(E.length){ const x=encDaily(E); e={id:x.id,name:x.name,cuando:x.cuando,img:x.img&&x.img.src?{src:x.img.src}:null}; try{ localStorage.setItem("historiapp.encHoy",JSON.stringify({d:todayKey(),e})); }catch(_){} } }\n    if(e&&document.getElementById("hoy")===hoy){ const c=sDep;')
    rep('  try{ const F=await getEfe(); const k=mmdd(new Date()); if(F&&F[k]&&document.getElementById("hoy")===hoy){ const f=F[k];',
        '  try{ const k=mmdd(new Date()); let f=null; const ch=load("historiapp.efeHoy",null); if(ch&&ch.d===k) f=ch.f; else { await homeWait(300); const F=await getEfe(); f=F&&F[k]||null; if(f) try{ localStorage.setItem("historiapp.efeHoy",JSON.stringify({d:k,f})); }catch(_){} }\n    if(f&&document.getElementById("hoy")===hoy){')
    # 3. anillos de progreso de los temas: se calculan después, uno a uno
    rep('if(!S.temaCache[m.num]) getTema(m.num).then(()=>{ const r=b.querySelector(".ring"); if(r) r.innerHTML=ringSVG(temaPct(m.num)); }).catch(()=>{});',
        'if(!S.temaCache[m.num]) setTimeout(()=>{ if(!b.isConnected) return; getTema(m.num).then(()=>{ const r=b.querySelector(".ring"); if(r) r.innerHTML=ringSVG(temaPct(m.num)); }).catch(()=>{}); },1500+m.num*700);')
    # 4. limpieza única de las copias antiguas de los temas
    rep('function save(){','(function(){ try{ for(let i=localStorage.length-1;i>=0;i--){ const k=localStorage.key(i); if(k&&/^historiapp\\.tema\\.\\d+$/.test(k)) localStorage.removeItem(k); } }catch(_){} })();\nfunction save(){')
    open(P,'w',encoding='utf-8').write(s); print('index ok')
W=os.path.join(H,'sw.js')
open(W,'w',encoding='utf-8').write(r'''/* Historiapp service worker (12-10-2026): instalación ligera y respuestas que no se quedan esperando a la red. */
const VERSION = "historiapp-v89";
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
  const heavy = /\/juegos\/|\/atlas\/|enciclopedia\.json$|efemerides\.json$|curiosidades\.json$|atlas(_mapa)?\.json$/.test(p);
  const isData = p.endsWith(".json") || p.endsWith(".html") || p.endsWith("/");
  if (heavy) {
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
''')
print('sw ok')
