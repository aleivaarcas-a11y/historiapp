# Historiapp: pestaña Atlas (#atlas) en la barra inferior, que abre atlas/index.html dentro de la app.
# Uso: python3 tools/patch_atlas.py  (desde la carpeta Historiapp). Idempotente.
import shutil, re
P="index.html"; t=open(P,encoding="utf8").read()
if "/* --- atlas (patch_atlas) --- */" in t: print("Ya aplicado."); raise SystemExit
shutil.copy(P,"tools/index_antes_atlas.html")
def R(a,b):
    global t
    assert t.count(a)==1,("no encontrado o repetido: "+a[:70]); t=t.replace(a,b)
# quitar la entrada provisional del Atlas en la lista de juegos, si existe
t=re.sub(r'\n  \{f:"juegos/atlas\.html"[^\n]*\},','',t)
R('["linea","🕰️","tabLine"],','["linea","🕰️","tabLine"],["atlas","🗺️","tabAtlas"],')
R('tabLine:"Línea"','tabLine:"Línea", tabAtlas:"Atlas"')
R('tabLine:"Timeline"','tabLine:"Timeline", tabAtlas:"Atlas"')
R('if(n==="linea") return "linea";','if(n==="linea") return "linea"; if(n==="atlas") return "atlas";')
R('if(v.name==="linea") return "linea";','if(v.name==="linea") return "linea"; if(v.name==="atlas") return "atlas";')
R('if(h==="linea") return {name:"linea"};','if(h==="linea") return {name:"linea"}; if(h==="atlas") return {name:"atlas"};')
R('  if(v.name==="linea") return renderLinea();','  if(v.name==="linea") return renderLinea();\n  if(v.name==="atlas") return renderAtlas();')
R('async function renderLinea(){','''/* --- atlas (patch_atlas) --- */
function renderAtlas(){
  app.innerHTML=header(t("tabAtlas"),true)+`<main class="atmain"></main><iframe id="atFr" title="${esc(t("tabAtlas"))}" src="atlas/index.html?lang=${S.lang||"es"}"></iframe>`;
  bindHeader(()=>nav({name:"home"}));
  const fr=document.getElementById("atFr");
  const fit=()=>{ if(!fr.isConnected){ removeEventListener("resize",fit); return; } const hd=app.querySelector(".top"); const top=hd?hd.getBoundingClientRect().bottom:0; const tb=document.getElementById("tabbar"); const bh=tb&&getComputedStyle(tb).display!=="none"?tb.getBoundingClientRect().height:0; fr.style.top=top+"px"; fr.style.height=Math.max(300,innerHeight-top-bh)+"px"; };
  fit(); requestAnimationFrame(fit); setTimeout(fit,250); fr.addEventListener("load",fit); addEventListener("resize",fit);
}
addEventListener("message",e=>{ if(e.origin!==location.origin) return; const d=e.data||{};
  if(d.atlas==="xp"&&d.key){ S.prog.atlas=S.prog.atlas||{}; if(!S.prog.atlas[d.key]){ S.prog.atlas[d.key]=1; addXP(d.n||5); try{renderXP();}catch(_){} } }
  else if(d.atlas==="go"&&typeof d.hash==="string"&&d.hash.startsWith("#")){ location.hash=d.hash; } });
async function renderLinea(){''')
t=t.replace("</style>","main.atmain{padding:0;overflow:hidden;gap:0}\n#atFr{position:fixed;left:0;right:0;width:100%;height:auto;border:0;background:#0e2a35;z-index:5}\n</style>",1)
open(P,"w",encoding="utf8").write(t); print("Atlas añadido a la barra inferior.")
