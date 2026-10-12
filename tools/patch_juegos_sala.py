# Historiapp: un solo botón «Juegos» en la portada y sala de juegos (#juegos) con miniaturas como las de los temas.
import re,sys
P="index.html"; s=open(P,encoding="utf-8").read(); o=s
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: sys.exit(f"esperaba {n} y hay {c}: {a[:70]}")
    s=s.replace(a,b)
# textos
rep('gamesCard:"Juegos de la asignatura",','gamesCard:"Juegos de la asignatura", gamesT:"Juegos", gamesN:"{n} juegos", gamesIntro:"Toca un juego para abrirlo. Dentro de Historiapp, cada acierto y cada victoria suman XP a tu progreso.",')
rep('gamesCard:"Course games",','gamesCard:"Course games", gamesT:"Games", gamesN:"{n} games", gamesIntro:"Tap a game to open it. Inside Historiapp, every correct answer and every win adds XP to your progress.",')
# portada: la tira de miniaturas pasa a ser un único botón
a=s.index('  { const gc=document.createElement("div"); gc.className="card reto games";'); b=s.index('\n',a)
s=s[:a]+'''  { const gc=document.createElement("button"); gc.className="card reto gbtn"; gc.innerHTML=`<div class="ic" aria-hidden="true">🎮</div><div class="tx"><small>${t("gamesT")}</small><b>${t("gamesCard")}</b><span>${t("gamesSub")}</span></div><div class="xp">${t("gamesN",{n:GAMES.length})}</div>`; gc.onclick=()=>nav({name:"juegos"}); hoy.appendChild(gc); }'''+s[b:]
# vista
rep('async function renderTemas(){','''function renderJuegos(){
  app.innerHTML=header(t("gamesT"),true)+`<main><p class="gintro">${t("gamesIntro")}</p><div class="tgrid" id="ggrid"></div></main>`;
  bindHeader(()=>nav({name:"home"}));
  const box=document.getElementById("ggrid");
  GAMES.forEach(g=>{ const b=document.createElement("button"); b.className="tcard gcard"; b.style.backgroundImage=`url('${g.img}')`; b.setAttribute("aria-label",L(g.title));
    const tl=(g.temas.length>1?(S.lang==="en"?"Units ":"Temas ")+g.temas[0]+"–"+g.temas[g.temas.length-1]:t("tema")+" "+g.temas[0]);
    b.innerHTML=`<div class="gchip">${esc(tl)}</div><div class="tx"><small>${esc(L(g.gen))}</small><b>${esc(L(g.n))}</b></div>`;
    b.onclick=()=>{ location.href=g.f; }; box.appendChild(b); });
}
async function renderTemas(){''')
rep('if(v.name==="temas") return renderTemas();','if(v.name==="temas") return renderTemas();\n  if(v.name==="juegos") return renderJuegos();')
rep('if(v.name==="temas") return "temas";','if(v.name==="temas") return "temas"; if(v.name==="juegos") return "juegos";')
rep('if(h==="temas") return {name:"temas"};','if(h==="temas") return {name:"temas"}; if(h==="juegos") return {name:"juegos"};')
# estilos
rep('.tcard.locked{','.tcard.gcard{aspect-ratio:16/10;min-height:0}.tcard.gcard .tx small{text-transform:none;letter-spacing:0;font-weight:700;font-size:11.5px;line-height:1.25;opacity:.92}.tcard.gcard .tx b{font-size:16px}.tcard .gchip{position:absolute;top:8px;left:8px;z-index:1;background:rgba(0,20,60,.78);color:#fff;font-size:11px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:4px 8px;border-radius:999px}.gintro{font-size:14px;color:var(--ink);line-height:1.4;margin:2px 2px 12px}.hoy .reto.gbtn .xp{white-space:nowrap}\n.tcard.locked{')
open(P,"w",encoding="utf-8").write(s)
W="sw.js"; w=open(W,encoding="utf-8").read()
w=re.sub(r'historiapp-v\d+','historiapp-v87',w,count=1)
if "img/juegos/" not in w:
    w=w.replace('"./juegos/gladiatura.html",','"./juegos/gladiatura.html", '+", ".join(f'"./img/juegos/{x}.jpg"' for x in "pentatlon halterios senet agon cuadrigas gladiatura".split())+",",1)
open(W,"w",encoding="utf-8").write(w)
print("ok", len(o), len(s))
