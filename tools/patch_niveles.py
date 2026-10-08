# 100 niveles sin nombre (08-10-2026). Los 10 primeros umbrales se mantienen; nadie baja de nivel.
import pathlib,sys
root=pathlib.Path(__file__).resolve().parent.parent
p=root/"index.html"; s=p.read_text(encoding="utf-8")
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: sys.exit(f"ERROR ({c} coincidencias): {a[:80]}")
    s=s.replace(a,b)
rep('const LEVEL_XP=[0,100,250,450,700,1000,1400,1900,2500,3300];',
 'const LEVEL_XP=(()=>{const a=[0,100,250,450,700,1000,1400,1900,2500,3300];for(let i=1;i<=90;i++)a.push(a[a.length-1]+Math.round((400+(i-1)*240/89)/10)*10);return a})();')
rep('levelUp:"¡Nivel {n}: {name}!"','levelUp:"¡Nivel {n}!", lvOf:"Nivel {n} de {t}"')
rep('levelUp:"Level {n}: {name}!"','levelUp:"Level {n}!", lvOf:"Level {n} of {t}"')
rep('lgNext:"Te faltan {n} XP para el nivel {l}, {name}"','lgNext:"Te faltan {n} XP para el nivel {l}"')
rep('lgNext:"{n} XP to go for level {l}, {name}"','lgNext:"{n} XP to go for level {l}"')
rep('lvl3:{n:"En marcha",d:"Llega al nivel 3"},lvl5:{n:"Mitad del camino",d:"Llega al nivel 5"},lvl10:{n:"Catedrático",d:"Llega al nivel máximo"},',
 'lvl3:{n:"En marcha",d:"Llega al nivel 3"},lvl5:{n:"Buen ritmo",d:"Llega al nivel 5"},lvl10:{n:"Dos cifras",d:"Llega al nivel 10"},lvl25:{n:"Un cuarto del camino",d:"Llega al nivel 25"},lvl50:{n:"Ecuador",d:"Llega al nivel 50"},lvl75:{n:"Recta final",d:"Llega al nivel 75"},lvl100:{n:"Catedrático",d:"Llega al nivel 100, el máximo"},')
rep('lvl3:{n:"Getting going",d:"Reach level 3"},lvl5:{n:"Halfway there",d:"Reach level 5"},lvl10:{n:"Professor",d:"Reach the top level"},',
 'lvl3:{n:"Getting going",d:"Reach level 3"},lvl5:{n:"Good pace",d:"Reach level 5"},lvl10:{n:"Double figures",d:"Reach level 10"},lvl25:{n:"A quarter of the way",d:"Reach level 25"},lvl50:{n:"Halfway there",d:"Reach level 50"},lvl75:{n:"Home straight",d:"Reach level 75"},lvl100:{n:"Professor",d:"Reach level 100, the top level"},')
rep(' ["lvl10","🎓",p=>levelOf(p.xp)>=9],',
 ' ["lvl10","🔟",p=>levelOf(p.xp)>=9],\n ["lvl25","🧗",p=>levelOf(p.xp)>=24],\n ["lvl50","⛰️",p=>levelOf(p.xp)>=49],\n ["lvl75","🏃",p=>levelOf(p.xp)>=74],\n ["lvl100","🎓",p=>levelOf(p.xp)>=99],')
rep('<div class="lv"><b>${t("level")} ${lvl+1} · ${esc(t("levels")[lvl])}</b>','<div class="lv"><b>${t("lvOf",{n:lvl+1,t:LEVEL_XP.length})}</b>')
rep('<small>${t("level")} ${lv+1}</small><b>${esc(names[lv])}</b>','<small>${t("level")}</small><b>${t("lvOf",{n:lv+1,t:LEVEL_XP.length})}</b>')
rep('t("lgNext",{n:nxt-p.xp,l:lv+2,name:names[lv+1]})','t("lgNext",{n:nxt-p.xp,l:lv+2})')
rep('<div class="lg-levels">${names.map((n,i)=>`<div class="lg-l ${i<lv?"done":i===lv?"now":"next"}"><span class="n">${i+1}</span><b>${esc(n)}</b><small>${LEVEL_XP[i]} ${t("xp")}</small><em>${i<lv?"✓":i===lv?t("lgHere"):"🔒"}</em></div>`).join("")}</div>',
 '<div class="lg-grid">${LEVEL_XP.map((x,i)=>`<button class="lg-c ${i<lv?"done":i===lv?"now":"next"}" data-t="${esc(t("level")+" "+(i+1)+" · "+x+" "+t("xp"))}" aria-label="${esc(t("level")+" "+(i+1)+", "+x+" "+t("xp"))}">${i+1}</button>`).join("")}</div>')
rep('<div class="card lg-how">${t("lgHowList").map(x=>`<p>${esc(x)}</p>`).join("")}</div></main>`;',
 '<div class="card lg-how">${t("lgHowList").map(x=>`<p>${esc(x)}</p>`).join("")}</div></main>`;\n  app.querySelectorAll(".lg-c").forEach(c=>c.onclick=()=>toast(c.dataset.t,1800));')
rep('.lg-levels{display:flex;flex-direction:column;gap:6px}',
 '.lg-levels{display:flex;flex-direction:column;gap:6px}\n.lg-grid{display:grid;grid-template-columns:repeat(10,1fr);gap:5px}\n.lg-c{aspect-ratio:1;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--muted);font:inherit;font-size:12px;font-weight:800;padding:0;cursor:pointer}\n.lg-c.done{background:var(--tp);border-color:var(--tp);color:var(--paper)}\n.lg-c.now{border:2px solid var(--accent);background:var(--warm);color:var(--ink)}\n.lg-c.next{opacity:.55}')
rep('de Aprendiz a Catedrático','del 1 al 100')
rep('from Apprentice to Professor','from 1 to 100')
p.write_text(s,encoding="utf-8")
g=root/"tools/guia_texto.js"
if g.exists():
    t=g.read_text(encoding="utf-8").replace('de Aprendiz a Catedrático','del 1 al 100').replace('from Apprentice to Professor','from 1 to 100'); g.write_text(t,encoding="utf-8")
w=root/"sw.js"; ws=w.read_text(encoding="utf-8")
import re; ws=re.sub(r'historiapp-v(\d+)',lambda m:f'historiapp-v{int(m.group(1))+1}',ws,1); w.write_text(ws,encoding="utf-8")
print("OK")
