#!/usr/bin/env python3
"""«Tarjetas» pasa a «Análisis de imágenes» (EN «Image analysis») en toda la app y en la guía del examen,
y el botón «Ajustes y ayuda» sube al principio de la portada.  Uso: python3 tools/patch_nombres.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
s = s.replace('cards:"Tarjetas"', 'cards:"Análisis de imágenes"', 1)
s = s.replace('cards:"Cards"', 'cards:"Image analysis"', 1)
s = s.replace('cards:"¿Verdadero o falso? Desliza"', 'cards:"¿Verdadero o falso? Desliza cada imagen"', 1)
s = s.replace('cards:"True or false? Swipe"', 'cards:"True or false? Swipe each image"', 1)
assert 'cards:"Análisis de imágenes"' in s and 'cards:"Image analysis"' in s
btn = '''    <button class="tema" id="setBtn" style="margin-top:6px"><div class="num" style="background:#EAF1F8;color:var(--primary-2)">⚙️</div><div class="t"><b>${t("setHome")}</b><span>${t("setHomeSub")}</span></div><div class="pct">›</div></button>\n'''
if btn in s:
    s = s.replace(btn, '', 1)
    old = '''  app.innerHTML=header("Historiapp",false)+`<main>\n'''
    assert old in s
    s = s.replace(old, old + btn.replace(' style="margin-top:6px"', ''), 1)
open(p, 'w', encoding='utf-8').write(s)

for f in ('data/examen.json', 'tools/examen.json'):
    q = os.path.join(R, f)
    if not os.path.exists(q): continue
    t = open(q, encoding='utf-8').read()
    for a, b in [('**Tarjetas**', '**Análisis de imágenes**'), ('(tarjetas del tema 2)', '(análisis de imágenes del tema 2)'),
                 ('**Cards**', '**Image analysis**'), ('(unit 2 cards)', '(unit 2 image analysis)')]:
        t = t.replace(a, b)
    open(q, 'w', encoding='utf-8').write(t)
print('ok')
