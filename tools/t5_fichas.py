#!/usr/bin/env python3
"""Tema 5 (China, Japón, India) en Historiapp, 19-11-2026: fichas ES/EN desde el texto de pantalla.
Cuerpo en castellano: texto de las diapositivas de «TEMAS NUEVOS/TEMA 5. China, Japón, India.pptx» (tools/fuentes/t5_slides.json).
Cuerpo en inglés: traducción de ese mismo texto (tools/fuentes/t5_slides_en.json), porque todavía no hay Topic 5 en inglés.
No se usan las notas del orador. Apartados según tools/secciones_t5.json; imágenes en img/t5 (tools/t5_imgsel.json).
Uso: python3 tools/t5_fichas.py"""
import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
import construir_fichas as CF

ES = {x['slide']: x for x in json.load(open('tools/fuentes/t5_slides.json'))}
EN = {x['slide']: x for x in json.load(open('tools/fuentes/t5_slides_en.json'))}
SECS = json.load(open('tools/secciones_t5.json'))
SEL = json.load(open('tools/t5_imgsel.json'))
se = json.load(open('tools/secciones_en.json')); se.update({s['code']: s['title']['en'] for s in SECS})
json.dump(se, open('tools/secciones_en.json', 'w'), ensure_ascii=False, indent=1)
im = json.load(open('tools/imgmap.json')); im['t5'] = {k: v['img'] for k, v in SEL.items()}
json.dump(im, open('tools/imgmap.json', 'w'), ensure_ascii=False, indent=1)

DIV = {4, 10, 16, 26, 32, 34, 41, 44, 49, 55, 57, 61}      # portadillas de apartado (título y foto de fondo)
NEXT = {5, 11, 27, 50}                                      # diapositivas sin título que van con la ficha siguiente
SKIP = {1, 2, 66, 67, 68}                                   # portada, índice, referencias y cierre
CIV = {'5.1': 'china', '5.2': 'japon', '5.3': 'india'}
CAP = re.compile(r'\s·\s')

def is_ref(p):
    return CF.is_ref(p) or '(s. f.)' in p or '(Obra original' in p or p.startswith('Elaboración propia')
def sec_of(n):
    best = ''
    for s in SECS:
        a, b = s['slides']
        if a <= n <= b and len(s['code']) >= len(best): best = s['code']
    return best or '5.1'
def limpio(paras, title):
    out = []
    for p in paras:
        p = p.strip()
        if len(p) < 4 or is_ref(p) or p.isdigit() or p.lower() == (title or '').lower() or p == 'VIDEO': continue
        if CAP.search(p) and len(p) < 260: continue                      # pie de imagen o rótulo con «·»
        if len(p) < 70 and not p.endswith(('.', ':', '?')): continue      # lugar y fecha, rótulos de gráfico
        if len(p) < 75 and re.search(r'(a|d)\.\s?C\.$', p): continue
        out.append(p)
    return out
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:40].strip('-')
def clean(t): return re.sub(r'\s*\((II|III|IV)\)\s*$', '', t or '').strip().rstrip(':.')

fichas, pend = [], []
for n in sorted(ES):
    if n in SKIP or n in DIV: continue
    e, en = ES[n], EN[n]
    title = (e['title'] or '').strip()
    imgs = [{'src': f"img/t5/{v['img']}.jpg", 'caption': v.get('cap', {})} for k, v in SEL.items() if int(k[1:3]) == n]
    body_es, body_en = limpio(e['paras'], title), limpio(en['paras'], en['title'])
    refs = [p for p in e['paras'] if is_ref(p) and not p.startswith('Elaboración propia')]
    if not title:
        if n in NEXT: pend.append((n, imgs, refs)); continue
        if fichas:
            f = fichas[-1]; f['slides'].append(n); f['images'] += imgs; f['refs'] += refs
            f['body']['es'] += body_es; f['body']['en'] += body_en
        continue
    t0 = clean(title)
    if fichas and (title != t0 or t0 == fichas[-1]['title']['es'] or (t0 == 'Cuju' and fichas[-1]['title']['es'].startswith('Cuju'))):
        f = fichas[-1]; f['slides'].append(n); f['images'] += imgs; f['refs'] += refs
        f['body']['es'] += body_es; f['body']['en'] += body_en
        continue
    sec = sec_of(n)
    f = {'id': slug(t0), 'sec': sec, 'title': {'es': t0, 'en': clean(en['title'])}, 'slides': [n], 'images': imgs,
         'source': 'diapositiva', 'essay': {'es': [], 'en': []}, 'body': {'es': body_es, 'en': body_en}, 'slide': {'es': [], 'en': []}, 'refs': refs}
    for pn, pim, pref in pend:
        f['slides'].insert(0, pn); f['images'] = pim + f['images']; f['refs'] = pref + f['refs']
    pend = []
    fichas.append(f)

# cuerpos especiales: frases partidas en la diapositiva (9) y cuadro de tres columnas (17)
def P(n, i, L): return (ES if L == 'es' else EN)[n]['paras'][i]
for f in fichas:
    if 9 in f['slides']:
        f['body'] = {'es': ['La cultura física china tuvo dos caras que a menudo se complementaban: una buscaba la salud, la longevidad y la armonía del espíritu, y la otra era la competición, ligada sobre todo a la guerra, a la corte y a la fiesta.'] + [P(9, i, 'es') for i in (4, 5, 6)],
                     'en': ['Chinese physical culture had two faces that often complemented each other: one sought health, longevity and harmony of spirit, and the other was competition, linked above all to war, the court and festivals.'] + [P(9, i, 'en') for i in (4, 5, 6)]}
    if 17 in f['slides']:
        f['body'] = {'es': ['Antigüedad. El cuerpo elegía al noble. ' + P(17, 7, 'es'), 'Desde el siglo VII d. C. El cuerpo sale del examen civil. ' + P(17, 8, 'es'), 'Desde 702 d. C. El cuerpo, examen del soldado. ' + P(17, 9, 'es'), P(17, 10, 'es')],
                     'en': ['Antiquity. The body chose the noble. ' + P(17, 7, 'en'), 'From the 7th century AD. The body leaves the civil examination. ' + P(17, 8, 'en'), 'From AD 702. The body, the soldier\'s examination. ' + P(17, 9, 'en'), P(17, 10, 'en')]}
for f in fichas:
    if f['slides'] == [3]:
        f['body'] = {'es': ['Periodos de China, Japón y la India, del III milenio a. C. al siglo XX d. C.'], 'en': ['Periods of China, Japan and India, from the third millennium BC to the 20th century AD.']}
# identificadores únicos y códigos
seen = {}
for f in fichas:
    b = f['id']
    if b in seen or b in ('introduccion-historica',): f['id'] = b + '-' + CIV[f['sec'][:3]]
    seen[f['id']] = 1
    u = []
    for x in f['refs']:
        if x not in u: u.append(x)
    f['refs'] = u
for k, f in enumerate(fichas, 1): f['code'] = f"H5·{k:02d}"
d = json.load(open('data/tema05.json')) if os.path.exists('data/tema05.json') else {}
d.update({'id': 't5', 'num': 5, 'title': {'es': 'China, Japón e India', 'en': 'China, Japan and India'},
          'unit': {'es': 'Unidad Didáctica III. El deporte en las civilizaciones orientales y de la América Precolombina', 'en': 'Teaching Unit III. Sport in the Eastern civilisations and Pre-Columbian America'}})
d['sections'] = [{'code': s['code'], 'title': s['title'], 'intro': {'es': [], 'en': []}, 'refs': []} for s in SECS]
d['fichas'] = fichas
json.dump(d, open('data/tema05.json', 'w'), ensure_ascii=False, indent=1)
for f in fichas:
    print(f['code'], f['id'], f['sec'], f['slides'], '|', f['title']['en'][:34], len(f['images']), len(f['body']['es']), len(f['body']['en']))
