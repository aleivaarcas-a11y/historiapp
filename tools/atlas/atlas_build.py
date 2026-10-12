#!/usr/bin/env python3
# Historiapp · Atlas. Construye data/atlas.json y data/atlas_mapa.json a partir de tools/atlas/.
# Uso (desde la carpeta Historiapp):  python3 tools/atlas/atlas_build.py
# Para añadir un tema: crear tools/atlas/atlas_tN.json con el mismo formato que los demás y volver a ejecutar.
# El Atlas solo muestra los temas que figuran como disponibles en data/temas.json, de modo que se puede
# preparar el archivo de un tema antes de abrirlo en la app.
import json, math, os, glob, datetime, re

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(BASE, '..', '..'))
mapa = json.load(open(os.path.join(BASE, 'mapa_base.json'), encoding='utf8'))

# ---------- proyección cónica conforme de Lambert (la misma de Agón) ----------
P = mapa['proj']; a = 6378137.0; f = 1/298.257223563; e = math.sqrt(2*f-f*f); R = math.radians
def _m(p): return math.cos(p)/math.sqrt(1-e*e*math.sin(p)**2)
def _t(p): return math.tan(math.pi/4-p/2)/((1-e*math.sin(p))/(1+e*math.sin(p)))**(e/2)
p1, p2, p0, l0 = R(P['lat1']), R(P['lat2']), R(P['lat0']), R(P['lon0'])
n = (math.log(_m(p1))-math.log(_m(p2)))/(math.log(_t(p1))-math.log(_t(p2))); F = _m(p1)/(n*_t(p1)**n); r0 = a*F*_t(p0)**n
S = P['W']/(P['x1']-P['x0'])
def px(lat, lon):
    r = a*F*_t(R(lat))**n; th = n*(R(lon)-l0)
    x, y = r*math.sin(th), r0-r*math.cos(th)
    return [round((x-P['x0'])*S, 1), round((P['y1']-y)*S, 1)]

# ---------- provincias: punto en polígono (par-impar) ----------
def rings(d):
    out = []
    for sub in re.findall(r'M[^M]+', d):
        v = list(map(float, re.findall(r'-?\d+\.?\d*', sub))); out.append(list(zip(v[0::2], v[1::2])))
    return out
PROV = [(p['id'], rings(p['d'])) for p in mapa['prov']]
def inside(pt, rs):
    x, y = pt; c = False
    for r in rs:
        for i in range(len(r)):
            (x1, y1), (x2, y2) = r[i], r[i-1]
            if (y1 > y) != (y2 > y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c = not c
    return c
def prov_of(pt):
    for pid, rs in PROV:
        if inside(pt, rs): return pid
    for r_ in (3,6,10,14):
      for dx, dy in ((r_,0),(-r_,0),(0,r_),(0,-r_),(r_,r_),(-r_,-r_),(r_,-r_),(-r_,r_)):
        for pid, rs in PROV:
            if inside((pt[0]+dx, pt[1]+dy), rs): return pid
    return None

# ---------- civilizaciones (color y forma, como en Agón) ----------
CIVS = {
 'pre': {'es':'Prehistoria','en':'Prehistory','c':'#8C7A57','s':'dia'},
 'his': {'es':'Hispania','en':'Hispania','c':'#9C5A2C','s':'dia'},
 'fen': {'es':'Fenicia','en':'Phoenicia','c':'#6B3F86','s':'dia'},
 'egi': {'es':'Egipto','en':'Egypt','c':'#E1A01C','s':'tri'},
 'per': {'es':'Persia','en':'Persia','c':'#2E62AE','s':'circ'},
 'ege': {'es':'Creta y Micenas','en':'Crete and Mycenae','c':'#2C7F7A','s':'dia'},
 'gre': {'es':'Grecia','en':'Greece','c':'#3A3431','s':'hex','st':'#C8643B'},
 'etr': {'es':'Etruria','en':'Etruria','c':'#5E7B37','s':'dia'},
 'rom': {'es':'Roma','en':'Rome','c':'#B6402C','s':'sq'},
}

import unicodedata
def norm(x): return ''.join(c for c in unicodedata.normalize('NFD',(x or '').lower()) if unicodedata.category(c)!='Mn')
def LX(o,l='es'): return o.get(l) or o.get('es') or '' if isinstance(o,dict) else (o or '')
def excerpt(paras, n=280):
    t=' '.join(paras or []).strip()
    if not t: return ''
    out=''
    for sent in re.split(r'(?<=[.!?])\s+', t):
        if len(out)+len(sent)>n and out: break
        out=(out+' '+sent).strip()
    return out
LINEA=json.load(open(os.path.join(APP,'data','linea.json'),encoding='utf8')) if os.path.exists(os.path.join(APP,'data','linea.json')) else {'hitos':[]}
def load_tema(num):
    p = os.path.join(APP, 'data', f'tema{num:02d}.json')
    return json.load(open(p, encoding='utf8')) if os.path.exists(p) else None

lugares, acont, avisos = [], [], []
for fn in sorted(glob.glob(os.path.join(BASE, 'atlas_t*.json')), key=lambda s: int(re.findall(r'\d+', os.path.basename(s))[0])):
    T = json.load(open(fn, encoding='utf8')); num = T['tema']
    for c in T.get('civs', []): CIVS[c['id']] = {k: v for k, v in c.items() if k != 'id'}
    td = load_tema(num)
    FI = {f['id']: f for f in td['fichas']} if td else {}
    VI = {v['id']: v for v in td.get('videos', [])} if td else {}
    for L in T['lugares']:
        if L['civ'] not in CIVS: avisos.append(f"t{num} {L['id']}: civilización desconocida {L['civ']}")
        xy = px(L['lat'], L['lon'])
        fichas, imgs, vids = [], [], []
        for fid in L.get('fichas', []):
            f = FI.get(fid)
            if f: fichas.append({'id': fid, 't': f['title'], 'code': f.get('code', '')})
            elif td: avisos.append(f"t{num} {L['id']}: no existe la ficha {fid}")
        for src in L.get('imgs', []):
            cap = {}; fid = None
            for f in FI.values():
                for im in f.get('images', []):
                    if im['src'] == src: cap = im.get('caption') or {}; fid = f['id']
            if td and fid is None: avisos.append(f"t{num} {L['id']}: imagen sin ficha {src}")
            if not cap and fid: cap = FI[fid]['title']
            imgs.append({'src': src, 'cap': cap})
        for vid in L.get('vids', []):
            v = VI.get(vid)
            if v: vids.append({'id': vid, 't': v['title'], 'src': v['src'], 'poster': v['poster']})
            elif td: avisos.append(f"t{num} {L['id']}: no existe el vídeo {vid}")
        o = {k: L[k] for k in ('id','civ','name','place','date','year','text','src','ref')}
        kw=[norm(k) for k in L.get('kw',[])]
        kre=[re.compile(r'(?<![a-z0-9])'+re.escape(k)) for k in kw]
        hit=lambda txt: any(r.search(norm(txt)) for r in kre)
        fobjs=[FI[f['id']] for f in fichas]
        secs=[]
        for fo in fobjs:
            if fo['sec'] not in secs: secs.append(fo['sec'])
        SEC={x['code']:x['title'] for x in (td or {}).get('sections',[])}
        o['secs']=[{'code':c,'t':SEC.get(c,{'es':c,'en':c})} for c in secs]
        # fichas con extracto e imagen
        for f,fo in zip(fichas,fobjs):
            f['sec']=fo['sec']; f['ex']={'es':excerpt(fo['body'].get('es')),'en':excerpt(fo['body'].get('en'))}
            f['img']=(fo.get('images') or [{}])[0].get('src')
        # nodos del mapa conceptual del tema
        nodos=[]
        for r in (td or {}).get('mapa',{}).get('ramas',[]):
            for nd in r.get('nodos',[]):
                fs=set(nd.get('fs') or [])|({nd['f']} if nd.get('f') else set())
                if fs & {f['id'] for f in fichas}: nodos.append({'t':nd['t'],'d':nd['d'],'sec':nd.get('sec',r['code'])})
        # hitos de la línea del tiempo (por diapositiva de las fichas o por palabra clave)
        sl=set(); [sl.update(fo.get('slides') or []) for fo in fobjs]
        hitos=[]
        for h in LINEA['hitos']:
            if h['tema']!=num: continue
            if hit(h['es']['t']+' '+h['es']['x']):
                hitos.append({'y':h['y'],'d':{'es':h['es']['d'],'en':h['en']['d']},'t':{'es':h['es']['t'],'en':h['en']['t']},'x':{'es':h['es']['x'],'en':h['en']['x']},'s':h.get('s','')})
        hitos.sort(key=lambda h:h['y'])
        # glosario: términos que aparecen en las fichas del lugar
        ftext=norm(LX(L['text'])+' '+' '.join(LX(f['t'])+' '+f['ex']['es'] for f in fichas))
        glos=[]
        for g in (td or {}).get('glossary',[]):
            term=norm(re.split(r'[(,]',g['term']['es'])[0]).strip()
            if term and (re.search(r'(?<![a-z0-9])'+re.escape(term)+r'(?![a-z0-9])',ftext) or hit(LX(g['term'])+' '+g['def']['es'])): glos.append({'term':g['term'],'def':g['def'],'sec':g.get('sec','')})
        # preguntas: las del lugar y las de los modos de estudio del tema que hablan de él
        preg=[{'k':'mc','q':q['q'],'o':q['o'],'a':0} for q in L['qs']]
        for q in (td or {}).get('quiz',[]):
            if hit(LX(q['q'])+' '+LX(q.get('explain',{}))+' '+' '.join(LX(o) for o in q['options'])):
                preg.append({'k':'mc','q':q['q'],'o':{'es':[LX(o) for o in q['options']],'en':[LX(o,'en') for o in q['options']]},'a':q['answer'],'ex':q.get('explain'),'sec':q.get('sec')})
        for m in (td or {}).get('myths',[]):
            if hit(LX(m['claim'])+' '+LX(m['explain'])): preg.append({'k':'vf','q':m['claim'],'a':bool(m['answer']),'ex':m['explain'],'sec':m.get('sec')})
        for c in (td or {}).get('cards',[]):
            if hit(LX(c['claim'])+' '+LX(c.get('caption',{}))+' '+LX(c.get('explain',{}))): preg.append({'k':'vf','q':c['claim'],'a':bool(c['answer']),'ex':c.get('explain'),'img':c.get('img'),'cap':c.get('caption'),'sec':c.get('sec')})
        o.update({'tema': num, 'xy': xy, 'prov': L.get('prov') or prov_of(xy), 'fichas': fichas, 'vids': vids,
                  'nodos': nodos[:3], 'hitos': hitos[:5], 'glos': glos[:6], 'preg': preg[:10]})
        lugares.append(o)
    for A in T.get('acontecimientos', []):
        acont.append({**A, 'tema': num})

ids = [l['id'] for l in lugares]
for i in set(ids):
    if ids.count(i) > 1: avisos.append(f'lugar repetido: {i}')
for A in acont:
    if A.get('lugar') and A['lugar'] not in ids: avisos.append(f"acontecimiento {A['year']}: lugar desconocido {A['lugar']}")

out = {'v': datetime.date.today().isoformat(), 'civs': CIVS, 'lugares': sorted(lugares, key=lambda l: l['year']), 'acontecimientos': sorted(acont, key=lambda a: a['year'])}
json.dump(out, open(os.path.join(APP, 'data', 'atlas.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
mp = {k: v for k, v in mapa.items() if k != 'proj'}
json.dump(mp, open(os.path.join(APP, 'data', 'atlas_mapa.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
por = {}
for l in lugares: por[l['tema']] = por.get(l['tema'], 0)+1
tot=lambda k: sum(len(l[k]) for l in lugares)
print(f"Enlaces: {tot('fichas')} fichas, {tot('nodos')} ideas del mapa, {tot('hitos')} hitos de la línea, {tot('glos')} términos, {tot('preg')} preguntas, {tot('vids')} vídeos.")
print('Atlas: ' + ', '.join(f'Tema {k}: {v} lugares' for k, v in sorted(por.items())) + f'; {len(acont)} acontecimientos.')
print('Avisos:' if avisos else 'Sin avisos.')
for a_ in avisos: print('  -', a_)
