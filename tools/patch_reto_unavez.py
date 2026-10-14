# 13-10-2026: el reto del día solo puede hacerse una vez por día.
# Antes: el avance solo se guardaba al terminar, así que salir y volver a entrar reiniciaba el reto con las mismas
# preguntas y el doble de XP; además, al salir a mitad, el multiplicador x2 seguía activo en el resto de la app.
import sys, re
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
old_a = """  const d=S.prog.daily||{}; if(d.date===todayKey() && d.done){ return dailyResult(m,d.correct,d.total); }
  let k=0, correct=0; S.xpMult=2;
  function step(){"""
new_a = """  const d=S.prog.daily||{}; if(d.date===todayKey() && d.done){ return dailyResult(m,d.correct,d.total); }
  /* una sola vez al día: el avance se guarda al mostrar cada prueba; si sales a mitad, al volver sigues en la siguiente sin repetir ninguna */
  let k=0, correct=0; if(d.date===todayKey()){ k=Math.min(Number(d.k)||0,steps.length); correct=Number(d.correct)||0; }
  S.xpMult=2;
  function step(){"""
old_b = """    const st=steps[k]; const fn={cards:modeSwipe"""
new_b = """    S.prog.daily={date:todayKey(),done:false,k:k+1,correct,total:steps.length}; save();
    const st=steps[k]; const fn={cards:modeSwipe"""
old_c = """{order:[st.i],onDone:(c)=>{ correct+=c; k++; step(); }});"""
new_c = """{order:[st.i],onDone:(c)=>{ if(S.view.name!=="daily") return; correct+=c; k++; S.prog.daily={date:todayKey(),done:false,k,correct,total:steps.length}; save(); step(); }});"""
old_d = """function render(){
  const v=S.view;"""
new_d = """function render(){
  const v=S.view; if(v.name!=="daily") S.xpMult=1;"""
for o,n in [(old_a,new_a),(old_b,new_b),(old_c,new_c),(old_d,new_d)]:
    if s.count(o)!=1: sys.exit("no encontrado: "+o[:60])
    s = s.replace(o,n)
open(p,"w",encoding="utf-8").write(s); print("ok")
