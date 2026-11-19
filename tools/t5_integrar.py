#!/usr/bin/env python3
"""Tema 5 (19-11-2026): vuelca en data/tema05.json los modos de estudio, vídeos, mapa, pódcast e introducción.
Ejecutar tras tools/t5_fichas.py. El mapa (tools/t5_mapa.json) cita las diapositivas como «sNN»; aquí se cambian por la ficha que las contiene."""
import json, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
d = json.load(open('data/tema05.json'))
m = json.load(open('tools/t5_modos.json'))
for k, v in m.items(): d[k] = v
d['videos'] = json.load(open('tools/videos_t5.json'))
mapa = json.load(open('tools/t5_mapa.json'))
SL = {n: f['id'] for f in d['fichas'] for n in f['slides']}
def fid(x):
    mm = re.fullmatch(r's(\d+)', x)
    return SL[int(mm.group(1))] if mm else x
for r in mapa['ramas']:
    for n in r['nodos']:
        n['f'] = fid(n['f'])
        if 'fs' in n: n['fs'] = list(dict.fromkeys(fid(x) for x in n['fs'] if fid(x) != n['f']))
d['mapa'] = mapa
json.dump(mapa, open('tools/t5_mapa.json', 'w'), ensure_ascii=False, indent=1)
M = json.load(open('tools/mapas.json')); M['5'] = mapa; json.dump(M, open('tools/mapas.json', 'w'), ensure_ascii=False, indent=1)
X = {f"{r['code']}.{i}": n['x'] for r in mapa['ramas'] for i, n in enumerate(r['nodos']) if 'x' in n}
json.dump(X, open('tools/mapa_x_tema05.json', 'w'), ensure_ascii=False, indent=1)
d['intro'] = {
 'es': ['El tema recorre tres civilizaciones de Asia, China, Japón y la India, desde el III milenio a. C. hasta el siglo XX d. C., y estudia cada una desde su propio orden social. En China la cultura física tuvo dos caras, la salud y la longevidad por un lado y la competición ligada a la guerra, a la corte y a la fiesta por otro; en Japón el deporte cambió con el grupo que tenía el poder, de la corte a los guerreros, la ciudad y el deporte moderno, y en la India estuvo unido a la casta y a la religión. El hilo es la pregunta de siempre en la asignatura, quién podía ejercitarse, para qué y ante quién, y cómo muchas de estas prácticas se reinventaron después como tradición nacional.'],
 'en': ['The topic covers three Asian civilisations, China, Japan and India, from the third millennium BC to the 20th century AD, and studies each from its own social order. In China physical culture had two faces, health and longevity on the one hand and competition linked to war, the court and festivals on the other; in Japan sport changed with the group that held power, from the court to the warriors, the city and modern sport, and in India it was bound up with caste and religion. The thread is the course\'s perennial question, who could exercise, what for and before whom, and how many of these practices were later reinvented as national tradition.']}
P = json.load(open('tools/podcast.json'))
P['5'] = [{'id': 't5_ep1', 'sec': '5', 'lang': 'es', 'dur': 1694, 'src': {'es': 'audio/t5_ep1.m4a?v=1', 'en': 'audio/t5_ep1.m4a?v=1'},
  'title': {'es': 'Cinco animales, flechas en el templo y luchadores en el barro', 'en': 'Five Animals, Arrows in the Temple and Wrestlers in the Mud'},
  'desc': {'es': 'Repaso del Tema 5 en forma de conversación y en el mismo orden que las clases, desde la gimnasia de salud china, Hua Tuo y Shaolin, el jiju, el chuiwan y el cuju, hasta el Japón de la corte, los samuráis, el sumo y el judo, y la India de las castas, el yoga, el kushti, el kabaddi y el chaturanga. El episodio está en castellano.',
           'en': 'A conversational review of Unit 5 that follows the order of the lectures, from Chinese health gymnastics, Hua Tuo and Shaolin, jiju, chuiwan and cuju, to the Japan of the court, the samurai, sumo and judo, and the India of castes, yoga, kushti, kabaddi and chaturanga. The episode is in Spanish.'},
  'durs': {'es': 1694, 'en': 1694}}]
json.dump(P, open('tools/podcast.json', 'w'), ensure_ascii=False, indent=1)
d['podcast'] = P['5']
ORDER = ['id', 'num', 'title', 'unit', 'cards', 'glossary', 'timeline', 'sources', 'match', 'myths', 'quiz', 'videos', 'intro', 'sections', 'fichas', 'mapa', 'podcast']
d = {k: d[k] for k in ORDER if k in d} | {k: v for k, v in d.items() if k not in ORDER}
# comprobaciones
ids = {f['id'] for f in d['fichas']}; secs = {s['code'] for s in d['sections']} | {'5.1', '5.2', '5.3'}
bad = []
for r in d['mapa']['ramas']:
    for n in r['nodos']:
        for f in [n['f']] + n.get('fs', []):
            if f not in ids: bad.append(('mapa', f))
for k in ['cards', 'glossary', 'sources', 'myths', 'quiz', 'match', 'timeline', 'videos']:
    for it in d[k]:
        if it.get('sec') and it['sec'] not in secs: bad.append((k, it['sec']))
for c in d['cards']:
    if not os.path.exists(c['img']): bad.append(c['img'])
for f in d['fichas']:
    for im in f['images']:
        if not os.path.exists(im['src']): bad.append(im['src'])
print('errores:', bad); print('fichas sin EN:', [f['code'] for f in d['fichas'] if f['body']['es'] and not f['body']['en']])
json.dump(d, open('data/tema05.json', 'w'), ensure_ascii=False, indent=1)
print({k: len(d[k]) for k in ['fichas', 'cards', 'glossary', 'timeline', 'sources', 'match', 'myths', 'quiz', 'videos', 'podcast']})
