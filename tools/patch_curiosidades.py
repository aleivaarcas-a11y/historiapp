# Curiosidad con foto al subir de nivel (08-10-2026). Datos: data/curiosidades.json (fuente tools/curio/lote_1..5.json).
import pathlib,sys,json,re
root=pathlib.Path(__file__).resolve().parent.parent
# 1) volcar los lotes
allc=[]
for i in range(1,6): allc+=json.load(open(root/f"tools/curio/lote_{i}.json",encoding="utf-8"))
allc.sort(key=lambda x:x["n"]); assert [c["n"] for c in allc]==list(range(1,101))
for c in allc: c.pop("nota",None)
json.dump(allc,open(root/"data/curiosidades.json","w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
# 2) index.html
p=root/"index.html"; s=p.read_text(encoding="utf-8")
if "showLevel(" in s: sys.exit("ya aplicado")
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: sys.exit(f"ERROR ({c}): {a[:90]}")
    s=s.replace(a,b)
rep('lvOf:"Nivel {n} de {t}"','lvOf:"Nivel {n} de {t}", lvUpT:"¡Nivel {n}!", lvCur:"Curiosidad desbloqueada", lvSrc:"Fuentes e imagen", lvImg:"Imagen", lvLocked:"Se desbloquea en el nivel {n} ({x} XP)", lvHint:"Cada nivel desbloquea una curiosidad de la historia del deporte. Toca un nivel conseguido para releerla.", lvPrev:"‹ Anterior", lvNext:"Siguiente ›"')
rep('lvOf:"Level {n} of {t}"','lvOf:"Level {n} of {t}", lvUpT:"Level {n}!", lvCur:"Fact unlocked", lvSrc:"Sources and image", lvImg:"Image", lvLocked:"Unlocks at level {n} ({x} XP)", lvHint:"Each level unlocks a fact from the history of sport. Tap a level you have reached to read it again.", lvPrev:"‹ Previous", lvNext:"Next ›"')
rep('if(after>before) setTimeout(()=>{ toast(t("levelUp",{n:after+1,name:t("levels")[after]}),2600); celebrate(); },350);',
    'if(after>before) setTimeout(()=>{ celebrate(); showLevel(after+1,true); track("nivel/"+(after+1),"Nivel",true); },350);')
rep('function showAch(list){ document.querySelectorAll(".achm").forEach(x=>x.remove());',
'''let CUR=null, ACHQ=null;
async function getCur(){ if(!CUR){ try{ CUR=await (await fetch("data/curiosidades.json")).json(); }catch(e){ CUR=null; } } return CUR; }
async function showLevel(n,isUp){
  const all=await getCur(); const c=all&&all[n-1];
  if(!c){ if(isUp) toast(t("levelUp",{n}),2600); return; }
  document.querySelectorAll(".lvm").forEach(x=>x.remove());
  const reach=levelOf(S.prog.xp)+1, im=c.img;
  const d=document.createElement("div"); d.className="lvm"; d.setAttribute("role","dialog"); d.setAttribute("aria-modal","true");
  d.innerHTML=`<div class="lvm-box">
    <div class="lvm-top">${isUp?`<b>🎉 ${esc(t("lvUpT",{n}))}</b><small>${esc(t("lvCur"))}</small>`:`<b>${esc(t("level"))} ${n}</b>`}</div>
    ${im?`<img class="lvm-img" src="${esc(im.src)}" alt="${esc(L(im.pie))}">`:""}
    <div class="lvm-era">${esc(L(c.era))} · ${esc(L(c.fecha))}</div>
    <h3 class="lvm-t">${esc(L(c.titulo))}</h3>
    <p class="lvm-x">${md(L(c.texto))}</p>
    <details class="lvm-src"><summary>${esc(t("lvSrc"))}</summary>${((S.lang==="en"?c.refs_en:c.refs)||[]).map(r=>`<p>${md(r)}</p>`).join("")}
      ${im?`<p><b>${esc(t("lvImg"))}.</b> ${esc(L(im.pie))} ${esc(L(im.autor)||"")}${im.licencia?", "+esc(im.licencia):""}. <a href="${esc(im.url)}" target="_blank" rel="noopener">Wikimedia Commons</a></p>`:""}</details>
    ${isUp?"":`<div class="lvm-nav"><button class="btn sec" id="lvP" ${n<=1?"disabled":""}>${t("lvPrev")}</button><button class="btn sec" id="lvN" ${n>=reach||n>=all.length?"disabled":""}>${t("lvNext")}</button></div>`}
    <button class="btn" id="lvOk">${t("achOk")}</button></div>`;
  document.body.appendChild(d);
  const close=()=>{ d.classList.add("out"); setTimeout(()=>{ d.remove(); if(ACHQ){ const q=ACHQ; ACHQ=null; showAch(q); } },250); };
  d.querySelector("#lvOk").onclick=close; d.onclick=e=>{ if(e.target===d) close(); };
  const P=d.querySelector("#lvP"), N=d.querySelector("#lvN");
  if(P) P.onclick=()=>showLevel(n-1,false); if(N) N.onclick=()=>showLevel(n+1,false);
  if(isUp){ const nx=all[n]; if(nx&&nx.img){ const i=new Image(); i.src=nx.img.src; } }
}
function showAch(list){ if(document.querySelector(".lvm")){ ACHQ=(ACHQ||[]).concat(list); return; } document.querySelectorAll(".achm").forEach(x=>x.remove());''')
rep('app.querySelectorAll(".lg-c").forEach(c=>c.onclick=()=>toast(c.dataset.t,1800));',
    'app.querySelectorAll(".lg-c").forEach((c,i)=>c.onclick=()=>{ if(i<=lv) showLevel(i+1,false); else toast(t("lvLocked",{n:i+1,x:LEVEL_XP[i]}),2200); });')
rep('<div class="lg-grid">','<p class="lg-hint">${esc(t("lvHint"))}</p><div class="lg-grid">')
rep('.lg-c.next{opacity:.55}','''.lg-c.next{opacity:.55}
.lg-hint{font-size:13px;color:var(--muted);margin:0 0 8px}
.lvm{position:fixed;inset:0;z-index:210;background:rgba(0,20,50,.6);display:flex;align-items:center;justify-content:center;padding:16px;animation:achIn .25s ease}
.lvm.out{opacity:0;transition:opacity .25s}
.lvm-box{width:100%;max-width:420px;max-height:92vh;overflow:auto;background:var(--paper);border-radius:22px;padding:18px 18px 16px;box-shadow:0 20px 60px rgba(0,0,0,.35);border:3px solid var(--accent);animation:achPop .45s cubic-bezier(.2,1.4,.4,1)}
.lvm-top{text-align:center;margin-bottom:12px}
.lvm-top b{display:block;font-size:24px;font-weight:800;color:var(--tp2)}
.lvm-top small{display:block;font-size:13px;font-weight:700;color:var(--wink);text-transform:uppercase;letter-spacing:.06em;margin-top:2px}
.lvm-img{display:block;width:100%;max-height:36vh;object-fit:cover;border-radius:14px;background:var(--soft)}
.lvm-era{font-size:12px;font-weight:800;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-top:12px}
.lvm-t{font-size:20px;line-height:1.2;color:var(--tp2);margin:4px 0 8px}
.lvm-x{font-size:15px;line-height:1.5;margin:0 0 10px}
.lvm-src{font-size:12px;color:var(--muted);margin-bottom:12px}
.lvm-src summary{cursor:pointer;font-weight:700}
.lvm-src p{margin:6px 0}
.lvm-nav{display:flex;gap:8px;margin-bottom:8px}.lvm-nav .btn{flex:1}
.lvm .btn{width:100%}
@media (prefers-reduced-motion: reduce){.lvm,.lvm-box{animation:none}}''')
p.write_text(s,encoding="utf-8")
w=root/"sw.js"; ws=w.read_text(encoding="utf-8"); ws=re.sub(r'historiapp-v(\d+)',lambda m:f'historiapp-v{int(m.group(1))+1}',ws,1); w.write_text(ws,encoding="utf-8")
print("OK")
