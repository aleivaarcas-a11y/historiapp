#!/usr/bin/env python3
"""Tema 4 en Historiapp (25-10-2026): portada del tema, colores de la línea del tiempo (Etruria y Roma),
eras e hitos del Tema 4 en data/linea.json y tema disponible en data/temas.json. Copia previa: tools/index_antes_t4.html"""
import os, json, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
import construir_fichas as CF
if not os.path.exists('tools/index_antes_t4.html'): shutil.copy('index.html', 'tools/index_antes_t4.html')
h = open('index.html', encoding='utf-8').read()
if '4:"img/t4/' not in h:
    h = h.replace('3:"img/t3/fresco_salto_toro.jpg"};', '3:"img/t3/fresco_salto_toro.jpg",4:"img/t4/mosaico_aurigas_merida.jpg"};', 1)
assert '4:"img/t4/mosaico_aurigas_merida.jpg"' in h
if '--ln-etr' not in h:
    h = h.replace('--ln-gre2:#8FCBC6;', '--ln-gre2:#8FCBC6;--ln-etr:#B5651D;--ln-etr2:#EDC39B;--ln-rom:#7A1F3D;--ln-rom2:#D9A3B5;', 1)
    h = h.replace('html.dark{--ln-ege:#9A6FC4;', 'html.dark{--ln-etr:#D08A47;--ln-etr2:#6B3E17;--ln-rom:#C2557A;--ln-rom2:#5A2235;--ln-ege:#9A6FC4;', 1)
    h = h.replace('.ln-sw.c-gre{background:var(--ln-gre)}', '.ln-sw.c-gre{background:var(--ln-gre)}.ln-era.c-etr{background:var(--ln-etr)}.ln-era.c-etr.alt{background:var(--ln-etr2);color:#1d252d}.ln-sw.c-etr{background:var(--ln-etr)}.ln-era.c-rom{background:var(--ln-rom)}.ln-era.c-rom.alt{background:var(--ln-rom2);color:#1d252d}.ln-sw.c-rom{background:var(--ln-rom)}', 1)
    assert h.count('--ln-etr') >= 4 and 'c-rom.alt' in h
open('index.html', 'w', encoding='utf-8').write(h)
# línea del tiempo: la fuente de cada hito sale de la Fuente de su diapositiva
sl = {s['slide']: s for s in json.load(open('tools/fuentes/t4_slides.json'))}
def fuente(n):
    out = []
    for p in sl[n]['paras']:
        if CF.is_ref(p):
            m = re.match(r"^(.+?)\s*\((\d{4}[a-z]?|s\. f\.)\)", p)
            if m:
                au = m.group(1).strip().rstrip(',')
                parts = [x.strip() for x in re.split(r",\s*(?:y\s+)?|\s+y\s+", au) if x.strip()]
                surn = [x for x in parts if not re.fullmatch(r"(?:[A-ZÁÉÍÓÚ]\.[\s-]*)+(?:[A-ZÁÉÍÓÚ]\.)?", x) and x != 'et al.']
                if len(surn) > 2: a = surn[0] + ' et al.'
                elif len(surn) == 2: a = surn[0] + ' y ' + surn[1]
                else: a = surn[0] if surn else au
                out.append(f"{a} ({m.group(2)})")
    return '; '.join(dict.fromkeys(out))
L = json.load(open('data/linea.json')); T = json.load(open('tools/linea_t4.json'))
L['civs'] = [c for c in L['civs'] if c['id'] not in ('etr', 'rom')] + T['civs']
for e in T['eras']: e['tema'] = 4
L['eras'] = [e for e in L['eras'] if e.get('tema') != 4] + T['eras']
for x in T['hitos']:
    x['tema'] = 4; x['s'] = fuente(x['sl'])
L['hitos'] = [x for x in L['hitos'] if x.get('tema') != 4] + T['hitos']
json.dump(L, open('data/linea.json', 'w'), ensure_ascii=False, indent=1)
for x in T['hitos']: print(x['id'], '|', x['s'])
# tema disponible
t = json.load(open('data/temas.json'))
for e in t['temas']:
    if e['num'] == 4: e.update({'available': True, 'title': {'es': 'Etruria y Roma', 'en': 'Etruria and Rome'}})
t['version'] = '2026-10-25'
json.dump(t, open('data/temas.json', 'w'), ensure_ascii=False, indent=2)
print('ok')
