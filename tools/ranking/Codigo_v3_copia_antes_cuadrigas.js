/* Historiapp · Ranking semanal (v3, 10-10-2026)
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

/* ---------- API ---------- */
function doPost(e){
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try{
    const b = JSON.parse(e.postData.contents||"{}");
    const uid = String(b.uid||"");
    if(!/^[a-z0-9]{12,40}$/.test(uid)) return json_({ok:false,err:"uid"});
    const sh = hoja_(); const v = sh.getDataRange().getValues();
    let fila = -1; for(let i=1;i<v.length;i++) if(v[i][0]===uid){ fila=i; break; }

    if(b.accion==="baja"){ if(fila>0) sh.deleteRow(fila+1); return json_({ok:true}); }

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
