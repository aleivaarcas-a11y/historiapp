# Historiapp · ranking de alumnos (10-10-2026). Uso: python3 tools/patch_ranking.py  (desde la carpeta Historiapp)
import re, shutil, sys
P = "index.html"
s = open(P, encoding="utf-8").read()
if "/* ============ ranking ============ */" in s:
    sys.exit("El parche del ranking ya está aplicado.")
shutil.copy(P, "tools/index_antes_ranking.html")

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f"No encuentro (o hay {c}): {old[:70]!r}")
    s = s.replace(old, new)

CSS = r"""
.hoy .rkc{background:var(--soft);border-color:var(--primary)}
.hoy .rkc .ic{background:var(--primary)}
.hoy .rkc .xp{border-color:var(--primary)}
.rk-seg{display:flex;margin:2px 0 12px}.rk-seg button{flex:1}
.rk-list{padding:6px}
.rk-h{font-size:13px;font-weight:700;color:var(--muted);margin:4px 10px 8px}
.rk-row{display:flex;align-items:center;gap:12px;padding:11px 12px;border-bottom:1px solid var(--line)}
.rk-row:last-child{border-bottom:0}
.rk-row.me{background:var(--ok-bg);border-radius:12px;border-bottom-color:transparent}
.rk-p{flex:0 0 34px;text-align:center;font-weight:800;font-size:17px;color:var(--tp)}
.rk-a{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:700}
.rk-a small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.rk-row b{font-variant-numeric:tabular-nums}
.rk-gap{text-align:center;color:var(--muted);padding:2px;letter-spacing:3px}
.rk-note,.rk-msg{font-size:12.5px;color:var(--muted);text-align:center;margin:12px 6px;line-height:1.5}
.rk-form h2{margin:0 0 6px;font-size:19px}
.rk-form p{line-height:1.5}
.rk-form label{display:block;font-weight:700;font-size:13.5px;margin:12px 0 0}
.rk-form input,.rk-form select{display:block;width:100%;box-sizing:border-box;margin-top:5px;padding:11px 12px;border:1px solid var(--line);border-radius:12px;font:inherit;font-size:16px;background:var(--paper);color:var(--ink)}
.rk-form label small{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:4px}
.rk-priv{font-size:12.5px;color:var(--muted);margin:14px 0 4px}
.rk-err{color:var(--ko);font-weight:700;font-size:14px;min-height:1em;margin:8px 0}
.rk-set{display:flex;align-items:center;justify-content:space-between;gap:10px}
.rk-set button{color:var(--ko);font-weight:700;font-size:13.5px;padding:6px 0}
.rk-set .go{color:var(--tp)}
"""
i = s.index("</style>"); s = s[:i] + CSS + s[i:]

JS = r"""
/* ============ ranking ============ */
const RK_URL="https://script.google.com/macros/s/AKfycbzjxo9QvXjWabkFGm3MtbgTJWV1OMT372TAD7n-iTSoSR7av2KMpYBb3LhRfXvWt36GeA/exec";
const RK_GRUPOS=["1ºA","1ºB","1ºTAMA","1ºEnglish"];
Object.assign(I18N.es,{rkT:"Ranking",rkCard:"Ranking semanal",rkJoinSub:"Apúntate con un alias y compite con tu clase",rkPos:"Vas {p}.º de {n} esta semana",rkNoPts:"Aún no tienes puntos esta semana",
 rkWeek:"Esta semana",rkGroup:"Mi grupo",rkTotal:"Total",rkReset:"El ranking semanal se reinicia cada lunes. Cuentan los puntos ganados desde que te apuntas, con un máximo de 1.500 al día.",
 rkEmpty:"Todavía no hay nadie con puntos en esta clasificación.",rkLoading:"Cargando…",rkOffline:"No se ha podido cargar el ranking. Revisa la conexión.",
 rkJoinT:"Apúntate al ranking",rkJoinIntro:"El ranking es voluntario. Los demás solo verán tu alias y tu grupo.",rkName:"Nombre",rkAp1:"Primer apellido",rkAp2:"Segundo apellido (opcional)",
 rkGroupL:"Grupo",rkGroupPick:"Elige tu grupo",rkAlias:"Alias público",rkAliasHint:"Entre 3 y 16 caracteres: letras, números, espacios, punto, guion o guion bajo.",
 rkPriv:"Tu nombre y tus apellidos solo los ve el profesor y sirven para identificar a quien haga un mal uso del ranking. Los alias ofensivos se rechazan y el profesor puede retirar cualquier alias. Puedes salir del ranking cuando quieras desde Ajustes, y tus datos se borrarán.",
 rkJoinBtn:"Entrar en el ranking",rkSending:"Enviando…",rkErr:{alias:"El alias no es válido.",veto:"Ese alias no está permitido. Elige otro.",ocupado:"Ese alias ya lo usa otra persona.",grupo:"Elige tu grupo.",nombre:"Escribe tu nombre y tu primer apellido reales.",red:"No hay conexión. Inténtalo de nuevo.",otro:"Algo ha fallado. Inténtalo de nuevo."},
 rkRetired:"El profesor ha retirado tu alias. Elige otro para volver al ranking.",rkNewAlias:"Nuevo alias",rkSave:"Guardar",rkSet:"Ranking",rkSetOn:"{a} · {g}",rkSetOff:"No estás en el ranking",rkJoinGo:"Apuntarme",
 rkLeave:"Salir del ranking",rkLeaveConfirm:"Se borrarán del ranking tu alias, tu grupo, tu nombre y tus puntos. Tu progreso en la app no cambia. ¿Continuar?",rkLeft:"Has salido del ranking",rkJoined:"Ya estás en el ranking",rkPts:"pts"});
Object.assign(I18N.en,{rkT:"Leaderboard",rkCard:"Weekly leaderboard",rkJoinSub:"Join with a nickname and compete with your class",rkPos:"You are #{p} of {n} this week",rkNoPts:"No points yet this week",
 rkWeek:"This week",rkGroup:"My group",rkTotal:"Overall",rkReset:"The weekly leaderboard resets every Monday. Points count from the moment you join, up to 1,500 a day.",
 rkEmpty:"Nobody has points in this ranking yet.",rkLoading:"Loading…",rkOffline:"The leaderboard could not be loaded. Check your connection.",
 rkJoinT:"Join the leaderboard",rkJoinIntro:"Joining is optional. Other students will only see your nickname and your group.",rkName:"First name",rkAp1:"Surname",rkAp2:"Second surname (optional)",
 rkGroupL:"Group",rkGroupPick:"Choose your group",rkAlias:"Public nickname",rkAliasHint:"3 to 16 characters: letters, numbers, spaces, full stop, hyphen or underscore.",
 rkPriv:"Only the lecturer can see your name and surnames, which are used to identify anyone who misuses the leaderboard. Offensive nicknames are rejected and the lecturer can remove any nickname. You can leave the leaderboard at any time from Settings, and your data will be deleted.",
 rkJoinBtn:"Join the leaderboard",rkSending:"Sending…",rkErr:{alias:"That nickname is not valid.",veto:"That nickname is not allowed. Choose another one.",ocupado:"Someone else is already using that nickname.",grupo:"Choose your group.",nombre:"Enter your real first name and surname.",red:"No connection. Please try again.",otro:"Something went wrong. Please try again."},
 rkRetired:"The lecturer has removed your nickname. Choose another one to rejoin the leaderboard.",rkNewAlias:"New nickname",rkSave:"Save",rkSet:"Leaderboard",rkSetOn:"{a} · {g}",rkSetOff:"You are not on the leaderboard",rkJoinGo:"Join",
 rkLeave:"Leave the leaderboard",rkLeaveConfirm:"Your nickname, group, name and points will be deleted from the leaderboard. Your progress in the app will not change. Continue?",rkLeft:"You have left the leaderboard",rkJoined:"You are on the leaderboard",rkPts:"pts"});
function rkGet(){ return load("historiapp.ranking",null); }
function rkSave(r){ try{ if(r) localStorage.setItem("historiapp.ranking",JSON.stringify(r)); else localStorage.removeItem("historiapp.ranking"); }catch(e){} }
function rkNewUid(){ try{ return Array.from(crypto.getRandomValues(new Uint8Array(12)),b=>b.toString(36).padStart(2,"0")).join(""); }catch(e){ return (Date.now().toString(36)+Math.random().toString(36).slice(2)+Math.random().toString(36).slice(2)).replace(/[^a-z0-9]/g,"").slice(0,24); } }
async function rkPost(body){ const r=await fetch(RK_URL,{method:"POST",keepalive:true,headers:{"Content-Type":"text/plain;charset=utf-8"},body:JSON.stringify(body)}); return r.json(); }
async function rkFetch(force){ const r=rkGet(); if(!r) return null; if(!force&&S.rkData&&Date.now()-S.rkData.at<60000) return S.rkData.d;
  const d=await fetch(RK_URL+"?uid="+encodeURIComponent(r.uid)).then(x=>x.json()); S.rkData={at:Date.now(),d}; return d; }
let RK_T=null, RK_BUSY=false;
function rkQueue(ms){ const r=rkGet(); if(!r||r.retirado) return; clearTimeout(RK_T); RK_T=setTimeout(rkSync,ms==null?5000:ms); }
async function rkSync(){ const r=rkGet(); if(!r||r.retirado||RK_BUSY||r.sent===S.prog.xp) return; RK_BUSY=true;
  try{ const x=S.prog.xp; const j=await rkPost({uid:r.uid,alias:r.alias,grupo:r.grupo,nombre:r.nombre,apellido1:r.apellido1,apellido2:r.apellido2,xp:x});
    const r2=rkGet(); if(!r2) return;
    if(j.ok){ r2.sent=x; rkSave(r2); S.rkData=null; }
    else if(j.err==="retirado"){ r2.retirado=true; rkSave(r2); toast(t("rkRetired"),3500); }
  }catch(e){} finally{ RK_BUSY=false; } }
document.addEventListener("visibilitychange",()=>{ if(document.visibilityState==="hidden") rkSync(); });
setTimeout(rkSync,4000);
function rkErrMsg(e){ return t("rkErr."+(["alias","veto","ocupado","grupo","nombre","red"].includes(e)?e:"otro")); }
function rkHomeCard(hoy){
  const r=rkGet(), c=document.createElement("button"); c.className="card reto rkc";
  c.innerHTML=`<div class="ic" aria-hidden="true">🏆</div><div class="tx"><small>${t("rkCard")}</small><b>${r?esc(r.alias):t("rkJoinT")}</b><span id="rkcSub">${r?(r.retirado?t("rkRetired"):t("rkLoading")):t("rkJoinSub")}</span></div><div class="xp">›</div>`;
  c.onclick=()=>nav({name:"ranking",back:{name:"home"}}); hoy.appendChild(c);
  if(r&&!r.retirado) rkFetch().then(d=>{ const e=document.getElementById("rkcSub"); if(!e||!d||!d.ok) return; e.textContent=d.sem.yo?t("rkPos",{p:d.sem.yo.p,n:d.sem.n}):t("rkNoPts"); }).catch(()=>{ const e=document.getElementById("rkcSub"); if(e) e.textContent=""; });
}
async function renderRanking(){
  const v=S.view; app.innerHTML=header(t("rkT"),true)+`<main id="rkM"></main>`; bindHeader(()=>nav(v.back||{name:"home"}));
  const m=document.getElementById("rkM"), r=rkGet();
  if(!r) return rkForm(m);
  if(r.retirado) return rkAliasForm(m,r);
  S.rkTab=S.rkTab||"sem";
  m.innerHTML=`<div class="seg rk-seg"><button data-k="sem">${t("rkWeek")}</button><button data-k="grp">${t("rkGroup")}</button><button data-k="total">${t("rkTotal")}</button></div>
    <div class="card rk-list" id="rkL"><p class="rk-msg">${t("rkLoading")}</p></div><p class="rk-note">${t("rkReset")}</p>`;
  let data=null; const L_=document.getElementById("rkL");
  const draw=()=>{ m.querySelectorAll(".rk-seg button").forEach(b=>b.classList.toggle("on",b.dataset.k===S.rkTab)); if(!data) return;
    const T=S.rkTab==="grp"?(data.grupos||{})[r.grupo]:data[S.rkTab]; if(!T){ L_.innerHTML=`<p class="rk-msg">${t("rkEmpty")}</p>`; return; }
    const row=(x)=>`<div class="rk-row${x.yo?" me":""}"><span class="rk-p">${x.p<=3?["🥇","🥈","🥉"][x.p-1]:x.p}</span><span class="rk-a">${esc(x.alias)}<small>${esc(x.grupo||"")}</small></span><b>${x.pts} ${t("rkPts")}</b></div>`;
    let h=S.rkTab==="grp"?`<div class="rk-h">${esc(r.grupo)}</div>`:"";
    h+=T.top.length?T.top.map(row).join(""):`<p class="rk-msg">${t("rkEmpty")}</p>`;
    if(T.yo&&T.yo.p>10) h+=`<div class="rk-gap">···</div>`+row({p:T.yo.p,alias:r.alias,grupo:r.grupo,pts:T.yo.pts,yo:true});
    else if(!T.yo&&T.top.length) h+=`<p class="rk-msg">${t("rkNoPts")}</p>`;
    L_.innerHTML=h; };
  m.querySelectorAll(".rk-seg button").forEach(b=>b.onclick=()=>{ S.rkTab=b.dataset.k; draw(); }); draw();
  try{ await rkSync(); data=await rkFetch(true); }catch(e){ L_.innerHTML=`<p class="rk-msg">${t("rkOffline")}</p>`; return; }
  if(S.view.name!=="ranking") return;
  if(data&&data.retirado){ r.retirado=true; rkSave(r); return renderRanking(); }
  if(data&&data.existe===false){ rkSave(null); return renderRanking(); }
  draw();
}
function rkForm(m){
  m.innerHTML=`<div class="card rk-form"><h2>${t("rkJoinT")}</h2><p>${t("rkJoinIntro")}</p>
    <label>${t("rkName")}<input id="rkN" autocomplete="given-name" maxlength="40"></label>
    <label>${t("rkAp1")}<input id="rkA1" autocomplete="family-name" maxlength="40"></label>
    <label>${t("rkAp2")}<input id="rkA2" maxlength="40"></label>
    <label>${t("rkGroupL")}<select id="rkG"><option value="">${t("rkGroupPick")}</option>${RK_GRUPOS.map(g=>`<option value="${g}">${g}</option>`).join("")}</select></label>
    <label>${t("rkAlias")}<input id="rkAl" maxlength="16" autocomplete="off" autocapitalize="off"><small>${t("rkAliasHint")}</small></label>
    <p class="rk-priv">🔒 ${t("rkPriv")}</p><p class="rk-err" id="rkE" role="alert"></p>
    <button class="btn" id="rkGo">${t("rkJoinBtn")}</button></div>`;
  const $=id=>document.getElementById(id), E=$("rkE"), go=$("rkGo");
  go.onclick=async()=>{ const d={nombre:$("rkN").value.trim(),apellido1:$("rkA1").value.trim(),apellido2:$("rkA2").value.trim(),grupo:$("rkG").value,alias:$("rkAl").value.replace(/\s+/g," ").trim()};
    if(!d.nombre||!d.apellido1) return E.textContent=rkErrMsg("nombre");
    if(!d.grupo) return E.textContent=rkErrMsg("grupo");
    if(d.alias.length<3||d.alias.length>16||!/^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _.\-]+$/.test(d.alias)) return E.textContent=rkErrMsg("alias");
    E.textContent=""; go.disabled=true; go.textContent=t("rkSending");
    const uid=rkNewUid(), x=S.prog.xp; let j;
    try{ j=await rkPost(Object.assign({uid,xp:x},d)); }catch(e){ j={ok:false,err:"red"}; }
    go.disabled=false; go.textContent=t("rkJoinBtn");
    if(!j.ok) return E.textContent=rkErrMsg(j.err);
    rkSave(Object.assign({uid,sent:x},d)); S.rkData=null; track("ranking/alta/"+d.grupo,"Ranking",true); toast(t("rkJoined")); celebrate(); renderRanking(); };
}
function rkAliasForm(m,r){
  m.innerHTML=`<div class="card rk-form"><p>${t("rkRetired")}</p>
    <label>${t("rkNewAlias")}<input id="rkAl" maxlength="16" autocomplete="off" autocapitalize="off"><small>${t("rkAliasHint")}</small></label>
    <p class="rk-err" id="rkE" role="alert"></p><button class="btn" id="rkGo">${t("rkSave")}</button>
    <button class="btn ghost" id="rkOut">${t("rkLeave")}</button></div>`;
  const E=document.getElementById("rkE"), go=document.getElementById("rkGo");
  document.getElementById("rkOut").onclick=async()=>{ if(await rkLeave()) nav({name:"home"}); };
  go.onclick=async()=>{ const a=document.getElementById("rkAl").value.replace(/\s+/g," ").trim();
    if(a.length<3||a.length>16||!/^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _.\-]+$/.test(a)) return E.textContent=rkErrMsg("alias");
    if(a.toLowerCase()===String(r.alias).toLowerCase()) return E.textContent=rkErrMsg("veto");
    go.disabled=true; let j; const x=S.prog.xp;
    try{ j=await rkPost({uid:r.uid,alias:a,grupo:r.grupo,nombre:r.nombre,apellido1:r.apellido1,apellido2:r.apellido2,xp:x}); }catch(e){ j={ok:false,err:"red"}; }
    go.disabled=false; if(!j.ok) return E.textContent=rkErrMsg(j.err);
    r.alias=a; r.retirado=false; r.sent=x; rkSave(r); S.rkData=null; toast(t("rkJoined")); renderRanking(); };
}
async function rkLeave(){ const r=rkGet(); if(!r) return true; if(!confirm(t("rkLeaveConfirm"))) return false;
  try{ const j=await rkPost({uid:r.uid,accion:"baja"}); if(!j.ok) throw 0; }catch(e){ toast(rkErrMsg("red"),2500); return false; }
  rkSave(null); S.rkData=null; track("ranking/baja","Ranking",true); toast(t("rkLeft")); return true; }
function rkSettingsBox(from){ const box=document.getElementById("sRk"); if(!box) return; const r=rkGet();
  box.innerHTML=`<div class="rk-set"><div><b>🏆 ${t("rkSet")}</b><br><small style="color:var(--muted)">${r?esc(t("rkSetOn",{a:r.alias,g:r.grupo})):t("rkSetOff")}</small></div>${r?`<button id="sRkOut">${t("rkLeave")}</button>`:`<button class="go" id="sRkIn">${t("rkJoinGo")} ›</button>`}</div>`;
  if(r) document.getElementById("sRkOut").onclick=async()=>{ if(await rkLeave()) nav({name:"settings",from}); };
  else document.getElementById("sRkIn").onclick=()=>nav({name:"ranking",back:{name:"settings",from}});
}

"""
rep("/* ============ modes ============ */", JS + "/* ============ modes ============ */")

# rutas
rep('if(v.name==="settings") return "ajustes";', 'if(v.name==="settings") return "ajustes"; if(v.name==="ranking") return "ranking";')
rep('if(h==="ajustes") return {name:"settings"};', 'if(h==="ajustes") return {name:"settings"}; if(h==="ranking") return {name:"ranking"};')
rep('  if(v.name==="settings") return renderSettings();', '  if(v.name==="settings") return renderSettings();\n  if(v.name==="ranking") return renderRanking();')
# envío de puntos
rep("const before=levelOf(S.prog.xp); S.prog.xp+=n;", "const before=levelOf(S.prog.xp); S.prog.xp+=n; rkQueue();")
# tarjeta en la portada
rep('rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc);', 'rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc); rkHomeCard(hoy);')
# ajustes
rep('<button class="btn" id="sInstall">', '<div class="card" id="sRk"></div>\n    <button class="btn" id="sInstall">')
rep('document.getElementById("sInstall").onclick=installApp;', 'document.getElementById("sInstall").onclick=installApp; rkSettingsBox(from);')
# cerrar sesión: dar de baja también del ranking
rep('track("sesion/cerrada","Cerrar sesión",true);', 'track("sesion/cerrada","Cerrar sesión",true); try{ const r=rkGet(); if(r) fetch(RK_URL,{method:"POST",keepalive:true,headers:{"Content-Type":"text/plain;charset=utf-8"},body:JSON.stringify({uid:r.uid,accion:"baja"})}); }catch(_){}')

open(P, "w", encoding="utf-8").write(s)
w = open("sw.js", encoding="utf-8").read()
m = re.search(r'historiapp-v(\d+)', w); w = w.replace(m.group(0), "historiapp-v%d" % (int(m.group(1))+1)); open("sw.js","w",encoding="utf-8").write(w)
print("Ranking aplicado. Copia previa en tools/index_antes_ranking.html; service worker", "v%d" % (int(m.group(1))+1))
