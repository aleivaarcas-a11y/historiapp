#!/usr/bin/env python3
"""Tema 3: vuelca en data/tema03.json los modos de estudio, vídeos y mapa (07-10-2026). Ejecutar tras t3_postfichas.py."""
import json,os
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
d=json.load(open('data/tema03.json'))
m=json.load(open('tools/t3_modos.json'))
for k,v in m.items(): d[k]=v
d['videos']=json.load(open('tools/videos_t3.json'))
CU=json.load(open('tools/t3_cuadros.json'))
for f in d['fichas']:
    if f['id'] in CU and not f['body']['es']: f['body']=CU[f['id']]
mapa=json.load(open('tools/fuentes/_t3_en/mapa3.json')); x=json.load(open('tools/mapa_x_tema03.json'))
for r in mapa['ramas']:
    for i,n in enumerate(r['nodos']):
        if f"{r['code']}.{i}" in x: n['x']=x[f"{r['code']}.{i}"]
M=json.load(open('tools/mapas.json')); M['3']=mapa; json.dump(M,open('tools/mapas.json','w'),ensure_ascii=False,indent=1)
d['mapa']=mapa
ids={f['id'] for f in d['fichas']}; secs={s['code'] for s in d['sections']}
bad=[]
for r in mapa['ramas']:
    for n in r['nodos']:
        for f in [n['f']]+n.get('fs',[]):
            if f not in ids: bad.append(f)
for k in ['cards','glossary','sources','myths','quiz','match','timeline','videos']:
    for it in d[k]:
        if it.get('sec') and it['sec'] not in secs: bad.append((k,it['sec']))
for c in d['cards']:
    if not os.path.exists(c['img']): bad.append(c['img'])
for v in d['videos']:
    for L in 'es','en':
        if not os.path.exists(v['src'][L].split('?')[0]) or not os.path.exists(v['poster'][L].split('?')[0]): bad.append(v['id'])
for f in d['fichas']:
    for im in f['images']:
        if not os.path.exists(im['src']): bad.append(im['src'])
print('errores:',bad); print('fichas sin EN:',[f['code'] for f in d['fichas'] if not f['body']['en']])
json.dump(d,open('data/tema03.json','w'),ensure_ascii=False,indent=1)
print({k:len(d[k]) for k in ['fichas','cards','glossary','timeline','sources','match','myths','quiz','videos']})
