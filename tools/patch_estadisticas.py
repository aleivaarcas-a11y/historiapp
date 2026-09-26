#!/usr/bin/env python3
# Estadísticas anónimas con GoatCounter (sin cookies ni datos personales) y aviso de privacidad en Ajustes.
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
s = open('index.html', encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

helper = r'''<script>
/* ---- estadísticas anónimas (GoatCounter: sin cookies ni datos personales) ---- */
const GC_CODE="historiapp";
const GCQ=[]; let GCOK=false;
(function(){ if(!GC_CODE) return; try{ const sc=document.createElement("script"); sc.async=true; sc.src="https://gc.zgo.at/count.js";
  sc.dataset.goatcounter="https://"+GC_CODE+".goatcounter.com/count"; sc.dataset.goatcounterSettings='{"no_onload":true}';
  sc.onload=()=>{ GCOK=true; while(GCQ.length) track(...GCQ.shift()); }; document.head.appendChild(sc); }catch(e){} })();
function track(path,title,event){ try{ if(!GC_CODE) return; if(!GCOK||!window.goatcounter||!window.goatcounter.count){ if(GCQ.length<50) GCQ.push([path,title,event]); return; }
  window.goatcounter.count({path:path, title:title||path, event:!!event}); }catch(e){} }
'''
rep('<script>\n', helper, )

# vistas de página: una por pantalla
rep('function render(){\n  const v=S.view;\n', 'function render(){\n  const v=S.view;\n  if(v.name!=="gate") track("/"+(S.lang||"es")+"/"+(viewToHash(v)||"inicio"));\n')

# eventos
rep('const vid=m.querySelector("video"); vid.play().catch(()=>{});',
    'const vid=m.querySelector("video"); vid.play().catch(()=>{}); let played=false; vid.addEventListener("play",()=>{ if(!played){ played=true; track("video/"+v.id+"/"+S.lang,"Vídeo "+v.id,true); } });')
rep('const k=+b.dataset.k, ok=k===q.a;', 'const k=+b.dataset.k, ok=k===q.a; track("video-test/"+v.id+"/"+(ok?"acierto":"fallo"),"Test vídeo "+v.id,true);')
rep('function resultScreen(m,tema,mode,correct,total,again){\n',
    'function resultScreen(m,tema,mode,correct,total,again){\n  track("ronda/"+tema.id+"/"+mode+"/"+(Math.round(correct/total*10)*10)+"%","Ronda "+mode,true);\n')
rep('S.prog.daily={date:todayKey(),done:true,correct,total:steps.length}; save();',
    'S.prog.daily={date:todayKey(),done:true,correct,total:steps.length}; save(); track("reto/completado/"+Math.round(correct/steps.length*10)*10+"%","Reto del día",true);')
rep('async function installApp(){\n', 'async function installApp(){\n  track("instalar","Instalar",true);\n')

# aviso de privacidad y de progreso local en Ajustes
rep('version:"Contenido actualizado",', 'privacy:"Tu progreso (XP, rachas, insignias) se guarda solo en este móvil y nadie más lo ve. Para no perderlo, instala la app y úsala siempre desde el icono. La app cuenta de forma anónima qué pantallas se visitan, sin cookies ni datos personales, para mejorar la asignatura.", version:"Contenido actualizado",')
rep('version:"Content updated",', 'privacy:"Your progress (XP, streaks, badges) is stored only on this phone and nobody else sees it. To keep it, install the app and always open it from its icon. The app counts anonymously which screens are visited, with no cookies or personal data, to improve the course.", version:"Content updated",')
rep('<p style="font-size:12px;color:var(--muted);text-align:center">${t("version")}:',
    '<p style="font-size:12.5px;color:var(--muted);line-height:1.5;margin:0 4px">🔒 ${t("privacy")}</p>\n    <p style="font-size:12px;color:var(--muted);text-align:center">${t("version")}:')

open('index.html', 'w', encoding='utf-8').write(s)
sw = open('sw.js').read(); sw = re.sub(r'historiapp-v\d+', 'historiapp-v9', sw); open('sw.js', 'w').write(sw)
print('ok')
