#!/usr/bin/env python3
"""Tema 4 (25-10-2026): enlaza las fichas de la Enciclopedia con las del tema (campo tema en la última tanda de cada deporte) y ejecuta enc_merge.py."""
import json,glob,os,subprocess,sys
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
F={f['id']:f['title'] for f in json.load(open('data/tema04.json'))['fichas']}
LINKS={'boxeo':['atletismo-lucha-y-pugilato','pugiles-luchadores-y-saltadores-etruscos'],
 'lucha-grecorromana':['atletismo-lucha-y-pugilato'],'lucha-libre-olimpica':['atletismo-lucha-y-pugilato'],
 'carreras-de-carros':['carreras-de-carros-etruscas','carreras-de-carros','circo-maximo','las-facciones-del-circo','los-aurigas-y-su-fortuna'],
 'carreras-de-caballos':['carreras-de-caballos-y-la-troia'],'hipica':['carreras-de-caballos-y-la-troia'],
 'atletismo':['atletismo-lucha-y-pugilato','el-atletismo-en-roma'],'natacion':['actividades-acuaticas'],'saltos':['actividades-acuaticas'],
 'juegos-de-pelota-romanos':['las-pelotas-romanas','trigon-y-harpastum','las-salas-de-las-termas'],'harpastum':['trigon-y-harpastum'],
 'combates-de-gladiadores':['combates-de-gladiadores','los-gladiadores-y-la-infamia','tipos-de-gladiadores','los-combates'],'caza':['venationes']}
last={}
for f in sorted(glob.glob('tools/enc_tandas/tanda_*.json')):
    for e in json.load(open(f)):
        if e.get('id') in LINKS: last[e['id']]=f
for i,fs in LINKS.items():
    assert all(x in F for x in fs), (i, fs)
    f=last[i]; d=json.load(open(f))
    for e in d:
        if e.get('id')==i:
            t=[x for x in (e.get('tema') or []) if x.get('num')!=4]
            t+= [{"num":4,"f":fid,"t":F[fid]} for fid in fs]
            e['tema']=t
    json.dump(d,open(f,'w'),ensure_ascii=False,indent=1); print(i,'->',f)
subprocess.run([sys.executable,'tools/enc_merge.py'],check=True)
