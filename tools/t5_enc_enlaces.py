#!/usr/bin/env python3
"""Tema 5 (19-11-2026): enlaza las fichas de la Enciclopedia con las del tema (campo tema en la última tanda de cada deporte) y ejecuta enc_merge.py."""
import json,glob,os,subprocess,sys
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
F={f['id']:f['title'] for f in json.load(open('data/tema05.json'))['fichas']}
LINKS={'polo':['jiju'],'tiro-con-arco':['entrenamiento-samurai-arco','toshiya'],'kyudo':['entrenamiento-samurai-arco','toshiya'],
 'yabusame':['entrenamiento-samurai-arco'],'tiro-con-arco-a-caballo':['entrenamiento-samurai-arco'],'kendo':['entrenamiento-samurai-combate'],
 'naginata':['armamento-de-los-samurais','la-mujer-japonesa'],'judo':['judo'],'karate':['karate'],'sumo':['sumo'],'jiu-jitsu':['jujutsu'],
 'kung-fu-wushu':['bodhidharma-y-shaolin','deportes-de-combate'],'tai-chi-chuan':['deporte-tradicional-chino'],'kabaddi':['deportes-de-equipo'],
 'kalaripayattu':['kalarippayattu'],'kushti':['lucha-kushti'],'mallakhamb':['metodos-de-entrenamiento-de-fuerza'],'yoga':['yoga'],
 'cuju':['cuju','cuju-sus-modalidades'],'kemari':['kemari'],'ajedrez':['chaturanga'],'golf':['chuiwan-un-juego-de-palo-y-bola'],'futbol':['cuju']}
last={}
for f in sorted(glob.glob('tools/enc_tandas/tanda_*.json')):
    for e in json.load(open(f)):
        if e.get('id') in LINKS: last[e['id']]=f
for i,fs in LINKS.items():
    if i not in last: print('sin ficha en la Enciclopedia:', i); continue
    assert all(x in F for x in fs), (i, fs)
    f=last[i]; d=json.load(open(f))
    for e in d:
        if e.get('id')==i:
            t=[x for x in (e.get('tema') or []) if x.get('num')!=5]
            t+= [{"num":5,"f":fid,"t":F[fid]} for fid in fs]
            e['tema']=t
    json.dump(d,open(f,'w'),ensure_ascii=False,indent=1); print(i,'->',f)
subprocess.run([sys.executable,'tools/enc_merge.py'],check=True)
