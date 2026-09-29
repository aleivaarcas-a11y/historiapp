#!/usr/bin/env python3
"""Buscador general de toda la app (fichas de los temas, enciclopedia, glosario, cronología y vídeos) arriba de la portada,
debajo del nivel; «Deporte del día» pasa debajo de «Reto del día». Uso: python3 tools/patch_buscador.py"""
import os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'id="homeQ"' in s: print('ya aplicado'); raise SystemExit
def rep(old, new):
    global s
    assert old in s, old[:80]; s = s.replace(old, new, 1)

# portada: quitar botón de búsqueda, buscador bajo el nivel, deporte del día bajo el reto
btn = '''    <button class="tema" id="searchBtn"><div class="num">🔎</div><div class="t"><b>${t("searchAll")}</b><span>${t("searchAllSub")}</span></div><div class="pct">›</div></button>\n'''
rep(btn, '')
day = '''    <div class="encday" id="encDay" style="display:none"></div>\n'''
rep(day, '')
rep('''    <button class="tema" id="dailyBtn"''', '''    <input class="search" id="homeQ" type="search" readonly placeholder="🔎 ${t("searchHome")}" style="cursor:pointer">\n    <button class="tema" id="dailyBtn"''')
m = re.search(r'(    <button class="tema" id="dailyBtn".*?</button>\n)', s, re.S)
s = s.replace(m.group(1), m.group(1) + day, 1)
rep('document.getElementById("searchBtn").onclick=()=>nav({name:"search"});', 'document.getElementById("homeQ").onclick=()=>nav({name:"search"});')

# textos
rep('searchAll:"Buscar en todas las fichas"', 'searchAll:"Buscar en Historiapp", searchHome:"Buscar en toda la app", sFicha:"Ficha", sEnc:"Enciclopedia", sGloss:"Glosario", sTime:"Cronología", sVid:"Vídeo", searchRes:"{n} resultados"')
rep('searchAll:"Search all study sheets"', 'searchAll:"Search Historiapp", searchHome:"Search the whole app", sFicha:"Study sheet", sEnc:"Encyclopedia", sGloss:"Glossary", sTime:"Timeline", sVid:"Video", searchRes:"{n} results"')

# nueva función de búsqueda
a = s.index('async function renderSearch(){'); b = s.index('\n/* --- mapa conceptual --- */')
NEW = r'''async function renderSearch(){
  const q0=S.view.q||"";
  app.innerHTML=header(t("searchAll"),true)+`<main>
    <input class="search" id="gq" type="search" placeholder="${t("searchPh")}" autocomplete="off" value="${esc(q0)}">
    <div class="counter" id="gcount">${t("searchLoading")}</div><div class="srch-res" id="gres"></div></main>`;
  bindHeader(()=>nav({name:"home"}));
  const inp0=document.getElementById("gq"); if(inp0&&!q0) inp0.focus();
  const temas=[]; let enc={entries:[]};
  try{ const idx=await getIndex(); for(const m of idx.temas){ if(m.available){ try{ temas.push(await getTema(m.num)); }catch(e){} } } }catch(e){}
  try{ enc=await getEnc(); }catch(e){}
  const inp=document.getElementById("gq"), res=document.getElementById("gres"), cnt=document.getElementById("gcount"); if(!inp) return;
  const hl=(txt,qq)=>{ const n=norm(txt); const i=n.indexOf(qq); if(i<0) return esc(txt.slice(0,160))+(txt.length>160?"…":"");
    const a=Math.max(0,i-70), e=Math.min(txt.length,i+qq.length+90);
    return (a>0?"…":"")+esc(txt.slice(a,i))+"<mark>"+esc(txt.slice(i,i+qq.length))+"</mark>"+esc(txt.slice(i+qq.length,e))+(e<txt.length?"…":""); };
  const plain=x=>String(x).replace(/\*+/g,"");
  let tmr=null;
  function paint(){
    const raw=inp.value.trim(), qq=norm(raw); res.innerHTML="";
    if(qq.length<3){ cnt.textContent=t("searchPh"); S.view.q=raw; return; }
    const out=[]; const has=x=>norm(x).includes(qq);
    for(const e of enc.entries||[]){ const title=L(e.name), body=plain(LL(e.body).join(" "));
      const inT=has(e.name.es+" "+e.name.en), inB=has(body)||has(L(e.cuando));
      if(inT||inB) out.push({score:inT?0:3,title,tag:t("sEnc"),meta:plain(L(e.cuando)),body:inT?"":body,go:()=>nav({name:"enc",id:e.id,back:{name:"search",q:raw}})}); }
    for(const tm of temas){
      (tm.fichas||[]).forEach(f=>{ const title=L(f.title), body=plain(LL(f.body).join(" "));
        const inT=has(title), inB=has(body); if(inT||inB) out.push({score:inT?1:4,num:tm.num,title,tag:t("sFicha"),meta:`${t("tema")} ${tm.num} · ${f.sec} · ${f.code}`,body,go:()=>nav({name:"mode",num:tm.num,mode:"fichas",f:f.id,back:{name:"search",q:raw}})}); });
      (tm.glossary||[]).forEach(g=>{ if(g.lang&&g.lang!==S.lang) return; const title=L(g.term), def=L(g.def);
        if(has(title)||has(def)) out.push({score:has(title)?2:5,num:tm.num,title,tag:t("sGloss"),meta:`${t("tema")} ${tm.num}`,body:def,full:true}); });
      (tm.timeline||[]).forEach(tl=>(tl.items||[]).forEach(it=>{ const lab=L(it.label);
        if(has(lab)) out.push({score:5,num:tm.num,title:L(it.date)+" · "+lab,tag:t("sTime"),meta:`${t("tema")} ${tm.num} · ${L(tl.title)}`,body:"",go:()=>nav({name:"mode",num:tm.num,mode:"timeline",back:{name:"search",q:raw}})}); }));
      (tm.videos||[]).forEach(vd=>{ const title=L(vd.title);
        if(has(title)||has(L(vd.more||""))) out.push({score:6,num:tm.num,title:"▶ "+title,tag:t("sVid"),meta:`${t("tema")} ${tm.num}`,body:"",go:()=>nav({name:"mode",num:tm.num,mode:"videos",back:{name:"search",q:raw}})}); });
    }
    out.sort((x,y)=>x.score-y.score||(x.num||0)-(y.num||0));
    cnt.textContent=out.length?t("searchRes",{n:out.length}):t("searchNone");
    for(const r of out.slice(0,100)){ const b=document.createElement("button");
      b.innerHTML=`<div class="tt">${esc(r.title)}</div><div class="mt"><b>${esc(r.tag)}</b> · ${esc(r.meta)}</div>${r.body?`<div class="sn">${r.full?esc(r.body):hl(r.body,qq)}</div>`:""}`;
      if(r.go) b.onclick=r.go; else b.style.cursor="default"; res.appendChild(b); }
    S.view.q=raw;
  }
  inp.oninput=()=>{ clearTimeout(tmr); tmr=setTimeout(paint,180); }; paint();
}
'''
s = s[:a] + NEW + s[b:]
open(p, 'w', encoding='utf-8').write(s)
sw = os.path.join(R, 'sw.js'); w = open(sw, encoding='utf-8').read()
w = re.sub(r'historiapp-v(\d+)', lambda m: 'historiapp-v%d' % (int(m.group(1)) + 1), w, 1); open(sw, 'w', encoding='utf-8').write(w)
print('ok', re.search(r'historiapp-v\d+', w).group(0))
