# Historiapp: línea del tiempo (#linea) y biblioteca de pódcast (#podcast) en la barra inferior.
# Uso: python3 tools/patch_linea.py  (desde la carpeta Historiapp). Idempotente: no hace nada si ya está aplicado.
import re, shutil, os, sys
P = "index.html"
t = open(P, encoding="utf-8").read()
if "/* --- línea del tiempo (patch_linea) --- */" in t:
    print("ya aplicado"); sys.exit(0)
shutil.copy(P, "tools/index_antes_linea.html")

def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c >= 1, "no encontrado: " + a[:60]
    t = t.replace(a, b, n)

CSS = r"""
/* --- línea del tiempo y pódcast (patch_linea) --- */
#tabbar button{font-size:9.5px;letter-spacing:-.02em;padding:6px 0 4px}
#tabbar button .i{font-size:19px}
:root{--ln-egi:#EDAB00;--ln-egi2:#F7D77A;--ln-per:#004379;--ln-per2:#5B8DB8;--ln-fen:#5E6B78;--ln-fen2:#A9B4BF;--ln-inter:#e3e7ec}
html.dark{--ln-per:#3d7cc0;--ln-per2:#2a5a8c;--ln-fen2:#46525e;--ln-egi2:#9c7a12;--ln-inter:#26313c}
.lnmain{padding-left:0!important;padding-right:0!important}
.lnsub{margin:0 16px 8px;color:var(--muted);font-size:14px}
.lnbar{display:flex;flex-wrap:wrap;gap:6px;padding:0 12px 8px;align-items:center}
.lnchip{border:1.5px solid var(--line);background:var(--paper);color:var(--ink);border-radius:16px;padding:4px 10px;font:inherit;font-size:13px;display:flex;align-items:center;gap:5px}
.lnchip .sw{width:10px;height:10px;border-radius:2px}.lnchip.off{opacity:.4;text-decoration:line-through}
.lnseg{display:flex;border:1.5px solid var(--line);border-radius:16px;overflow:hidden;background:var(--paper)}
.lnseg button{background:transparent;color:var(--ink);font:inherit;font-size:13px;padding:4px 9px}.lnseg button.on{background:var(--primary);color:#fff}
.lnsp{flex:1}.lnic{border:1.5px solid var(--line);background:var(--paper);color:var(--ink);border-radius:50%;width:30px;height:30px;font-size:16px;line-height:1}
.lnprog{font-size:12px;color:var(--muted);padding:0 16px 6px}.lnprog b{color:var(--tp)}
#lnVp{position:relative}#lnVp.h{overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain}
#lnTl{position:relative}
.ln-era{position:absolute;border-radius:4px;overflow:hidden;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;border:1px solid rgba(255,255,255,.5)}
.ln-era span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:2px}.ln-v .ln-era span{writing-mode:vertical-rl;transform:rotate(180deg)}
.ln-era.c-egi{background:var(--ln-egi);color:#2b2100}.ln-era.c-egi.alt{background:var(--ln-egi2);color:#2b2100}
.ln-era.c-per{background:var(--ln-per)}.ln-era.c-per.alt{background:var(--ln-per2)}
.ln-era.c-fen{background:var(--ln-fen)}.ln-era.c-fen.alt{background:var(--ln-fen2);color:#1d252d}
.ln-era.inter{background:repeating-linear-gradient(45deg,var(--ln-inter),var(--ln-inter) 4px,transparent 4px,transparent 8px)!important;color:var(--muted)!important;border:1px dashed var(--line)}
.ln-colhd{position:absolute;font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.ln-axis{position:absolute;background:var(--line)}
.ln-tick{position:absolute;font-size:10.5px;color:var(--muted);background:var(--bg);padding:1px 5px;border:1px solid var(--line);border-radius:9px;white-space:nowrap;transform:translate(-50%,-50%)}
.ln-brk{position:absolute;font-size:10px;color:var(--muted);background:var(--bg);padding:0 4px;white-space:nowrap;transform:translate(-50%,-50%);font-style:italic}
.ln-dot{position:absolute;width:12px;height:12px;border-radius:50%;transform:translate(-50%,-50%);border:2px solid var(--paper)}.ln-dot.h{background:var(--paper)!important;border:2px solid var(--muted)}
.ln-con{position:absolute;background:var(--line)}
.ln-card{position:absolute;background:var(--paper);border-radius:10px;padding:7px 10px 8px 12px;box-shadow:var(--shadow);cursor:pointer;border-left:5px solid var(--muted);color:var(--ink)}
.ln-card .dt{font-size:12px;color:var(--muted);display:flex;gap:6px;align-items:center}
.ln-card .tt{font-size:15px;line-height:1.2;margin-top:2px}.ln-card.d .tt{font-weight:700}.ln-card.h{border-left-style:dashed}
.ln-h .ln-card .tt{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.ln-tag{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.3px;border-radius:4px;padding:0 4px}
.ln-tag.d{background:var(--primary);color:#fff}.ln-tag.h{border:1px solid var(--muted);color:var(--muted)}
.ln-ok{margin-left:auto;font-weight:700;color:var(--ok)}.ln-ko{margin-left:auto;font-weight:700;color:var(--ko)}
#lnBk{position:fixed;inset:0;background:rgba(0,0,0,.35);opacity:0;pointer-events:none;transition:opacity .2s;z-index:50}#lnBk.on{opacity:1;pointer-events:auto}
#lnSh{position:fixed;left:0;right:0;bottom:0;max-height:88vh;overflow:auto;background:var(--paper);color:var(--ink);border-radius:18px 18px 0 0;padding:10px 18px calc(24px + var(--safe-bottom));transform:translateY(105%);transition:transform .25s;max-width:640px;margin:0 auto;box-shadow:0 -4px 20px rgba(0,0,0,.2);z-index:51}
#lnSh.on{transform:none}#lnSh .grip{width:40px;height:4px;border-radius:2px;background:var(--line);margin:0 auto 10px}
#lnSh h2{margin:6px 0 2px;font-size:21px;line-height:1.2;color:var(--tp)}
#lnSh .meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
#lnSh .big{font-size:17px;font-weight:700;margin-top:6px}#lnSh .era{font-size:14px;margin-top:2px}
#lnSh p.x{font-size:15.5px;line-height:1.45;margin:10px 0 6px}#lnSh .src{font-size:12.5px;color:var(--muted);margin-bottom:12px}
#lnSh .qbox{border-top:1px solid var(--line);padding-top:10px}#lnSh .qbox h3{font-size:13px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);margin:0 0 4px}
#lnSh .q{font-size:16px;font-weight:700;margin:0 0 8px}
#lnSh .lopt{display:block;width:100%;text-align:left;font:inherit;font-size:15px;color:var(--ink);background:transparent;border:1.5px solid var(--line);border-radius:10px;padding:9px 12px;margin:6px 0}
#lnSh .lopt.ok{border-color:var(--ok);background:var(--ok-bg);font-weight:700}#lnSh .lopt.ko{border-color:var(--ko);background:var(--ko-bg)}
#lnSh .res{font-size:14px;margin-top:6px;font-weight:700}
#lnSh .nav2{display:flex;justify-content:space-between;margin-top:14px}
#lnSh .nav2 button{font:inherit;font-size:14px;background:var(--primary);color:#fff;border-radius:18px;padding:7px 14px}#lnSh .nav2 button[disabled]{opacity:.35}
.ln-sw.c-egi{background:var(--ln-egi)}.ln-sw.c-per{background:var(--ln-per)}.ln-sw.c-fen{background:var(--ln-fen)}
/* biblioteca de pódcast */
.pdmain{padding:0!important;background:#121417;color:#fff;min-height:calc(100vh - 60px)}
.pdhero{background:linear-gradient(180deg,#0b4d86 0%,#0b2a4a 55%,#121417 100%);padding:22px 16px 18px}
.pdhero .k{font-size:12px;letter-spacing:.6px;text-transform:uppercase;opacity:.8}.pdhero h2{margin:4px 0 2px;font-size:30px;color:#fff}.pdhero p{margin:0;font-size:14px;opacity:.85}
.pdsec{padding:6px 16px 4px;font-size:18px;font-weight:700}
.pdcont{display:flex;gap:12px;margin:6px 16px 14px;background:#22262c;border-radius:10px;overflow:hidden;cursor:pointer;align-items:center}
.pdcont .pdcv{width:84px;height:84px;border-radius:0}.pdcont .ci{padding:8px 10px 8px 0;min-width:0;flex:1}.pdcont .ci b{display:block;font-size:15px;line-height:1.2}.pdcont .ci small{color:#b3b3b3;font-size:12px}
.pdbar{height:3px;background:#444;border-radius:2px;margin-top:6px;overflow:hidden}.pdbar i{display:block;height:100%;background:var(--accent)}
.pdcv{flex:none;border-radius:6px;background:linear-gradient(135deg,#004379,#002060);display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-weight:800;line-height:1;position:relative;overflow:hidden}
.pdcv.t1{background:linear-gradient(135deg,#7a4e00,#EDAB00)}.pdcv img{width:42%;height:auto;opacity:.95;margin-bottom:3px;filter:none!important}
.pdep{display:flex;gap:12px;align-items:center;padding:10px 16px;cursor:pointer}.pdep:active{background:#1c2026}
.pdep .pdcv{width:56px;height:56px;font-size:15px}.pdep .ei{flex:1;min-width:0}.pdep .ei b{display:block;font-size:15px;line-height:1.25;font-weight:600}
.pdep .ei small{display:block;color:#b3b3b3;font-size:12.5px;margin-top:2px}.pdep .pdbar{max-width:160px}
.pdplay{flex:none;width:40px;height:40px;border-radius:50%;background:var(--accent);color:#1d1600;font-size:16px;display:flex;align-items:center;justify-content:center}
.pdnote{color:#8a8f96;font-size:12px;padding:10px 16px 24px}
#pdFull{position:fixed;inset:0;background:linear-gradient(180deg,#0b4d86,#121417 70%);color:#fff;z-index:52;transform:translateY(100%);transition:transform .3s;display:flex;flex-direction:column;padding:calc(14px + var(--safe-top)) 22px calc(26px + var(--safe-bottom));overflow:auto;max-width:640px;margin:0 auto}
#pdFull.on{transform:none}
#pdFull .top{display:flex;align-items:center;justify-content:space-between;font-size:12px;letter-spacing:.5px;text-transform:uppercase;opacity:.85;text-align:center}
#pdFull .top button{background:transparent;color:#fff;font-size:26px;width:40px}
#pdFull .pdcv{width:min(74vw,320px);height:min(74vw,320px);margin:20px auto 18px;font-size:58px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.5)}
#pdFull h2{margin:0;font-size:21px;line-height:1.25;color:#fff}#pdFull .tm{color:#b3b3b3;font-size:14px;margin-top:4px}
#pdFull input[type=range]{width:100%;margin:18px 0 2px;accent-color:#fff}
#pdFull .times{display:flex;justify-content:space-between;font-size:12px;color:#b3b3b3}
#pdFull .ctrl{display:flex;align-items:center;justify-content:space-around;margin:14px 0}
#pdFull .ctrl button{background:transparent;color:#fff;font:inherit;font-size:15px}
#pdFull .ctrl .pp{width:66px;height:66px;border-radius:50%;background:#fff;color:#121417;font-size:26px}
#pdFull .spd{border:1px solid #777;border-radius:14px;padding:3px 10px}
#pdFull .ds{font-size:14px;line-height:1.45;color:#d0d4d9;background:#22262c;border-radius:10px;padding:12px 14px;margin-top:10px}
"""
i = t.index("</style>")
t = t[:i] + CSS + t[i:]

# textos
rep('tabSearch:"Buscar",', 'tabSearch:"Buscar", tabLine:"Línea", tabPod:"Pódcast", tabEncS:"Deportes", lnTitle:"Línea del tiempo", lnSub:"Eras, deportes y hechos fechados de los temas publicados. Toca un hito para ver su ficha y su pregunta.", lnAll:"Todo", lnD:"Deporte", lnH:"Historia", lnZin:"Acercar", lnZout:"Alejar", lnVert:"Ver en vertical", lnHor:"Ver en horizontal", lnProg:"Preguntas respondidas: <b>{a}/{v}</b> · aciertos: <b>{o}</b>", lnEra:"Era", lnSrc:"Fuente", lnSlide:"diapositiva {n} del Tema {t}", lnTest:"Pon a prueba lo que sabes", lnPrev:"‹ Anterior", lnNext:"Siguiente ›", lnOk:"✓ Correcto · +{n} XP", lnOk0:"✓ Correcto", lnKo:"✗ No es esa. La respuesta correcta está marcada en azul.", lnYears:"≈ {n} años", lnBC:"a. C.", lnAD:"d. C.", pdTitle:"Pódcast", pdK:"Historiapp", pdH:"Pódcast", pdP:"Repasos de cada tema en forma de conversación", pdCont:"Seguir escuchando", pdEps:"Episodios", pdLeft:"quedan {m} min", pdPlaying:"Reproduciendo", pdFrom:"Desde Historiapp", pdNone:"Todavía no hay episodios publicados.", pdNote:"El reproductor sigue sonando aunque cambies de pantalla o bloquees el móvil.",')
rep('tabSearch:"Search",', 'tabSearch:"Search", tabLine:"Timeline", tabPod:"Podcast", tabEncS:"Sports", lnTitle:"Timeline", lnSub:"Eras, sports and dated events from the published units. Tap a milestone to open it and answer its question.", lnAll:"All", lnD:"Sport", lnH:"History", lnZin:"Zoom in", lnZout:"Zoom out", lnVert:"Vertical view", lnHor:"Horizontal view", lnProg:"Questions answered: <b>{a}/{v}</b> · correct: <b>{o}</b>", lnEra:"Era", lnSrc:"Source", lnSlide:"slide {n} of Unit {t}", lnTest:"Test yourself", lnPrev:"‹ Previous", lnNext:"Next ›", lnOk:"✓ Correct · +{n} XP", lnOk0:"✓ Correct", lnKo:"✗ Not that one. The correct answer is marked in blue.", lnYears:"≈ {n} years", lnBC:"BC", lnAD:"AD", pdTitle:"Podcast", pdK:"Historiapp", pdH:"Podcast", pdP:"Conversational reviews of each unit", pdCont:"Continue listening", pdEps:"Episodes", pdLeft:"{m} min left", pdPlaying:"Now playing", pdFrom:"From Historiapp", pdNone:"No episodes published yet.", pdNote:"The player keeps going when you change screen or lock your phone.",')

# barra inferior, rutas y render
rep('const TABS=[["home","🏠","tabHome"],["temas","📚","tabTemas"],["videos","▶️","tabVid"],["search","🔎","tabSearch"],["enc","📖","tabEnc"],["exam","🎓","tabExam"]];',
    'const TABS=[["home","🏠","tabHome"],["temas","📚","tabTemas"],["videos","▶️","tabVid"],["linea","🕰️","tabLine"],["pods","🎧","tabPod"],["search","🔎","tabSearch"],["enc","📖","tabEncS"],["exam","🎓","tabExam"]];')
rep('function tabOf(v){ const n=(v||{}).name; ', 'function tabOf(v){ const n=(v||{}).name; if(n==="linea") return "linea"; if(n==="pods") return "pods"; ')
rep('if(v.name==="settings") return "ajustes";', 'if(v.name==="settings") return "ajustes"; if(v.name==="linea") return "linea"; if(v.name==="pods") return "podcast";')
rep('if(h==="ajustes") return {name:"settings"};', 'if(h==="ajustes") return {name:"settings"}; if(h==="linea") return {name:"linea"}; if(h==="podcast") return {name:"pods"};')
rep('  if(v.name==="home") return renderHome();', '  try{ lnClose(); pdCloseFull(); }catch(_){}\n  if(v.name==="linea") return renderLinea();\n  if(v.name==="pods") return renderPods();\n  if(v.name==="home") return renderHome();')

JS = r"""
/* --- línea del tiempo (patch_linea) --- */
const LN={data:null,civ:null,kind:"all",zoom:1,orient:"auto"};
const LN_ZK=[0.09,0.18,0.36,0.7], LN_ZMAX=[70,120,190,280];
async function getLinea(){
  if(!LN.data){ const D=await fetch("data/linea.json",{cache:"no-cache"}).then(r=>r.json()); const idx=await getIndex();
    const av=new Set(idx.temas.filter(m=>m.available).map(m=>m.num));
    D.hitos=D.hitos.filter(h=>av.has(h.tema)); D.eras=D.eras.filter(e=>av.has(e.tema));
    D.civs=D.civs.filter(c=>D.eras.some(e=>e.civ===c.id)||D.hitos.some(h=>h.civ===c.id)); LN.data=D; }
  return LN.data;
}
const lnIsH=()=>{ const m=app.querySelector("main"); return LN.orient==="h"||(LN.orient==="auto"&&!!m&&m.clientWidth>=760); };
const lnT=h=>h[S.lang]||h.es;
const lnFmt=y=>y<0?`${-y} ${t("lnBC")}`:(S.lang==="en"?`${t("lnAD")} ${y}`:`${y} ${t("lnAD")}`);
const lnSrc=s=>S.lang==="en"?s.replace(/ y /g," and ").replace(/ e /g," and "):s;
function lnEl(cls,css,html){ const d=document.createElement("div"); d.className=cls; Object.assign(d.style,css||{}); if(html!=null) d.innerHTML=html; return d; }
function lnVis(){ return LN.data.hitos.filter(h=>LN.civ.has(h.civ)&&(LN.kind==="all"||h.k===LN.kind)).sort((a,b)=>a.y-b.y||a.civ.localeCompare(b.civ)); }
function lnEra(h){ const tt=lnT(h); if(tt.era) return {n:tt.era}; const e=LN.data.eras.find(e=>e.civ===h.civ&&h.y>=e.from&&h.y<e.to); return e?{n:L(e.n),f:L(e.f)}:{n:""}; }
async function renderLinea(){
  app.innerHTML=header(t("lnTitle"),true)+`<main class="lnmain"><div class="empty">…</div></main>`;
  bindHeader(()=>nav({name:"home"}));
  let D; try{ D=await getLinea(); }catch(e){ app.querySelector("main").innerHTML=`<div class="empty">${t("loadError")}</div>`; return; }
  if(S.view.name!=="linea") return;
  if(!LN.civ) LN.civ=new Set(D.civs.map(c=>c.id));
  const m=app.querySelector("main");
  m.innerHTML=`<p class="lnsub">${esc(t("lnSub"))}</p><div class="lnbar" id="lnBar"></div><div class="lnprog" id="lnProg"></div><div id="lnVp"><div id="lnTl"></div></div>`;
  lnBar(); lnDraw();
}
function lnBar(){
  const b=document.getElementById("lnBar"); if(!b) return; b.innerHTML="";
  LN.data.civs.forEach(c=>{ const x=document.createElement("button"); x.className="lnchip"+(LN.civ.has(c.id)?"":" off");
    x.innerHTML=`<span class="sw ln-sw c-${c.id}"></span>${esc(L(c.name))}`;
    x.onclick=()=>{ if(LN.civ.has(c.id)){ if(LN.civ.size>1) LN.civ.delete(c.id); } else LN.civ.add(c.id); lnBar(); lnDraw(); }; b.appendChild(x); });
  const s=document.createElement("div"); s.className="lnseg";
  [["all","lnAll"],["d","lnD"],["h","lnH"]].forEach(([k,l])=>{ const x=document.createElement("button"); x.textContent=t(l); if(LN.kind===k) x.className="on"; x.onclick=()=>{ LN.kind=k; lnBar(); lnDraw(); }; s.appendChild(x); });
  b.appendChild(s); b.appendChild(lnEl("lnsp"));
  const mk=(tx,ti,f)=>{ const x=document.createElement("button"); x.className="lnic"; x.textContent=tx; x.title=t(ti); x.setAttribute("aria-label",t(ti)); x.onclick=f; b.appendChild(x); };
  mk("−","lnZout",()=>{ if(LN.zoom>0){ LN.zoom--; lnDraw(true); } });
  mk("+","lnZin",()=>{ if(LN.zoom<LN_ZK.length-1){ LN.zoom++; lnDraw(true); } });
  mk(lnIsH()?"⇅":"⇆",lnIsH()?"lnVert":"lnHor",()=>{ LN.orient=lnIsH()?"v":"h"; lnBar(); lnDraw(); });
}
function lnProg(){ const p=document.getElementById("lnProg"); if(!p) return; const A=S.prog.linea||{}, ids=LN.data.hitos.map(h=>h.id);
  const a=ids.filter(i=>A[i]).length, o=ids.filter(i=>A[i]&&A[i].ok).length; p.innerHTML=t("lnProg",{a,v:ids.length,o}); }
function lnDraw(keep){
  const vp=document.getElementById("lnVp"), tl=document.getElementById("lnTl"); if(!vp||!tl) return;
  const H=lnIsH(), D=LN.data;
  let frac=0;
  if(keep&&tl.offsetHeight){ if(H) frac=(vp.scrollLeft+vp.clientWidth/2)/tl.offsetWidth; else { const top=tl.getBoundingClientRect().top; frac=(innerHeight/2-top)/tl.offsetHeight; } }
  tl.innerHTML=""; tl.className=H?"ln-h":"ln-v"; vp.className=H?"h":"";
  const hs=lnVis(), civs=D.civs.filter(c=>LN.civ.has(c.id)), eras=D.eras.filter(e=>LN.civ.has(e.civ));
  const k=LN_ZK[LN.zoom], MAXG=LN_ZMAX[LN.zoom]*(H?1.6:1);
  const by={}; hs.forEach(h=>(by[h.y]=by[h.y]||[]).push(h));
  const anc=[...new Set([...hs.map(h=>h.y),...eras.flatMap(e=>[e.from,e.to])])].sort((a,b)=>a-b);
  if(!anc.length) return;
  const W=vp.clientWidth, COLW=22, COLG=4, ERAX=8, ax=H?0:ERAX+civs.length*(COLW+COLG)+76;
  const CL=ax+18, CW=H?210:Math.max(160,Math.min(W-CL-10,460));
  const A=S.prog.linea||{}, cards={};
  hs.forEach(h=>{ const tt=lnT(h), a=A[h.id]; const c=lnEl("ln-card "+h.k,{width:CW+"px",borderLeftColor:`var(--ln-${h.civ})`});
    c.innerHTML=`<div class="dt"><span class="ln-tag ${h.k}">${t(h.k==="d"?"lnD":"lnH")}</span>${esc(tt.d)}${a?`<span class="${a.ok?"ln-ok":"ln-ko"}">${a.ok?"✓":"✗"}</span>`:""}</div><div class="tt">${esc(tt.t)}</div>`;
    c.onclick=()=>lnOpen(h.id); tl.appendChild(c); if(H) c.style.height="96px"; cards[h.id]=c; });
  const pos=[], breaks=[]; let p=H?70:46, prev=null;
  const gap=a=>{ if(prev===null) return; const dy=(a-prev)*k, g=Math.min(dy,MAXG); if(dy>MAXG&&a-prev>=120) breaks.push([pos.length-1,a-prev]); p+=Math.max(g,2); };
  const AY=250;
  if(!H){ let lastB=0;
    anc.forEach(a=>{ gap(a); const cs=by[a];
      if(cs){ p=Math.max(p,lastB+28); let top=p-16; cs.forEach(h=>{ const c=cards[h.id]; c.style.left=CL+"px"; c.style.top=top+"px"; top+=c.offsetHeight+8; }); lastB=top-8; }
      pos.push(p); prev=a; });
    tl.style.height=(Math.max(p,lastB)+40)+"px"; tl.style.width="100%"; vp.style.height="";
  } else { const lanes=[0,0];
    anc.forEach(a=>{ gap(a); const cs=by[a];
      if(cs){ const ls=cs.length===1?[lanes[0]<=lanes[1]?0:1]:[0,1]; p=Math.max(p,...ls.map(l=>lanes[l]+28));
        cs.forEach((h,i)=>{ const l=ls[i%ls.length], c=cards[h.id]; c.style.left=(p-18)+"px"; c.style.top=(l===0?128:18)+"px"; lanes[l]=p-18+CW; }); }
      pos.push(p); prev=a; });
    tl.style.width=(Math.max(p,...lanes)+80)+"px"; const hh=AY+30+civs.length*32+10; tl.style.height=hh+"px"; vp.style.height=hh+"px"; }
  const map=y=>{ if(y<=anc[0]) return pos[0]; if(y>=anc[anc.length-1]) return pos[pos.length-1]; let i=0; while(anc[i+1]<y) i++; return pos[i]+(pos[i+1]-pos[i])*(y-anc[i])/(anc[i+1]-anc[i]); };
  tl.appendChild(H?lnEl("ln-axis",{left:"30px",width:(parseFloat(tl.style.width)-60)+"px",top:(AY-1)+"px",height:"3px"}):lnEl("ln-axis",{left:(ax-1)+"px",width:"3px",top:"20px",height:(parseFloat(tl.style.height)-30)+"px"}));
  civs.forEach((c,ci)=>{
    tl.appendChild(H?lnEl("ln-colhd",{left:"6px",top:(AY+14+ci*32)+"px"},esc(L(c.name))):lnEl("ln-colhd",{left:(ERAX+ci*(COLW+COLG))+"px",top:"4px",width:COLW+"px",textAlign:"center"},esc(L(c.name).slice(0,3))));
    let alt=0;
    eras.filter(e=>e.civ===c.id).forEach(e=>{ const a=map(e.from), b=map(e.to), len=b-a, nm=L(e.n), fd=L(e.f);
      const d=lnEl("ln-era c-"+c.id+(e.inter?" inter":(alt++%2?" alt":"")),H?{left:a+"px",width:Math.max(len,3)+"px",top:(AY+26+ci*32)+"px",height:"26px"}:{left:(ERAX+ci*(COLW+COLG))+"px",width:COLW+"px",top:a+"px",height:Math.max(len,3)+"px"});
      d.title=nm+(fd?" ("+fd+")":""); if(len>(H?40:34)) d.innerHTML=`<span>${esc(nm)}</span>`; tl.appendChild(d); }); });
  const step=[1000,500,250,100][LN.zoom], y0=Math.ceil(anc[0]/step)*step; let last=-1e9;
  for(let y=y0;y<=anc[anc.length-1];y+=step){ if(y===0) continue; const q=map(y); if(q-last<(H?90:30)) continue; last=q;
    tl.appendChild(lnEl("ln-tick",H?{left:q+"px",top:(AY+13)+"px"}:{left:(ax-8)+"px",top:q+"px",transform:"translate(-100%,-50%)"},lnFmt(y))); }
  breaks.forEach(([i,n])=>{ const m=(pos[i]+pos[i+1])/2, r=n>=1000?Math.round(n/100)*100:Math.round(n/50)*50;
    tl.appendChild(lnEl("ln-brk",H?{left:m+"px",top:(AY-14)+"px"}:{left:ax+"px",top:m+"px"},t("lnYears",{n:r}))); });
  hs.forEach(h=>{ const c=cards[h.id];
    if(!H){ const cy=parseFloat(c.style.top)+16; tl.appendChild(lnEl("ln-con",{left:ax+"px",width:(CL-ax)+"px",top:(cy-1)+"px",height:"2px"})); tl.appendChild(lnEl("ln-dot "+h.k,{left:(ax+1)+"px",top:cy+"px",background:`var(--ln-${h.civ})`})); }
    else { const cx=parseFloat(c.style.left)+18, cb=parseFloat(c.style.top)+96; tl.insertBefore(lnEl("ln-con",{left:(cx-1)+"px",width:"2px",top:cb+"px",height:(AY-cb)+"px"}),tl.firstChild); tl.appendChild(lnEl("ln-dot "+h.k,{left:cx+"px",top:(AY+1)+"px",background:`var(--ln-${h.civ})`})); } });
  if(keep){ if(H) vp.scrollLeft=frac*tl.offsetWidth-vp.clientWidth/2; else { const top=tl.getBoundingClientRect().top+scrollY; scrollTo(0,top+frac*tl.offsetHeight-innerHeight/2); } }
  lnProg();
}
document.addEventListener("wheel",e=>{ const vp=document.getElementById("lnVp"); if(vp&&vp.classList.contains("h")&&vp.contains(e.target)&&Math.abs(e.deltaY)>Math.abs(e.deltaX)){ vp.scrollLeft+=e.deltaY; e.preventDefault(); } },{passive:false});
function lnShuffle(n,seed){ const a=[...Array(n).keys()]; let s=seed; for(let i=n-1;i>0;i--){ s=(s*9301+49297)%233280; const j=Math.floor(s/233280*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function lnSheet(){ let s=document.getElementById("lnSh"); if(!s){ const bk=document.createElement("div"); bk.id="lnBk"; bk.onclick=lnClose; document.body.appendChild(bk);
    s=document.createElement("div"); s.id="lnSh"; document.body.appendChild(s);
    let ty=null; s.addEventListener("touchstart",e=>{ ty=s.scrollTop<=0?e.touches[0].clientY:null; },{passive:true});
    s.addEventListener("touchmove",e=>{ if(ty!==null&&e.touches[0].clientY-ty>80){ ty=null; lnClose(); } },{passive:true}); }
  return s; }
function lnOpen(id){
  const list=lnVis(), i=list.findIndex(h=>h.id===id), h=list[i]; if(!h) return; const tt=lnT(h), c=LN.data.civs.find(x=>x.id===h.civ), e=lnEra(h), A=S.prog.linea||{}, a=A[h.id];
  const ord=lnShuffle(tt.o.length,[...h.id].reduce((s,ch)=>s+ch.charCodeAt(0),7));
  const s=lnSheet();
  s.innerHTML=`<div class="grip"></div><div class="meta"><span class="lnchip" style="pointer-events:none"><span class="sw ln-sw c-${h.civ}"></span>${esc(L(c.name))}</span><span class="ln-tag ${h.k}">${t(h.k==="d"?"lnD":"lnH")}</span></div>
    <h2>${esc(tt.t)}</h2><div class="big">${esc(tt.d)}</div><div class="era">${e.n?`${t("lnEra")}: <b>${esc(e.n)}</b>${e.f?` (${esc(e.f)})`:""}`:""}</div>
    <p class="x">${esc(tt.x)}</p><div class="src">${t("lnSrc")}: ${esc(lnSrc(h.s))} · ${t("lnSlide",{n:h.sl,t:h.tema})}</div>
    <div class="qbox"><h3>${t("lnTest")}</h3><p class="q">${esc(tt.q)}</p><div id="lnOpts"></div><div class="res" id="lnRes"></div></div>
    <div class="nav2"><button id="lnPv" ${i<=0?"disabled":""}>${t("lnPrev")}</button><button id="lnNx" ${i>=list.length-1?"disabled":""}>${t("lnNext")}</button></div>`;
  const box=s.querySelector("#lnOpts");
  ord.forEach(j=>{ const b=document.createElement("button"); b.className="lopt"; b.textContent=tt.o[j]; b.dataset.j=j; b.onclick=()=>lnAnswer(h,j); box.appendChild(b); });
  if(a) lnPaint(a.j,false);
  s.querySelector("#lnPv").onclick=()=>lnOpen(list[i-1].id); s.querySelector("#lnNx").onclick=()=>lnOpen(list[i+1].id);
  s.scrollTop=0; s.classList.add("on"); document.getElementById("lnBk").classList.add("on");
}
function lnPaint(j,xp){ const s=document.getElementById("lnSh"); s.querySelectorAll(".lopt").forEach(b=>{ b.disabled=true; const k=+b.dataset.j; if(k===0) b.classList.add("ok"); else if(k===j) b.classList.add("ko"); });
  s.querySelector("#lnRes").innerHTML=j===0?`<span style="color:var(--ok)">${xp?t("lnOk",{n:10*(S.xpMult||1)}):t("lnOk0")}</span>`:`<span style="color:var(--ko)">${t("lnKo")}</span>`; }
function lnAnswer(h,j){ S.prog.linea=S.prog.linea||{}; if(S.prog.linea[h.id]) return; const ok=j===0;
  S.prog.linea[h.id]={j,ok}; save(); track("linea/"+h.id+"/"+(ok?"acierto":"fallo"),"Línea "+h.id,true);
  if(ok) addXP(10); else { try{ checkAch(); }catch(_){} } lnPaint(j,ok); lnDraw(true); }
function lnClose(){ const s=document.getElementById("lnSh"); if(s) s.classList.remove("on"); const b=document.getElementById("lnBk"); if(b) b.classList.remove("on"); }
addEventListener("resize",()=>{ if(S.view&&S.view.name==="linea"){ lnBar(); lnDraw(true); } });

/* --- biblioteca de pódcast (patch_linea) --- */
let PD_L=[], PD_CUR=null;
function pdEps(tema){ return modeIdxs(tema,"podcast").map(i=>{ const e=tema.podcast[i]; if(e.durs&&e.durs[S.lang]) return Object.assign({},e,{id:S.lang==="es"?e.id:e.id+"_"+S.lang,dur:e.durs[S.lang],lang:S.lang}); return e; }); }
const pdCover=(n,cls="")=>`<div class="pdcv t${n} ${cls}"><img src="icons/emblema_blanco.png" alt=""><span>T${n}</span></div>`;
const pdIsCur=it=>POD.ep&&POD.audio&&POD.ep.id===it.ep.id;
function pdPos(it){ return pdIsCur(it)?POD.audio.currentTime:(podState(it.ep.id).t||0); }
function pdDur(it){ return pdIsCur(it)&&POD.audio.duration?POD.audio.duration:it.ep.dur; }
async function renderPods(){
  app.innerHTML=header(t("pdTitle"),true)+`<main class="pdmain"><div class="empty">…</div></main>`;
  bindHeader(()=>nav({name:"home"}));
  const list=[];
  try{ const idx=await getIndex(); for(const m of idx.temas){ if(!m.available) continue; const tm=await getTema(m.num); if(!tm.podcast||!tm.podcast.length) continue; pdEps(tm).forEach(ep=>list.push({tema:tm,ep})); } }
  catch(e){ app.querySelector("main").innerHTML=`<div class="empty">${t("loadError")}</div>`; return; }
  if(S.view.name!=="pods") return;
  list.sort((a,b)=>b.tema.num-a.tema.num); PD_L=list; pdList();
}
function pdList(){
  const m=app.querySelector("main.pdmain"); if(!m) return;
  let h=`<div class="pdhero"><div class="k">${t("pdK")}</div><h2>${t("pdH")}</h2><p>${t("pdP")}</p></div>`;
  if(!PD_L.length){ m.innerHTML=h+`<div class="pdnote">${t("pdNone")}</div>`; return; }
  const started=PD_L.filter(it=>pdIsCur(it)||(podState(it.ep.id).t>5&&!podState(it.ep.id).done));
  if(started.length){ const it=started.find(pdIsCur)||started[0];
    h+=`<div class="pdsec">${t("pdCont")}</div><div class="pdcont" data-i="${PD_L.indexOf(it)}">${pdCover(it.tema.num)}<div class="ci"><b>${esc(L(it.ep.title))}</b><small class="pdleft">${t("tema")} ${it.tema.num} · ${t("pdLeft",{m:Math.max(1,Math.round((pdDur(it)-pdPos(it))/60))})}</small><div class="pdbar"><i style="width:${Math.min(100,pdPos(it)/pdDur(it)*100)}%"></i></div></div></div>`; }
  h+=`<div class="pdsec">${t("pdEps")}</div>`;
  PD_L.forEach((it,i)=>{ const pl=pdIsCur(it)&&!POD.audio.paused, pos=pdPos(it);
    h+=`<div class="pdep" data-i="${i}">${pdCover(it.tema.num)}<div class="ei"><b>${esc(L(it.ep.title))}</b><small>${t("tema")} ${it.tema.num} · ${esc(L(it.tema.title))} · ${t("pMin",{m:Math.round(it.ep.dur/60)})}${it.ep.lang&&it.ep.lang!==S.lang?` · ${esc(it.ep.lang.toUpperCase())}`:""}</small>${pos>5?`<div class="pdbar"><i style="width:${Math.min(100,pos/pdDur(it)*100)}%"></i></div>`:""}</div><button class="pdplay" data-p="${i}" aria-label="▶">${pl?"❚❚":"▶"}</button></div>`; });
  h+=`<div class="pdnote">🔒 ${t("pdNote")}</div>`;
  m.innerHTML=h;
  m.querySelectorAll("[data-i]").forEach(d=>d.onclick=()=>{ const it=PD_L[+d.dataset.i]; if(!pdIsCur(it)) podPlay(it.tema,it.ep); pdOpenFull(it); });
  m.querySelectorAll(".pdplay").forEach(b=>b.onclick=e=>{ e.stopPropagation(); const it=PD_L[+b.dataset.p]; if(pdIsCur(it)&&!POD.audio.paused) POD.audio.pause(); else podPlay(it.tema,it.ep); });
}
function pdFullEl(){ let f=document.getElementById("pdFull"); if(!f){ f=document.createElement("div"); f.id="pdFull"; document.body.appendChild(f); } return f; }
function pdOpenFull(it){ PD_CUR=it; pdFull(); pdFullEl().classList.add("on"); }
function pdCloseFull(){ const f=document.getElementById("pdFull"); if(f) f.classList.remove("on"); }
function pdFull(){ const it=PD_CUR; if(!it) return; const f=pdFullEl(), d=pdDur(it), pos=pdPos(it), st=podState(it.ep.id), a=POD.audio, cur=pdIsCur(it);
  f.innerHTML=`<div class="top"><button id="pfX" aria-label="✕">⌄</button><span>${t("pdPlaying")}<br><b>${t("pdFrom")}</b></span><span style="width:40px"></span></div>
    ${pdCover(it.tema.num)}<h2>${esc(L(it.ep.title))}</h2><div class="tm">${t("tema")} ${it.tema.num} · ${esc(L(it.tema.title))}</div>
    <input type="range" id="pfR" min="0" step="1" max="${Math.floor(d)}" value="${Math.floor(pos)}">
    <div class="times"><span id="pfC">${fmtT(pos)}</span><span id="pfL">-${fmtT(d-pos)}</span></div>
    <div class="ctrl"><button class="spd" id="pfS">${String(st.rate||1).replace(".",S.lang==="es"?",":".")}×</button><button id="pfB">↺ 15</button><button class="pp" id="pfP">${cur&&!a.paused?"❚❚":"▶"}</button><button id="pfF">30 ↻</button><span style="width:44px"></span></div>
    ${L(it.ep.desc)?`<div class="ds">${md(L(it.ep.desc))}</div>`:""}`;
  f.querySelector("#pfX").onclick=pdCloseFull;
  f.querySelector("#pfP").onclick=()=>{ if(pdIsCur(it)&&!POD.audio.paused) POD.audio.pause(); else podPlay(it.tema,it.ep); };
  f.querySelector("#pfB").onclick=()=>{ if(pdIsCur(it)) POD.audio.currentTime=Math.max(0,POD.audio.currentTime-15); else { st.t=Math.max(0,(st.t||0)-15); save(); pdFull(); } };
  f.querySelector("#pfF").onclick=()=>{ if(pdIsCur(it)) POD.audio.currentTime+=30; else { st.t=Math.min(it.ep.dur-5,(st.t||0)+30); save(); pdFull(); } };
  f.querySelector("#pfS").onclick=()=>{ const r=[1,1.25,1.5,1.75], n=r[(r.indexOf(st.rate||1)+1)%r.length]; st.rate=n; if(pdIsCur(it)) POD.audio.playbackRate=n; save(); pdFull(); };
  const R=f.querySelector("#pfR"); R.oninput=()=>{ R._drag=true; f.querySelector("#pfC").textContent=fmtT(+R.value); };
  R.onchange=()=>{ R._drag=false; if(pdIsCur(it)) POD.audio.currentTime=+R.value; else { st.t=+R.value; save(); } pdUI(); };
}
function pdUI(){
  const f=document.getElementById("pdFull");
  if(f&&f.classList.contains("on")&&PD_CUR){ const it=PD_CUR, d=pdDur(it), pos=pdPos(it), R=f.querySelector("#pfR");
    if(R&&!R._drag){ R.max=Math.floor(d); R.value=Math.floor(pos); } const c=f.querySelector("#pfC"); if(c){ c.textContent=fmtT(pos); f.querySelector("#pfL").textContent="-"+fmtT(d-pos); }
    const p=f.querySelector("#pfP"); if(p) p.textContent=pdIsCur(it)&&!POD.audio.paused?"❚❚":"▶"; }
  const m=app.querySelector("main.pdmain"); if(!m) return;
  m.querySelectorAll(".pdplay").forEach(b=>{ const it=PD_L[+b.dataset.p]; b.textContent=pdIsCur(it)&&!POD.audio.paused?"❚❚":"▶"; });
  m.querySelectorAll("[data-i]").forEach(d=>{ const it=PD_L[+d.dataset.i], i=d.querySelector(".pdbar i"); if(i) i.style.width=Math.min(100,pdPos(it)/pdDur(it)*100)+"%";
    const l=d.querySelector(".pdleft"); if(l) l.textContent=`${t("tema")} ${it.tema.num} · ${t("pdLeft",{m:Math.max(1,Math.round((pdDur(it)-pdPos(it))/60))})}`; });
}
{ const _podUI0=podUI; podUI=function(){ _podUI0.apply(this,arguments); try{ pdUI(); }catch(_){} }; }
"""

# logros de la línea del tiempo
rep('bdg9:{n:"Nueve medallas",d:"Consigue nueve medallas de modos de estudio"}}', 'bdg9:{n:"Nueve medallas",d:"Consigue nueve medallas de modos de estudio"},ln10:{n:"Viajero del tiempo",d:"Acierta diez preguntas de la línea del tiempo"},lnAll:{n:"Toda la historia",d:"Responde todos los hitos publicados en la línea del tiempo"}}')
rep('bdg9:{n:"Nine badges",d:"Earn nine study-mode badges"}}', 'bdg9:{n:"Nine badges",d:"Earn nine study-mode badges"},ln10:{n:"Time traveller",d:"Get ten timeline questions right"},lnAll:{n:"The whole story",d:"Answer every published milestone on the timeline"}}')
rep(' ["bdg9","🎖️",p=>Object.keys(p.badges||{}).length>=9]', ' ["bdg9","🎖️",p=>Object.keys(p.badges||{}).length>=9],\n ["ln10","🕰️",p=>Object.values(p.linea||{}).filter(x=>x.ok).length>=10],\n ["lnAll","⏳",p=>{ try{ const D=LN.data; return !!(D&&D.hitos.length&&D.hitos.every(h=>(p.linea||{})[h.id])); }catch(e){ return false; } }]')

# insertar el módulo justo antes del bloque de vídeos en feed
rep("/* --- vídeos en feed --- */", JS + "\n/* --- vídeos en feed --- */")
open(P, "w", encoding="utf-8").write(t)
print("aplicado")
