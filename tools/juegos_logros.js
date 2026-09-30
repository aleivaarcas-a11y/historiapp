/* ============ palabra del día (wordle) ============ */
const WORDS={
es:[
 {w:"JUEGO",t:1,d:"Para Popplow, junto con la danza, el subsuelo que sirve de soporte al movimiento humano."},
 {w:"DANZA",t:1,d:"Popplow la considera la primera expresión de la cultura física, con finalidad erótica, mágica o guerrera."},
 {w:"PESCA",t:1,d:"Actividad de subsistencia prehistórica con arpón, anzuelo, tridente, nasa o canoa; hoy se discute si la pesca es deporte."},
 {w:"CAZAR",t:1,d:"Con arco y flecha, azagaya, jabalina, honda o bumerán; que la caza fuera cosa solo de varones no está demostrado."},
 {w:"ARPON",t:1,d:"Útil de pesca prehistórico; en las sociedades de cazadores, ejercicios como el arpón o la jabalina servían para mejorar la caza."},
 {w:"CUEVA",t:1,d:"En la de Obłazowa (Polonia) apareció el bumerán más antiguo que se conoce, tallado en marfil de mamut."},
 {w:"MAMUT",t:1,d:"De su marfil está tallado el bumerán más antiguo conocido, hallado en la cueva de Obłazowa."},
 {w:"FEMUR",t:1,d:"Hueso cuya resistencia a la flexión cae de forma pronunciada entre el 5000 y el 2000 a. C., señal de menos actividad física."},
 {w:"RITMO",t:1,d:"Las huellas de Engare Sero muestran a catorce mujeres caminando juntas al mismo ritmo, a 1,5 m/s."},
 {w:"MARCA",t:1,d:"En el modelo del rendimiento, el cuerpo produce marcas, rankings y una pirámide con la élite en la cúspide."},
 {w:"ELITE",t:1,d:"La cúspide de la pirámide del rendimiento, el modelo del deporte de competición."},
 {w:"TRIBU",t:1,d:"El grupo cuya seguridad y continuidad garantizaban las actividades físicas adaptadas al entorno y a las costumbres colectivas."},
 {w:"CANOA",t:1,d:"Uno de los útiles de pesca prehistóricos, junto al arpón, el anzuelo, el tridente y la nasa."},
 {w:"TUMBA",t:2,d:"Las pinturas de las tumbas egipcias, como las de Beni Hasan, son la fuente principal sobre la lucha y los juegos."},
 {w:"LUCHA",t:2,d:"Una de las tres modalidades de combate practicadas en Egipto, junto a la esgrima con bastones (tahtib) y el boxeo."},
 {w:"PERSA",t:2,d:"Del antiguo Irán, cuya tradición de fuerza pervive en la zurkhaneh, con sus flexiones, mazas y giros."},
 {w:"TEBAS",t:2,d:"En su necrópolis occidental, la tumba de Kheruef representa hacia 1360 a. C. un combate de boxeo."},
 {w:"CARRO",t:2,d:"El carro de guerra fue una de las destrezas del faraón, junto a la doma de caballos, la caza y el tiro con arco."},
 {w:"SENET",t:2,d:"Juego de tablero del antiguo Egipto."},
 {w:"DIANA",t:2,d:"El faraón tiraba con arco sobre lingotes de cobre bruto, piezas que se usaban para comerciar en el Mediterráneo."},
 {w:"ARCOS",t:2,d:"El arco compuesto, más manejable en los carros de guerra, lanzaba flechas hasta 300 metros, frente a los 150 del simple."},
 {w:"JUSTA",t:2,d:"Nace del manejo de las pértigas con que se llevaban las barcas y de las competiciones de obreros al acabar una gran obra."},
 {w:"BRAZA",t:2,d:"Algunos autores han creído reconocer el crol y la braza en las representaciones egipcias, aunque otros lo discuten."},
 {w:"BOXEO",t:2,d:"Presencia marginal en Egipto; la única evidencia indiscutible es una escena de la tumba de Kheruef, en Tebas."},
 {w:"MAZAS",t:2,d:"Piezas de madera que en la zurkhaneh se voltean por detrás de los hombros, siguiendo el ritmo del tambor."},
 {w:"NUBIA",t:2,d:"Tierra de origen del rey Taharqa, cuya estela aporta una de las evidencias de la carrera de fondo."},
 {w:"LUXOR",t:2,d:"Junto a ella, en Medamud, una inscripción del santuario de Montu narra los tiros con arco de Amenofis II."},
 {w:"NADAR",t:2,d:"En un pueblo fluvial nadaban barqueros y pescadores; nadar era destreza de élite si se aprendía con instructor."}
],
en:[
 {w:"GAMES",t:1,d:"For Popplow, together with dance, the ground that supports human movement."},
 {w:"DANCE",t:1,d:"Popplow sees it as the first expression of physical culture, with an erotic, magical or warlike purpose."},
 {w:"CAVES",t:1,d:"Obłazowa cave in Poland yielded the oldest known boomerang, carved from mammoth ivory."},
 {w:"IVORY",t:1,d:"The oldest known boomerang, found in Obłazowa cave, is carved from mammoth ivory."},
 {w:"FEMUR",t:1,d:"A bone whose bending strength falls sharply between 5000 and 2000 BC, a sign of less physical activity."},
 {w:"TRIBE",t:1,d:"The group whose safety and continuity physical activities, adapted to the setting and shared customs, helped to secure."},
 {w:"CANOE",t:1,d:"One of the prehistoric fishing tools, along with the harpoon, hook, trident and fish trap."},
 {w:"TRAPS",t:1,d:"One of the prehistoric strategies for hunting and fishing, alongside pursuit, stalking and ambush."},
 {w:"MARKS",t:1,d:"In the performance model, the body produces marks, rankings and a pyramid with the elite at the top."},
 {w:"ELITE",t:1,d:"The top of the performance pyramid, the model of competitive sport."},
 {w:"TOMBS",t:2,d:"Egyptian tomb paintings, such as those at Beni Hasan, are the main source on wrestling and games."},
 {w:"SENET",t:2,d:"A board game of ancient Egypt."},
 {w:"NUBIA",t:2,d:"Homeland of King Taharqa, whose stela is one of the pieces of evidence for long-distance running."},
 {w:"MACES",t:2,d:"Wooden clubs swung behind the shoulders in the zurkhaneh, following the beat of the drum."},
 {w:"JOUST",t:2,d:"It grew out of handling the poles used to move boats and out of workers' contests held when a great building was finished."},
 {w:"ARROW",t:2,d:"The composite bow, easier to handle on war chariots, shot arrows up to 300 metres, against 150 for the simple bow."},
 {w:"INGOT",t:2,d:"The pharaoh shot at targets made of raw copper ingots, pieces traded across the Mediterranean."},
 {w:"CRAWL",t:2,d:"Some authors have seen the crawl and breaststroke in Egyptian images, though others dispute it."},
 {w:"BOXER",t:2,d:"Boxing was marginal in Egypt; the only undisputed evidence is a scene in the tomb of Kheruef at Thebes."},
 {w:"LUXOR",t:2,d:"Near it, at Medamud, an inscription in the shrine of Montu tells of Amenhotep II's archery."},
 {w:"BOATS",t:2,d:"Handling the poles that moved the boats is one of the origins of the Egyptian joust."}
]};
function wdKey(){ return todayKey()+"|"+S.lang; }
async function wdPool(){ const idx=await getIndex(); const av=new Set(idx.temas.filter(x=>x.available).map(x=>x.num)); return (WORDS[S.lang]||WORDS.es).filter(x=>av.has(x.t)); }
async function wdToday(){ const P=await wdPool(); if(!P.length) return null; return P[dayHash(todayKey()+"wd"+S.lang)%P.length]; }
function wdState(){ const w=S.prog.wd||{}; if(w.key!==wdKey()) return {key:wdKey(),g:[],done:false,won:false}; return w; }
function wdEval(guess,sol){ const r=Array(5).fill("no"), left={}; for(let i=0;i<5;i++){ if(guess[i]===sol[i]) r[i]="ok"; else left[sol[i]]=(left[sol[i]]||0)+1; }
  for(let i=0;i<5;i++){ if(r[i]!=="ok"&&left[guess[i]]){ r[i]="pr"; left[guess[i]]--; } } return r; }
async function renderPalabra(){
  app.innerHTML=header(t("wdTitle"),true)+`<main id="wdM"><div class="empty">…</div></main>`;
  bindHeader(()=>nav(S.view.back||{name:"home"}));
  const W=await wdToday(); const m=document.getElementById("wdM"); if(!m) return; if(!W){ m.innerHTML=`<div class="empty">${t("soon")}</div>`; return; }
  const sol=W.w; let st=wdState(); let cur="";
  const KEYS=S.lang==="es"?["QWERTYUIOP","ASDFGHJKLÑ","⏎ZXCVBNM⌫"]:["QWERTYUIOP","ASDFGHJKL","⏎ZXCVBNM⌫"];
  function draw(){
    const rows=[]; for(let r=0;r<6;r++){ const g=st.g[r]; const ev=g?wdEval(g,sol):null; const txt=g||(r===st.g.length&&!st.done?cur:"");
      rows.push(`<div class="wd-row">${[0,1,2,3,4].map(i=>{ const c=ev?ev[i]:(txt[i]?"typ":""); return `<div class="wd-t ${c}" aria-label="${txt[i]||""} ${c==="ok"?t("wdOk"):c==="pr"?t("wdPr"):c==="no"?t("wdNo"):""}">${txt[i]||""}</div>`; }).join("")}</div>`); }
    const ks={}; st.g.forEach(g=>{ const ev=wdEval(g,sol); [...g].forEach((ch,i)=>{ const v=ev[i], o=ks[ch]; if(v==="ok"||(v==="pr"&&o!=="ok")||(!o)) ks[ch]=v; }); });
    const kb=KEYS.map(r=>`<div class="wd-kr">${[...r].map(k=>`<button class="wd-k ${ks[k]||""} ${k==="⏎"||k==="⌫"?"wide":""}" data-k="${k}" aria-label="${k==="⏎"?t("wdEnter"):k==="⌫"?t("wdDel"):k}">${k==="⏎"?t("wdEnter"):k}</button>`).join("")}</div>`).join("");
    const fin=st.done?`<div class="card wd-end"><small>${st.won?t("wdWon",{n:st.g.length}):t("wdLost")}</small><b>${esc(sol)}</b><p>${esc(W.d)}</p><button class="btn" id="wdTema">📖 ${t("tema")} ${W.t}</button><p class="wd-next">${t("wdNext")}</p></div>`:"";
    m.innerHTML=`<p class="wd-intro">${t("wdIntro")}</p><div class="wd-grid">${rows.join("")}</div>
      <div class="wd-leg"><span><i class="wd-t ok mini"></i>${t("wdOk")}</span><span><i class="wd-t pr mini"></i>${t("wdPr")}</span><span><i class="wd-t no mini"></i>${t("wdNo")}</span></div>
      ${fin||`<div class="wd-kb">${kb}</div>`}`;
    m.querySelectorAll(".wd-k").forEach(b=>b.onclick=()=>key(b.dataset.k));
    const tb=document.getElementById("wdTema"); if(tb) tb.onclick=()=>nav({name:"tema",num:W.t});
  }
  function key(k){ if(st.done) return;
    if(k==="⌫"){ cur=cur.slice(0,-1); }
    else if(k==="⏎"){ if(cur.length<5){ toast(t("wdShort")); return; }
      st.g.push(cur); cur=""; const won=st.g[st.g.length-1]===sol;
      if(won||st.g.length>=6){ st.done=true; st.won=won; const s=S.prog.wdStats||{plays:0,wins:0};
        s.plays++; if(won){ s.wins++; addXP(Math.max(10,35-st.g.length*5)); celebrate(); } S.prog.wdStats=s; track("palabra/"+(won?"acierto":"fallo"),"Palabra del día",true); }
      S.prog.wd=st; save(); checkAch(); }
    else if(cur.length<5) cur+=k;
    draw(); }
  draw();
  document.onkeydown=e=>{ if(S.view.name!=="palabra") return; const k=e.key.toUpperCase(); if(k==="ENTER") key("⏎"); else if(k==="BACKSPACE") key("⌫"); else if(/^[A-ZÑ]$/.test(k)) key(k); };
}

/* ============ logros ============ */
const ACH=[
 ["pts10","⭐",p=>p.xp>=10],
 ["lvl3","📈",p=>levelOf(p.xp)>=2],
 ["lvl5","🏛️",p=>levelOf(p.xp)>=4],
 ["lvl10","🎓",p=>levelOf(p.xp)>=9],
 ["st3","🔥",p=>(p.bestStreak||p.streak||0)>=3],
 ["st7","🔥",p=>(p.bestStreak||p.streak||0)>=7],
 ["st30","🌋",p=>(p.bestStreak||p.streak||0)>=30],
 ["reto1","☀️",p=>(p.retos||0)>=1],
 ["reto7","🌞",p=>(p.retos||0)>=7],
 ["wd1","🔤",p=>((p.wdStats||{}).wins||0)>=1],
 ["wd10","🧠",p=>((p.wdStats||{}).wins||0)>=10],
 ["enc10","📖",p=>Object.keys(p.encSeen||{}).length>=10],
 ["enc50","📚",p=>Object.keys(p.encSeen||{}).length>=50],
 ["enc200","🌍",p=>Object.keys(p.encSeen||{}).length>=200],
 ["efe7","📅",p=>Object.keys(p.efeSeen||{}).length>=7],
 ["bdg1","🏅",p=>Object.keys(p.badges||{}).length>=1],
 ["bdg9","🎖️",p=>Object.keys(p.badges||{}).length>=9]
];
function checkAch(){ const p=S.prog; p.ach=p.ach||{}; if((p.streak||0)>(p.bestStreak||0)) p.bestStreak=p.streak; let n=[];
  ACH.forEach(([id,ic,f])=>{ if(!p.ach[id]&&f(p)){ p.ach[id]=todayKey(); n.push(ic+" "+t("ach."+id+".n")); } });
  if(n.length){ save(); setTimeout(()=>toast("🏆 "+n[0],2600),1200); } }
function renderLogros(){
  checkAch(); const p=S.prog, lv=levelOf(p.xp), nxt=LEVEL_XP[lv+1], names=t("levels");
  const pct=nxt?Math.round((p.xp-LEVEL_XP[lv])/(nxt-LEVEL_XP[lv])*100):100;
  const got=ACH.filter(a=>p.ach&&p.ach[a[0]]).length;
  app.innerHTML=header(t("achT"),true)+`<main>
    <div class="card lg-lv"><small>${t("level")} ${lv+1}</small><b>${esc(names[lv])}</b>
      <div class="bar"><i style="width:${pct}%"></i></div>
      <span>${nxt?t("lgNext",{n:nxt-p.xp,l:lv+2,name:names[lv+1]}):t("lgMax")}</span>
      <div class="lg-stats"><div><b>⭐ ${p.xp}</b><small>${t("xp")}</small></div><div><b>🔥 ${p.streak||0}</b><small>${t("lgStreak")}</small></div><div><b>🏆 ${got}/${ACH.length}</b><small>${t("achT")}</small></div></div></div>
    <div class="section-title">${t("achT")}</div>
    <div class="lg-ach">${ACH.map(([id,ic])=>{ const on=p.ach&&p.ach[id]; return `<div class="lg-a ${on?"on":"off"}"><span class="ic">${on?ic:"🔒"}</span><div><b>${t("ach."+id+".n")}</b><small>${t("ach."+id+".d")}${on?" · ✓":""}</small></div></div>`; }).join("")}</div>
    <div class="section-title">${t("lgLevels")}</div>
    <div class="lg-levels">${names.map((n,i)=>`<div class="lg-l ${i<lv?"done":i===lv?"now":"next"}"><span class="n">${i+1}</span><b>${esc(n)}</b><small>${LEVEL_XP[i]} ${t("xp")}</small><em>${i<lv?"✓":i===lv?t("lgHere"):"🔒"}</em></div>`).join("")}</div>
    <div class="section-title">${t("lgHow")}</div>
    <div class="card lg-how">${t("lgHowList").map(x=>`<p>${esc(x)}</p>`).join("")}</div></main>`;
  bindHeader(()=>nav(S.view.back||{name:"home"}));
}
