p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,c=1):
    global s; assert s.count(o)==c,(o[:70],s.count(o)); s=s.replace(o,n)
# tabs
rep('const TABS=[["home","🏠","tabHome"],["temas","📚","tabTemas"],["videos","▶️","tabVid"],["enc","📖","tabEnc"],["exam","🎓","tabExam"],["settings","⚙️","tabSet"]];',
    'const TABS=[["home","🏠","tabHome"],["temas","📚","tabTemas"],["videos","▶️","tabVid"],["search","🔎","tabSearch"],["enc","📖","tabEnc"],["exam","🎓","tabExam"]];')
rep('if(n==="settings") return "settings"; return "home"; }','if(n==="search") return "search"; if(n==="settings"||n==="guia") return "settings"; return "home"; }')
# header: gear instead of search
rep('<button class="srch" id="hSearch" aria-label="${esc(t("searchAll"))}">🔎</button></div>`;','<button class="srch" id="hSearch" aria-label="${esc(t("settings"))}" title="${esc(t("settings"))}">⚙️</button></div>`;')
rep('if(g) g.onclick=()=>nav({name:"search",back:S.view});','if(g) g.onclick=()=>nav({name:"settings",from:S.view});')
# i18n
rep('tabSet:"Ajustes",','tabSet:"Ajustes", tabSearch:"Buscar", guide:"Guía de la app", guideSub:"Qué hay en cada apartado y cómo se usa",')
rep('tabSet:"Settings",','tabSet:"Settings", tabSearch:"Search", guide:"App guide", guideSub:"What each section contains and how to use it",')
# routes
rep('if(v.name==="settings") return "ajustes";','if(v.name==="settings") return "ajustes"; if(v.name==="guia") return "guia";')
rep('if(h==="ajustes") return {name:"settings"};','if(h==="ajustes") return {name:"settings"}; if(h==="guia") return {name:"guia"};')
rep('  if(v.name==="search") return renderSearch();','  if(v.name==="guia") return renderGuia();\n  if(v.name==="search") return renderSearch();')
# home: remove continuar and píldora
rep('    <div id="contBox"></div>\n','')
rep('const sDep=slot("dep"), sEfe=slot("efe"), sPil=slot("pil");','const sDep=slot("dep"), sEfe=slot("efe");')
a=s.index("  // píldora del día"); b=s.index("}catch(e){}",a)+len("}catch(e){}")
s=s[:a]+s[b:]
# settings: guide button
rep('''    <button class="btn" id="sInstall">📲 ${t("installBtn")}</button>''','''    <button class="tema" id="sGuide"><div class="num">🧭</div><div class="t"><b>${t("guide")}</b><span>${t("guideSub")}</span></div><div class="pct">›</div></button>
    <button class="btn" id="sInstall">📲 ${t("installBtn")}</button>''')
rep('''  document.getElementById("sInstall").onclick=installApp;''','''  document.getElementById("sInstall").onclick=installApp;
  document.getElementById("sGuide").onclick=()=>nav({name:"guia",from});''')
GUIDE=open("tools/guia_texto.js",encoding="utf-8").read()
rep('function renderSettings(){',GUIDE+'\nfunction renderSettings(){')
open(p,"w",encoding="utf-8").write(s); print("ok")
