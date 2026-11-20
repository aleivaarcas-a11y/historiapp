#!/usr/bin/env python3
"""Historiapp, 20-11-2026: añade el «Simulacro de test» (examen tipo test con los temas que se elijan) a index.html.
Uso: python3 patch_simulacro.py ruta/index.html ruta/simu.js
Se aplica sobre la versión más reciente de index.html; si ya está aplicado, no hace nada."""
import sys

idx, js = sys.argv[1], sys.argv[2]
s = open(idx, encoding="utf-8").read()
if "function renderSimu(" in s:
    print("ya aplicado"); sys.exit(0)
code = open(js, encoding="utf-8").read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"ancla {n} veces (esperaba {count}): {old[:70]!r}")
    s = s.replace(old, new)

CSS = """/* simulacro de test (20-11-2026) */
.smlead{font-size:14.5px;line-height:1.5;margin-top:6px}
.smchips{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.smchip{background:var(--paper);border:2px solid var(--line);border-radius:14px;padding:10px 12px;text-align:left;display:flex;flex-direction:column;gap:2px;position:relative}
.smchip b{font-size:20px;color:var(--muted)}
.smchip span{font-size:13.5px;font-weight:700;line-height:1.25;padding-right:20px}
.smchip small{font-size:12px;color:var(--muted)}
.smchip.on{border-color:var(--primary);background:var(--warm)}
.smchip.on b{color:var(--tp)}
.smchip.on:after{content:"✓";position:absolute;top:8px;right:10px;width:22px;height:22px;border-radius:50%;background:var(--primary);color:#fff;font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center}
.smchip:disabled{opacity:.45}
.smseg button{flex:1}
.smmodes{display:flex;flex-direction:column;gap:10px}
.smmode{background:var(--paper);border:2px solid var(--line);border-radius:14px;padding:12px 14px;text-align:left;display:flex;flex-direction:column;gap:3px}
.smmode b{font-size:15.5px}
.smmode span{font-size:13px;color:var(--muted);line-height:1.35}
.smmode.on{border-color:var(--primary);background:var(--warm)}
.smhist{padding:6px 14px}
.smhist div{display:flex;gap:10px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.smhist div:last-child{border-bottom:0}
.smhist span:nth-child(2){flex:1;color:var(--muted)}
.smhist b{color:var(--tp);font-size:15px}
.smbar{position:sticky;top:-16px;z-index:6;margin:-16px -16px 0;padding:10px 16px;background:var(--bg);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;font-weight:700;font-size:14px}
.smbar span{flex:1}
.smbar button{background:var(--primary);color:#fff;font-weight:700;padding:9px 16px;border-radius:12px}
.smrule{font-size:13px;color:var(--muted);line-height:1.45;margin:0 4px}
.smq{display:flex;flex-direction:column;gap:10px}
.smqh{display:flex;align-items:center;gap:8px}
.smqh b{width:28px;height:28px;border-radius:8px;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px}
.smqh small{color:var(--muted);font-size:12px;font-weight:600}
.smqh em{margin-left:auto;font-style:normal;font-weight:800;font-size:13px}
.smq.ok .smqh em{color:var(--ok)}
.smq.ko .smqh em{color:var(--ko)}
.smq.bl .smqh em{color:var(--muted)}
.smq .qtext{font-size:16px}
.opt.sel{border-color:var(--primary);background:var(--warm)}
.opt.sel .k{background:var(--primary);color:#fff}
.smexp{font-size:13.5px;line-height:1.5;background:var(--warm);border-radius:10px;padding:10px 12px}
.smsum{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;font-weight:700;font-size:14px}
.smcalc{font-size:13px;color:var(--muted);line-height:1.45}
.smtem{display:flex;flex-direction:column;gap:8px;padding:12px 14px}
.smtem div{display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:600}
.smtem div span:first-child{width:64px}
.smtem i{flex:1;height:8px;border-radius:99px;background:var(--line);overflow:hidden}
.smtem i b{display:block;height:100%;background:var(--tp)}
"""
rep("/* examen */\n", CSS + "/* examen */\n")

ES = dict(
 smCardS="Simulacro de test", smCardB="Hazte un examen tipo test",
 smCardSub="Con las preguntas de los temas que elijas y la nota calculada como en el examen",
 smTitle="Simulacro de test",
 smLead="Elige los temas que entran, cuántas preguntas quieres y cómo quieres hacerlo. Las preguntas se reparten por igual entre los temas elegidos.",
 smTemas="Temas", smNq="{n} preguntas", smAllT="Marcar todos", smNone="Quitar todos",
 smHowMany="Número de preguntas", smTodas="Todas", smModo="Modo",
 smExam="Examen", smExamSub="Como el test real, con penalización por fallo y sin ver las soluciones hasta que entregas",
 smPrac="Práctica", smPracSub="Una pregunta cada vez, con 20 segundos y la corrección al momento",
 smStart="Empezar ({n} preguntas)", smPick="Elige al menos un tema",
 smHist="Tus últimos simulacros", smHistT="Temas {t} · {n} preg.",
 smRule="Funciona como el test del examen, con cuatro opciones y una sola correcta, de modo que cada tres fallos se descuenta un acierto y las preguntas en blanco ni suman ni restan. Si vuelves a tocar la opción marcada, la pregunta queda en blanco. Las soluciones aparecen al entregar.",
 smAns="Respondidas {a} de {b}", smSend="Entregar",
 smBlank1="Queda 1 pregunta en blanco. ¿Entregas el examen?", smBlankN="Quedan {n} preguntas en blanco. ¿Entregas el examen?",
 smLeave="Si sales ahora, se pierde este simulacro. ¿Quieres salir?",
 smDone="Simulacro terminado", smOver10="Nota sobre 10",
 smA="{n} aciertos", smF="{n} fallos", smB="{n} en blanco",
 smA1="1 acierto", smF1="1 fallo",
 smCalc="Se calcula como en el examen, restando a los aciertos un tercio de los fallos y dividiendo entre el número de preguntas.",
 smReal="En el examen real, el test te daría {x} de sus 5 puntos.",
 smAgain="Otro simulacro con los mismos temas", smToRp="Repasar mis fallos", smChange="Cambiar temas o modo",
 smReview="Corrección", smBl="En blanco",
)
EN = dict(
 smCardS="Practice test", smCardB="Take a multiple-choice test",
 smCardSub="With questions from the units you choose and the mark worked out as in the exam",
 smTitle="Practice test",
 smLead="Choose the units, how many questions you want and how you want to take it. The questions are shared out evenly among the units you choose.",
 smTemas="Units", smNq="{n} questions", smAllT="Select all", smNone="Clear all",
 smHowMany="Number of questions", smTodas="All", smModo="Mode",
 smExam="Exam", smExamSub="Like the real test, with a penalty for wrong answers and no solutions until you hand it in",
 smPrac="Practice", smPracSub="One question at a time, 20 seconds each, marked straight away",
 smStart="Start ({n} questions)", smPick="Choose at least one unit",
 smHist="Your last practice tests", smHistT="Units {t} · {n} q.",
 smRule="It works like the exam test, with four options and only one correct, so every three wrong answers cancel one correct answer and blank questions neither add nor subtract. Tap the chosen option again to leave the question blank. The solutions appear when you hand it in.",
 smAns="{a} of {b} answered", smSend="Hand in",
 smBlank1="1 question is blank. Hand in the test?", smBlankN="{n} questions are blank. Hand in the test?",
 smLeave="If you leave now, this practice test will be lost. Leave?",
 smDone="Practice test finished", smOver10="Mark out of 10",
 smA="{n} correct", smF="{n} wrong", smB="{n} blank",
 smA1="1 correct", smF1="1 wrong",
 smCalc="Worked out as in the exam, taking a third of the wrong answers off the correct ones and dividing by the number of questions.",
 smReal="In the real exam, the test would give you {x} of its 5 points.",
 smAgain="Another test with the same units", smToRp="Review my mistakes", smChange="Change units or mode",
 smReview="Answers", smBl="Blank",
)
import json
i18n = "/* 20-11-2026: simulacro de test */\nObject.assign(I18N.es," + json.dumps(ES, ensure_ascii=False) + ");\nObject.assign(I18N.en," + json.dumps(EN, ensure_ascii=False) + ");\n"
a = s.index("Object.assign(I18N.en,{rpCard:")
e = s.index("\n", a) + 1
s = s[:e] + i18n + s[e:]

rep('if(v.name==="exam") return "examen";', 'if(v.name==="exam") return "examen"; if(v.name==="simu") return "simulacro";')
rep('if(h==="examen") return {name:"exam"};', 'if(h==="examen") return {name:"exam"}; if(h==="simulacro") return {name:"simu"};')
rep('  if(v.name==="exam") return renderExam();\n', '  if(v.name==="exam") return renderExam();\n  if(v.name==="simu") return renderSimu();\n')

HOME = """rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc);
  /* 20-11-2026: simulacro de test, petición de los alumnos; segunda tarjeta de «Hoy», tras el reto del día */
  { const hs=S.prog.simuHist||[], last=hs[hs.length-1]; const sc=document.createElement("button"); sc.className="card reto";
    sc.innerHTML=`<div class="ic" aria-hidden="true">📝</div><div class="tx"><small>${t("smCardS")}</small><b>${t("smCardB")}</b><span>${t("smCardSub")}</span></div><div class="xp">${last?smNota(last.nota):"›"}</div>`;
    sc.onclick=()=>nav({name:"simu",back:{name:"home"}}); hoy.appendChild(sc); }
  rkHomeCard(hoy);"""
rep('rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc); rkHomeCard(hoy);', HOME)

# pestaña Examen encendida en el simulacro
rep('if(n==="exam") return "exam";', 'if(n==="exam"||n==="simu") return "exam";')

# botón al simulacro al principio de «Cómo preparar el examen»
EXB = """${md(G.lead)}</p></div>
    <div class="hoy"><button class="card reto" id="xSimu"><div class="ic" aria-hidden="true">📝</div><div class="tx"><small>${t("smCardS")}</small><b>${t("smCardB")}</b><span>${t("smCardSub")}</span></div><div class="xp">›</div></button></div>"""
rep('${md(G.lead)}</p></div>', EXB)
rep('  app.querySelectorAll(".xcheck input").forEach(c=>c.onchange=', '  document.getElementById("xSimu").onclick=()=>nav({name:"simu",back:{name:"exam"}});\n  app.querySelectorAll(".xcheck input").forEach(c=>c.onchange=')

rep("/* --- cómo preparar el examen --- */\n", code.rstrip("\n") + "\n\n/* --- cómo preparar el examen --- */\n")

G_ES = ' ["📝","Simulacro de test","Desde la portada eliges los temas, el número de preguntas y el modo. En el modo examen respondes como en el test real, con la misma penalización por fallo, y al entregar ves la nota y la corrección de cada pregunta. En el modo práctica cada pregunta se corrige al momento. Las preguntas que fallas pasan al repaso de fallos."],\n'
G_EN = ' ["📝","Practice test","From the home screen you choose the units, the number of questions and the mode. In exam mode you answer as in the real test, with the same penalty for wrong answers, and when you hand it in you see your mark and the answer to every question. In practice mode each question is marked straight away. The questions you miss go to the mistakes review."],\n'
a = s.index(' ["🎓","Examen",'); e = s.index("\n", a) + 1; s = s[:e] + G_ES + s[e:]
a = s.index(' ["🎓","Exam",'); e = s.index("\n", a) + 1; s = s[:e] + G_EN + s[e:]

open(idx, "w", encoding="utf-8").write(s)
print("aplicado")
