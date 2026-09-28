#!/usr/bin/env python3
"""Actualizaciones que llegan solas:
- sw.js: index.html y los .json se piden siempre revalidando (GitHub Pages los deja 10 min en la caché del navegador).
- index.html: busca versión nueva al abrir la app y al volver a ella; si la hay, recarga sola (salvo si suena audio o vídeo).
Uso: python3 tools/patch_update.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

p = os.path.join(R, 'sw.js'); s = open(p).read()
old = 'e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request)));'
if old in s:
    s = s.replace(old, 'e.respondWith(fetch(new Request(e.request.url, { cache: "no-cache", credentials: "same-origin" })).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request, { ignoreSearch: true })));')
    open(p, 'w').write(s); print('sw ok')
else:
    print('sw: ya aplicado o distinto')

p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'historiapp.updated' in s:
    print('index: ya aplicado'); raise SystemExit
old = '  if("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(()=>{});'
assert old in s
s = s.replace(old, '''  if("serviceWorker" in navigator){
    const hadCtrl=!!navigator.serviceWorker.controller; let pend=false, done=false;
    const busy=()=>(typeof POD!=="undefined"&&POD.audio&&!POD.audio.paused)||document.body.classList.contains("feedon")||[...document.querySelectorAll("video")].some(v=>!v.paused);
    const reloadNow=()=>{ if(done) return; done=true; try{ sessionStorage.setItem("historiapp.updated","1"); }catch(e){} location.reload(); };
    navigator.serviceWorker.addEventListener("controllerchange",()=>{ if(!hadCtrl) return; if(busy()) pend=true; else reloadNow(); });
    navigator.serviceWorker.register("sw.js").then(reg=>{
      window.checkUpdate=()=>{ reg.update().catch(()=>{}); };
      document.addEventListener("visibilitychange",()=>{ if(document.visibilityState==="visible") checkUpdate(); else if(pend) reloadNow(); });
      setInterval(()=>{ if(pend&&!busy()) reloadNow(); },15000);
    }).catch(()=>{});
    try{ if(sessionStorage.getItem("historiapp.updated")){ sessionStorage.removeItem("historiapp.updated"); setTimeout(()=>toast(S.lang==="en"?"Historiapp has been updated":"Historiapp se ha actualizado",2200),2000); } }catch(e){}
  }''', 1)
open(p, 'w', encoding='utf-8').write(s)
print('index ok')
