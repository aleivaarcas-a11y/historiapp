/* Historiapp · Ranking semanal (Apps Script que escribe en la hoja «Historiapp - Ranking» de Drive)
   Columna «oculto»: escribe X para sacar a alguien del ranking (alias ofensivo, puntos absurdos). */
const HOJA = "Jugadores";
const TOPE_DIA = 1500;          // puntos máximos que cuentan por alumno y día
const CAB = ["uid","alias","ultimaXP","total","semana","puntosSemana","dia","puntosHoy","actualizado","oculto","grupo","nombre","apellido1","apellido2"];
const GRUPOS = ["1ºA","1ºB","1ºTAMA","1ºEnglish"];
// nombre y apellidos solo se guardan en esta hoja: doGet nunca los devuelve
const TZ = "Europe/Madrid";

function hoja_(){
  const ss = SpreadsheetApp.openById("18Wr8HdKY6nsR_gNK2KiWb0q0ljjB1Rxd6YLRKOK5XQ4");
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
function json_(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function limpiaAlias_(a){
  a = String(a||"").replace(/\s+/g," ").trim();
  if(a.length<3 || a.length>16) return null;
  if(!/^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _.\-]+$/.test(a)) return null;
  return a;
}
function limpiaNombre_(a, obligatorio){
  a = String(a||"").replace(/\s+/g," ").trim().slice(0,40);
  if(!a) return obligatorio ? null : "";
  if(!/^[A-Za-zÀ-ÿ' .\-]+$/.test(a)) return null;
  return a;
}

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
    const low = alias.toLowerCase();
    for(let i=1;i<v.length;i++) if(i!==fila && String(v[i][1]).toLowerCase()===low) return json_({ok:false,err:"ocupado"});

    const grupo = GRUPOS.indexOf(b.grupo)>=0 ? b.grupo : null; if(!grupo) return json_({ok:false,err:"grupo"});
    const nombre = limpiaNombre_(b.nombre,true), ap1 = limpiaNombre_(b.apellido1,true), ap2 = limpiaNombre_(b.apellido2,false);
    if(nombre===null || ap1===null || ap2===null) return json_({ok:false,err:"nombre"});
    const xp = Math.max(0, Math.floor(Number(b.xp)||0));
    const sem = semana_(), dia = hoy_(), ahora = new Date();
    if(fila<0){ sh.appendRow([uid,alias,xp,0,sem,0,dia,0,ahora,"",grupo,nombre,ap1,ap2]); return json_({ok:true,semana:0}); }

    let [ , , ultima, total, s, pSem, d, pHoy, , oculto] = v[fila];
    if(s!==sem && Utilities.formatDate(new Date(s),TZ,"yyyy-MM-dd")!==sem){ s=sem; pSem=0; }
    if(d!==dia && Utilities.formatDate(new Date(d),TZ,"yyyy-MM-dd")!==dia){ d=dia; pHoy=0; }
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
  const v = hoja_().getDataRange().getValues().slice(1)
    .filter(r=>!String(r[9]).trim())
    .map(r=>({uid:r[0],alias:r[1],grupo:r[10],total:Number(r[3])||0,
      semana:(r[4]===sem||Utilities.formatDate(new Date(r[4]),TZ,"yyyy-MM-dd")===sem)?(Number(r[5])||0):0}));
  const tabla = (k,g)=>{
    const o = v.filter(x=>x[k]>0 && (!g || x.grupo===g)).sort((a,b)=>b[k]-a[k]);
    const yo = o.findIndex(x=>x.uid===uid);
    return {top:o.slice(0,10).map((x,i)=>({p:i+1,alias:x.alias,grupo:x.grupo,pts:x[k],yo:x.uid===uid})),
            yo: yo>=0?{p:yo+1,pts:o[yo][k]}:null, n:o.length};
  };
  const grupos = {}; GRUPOS.forEach(g=>grupos[g]=tabla("semana",g));
  return json_({ok:true, semana:sem, sem:tabla("semana"), total:tabla("total"), grupos:grupos});
}
