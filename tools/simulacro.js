/* --- simulacro de test (20-11-2026, petición de los alumnos): preguntas de los temas que se elijan, desde la portada --- */
const SIMU_N=[10,20,30,0];
function smNota(x){ return (Math.round(x*100)/100).toFixed(2).replace(".",S.lang==="en"?".":","); }
async function renderSimu(){
  const v=S.view; let running=false, answered=()=>0;
  app.innerHTML=header(t("smTitle"),true)+`<main><div class="empty">…</div></main>`;
  bindHeader(()=>{ if(running&&answered()>0&&!confirm(t("smLeave"))) return; nav(v.back||{name:"home"}); });
  const main=app.querySelector("main");
  let idx; try{ idx=await getIndex(); }catch(e){ main.innerHTML=`<div class="empty">${t("loadError")}</div>`; return; }
  const av=idx.temas.filter(m=>m.available), temas={};
  await Promise.all(av.map(m=>getTema(m.num).then(tm=>{ temas[m.num]=tm; }).catch(()=>{})));
  if(!main.isConnected) return;
  const cnt=n=>((temas[n]||{}).quiz||[]).length;
  const cfg=S.prog.simuCfg||{};
  let sel=new Set((cfg.temas||[]).filter(n=>av.some(m=>m.num===n)&&cnt(n)));
  if(!sel.size) av.forEach(m=>{ if(cnt(m.num)) sel.add(m.num); });
  let nq=SIMU_N.includes(cfg.n)?cfg.n:20, modo=cfg.modo==="prac"?"prac":"exam";
  const keep=()=>{ S.prog.simuCfg={temas:[...sel],n:nq,modo}; save(); };

  function setup(){
    running=false; scrollTop0();
    const pool=[...sel].reduce((a,n)=>a+cnt(n),0), go=nq?Math.min(nq,pool):pool;
    const hist=(S.prog.simuHist||[]).slice(-5).reverse(), dl=S.lang==="en"?"en-GB":"es-ES";
    main.innerHTML=`<div class="card" style="padding:14px 16px"><h2 style="font-size:20px">${t("smTitle")}</h2><p class="smlead">${t("smLead")}</p></div>
      <div class="section-title">${t("smTemas")}</div>
      <div class="smchips">${av.map(m=>`<button class="smchip ${sel.has(m.num)?"on":""}" data-n="${m.num}" ${cnt(m.num)?"":"disabled"}><b>${m.num}</b><span>${esc(L(m.title))}</span><small>${t("smNq",{n:cnt(m.num)})}</small></button>`).join("")}</div>
      <button class="btn ghost" id="smAll" style="padding:6px">${sel.size===av.filter(m=>cnt(m.num)).length?t("smNone"):t("smAllT")}</button>
      <div class="section-title">${t("smHowMany")}</div>
      <div class="seg smseg">${SIMU_N.map(n=>`<button class="${nq===n?"on":""}" data-q="${n}">${n||t("smTodas")}</button>`).join("")}</div>
      <div class="section-title">${t("smModo")}</div>
      <div class="smmodes">
        <button class="smmode ${modo==="exam"?"on":""}" data-m="exam"><b>🎓 ${t("smExam")}</b><span>${t("smExamSub")}</span></button>
        <button class="smmode ${modo==="prac"?"on":""}" data-m="prac"><b>⚡ ${t("smPrac")}</b><span>${t("smPracSub")}</span></button>
      </div>
      <button class="btn" id="smGo" ${pool?"":"disabled"}>${pool?t("smStart",{n:go}):t("smPick")}</button>
      ${hist.length?`<div class="section-title">${t("smHist")}</div><div class="card smhist">${hist.map(h=>`<div><span>${h.m==="prac"?"⚡":"🎓"} ${esc(new Date(h.d).toLocaleDateString(dl,{day:"numeric",month:"short"}))}</span><span>${t("smHistT",{t:h.t.join(", "),n:h.n})}</span><b>${smNota(h.nota)}</b></div>`).join("")}</div>`:""}`;
    main.querySelectorAll(".smchip").forEach(b=>b.onclick=()=>{ const n=+b.dataset.n; sel.has(n)?sel.delete(n):sel.add(n); keep(); setup(); });
    document.getElementById("smAll").onclick=()=>{ const all=av.filter(m=>cnt(m.num)); if(sel.size===all.length) sel.clear(); else all.forEach(m=>sel.add(m.num)); keep(); setup(); };
    main.querySelectorAll(".smseg button").forEach(b=>b.onclick=()=>{ nq=+b.dataset.q; keep(); setup(); });
    main.querySelectorAll(".smmode").forEach(b=>b.onclick=()=>{ modo=b.dataset.m; keep(); setup(); });
    document.getElementById("smGo").onclick=()=>{ if(!pool) return; keep(); start(); };
  }

  // reparto equilibrado entre los temas elegidos, para que un tema con muchas preguntas no se coma el examen
  function pick(){
    const per=[...sel].sort((a,b)=>a-b).map(n=>shuffle(((temas[n]||{}).quiz||[]).map((q,i)=>({n,i,q}))));
    const total=per.reduce((a,x)=>a+x.length,0), want=nq?Math.min(nq,total):total, out=[];
    let k=0; while(out.length<want){ const l=per[k%per.length]; if(l.length) out.push(l.pop()); k++; }
    return shuffle(out);
  }

  function start(){
    const list=pick(), ans=list.map(()=>-1), ord=list.map(x=>shuffle(x.q.options.map((o,i)=>i)));
    running=true; answered=()=>ans.filter(a=>a>=0).length;
    track("simulacro/"+modo+"/"+list.length,"Simulacro",true);
    if(modo==="prac") return prac(list,ans,ord);
    scrollTop0();
    main.innerHTML=`<div class="smbar"><span id="smCount"></span><button id="smSend">${t("smSend")}</button></div>
      <p class="smrule">${t("smRule")}</p>
      ${list.map((x,j)=>`<div class="card smq"><div class="smqh"><b>${j+1}</b><small>${t("tema")} ${x.n}</small></div><div class="qtext">${esc(L(x.q.q))}</div>
        <div class="opts">${ord[j].map((oi,k)=>`<button class="opt" data-j="${j}" data-i="${oi}"><span class="k">${"abcd"[k]}</span><span>${esc(L(x.q.options[oi]))}</span></button>`).join("")}</div></div>`).join("")}
      <button class="btn" id="smSend2">${t("smSend")}</button>`;
    const upd=()=>{ document.getElementById("smCount").textContent=t("smAns",{a:answered(),b:list.length}); };
    main.querySelectorAll(".opt").forEach(b=>b.onclick=()=>{ const j=+b.dataset.j, i=+b.dataset.i; ans[j]=ans[j]===i?-1:i;
      main.querySelectorAll(`.opt[data-j="${j}"]`).forEach(o=>o.classList.toggle("sel",+o.dataset.i===ans[j])); upd(); });
    const send=()=>{ const bl=list.length-answered(); if(bl&&!confirm(bl===1?t("smBlank1"):t("smBlankN",{n:bl}))) return; finish(list,ans,ord); };
    document.getElementById("smSend").onclick=send; document.getElementById("smSend2").onclick=send; upd();
  }

  // modo práctica: una pregunta cada vez, con 20 segundos y la corrección al momento, como en Preguntas rápidas
  function prac(list,ans,ord){
    let pos=0, timer=null;
    const draw=()=>{ scrollTop0(); const x=list[pos], it=x.q;
      main.innerHTML=`<div class="counter">${t("seen",{a:pos+1,b:list.length})} · ${t("tema")} ${x.n}</div><div class="progress"><i style="width:${pos/list.length*100}%"></i></div>
        <div class="timer"><i id="tm"></i></div><div class="card qtext">${esc(L(it.q))}</div>
        <div class="opts">${ord[pos].map((oi,k)=>`<button class="opt" data-i="${oi}"><span class="k">${"ABCD"[k]}</span><span>${esc(L(it.options[oi]))}</span></button>`).join("")}</div>`;
      let done=false;
      const fin=ch=>{ if(done) return; done=true; clearInterval(timer); ans[pos]=ch; const ok=ch===it.answer; if(ok) addXP(15);
        main.querySelectorAll(".opt").forEach(b=>{ b.disabled=true; const i=+b.dataset.i; if(i===it.answer) b.classList.add("ok"); else if(i===ch) b.classList.add("ko"); });
        note(x,ch);
        sheet(ok, ok?t("correct"):(ch===-1?t("timeUp"):t("wrong")), L(it.explain), ok?15:0, ()=>{ pos++; if(pos>=list.length) finish(list,ans,ord,true); else draw(); }, L(it.q)); };
      main.querySelectorAll(".opt").forEach(b=>b.onclick=()=>fin(+b.dataset.i));
      let left=20; const bar=document.getElementById("tm"); bar.style.width="100%";
      timer=setInterval(()=>{ if(!bar.isConnected){ clearInterval(timer); return; } left--; bar.style.width=(left/20*100)+"%"; if(left<=0) fin(-1); },1000); };
    draw();
  }

  // apunta la pregunta como vista en el tema y la manda al repaso de fallos si se ha fallado
  function note(x,ch){ const it=x.q, tm=temas[x.n]; if(ch<0) return;
    try{ markSeen(tm.id,"quiz",x.i); }catch(_){}
    try{ if(ch===it.answer) rpAcierto(it.q); else { const oo=[it.options[it.answer],...it.options.filter((_,i)=>i!==it.answer)]; rpFallo("historiapp",it.q,{es:oo.map(o=>o&&o.es||o),en:oo.map(o=>o&&(o.en||o.es)||o)},null,x.n,null); } }catch(_){} }

  function finish(list,ans,ord,noted){
    running=false; scrollTop0();
    let A=0,F=0,B=0; const byT={};
    list.forEach((x,j)=>{ const r=byT[x.n]||(byT[x.n]={a:0,n:0}); r.n++; if(ans[j]<0) B++; else if(ans[j]===x.q.answer){ A++; r.a++; } else F++; if(!noted) note(x,ans[j]); });
    const nota=Math.max(0,A-F/3)/list.length*10;
    if(!noted) addXP(A*15);
    const h=S.prog.simuHist||(S.prog.simuHist=[]); h.push({d:Date.now(),m:modo,t:Object.keys(byT).map(Number).sort((a,b)=>a-b),n:list.length,a:A,f:F,b:B,nota:Math.round(nota*100)/100}); if(h.length>30) h.splice(0,h.length-30); save();
    track("simulacro/fin/"+modo+"/"+(Math.round(nota)*10)+"%","Simulacro",true);
    const lt="abcd";
    main.innerHTML=`<div class="card result"><div class="big">${nota>=8?"🏆":nota>=5?"👍":"📚"}</div><h2>${t("smDone")}</h2>
        <div class="score">${smNota(nota)}</div><p>${t("smOver10")}</p>
        <div class="smsum"><span>✓ ${t(A===1?"smA1":"smA",{n:A})}</span><span>✗ ${t(F===1?"smF1":"smF",{n:F})}</span><span>○ ${t("smB",{n:B})}</span></div>
        <p class="smcalc">${t("smCalc")}${list.length===20?" "+t("smReal",{x:smNota(nota/2)}):""}</p></div>
      ${Object.keys(byT).length>1?`<div class="card smtem">${Object.entries(byT).map(([n,r])=>`<div><span>${t("tema")} ${n}</span><i><b style="width:${r.a/r.n*100}%"></b></i><span>${r.a}/${r.n}</span></div>`).join("")}</div>`:""}
      <button class="btn" id="smAgain">${t("smAgain")}</button>
      ${F?`<button class="btn sec" id="smRp">${t("smToRp")}</button>`:""}
      <button class="btn ghost" id="smCfg">${t("smChange")}</button>
      <div class="section-title">${t("smReview")}</div>
      ${list.map((x,j)=>{ const ok=ans[j]===x.q.answer, bl=ans[j]<0; return `<div class="card smq ${bl?"bl":ok?"ok":"ko"}"><div class="smqh"><b>${j+1}</b><small>${t("tema")} ${x.n}</small><em>${bl?"○ "+t("smBl"):ok?"✓ "+t("correct"):"✗ "+t("wrong")}</em></div><div class="qtext">${esc(L(x.q.q))}</div>
        <div class="opts">${ord[j].map((oi,k)=>`<div class="opt ${oi===x.q.answer?"ok":oi===ans[j]?"ko":""}"><span class="k">${lt[k]}</span><span>${esc(L(x.q.options[oi]))}</span></div>`).join("")}</div>
        ${L(x.q.explain)?`<p class="smexp">${md(L(x.q.explain))}</p>`:""}</div>`; }).join("")}`;
    document.getElementById("smAgain").onclick=()=>start();
    document.getElementById("smCfg").onclick=()=>setup();
    const rp=document.getElementById("smRp"); if(rp) rp.onclick=()=>nav({name:"repaso"});
    renderXP();
  }
  setup();
}
