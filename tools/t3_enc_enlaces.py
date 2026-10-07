#!/usr/bin/env python3
"""Tema 3: enlaza las fichas de la Enciclopedia con las del tema (campo tema en la última tanda de cada deporte) y ejecuta enc_merge.py."""
import json,glob,os,subprocess,sys
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
F={f['id']:f['title'] for f in json.load(open('data/tema03.json'))['fichas']}
LINKS={'salto-del-toro':['salto-del-toro','que-significaba-el-salto-del-toro'],'boxeo':['pugilato','el-pugilato'],
 'lucha-grecorromana':['la-lucha'],'lucha-libre-olimpica':['la-lucha'],'pancracio':['el-pancracio'],
 'atletismo':['la-carrera-del-estadio','el-pentatlon'],'pentatlon-moderno':['el-pentatlon'],
 'hipica':['la-hipica'],'carreras-de-carros':['carros-y-caballos','los-juegos-funebres-de-patroclo'],'carreras-de-caballos':['carros-y-caballos']}
last={}
for f in sorted(glob.glob('tools/enc_tandas/tanda_*.json')):
    for e in json.load(open(f)):
        if e.get('id') in LINKS: last[e['id']]=f
for i,fs in LINKS.items():
    f=last[i]; d=json.load(open(f))
    for e in d:
        if e.get('id')==i:
            t=[x for x in (e.get('tema') or []) if x.get('num')!=3]
            t+= [{"num":3,"f":fid,"t":F[fid]} for fid in fs]
            e['tema']=t
    json.dump(d,open(f,'w'),ensure_ascii=False,indent=1); print(i,'->',f)
subprocess.run([sys.executable,'tools/enc_merge.py'],check=True)
