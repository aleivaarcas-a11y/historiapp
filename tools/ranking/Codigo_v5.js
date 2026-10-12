/* Historiapp · Ranking semanal (v5, 12-10-2026: v4 de Cuadrigas con sus acciones cq_* y, además, la clasificación genérica de los juegos, hoja «Juegos», acción «juego»)
   Hoja propia en el Drive de la UCAM («Historiapp - Ranking (alumnos)», ID en la propiedad HOJA_ID).
   Columna «oculto»: escribe X para retirar un alias; al alumno se le pedirá que elija otro.
   Nombre y apellidos solo se guardan en la hoja: doGet nunca los devuelve. */
const HOJA = "Jugadores";
const TOPE_DIA = 1500;          // puntos máximos que cuentan por alumno y día
const CAB = ["uid","alias","ultimaXP","total","semana","puntosSemana","dia","puntosHoy","actualizado","oculto","grupo","nombre","apellido1","apellido2"];
const GRUPOS = ["1ºA","1ºB","1ºTAMA","1ºEnglish"];
const TZ = "Europe/Madrid";

/* ---------- filtro automático ---------- */
// Se vetan si aparecen en cualquier parte del alias (letras repetidas, números por letras y separadores incluidos: «p.u.t.4», «zorraaa»)
const VETO_DENTRO = ["hijodeputa","hijoputa","gilipoll","subnormal","maricon","mariquita","bollera","tortillera","retrasad","mongolo","mongola","follar","follad","chupamela","chupapoll","comepoll","mamada","mamon","cabron","zorra","furcia","fulana","ramera","prostitut","polla","pollon","cojon","chocho","mierda","pajiller","pajera","nazi","hitler","fascist","facha","negrata","sudaca","panchit","moromierda","gitanaz","violad","violar","pedofil","pederast","terrorist","yihad","jihad","drogat","cocain","heroin","fuck","shit","bitch","whore","slut","cunt","pussy","penis","vagina","nigger","nigga","faggot","retard","porn","boobs","tetas","teton","culon","culazo","culito","verga","ojete","orgasm","semen","esperma","puta","puto","joder","jodete","conazo","idiota","imbecil","estupid","pringao","pringad","capullo","franco","profesor","leiva","admin","moderador","ucam"];
// Se vetan solo como palabra completa, para no bloquear «cálculo», «canal», «Trapero» o «Penélope»
const VETO_PALABRA = ["ano","anal","cono","culo","teta","coca","eta","sex","pija","feo","fea","isis","porro","cagar","cagon","tonto","tonta","gordo","gorda","pene","rape","dick","cock","kkk","sieg","heil","isis","caca","pis","nabo"];
// Palabras legítimas que contienen una vetada
const SEGURAS = ["diputad","imputad","computa","computo","disputa","reputa","amputa","estupend"];
// En nombre y apellidos no se aplican estas (son apellidos o nombres reales)
const NOMBRE_SEGURAS = ["franco","leiva","ucam","profesor","admin","moderador"];
const NOMBRES_FALSOS = ["test","prueba","asdf","qwerty","qwer","xxx","nombre","apellido","anonimo","anonima","nadie","yo","messi","ronaldo","cristiano","neymar","mbappe","batman","superman","goku","pikachu","mickey","mortadelo","filemon","homer","bart","fulano","mengano","zutano","lalala","jajaja","jejeje","jijiji","no","si","ninguno","ninguna","xd","lol"];

function plano_(s){ // minúsculas, sin tildes, ñ como n, números y símbolos como letras
  return String(s||"").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"")
    .replace(/0/g,"o").replace(/1/g,"i").replace(/3/g,"e").replace(/4/g,"a").replace(/5/g,"s").replace(/7/g,"t").replace(/8/g,"b")
    .replace(/@/g,"a").replace(/\$/g,"s").replace(/[|!]/g,"i");
}
// «zorra» → /z+o+r{2,}a+/: admite letras estiradas sin confundir «zorra» con «Zoraida» ni «polla» con «Pola»
function rx_(v,entera){ const c=v.replace(/(.)\1*/g,(m,x)=>m.length>1?x+"{2,}":x+"+"); return new RegExp(entera?"^"+c+"$":c); }
const RX_DENTRO = VETO_DENTRO.map(v=>[v,rx_(v)]), RX_PALABRA = VETO_PALABRA.map(v=>rx_(v,true));
function ofensivo_(s, esNombre){
  let pegado = plano_(s).replace(/[^a-z]/g,"");
  SEGURAS.forEach(w=>{ pegado = pegado.split(w).join("_"); });
  if(RX_DENTRO.some(([v,r])=>!(esNombre && NOMBRE_SEGURAS.indexOf(v)>=0) && r.test(pegado))) return true;
  if(esNombre) return false;
  const ws = plano_(s).split(/[^a-z]+/).filter(Boolean).concat([plano_(s).replace(/[^a-z]/g,"")]);
  return ws.some(w=>RX_PALABRA.some(r=>r.test(w)));
}
function absurdo_(s){ // para nombre y apellidos
  const base = plano_(s), ws = base.split(/[^a-z]+/).filter(Boolean);
  if(!ws.length) return true;
  for(const w of ws){
    if(w.length<2 && ws.length===1) return true;
    if(!/[aeiouy]/.test(w) && w!=="ng") return true;             // sin vocales: «xkcd»
    if(/[bcdfghjklmnpqrstvwxz]{5,}/.test(w)) return true;       // cinco consonantes seguidas
    if(NOMBRES_FALSOS.indexOf(w)>=0) return true;
    if(/^(..?)\1{2,}$/.test(w)) return true;                    // «jajaja», «lalala»
  }
  if(/(.)\1\1/.test(base)) return true;                         // «aaa», «lll»
  if(/asdf|qwer|zxcv|hjkl|uiop/.test(base.replace(/[^a-z]/g,""))) return true;
  return false;
}

/* ---------- utilidades ---------- */
function hoja_(){
  const pr = PropertiesService.getScriptProperties(); let id = pr.getProperty("HOJA_ID"), ss;
  if(id){ ss = SpreadsheetApp.openById(id); } else { ss = SpreadsheetApp.create("Historiapp - Ranking (alumnos)"); pr.setProperty("HOJA_ID", ss.getId()); }
  let sh = ss.getSheetByName(HOJA);
  if(!sh){ sh = ss.insertSheet(HOJA); sh.appendRow(CAB); sh.setFrozenRows(1); }
  return sh;
}
function hoy_(){ return Utilities.formatDate(new Date(), TZ, "yyyy-MM-dd"); }
function semana_(){ // lunes de la semana actual
  const d = new Date(Utilities.formatDate(new Date(), TZ, "yyyy-MM-dd'T'12:00:00"));
  const w = (d.getDay()+6)%7; d.setDate(d.getDate()-w);
  return Utilities.formatDate(d, TZ, "yyyy-MM-dd");
}
function fecha_(x){ return x instanceof Date ? Utilities.formatDate(x,TZ,"yyyy-MM-dd") : String(x||""); }
function json_(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function limpiaAlias_(a){
  a = String(a||"").replace(/\s+/g," ").trim();
  if(a.length<3 || a.length>16) return null;
  if(!/^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _.\-]+$/.test(a)) return null;
  if(!/[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]/.test(a)) return null;          // al menos una letra
  return a;
}
function limpiaNombre_(a, obligatorio){
  a = String(a||"").replace(/\s+/g," ").trim().slice(0,40);
  if(!a) return obligatorio ? null : "";
  if(!/^[A-Za-zÀ-ÿ' .\-]+$/.test(a)) return null;
  return a;
}

/* ---------- clasificación de los juegos (v5) ----------
   Cada juego de la asignatura envía su mejor puntuación con el uid del alumno ya apuntado al ranking.
   Se guarda solo la mejor; el alias y el grupo salen de la hoja de jugadores, y la columna «oculto» también vale aquí. */
const HOJA_J = "Juegos", CAB_J = ["uid","juego","puntos","detalle","actualizado"], TOPE_JUEGO = 100000;
function hojaJ_(){
  const ss = hoja_().getParent(); let sh = ss.getSheetByName(HOJA_J);
  if(!sh){ sh = ss.insertSheet(HOJA_J); sh.appendRow(CAB_J); sh.setFrozenRows(1); }
  return sh;
}
function postJuego_(b, v, fila){
  if(fila<0) return json_({ok:false,err:"noalta"});
  if(String(v[fila][9]).trim()) return json_({ok:false,err:"retirado"});
  const juego = String(b.juego||""); if(!/^[a-z0-9_-]{2,20}$/.test(juego)) return json_({ok:false,err:"juego"});
  const pts = Math.max(0, Math.min(TOPE_JUEGO, Math.floor(Number(b.puntos)||0)));
  const det = String(b.detalle||"").replace(/[<>]/g,"").slice(0,80);
  const sh = hojaJ_(), w = sh.getDataRange().getValues(), uid = v[fila][0];
  for(let i=1;i<w.length;i++) if(w[i][0]===uid && w[i][1]===juego){
    if(pts>Number(w[i][2]||0)) sh.getRange(i+1,1,1,5).setValues([[uid,juego,pts,det,new Date()]]);
    return json_({ok:true,puntos:Math.max(pts,Number(w[i][2]||0))});
  }
  sh.appendRow([uid,juego,pts,det,new Date()]);
  return json_({ok:true,puntos:pts});
}
function getJuego_(juego, uid){
  const jug = {}; hoja_().getDataRange().getValues().slice(1).forEach(r=>{ jug[r[0]] = {alias:r[1], grupo:r[10], oculto:!!String(r[9]).trim()}; });
  const v = hojaJ_().getDataRange().getValues().slice(1).filter(r=>r[1]===juego && jug[r[0]] && !jug[r[0]].oculto)
    .map(r=>({uid:r[0], alias:jug[r[0]].alias, grupo:jug[r[0]].grupo, pts:Number(r[2])||0, det:String(r[3]||"")}));
  const tabla = g=>{
    const o = v.filter(x=>x.pts>0 && (!g || x.grupo===g)).sort((a,b)=>b.pts-a.pts);
    const yo = o.findIndex(x=>x.uid===uid);
    return {top:o.slice(0,10).map((x,i)=>({p:i+1,alias:x.alias,grupo:x.grupo,pts:x.pts,det:x.det,yo:x.uid===uid})), yo: yo>=0?{p:yo+1,pts:o[yo].pts}:null, n:o.length};
  };
  const grupos = {}; GRUPOS.forEach(g=>grupos[g]=tabla(g));
  const yo = jug[uid];
  return json_({ok:true, juego, existe:!!yo, retirado:!!(yo && yo.oculto), grupo: yo ? yo.grupo : null, total:tabla(), grupos});
}

/* ---------- API ---------- */
function doPost(e){
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try{
    const b = JSON.parse(e.postData.contents||"{}");
    if(String(b.accion||"").indexOf("cq_")===0) return json_(cqPost_(b));
    const uid = String(b.uid||"");
    if(!/^[a-z0-9]{12,40}$/.test(uid)) return json_({ok:false,err:"uid"});
    const sh = hoja_(); const v = sh.getDataRange().getValues();
    let fila = -1; for(let i=1;i<v.length;i++) if(v[i][0]===uid){ fila=i; break; }

    if(b.accion==="baja"){ if(fila>0) sh.deleteRow(fila+1); return json_({ok:true}); }
    if(b.accion==="juego") return postJuego_(b, v, fila);

    const alias = limpiaAlias_(b.alias); if(!alias) return json_({ok:false,err:"alias"});
    if(ofensivo_(alias)) return json_({ok:false,err:"veto"});
    const low = alias.toLowerCase();
    for(let i=1;i<v.length;i++) if(i!==fila && String(v[i][1]).toLowerCase()===low) return json_({ok:false,err:"ocupado"});

    const grupo = GRUPOS.indexOf(b.grupo)>=0 ? b.grupo : null; if(!grupo) return json_({ok:false,err:"grupo"});
    const nombre = limpiaNombre_(b.nombre,true), ap1 = limpiaNombre_(b.apellido1,true), ap2 = limpiaNombre_(b.apellido2,false);
    if(nombre===null || ap1===null || ap2===null) return json_({ok:false,err:"nombre"});
    if(absurdo_(nombre) || absurdo_(ap1) || (ap2 && absurdo_(ap2)) || ofensivo_(nombre+" "+ap1+" "+ap2, true)) return json_({ok:false,err:"nombre"});

    const xp = Math.max(0, Math.floor(Number(b.xp)||0));
    const sem = semana_(), dia = hoy_(), ahora = new Date();
    if(fila<0){ sh.appendRow([uid,alias,xp,0,sem,0,dia,0,ahora,"",grupo,nombre,ap1,ap2]); return json_({ok:true,semana:0}); }

    let [ , aliasViejo, ultima, total, s, pSem, d, pHoy, , oculto] = v[fila];
    if(String(oculto).trim()){
      if(String(aliasViejo).toLowerCase()===low) return json_({ok:false,err:"retirado"});
      oculto = "";                                               // eligió otro alias: vuelve al ranking
    }
    if(fecha_(s)!==sem){ pSem=0; }
    if(fecha_(d)!==dia){ pHoy=0; }
    let delta = xp - Number(ultima||0); if(delta<0) delta=0;   // si el alumno reinició la app, no resta
    const suma = Math.max(0, Math.min(delta, TOPE_DIA - Number(pHoy||0)));
    sh.getRange(fila+1,1,1,14).setValues([[uid,alias,xp,Number(total||0)+suma,sem,Number(pSem||0)+suma,dia,Number(pHoy||0)+suma,ahora,oculto,grupo,nombre,ap1,ap2]]);
    return json_({ok:true,semana:Number(pSem||0)+suma});
  } catch(err){ return json_({ok:false,err:String(err)}); }
  finally{ lock.releaseLock(); }
}

function doGet(e){
  if(String((e.parameter||{}).accion||"").indexOf("cq_")===0) return json_(cqGet_(e.parameter));
  { const jg = String((e.parameter||{}).juego||""); if(/^[a-z0-9_-]{2,20}$/.test(jg)) return getJuego_(jg, String((e.parameter||{}).uid||"")); }
  const uid = String((e.parameter||{}).uid||"");
  const sem = semana_();
  const filas = hoja_().getDataRange().getValues().slice(1);
  const mia = filas.find(r=>r[0]===uid);
  const v = filas.filter(r=>!String(r[9]).trim())
    .map(r=>({uid:r[0],alias:r[1],grupo:r[10],total:Number(r[3])||0,semana:fecha_(r[4])===sem?(Number(r[5])||0):0}));
  const tabla = (k,g)=>{
    const o = v.filter(x=>x[k]>0 && (!g || x.grupo===g)).sort((a,b)=>b[k]-a[k]);
    const yo = o.findIndex(x=>x.uid===uid);
    return {top:o.slice(0,10).map((x,i)=>({p:i+1,alias:x.alias,grupo:x.grupo,pts:x[k],yo:x.uid===uid})),
            yo: yo>=0?{p:yo+1,pts:o[yo][k]}:null, n:o.length};
  };
  const grupos = {}; GRUPOS.forEach(g=>grupos[g]=tabla("semana",g));
  return json_({ok:true, semana:sem, retirado: !!(mia && String(mia[9]).trim()), existe: !!mia,
    sem:tabla("semana"), total:tabla("total"), grupos:grupos});
}

/* Prueba del filtro: ejecútala desde el editor y mira el registro */
function probarFiltro(){
  ["Rayo Veloz","P.u.t.a","Gilipooollas","Calculo","Fernando","Hijo de Put4","Atleta_23","Cono Sur","Messi10"].forEach(a=>Logger.log(a+" → "+(ofensivo_(a)?"VETADO":"ok")));
  ["María José","asdf","Xkcd","Messi","Fernández","Ñúñez","Lll","Pérez-Reverte"].forEach(a=>Logger.log(a+" → "+(absurdo_(a)?"ABSURDO":"ok")));
}

/* =====================================================================
   Cuadrigas (juego del Tema 4 dentro de Historiapp)
   · Pestaña «Cuadrigas»: resultados que el juego envía solo al terminar la clase de veinte minutos,
     una carrera de la clase o una temporada. Solo la ve el profesor.
   · Pestaña «Cuadrigas fantasmas»: la mejor contrarreloj de cada alumno por circo y tiro.
     Solo pueden subir fantasma los alumnos apuntados al ranking, con su alias ya filtrado;
     si el profesor oculta un alias en «Jugadores», su fantasma deja de aparecer.
     Columna «oculto» de los fantasmas: escribe X para retirar uno.
   ===================================================================== */
const CQ_RES = "Cuadrigas", CQ_FAN = "Cuadrigas fantasmas";
const CQ_RES_CAB = ["fecha","nombre","apellido1","apellido2","grupo","modo","detalle","puesto","tiempo","segundos","aciertos","preguntas","victorias","prestigio","codice","idioma","enRanking","uid","id"];
const CQ_FAN_CAB = ["id","uid","alias","grupo","pista","tiro","vueltas","tiempo","datos","fecha","oculto","dia","subidasHoy"];
const CQ_VUELTAS = {tarraco:3, maximo:2}, CQ_TIROS = ["biga","triga","cuadriga"];
const CQ_VUELTA_M = {tarraco:2*184+2*Math.PI*18, maximo:2*330+2*Math.PI*21};   // metros por vuelta en el juego
function cqHoja_(nombre, cab){
  const ss = hoja_().getParent(); let sh = ss.getSheetByName(nombre);
  if(!sh){ sh = ss.insertSheet(nombre); sh.appendRow(cab); sh.setFrozenRows(1); }
  return sh;
}
function cqJugador_(uid){
  const v = hoja_().getDataRange().getValues();
  for(let i=1;i<v.length;i++) if(v[i][0]===uid) return {alias:v[i][1], oculto:String(v[i][9]).trim(), grupo:v[i][10], nombre:v[i][11], ap1:v[i][12], ap2:v[i][13]};
  return null;
}
function cqNum_(x, lo, hi){ const n = Number(x); return isFinite(n) && n>=lo && n<=hi ? n : ""; }
function cqPost_(b){
  const uid = String(b.uid||""); if(!/^[a-z0-9]{12,40}$/.test(uid)) return {ok:false,err:"uid"};
  if(b.accion==="cq_resultado"){
    const sh = cqHoja_(CQ_RES, CQ_RES_CAB);
    const id = String(b.id||"").slice(0,40); if(!/^[a-z0-9]{8,40}$/.test(id)) return {ok:false,err:"id"};
    const n = sh.getLastRow(); if(n>1){ const ids = sh.getRange(Math.max(2,n-600),19,Math.min(600,n-1),1).getValues().map(r=>r[0]); if(ids.indexOf(id)>=0) return {ok:false,err:"duplicado"}; }
    let nombre, ap1, ap2, grupo, enR = "no";
    const j = cqJugador_(uid);
    if(j){ nombre=j.nombre; ap1=j.ap1; ap2=j.ap2; grupo=j.grupo; enR="sí"; }
    else{
      nombre = limpiaNombre_(b.nombre,true); ap1 = limpiaNombre_(b.apellido1,true); ap2 = limpiaNombre_(b.apellido2,false);
      if(nombre===null || ap1===null || ap2===null || absurdo_(nombre) || absurdo_(ap1) || ofensivo_(nombre+" "+ap1, true)) return {ok:false,err:"nombre"};
      grupo = GRUPOS.indexOf(b.grupo)>=0 ? b.grupo : ""; if(!grupo) return {ok:false,err:"grupo"};
    }
    const modo = ["campana","clase","temporada"].indexOf(b.modo)>=0 ? b.modo : null; if(!modo) return {ok:false,err:"modo"};
    sh.appendRow([new Date(), nombre, ap1, ap2||"", grupo, modo, String(b.detalle||"").slice(0,600), cqNum_(b.puesto,0,20), String(b.tiempo||"").slice(0,12), cqNum_(b.segundos,0,3600),
      cqNum_(b.aciertos,0,999), cqNum_(b.preguntas,0,999), cqNum_(b.victorias,0,99), cqNum_(b.puntos,0,100), cqNum_(b.codice,0,999), b.idioma==="en"?"en":"es", enR, uid, id]);
    return {ok:true};
  }
  if(b.accion==="cq_fantasma"){
    const j = cqJugador_(uid); if(!j) return {ok:false,err:"ranking"}; if(j.oculto) return {ok:false,err:"retirado"};
    const pista = CQ_VUELTAS[b.pista] ? b.pista : null, tiro = CQ_TIROS.indexOf(b.tiro)>=0 ? b.tiro : null;
    if(!pista || !tiro || Number(b.vueltas)!==CQ_VUELTAS[pista]) return {ok:false,err:"carrera"};
    const t = Number(b.t), datos = String(b.datos||"");
    if(!isFinite(t) || datos.length>45000 || !/^[0-9a-z,\-]+$/.test(datos)) return {ok:false,err:"datos"};
    // comprobaciones: duración coherente con las muestras, velocidad máxima posible y tiempo mínimo del recorrido
    const a = datos.split(",").map(x=>parseInt(x,36)); if(a.length%4 || a.length<40) return {ok:false,err:"datos"};
    const m = a.length/4; if(Math.abs(m/10 - t) > 1.5) return {ok:false,err:"tiempo"};
    if(t < 0.85*CQ_VUELTA_M[pista]*CQ_VUELTAS[pista]/18) return {ok:false,err:"tiempo"};
    let x=0,y=0; for(let i=0;i<a.length;i+=4){ const dx=a[i], dy=a[i+1]; if(i>0 && Math.hypot(dx,dy)>26) return {ok:false,err:"datos"}; x+=dx; y+=dy; if(Math.abs(x)>3300 || Math.abs(y)>500) return {ok:false,err:"datos"}; }
    const sh = cqHoja_(CQ_FAN, CQ_FAN_CAB); const v = sh.getDataRange().getValues(); const dia = hoy_();
    let fila=-1, hoyN=0;
    for(let i=1;i<v.length;i++){ if(v[i][1]===uid){ if(fecha_(v[i][11])===dia) hoyN = Math.max(hoyN, Number(v[i][12])||0); if(v[i][4]===pista && v[i][5]===tiro) fila=i; } }
    if(hoyN>=30) return {ok:false,err:"tope"};
    if(fila>0 && Number(v[fila][7])<=t){ sh.getRange(fila+1,12,1,2).setValues([[dia,hoyN+1]]); return {ok:true,mejor:false}; }
    const fil = [fila>0?v[fila][0]:Utilities.getUuid().slice(0,8), uid, j.alias, j.grupo, pista, tiro, CQ_VUELTAS[pista], Math.round(t*10)/10, datos, new Date(), fila>0?v[fila][10]:"", dia, hoyN+1];
    if(fila>0) sh.getRange(fila+1,1,1,fil.length).setValues([fil]); else sh.appendRow(fil);
    return {ok:true,mejor:true};
  }
  return {ok:false,err:"accion"};
}
function cqGet_(p){
  const sh = cqHoja_(CQ_FAN, CQ_FAN_CAB); const v = sh.getDataRange().getValues().slice(1);
  if(p.accion==="cq_fantasma"){ const r = v.find(r=>String(r[0])===String(p.id) && !String(r[10]).trim()); return r ? {ok:true,d:r[8],t:r[7]} : {ok:false,err:"no"}; }
  if(p.accion==="cq_lista"){
    const jug = {}; hoja_().getDataRange().getValues().slice(1).forEach(r=>{ jug[r[0]] = {alias:r[1], oculto:String(r[9]).trim(), grupo:r[10]}; });
    const lista = v.filter(r=>r[4]===p.pista && r[5]===p.tiro && !String(r[10]).trim() && jug[r[1]] && !jug[r[1]].oculto)
      .map(r=>({id:String(r[0]), alias:jug[r[1]].alias, grupo:jug[r[1]].grupo, t:Number(r[7])})).sort((a,b)=>a.t-b.t).slice(0,50);
    return {ok:true,lista:lista};
  }
  return {ok:false,err:"accion"};
}
