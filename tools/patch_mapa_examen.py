#!/usr/bin/env python3
# Añade a Historiapp la sección «Mapa» (por tema) y la guía «Cómo preparar el examen».
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

# ---- datos ----
mapas = json.load(open('tools/mapas.json'))
for n, mp in mapas.items():
    p = f'data/tema{int(n):02d}.json'
    d = json.load(open(p))
    d['mapa'] = mp
    json.dump(d, open(p, 'w'), ensure_ascii=False, separators=(',', ':'))
ex = json.load(open('tools/examen.json'))
json.dump(ex, open('data/examen.json', 'w'), ensure_ascii=False, separators=(',', ':'))

s = open('index.html', encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, old[:80]
    s = s.replace(old, new, count)

# ---- CSS ----
css = """
/* mapa conceptual */
.mtools{display:flex;gap:8px;justify-content:flex-end;margin-bottom:10px}
.mtools button{font-size:12px;font-weight:700;color:var(--primary);background:var(--ok-bg);border-radius:999px;padding:7px 12px}
.mroot{background:linear-gradient(135deg,var(--primary),var(--primary-2));color:#fff;border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow);position:relative}
.mroot .k{font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.75;font-weight:700}
.mroot h2{font-size:19px;margin:4px 0 8px;color:#fff}
.mroot p{font-size:14px;line-height:1.5;opacity:.95}
.mtree{position:relative;margin-left:14px;padding-left:18px;border-left:3px solid var(--line);padding-top:14px}
.rama{position:relative;margin-bottom:14px}
.rama:before{content:"";position:absolute;left:-21px;top:24px;width:18px;border-top:3px solid var(--line)}
.rama>.rh{display:block;width:100%;text-align:left;background:var(--paper);border:1px solid var(--line);border-left:6px solid var(--rc);border-radius:14px;padding:12px 14px;box-shadow:var(--shadow)}
.rama>.rh .code{display:inline-block;font-size:11px;font-weight:800;color:#fff;background:var(--rc);border-radius:6px;padding:2px 7px;margin-right:6px}
.rama>.rh b{font-size:15px;line-height:1.3}
.rama>.rh p{font-size:13.5px;color:var(--ink);line-height:1.45;margin-top:6px}
.rama>.rh .chev{float:right;font-size:14px;color:var(--muted);transition:transform .2s}
.rama.open>.rh .chev{transform:rotate(90deg)}
.nodos{display:none;margin:8px 0 0 12px;padding-left:16px;border-left:2px dashed var(--rc)}
.rama.open>.nodos{display:block}
.nodo{position:relative;margin-top:8px}
.nodo:before{content:"";position:absolute;left:-17px;top:18px;width:14px;border-top:2px dashed var(--rc)}
.nodo>button.nh{display:flex;align-items:center;gap:8px;width:100%;text-align:left;background:var(--paper);border:1.5px solid var(--rc);border-radius:12px;padding:9px 12px;font-weight:700;font-size:14px}
.nodo>button.nh i{width:9px;height:9px;border-radius:50%;background:var(--line);flex-shrink:0}
.nodo.seen>button.nh i{background:var(--rc)}
.nodo .nd{display:none;background:var(--paper);border:1.5px solid var(--rc);border-top:0;border-radius:0 0 12px 12px;margin-top:-6px;padding:12px;font-size:14px;line-height:1.5}
.nodo.open>button.nh{border-radius:12px 12px 0 0}
.nodo.open .nd{display:block}
.nd .acts{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.nd .acts button{font-size:12.5px;font-weight:700;border-radius:999px;padding:7px 12px;background:var(--ok-bg);color:var(--primary)}
/* examen */
.xsec{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}
.xsec>summary{list-style:none;display:flex;align-items:center;gap:12px;padding:14px 16px;cursor:pointer;font-weight:800;font-size:16px;color:var(--primary-2)}
.xsec>summary::-webkit-details-marker{display:none}
.xsec>summary .ic{font-size:22px}
.xsec>summary:after{content:"›";margin-left:auto;font-size:22px;color:var(--muted);transition:transform .2s}
.xsec[open]>summary:after{transform:rotate(90deg)}
.xsec .xb{padding:0 16px 16px;font-size:14.5px;line-height:1.55}
.xsec .xb p{margin-bottom:10px}
.xtab{width:100%;border-collapse:collapse;font-size:13px;margin:6px 0 12px}
.xtab th{background:var(--primary);color:#fff;text-align:left;padding:7px 8px;font-weight:700}
.xtab td{border-bottom:1px solid var(--line);padding:7px 8px;vertical-align:top}
.xtab td:last-child,.xtab th:last-child{text-align:right;white-space:nowrap}
.xnote{background:#fff8e1;border-left:4px solid var(--accent);border-radius:10px;padding:10px 12px;font-size:13.5px;margin:4px 0 12px}
.xtips{margin:4px 0 0;padding:0;list-style:none}
.xtips li{position:relative;padding-left:22px;margin-bottom:7px;font-size:14px}
.xtips li:before{content:"✓";position:absolute;left:0;color:var(--primary);font-weight:800}
.xstep{display:flex;gap:12px;margin:10px 0}
.xstep .k{flex-shrink:0;width:42px;height:42px;border-radius:12px;background:var(--primary);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;flex-direction:column;font-size:14px;line-height:1}
.xstep .k small{font-size:10px;font-weight:600;opacity:.85;margin-top:2px}
.xstep b{display:block;font-size:14.5px;margin-bottom:2px}
.xex{background:var(--ok-bg);border-radius:12px;padding:12px;margin:10px 0 12px;font-size:13.5px}
.xex h4{font-size:13px;margin:0 0 6px;color:var(--primary-2)}
.xex p{margin-bottom:8px}
.xex img{width:100%;border-radius:8px;margin-bottom:8px;display:block}
.xphase{position:relative;padding:0 0 12px 22px;border-left:3px solid var(--accent);margin-left:6px}
.xphase:before{content:"";position:absolute;left:-8px;top:2px;width:13px;height:13px;border-radius:50%;background:var(--accent)}
.xphase b{display:block;font-size:14.5px;margin-bottom:3px}
.xcheck label{display:flex;gap:10px;align-items:flex-start;padding:9px 0;border-bottom:1px solid var(--line);font-size:14.5px}
.xcheck input{width:20px;height:20px;accent-color:var(--primary);flex-shrink:0;margin-top:1px}
"""
rep(".empty{text-align:center;", css.strip() + "\n.empty{text-align:center;")

# ---- i18n ----
rep('modes:{fichas:"Fichas",', 'modes:{fichas:"Fichas",mapa:"Mapa",')
rep('modesSub:{fichas:"El manual de bolsillo, por apartados",', 'modesSub:{fichas:"El manual de bolsillo, por apartados",mapa:"Ideas principales y secundarias del tema",')
rep('modes:{fichas:"Study sheets",', 'modes:{fichas:"Study sheets",mapa:"Map",')
rep('modesSub:{fichas:"The pocket manual, by section",', 'modesSub:{fichas:"The pocket manual, by section",mapa:"Main and secondary ideas of the unit",')
rep('badgeName:{fichas:"Lector",', 'badgeName:{fichas:"Lector",mapa:"Cartógrafo",')
rep('badgeName:{fichas:"Reader",', 'badgeName:{fichas:"Reader",mapa:"Cartographer",')
rep('daily:"Reto del día"', 'daily:"Reto del día", exam:"Cómo preparar el examen", examSub:"Test, desarrollo y comentario de imagen, paso a paso", mapOpen:"Desplegar todo", mapClose:"Plegar todo", mapTema:"Tema {n}", mapFicha:"📖 Leer la ficha", mapPractice:"⚡ Practicar este apartado", mapHint:"Toca cada apartado para ver sus ideas y cada idea para leer el detalle."')
rep('daily:"Daily challenge"', 'daily:"Daily challenge", exam:"How to prepare for the exam", examSub:"Multiple choice, essay and image commentary, step by step", mapOpen:"Expand all", mapClose:"Collapse all", mapTema:"Unit {n}", mapFicha:"📖 Read the study sheet", mapPractice:"⚡ Practise this section", mapHint:"Tap each section to see its ideas and each idea to read the detail."')

# ---- modos ----
rep('const MODE_ICONS={fichas:"📖",', 'const MODE_ICONS={fichas:"📖",mapa:"🧭",')
rep('const MODES=["fichas","cards",', 'const MODES=["fichas","mapa","cards",')
rep('function modeTotal(tema,mode){ if(mode==="glossary") return tema.glossary.length;',
    'function modeTotal(tema,mode){ if(mode==="glossary") return tema.glossary.length; if(mode==="mapa") return tema.mapa?tema.mapa.ramas.reduce((a,r)=>a+r.nodos.length,0):0;')
rep('  if(mode==="fichas") return modeFichas(tema,m,v);\n',
    '  if(mode==="fichas") return modeFichas(tema,m,v);\n  if(mode==="mapa") return modeMapa(tema,m,v);\n')

# ---- rutas ----
rep('if(v.name==="daily") return "reto";', 'if(v.name==="daily") return "reto"; if(v.name==="exam") return "examen";')
rep('if(h==="reto") return {name:"daily"};', 'if(h==="reto") return {name:"daily"}; if(h==="examen") return {name:"exam"};')
rep('  if(v.name==="daily") return renderDaily();\n', '  if(v.name==="daily") return renderDaily();\n  if(v.name==="exam") return renderExam();\n')

# ---- botón en portada ----
rep('<div id="temaList">', '<button class="tema" id="examBtn" style="border:2px solid var(--primary)"><div class="num" style="background:var(--primary);color:#fff">🎓</div><div class="t"><b>${t("exam")}</b><span>${t("examSub")}</span></div><div class="pct">›</div></button>\n    <div id="temaList">')
rep('document.getElementById("dailyBtn").onclick=()=>nav({name:"daily"});', 'document.getElementById("dailyBtn").onclick=()=>nav({name:"daily"}); document.getElementById("examBtn").onclick=()=>nav({name:"exam"});')

# ---- funciones ----
js = r'''
/* --- mapa conceptual --- */
const MAP_COLORS=["#004379","#C77700","#2F6DB5","#8A5A00"];
function modeMapa(tema,m,v){
  const mp=tema.mapa; if(!mp){ m.innerHTML=`<div class="empty"><div class="ic">🧭</div>${t("soon")}</div>`; return; }
  const seen=S.prog.seen[tema.id+".mapa"]||{};
  m.innerHTML=`<div class="mtools"><button id="mAll">${t("mapOpen")}</button><button id="mNone">${t("mapClose")}</button></div>
  <div class="mroot"><div class="k">${t("mapTema",{n:tema.num})}</div><h2>${esc(L(tema.title))}</h2><p>${md(L(mp.tesis))}</p></div>
  <div class="mtree">${mp.ramas.map((r,ri)=>`<div class="rama" style="--rc:${MAP_COLORS[ri%MAP_COLORS.length]}" data-r="${ri}">
    <button class="rh"><span class="chev">›</span><span class="code">${esc(r.code)}</span><b>${esc(L(r.t))}</b><p>${md(L(r.idea))}</p></button>
    <div class="nodos">${r.nodos.map((n,ni)=>{const key=r.code+"."+ni;return `<div class="nodo ${seen[key]?"seen":""}" data-k="${key}">
      <button class="nh"><i></i>${esc(L(n.t))}</button>
      <div class="nd">${md(L(n.d))}<div class="acts">${n.f?`<button data-f="${esc(n.f)}">${t("mapFicha")}</button>`:""}<button data-s="${esc(n.sec||r.code)}">${t("mapPractice")}</button></div></div></div>`}).join("")}</div></div>`).join("")}</div>
  <p style="font-size:12px;color:var(--muted);text-align:center;margin-top:6px">${t("mapHint")}</p>`;
  m.querySelectorAll(".rama>.rh").forEach(b=>b.onclick=()=>b.parentElement.classList.toggle("open"));
  m.querySelectorAll(".nodo>.nh").forEach(b=>b.onclick=()=>{ const n=b.parentElement; n.classList.toggle("open");
    const k=n.dataset.k; if(!seen[k]){ seen[k]=1; markSeen(tema.id,"mapa",k); n.classList.add("seen"); addXP(2); checkBadge(tema,"mapa"); } });
  m.querySelectorAll(".nd [data-f]").forEach(b=>b.onclick=()=>nav({name:"mode",num:tema.num,mode:"fichas",f:b.dataset.f,back:{name:"mode",num:tema.num,mode:"mapa"}}));
  m.querySelectorAll(".nd [data-s]").forEach(b=>b.onclick=()=>nav({name:"mode",num:tema.num,mode:"quiz",sec:b.dataset.s,back:{name:"mode",num:tema.num,mode:"mapa"}}));
  document.getElementById("mAll").onclick=()=>m.querySelectorAll(".rama").forEach(r=>r.classList.add("open"));
  document.getElementById("mNone").onclick=()=>m.querySelectorAll(".rama,.nodo").forEach(r=>r.classList.remove("open"));
}

/* --- cómo preparar el examen --- */
async function renderExam(){
  app.innerHTML=header(t("exam"),true)+`<main><div class="empty">…</div></main>`;
  bindHeader(()=>nav({name:"home"}));
  let X; try{ X=S.examCache||(S.examCache=await fetch("data/examen.json").then(r=>r.json())); }catch(e){ app.querySelector("main").innerHTML=`<div class="empty">${t("loadError")}</div>`; return; }
  const G=X[S.lang]||X.es, ck=S.prog.examCheck||(S.prog.examCheck={});
  const tab=tb=>`<table class="xtab"><tr>${tb.cab.map(c=>`<th>${esc(c)}</th>`).join("")}</tr>${tb.filas.map(f=>`<tr>${f.map(c=>`<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</table>`;
  const sec=(s,i)=>`<details class="xsec" ${i===0?"open":""}><summary><span class="ic">${s.ic}</span>${esc(s.h)}</summary><div class="xb">
    ${(s.p||[]).map(p=>`<p>${md(p)}</p>`).join("")}
    ${s.tabla?tab(s.tabla):""}
    ${s.aviso?`<div class="xnote">${md(s.aviso)}</div>`:""}
    ${(s.pasos||[]).map(p=>`<div class="xstep"><div class="k">${esc(p.k)}<small>${esc(p.pts)}</small></div><div><b>${esc(p.t)}</b>${md(p.d)}</div></div>`).join("")}
    ${s.ejemplo?`<div class="xex"><h4>${esc(s.ejemplo.h)}</h4><img src="img/t2/justa_pescadores.jpg" alt="" loading="lazy" onerror="this.remove()">${s.ejemplo.p.map(p=>`<p>${md(p)}</p>`).join("")}</div>`:""}
    ${(s.fases||[]).map(f=>`<div class="xphase"><b>${esc(f.t)}</b>${md(f.d)}</div>`).join("")}
    ${s.consejos?`<ul class="xtips">${s.consejos.map(c=>`<li>${md(c).replace(/<em>/g,"<b>").replace(/<\/em>/g,"</b>")}</li>`).join("")}</ul>`:""}
  </div></details>`;
  app.querySelector("main").innerHTML=`<div class="card" style="padding:14px 16px"><h2 style="font-size:20px">${esc(G.title)}</h2><p style="font-size:14.5px;line-height:1.55;margin-top:6px">${md(G.lead)}</p></div>
    ${G.secciones.map(sec).join("")}
    <div class="card xcheck"><div class="section-title" style="margin:0 0 4px">${esc(G.check.h)}</div>${G.check.items.map((it,i)=>`<label><input type="checkbox" data-i="${i}" ${ck[i]?"checked":""}><span>${esc(it)}</span></label>`).join("")}</div>`;
  app.querySelectorAll(".xcheck input").forEach(c=>c.onchange=()=>{ ck[c.dataset.i]=c.checked?1:0; S.prog.examCheck=ck; save(); });
}
'''
rep('/* --- videos --- */', js.strip() + '\n\n/* --- videos --- */')

# md(): los ** de negrita
if 'replace(/\\*\\*([^*]+)\\*\\*/g' not in s:
    rep('function md(s){ return esc(s).replace(/\\*([^*]+)\\*/g,"<em>$1</em>")',
        'function md(s){ return esc(s).replace(/\\*\\*([^*]+)\\*\\*/g,"<b>$1</b>").replace(/\\*([^*]+)\\*/g,"<em>$1</em>")')

open('index.html', 'w', encoding='utf-8').write(s)

sw = open('sw.js').read()
sw = re.sub(r'historiapp-v\d+', 'historiapp-v8', sw)
open('sw.js', 'w').write(sw)
print('ok')
