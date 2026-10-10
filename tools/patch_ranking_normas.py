# Historiapp · normas del ranking en el alta (10-10-2026). Uso: python3 tools/patch_ranking_normas.py
import re, sys
P="index.html"; s=open(P,encoding="utf-8").read()
if "rkRulesT" in s: sys.exit("Las normas ya están aplicadas.")
def rep(old,new):
    global s
    if s.count(old)!=1: sys.exit("No encuentro: "+old[:70])
    s=s.replace(old,new)
ES='rkRulesT:"Normas del ranking",rkRules:"Los alias no pueden contener palabras malsonantes, insultos ni expresiones racistas, sexistas u homófobas, y tampoco el nombre de otra persona, sea un compañero, un profesor o un personaje conocido. El alias que incumpla estas normas se retirará, y su autor podrá ser sancionado según los artículos 10 a 12 de las Normas de Convivencia Universitaria y Reglamento de Régimen Interno de la UCAM, que tipifican como falta las palabras impropias y las ofensas a otros miembros de la comunidad universitaria.",rkAccept:"He leído y acepto las normas del ranking.",rkMustAccept:"Para entrar tienes que aceptar las normas del ranking.",'
EN='rkRulesT:"Leaderboard rules",rkRules:"Nicknames must not contain offensive language, insults or racist, sexist or homophobic expressions, nor the name of another person, whether a classmate, a lecturer or a well-known figure. Any nickname that breaks these rules will be removed, and its author may be sanctioned under Articles 10 to 12 of the UCAM Rules of University Conduct and Internal Regulations (Normas de Convivencia Universitaria y Reglamento de Régimen Interno), which classify improper language and offences against other members of the university community as disciplinary offences.",rkAccept:"I have read and accept the leaderboard rules.",rkMustAccept:"You must accept the leaderboard rules to join.",'
rep('Object.assign(I18N.es,{rkT:"Ranking",','Object.assign(I18N.es,{'+ES+'rkT:"Ranking",')
rep('Object.assign(I18N.en,{rkT:"Leaderboard",','Object.assign(I18N.en,{'+EN+'rkT:"Leaderboard",')
RULES='<div class="rk-rules"><b>⚖️ ${t("rkRulesT")}</b><p>${t("rkRules")}</p>'
# alta: normas + casilla obligatoria
rep('<p class="rk-priv">🔒 ${t("rkPriv")}</p><p class="rk-err" id="rkE" role="alert"></p>\n    <button class="btn" id="rkGo">${t("rkJoinBtn")}</button></div>`;',
    RULES+'<label class="rk-chk"><input type="checkbox" id="rkOk"> <span>${t("rkAccept")}</span></label></div>\n    <p class="rk-priv">🔒 ${t("rkPriv")}</p><p class="rk-err" id="rkE" role="alert"></p>\n    <button class="btn" id="rkGo">${t("rkJoinBtn")}</button></div>`;')
rep('    if(!d.grupo) return E.textContent=rkErrMsg("grupo");','    if(!d.grupo) return E.textContent=rkErrMsg("grupo");\n    if(!$("rkOk").checked) return E.textContent=t("rkMustAccept");')
rep('    if(d.alias.length<3||d.alias.length>16||!/^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _.\\-]+$/.test(d.alias)) return E.textContent=rkErrMsg("alias");\n    E.textContent="";',
    '    if(d.alias.length<3||d.alias.length>16||!/^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ _.\\-]+$/.test(d.alias)) return E.textContent=rkErrMsg("alias");\n    if(!$("rkOk").checked) return E.textContent=t("rkMustAccept");\n    E.textContent="";')
# alias retirado: recordar las normas
rep('<label>${t("rkNewAlias")}<input id="rkAl" maxlength="16" autocomplete="off" autocapitalize="off"><small>${t("rkAliasHint")}</small></label>\n    <p class="rk-err"',
    '<label>${t("rkNewAlias")}<input id="rkAl" maxlength="16" autocomplete="off" autocapitalize="off"><small>${t("rkAliasHint")}</small></label>\n    '+RULES+'</div>\n    <p class="rk-err"')
CSS='.rk-rules{margin:16px 0 4px;padding:12px 14px;border:1.5px solid var(--accent);border-radius:12px;background:var(--warm)}\n.rk-rules b{font-size:14px}\n.rk-rules p{font-size:13px;margin:6px 0 0;line-height:1.5}\n.rk-form label.rk-chk{display:flex;gap:10px;align-items:flex-start;font-weight:700;font-size:13.5px;margin:10px 0 0;cursor:pointer}\n.rk-form label.rk-chk input{width:20px;height:20px;margin:1px 0 0;flex:0 0 20px;padding:0;accent-color:var(--primary)}\n'
i=s.index("</style>"); s=s[:i]+CSS+s[i:]
open(P,"w",encoding="utf-8").write(s)
w=open("sw.js",encoding="utf-8").read(); m=re.search(r'historiapp-v(\d+)',w); n=int(m.group(1))+1
open("sw.js","w",encoding="utf-8").write(w.replace(m.group(0),"historiapp-v%d"%n)); print("Normas añadidas; service worker v%d"%n)
