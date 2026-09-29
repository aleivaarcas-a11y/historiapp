#!/usr/bin/env python3
"""Une las tandas de tools/enc_tandas/ en data/enciclopedia.json, con comprobaciones de estilo y de campos.
Las fichas de HOLD se quedan fuera hasta rehacer sus fuentes. Uso: python3 tools/enc_merge.py"""
import json,glob,os,re
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
HOLD=set(json.load(open(os.path.join(R,'tools/enc_tandas/HOLD.json')))) if os.path.exists(os.path.join(R,'tools/enc_tandas/HOLD.json')) else set()
D=json.load(open(os.path.join(R,'data/enciclopedia.json')))
lista=json.load(open(os.path.join(R,'tools/enciclopedia_lista.json'))); L={x['id']:x for x in lista}
cur={e['id']:e for e in D['entries']}
KEYS={'id','name','bloque','tipo','cuando','body','tema','img','refs','refs_en'}
prob=[]
for f in sorted(glob.glob(os.path.join(R,'tools/enc_tandas/tanda_*.json'))):
  for e in json.load(open(f)):
    i=e.get('id')
    if i not in L: prob.append(f'{i}: id desconocido'); continue
    if i in HOLD: continue
    miss=KEYS-set(e); 
    if miss: prob.append(f'{i}: faltan {miss}'); continue
    txt=' '.join(e['body']['es']+e['body']['en']+[e['cuando']['es'],e['cuando']['en']])
    if '—' in txt or '–' in txt: prob.append(f'{i}: guion largo')
    if re.search(r'\bsino\b',' '.join(e['body']['es'])): prob.append(f'{i}: sino')
    im=e.get('img') or {}
    if im.get('src') and not os.path.exists(os.path.join(R,im['src'])): prob.append(f'{i}: falta imagen {im["src"]}')
    e['name']={'es':L[i]['es'],'en':L[i]['en']}; e['bloque']=L[i]['bloque']; e['tipo']=L[i]['tipo']
    cur[i]=e
D['entries']=list(cur.values()); D['total']=len(lista)
json.dump(D,open(os.path.join(R,'data/enciclopedia.json'),'w'),ensure_ascii=False,indent=1)
for x in lista: x['estado']='lista' if x['id'] in cur else ('revisar' if x['id'] in HOLD else 'pendiente')
json.dump(lista,open(os.path.join(R,'tools/enciclopedia_lista.json'),'w'),ensure_ascii=False,indent=1)
print('publicadas',len(cur),'| en revisión',len(HOLD),'| pendientes',sum(x['estado']=='pendiente' for x in lista))
print('\n'.join(prob) or 'sin problemas')
