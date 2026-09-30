#!/usr/bin/env python3
"""Interfaz nueva: la página no se desplaza (solo <main>), así iOS 26 no difumina la cabecera sin reinstalar;
barra de pestañas (Inicio, Temas, Enciclopedia, Examen, Ajustes); buscador en la cabecera; portada con racha
compacta, «Continuar», carrusel «Hoy» (reto, deporte del día, tal día como hoy, píldora) y temas en cuadrícula
con imagen y anillo; vista «Temas»; vista «Tal día como hoy»; pequeña celebración al subir de nivel y al completar el reto.
Uso: python3 tools/patch_ui3.py"""
import os,re
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
p=os.path.join(R,'index.html'); s=open(p,encoding='utf-8').read()
if 'id="tabbar"' in s or 'function renderTemas(' in s: print('ya aplicado'); raise SystemExit
def rep(o,n,cnt=1):
    global s
    assert o in s, o[:90]; s=s.replace(o,n,cnt)

# ---------- CSS ----------
rep('#app{width:100%;max-width:520px;min-height:100vh;display:flex;flex-direction:column;position:relative}',
    '#app{width:100%;max-width:520px;height:100vh;height:100dvh;min-height:0;overflow:hidden;display:flex;flex-direction:column;position:relative}\nhtml,body{overflow:hidden}')
rep('.top{position:sticky;top:0;z-index:20;','.top{position:relative;flex-shrink:0;z-index:20;')
rep('main{flex:1;padding:16px 16px calc(24px + var(--safe-bottom));display:flex;flex-direction:column;gap:14px}',
    'main{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;padding:16px 16px calc(92px + var(--safe-bottom));display:flex;flex-direction:column;gap:14px}\nmain>*{flex-shrink:0}')
rep('.gate{min-height:100vh;','.gate{flex:1;overflow-y:auto;min-height:100%;')
rep('#podbar{position:fixed;left:10px;right:10px;bottom:calc(10px + var(--safe-bottom,0px));','#podbar{position:fixed;left:10px;right:10px;bottom:calc(74px + var(--safe-bottom,0px));')
CSS='''
/* --- interfaz 3: pestañas, portada nueva --- */
#tabbar{position:fixed;left:0;right:0;bottom:0;z-index:30;max-width:520px;margin:0 auto;background:#fff;border-top:1px solid var(--line);display:flex;padding:6px 4px calc(6px + var(--safe-bottom));box-shadow:0 -4px 16px rgba(0,32,96,.06)}
#tabbar button{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 0 4px;border-radius:12px;color:var(--muted);font-size:11px;font-weight:600;position:relative}
#tabbar button .i{font-size:21px;line-height:1;filter:grayscale(1);opacity:.75}
#tabbar button.on{color:var(--primary-2);font-weight:800}
#tabbar button.on .i{filter:none;opacity:1}
#tabbar button.on::before{content:"";position:absolute;top:-7px;left:28%;right:28%;height:3px;border-radius:0 0 3px 3px;background:var(--accent)}
body.gateon #tabbar,body.feedon #tabbar{display:none}
.top .srch{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;background:rgba(255,255,255,.12);flex-shrink:0}
.strip{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:10px 12px;box-shadow:var(--shadow)}
.strip .st{display:flex;align-items:center;gap:4px;font-weight:800;color:var(--primary-2);font-size:15px;white-space:nowrap}
.strip .lv{flex:1;min-width:0}
.strip .lv b{display:block;font-size:12px;color:var(--muted);font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.strip .bar{height:6px;border-radius:6px;background:#e9eef4;overflow:hidden;margin-top:4px}
.strip .bar i{display:block;height:100%;background:var(--accent);border-radius:6px}
.cont{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,var(--primary),var(--primary-2));color:#fff;border-radius:18px;padding:14px 16px;text-align:left;box-shadow:var(--shadow)}
.cont .pl{width:42px;height:42px;border-radius:50%;background:var(--accent);color:var(--primary-2);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.cont small{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;opacity:.8;font-weight:700}
.cont b{display:block;font-size:15px;line-height:1.25}
.hoy{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:2px 16px 8px;scrollbar-width:none}
.hoy::-webkit-scrollbar{display:none}
.hoy .card{flex:0 0 78%;scroll-snap-align:start;text-align:left;border-radius:18px;padding:14px;min-height:132px;display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);background:#fff;box-shadow:var(--shadow)}
.hoy .card small{font-size:11px;text-transform:uppercase;letter-spacing:.06em;font-weight:800;color:var(--muted)}
.hoy .card b{font-size:17px;color:var(--primary-2);line-height:1.2}
.hoy .card span{font-size:13.5px;color:var(--ink);line-height:1.35;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.hoy .card .ft{margin-top:auto;display:flex;align-items:center;justify-content:space-between;font-size:12px;font-weight:700;color:var(--primary)}
.hoy .card.reto{background:#fff8e1;border:2px solid var(--accent)}
.hoy .dice{width:40px;height:40px;font-size:20px;border-radius:12px}
.tgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tcard{position:relative;border-radius:18px;overflow:hidden;min-height:150px;display:flex;flex-direction:column;justify-content:flex-end;text-align:left;color:#fff;background:var(--primary-2) center/cover no-repeat;box-shadow:var(--shadow)}
.tcard::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,32,96,.05) 20%,rgba(0,20,60,.88) 100%)}
.tcard .tx{position:relative;z-index:1;padding:10px 12px}
.tcard .tx small{display:block;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;opacity:.85}
.tcard .tx b{display:block;font-size:14.5px;line-height:1.2}
.tcard .ring{position:absolute;top:8px;right:8px;z-index:1;width:44px;height:44px}
.tcard .ring svg{width:44px;height:44px;transform:rotate(-90deg)}
.tcard .ring span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800}
.tcard.locked{background:linear-gradient(135deg,#7d8ea3,#4b5b70)}
.tcard.locked .big{position:absolute;top:10px;left:12px;z-index:1;font-size:34px;font-weight:800;opacity:.55}
.tcard.locked .lk{position:absolute;top:10px;right:12px;z-index:1;font-size:20px}
.efe-date{font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.efe-year{font-size:40px;font-weight:800;color:var(--primary);line-height:1}
.efe-txt p{line-height:1.55;margin:10px 0}
.efe-nav{display:flex;gap:10px}
.efe-nav button{flex:1;padding:12px;border-radius:12px;background:#EAF1F8;color:var(--primary-2);font-weight:700}
.confetti{position:fixed;inset:0;pointer-events:none;z-index:80;overflow:hidden}
.confetti i{position:absolute;top:-12px;width:8px;height:14px;border-radius:2px;animation:cf 1.4s ease-in forwards}
@keyframes cf{to{transform:translateY(110vh) rotate(540deg);opacity:.9}}
'''
rep('.srch-res{display:flex;',CSS+'.srch-res{display:flex;')

# ---------- textos ----------
rep('searchAll:"Buscar en Historiapp"','tabHome:"Inicio", tabTemas:"Temas", tabEnc:"Enciclopedia", tabExam:"Examen", tabSet:"Ajustes", contTitle:"Continuar", hoy:"Hoy", temasT:"Temas", dailyCard:"Reto del día", encCard:"Deporte del día", efeCard:"Tal día como hoy", pilCard:"Píldora del día", pilSub:"Un vídeo corto del tema", open:"Abrir", efePrev:"‹ Día anterior", efeNext:"Día siguiente ›", efeToday:"Hoy", efeNone:"Todavía no hay una curiosidad para este día.", allTemas:"Ver todos los temas ›", modeWord:"Modo", searchAll:"Buscar en Historiapp"')
rep('searchAll:"Search Historiapp"','tabHome:"Home", tabTemas:"Units", tabEnc:"Encyclopedia", tabExam:"Exam", tabSet:"Settings", contTitle:"Continue", hoy:"Today", temasT:"Units", dailyCard:"Daily challenge", encCard:"Sport of the day", efeCard:"On this day", pilCard:"Clip of the day", pilSub:"A short video from the unit", open:"Open", efePrev:"‹ Previous day", efeNext:"Next day ›", efeToday:"Today", efeNone:"There is no fact for this day yet.", allTemas:"See all units ›", modeWord:"Mode", searchAll:"Search Historiapp"')

# ---------- cabecera: lupa en lugar de la rueda ----------
rep('<button class="gear" id="hGear">⚙︎</button></div>`;','<button class="srch" id="hSearch" aria-label="${esc(t("searchAll"))}">🔎</button></div>`;')
rep('const g=document.getElementById("hGear"); if(g) g.onclick=()=>nav({name:"settings",from:S.view});','const g=document.getElementById("hSearch"); if(g) g.onclick=()=>nav({name:"search",back:S.view});')

# ---------- rutas ----------
rep('if(v.name==="search") return "buscar";','if(v.name==="search") return "buscar"; if(v.name==="temas") return "temas"; if(v.name==="efe") return v.d?"hoy/"+v.d:"hoy";')
rep('if(h==="buscar") return {name:"search"};','if(h==="buscar") return {name:"search"}; if(h==="temas") return {name:"temas"}; if(h==="hoy") return {name:"efe"}; if(h.startsWith("hoy/")) return {name:"efe",d:h.slice(4)};')
rep('  if(v.name==="home") return renderHome();\n','  document.body.classList.toggle("gateon",v.name==="gate"); updateTabbar(); rememberLast(v);\n  if(v.name==="home") return renderHome();\n  if(v.name==="temas") return renderTemas();\n  if(v.name==="efe") return renderEfe();\n')

# ---------- scroll dentro de main ----------
s=s.replace('window.scrollTo(0,0)','scrollTop0()')
rep('if(el){ const top=el.getBoundingClientRect().top+window.scrollY-(document.querySelector(".top")?.offsetHeight||60)-8; window.scrollTo(0,top); } }',
    'if(el){ const mm=document.querySelector("#app main"); if(mm) mm.scrollTo(0,el.getBoundingClientRect().top-mm.getBoundingClientRect().top+mm.scrollTop-8); } }')

# ---------- celebración ----------
rep('if(after>before) setTimeout(()=>toast(t("levelUp",{n:after+1,name:t("levels")[after]}),2600),350);',
    'if(after>before) setTimeout(()=>{ toast(t("levelUp",{n:after+1,name:t("levels")[after]}),2600); celebrate(); },350);')
rep('S.prog.daily={date:todayKey(),done:true,correct,total:steps.length}; save();','S.prog.daily={date:todayKey(),done:true,correct,total:steps.length}; save(); celebrate();')

# ---------- portada nueva ----------
a=s.index('async function renderHome(){'); b=s.index('async function renderTema(')
HOME=r'''function scrollTop0(){ const m=document.querySelector("#app main"); if(m) m.scrollTo(0,0); }
function celebrate(){ try{ if(matchMedia("(prefers-reduced-motion: reduce)").matches) return; const c=document.createElement("div"); c.className="confetti"; const col=["#004379","#EDAB00","#FBAE40","#002060","#7fb2e5"]; for(let i=0;i<26;i++){ const e=document.createElement("i"); e.style.left=(Math.random()*100)+"%"; e.style.background=col[i%col.length]; e.style.animationDelay=(Math.random()*.35)+"s"; e.style.transform="rotate("+(Math.random()*180)+"deg)"; c.appendChild(e); } document.body.appendChild(c); setTimeout(()=>c.remove(),2100); }catch(e){} }
const TABS=[["home","🏠","tabHome"],["temas","📚","tabTemas"],["enc","📖","tabEnc"],["exam","🎓","tabExam"],["settings","⚙️","tabSet"]];
function tabOf(v){ const n=(v||{}).name; if(n==="tema"||n==="mode"||n==="temas") return "temas"; if(n==="enc") return "enc"; if(n==="exam") return "exam"; if(n==="settings") return "settings"; return "home"; }
function updateTabbar(){ let tb=document.getElementById("tabbar"); if(!tb){ tb=document.createElement("nav"); tb.id="tabbar"; document.body.appendChild(tb); }
  const cur=tabOf(S.view); tb.innerHTML=TABS.map(([k,i,l])=>`<button data-k="${k}" class="${k===cur?"on":""}" aria-current="${k===cur?"page":"false"}"><span class="i">${i}</span>${esc(t(l))}</button>`).join("");
  tb.querySelectorAll("button").forEach(b=>b.onclick=()=>{ const k=b.dataset.k; nav(k==="settings"?{name:"settings",from:{name:"home"}}:{name:k}); }); }
function rememberLast(v){ if(!v) return; if(v.name==="mode"||v.name==="tema"||(v.name==="enc"&&v.id)){ S.prog.last={name:v.name,num:v.num,mode:v.mode,f:v.f,id:v.id,sec:v.sec,at:Date.now()}; save(); } }
function dayHash(k){ let h=7; for(const c of k) h=(h*31+c.charCodeAt(0))>>>0; return h; }
async function getEfe(){ if(S.efe===undefined){ try{ S.efe=await fetch("data/efemerides.json",{cache:"no-cache"}).then(r=>r.ok?r.json():null); }catch(e){ S.efe=null; } } return S.efe; }
function mmdd(d){ return String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0"); }
function fmtDay(k){ const [m,d]=k.split("-").map(Number); return new Date(2024,m-1,d).toLocaleDateString(S.lang==="en"?"en-GB":"es-ES",{day:"numeric",month:"long"}); }
function ringSVG(p){ const r=18,c=2*Math.PI*r; return `<svg viewBox="0 0 44 44"><circle cx="22" cy="22" r="${r}" fill="rgba(0,0,0,.35)" stroke="rgba(255,255,255,.3)" stroke-width="4"/><circle cx="22" cy="22" r="${r}" fill="none" stroke="#EDAB00" stroke-width="4" stroke-linecap="round" stroke-dasharray="${(c*p/100).toFixed(1)} ${c.toFixed(1)}"/></svg><span>${p}%</span>`; }
const TEMA_IMG={1:"img/t1/valltorta_caza.jpg",2:"img/t2/hatshepsut_hebsed.jpg"};
function temaPct(num){ const tm=S.temaCache[num]; if(!tm) return 0; return Math.round(MODES.filter(x=>!MEDIA.includes(x)).reduce((a,x)=>a+modePct(tm,x),0)/(MODES.length-MEDIA.length)); }
async function fillTemaGrid(box,short){
  try{ const idx=await getIndex(); box.innerHTML=""; let locked=0;
    for(const m of idx.temas){ if(short&&!m.available&&++locked>2) break; const b=document.createElement("button"); const ttl=esc(L(m.title))||t("tema")+" "+m.num;
      if(m.available){ b.className="tcard"; if(TEMA_IMG[m.num]) b.style.backgroundImage=`url('${TEMA_IMG[m.num]}')`;
        b.innerHTML=`<div class="ring">${ringSVG(temaPct(m.num))}</div><div class="tx"><small>${t("tema")} ${m.num}</small><b>${ttl}</b></div>`;
        b.onclick=()=>nav({name:"tema",num:m.num});
        if(!S.temaCache[m.num]) getTema(m.num).then(()=>{ const r=b.querySelector(".ring"); if(r) r.innerHTML=ringSVG(temaPct(m.num)); }).catch(()=>{});
      } else { b.className="tcard locked"; b.innerHTML=`<div class="big">${m.num}</div><div class="lk" aria-label="${esc(t("soon"))}">🔒</div><div class="tx"><small>${t("tema")} ${m.num} · ${t("soon")}</small><b>${ttl}</b></div>`; b.onclick=()=>toast(t("locked"),2200); }
      box.appendChild(b); }
  }catch(e){ box.innerHTML=`<div class="empty">${t("loadError")}</div>`; }
}
async function renderHome(){
  const lvl=levelOf(S.prog.xp), nextXP=LEVEL_XP[lvl+1]||LEVEL_XP[lvl], prevXP=LEVEL_XP[lvl];
  const pct=LEVEL_XP[lvl+1]?Math.round((S.prog.xp-prevXP)/(nextXP-prevXP)*100):100;
  const nb=Object.keys(S.prog.badges||{}).length;
  app.innerHTML=header("Historiapp",false)+`<main>
    <div class="strip"><span class="st" title="${esc(t("days"))}">🔥 ${S.prog.streak}</span><span class="st">⭐ ${S.prog.xp}</span><span class="st">🏅 ${nb}</span>
      <div class="lv"><b>${t("level")} ${lvl+1} · ${esc(t("levels")[lvl])}</b><div class="bar"><i style="width:${pct}%"></i></div></div></div>
    <div id="contBox"></div>
    <div class="section-title">${t("hoy")}</div>
    <div class="hoy" id="hoy"></div>
    <div class="section-title">${t("temasT")}</div>
    <div class="tgrid" id="tgrid"></div>
    <button class="tema" id="allT" style="justify-content:center;font-weight:700;color:var(--primary)">${t("allTemas")}</button>
    <p style="font-size:12px;color:var(--muted);text-align:center;margin-top:10px">${t("author")}</p></main>`;
  bindHeader();
  const hoy=document.getElementById("hoy");
  const d=S.prog.daily||{}; const done=d.date===todayKey()&&d.done;
  const rc=document.createElement("button"); rc.className="card reto";
  rc.innerHTML=`<small>☀️ ${t("dailyCard")}</small><b>${done?t("dailyScore",{a:d.correct,b:d.total}):t("daily")}</b><span>${t("dailySub")}</span><div class="ft"><span>${done?"✓":"×2 XP"}</span><span>›</span></div>`;
  rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc);
  fillTemaGrid(document.getElementById("tgrid"),true); document.getElementById("allT").onclick=()=>nav({name:"temas"});
  // continuar
  (async()=>{ const l=S.prog.last, box=document.getElementById("contBox"); if(!l||!box) return; let label="", sub="";
    try{ if(l.name==="enc"){ const D=await getEnc(); const e=D.entries.find(x=>x.id===l.id); if(!e) return; label=L(e.name); sub=t("enc"); }
      else { const tm=await getTema(l.num); sub=t("tema")+" "+l.num; if(l.name==="tema") label=L(tm.title); else if(l.mode==="fichas"&&l.f){ const f=(tm.fichas||[]).find(x=>x.id===l.f); label=f?L(f.title):t("modes.fichas"); } else label=t("modes."+l.mode); }
    }catch(e){ return; }
    if(!document.getElementById("contBox")) return;
    box.innerHTML=`<button class="cont" id="contBtn"><div class="pl">▶</div><div><small>${t("contTitle")} · ${esc(sub)}</small><b>${esc(label)}</b></div></button>`;
    document.getElementById("contBtn").onclick=()=>{ const v={name:l.name,num:l.num,mode:l.mode,f:l.f,id:l.id,sec:l.sec}; Object.keys(v).forEach(k=>v[k]===undefined&&delete v[k]); nav(v); }; })();
  // deporte del día
  try{ const D=await getEnc(); const E=D.entries; if(E.length&&document.getElementById("hoy")===hoy){ const e=encDaily(E); const c=document.createElement("div"); c.className="card";
    c.innerHTML=`<small>🏅 ${t("encCard")}</small><b>${esc(L(e.name))}</b><span>${md(L(e.cuando))}</span><div class="ft"><button class="dice" aria-label="${esc(t("encRand"))}">🎲</button><span>${t("open")} ›</span></div>`;
    c.onclick=ev=>{ if(ev.target.closest(".dice")){ const r=encRandom(E); nav({name:"enc",id:r.id,back:{name:"home"}}); } else nav({name:"enc",id:e.id,back:{name:"home"}}); };
    c.style.cursor="pointer"; hoy.appendChild(c); } }catch(e){}
  // tal día como hoy
  try{ const F=await getEfe(); const k=mmdd(new Date()); if(F&&F[k]&&document.getElementById("hoy")===hoy){ const f=F[k]; const c=document.createElement("button"); c.className="card";
    c.innerHTML=`<small>📅 ${t("efeCard")} · ${esc(fmtDay(k))}</small><b>${esc(String(f.year||""))}</b><span>${md(L(f))}</span><div class="ft"><span></span><span>${t("open")} ›</span></div>`;
    c.onclick=()=>nav({name:"efe"}); hoy.appendChild(c); } }catch(e){}
  // píldora del día
  try{ const idx=await getIndex(); const vids=[]; for(const m of idx.temas){ if(!m.available) continue; const tm=await getTema(m.num); (tm.videos||[]).forEach(v=>vids.push({num:m.num,v})); }
    if(vids.length&&document.getElementById("hoy")===hoy){ const p=vids[dayHash(todayKey()+"v")%vids.length]; const c=document.createElement("button"); c.className="card";
      c.innerHTML=`<small>▶ ${t("pilCard")} · ${t("tema")} ${p.num}</small><b>${esc(L(p.v.title))}</b><span>${t("pilSub")}</span><div class="ft"><span></span><span>${t("open")} ›</span></div>`;
      c.onclick=()=>nav({name:"mode",num:p.num,mode:"videos"}); hoy.appendChild(c); } }catch(e){}
}
async function renderTemas(){
  app.innerHTML=header(t("tabTemas"),false)+`<main><div class="tgrid" id="tgrid2"></div></main>`;
  bindHeader(); fillTemaGrid(document.getElementById("tgrid2"));
}
async function renderEfe(){
  const v=S.view; const k=v.d||mmdd(new Date());
  app.innerHTML=header(t("efeCard"),true)+`<main id="efeM"><div class="empty">…</div></main>`;
  bindHeader(()=>nav(v.back||{name:"home"}));
  const F=await getEfe(); const m=document.getElementById("efeM"); if(!m) return; const f=F&&F[k];
  const shift=n=>{ const [mm,dd]=k.split("-").map(Number); const d=new Date(2024,mm-1,dd+n); return mmdd(d); };
  const refs=f?((S.lang==="en"&&f.refs_en)?f.refs_en:(f.refs||[])):[];
  m.innerHTML=`<div class="efe-date">📅 ${esc(fmtDay(k))}</div>
    ${f?`<div class="efe-year">${esc(String(f.year||""))}</div><div class="efe-txt">${LL(f.body||{es:[f.es],en:[f.en]}).map(x=>`<p>${md(x)}</p>`).join("")}</div>
    ${f.enc?`<div class="enc-links"><button id="efeEnc">🔍 ${esc(t("enc"))}</button></div>`:""}
    ${refs.length?`<div class="section-title" style="margin-top:14px">${t("encRefs")}</div><div class="enc-refs">${refs.map(r=>`<p>${md(r)}</p>`).join("")}</div>`:""}`:`<div class="empty">${t("efeNone")}</div>`}
    <div class="efe-nav"><button id="efeP">${t("efePrev")}</button><button id="efeN">${t("efeNext")}</button></div>`;
  document.getElementById("efeP").onclick=()=>nav({name:"efe",d:shift(-1),back:v.back});
  document.getElementById("efeN").onclick=()=>nav({name:"efe",d:shift(1),back:v.back});
  const eb=document.getElementById("efeEnc"); if(eb) eb.onclick=()=>nav({name:"enc",id:f.enc,back:{name:"efe",d:k}});
}
'''
s=s[:a]+HOME+s[b:]
open(p,'w',encoding='utf-8').write(s)
sw=os.path.join(R,'sw.js'); w=open(sw,encoding='utf-8').read()
w=re.sub(r'historiapp-v(\d+)',lambda m:'historiapp-v%d'%(int(m.group(1))+1),w,1); open(sw,'w',encoding='utf-8').write(w)
print('ok',re.search(r'historiapp-v\d+',w).group(0))
