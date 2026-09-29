#!/usr/bin/env python3
"""Enciclopedia del deporte: botón y deporte del día en portada, dados, buscador, índice A-Z lateral y ficha ES/EN.
Datos en data/enciclopedia.json. Uso: python3 tools/patch_enciclopedia.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'function renderEnc(' in s: print('ya aplicado'); raise SystemExit
def rep(old, new):
    global s
    assert old in s, old[:70]; s = s.replace(old, new, 1)

CSS = '''.encday{display:flex;gap:10px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:12px 14px;box-shadow:var(--shadow)}
.encday .d{flex:1;text-align:left;background:none;border:0;padding:0;font:inherit;color:inherit}
.encday small{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}
.encday b{display:block;color:var(--primary-2);font-size:16px;margin:1px 0}
.encday span{display:block;font-size:13px;color:var(--muted)}
.dice{width:48px;height:48px;border-radius:14px;background:var(--accent);font-size:24px;border:0;flex-shrink:0;cursor:pointer}
.enc-wrap{padding-right:22px}
.enc-list .letter{font-weight:800;color:var(--primary);font-size:15px;margin:14px 4px 6px;padding-bottom:2px;border-bottom:2px solid var(--accent);display:inline-block}
.enc-list button{display:block;width:100%;text-align:left;background:var(--paper);border:0;border-radius:12px;padding:10px 12px;margin-bottom:6px;box-shadow:var(--shadow);cursor:pointer}
.enc-list button b{color:var(--primary-2);font-size:15px}
.enc-list button span{display:block;font-size:12.5px;color:var(--muted);margin-top:2px}
.az{position:fixed;right:2px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;z-index:15;touch-action:none;user-select:none;-webkit-user-select:none;background:rgba(255,255,255,.85);border-radius:10px;padding:4px 0}
.az a{font-size:11px;font-weight:800;color:var(--primary);padding:1px 6px;text-align:center;line-height:1.2;text-decoration:none}
.az a.off{color:#c3cbd6}
.enc-when{background:#fff8e1;border-left:4px solid var(--accent);border-radius:10px;padding:10px 12px;font-weight:700;color:var(--primary-2);margin-top:12px}
.enc-blq{font-size:12px;color:var(--muted);margin:8px 2px 0;text-transform:uppercase;letter-spacing:.05em;font-weight:700}
.enc-body p{line-height:1.55;margin:12px 0}
.enc-refs p{font-size:12.5px;color:#444;margin:6px 0;padding-left:1.4em;text-indent:-1.4em;line-height:1.4}
.enc-links{display:flex;flex-direction:column;gap:8px;margin-top:8px}
.enc-links button{text-align:left;background:#EAF1F8;color:var(--primary-2);border:0;border-radius:12px;padding:10px 12px;font-weight:700;cursor:pointer}
.enc-act{display:flex;gap:8px;margin-top:18px}
.enc-act button{flex:1;border:0;border-radius:12px;padding:12px;font-weight:700;cursor:pointer}
'''
rep('.srch-res{display:flex;', CSS + '.srch-res{display:flex;')

rep('searchAll:"Buscar en todas las fichas"', 'enc:"Enciclopedia del deporte", encSub:"Origen e historia de {n} deportes", encDay:"Deporte del día", encPh:"Busca un deporte", encN:"{n} deportes", encNone:"No hay ningún deporte con ese nombre", encRand:"🎲 Otro deporte al azar", encCourse:"En la asignatura", encRefs:"Fuentes", encGrow:"La enciclopedia crece por tandas: {n} de {t} deportes publicados.", encImg:"Imagen", searchAll:"Buscar en todas las fichas"')
rep('searchAll:"Search all study sheets"', 'enc:"Sports Encyclopedia", encSub:"Origins and history of {n} sports", encDay:"Sport of the day", encPh:"Search for a sport", encN:"{n} sports", encNone:"No sport with that name", encRand:"🎲 Another random sport", encCourse:"In the course", encRefs:"Sources", encGrow:"The encyclopedia grows in batches: {n} of {t} sports published.", encImg:"Image", searchAll:"Search all study sheets"')

# rutas
rep('if(v.name==="search") return "buscar";', 'if(v.name==="search") return "buscar"; if(v.name==="enc") return v.id?"enciclopedia/"+encodeURIComponent(v.id):"enciclopedia";')
rep('if(h==="buscar") return {name:"search"};', 'if(h==="buscar") return {name:"search"}; if(h==="enciclopedia") return {name:"enc"}; if(h.startsWith("enciclopedia/")) return {name:"enc",id:decodeURIComponent(h.slice(13))};')
rep('  if(v.name==="search") return renderSearch();\n', '  if(v.name==="search") return renderSearch();\n  if(v.name==="enc") return v.id?renderEncFicha(v.id):renderEnc();\n')

# portada
old = '''<button class="tema" id="searchBtn"><div class="num">🔎</div><div class="t"><b>${t("searchAll")}</b><span>${t("searchAllSub")}</span></div><div class="pct">›</div></button>\n'''
rep(old, old + '''    <button class="tema" id="encBtn"><div class="num" style="background:var(--primary);color:#fff">📚</div><div class="t"><b>${t("enc")}</b><span id="encSub">${t("encSub",{n:"…"})}</span></div><div class="pct">›</div></button>
    <div class="encday" id="encDay" style="display:none"></div>\n''')
rep('document.getElementById("searchBtn").onclick=()=>nav({name:"search"});', 'document.getElementById("searchBtn").onclick=()=>nav({name:"search"}); document.getElementById("encBtn").onclick=()=>nav({name:"enc"}); encHome();')

JS = r'''
/* --- enciclopedia del deporte --- */
async function getEnc(){ if(!S.enc){ S.enc=await fetch("data/enciclopedia.json",{cache:"no-cache"}).then(r=>r.json()); } return S.enc; }
function encSorted(D){ return D.entries.slice().sort((a,b)=>L(a.name).localeCompare(L(b.name),S.lang)); }
function encDaily(E){ const k=todayKey(); let h=7; for(const c of k) h=(h*31+c.charCodeAt(0))>>>0; const A=E.slice().sort((a,b)=>a.id<b.id?-1:1); return A[h%A.length]; }
function encRandom(E,not){ if(E.length<2) return E[0]; let e; do{ e=E[Math.floor(Math.random()*E.length)]; }while(e.id===not); return e; }
function encLetter(e){ const c=norm(L(e.name)).replace(/[^a-z0-9]/g,"")[0]||"#"; return /[a-z]/.test(c)?c.toUpperCase():"#"; }
async function encHome(){
  try{ const D=await getEnc(); const E=D.entries; if(!E.length) return;
    const sub=document.getElementById("encSub"); if(sub) sub.textContent=t("encSub",{n:E.length});
    const box=document.getElementById("encDay"); if(!box) return; const d=encDaily(E);
    box.innerHTML=`<button class="d" id="encDayGo"><small>${t("encDay")}</small><b>${esc(L(d.name))}</b><span>${md(L(d.cuando))}</span></button><button class="dice" id="encDice" aria-label="${esc(t("encRand"))}">🎲</button>`;
    box.style.display="flex";
    document.getElementById("encDayGo").onclick=()=>nav({name:"enc",id:d.id,back:{name:"home"}});
    document.getElementById("encDice").onclick=()=>{ const r=encRandom(E); nav({name:"enc",id:r.id,back:{name:"home"}}); };
  }catch(e){}
}
async function renderEnc(){
  const q0=S.view.q||"";
  app.innerHTML=header(t("enc"),true)+`<main><div class="enc-wrap">
    <div style="display:flex;gap:8px"><input class="search" id="eq" type="search" placeholder="${t("encPh")}" autocomplete="off" value="${esc(q0)}" style="flex:1"><button class="dice" id="eDice" aria-label="${esc(t("encRand"))}">🎲</button></div>
    <div class="counter" id="ecount" style="margin-top:8px">…</div><div class="enc-list" id="elist"></div>
    <p class="counter" id="egrow" style="margin-top:14px;font-weight:400"></p></div></main><nav class="az" id="az"></nav>`;
  bindHeader(()=>nav({name:"home"}));
  let D; try{ D=await getEnc(); }catch(e){ app.querySelector("main").innerHTML=`<div class="empty">${t("loadError")}</div>`; return; }
  const E=encSorted(D), inp=document.getElementById("eq"), list=document.getElementById("elist"), cnt=document.getElementById("ecount"), az=document.getElementById("az");
  if(!inp) return;
  document.getElementById("egrow").textContent=t("encGrow",{n:E.length,t:D.total||E.length});
  document.getElementById("eDice").onclick=()=>{ const r=encRandom(E); nav({name:"enc",id:r.id,back:{name:"enc",q:inp.value.trim()}}); };
  const LET="ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  function paint(){
    const raw=inp.value.trim(), qq=norm(raw); list.innerHTML="";
    const out=E.filter(e=>!qq||norm(e.name.es+" "+e.name.en+" "+L(e.cuando)).includes(qq));
    cnt.textContent=out.length?t("encN",{n:out.length}):t("encNone");
    let last=""; const have=new Set();
    for(const e of out){ const l=encLetter(e); if(l!==last){ const h=document.createElement("div"); h.className="letter"; h.id="L-"+l; h.textContent=l; list.appendChild(h); last=l; have.add(l); }
      const b=document.createElement("button"); b.innerHTML=`<b>${esc(L(e.name))}</b><span>${md(L(e.cuando))}</span>`;
      b.onclick=()=>nav({name:"enc",id:e.id,back:{name:"enc",q:raw}}); list.appendChild(b); }
    az.style.display=qq?"none":"flex";
    az.innerHTML=LET.map(l=>`<a data-l="${l}" class="${have.has(l)?"":"off"}">${l}</a>`).join("");
    S.view.q=raw;
  }
  function jump(l){ let el=document.getElementById("L-"+l); if(!el){ const i=LET.indexOf(l); for(let j=i+1;j<LET.length&&!el;j++) el=document.getElementById("L-"+LET[j]); for(let j=i-1;j>=0&&!el;j--) el=document.getElementById("L-"+LET[j]); }
    if(el){ const top=el.getBoundingClientRect().top+window.scrollY-(document.querySelector(".top")?.offsetHeight||60)-8; window.scrollTo(0,top); } }
  function fromTouch(ev){ const p=ev.touches?ev.touches[0]:ev; const el=document.elementFromPoint(p.clientX,p.clientY); if(el&&el.dataset&&el.dataset.l) jump(el.dataset.l); }
  az.addEventListener("touchstart",e=>{ e.preventDefault(); fromTouch(e); },{passive:false});
  az.addEventListener("touchmove",e=>{ e.preventDefault(); fromTouch(e); },{passive:false});
  az.addEventListener("click",fromTouch);
  let tmr=null; inp.oninput=()=>{ clearTimeout(tmr); tmr=setTimeout(paint,150); }; paint();
}
async function renderEncFicha(id){
  const v=S.view; let D; try{ D=await getEnc(); }catch(e){ D={entries:[]}; }
  const e=D.entries.find(x=>x.id===id); if(!e){ nav({name:"enc"}); return; }
  const im=e.img||{}, refs=(S.lang==="en"&&e.refs_en)?e.refs_en:(e.refs||[]);
  const LX=x=>x&&typeof x==="object"?L(x):x; const lic=[LX(im.autor),LX(im.licencia)].filter(Boolean).map(esc).join(" · ");
  app.innerHTML=header(L(e.name),true)+`<main>
    ${im.src?`<div class="fimg" id="eImg"><img src="${esc(im.src)}" alt="${esc(L(e.name))}" loading="lazy"><div class="cap">${md(L(im.pie))}${lic?`<br>${lic}${im.url?` · <a href="${esc(im.url)}" target="_blank" rel="noopener">Wikimedia Commons</a>`:""}`:""}</div></div>`:""}
    <div class="enc-when">🕰️ ${md(L(e.cuando))}</div>
    <div class="enc-blq">${esc(L(e.bloque))}</div>
    <div class="enc-body">${LL(e.body).map(x=>`<p>${md(x)}</p>`).join("")}</div>
    ${(e.tema&&e.tema.length)?`<div class="section-title" style="margin-top:14px">${t("encCourse")}</div><div class="enc-links">${e.tema.map((x,j)=>`<button data-j="${j}">📖 ${t("tema")} ${x.num} · ${esc(L(x.t))}</button>`).join("")}</div>`:""}
    ${refs.length?`<div class="section-title" style="margin-top:16px">${t("encRefs")}</div><div class="enc-refs">${refs.map(r=>`<p>${md(r)}</p>`).join("")}</div>`:""}
    <div class="enc-act"><button id="eRand" style="background:var(--accent);color:var(--primary-2)">${t("encRand")}</button></div>
    <div class="enc-act" style="margin-top:8px"><button id="eRep" style="background:#F1F3F6;color:var(--muted)">${t("report")}</button></div>
  </main>`;
  bindHeader(()=>nav(v.back||{name:"enc"}));
  document.querySelectorAll(".enc-links button").forEach(b=>b.onclick=()=>{ const x=e.tema[+b.dataset.j]; nav({name:"mode",num:x.num,mode:"fichas",f:x.f,back:{name:"enc",id:e.id,back:v.back}}); });
  document.getElementById("eRand").onclick=()=>{ const r=encRandom(D.entries,e.id); nav({name:"enc",id:r.id,back:v.back}); };
  document.getElementById("eRep").onclick=()=>reportMail({where:t("enc")+" · "+L(e.name),text:LL(e.body)[0]||""});
  const ei=document.getElementById("eImg"); if(ei) ei.querySelector("img").onclick=()=>{ const lb=document.createElement("div"); lb.className="lightbox"; lb.innerHTML=`<img src="${esc(im.src)}" alt=""><div class="cap">${md(L(im.pie))}</div>`; lb.onclick=()=>lb.remove(); document.body.appendChild(lb); };
}
'''
rep('\n/* --- avisar de un error --- */', JS + '\n/* --- avisar de un error --- */')
open(p, 'w', encoding='utf-8').write(s)
sw = os.path.join(R, 'sw.js'); w = open(sw, encoding='utf-8').read()
import re
w = re.sub(r'historiapp-v(\d+)', lambda m: 'historiapp-v%d' % (int(m.group(1)) + 1), w, 1)
open(sw, 'w', encoding='utf-8').write(w)
print('ok', re.search(r'historiapp-v\d+', w).group(0))
