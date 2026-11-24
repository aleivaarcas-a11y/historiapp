#!/usr/bin/env python3
"""Tema 5 en Historiapp (24-11-2026): referencias inglesas (refs_en) y versiones inglesas de los gráficos con texto (diapositivas 3, 5, 27, 50, 52 y 63).
Copia los PNG ingleses del Topic 5 a img/t5/sNN_1_en.jpg con el mismo ancho que la versión castellana y, en data/tema05.json,
marca la imagen castellana con "lang": "es" y añade detrás la inglesa con "lang": "en" (como en el Tema 4).
Se ejecuta después de tools/t5_fichas.py. Uso: python3 tools/t5_imagenes_en.py"""
import json, os
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
G = os.path.expanduser('~/mnt/ASIGNATURAS/HISTORIA DEL DEPORTE/Claude outputs/TEMA 5 - China, Japon, India/Topic 5 EN (24-11)/graficos_en/')
if not os.path.isdir(G):
    G = '/Users/leiva/Mi unidad /UCAM/ASIGNATURAS/HISTORIA DEL DEPORTE/Claude outputs/TEMA 5 - China, Japon, India/Topic 5 EN (24-11)/graficos_en/'
M = {'s03_1': 'china_india_japan_time_en.png', 's05_1': 'chinese_dynasties_en.png', 's27_1': 'periods_japan_en.png',
     's50_1': 'periods_india_en.png', 's52_1': 'castes_purusha_en.png', 's63_1': 'how_kabaddi_is_played_en.png'}
for k, f in M.items():
    w = Image.open(f'img/t5/{k}.jpg').size[0]
    im = Image.open(G + f).convert('RGB')
    im = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)
    im.save(f'img/t5/{k}_en.jpg', quality=85, optimize=True)
d = json.load(open('data/tema05.json'))
n = 0
for fi in d['fichas']:
    out = []
    for im in fi['images']:
        out.append(im)
        k = im['src'].split('/')[-1].split('.')[0]
        if k in M and 'lang' not in im:
            im['lang'] = 'es'
            out.append({'src': f'img/t5/{k}_en.jpg', 'caption': im.get('caption', {}), 'lang': 'en'}); n += 1
    fi['images'] = out
# referencias en inglés (refs_en), sacadas de las mismas diapositivas del Topic 5
import re, sys
sys.path.insert(0, 'tools'); import construir_fichas as CF
EN = {x['slide']: x for x in json.load(open('tools/fuentes/t5_slides_en.json'))}
def is_ref(p):
    return (CF.is_ref(p) or '(n.d.)' in p or re.search(r'\(\d{4}\)\. [A-Z]', p) is not None) and not p.startswith("Author's elaboration")
for fi in d['fichas']:
    r = []
    for sl in fi['slides']:
        for p in EN[sl]['paras']:
            if is_ref(p) and p not in r: r.append(p)
    fi['refs_en'] = r
json.dump(d, open('data/tema05.json', 'w'), ensure_ascii=False, indent=1)
print('imágenes inglesas añadidas', n)
