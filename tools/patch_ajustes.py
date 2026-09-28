#!/usr/bin/env python3
"""Acceso visible a Ajustes desde la portada (además de la rueda de la cabecera).
Uso: python3 tools/patch_ajustes.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'id="setBtn"' in s:
    print('ya aplicado'); raise SystemExit
old = '''    <div id="temaList"><div class="empty">…</div></div>
    <p style="font-size:12px;color:var(--muted);text-align:center;margin-top:10px">${t("author")}</p></main>`;'''
assert old in s
s = s.replace(old, '''    <div id="temaList"><div class="empty">…</div></div>
    <button class="tema" id="setBtn" style="margin-top:6px"><div class="num" style="background:#EAF1F8;color:var(--primary-2)">⚙️</div><div class="t"><b>${t("setHome")}</b><span>${t("setHomeSub")}</span></div><div class="pct">›</div></button>
    <p style="font-size:12px;color:var(--muted);text-align:center;margin-top:10px">${t("author")}</p></main>`;''', 1)
old = ''' document.getElementById("searchBtn").onclick=()=>nav({name:"search"});'''
assert old in s
s = s.replace(old, old + ''' document.getElementById("setBtn").onclick=()=>nav({name:"settings",from:{name:"home"}});''', 1)
a = s.index('searchAll:"Buscar en todas las fichas"')
s = s[:a] + 'setHome:"Ajustes y ayuda", setHomeSub:"Idioma, instalar en el móvil, privacidad y cerrar sesión", ' + s[a:]
b = s.index('searchAll:"Search all study sheets"')
s = s[:b] + 'setHome:"Settings and help", setHomeSub:"Language, install on your phone, privacy and log out", ' + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('ok')
