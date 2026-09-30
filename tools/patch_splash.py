p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,c=1):
    global s; assert s.count(o)==c,(o[:70],s.count(o)); s=s.replace(o,n)
# --- wordle key includes word
rep('function wdKey(){ return todayKey()+"|"+S.lang; }','function wdKey(W){ return todayKey()+"|"+S.lang+"|"+(W?W.w:""); }')
rep('function wdState(){ const w=S.prog.wd||{}; if(w.key!==wdKey()) return {key:wdKey(),g:[],done:false,won:false}; return w; }',
    'function wdState(W){ const k=wdKey(W), w=S.prog.wd||{}; if(w.key!==k) return {key:k,g:[],done:false,won:false}; return w; }')
rep('const W=await wdToday(); if(!W) return; const st=wdState();','const W=await wdToday(); if(!W) return; const st=wdState(W);')
rep('const sol=W.w; let st=wdState(); let cur="";','const sol=W.w; let st=wdState(W); let cur="";')
# --- achievement modal
rep('''  ACH.forEach(([id,ic,f])=>{ if(!p.ach[id]&&f(p)){ p.ach[id]=todayKey(); n.push(ic+" "+t("ach."+id+".n")); } });
  if(n.length){ save(); setTimeout(()=>toast("🏆 "+n[0],2600),1200); } }''','''  ACH.forEach(([id,ic,f])=>{ if(!p.ach[id]&&f(p)){ p.ach[id]=todayKey(); n.push([id,ic]); } });
  if(n.length){ save(); if(S.lang) setTimeout(()=>showAch(n),900); } }
function showAch(list){ document.querySelectorAll(".achm").forEach(x=>x.remove());
  const d=document.createElement("div"); d.className="achm"; d.setAttribute("role","dialog"); d.setAttribute("aria-modal","true");
  d.innerHTML=`<div class="achm-box"><div class="achm-t">🏆 ${t(list.length>1?"achNewN":"achNew")}</div>${list.map(([id,ic])=>`<div class="achm-i"><span>${ic}</span><div><b>${esc(t("ach."+id+".n"))}</b><small>${esc(t("ach."+id+".d"))}</small></div></div>`).join("")}
    <div class="achm-b"><button class="btn" id="achOk">${t("achOk")}</button><button class="btn sec" id="achSee">${t("achSee")}</button></div></div>`;
  document.body.appendChild(d); celebrate();
  const close=()=>{ d.classList.add("out"); setTimeout(()=>d.remove(),250); };
  d.querySelector("#achOk").onclick=close; d.onclick=e=>{ if(e.target===d) close(); };
  d.querySelector("#achSee").onclick=()=>{ close(); nav({name:"logros",back:S.view}); }; }''')
rep('achT:"Logros",','achT:"Logros", achNew:"¡Logro desbloqueado!", achNewN:"¡Logros desbloqueados!", achOk:"Seguir", achSee:"Ver mis logros", loading:"Preparando la app…",')
rep('achT:"Achievements",','achT:"Achievements", achNew:"Achievement unlocked!", achNewN:"Achievements unlocked!", achOk:"Continue", achSee:"See my achievements", loading:"Getting the app ready…",')
CSS='''.achm{position:fixed;inset:0;z-index:200;background:rgba(0,20,50,.55);display:flex;align-items:center;justify-content:center;padding:24px;animation:achIn .25s ease}
.achm.out{opacity:0;transition:opacity .25s}
.achm-box{width:100%;max-width:360px;background:var(--paper);border-radius:22px;padding:22px 20px;box-shadow:0 20px 60px rgba(0,0,0,.35);border:3px solid var(--accent);text-align:center;animation:achPop .45s cubic-bezier(.2,1.4,.4,1)}
.achm-t{font-size:20px;font-weight:800;color:var(--tp2);margin-bottom:14px}
.achm-i{display:flex;align-items:center;gap:14px;text-align:left;background:var(--warm);border-radius:14px;padding:12px 14px;margin-bottom:10px}
.achm-i span{font-size:40px;line-height:1}
.achm-i b{display:block;font-size:18px;color:var(--tp2)}
.achm-i small{display:block;font-size:13px;color:var(--muted);margin-top:2px}
.achm-b{display:flex;flex-direction:column;gap:8px;margin-top:8px}
@keyframes achIn{from{opacity:0}to{opacity:1}}
@keyframes achPop{from{transform:scale(.6);opacity:0}to{transform:scale(1);opacity:1}}
@media (prefers-reduced-motion: reduce){.achm,.achm-box{animation:none}}
#splash .sp-bar{width:min(60vw,240px);height:6px;border-radius:99px;background:rgba(255,255,255,.2);overflow:hidden;margin-top:6px}
#splash .sp-bar i{display:block;height:100%;width:0;background:#EDAB00;transition:width .3s}
#splash .sp-msg{font-size:12.5px;opacity:.85;min-height:16px}
'''
rep('#splash.out{opacity:0;pointer-events:none}','#splash.out{opacity:0;pointer-events:none}\n'+CSS)
rep('<div id="splash"><img src="icons/logo_oro.png" alt="Historiapp"><small>Historia del Deporte · UCAM</small></div>',
    '<div id="splash"><img src="icons/logo_oro.png" alt="Historiapp"><small>Historia del Deporte · UCAM</small><div class="sp-bar"><i id="spBar"></i></div><div class="sp-msg" id="spMsg"></div></div>')
# --- boot: preload before first render
rep('''  if(l){ S.lang=l; document.documentElement.lang=l; S.view=hashToView(location.hash); } else { S.view={name:"gate"}; S.pending=location.hash||null; }
  render();
  const sp=document.getElementById("splash");
  if(sp){ let done=false; const hide=()=>{ if(done) return; done=true; sp.classList.add("out"); setTimeout(()=>sp.remove(),650); };
    sp.onclick=hide; setTimeout(hide,1800); }''','''  if(l){ S.lang=l; document.documentElement.lang=l; S.view=hashToView(location.hash); } else { S.view={name:"gate"}; S.pending=location.hash||null; }
  const sp=document.getElementById("splash");
  let hidden=false; const hide=()=>{ if(hidden||!sp) return; hidden=true; sp.classList.add("out"); setTimeout(()=>sp.remove(),650); };
  if(!l){ render(); if(sp){ sp.onclick=hide; setTimeout(hide,1800); } }
  else { const t0=Date.now(); const bar=document.getElementById("spBar"), msg=document.getElementById("spMsg"); if(msg) msg.textContent=t("loading");
    let rendered=false; const go=()=>{ if(rendered) return; rendered=true; render(); setTimeout(hide,Math.max(0,1200-(Date.now()-t0))); };
    const img=src=>new Promise(r=>{ const i=new Image(); i.onload=i.onerror=()=>r(); i.src=src; });
    const jobs=[]; const add=p=>{ jobs.push(p.catch(()=>{}).then(()=>{ done++; if(bar) bar.style.width=Math.round(done/Math.max(1,jobs.length)*100)+"%"; })); }; let done=0;
    add(getIndex().then(idx=>Promise.all(idx.temas.filter(x=>x.available).map(x=>getTema(x.num).catch(()=>{})))));
    add(getEnc().then(D=>{ try{ const e=encDaily(D.entries); if(e&&e.img&&e.img.src) return img(e.img.src); }catch(_){} }));
    add(getEfe()); add(document.fonts?document.fonts.ready:Promise.resolve());
    Object.values(typeof TEMA_IMG!=="undefined"?TEMA_IMG:{}).forEach(src=>add(img(src)));
    Promise.all(jobs).then(go); setTimeout(go,7000); if(sp) sp.onclick=()=>{ go(); hide(); }; }''')
open(p,"w",encoding="utf-8").write(s); print("ok")
