# 22-10-2026: el repaso de fallos guarda y muestra el texto de las preguntas de Fuentes
# (aviso de un alumno: «¿Qué autor describe así la educación persa?» salía sin la cita).
import re,sys,pathlib
p=pathlib.Path(__file__).resolve().parent.parent/"index.html"; s=p.read_text(encoding="utf-8")
if "rpFillX" in s: print("ya aplicado"); sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:60]; s=s.replace(a,b)
rep('function rpFallo(g,q,o,f,tm){ const d=rpLoad(), id=rpId(q), it=d.items[id]||{g,q,o,f:f||null,t:tm||null,box:0,n:0}; ',
    'function rpFallo(g,q,o,f,tm,x){ const d=rpLoad(), id=rpId(q), it=d.items[id]||{g,q,o,f:f||null,t:tm||null,box:0,n:0}; if(x&&!it.x) it.x=x; ')
rep('return {es:oo.map(x=>x&&x.es||x),en:oo.map(x=>x&&(x.en||x.es)||x)}; })(),null,tema.num); }catch(_){}',
    'return {es:oo.map(x=>x&&x.es||x),en:oo.map(x=>x&&(x.en||x.es)||x)}; })(),null,tema.num,mode==="sources"?it.text:null); }catch(_){}')
# fallos antiguos sin texto: se busca la cita en el tema por el enunciado
rep('function renderRepaso(){',
    '''async function rpFillX(items){ const d=rpLoad(); let ch=false;
  for(const it of items){ if(it.x||!it.t||!it.q||!it.q.es) continue;
    try{ const tm=await getTema(it.t), hit=(tm.sources||[]).find(s=>s.question&&s.question.es===it.q.es&&s.text);
      if(hit){ it.x=hit.text; if(d.items[it.id]){ d.items[it.id].x=hit.text; ch=true; } } }catch(_){} }
  if(ch) rpSave(d); }
function renderRepaso(){''')
rep('<div class="card qtext">${esc(L(it.q))}</div><div class="opts">${ch.map((x,k)=>`<button class="opt" data-i="${x.i}"><span class="k">${"ABCDE"[k]}</span>',
    '${it.x?`<div class="quote">${esc(L(it.x))}</div><div class="qtext">${esc(L(it.q))}</div>`:`<div class="card qtext">${esc(L(it.q))}</div>`}<div class="opts">${ch.map((x,k)=>`<button class="opt" data-i="${x.i}"><span class="k">${"ABCDE"[k]}</span>')
rep('else { rpFallo(it.g,it.q,it.o,it.f,it.t); msg=t("rpWrong"); }','else { rpFallo(it.g,it.q,it.o,it.f,it.t,it.x); msg=t("rpWrong"); }')
rep('''      const xp=ok?10:2; addXP(xp); sheet(ok, ok?t("correct"):t("wrong"), msg, xp, ()=>{ pos++; draw(); }, L(it.q)); });
  }
  draw();''','''      const xp=ok?10:2; addXP(xp); sheet(ok, ok?t("correct"):t("wrong"), msg, xp, ()=>{ pos++; draw(); }, L(it.q)); });
  }
  rpFillX(items).then(draw,draw);''')
p.write_text(s,encoding="utf-8"); print("aplicado")
