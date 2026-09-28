#!/usr/bin/env python3
"""Sección «Pódcast» por tema, con reproductor que sigue sonando al cambiar de pantalla
y con la pantalla apagada (controles en la pantalla de bloqueo).
Episodios en tools/podcast.json -> campo `podcast` de data/temaNN.json.  Audio en audio/.
Uso: python3 tools/patch_podcast.py"""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# ---------- datos ----------
P = json.load(open(os.path.join(R, 'tools', 'podcast.json')))
for num, eps in P.items():
    p = os.path.join(R, 'data', f'tema{int(num):02d}.json'); t = json.load(open(p))
    t['podcast'] = eps; json.dump(t, open(p, 'w'), ensure_ascii=False, indent=1)

# ---------- sw.js: el audio no se cachea (peticiones por rangos) ----------
p = os.path.join(R, 'sw.js'); s = open(p).read()
s = s.replace('if (url.pathname.endsWith(".mp4")) return;', 'if (/\\.(mp4|m4a|mp3)$/.test(url.pathname)) return;')
open(p, 'w').write(s)

# ---------- index.html ----------
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'function podPlay' in s:
    print('ya aplicado'); raise SystemExit

s = s.replace('quiz:"Preguntas rápidas",videos:"Vídeos"}', 'quiz:"Preguntas rápidas",videos:"Vídeos",podcast:"Pódcast"}', 1)
s = s.replace('quiz:"Test con tiempo",videos:"Píldoras en vídeo"}', 'quiz:"Test con tiempo",videos:"Píldoras en vídeo",podcast:"El tema para escuchar"}', 1)
s = s.replace('quiz:"Quick quiz",videos:"Videos"}', 'quiz:"Quick quiz",videos:"Videos",podcast:"Podcast"}', 1)
s = s.replace('quiz:"Timed test",videos:"Video bites"}', 'quiz:"Timed test",videos:"Video bites",podcast:"The unit to listen to"}', 1)
ES = ('pListen:"▶ Escuchar", pResume:"▶ Continuar", pPause:"❚❚ Pausa", pDone:"✓ Escuchado", pLeft:"quedan {m} min", pMin:"{m} min", '
      'pBg:"Sigue sonando si apagas la pantalla o si pasas a otras secciones de la app. En iPhone, instala la app para que funcione mejor.", '
      'pEsOnly:"", noPod:"Todavía no hay pódcast para este tema.", pSpeed:"Velocidad", ')
EN = ('pListen:"▶ Listen", pResume:"▶ Resume", pPause:"❚❚ Pause", pDone:"✓ Listened", pLeft:"{m} min left", pMin:"{m} min", '
      'pBg:"It keeps playing if you switch the screen off or move to other sections of the app. On iPhone, install the app for best results.", '
      'pEsOnly:"This episode is in Spanish.", noPod:"No podcast for this unit yet.", pSpeed:"Speed", ')
a = s.index('vMore:"Saber más"'); s = s[:a] + ES + s[a:]
b = s.index('vMore:"Learn more"'); s = s[:b] + EN + s[b:]

s = s.replace('videos:"🎬"};', 'videos:"🎬",podcast:"🎧"};', 1)
s = s.replace('"quiz","videos"];', '"quiz","videos","podcast"];', 1)
assert '"podcast"];' in s and 'podcast:"🎧"' in s
# medios (vídeos y pódcast) fuera de insignias y porcentajes
s = s.replace('function checkBadge(tema,mode){ if(mode==="videos") return;', 'const MEDIA=["videos","podcast"];\nfunction checkBadge(tema,mode){ if(MEDIA.includes(mode)) return;', 1)
s = s.replace('pctT=Math.round(MODES.filter(x=>x!=="videos").reduce((a,x)=>a+modePct(tm,x),0)/(MODES.length-1))+"%";',
              'pctT=Math.round(MODES.filter(x=>!MEDIA.includes(x)).reduce((a,x)=>a+modePct(tm,x),0)/(MODES.length-MEDIA.length))+"%";', 1)
s = s.replace('${m==="videos"?`<span class="pill" style="margin-top:auto">${tot}</span>`', '${MEDIA.includes(m)?`<span class="pill" style="margin-top:auto">${tot}</span>`', 1)
s = s.replace('${pct>=100&&m!=="videos"?`<div class="done">🏅</div>`:""}', '${pct>=100&&!MEDIA.includes(m)?`<div class="done">🏅</div>`:""}', 1)
s = s.replace('bd.innerHTML=MODES.filter(x=>x!=="videos").map(', 'bd.innerHTML=MODES.filter(x=>!MEDIA.includes(x)).map(', 1)
old = '''  for(const m of MODES){
    const tot=modeTotal(tema,m), pct=modePct(tema,m);'''
assert old in s
s = s.replace(old, '''  for(const m of MODES){
    const tot=modeTotal(tema,m), pct=modePct(tema,m);
    if(m==="podcast" && !tot) continue;''', 1)
s = s.replace('${mode==="videos"?t("noVideos"):t("soon")}</div>`; return; }\n  ({cards:modeSwipe',
              '${mode==="videos"?t("noVideos"):mode==="podcast"?t("noPod"):t("soon")}</div>`; return; }\n  ({cards:modeSwipe', 1)
s = s.replace('match:modeMatch,videos:modeVideos})[mode](tema,mode,m);', 'match:modeMatch,videos:modeVideos,podcast:modePodcast})[mode](tema,mode,m);', 1)
assert 'podcast:modePodcast' in s

CSS = '''.pod{background:var(--paper);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px;display:flex;flex-direction:column;gap:10px}
.pod .ph{display:flex;gap:12px;align-items:center}
.pod .ph img{width:64px;height:64px;border-radius:14px;flex:0 0 auto}
.pod .ph b{display:block;font-size:16px;color:var(--primary-2);line-height:1.25}
.pod .ph span{font-size:12.5px;color:var(--muted)}
.pod .desc{font-size:14px;line-height:1.5;margin:0}
.pod input[type=range]{width:100%;accent-color:var(--primary)}
.pod .tm{display:flex;justify-content:space-between;font-size:12px;color:var(--muted);margin-top:-6px}
.pod .ctl{display:flex;gap:8px;align-items:center;justify-content:center}
.pod .ctl button{border:0;border-radius:999px;background:#EAF1F8;color:var(--primary-2);font-weight:800;padding:10px 14px;font-size:14px}
.pod .ctl button.main{background:var(--primary);color:#fff;padding:12px 22px;font-size:16px}
.pod .spd{display:flex;gap:6px;justify-content:center;align-items:center;font-size:12px;color:var(--muted)}
.pod .spd button{border:1px solid #cdd6e2;background:#fff;border-radius:8px;padding:4px 9px;font-weight:700;color:var(--primary-2);font-size:12.5px}
.pod .spd button.on{background:var(--primary);color:#fff;border-color:var(--primary)}
.pod .note{font-size:12px;color:var(--muted);margin:0}
#podbar{position:fixed;left:10px;right:10px;bottom:calc(10px + var(--safe-bottom,0px));z-index:35;background:#002060;color:#fff;border-radius:16px;box-shadow:0 8px 24px rgba(0,0,0,.25);display:none;align-items:center;gap:10px;padding:8px 10px;max-width:520px;margin:0 auto}
#podbar.on{display:flex}
#podbar img{width:38px;height:38px;border-radius:9px}
#podbar .tt{flex:1;min-width:0;font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}
#podbar .tt small{display:block;font-weight:500;opacity:.8;font-size:11.5px}
#podbar button{border:0;background:rgba(255,255,255,.16);color:#fff;border-radius:999px;width:38px;height:38px;font-size:15px;font-weight:800}
body.feedon #podbar{display:none}
body.podon main{padding-bottom:84px}
</style>'''
assert s.count('</style>') == 1
s = s.replace('</style>', CSS, 1)
s = s.replace('<div id="app"></div>', '<div id="app"></div>\n<div id="podbar"><img src="icons/icon-192.png?v=2" alt=""><div class="tt" id="pbT"></div><button id="pbB">−15</button><button id="pbP">▶</button><button id="pbX">✕</button></div>', 1)

JS = r'''
/* --- pódcast --- */
const POD={audio:null,ep:null,tema:null,saveT:0};
function fmtT(x){ x=Math.max(0,Math.floor(x||0)); const h=Math.floor(x/3600), m=Math.floor(x%3600/60), s=x%60; return (h?h+":"+String(m).padStart(2,"0"):m)+":"+String(s).padStart(2,"0"); }
function podState(id){ S.prog.pod=S.prog.pod||{}; return S.prog.pod[id]||(S.prog.pod[id]={t:0,done:0,rate:1}); }
function podAudio(){
  if(POD.audio) return POD.audio;
  const a=new Audio(); a.preload="metadata"; POD.audio=a;
  a.addEventListener("timeupdate",()=>{ if(!POD.ep) return; const st=podState(POD.ep.id); st.t=a.currentTime;
    if(a.duration&&a.currentTime/a.duration>.95&&!st.done){ st.done=1; track("podcast/"+POD.ep.id+"/fin","Pódcast terminado",true); }
    const now=Date.now(); if(now-POD.saveT>5000){ POD.saveT=now; save(); } podUI(); });
  ["play","pause","ended","loadedmetadata"].forEach(ev=>a.addEventListener(ev,()=>{ if(ev==="ended"&&POD.ep){ podState(POD.ep.id).t=0; } save(); podUI(); }));
  if("mediaSession" in navigator){ const ms=navigator.mediaSession;
    ms.setActionHandler("play",()=>a.play()); ms.setActionHandler("pause",()=>a.pause());
    ms.setActionHandler("seekbackward",()=>{ a.currentTime=Math.max(0,a.currentTime-15); });
    ms.setActionHandler("seekforward",()=>{ a.currentTime=Math.min(a.duration||1e9,a.currentTime+30); });
    try{ ms.setActionHandler("seekto",d=>{ a.currentTime=d.seekTime; }); }catch(e){} }
  document.getElementById("pbP").onclick=()=>{ a.paused?a.play():a.pause(); };
  document.getElementById("pbB").onclick=()=>{ a.currentTime=Math.max(0,a.currentTime-15); };
  document.getElementById("pbX").onclick=()=>{ a.pause(); if(POD.ep){ podState(POD.ep.id).t=a.currentTime; save(); } POD.ep=null; a.removeAttribute("src"); a.load(); podUI(); };
  document.getElementById("pbT").onclick=()=>{ if(POD.tema) nav({name:"mode",num:POD.tema,mode:"podcast"}); };
  return a;
}
function podPlay(tema,ep){
  const a=podAudio(); const st=podState(ep.id);
  if(!POD.ep||POD.ep.id!==ep.id){ POD.ep=ep; POD.tema=tema.num; a.src=L(ep.src); a.currentTime=0;
    a.addEventListener("loadedmetadata",function f(){ a.removeEventListener("loadedmetadata",f); if(st.t&&st.t<(a.duration||1e9)-5) a.currentTime=st.t; },{once:true});
    track("podcast/"+ep.id+"/"+S.lang,"Pódcast "+ep.id,true);
    if("mediaSession" in navigator) navigator.mediaSession.metadata=new MediaMetadata({title:L(ep.title),artist:"Historiapp · "+t("tema")+" "+tema.num,album:"Historia del Deporte",artwork:[{src:"icons/icon-512.png?v=2",sizes:"512x512",type:"image/png"},{src:"icons/icon-192.png?v=2",sizes:"192x192",type:"image/png"}]}); }
  a.playbackRate=st.rate||1; a.play().catch(()=>{}); podUI();
}
function podUI(){
  const a=POD.audio, bar=document.getElementById("podbar"); if(!bar) return;
  document.body.classList.toggle("podon",!!(a&&POD.ep));
  if(!a||!POD.ep){ bar.classList.remove("on"); } else { bar.classList.add("on");
    document.getElementById("pbT").innerHTML=`${esc(L(POD.ep.title))}<small>${fmtT(a.currentTime)} / ${fmtT(a.duration||POD.ep.dur)}</small>`;
    document.getElementById("pbP").textContent=a.paused?"▶":"❚❚"; }
  document.querySelectorAll(".pod[data-id]").forEach(c=>{ const id=c.dataset.id, st=podState(id), cur=POD.ep&&POD.ep.id===id&&a;
    const dur=+c.dataset.dur, t0=cur?a.currentTime:st.t, d=cur&&a.duration?a.duration:dur;
    const r=c.querySelector("input[type=range]"); if(r&&!r._drag){ r.max=d; r.value=t0; }
    c.querySelector(".t0").textContent=fmtT(t0); c.querySelector(".t1").textContent=st.done&&!cur?t("pDone"):t("pLeft",{m:Math.max(1,Math.round((d-t0)/60))});
    c.querySelector(".main").textContent= cur&&!a.paused ? t("pPause") : (t0>5?t("pResume"):t("pListen"));
    c.querySelectorAll(".spd button").forEach(b=>b.classList.toggle("on",+b.dataset.r===(st.rate||1))); });
}
document.addEventListener("play",e=>{ if(e.target&&e.target.tagName==="VIDEO"&&POD.audio&&!POD.audio.paused) POD.audio.pause(); },true);
function modePodcast(tema,mode,m){
  const eps=modeIdxs(tema,mode).map(i=>tema.podcast[i]);
  m.innerHTML=eps.map(ep=>`<div class="pod" data-id="${esc(ep.id)}" data-dur="${ep.dur}">
    <div class="ph"><img src="icons/icon-192.png?v=2" alt=""><div><b>${esc(L(ep.title))}</b><span>${t("tema")} ${tema.num} · ${t("pMin",{m:Math.round(ep.dur/60)})}${ep.lang&&ep.lang!==S.lang?` · ${esc(ep.lang.toUpperCase())}`:""}</span></div></div>
    ${L(ep.desc)?`<p class="desc">${md(L(ep.desc))}</p>`:""}
    ${ep.lang&&ep.lang!==S.lang&&t("pEsOnly")?`<p class="note">${t("pEsOnly")}</p>`:""}
    <input type="range" min="0" step="1" value="0"><div class="tm"><span class="t0">0:00</span><span class="t1"></span></div>
    <div class="ctl"><button data-a="b">−15</button><button class="main" data-a="p"></button><button data-a="f">+30</button></div>
    <div class="spd">${t("pSpeed")} ${[1,1.25,1.5,1.75].map(r=>`<button data-r="${r}">${String(r).replace(".",",")}×</button>`).join("")}</div>
  </div>`).join("")+`<p class="note" style="text-align:center;margin:12px 8px">🔒 ${t("pBg")}</p>`;
  m.querySelectorAll(".pod").forEach(c=>{ const ep=eps.find(e=>e.id===c.dataset.id), st=podState(ep.id);
    const isCur=()=>POD.ep&&POD.ep.id===ep.id&&POD.audio;
    c.querySelector('[data-a="p"]').onclick=()=>{ if(isCur()&&!POD.audio.paused) POD.audio.pause(); else podPlay(tema,ep); };
    c.querySelector('[data-a="b"]').onclick=()=>{ if(isCur()) POD.audio.currentTime=Math.max(0,POD.audio.currentTime-15); else { st.t=Math.max(0,st.t-15); save(); podUI(); } };
    c.querySelector('[data-a="f"]').onclick=()=>{ if(isCur()) POD.audio.currentTime+=30; else { st.t=Math.min(ep.dur-5,st.t+30); save(); podUI(); } };
    const r=c.querySelector("input[type=range]");
    r.oninput=()=>{ r._drag=true; c.querySelector(".t0").textContent=fmtT(+r.value); };
    r.onchange=()=>{ r._drag=false; if(isCur()) POD.audio.currentTime=+r.value; else { st.t=+r.value; save(); } podUI(); };
    c.querySelectorAll(".spd button").forEach(b=>b.onclick=()=>{ st.rate=+b.dataset.r; if(isCur()) POD.audio.playbackRate=st.rate; save(); podUI(); });
  });
  podUI();
}
'''
anchor = '/* --- vídeos en feed --- */'
assert anchor in s
s = s.replace(anchor, JS + '\n' + anchor, 1)
# al abrir el feed de vídeos se pausa el pódcast
s = s.replace('function openFeed(tema,idxs,start,onClose){', 'function openFeed(tema,idxs,start,onClose){\n  if(POD.audio&&!POD.audio.paused) POD.audio.pause();', 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
