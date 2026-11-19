#!/usr/bin/env python3
"""Tema 5 en Historiapp (19-11-2026): portada del tema, colores de la línea del tiempo (China, Japón e India),
eras e hitos del Tema 5 en data/linea.json, juegos de la sala con el Tema 5 y tema disponible en data/temas.json.
Copia previa: tools/index_antes_t5.html"""
import os, json, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
import construir_fichas as CF
if not os.path.exists('tools/index_antes_t5.html'): shutil.copy('index.html', 'tools/index_antes_t5.html')
h = open('index.html', encoding='utf-8').read()
if '5:"img/t5/' not in h:
    h = h.replace('4:"img/t4/mosaico_aurigas_merida.jpg"};', '4:"img/t4/mosaico_aurigas_merida.jpg",5:"img/t5/s22.jpg"};', 1)
assert '5:"img/t5/s22.jpg"' in h
if '--ln-chn' not in h:
    h = h.replace('--ln-rom2:#D9A3B5;', '--ln-rom2:#D9A3B5;--ln-chn:#B8262A;--ln-chn2:#E8A3A0;--ln-jap:#2E3A59;--ln-jap2:#A9B4D6;--ln-ind:#D9822B;--ln-ind2:#F2C99A;', 1)
    h = h.replace('html.dark{--ln-etr:#D08A47;', 'html.dark{--ln-chn:#D9534F;--ln-chn2:#5A1F1F;--ln-jap:#6A7BB0;--ln-jap2:#2A3150;--ln-ind:#E89A4A;--ln-ind2:#6B3E14;--ln-etr:#D08A47;', 1)
    css = ''.join(f'.ln-era.c-{c}{{background:var(--ln-{c})}}.ln-era.c-{c}.alt{{background:var(--ln-{c}2);color:#1d252d}}.ln-sw.c-{c}{{background:var(--ln-{c})}}' for c in ('chn', 'jap', 'ind'))
    h = h.replace('.ln-sw.c-rom{background:var(--ln-rom)}', '.ln-sw.c-rom{background:var(--ln-rom)}' + css, 1)
    assert h.count('--ln-chn') >= 4 and 'c-ind.alt' in h
# juegos de la sala que ya llevan preguntas del Tema 5
for f in ('juegos/trivium.html', 'juegos/historiapp-arena.html', 'juegos/historiapp-brawl.html'):
    k = h.index('{f:"' + f + '"'); j = h.index('temas:[', k); e = h.index(']', j)
    if '5' not in h[j:e].split('[')[1].split(','): h = h[:e] + ',5' + h[e:]
open('index.html', 'w', encoding='utf-8').write(h)
# línea del tiempo: la fuente de cada hito sale de la Fuente de su diapositiva
sl = {s['slide']: s for s in json.load(open('tools/fuentes/t5_slides.json'))}
def fuente(n):
    out = []
    for p in sl[n]['paras']:
        if CF.is_ref(p):
            m = re.match(r"^(.+?)\s*\((\d{4}[a-z]?|s\. f\.)\)", p)
            if m:
                au = m.group(1).strip().rstrip(',')
                parts = [x.strip() for x in re.split(r",\s*(?:y\s+)?|\s+y\s+", au) if x.strip()]
                surn = [x for x in parts if not re.fullmatch(r"(?:[A-ZÁÉÍÓÚ]\.[\s-]*)+(?:[A-ZÁÉÍÓÚ]\.)?(?:,?\s*III)?", x) and x not in ('et al.', 'III')]
                if len(surn) > 2: a = surn[0] + ' et al.'
                elif len(surn) == 2: a = surn[0] + ' y ' + surn[1]
                else: a = surn[0] if surn else au
                out.append(f"{a} ({m.group(2)})")
    return '; '.join(dict.fromkeys(out))
L = json.load(open('data/linea.json')); T = json.load(open('tools/linea_t5.json'))
L['civs'] = [c for c in L['civs'] if c['id'] not in ('chn', 'jap', 'ind')] + T['civs']
for e in T['eras']:
    e['tema'] = 5
    # el Imperio mogol (1526-1858) y el dominio británico (1757-1947) se solapan: la barra mogola se corta donde empieza la británica
    # y conserva sus fechas reales en el rótulo
    if e['civ'] == 'ind' and e['from'] == 1526 and e['to'] == 1858: e['to'] = 1757
L['eras'] = [e for e in L['eras'] if e.get('tema') != 5] + T['eras']
for x in T['hitos']:
    x['tema'] = 5; x['s'] = fuente(x['sl']) if x.get('sl') in sl else ''
L['hitos'] = [x for x in L['hitos'] if x.get('tema') != 5] + T['hitos']
json.dump(L, open('data/linea.json', 'w'), ensure_ascii=False, indent=1)
for x in T['hitos']: print(x['id'], x.get('sl'), '|', x['s'])
t = json.load(open('data/temas.json'))
for e in t['temas']:
    if e['num'] == 5: e.update({'available': True})
t['version'] = '2026-11-19'
json.dump(t, open('data/temas.json', 'w'), ensure_ascii=False, indent=2)
print('ok')
