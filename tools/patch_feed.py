#!/usr/bin/env python3
"""Vídeos en modo feed (deslizar como en TikTok) con «Saber más» y test sobre el vídeo.
Uso: python3 tools/patch_feed.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'function openFeed' in s:
    print('ya aplicado'); raise SystemExit

ES = 'vFeed:"▶ Verlos seguidos", vFeedSub:"Desliza hacia arriba para pasar al siguiente", vTap:"Toca para activar el sonido", vNext:"Siguiente vídeo ›", vEnd:"Has llegado al último vídeo del tema", vClose:"Volver", vTestB:"Test", vMoreB:"Saber más", '
EN = 'vFeed:"▶ Watch them in a row", vFeedSub:"Swipe up for the next one", vTap:"Tap to turn the sound on", vNext:"Next video ›", vEnd:"That was the last video of this unit", vClose:"Back", vTestB:"Test", vMoreB:"Learn more", '
a = s.index('vMore:"Saber más"'); s = s[:a] + ES + s[a:]
b = s.index('vMore:"Learn more"'); s = s[:b] + EN + s[b:]

CSS = '''.vfeedbtn{width:100%;margin-bottom:12px;display:flex;flex-direction:column;align-items:center;gap:2px}
.vfeedbtn small{font-weight:500;font-size:12px;opacity:.85}
body.feedon{overflow:hidden}
.feed{position:fixed;inset:0;z-index:60;background:#000;color:#fff}
.fscroll{height:100%;overflow-y:scroll;scroll-snap-type:y mandatory;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;scrollbar-width:none}
.fscroll::-webkit-scrollbar{display:none}
.fitem{position:relative;height:100%;scroll-snap-align:start;scroll-snap-stop:always;background:#000 center/contain no-repeat;display:flex;align-items:center;justify-content:center;overflow:hidden}
.fitem video{width:100%;height:100%;object-fit:contain;background:#000}
.ftop{position:absolute;top:0;left:0;right:0;z-index:3;display:flex;align-items:center;gap:10px;padding:calc(10px + env(safe-area-inset-top)) 12px 10px;background:linear-gradient(#000a,#0000)}
.ftop button{background:rgba(255,255,255,.18);color:#fff;border:0;border-radius:999px;padding:8px 14px;font-weight:700;font-size:14px}
.ftop .fc{margin-left:auto;font-size:13px;font-weight:700;opacity:.9}
.fside{position:absolute;right:10px;bottom:calc(110px + env(safe-area-inset-bottom));z-index:3;display:flex;flex-direction:column;gap:14px}
.fside button{width:64px;border:0;background:rgba(0,0,0,.45);color:#fff;border-radius:16px;padding:9px 4px;font-size:11.5px;font-weight:700;display:flex;flex-direction:column;align-items:center;gap:3px}
.fside button b{font-size:22px;line-height:1}
.fside button.done{background:var(--primary)}
.fcap{position:absolute;left:14px;right:86px;bottom:calc(26px + env(safe-area-inset-bottom));z-index:3;font-weight:800;font-size:15px;line-height:1.3;text-shadow:0 1px 4px #000}
.fcap small{display:block;font-weight:600;font-size:12px;opacity:.85;margin-top:3px}
.fbar{position:absolute;left:0;right:0;bottom:env(safe-area-inset-bottom);height:3px;background:rgba(255,255,255,.25);z-index:3}
.fbar i{display:block;height:100%;width:0;background:var(--accent-2)}
.fcenter{position:absolute;inset:0;z-index:2;display:flex;align-items:center;justify-content:center;pointer-events:none}
.fcenter span{background:rgba(0,0,0,.55);border-radius:999px;padding:12px 18px;font-weight:700;font-size:15px;opacity:0;transition:opacity .2s}
.fcenter span.on{opacity:1}
.fsheet{position:absolute;left:0;right:0;bottom:0;z-index:5;background:var(--paper);color:#383838;border-radius:22px 22px 0 0;padding:16px 18px calc(18px + env(safe-area-inset-bottom));max-height:72vh;overflow:auto;transform:translateY(105%);transition:transform .28s cubic-bezier(.2,.8,.2,1)}
.fsheet.show{transform:none}
.fsheet h3{margin:0 0 8px;color:var(--primary-2);font-size:17px}
.fsheet .qq{font-weight:700;margin:4px 0 10px;line-height:1.4}
.fsheet p{line-height:1.5;margin:0 0 10px;font-size:14.5px}
.fsheet .row2{display:flex;gap:10px;margin-top:12px}
.fsheet .row2 .btn{flex:1}
.fend{height:100%;scroll-snap-align:start;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:24px;text-align:center}
</style>'''
assert s.count('</style>') == 1
s = s.replace('</style>', CSS, 1)

JS = r'''
/* --- vídeos en feed --- */
function videoAnswer(tema,v,k,box){
  const q=L(v.q), ok=k===q.a; track("video-test/"+v.id+"/"+(ok?"acierto":"fallo"),"Test vídeo "+v.id,true);
  box.querySelectorAll(".opt").forEach(x=>{ x.disabled=true; const j=+x.dataset.k; if(j===q.a) x.classList.add("ok"); else if(j===k) x.classList.add("ko"); });
  const first=!S.prog.seen[tema.id+".videoq"]||!S.prog.seen[tema.id+".videoq"][v.id];
  if(ok&&first){ addXP(10); markSeen(tema.id,"videoq",v.id); toast(t("vOk",{n:10*(S.xpMult||1)})); } else if(!ok) toast(t("vKo"));
  const seen=S.prog.seen[tema.id+".videos"]||{}; if(!seen[v.id]) markSeen(tema.id,"videos",v.id);
  return ok;
}
function openFeed(tema,idxs,start,onClose){
  const vs=tema.videos; const answered=()=>S.prog.seen[tema.id+".videoq"]||{};
  const fd=document.createElement("div"); fd.className="feed";
  fd.innerHTML=`<div class="fscroll">${idxs.map((i,n)=>{ const v=vs[i]; return `<section class="fitem" data-n="${n}" style="background-image:url('${esc(L(v.poster))}')">
      <div class="fcenter"><span></span></div>
      <div class="fside"><button data-a="more"><b>📖</b>${t("vMoreB")}</button>${L(v.q)&&L(v.q).q?`<button data-a="test" class="${answered()[v.id]?"done":""}"><b>${answered()[v.id]?"✓":"❓"}</b>${t("vTestB")}</button>`:""}</div>
      <div class="fcap">${esc(L(v.title))}<small>${t("tema")} ${tema.num} · ${n+1}/${idxs.length}</small></div>
      <div class="fbar"><i></i></div></section>`; }).join("")}
      <section class="fend"><div style="font-size:40px">🏁</div><b style="font-size:18px">${t("vEnd")}</b><button class="btn" id="fEndBack">${t("vClose")}</button></section></div>
    <div class="ftop"><button id="fClose">✕ ${t("vClose")}</button><span class="fc" id="fCount"></span></div>
    <div class="fsheet" id="fSheet"></div>`;
  document.body.appendChild(fd); document.body.classList.add("feedon");
  const sc=fd.querySelector(".fscroll"), items=[...fd.querySelectorAll(".fitem")], sh=fd.querySelector("#fSheet");
  const vid=document.createElement("video"); vid.playsInline=true; vid.setAttribute("playsinline",""); vid.preload="auto";
  const pre=document.createElement("video"); pre.preload="auto"; pre.muted=true;
  let cur=-1, tracked={};
  const hint=(txt,ms)=>{ const sp=items[cur]&&items[cur].querySelector(".fcenter span"); if(!sp) return; sp.textContent=txt; sp.classList.add("on"); clearTimeout(hint.t); if(ms) hint.t=setTimeout(()=>sp.classList.remove("on"),ms); };
  const tryPlay=()=>{ vid.play().then(()=>{ if(!vid.muted) return; hint("🔇 "+t("vTap")); }).catch(()=>{ vid.muted=true; vid.play().then(()=>hint("🔇 "+t("vTap"))).catch(()=>hint("▶")); }); };
  function activate(n){
    if(n===cur||n<0||n>=items.length) return; cur=n; closeSh();
    const v=vs[idxs[n]]; items[n].insertBefore(vid,items[n].firstChild);
    vid.src=L(v.src); vid.poster=L(v.poster); vid.currentTime=0; tryPlay();
    fd.querySelector("#fCount").textContent=`${n+1}/${items.length}`;
    if(idxs[n+1]!=null){ pre.src=L(vs[idxs[n+1]].src); pre.load(); }
    if(!tracked[v.id]){ tracked[v.id]=1; track("video/"+v.id+"/"+S.lang,"Vídeo "+v.id,true); }
  }
  const io=new IntersectionObserver(es=>es.forEach(e=>{ if(e.isIntersecting&&e.intersectionRatio>=.6){ if(e.target.classList.contains("fend")){ vid.pause(); cur=-1; fd.querySelector("#fCount").textContent=""; } else activate(+e.target.dataset.n); } }),{root:sc,threshold:[.6]});
  items.forEach(it=>io.observe(it)); io.observe(fd.querySelector(".fend"));
  vid.addEventListener("timeupdate",()=>{ const b=items[cur]&&items[cur].querySelector(".fbar i"); if(b&&vid.duration) b.style.width=(vid.currentTime/vid.duration*100)+"%"; });
  vid.addEventListener("ended",()=>{ const v=vs[idxs[cur]]; const seen=S.prog.seen[tema.id+".videos"]||{}; if(!seen[v.id]) markSeen(tema.id,"videos",v.id);
    const q=L(v.q); if(q&&q.q&&!answered()[v.id]) showTest(true); else showNextOnly(); });
  sc.addEventListener("click",e=>{ if(e.target.closest(".fside")||e.target.closest(".fend")) return; if(sh.classList.contains("show")){ closeSh(); return; }
    if(vid.muted){ vid.muted=false; if(vid.paused) vid.play().catch(()=>{}); hint("🔊",700); return; }
    if(vid.paused){ vid.play().catch(()=>{}); hint("▶",500); } else { vid.pause(); hint("❚❚"); } });
  function closeSh(){ sh.classList.remove("show"); }
  function goNext(){ closeSh(); const nx=items[cur+1]||fd.querySelector(".fend"); nx.scrollIntoView({behavior:"smooth"}); }
  function showMore(){ const v=vs[idxs[cur]]; vid.pause();
    sh.innerHTML=`<h3>${t("vMore")}</h3>${String(L(v.more)).split(/\n+/).map(p=>`<p>${md(p)}</p>`).join("")}<div class="row2"><button class="btn sec" id="fsX">${t("close")}</button></div>`;
    sh.classList.add("show"); sh.querySelector("#fsX").onclick=()=>{ closeSh(); vid.play().catch(()=>{}); }; }
  function showTest(fromEnd){ const v=vs[idxs[cur]], q=L(v.q); if(!(q&&q.q)) return; if(!fromEnd) vid.pause();
    sh.innerHTML=`<h3>${t("vTest")}</h3><div class="qq">${esc(q.q)}</div><div class="opts">${q.opts.map((o,k)=>`<button class="opt" data-k="${k}"><span class="k">${"ABCD"[k]}</span><span>${esc(o)}</span></button>`).join("")}</div>
      <div class="row2"><button class="btn sec" id="fsX">${t("close")}</button><button class="btn" id="fsN">${t("vNext")}</button></div>`;
    sh.classList.add("show");
    sh.querySelectorAll(".opt").forEach(b=>b.onclick=()=>{ videoAnswer(tema,v,+b.dataset.k,sh); const tb=items[cur].querySelector('[data-a="test"]'); if(tb){ tb.classList.add("done"); tb.querySelector("b").textContent="✓"; } });
    sh.querySelector("#fsX").onclick=closeSh; sh.querySelector("#fsN").onclick=goNext; }
  function showNextOnly(){ sh.innerHTML=`<div class="row2"><button class="btn sec" id="fsR">↺</button><button class="btn" id="fsN">${t("vNext")}</button></div>`; sh.classList.add("show");
    sh.querySelector("#fsR").onclick=()=>{ closeSh(); vid.currentTime=0; vid.play().catch(()=>{}); }; sh.querySelector("#fsN").onclick=goNext; }
  fd.querySelectorAll(".fside button").forEach(b=>b.onclick=e=>{ e.stopPropagation(); if(b.dataset.a==="more") showMore(); else showTest(false); });
  const close=()=>{ io.disconnect(); vid.pause(); vid.removeAttribute("src"); pre.removeAttribute("src"); fd.remove(); document.body.classList.remove("feedon"); onClose&&onClose(); };
  fd.querySelector("#fClose").onclick=close; fd.querySelector("#fEndBack").onclick=close;
  requestAnimationFrame(()=>{ items[start].scrollIntoView(); activate(start); });
}
'''
anchor = 'function modeVideos(tema,mode,m){'
assert anchor in s
s = s.replace(anchor, JS + '\n' + anchor, 1)

old = '''    m.innerHTML=`<div class="vlist">${idxs.map('''
assert old in s
s = s.replace(old, '''    m.innerHTML=`<button class="btn vfeedbtn" id="vFeed">${t("vFeed")}<small>${t("vFeedSub")}</small></button><div class="vlist">${idxs.map(''', 1)
old = '''    m.querySelectorAll(".vcard").forEach(b=>b.onclick=()=>open(+b.dataset.i));'''
assert old in s
s = s.replace(old, old + '''
    const fb=m.querySelector("#vFeed"); if(fb) fb.onclick=()=>{ const st=Math.max(0,idxs.findIndex(i=>!(S.prog.seen[tema.id+".videos"]||{})[vs[i].id])); openFeed(tema,idxs,st,()=>{ Object.assign(seen,S.prog.seen[tema.id+".videos"]||{}); list(); }); };''', 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
