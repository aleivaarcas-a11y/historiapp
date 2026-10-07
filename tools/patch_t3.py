#!/usr/bin/env python3
"""Tema 3 en Historiapp (07-10-2026): portada del tema, colores de la línea del tiempo (Creta y Micenas, Grecia),
hitos y eras del Tema 3 en data/linea.json y tema disponible en data/temas.json. Copia previa: tools/index_antes_t3.html"""
import os,json,re,shutil,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
import construir_fichas as CF
if not os.path.exists('tools/index_antes_t3.html'): shutil.copy('index.html','tools/index_antes_t3.html')
h=open('index.html',encoding='utf-8').read()
h=h.replace('2:"img/t2/hatshepsut_hebsed.jpg"};','2:"img/t2/hatshepsut_hebsed.jpg",3:"img/t3/fresco_salto_toro.jpg"};',1)
assert '3:"img/t3/fresco_salto_toro.jpg"' in h
if '--ln-ege' not in h:
    h=h.replace('--ln-fen2:#A9B4BF;','--ln-fen2:#A9B4BF;--ln-ege:#6A3D9A;--ln-ege2:#C3A6DA;--ln-gre:#1B7F79;--ln-gre2:#8FCBC6;',1)
    h=h.replace('html.dark{--ln-per:#3d7cc0;','html.dark{--ln-ege:#9A6FC4;--ln-ege2:#4A2E66;--ln-gre:#3BA79F;--ln-gre2:#1F5552;--ln-per:#3d7cc0;',1)
    h=h.replace('.ln-sw.c-fen{background:var(--ln-fen)}','.ln-sw.c-fen{background:var(--ln-fen)}.ln-era.c-ege{background:var(--ln-ege)}.ln-era.c-ege.alt{background:var(--ln-ege2);color:#1d252d}.ln-sw.c-ege{background:var(--ln-ege)}.ln-era.c-gre{background:var(--ln-gre)}.ln-era.c-gre.alt{background:var(--ln-gre2);color:#1d252d}.ln-sw.c-gre{background:var(--ln-gre)}',1)
    assert h.count('--ln-ege')>=4 and 'c-gre.alt' in h
# podcast sin filtro de idioma: el episodio solo en castellano se muestra en inglés con el aviso pEsOnly
old='return a.map((it,i)=>i).filter(i=>(!a[i].lang||a[i].lang===S.lang) && (!sec || secMatch(a[i].sec,sec))); }'
new='return a.map((it,i)=>i).filter(i=>(mode==="podcast"||!a[i].lang||a[i].lang===S.lang) && (!sec || secMatch(a[i].sec,sec))); }'
if old in h: h=h.replace(old,new,1)
assert new in h
open('index.html','w',encoding='utf-8').write(h)
# línea del tiempo
sl={s['slide']:s for s in json.load(open('tools/fuentes/t3_slides.json'))}
def fuente(n):
    out=[]
    for p in sl[n]['paras']:
        if CF.is_ref(p):
            m=re.match(r"^(.+?)\s*\((\d{4}[a-z]?|s\. f\.)\)",p)
            if m:
                au=m.group(1).strip().rstrip(',')
                parts=[x.strip() for x in re.split(r",\s*(?:y\s+)?|\s+y\s+",au) if x.strip()]
                surn=[x for x in parts if not re.fullmatch(r"(?:[A-ZÁÉÍÓÚ]\.\s*)+(?:[A-ZÁÉÍÓÚ]\.)?",x) and x!='et al.']
                if len(surn)>2: a=surn[0]+' et al.'
                elif len(surn)==2: a=surn[0]+' y '+surn[1]
                else: a=surn[0] if surn else au
                out.append(f"{a} ({m.group(2)})")
    return '; '.join(dict.fromkeys(out))
L=json.load(open('data/linea.json')); T=json.load(open('tools/linea_t3.json'))
L['civs']=[c for c in L['civs'] if c['id'] not in ('ege','gre')]+T['civs']
L['eras']=[e for e in L['eras'] if e['tema']!=3]+T['eras']
for x in T['hitos']: x['s']=fuente(x['sl']).replace('Heródoto. (1989)','Heródoto (1989)').replace('Brophy y III. (1978)','Brophy (1978)').replace('Filóstrato. (1996)','Filóstrato (1996)').replace('Arrechea Rivas y F. et al. (2019)','Arrechea et al. (2019)')
L['hitos']=[x for x in L['hitos'] if x['tema']!=3]+T['hitos']
json.dump(L,open('data/linea.json','w'),ensure_ascii=False,indent=1)
for x in T['hitos']: print(x['id'],'|',x['s'])
# tema disponible
t=json.load(open('data/temas.json'))
for e in t['temas']:
    if e['num']==3: e['available']=True
t['version']='2026-10-07'
json.dump(t,open('data/temas.json','w'),ensure_ascii=False,indent=2)
print('ok')
