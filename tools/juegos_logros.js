/* ============ palabra del día (wordle) ============ */
const WORDS={
es:[
 {w:"JUEGO",t:1,d:"Actividad libre, sujeta a reglas y separada de la vida corriente; Huizinga la situó en la raíz de la cultura en Homo ludens."},
 {w:"LUDUS",t:1,d:"En la teoría de Caillois, el polo del juego sometido a reglas, esfuerzo y convenciones, opuesto a la improvisación de la paidia."},
 {w:"ILINX",t:1,d:"Categoría de Caillois para los juegos que buscan el vértigo, como girar, deslizarse o dejarse caer."},
 {w:"RASGO",t:1,d:"Cada una de las características con que Guttmann distingue el deporte moderno, como la secularización, la igualdad o la búsqueda del récord."},
 {w:"REGLA",t:1,d:"Norma que fija cómo se juega; su codificación por escrito marca el paso del juego tradicional al deporte moderno."},
 {w:"MARCA",t:1,d:"Resultado medido de una prueba; batir la mejor, el récord, es uno de los rasgos del deporte moderno según Guttmann."},
 {w:"RITOS",t:1,d:"Ceremonias religiosas o sociales a las que muchas prácticas físicas antiguas estuvieron ligadas antes de convertirse en deporte."},
 {w:"CUEVA",t:1,d:"Soporte del arte rupestre, cuyas escenas de caza, danza o lucha sirven de fuente para estudiar la actividad física en la Prehistoria."},
 {w:"HECHO",t:1,d:"Acontecimiento del pasado que el historiador establece a partir de las fuentes y después interpreta."},
 {w:"LANZA",t:1,d:"Arma arrojadiza de caza prehistórica, antecedente remoto del lanzamiento de jabalina."},
 {w:"MITOS",t:1,d:"Relatos tradicionales; en la asignatura, también los tópicos sin base en las fuentes que conviene desmontar."},
 {w:"ELITE",t:1,d:"Grupo social privilegiado; durante siglos muchas prácticas físicas funcionaron como signo de distinción de las élites."},
 {w:"SENET",t:2,d:"Juego de tablero egipcio de treinta casillas para dos jugadores, ligado a las creencias sobre el más allá."},
 {w:"TUMBA",t:2,d:"Enterramiento egipcio cuyas pinturas, como las de Beni Hasan, son la principal fuente sobre lucha, juegos y ejercicio físico."},
 {w:"LUCHA",t:2,d:"Combate cuerpo a cuerpo; las tumbas de Beni Hasan conservan cientos de parejas de luchadores pintadas."},
 {w:"CARRO",t:2,d:"Vehículo tirado por caballos que los faraones del Imperio Nuevo usaron en la guerra, la caza y la exhibición de su destreza."},
 {w:"PERSA",t:2,d:"Del antiguo Irán, cultura de la que proceden el polo (chovgán) y la zurkhaneh, la casa de fuerza tradicional."},
 {w:"MAZAS",t:2,d:"Pesadas piezas de madera que se voltean en los ejercicios de la zurkhaneh iraní."},
 {w:"JUSTA",t:2,d:"Combate entre tripulaciones de barcas que intentan derribarse al agua con pértigas; las tumbas egipcias ya lo representan."},
 {w:"TEBAS",t:2,d:"Capital religiosa del Egipto del Imperio Nuevo, en cuyas tumbas y templos aparecen escenas de caza, carros y juegos."},
 {w:"NUBIO",t:2,d:"Habitante de Nubia, al sur de Egipto; las representaciones egipcias muestran combates de lucha entre egipcios y nubios."},
 {w:"ARCOS",t:2,d:"Arma de caza y de guerra con la que los faraones exhibían su destreza en inscripciones que narran tiros asombrosos."}
],
en:[
 {w:"LUDUS",t:1,d:"In Caillois's theory, the pole of play governed by rules, effort and conventions, opposed to the improvisation of paidia."},
 {w:"ILINX",t:1,d:"Caillois's category for games that seek vertigo, such as spinning, sliding or falling."},
 {w:"TRAIT",t:1,d:"Each of the characteristics Guttmann uses to define modern sport, such as secularism, equality or the quest for records."},
 {w:"RULES",t:1,d:"The norms that set how a game is played; writing them down marks the shift from traditional games to modern sport."},
 {w:"RITES",t:1,d:"Religious or social ceremonies to which many ancient physical practices were tied before they became sport."},
 {w:"CAVES",t:1,d:"The setting of rock art, whose hunting, dancing and fighting scenes are sources for physical activity in Prehistory."},
 {w:"SPEAR",t:1,d:"A prehistoric hunting weapon, a distant forerunner of the javelin throw."},
 {w:"MYTHS",t:1,d:"Traditional stories; in the course, also the clichés with no basis in the sources that need taking apart."},
 {w:"ELITE",t:1,d:"A privileged social group; for centuries many physical practices served as a mark of distinction for elites."},
 {w:"FACTS",t:1,d:"Events of the past that the historian establishes from the sources and then interprets."},
 {w:"SENET",t:2,d:"An Egyptian board game of thirty squares for two players, linked to beliefs about the afterlife."},
 {w:"TOMBS",t:2,d:"Egyptian burials whose paintings, such as those at Beni Hasan, are the main source on wrestling, games and exercise."},
 {w:"NUBIA",t:2,d:"The land south of Egypt; Egyptian images show wrestling bouts between Egyptians and Nubians."},
 {w:"MACES",t:2,d:"Heavy wooden clubs swung in the exercises of the Iranian zurkhaneh."},
 {w:"JOUST",t:2,d:"A contest between boat crews who try to knock each other into the water with poles; Egyptian tombs already depict it."},
 {w:"ARROW",t:2,d:"Pharaohs displayed their archery in inscriptions that tell of astonishing shots."},
 {w:"STELA",t:2,d:"A carved stone slab; the stelae of Amenhotep II boast of his feats in archery, rowing and horsemanship."}
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
