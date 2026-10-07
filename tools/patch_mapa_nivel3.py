#!/usr/bin/env python3
"""Mapa conceptual: tercer nivel («Para saber más») en cada idea secundaria.
Añade el campo x (lista de {k,v} en es/en) a los nodos de data/temaNN.json y tools/mapas.json,
y el código que lo muestra en index.html. Uso: python3 tools/patch_mapa_nivel3.py"""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
X = {n: json.load(open(os.path.join(R, "tools", f"mapa_x_tema{n:02d}.json"))) for n in (1, 2, 3)}
def add(mapa, x):
    for r in mapa['ramas']:
        for i, n in enumerate(r['nodos']):
            k = f"{r['code']}.{i}"
            if k in x: n['x'] = x[k]
M = json.load(open(os.path.join(R, 'tools', 'mapas.json')))
for num, x in X.items():
    p = os.path.join(R, 'data', f'tema{num:02d}.json')
    t = json.load(open(p)); add(t['mapa'], x); json.dump(t, open(p, 'w'), ensure_ascii=False, indent=1)
    add(M[str(num)], x)
json.dump(M, open(os.path.join(R, 'tools', 'mapas.json'), 'w'), ensure_ascii=False, indent=1)

p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'class="mx"' not in s:
    old = '<div class="nd">${md(L(n.d))}<div class="acts">'
    assert old in s
    s = s.replace(old, '<div class="nd">${md(L(n.d))}${n.x?`<div class="mx"><div class="mxh">${t("mapMore")}</div>${(n.x[S.lang]||n.x.es).map(it=>`<div class="mxi"><span class="mxk mxk-${esc(it.k)}">${esc(t("mapK."+it.k))}</span>${md(it.v)}</div>`).join("")}</div>`:""}<div class="acts">', 1)
    a = s.index('mapPractice:"'); b = s.index('mapPractice:"', a + 20)
    s = (s[:a] + 'mapMore:"Para saber más", mapK:{concepto:"Concepto",autor:"Autor",fecha:"Fecha",ejemplo:"Ejemplo"}, ' + s[a:b]
         + 'mapMore:"Learn more", mapK:{concepto:"Concept",autor:"Author",fecha:"Date",ejemplo:"Example"}, ' + s[b:])
    css = '''.mx{margin:10px 0 4px;padding:10px 12px;background:#F4F7FB;border-radius:12px;border-left:3px solid var(--rc,var(--primary))}
.mxh{font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--primary-2);margin-bottom:6px}
.mxi{margin:8px 0;font-size:14px;line-height:1.45}
.mxk{display:inline-block;margin-right:6px;vertical-align:1px;font-size:10px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:1px 6px;border-radius:6px;border:1px solid var(--primary);color:var(--primary);background:#fff}
.mxk-autor{background:var(--primary);color:#fff}
.mxk-fecha{border-color:#8A5A00;color:#8A5A00}
.mxk-ejemplo{background:#FFF3D6;border-color:#C77700;color:#7A4A00}
</style>'''
    assert s.count('</style>') == 1
    s = s.replace('</style>', css, 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
