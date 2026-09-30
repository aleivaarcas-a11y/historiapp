p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,c=1):
    global s; assert s.count(o)==c,(o[:70],s.count(o)); s=s.replace(o,n)
ES='''wdTitle:"Palabra del día", wdCardSub:"Adivina un término de la asignatura en seis intentos", wdCardDone:"Resuelta en {n} intentos ✓", wdCardLost:"Hoy no ha salido; mañana habrá otra", wdIntro:"Adivina el término de la asignatura en seis intentos. Escribe palabras de cinco letras, sin tildes.", wdOk:"en su sitio", wdPr:"está, en otra posición", wdNo:"no está", wdEnter:"Enviar", wdDel:"Borrar", wdShort:"Faltan letras", wdWon:"Acertada en {n} intentos", wdLost:"La palabra era", wdNext:"Mañana habrá una palabra nueva.", achT:"Logros", lgNext:"Te faltan {n} XP para el nivel {l}, {name}", lgMax:"Has llegado al nivel máximo", lgStreak:"días de racha", lgLevels:"Niveles", lgHere:"Estás aquí", lgHow:"Cómo ganar experiencia", lgTap:"Toca para ver logros y niveles",
    lgHowList:["Leer una ficha por primera vez da 3 XP.","Cada acierto en análisis de imágenes, mitos o fuentes da 10 XP, y 15 en las preguntas rápidas; un fallo da 2.","Ordenar una cronología sin errores da 20 XP.","Cada pareja bien unida en relaciona da 5 XP, y cada término acertado en el glosario, 8.","Abrir una idea nueva del mapa da 2 XP, y acertar la pregunta de un vídeo, 10.","El reto del día duplica los puntos que ganas mientras lo haces.","Acertar la palabra del día da entre 10 y 30 XP; cuantos menos intentos, más puntos.","La racha suma un día cada vez que ganas puntos en días seguidos."],
    ach:{pts10:{n:"Primeros puntos",d:"Consigue tus primeros 10 XP"},lvl3:{n:"En marcha",d:"Llega al nivel 3"},lvl5:{n:"Mitad del camino",d:"Llega al nivel 5"},lvl10:{n:"Catedrático",d:"Llega al nivel máximo"},st3:{n:"Constancia",d:"Tres días seguidos de racha"},st7:{n:"Semana completa",d:"Siete días seguidos de racha"},st30:{n:"Un mes sin fallar",d:"Treinta días seguidos de racha"},reto1:{n:"Primer reto",d:"Completa un reto del día"},reto7:{n:"Retador",d:"Completa siete retos del día"},wd1:{n:"Buen ojo",d:"Acierta una palabra del día"},wd10:{n:"Lexicógrafo",d:"Acierta diez palabras del día"},enc10:{n:"Curioso",d:"Abre 10 deportes de la Enciclopedia"},enc50:{n:"Enciclopedista",d:"Abre 50 deportes de la Enciclopedia"},enc200:{n:"Trotamundos",d:"Abre 200 deportes de la Enciclopedia"},efe7:{n:"Calendario",d:"Lee siete «Tal día como hoy» distintos"},bdg1:{n:"Primera medalla",d:"Completa un modo de estudio de un tema"},bdg9:{n:"Nueve medallas",d:"Consigue nueve medallas de modos de estudio"}},'''
EN='''wdTitle:"Word of the day", wdCardSub:"Guess a course term in six tries", wdCardDone:"Solved in {n} tries ✓", wdCardLost:"Not today; there will be a new one tomorrow", wdIntro:"Guess the course term in six tries. Type five-letter words.", wdOk:"right place", wdPr:"in the word, wrong place", wdNo:"not in the word", wdEnter:"Enter", wdDel:"Delete", wdShort:"Not enough letters", wdWon:"Solved in {n} tries", wdLost:"The word was", wdNext:"There will be a new word tomorrow.", achT:"Achievements", lgNext:"{n} XP to go for level {l}, {name}", lgMax:"You have reached the top level", lgStreak:"day streak", lgLevels:"Levels", lgHere:"You are here", lgHow:"How to earn experience", lgTap:"Tap to see achievements and levels",
    lgHowList:["Reading a study sheet for the first time gives 3 XP.","Each correct answer in image analysis, myths or sources gives 10 XP, and 15 in the quick quiz; a wrong one gives 2.","Ordering a timeline with no mistakes gives 20 XP.","Each correct pair in match gives 5 XP, and each glossary term you get right, 8.","Opening a new idea in the map gives 2 XP, and answering a video question correctly, 10.","The daily challenge doubles the points you earn while doing it.","Guessing the word of the day gives between 10 and 30 XP; the fewer tries, the more points.","Your streak adds a day each time you earn points on consecutive days."],
    ach:{pts10:{n:"First points",d:"Earn your first 10 XP"},lvl3:{n:"Getting going",d:"Reach level 3"},lvl5:{n:"Halfway there",d:"Reach level 5"},lvl10:{n:"Professor",d:"Reach the top level"},st3:{n:"Consistency",d:"A three-day streak"},st7:{n:"Full week",d:"A seven-day streak"},st30:{n:"A month without a break",d:"A thirty-day streak"},reto1:{n:"First challenge",d:"Complete a daily challenge"},reto7:{n:"Challenger",d:"Complete seven daily challenges"},wd1:{n:"Sharp eye",d:"Guess a word of the day"},wd10:{n:"Lexicographer",d:"Guess ten words of the day"},enc10:{n:"Curious",d:"Open 10 sports in the Encyclopedia"},enc50:{n:"Encyclopedist",d:"Open 50 sports in the Encyclopedia"},enc200:{n:"Globetrotter",d:"Open 200 sports in the Encyclopedia"},efe7:{n:"Calendar",d:"Read seven different «On this day» entries"},bdg1:{n:"First badge",d:"Complete a study mode in a unit"},bdg9:{n:"Nine badges",d:"Earn nine study-mode badges"}},'''
rep('tabSearch:"Buscar",','tabSearch:"Buscar", '+ES)
rep('tabSearch:"Search",','tabSearch:"Search", '+EN)
# routes
rep('if(v.name==="guia") return "guia";','if(v.name==="guia") return "guia"; if(v.name==="palabra") return "palabra"; if(v.name==="logros") return "logros";')
rep('if(h==="guia") return {name:"guia"};','if(h==="guia") return {name:"guia"}; if(h==="palabra") return {name:"palabra"}; if(h==="logros") return {name:"logros"};')
rep('  if(v.name==="guia") return renderGuia();','  if(v.name==="guia") return renderGuia();\n  if(v.name==="palabra") return renderPalabra();\n  if(v.name==="logros") return renderLogros();')
# hooks
rep('''celebrate(); },350);\n  renderXP();\n}''','''celebrate(); },350);\n  renderXP(); try{ checkAch(); }catch(_){}\n}''')
rep('S.prog.daily={date:todayKey(),done:true,correct,total:steps.length};','S.prog.daily={date:todayKey(),done:true,correct,total:steps.length}; S.prog.retos=(S.prog.retos||0)+1;')
rep('''  const e=D.entries.find(x=>x.id===id); if(!e){ nav({name:"enc"}); return; }''','''  const e=D.entries.find(x=>x.id===id); if(!e){ nav({name:"enc"}); return; }
  S.prog.encSeen=S.prog.encSeen||{}; if(!S.prog.encSeen[e.id]){ S.prog.encSeen[e.id]=1; save(); checkAch(); }''')
rep('''  let eimg="";''','''  if(f){ S.prog.efeSeen=S.prog.efeSeen||{}; if(!S.prog.efeSeen[k]){ S.prog.efeSeen[k]=1; save(); checkAch(); } }
  let eimg="";''')
# header xp pill -> logros
rep('''  const g=document.getElementById("hSearch");''','''  const hx=document.getElementById("hXP"); if(hx){ hx.style.cursor="pointer"; hx.onclick=()=>nav({name:"logros",back:S.view}); }
  const g=document.getElementById("hSearch");''')
# strip clickable
rep('<div class="strip">','<div class="strip" id="stripBtn" role="button" tabindex="0" aria-label="${esc(t("lgTap"))}">')
rep('''  bindHeader();\n  const hoy=document.getElementById("hoy");''','''  bindHeader();\n  document.getElementById("stripBtn").onclick=()=>nav({name:"logros",back:{name:"home"}});\n  const hoy=document.getElementById("hoy");''')
# wordle card in Hoy
rep('const sDep=slot("dep"), sEfe=slot("efe");','const sDep=slot("dep"), sEfe=slot("efe"), sWd=slot("wdc");\n  (async()=>{ try{ const W=await wdToday(); if(!W) return; const st=wdState(); sWd.setAttribute("role","button");\n    sWd.innerHTML=`<div class="wd-mini">${[...(st.done?W.w:"?????")].map((c,i)=>`<i class="${st.done?(st.won?"ok":"no"):""}">${st.done?c:""}</i>`).join("")}</div><div class="tx"><small>🔤 ${t("wdTitle")}</small><b>${st.done?(st.won?t("wdCardDone",{n:st.g.length}):t("wdCardLost")):t("wdCardSub")}</b></div><div class="go">›</div>`;\n    sWd.onclick=()=>nav({name:"palabra",back:{name:"home"}}); sWd.style.display=""; }catch(_){} })();')
CSS='''.strip{cursor:pointer}
.hoy .wdc{grid-column:1/-1;flex-direction:row;align-items:center;gap:12px;background:var(--soft)}
.hoy .wdc .tx{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}
.hoy .wdc .tx b{font-size:15px}
.hoy .wdc .go{font-size:22px;color:var(--tp)}
.wd-mini{display:flex;gap:3px}
.wd-mini i{width:22px;height:26px;border-radius:5px;border:2px solid var(--line);background:var(--paper);font-style:normal;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;color:var(--tp2)}
.wd-mini i.ok{background:var(--primary);border-color:var(--primary);color:#fff}
.wd-mini i.no{background:var(--soft2)}
.wd-intro{font-size:14px;color:var(--muted);text-align:center;margin:0 8px 12px;line-height:1.4}
.wd-grid{display:flex;flex-direction:column;gap:6px;align-items:center}
.wd-row{display:flex;gap:6px}
.wd-t{position:relative;width:54px;height:54px;border:2px solid var(--line);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;color:var(--ink);background:var(--paper);text-transform:uppercase}
.wd-t.typ{border-color:var(--muted)}
.wd-t.ok{background:var(--primary);border-color:var(--primary);color:#fff}
.wd-t.ok::after{content:"✓";position:absolute;top:1px;right:4px;font-size:11px}
.wd-t.pr{background:var(--accent);border:2px dashed var(--primary-2);color:#1a1a1a}
.wd-t.pr::after{content:"↔";position:absolute;top:0;right:3px;font-size:11px}
.wd-t.no{background:var(--soft2);color:var(--muted);border-color:var(--soft2)}
.wd-t.mini{width:18px;height:18px;border-radius:5px;display:inline-flex;margin-right:5px;vertical-align:-4px}
.wd-t.mini::after{font-size:9px;top:-1px;right:2px}
.wd-leg{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 14px;font-size:12px;color:var(--muted);margin:12px 0 4px}
.wd-kb{margin-top:10px;display:flex;flex-direction:column;gap:6px}
.wd-kr{display:flex;gap:4px;justify-content:center}
.wd-k{flex:1;max-width:36px;height:48px;border-radius:8px;background:var(--soft);color:var(--ink);font-weight:800;font-size:16px;position:relative}
.wd-k.wide{max-width:64px;flex:1.6;font-size:12px}
.wd-k.ok{background:var(--primary);color:#fff}
.wd-k.pr{background:var(--accent);color:#1a1a1a;outline:2px dashed var(--primary-2);outline-offset:-3px}
.wd-k.no{opacity:.35}
.wd-end{margin-top:14px;text-align:center}
.wd-end small{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.06em;font-weight:800;color:var(--muted)}
.wd-end b{display:block;font-size:30px;letter-spacing:.12em;color:var(--tp2);margin:4px 0 8px}
.wd-end p{line-height:1.5;margin:0 0 12px}
.wd-end .wd-next{font-size:12.5px;color:var(--muted);margin:10px 0 0}
.lg-lv{text-align:center}
.lg-lv small{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.06em;font-weight:800;color:var(--muted)}
.lg-lv>b{display:block;font-size:26px;color:var(--tp2);margin:2px 0 10px}
.lg-lv .bar{height:10px;border-radius:99px;background:var(--soft2);overflow:hidden}
.lg-lv .bar i{display:block;height:100%;background:var(--accent)}
.lg-lv>span{display:block;font-size:13.5px;margin-top:8px}
.lg-stats{display:flex;justify-content:space-around;margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
.lg-stats div{display:flex;flex-direction:column;align-items:center}
.lg-stats small{font-size:11.5px;color:var(--muted)}
.lg-ach{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.lg-a{display:flex;gap:8px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:10px}
.lg-a .ic{font-size:24px}
.lg-a b{display:block;font-size:13.5px;color:var(--tp2)}
.lg-a small{display:block;font-size:11.5px;color:var(--muted);line-height:1.3}
.lg-a.off{opacity:.55}
.lg-a.on{border:2px solid var(--accent)}
.lg-levels{display:flex;flex-direction:column;gap:6px}
.lg-l{display:flex;align-items:center;gap:10px;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
.lg-l .n{width:30px;height:30px;border-radius:50%;background:var(--soft);display:flex;align-items:center;justify-content:center;font-weight:800;color:var(--tp2)}
.lg-l b{flex:1}
.lg-l small{color:var(--muted);font-size:12px}
.lg-l em{font-style:normal;font-size:12px;font-weight:800;min-width:64px;text-align:right}
.lg-l.now{border:2px solid var(--accent);background:var(--warm)}
.lg-l.next{opacity:.6}
.lg-how p{margin:0 0 8px;line-height:1.45;font-size:14.5px}
'''
rep('.guia details{',CSS+'.guia details{')
JS=open("tools/juegos_logros.js",encoding="utf-8").read()
rep('function renderSettings(){',JS+'\nfunction renderSettings(){')
open(p,"w",encoding="utf-8").write(s); print("ok")
