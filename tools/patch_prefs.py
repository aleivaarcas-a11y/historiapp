import re
p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,c=1):
    global s; assert s.count(o)==c,(o[:70],s.count(o)); s=s.replace(o,n)
# ---------- vars & dark ----------
rep("  --line:#e6e6e6; --radius:18px; --shadow:0 4px 18px rgba(0,32,96,.10);",
"""  --line:#e6e6e6; --radius:18px; --shadow:0 4px 18px rgba(0,32,96,.10);
  --tp:var(--primary); --tp2:var(--primary-2); --warm:#fff8e1; --warm2:#FFF3D6; --soft:#EAF1F8; --soft2:#f3f5f8; --wink:#8A5A00;""")
rep("@font-face{font-family:\"Carlito\";src:url(\"fonts/Carlito-Regular.woff2\")",
"""html.dark{--bg:#0e141b;--paper:#17212c;--ink:#e3e8ee;--muted:#9aa6b3;--line:#2b3848;--tp:#8fc0f0;--tp2:#d9e8f8;--warm:#2d2511;--warm2:#382d12;--soft:#1c2b3b;--soft2:#1f2935;--ok-bg:#16304a;--ko-bg:#3b2615;--wink:#f1c35a;--shadow:0 4px 18px rgba(0,0,0,.45);color-scheme:dark}
html.dark img{filter:brightness(.92)}
#app main{zoom:var(--fs,1)}
@font-face{font-family:"Carlito";src:url("fonts/Carlito-Regular.woff2")""")
s=s.replace("color:var(--primary-2)","color:var(--tp2)").replace("color:var(--primary)","color:var(--tp)")
s=re.sub(r"background:#fff(?![0-9a-fA-F])","background:var(--paper)",s)
for c,v in [("#fff8e1","--warm"),("#EAF1F8","--soft"),("#f3f5f8","--soft2"),("#F4F7FB","--soft2"),("#e9eef4","--soft2"),("#F1F3F6","--soft2"),("#FFF3D6","--warm2"),("#FFE7A3","--warm2")]:
    s=re.sub("background:"+c+r"(?![0-9a-fA-F])","background:var("+v+")",s,flags=re.I)
for c in ["#383838","#444"]: s=re.sub("color:"+c+r"(?![0-9a-fA-F])","color:var(--ink)",s)
for c in ["#8A5A00","#7A4A00","#C77700"]: s=s.replace("color:"+c,"color:var(--wink)")
s=s.replace("linear-gradient(170deg,#eaf1fb,#fff 60%)","linear-gradient(170deg,var(--soft),var(--paper) 60%)")
# ---------- enc font -> global ----------
for a in ["calc(17px * var(--encfs,1))","calc(15.5px * var(--encfs,1))","calc(16px * var(--encfs,1))","calc(13px * var(--encfs,1))"]:
    s=s.replace(a,a.split("*")[0].replace("calc(","").strip())
rep('function encFs(){ try{ const v=parseFloat(localStorage.getItem("historiapp.encfs")); return v>=0.9&&v<=1.5?v:1; }catch(_){ return 1; } }',
'function encFs(){ return prefFs(); }')
rep('<main style="--encfs:${encFs()}">','<main>')
i=s.index('  const fsSet=d=>{'); j=s.index("\n",i)
s=s[:i]+'''  const fsSet=d=>{ const f=setFs(prefFs()+d); document.getElementById("fsD").disabled=f<=FS_MIN; document.getElementById("fsU").disabled=f>=FS_MAX; };'''+s[j:]
# ---------- prefs core ----------
PREF='''const FS_MIN=0.9, FS_MAX=1.4;
function getPref(k,d){ try{ const v=localStorage.getItem("historiapp."+k); return v===null?d:v; }catch(_){ return d; } }
function setPref(k,v){ try{ localStorage.setItem("historiapp."+k,String(v)); }catch(_){} }
function prefFs(){ const v=parseFloat(getPref("fs",getPref("encfs","1"))); return v>=FS_MIN&&v<=FS_MAX?v:1; }
function setFs(v){ const f=Math.min(FS_MAX,Math.max(FS_MIN,Math.round(v*10)/10)); setPref("fs",f); applyPrefs(); return f; }
function applyPrefs(){ const th=getPref("theme","auto"); let dk=th==="dark"; if(th==="auto"){ try{ dk=matchMedia("(prefers-color-scheme: dark)").matches; }catch(_){} }
  const r=document.documentElement; r.classList.toggle("dark",dk); r.style.setProperty("--fs",prefFs());
  const m=document.querySelector('meta[name="theme-color"]'); if(m) m.setAttribute("content",dk?"#0e141b":"#004379"); }
applyPrefs(); try{ matchMedia("(prefers-color-scheme: dark)").addEventListener("change",applyPrefs); }catch(_){}
'''
rep('function renderSettings(){',PREF+'function renderSettings(){')
# settings rows
rep('''      <div class="set-row"><span>${t("xp")}</span><b>${S.prog.xp}</b></div>''',
'''      <div class="set-row"><span>${t("themeL")}</span><div class="seg"><button id="thL" class="${getPref("theme","auto")==="light"?"on":""}">${t("themeLight")}</button><button id="thD" class="${getPref("theme","auto")==="dark"?"on":""}">${t("themeDark")}</button><button id="thA" class="${getPref("theme","auto")==="auto"?"on":""}">${t("themeAuto")}</button></div></div>
      <div class="set-row"><span>${t("fsLbl")}</span><div class="seg"><button id="fsD2" aria-label="${esc(t("fsDown"))}" style="font-size:13px">A−</button><button id="fsV" disabled style="min-width:58px">${Math.round(prefFs()*100)} %</button><button id="fsU2" aria-label="${esc(t("fsUp"))}" style="font-size:18px">A+</button></div></div>
      <div class="set-row"><span>${t("xp")}</span><b>${S.prog.xp}</b></div>''')
rep('''  document.getElementById("sGuide").onclick=()=>nav({name:"guia",from});''','''  document.getElementById("sGuide").onclick=()=>nav({name:"guia",from});
  [["thL","light"],["thD","dark"],["thA","auto"]].forEach(([id,v])=>document.getElementById(id).onclick=()=>{ setPref("theme",v); applyPrefs(); nav({name:"settings",from}); });
  const fsu=d=>{ const f=setFs(prefFs()+d); document.getElementById("fsV").textContent=Math.round(f*100)+" %"; };
  document.getElementById("fsD2").onclick=()=>fsu(-0.1); document.getElementById("fsU2").onclick=()=>fsu(0.1);''')
rep('tabSearch:"Buscar",','tabSearch:"Buscar", themeL:"Tema", themeLight:"Claro", themeDark:"Oscuro", themeAuto:"Auto", famAll:"Todas las familias", share:"Compartir", shareHint:"Imagen lista para tus historias", shareTag:"Historia del Deporte · UCAM",')
rep('tabSearch:"Search",','tabSearch:"Search", themeL:"Theme", themeLight:"Light", themeDark:"Dark", themeAuto:"Auto", famAll:"All families", share:"Share", shareHint:"Image ready for your stories", shareTag:"History of Sport · UCAM",')
# ---------- enc family filter ----------
rep('''  const q0=S.view.q||"";
  app.innerHTML=header(t("encShort"),true)+`<main><div class="enc-wrap">''','''  const q0=S.view.q||"", fam0=S.view.fam||"";
  app.innerHTML=header(t("encShort"),true)+`<main><div class="enc-wrap">''')
rep('''    <div class="counter" id="ecount" style="margin-top:8px">…</div>''','''    <select class="search fam" id="efam" aria-label="${esc(t("famAll"))}"><option value="">${esc(t("famAll"))}</option></select>
    <div class="counter" id="ecount" style="margin-top:8px">…</div>''')
rep('''  const LET="ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");''','''  const LET="ABCDEFGHIJKLMNOPQRSTUVWXYZ".split(""); const fs=document.getElementById("efam");
  { const cnt={}; E.forEach(e=>{ const k=e.bloque.es; cnt[k]=cnt[k]||{n:0,l:L(e.bloque)}; cnt[k].n++; });
    Object.keys(cnt).sort((a,b)=>cnt[a].l.localeCompare(cnt[b].l,S.lang)).forEach(k=>{ const o=document.createElement("option"); o.value=k; o.textContent=`${cnt[k].l} (${cnt[k].n})`; fs.appendChild(o); }); fs.value=fam0; fs.onchange=()=>{ paint(); const mm=document.querySelector("#app main"); if(mm) mm.scrollTo(0,0); }; }''')
rep('''const out=E.filter(e=>!qq||norm(e.name.es+" "+e.name.en+" "+L(e.cuando)).includes(qq));''','''const fam=fs.value; const out=E.filter(e=>(!fam||e.bloque.es===fam)&&(!qq||norm(e.name.es+" "+e.name.en+" "+L(e.cuando)).includes(qq)));''')
rep('''    az.style.display=qq?"none":"flex";''','''    az.style.display=(qq||fam)?"none":"flex";''')
rep('''.join("");\n    S.view.q=raw;''','''.join("");\n    S.view.q=raw; S.view.fam=fam;''')
rep('''S.encRet={q:raw,top:mm?mm.scrollTop:0,id:e.id}; nav({name:"enc",id:e.id,back:{name:"enc",q:raw}});''','''S.encRet={q:raw,fam,top:mm?mm.scrollTop:0,id:e.id}; nav({name:"enc",id:e.id,back:{name:"enc",q:raw,fam}});''')
rep('''if(R&&R.q===inp.value.trim()){''','''if(R&&R.q===inp.value.trim()&&(R.fam||"")===fs.value){''')
# ---------- share efe ----------
rep('''    <div class="efe-nav"><button id="efeP">''','''    ${f?`<button class="btn efe-share" id="efeSh">📤 ${t("share")}<small>${t("shareHint")}</small></button>`:""}
    <div class="efe-nav"><button id="efeP">''')
rep('''  const eb=document.getElementById("efeEnc"); if(eb) eb.onclick=()=>nav({name:"enc",id:f.enc,back:{name:"efe",d:k}});''','''  const eb=document.getElementById("efeEnc"); if(eb) eb.onclick=()=>nav({name:"enc",id:f.enc,back:{name:"efe",d:k}});
  const sh=document.getElementById("efeSh"); if(sh) sh.onclick=()=>shareEfe(k,f);''')
SHARE=r'''async function shareEfe(k,f){
  const W=1080,H=1920,c=document.createElement("canvas"); c.width=W; c.height=H; const x=c.getContext("2d");
  try{ await document.fonts.load('700 60px Carlito'); await document.fonts.load('400 40px Carlito'); }catch(_){}
  const g=x.createLinearGradient(0,0,W,H); g.addColorStop(0,"#004379"); g.addColorStop(1,"#002060"); x.fillStyle=g; x.fillRect(0,0,W,H);
  const img=await new Promise(r=>{ const i=new Image(); i.onload=()=>r(i); i.onerror=()=>r(null); i.src="icons/emblema_blanco.png"; });
  if(img){ x.globalAlpha=.08; x.drawImage(img,W-620,H-760,700,700); x.globalAlpha=1; x.drawImage(img,90,150,120,120); }
  x.fillStyle="#fff"; x.font='700 46px Carlito, Calibri, sans-serif'; x.fillText("Historiapp",230,228);
  x.fillStyle="#EDAB00"; x.font='700 44px Carlito, Calibri, sans-serif'; x.fillText(t("efeCard").toUpperCase(),90,420);
  x.fillStyle="#fff"; x.font='700 56px Carlito, Calibri, sans-serif'; x.fillText(fmtDay(k),90,500);
  x.fillStyle="#EDAB00"; x.font='700 230px Carlito, Calibri, sans-serif'; x.fillText(String(f.year||""),80,740);
  const txt=String(L(f)).replace(/\*/g,"");
  let fsz=50; const wrap=sz=>{ x.font=`400 ${sz}px Carlito, Calibri, sans-serif`; const words=txt.split(/\s+/), lines=[]; let cur="";
    for(const w of words){ const tr=cur?cur+" "+w:w; if(x.measureText(tr).width>W-180&&cur){ lines.push(cur); cur=w; } else cur=tr; } if(cur) lines.push(cur); return lines; };
  let lines=wrap(fsz); while(lines.length*fsz*1.38>900&&fsz>34){ fsz-=2; lines=wrap(fsz); }
  x.fillStyle="#fff"; lines.forEach((l,i)=>x.fillText(l,90,860+i*fsz*1.38));
  x.fillStyle="rgba(255,255,255,.85)"; x.font='700 38px Carlito, Calibri, sans-serif'; x.fillText(t("shareTag"),90,H-200);
  x.fillStyle="#EDAB00"; x.font='400 34px Carlito, Calibri, sans-serif'; x.fillText("aleivaarcas-a11y.github.io/historiapp",90,H-145);
  const blob=await new Promise(r=>c.toBlob(r,"image/png")); if(!blob) return;
  const name=`historiapp_${k}.png`, file=new File([blob],name,{type:"image/png"});
  try{ if(navigator.canShare&&navigator.canShare({files:[file]})){ await navigator.share({files:[file],title:"Historiapp"}); track("compartir/efe","Compartir efeméride",true); return; } }catch(e){ if(e&&e.name==="AbortError") return; }
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },1500);
}
async function renderEfe(){'''
rep('async function renderEfe(){',SHARE)
rep('.efe-nav button{','.efe-share{margin:18px 0 12px;display:flex;flex-direction:column;align-items:center;gap:2px;background:linear-gradient(135deg,var(--primary),var(--primary-2))}\n.efe-share small{font-size:12px;font-weight:400;opacity:.85}\n.fam{margin-top:10px;padding:11px 12px;font-weight:700;color:var(--tp2);-webkit-appearance:none;appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);background-position:calc(100% - 20px) 50%,calc(100% - 14px) 50%;background-size:6px 6px;background-repeat:no-repeat}\n.efe-nav button{')
open(p,"w",encoding="utf-8").write(s); print("ok")
