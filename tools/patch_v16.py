#!/usr/bin/env python3
"""v16: «Avisar de un error» (fichas y preguntas), buscador en todas las fichas,
fichas relacionadas en el mapa y correcciones del mapa del Tema 2.
Uso: python3 tools/patch_v16.py   (después: python3 tools/patch_mapa_nivel3.py)"""
import json, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EMAIL = 'aleiva@ucam.edu'

# ---------- datos ----------
FS = {  # nodo del mapa -> fichas relacionadas (la primera es la principal)
    '2.1.4': ['los-deportes-de-combate', 'beni-hasan-registros-de-lucha', 'esgrima-y-combate-en-medinet-habu', 'la-carrera-de-fondo'],
    '2.2.4': ['pahlavan-periodo-arabe', 'zurkhaneh-periodo-arabe-en-adelante', 'la-sesion'],
    '2.2.5': ['chovgan', 'el-chovgan-como-adiestramiento-belico', 'jereed', 'buzkashi'],
    '2.3.1': ['remar', 'un-acercamiento-desde-la-arqueologia-exp', 'los-pecios-de-mazarron'],
}
D = {
    '2.2.4': {'es': 'El pahlavan, luchador profesional de la ciudad islámica, vive de su cuerpo y entrena en la casa de fuerza, de la que no hay pruebas claras antes del siglo XVII (Krawietz, 2013).',
              'en': 'The pahlavan, a professional wrestler of the Islamic city, lives off his body and trains in the house of strength, for which there is no clear evidence before the seventeenth century (Krawietz, 2013).'},
    '2.3.1': {'es': 'Remar es el esfuerzo físico mejor documentado; la arqueología experimental permite medirlo y los pecios de Mazarrón muestran los barcos de cabotaje de la época.',
              'en': 'Rowing is the best-documented physical effort; experimental archaeology makes it measurable and the Mazarrón wrecks show the coastal boats of the period.'},
}
def fix_mapa(mapa):
    for r in mapa['ramas']:
        for i, n in enumerate(r['nodos']):
            k = f"{r['code']}.{i}"
            if k in FS: n['fs'] = FS[k]; n['f'] = FS[k][0]
            if k in D: n['d'] = D[k]
M = json.load(open(os.path.join(R, 'tools', 'mapas.json')))
fix_mapa(M['2']); json.dump(M, open(os.path.join(R, 'tools', 'mapas.json'), 'w'), ensure_ascii=False, indent=1)
for num in (1, 2):
    p = os.path.join(R, 'data', f'tema{num:02d}.json'); t = json.load(open(p))
    if num == 2: fix_mapa(t['mapa'])
    for f in t['fichas']:  # restos de diapositivas de transición pegados al final de una ficha
        for L in ('es', 'en'):
            f['body'][L] = [x for x in f['body'].get(L, []) if not re.match(r'^(Diapositiva de transición|Transition slide)', x)]
    json.dump(t, open(p, 'w'), ensure_ascii=False, indent=1)

# ---------- index.html ----------
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'function reportMail' in s:
    print('ya aplicado'); raise SystemExit

ES = ('searchAll:"Buscar en todas las fichas", searchAllSub:"Conceptos, autores, fechas y lugares de todos los temas", searchPh:"Escribe al menos 3 letras", '
      'searchN:"{n} fichas encontradas", searchNone:"No hay fichas con esa palabra", searchLoading:"Cargando los temas…", '
      'report:"⚑ Avisar de un error", reportHint:"Se abrirá tu correo con el mensaje preparado para el profesor.", reportWrite:"Explica aquí el error:", ')
EN = ('searchAll:"Search all study sheets", searchAllSub:"Concepts, authors, dates and places from every unit", searchPh:"Type at least 3 letters", '
      'searchN:"{n} study sheets found", searchNone:"No study sheets contain that word", searchLoading:"Loading the units…", '
      'report:"⚑ Report a mistake", reportHint:"Your email app will open with a message ready for the lecturer.", reportWrite:"Describe the mistake here:", ')
a = s.index('mapMore:"Para saber más"'); s = s[:a] + ES + s[a:]
b = s.index('mapMore:"Learn more"'); s = s[:b] + EN + s[b:]

CSS = '''.rep{display:block;margin:10px auto 0;background:none;border:0;color:var(--muted);font-size:13px;text-decoration:underline;cursor:pointer;padding:6px}
.srch-res{display:flex;flex-direction:column;gap:10px;margin-top:10px}
.srch-res button{text-align:left;background:var(--paper);border-radius:14px;padding:12px 14px;box-shadow:var(--shadow);border:0;cursor:pointer}
.srch-res .tt{font-weight:800;color:var(--primary-2);font-size:15px}
.srch-res .mt{font-size:12px;color:var(--muted);margin:2px 0 6px}
.srch-res .sn{font-size:13.5px;line-height:1.45;color:#383838}
.srch-res mark{background:#FFE7A3;color:inherit;border-radius:3px;padding:0 2px;font-weight:700}
</style>'''
assert s.count('</style>') == 1
s = s.replace('</style>', CSS, 1)

JS = r'''
/* --- avisar de un error --- */
function reportMail(ctx){
  const v=S.view||{}; const ver=S.temasIndex?S.temasIndex.version:"";
  const subj=`Historiapp · error · ${ctx.where}`;
  const body=`${t("reportWrite")}\n\n\n\n---\n${ctx.where}\n${ctx.text?ctx.text.slice(0,300)+"\n":""}${S.lang.toUpperCase()} · ${ver}\n${location.href}`;
  track("aviso-error/"+(v.num||"")+"/"+(v.mode||v.name||""),"Aviso de error",true);
  location.href=`mailto:REPORT_EMAIL?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(body)}`;
}
function sheetReportCtx(explain){
  const v=S.view||{}; const q=document.querySelector("main .qtext")||document.querySelector("main .deck > :last-child")||document.querySelector("main .card");
  const qt=q?q.innerText.replace(/\s+/g," ").trim():"";
  return {where:`${t("tema")} ${v.num||""} · ${v.mode?t("modes."+v.mode):""}`, text:(qt?qt+" | ":"")+(explain||"")};
}

/* --- buscador global --- */
async function renderSearch(){
  const q0=S.view.q||"";
  app.innerHTML=header(t("searchAll"),true)+`<main>
    <input class="search" id="gq" type="search" placeholder="${t("searchPh")}" autocomplete="off" value="${esc(q0)}">
    <div class="counter" id="gcount">${t("searchLoading")}</div><div class="srch-res" id="gres"></div></main>`;
  bindHeader(()=>nav({name:"home"}));
  const temas=[]; try{ const idx=await getIndex(); for(const m of idx.temas){ if(m.available){ try{ temas.push(await getTema(m.num)); }catch(e){} } } }catch(e){}
  const inp=document.getElementById("gq"), res=document.getElementById("gres"), cnt=document.getElementById("gcount"); if(!inp) return;
  const hl=(txt,qq)=>{ const n=norm(txt); const i=n.indexOf(qq); if(i<0) return esc(txt.slice(0,160))+(txt.length>160?"…":"");
    const a=Math.max(0,i-70), e=Math.min(txt.length,i+qq.length+90);
    return (a>0?"…":"")+esc(txt.slice(a,i))+"<mark>"+esc(txt.slice(i,i+qq.length))+"</mark>"+esc(txt.slice(i+qq.length,e))+(e<txt.length?"…":""); };
  let tmr=null;
  function paint(){
    const raw=inp.value.trim(), qq=norm(raw); res.innerHTML="";
    if(qq.length<3){ cnt.textContent=t("searchPh"); return; }
    const out=[];
    for(const tm of temas){ (tm.fichas||[]).forEach(f=>{ const title=L(f.title), body=LL(f.body).join(" ");
      const inT=norm(title).includes(qq), inB=norm(body).includes(qq); if(inT||inB) out.push({tm,f,score:inT?0:1,title,body}); }); }
    out.sort((x,y)=>x.score-y.score||x.tm.num-y.tm.num);
    cnt.textContent=out.length?t("searchN",{n:out.length}):t("searchNone");
    for(const r of out.slice(0,60)){ const b=document.createElement("button");
      b.innerHTML=`<div class="tt">${esc(r.title)}</div><div class="mt">${t("tema")} ${r.tm.num} · ${esc(r.f.sec)} · ${esc(r.f.code)}</div><div class="sn">${hl(r.body,qq)}</div>`;
      b.onclick=()=>nav({name:"mode",num:r.tm.num,mode:"fichas",f:r.f.id,back:{name:"search",q:raw}}); res.appendChild(b); }
    S.view.q=raw;
  }
  inp.oninput=()=>{ clearTimeout(tmr); tmr=setTimeout(paint,180); }; paint(); if(!q0) inp.focus();
}
'''.replace('REPORT_EMAIL', EMAIL)
anchor = '/* --- mapa conceptual --- */'
assert anchor in s
s = s.replace(anchor, JS + '\n' + anchor, 1)

# sheet(): enlace de aviso bajo el botón
old = '''    <button class="btn" id="sheetNext">${t("next")}</button>`;
  requestAnimationFrame(()=>el.classList.add("show"));
  document.getElementById("sheetNext").onclick=()=>{ el.classList.remove("show"); setTimeout(onNext,200); };'''
assert old in s
s = s.replace(old, '''    <button class="btn" id="sheetNext">${t("next")}</button><button class="rep" id="sheetRep">${t("report")}</button>`;
  requestAnimationFrame(()=>el.classList.add("show"));
  const rctx=sheetReportCtx(explain); document.getElementById("sheetRep").onclick=()=>reportMail(rctx);
  document.getElementById("sheetNext").onclick=()=>{ el.classList.remove("show"); setTimeout(onNext,200); };''', 1)

# ficha: botón de aviso al final
old = '''<button class="btn sec" id="fNext" ${k===fs.length-1?"disabled":""}>${t("nextF")} ›</button></div>
    </div>`;'''
assert old in s
s = s.replace(old, '''<button class="btn sec" id="fNext" ${k===fs.length-1?"disabled":""}>${t("nextF")} ›</button></div>
    <button class="rep" id="fRep">${t("report")}</button><p style="font-size:11.5px;color:var(--muted);text-align:center;margin:0">${t("reportHint")}</p>
    </div>`;''', 1)
old = '''  document.getElementById("fNext").onclick=()=>nav({name:"mode",num:tema.num,mode:"fichas",f:fs[k+1].id});'''
assert old in s
s = s.replace(old, old + '''
  document.getElementById("fRep").onclick=()=>reportMail({where:`${t("tema")} ${tema.num} · ${f.code} · ${L(f.title)}`,text:""});''', 1)

# mapa: una entrada por ficha relacionada
old = '''${n.f?`<button data-f="${esc(n.f)}">${t("mapFicha")}</button>`:""}'''
assert old in s
s = s.replace(old, '''${(n.fs||(n.f?[n.f]:[])).map(id=>{ const fi=(tema.fichas||[]).find(x=>x.id===id); return `<button data-f="${esc(id)}">📖 ${esc(fi?L(fi.title):t("mapFicha"))}</button>`; }).join("")}''', 1)

# portada: botón del buscador
old = '''    <div id="temaList"><div class="empty">…</div></div>'''
assert old in s
s = s.replace(old, '''    <button class="tema" id="searchBtn"><div class="num">🔎</div><div class="t"><b>${t("searchAll")}</b><span>${t("searchAllSub")}</span></div><div class="pct">›</div></button>
''' + old, 1)
old = '''document.getElementById("examBtn").onclick=()=>nav({name:"exam"});'''
assert old in s
s = s.replace(old, old + ''' document.getElementById("searchBtn").onclick=()=>nav({name:"search"});''', 1)

# rutas
s = s.replace('if(v.name==="exam") return "examen";', 'if(v.name==="exam") return "examen"; if(v.name==="search") return "buscar";', 1)
s = s.replace('if(h==="examen") return {name:"exam"};', 'if(h==="examen") return {name:"exam"}; if(h==="buscar") return {name:"search"};', 1)
s = s.replace('  if(v.name==="exam") return renderExam();', '  if(v.name==="exam") return renderExam();\n  if(v.name==="search") return renderSearch();', 1)
assert 'renderSearch();' in s and '"buscar"' in s
open(p, 'w', encoding='utf-8').write(s)
print('ok')
