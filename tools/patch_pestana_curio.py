# Pestaña «Curiosidades» en la barra inferior (08-10-2026): las 100 curiosidades, desbloqueadas según el nivel.
import pathlib,sys,re
root=pathlib.Path(__file__).resolve().parent.parent
p=root/"index.html"; s=p.read_text(encoding="utf-8")
if "renderCur(" in s: sys.exit("ya aplicado")
def rep(a,b):
    global s
    c=s.count(a)
    if c!=1: sys.exit(f"ERROR ({c}): {a[:90]}")
    s=s.replace(a,b)
rep('lvOf:"Nivel {n} de {t}",','lvOf:"Nivel {n} de {t}", tabCur:"¿Sabías?", curT:"Curiosidades", curN:"{a} de {b} desbloqueadas", curSub:"Cada nivel que subes desbloquea una curiosidad de la historia del deporte, en orden cronológico.", curLock:"Nivel {n} · {x} XP",')
rep('lvOf:"Level {n} of {t}",','lvOf:"Level {n} of {t}", tabCur:"Did you know?", curT:"Facts", curN:"{a} of {b} unlocked", curSub:"Every level you reach unlocks a fact from the history of sport, in chronological order.", curLock:"Level {n} · {x} XP",')
rep('["enc","📖","tabEncS"],','["enc","📖","tabEncS"],["cur","✨","tabCur"],')
rep('if(n==="enc") return "enc";','if(n==="enc") return "enc"; if(n==="cur") return "cur";')
rep('if(v.name==="logros") return "logros";','if(v.name==="logros") return "logros"; if(v.name==="cur") return "curiosidades";')
rep('if(h==="logros") return {name:"logros"};','if(h==="logros") return {name:"logros"}; if(h==="curiosidades") return {name:"cur"};')
rep('  if(v.name==="logros") return renderLogros();\n','  if(v.name==="logros") return renderLogros();\n  if(v.name==="cur") return renderCur();\n')
rep('function showAch(list){','''async function renderCur(){
  app.innerHTML=header(t("curT"),false)+`<main><div class="empty">${t("loading")}</div></main>`;
  const all=await getCur(); if(S.view.name!=="cur") return;
  const lv=levelOf(S.prog.xp)+1, tot=(all||[]).length, got=Math.min(lv,tot);
  const m=app.querySelector("main");
  if(!all){ m.innerHTML=`<div class="empty">${t("loadError")}</div>`; return; }
  m.innerHTML=`<p class="cur-sub">${esc(t("curSub"))}</p>
    <div class="card cur-pg"><b>${esc(t("curN",{a:got,b:tot}))}</b><div class="bar"><i style="width:${Math.round(got/tot*100)}%"></i></div></div>
    <div class="cur-list">${all.map((c,i)=>i<lv?`<button class="cur-i" data-n="${i+1}">${c.img?`<img src="${esc(c.img.src)}" alt="" loading="lazy">`:`<span class="cur-ph">✨</span>`}<div><small>${i+1} · ${esc(L(c.era))} · ${esc(L(c.fecha))}</small><b>${esc(L(c.titulo))}</b></div></button>`
      :`<div class="cur-i off"><span class="cur-ph">🔒</span><div><small>${esc(t("curLock",{n:i+1,x:LEVEL_XP[i]}))}</small><b>${esc(L(c.era))}</b></div></div>`).join("")}</div>`;
  m.querySelectorAll("button.cur-i").forEach(b=>b.onclick=()=>showLevel(+b.dataset.n,false));
}
function showAch(list){''')
rep('.lg-hint{','''.cur-sub{font-size:14px;color:var(--muted);margin:0 0 10px}
.cur-pg{margin-bottom:12px}.cur-pg .bar{height:8px;background:var(--soft);border-radius:6px;overflow:hidden}.cur-pg .bar i{display:block;height:100%;background:var(--accent);border-radius:6px}.cur-pg b{display:block;margin-bottom:6px;color:var(--tp2)}
.cur-list{display:flex;flex-direction:column;gap:8px}
.cur-i{display:flex;align-items:center;gap:12px;text-align:left;width:100%;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:8px;font:inherit;color:var(--ink);cursor:pointer}
.cur-i img,.cur-ph{flex:none;width:64px;height:64px;border-radius:10px;object-fit:cover;background:var(--soft);display:flex;align-items:center;justify-content:center;font-size:24px}
.cur-i small{display:block;font-size:11px;font-weight:800;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.cur-i b{display:block;font-size:15px;line-height:1.25;color:var(--tp2);margin-top:2px}
.cur-i.off{opacity:.55;cursor:default}.cur-i.off b{color:var(--muted);font-weight:600}
.lg-hint{''')
p.write_text(s,encoding="utf-8")
w=root/"sw.js"; ws=w.read_text(encoding="utf-8"); ws=re.sub(r'historiapp-v(\d+)',lambda m:f'historiapp-v{int(m.group(1))+1}',ws,1); w.write_text(ws,encoding="utf-8")
print("OK")
