# Historiapp · ver el ranking sin apuntarse (10-10-2026). Uso: python3 tools/patch_ranking_ver.py
# Enlace discreto en el formulario de alta; dura hasta cerrar la app.
import re, sys
P="index.html"; s=open(P,encoding="utf-8").read()
if "rkJustLook" in s: sys.exit("Ya aplicado.")
def rep(old,new):
    global s
    if s.count(old)!=1: sys.exit("No encuentro: "+old[:80])
    s=s.replace(old,new)
rep('Object.assign(I18N.es,{','Object.assign(I18N.es,{rkJustLook:"Solo quiero verlo, sin apuntarme",rkLooking:"Estás viendo el ranking sin apuntarte.",rkJoinNow:"Apuntarme",')
rep('Object.assign(I18N.en,{','Object.assign(I18N.en,{rkJustLook:"Just let me look, without joining",rkLooking:"You are viewing the leaderboard without joining.",rkJoinNow:"Join",')
rep('async function rkFetch(force){ const r=rkGet(); if(!r) return null;',
    'async function rkFetch(force){ const r=rkGet()||(S.rkVer?{uid:"visitante000"}:null); if(!r) return null;')

a=s.index("async function renderRanking(){"); b=s.index("function rkForm(m){")
s=s[:a]+r'''async function renderRanking(){
  const v=S.view; app.innerHTML=header(t("rkT"),true)+`<main id="rkM"></main>`; bindHeader(()=>nav(v.back||{name:"home"}));
  const m=document.getElementById("rkM"), r=rkGet(), ver=!r&&S.rkVer;
  if(!r&&!ver) return rkForm(m);
  if(r&&r.retirado) return rkAliasForm(m,r);
  const me=r||{alias:"",grupo:S.rkGrp||RK_GRUPOS[0]};
  S.rkTab=S.rkTab||"sem";
  m.innerHTML=`${ver?`<div class="rk-ver"><span>${t("rkLooking")}</span><button id="rkJoinNow">${t("rkJoinNow")} ›</button></div>`:""}<div class="seg rk-seg"><button data-k="sem">${t("rkWeek")}</button><button data-k="grp">${ver?t("rkGroupL"):t("rkGroup")}</button><button data-k="total">${t("rkTotal")}</button></div>
    <div class="card rk-list" id="rkL"><p class="rk-msg">${t("rkLoading")}</p></div><p class="rk-note">${t("rkReset")}</p>`;
  if(ver) document.getElementById("rkJoinNow").onclick=()=>{ S.rkVer=false; renderRanking(); };
  let data=null; const L_=document.getElementById("rkL");
  const draw=()=>{ m.querySelectorAll(".rk-seg button").forEach(b=>b.classList.toggle("on",b.dataset.k===S.rkTab)); if(!data) return;
    const T=S.rkTab==="grp"?(data.grupos||{})[me.grupo]:data[S.rkTab];
    const row=(x)=>`<div class="rk-row${x.yo?" me":""}"><span class="rk-p">${x.p<=3?["🥇","🥈","🥉"][x.p-1]:x.p}</span><span class="rk-a">${esc(x.alias)}<small>${esc(x.grupo||"")}</small></span><b>${x.pts} ${t("rkPts")}</b></div>`;
    let h="";
    if(S.rkTab==="grp") h=ver?`<div class="rk-h"><select id="rkGs" aria-label="${esc(t("rkGroupL"))}">${RK_GRUPOS.map(g=>`<option${g===me.grupo?" selected":""}>${g}</option>`).join("")}</select></div>`:`<div class="rk-h">${esc(me.grupo)}</div>`;
    if(!T) h+=`<p class="rk-msg">${t("rkEmpty")}</p>`;
    else { h+=T.top.length?T.top.map(row).join(""):`<p class="rk-msg">${t("rkEmpty")}</p>`;
      if(r&&T.yo&&T.yo.p>10) h+=`<div class="rk-gap">···</div>`+row({p:T.yo.p,alias:me.alias,grupo:me.grupo,pts:T.yo.pts,yo:true});
      else if(r&&!T.yo&&T.top.length) h+=`<p class="rk-msg">${t("rkNoPts")}</p>`; }
    L_.innerHTML=h;
    const gs=document.getElementById("rkGs"); if(gs) gs.onchange=()=>{ me.grupo=S.rkGrp=gs.value; draw(); }; };
  m.querySelectorAll(".rk-seg button").forEach(b=>b.onclick=()=>{ S.rkTab=b.dataset.k; draw(); }); draw();
  try{ await rkSync(); data=await rkFetch(true); }catch(e){ L_.innerHTML=`<p class="rk-msg">${t("rkOffline")}</p>`; return; }
  if(S.view.name!=="ranking") return;
  if(r&&data&&data.retirado){ r.retirado=true; rkSave(r); return renderRanking(); }
  if(r&&data&&data.existe===false){ rkSave(null); return renderRanking(); }
  draw();
}
'''+s[b:]
# enlace discreto bajo el botón de alta
rep('<button class="btn" id="rkGo">${t("rkJoinBtn")}</button></div>`;\n  const $=id=>document.getElementById(id), E=$("rkE"), go=$("rkGo");',
    '<button class="btn" id="rkGo">${t("rkJoinBtn")}</button>\n    <button class="btn ghost" id="rkLook">${t("rkJustLook")}</button></div>`;\n  const $=id=>document.getElementById(id), E=$("rkE"), go=$("rkGo");\n  $("rkLook").onclick=()=>{ S.rkVer=true; renderRanking(); };')
CSS='.rk-ver{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 12px;font-size:13px;color:var(--muted)}\n.rk-ver button{color:var(--tp);font-weight:700;font-size:13.5px;white-space:nowrap}\n.rk-h select{font:inherit;font-size:16px;font-weight:700;padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:var(--paper);color:var(--ink)}\n'
i=s.index("</style>"); s=s[:i]+CSS+s[i:]
open(P,"w",encoding="utf-8").write(s)
w=open("sw.js",encoding="utf-8").read(); m=re.search(r'historiapp-v(\d+)',w); n=int(m.group(1))+1
open("sw.js","w",encoding="utf-8").write(w.replace(m.group(0),"historiapp-v%d"%n)); print("Ver sin apuntarse aplicado; service worker v%d"%n)
