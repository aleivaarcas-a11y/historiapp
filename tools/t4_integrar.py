#!/usr/bin/env python3
"""Tema 4 (25-10-2026): vuelca en data/tema04.json los modos de estudio, vídeos, mapa, pódcast e introducción.
Ejecutar tras tools/t4_fichas.py. Todo el contenido sale del texto de pantalla del Tema 4 y del Topic 4."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
d = json.load(open('data/tema04.json'))
m = json.load(open('tools/t4_modos.json'))
for k, v in m.items(): d[k] = v
d['videos'] = json.load(open('tools/videos_t4.json'))
d['mapa'] = json.load(open('tools/t4_mapa.json'))
M = json.load(open('tools/mapas.json')); M['4'] = d['mapa']; json.dump(M, open('tools/mapas.json', 'w'), ensure_ascii=False, indent=1)
X = {f"{r['code']}.{i}": n['x'] for r in d['mapa']['ramas'] for i, n in enumerate(r['nodos']) if 'x' in n}
json.dump(X, open('tools/mapa_x_tema04.json', 'w'), ensure_ascii=False, indent=1)
d['intro'] = {
 'es': ['El tema recorre unos mil cuatrocientos años, desde los primeros siglos de Etruria, hacia 900 a. C., hasta las últimas carreras de Italia, en 549 d. C. Etruria no dejó textos sobre sus juegos y se conoce por las tumbas pintadas, mientras que Roma dejó muchos textos escritos casi siempre por la élite, de modo que cada dato se contrasta con inscripciones e imágenes. El hilo es el paso del agón griego al ludus romano, el juego ofrecido al público, y la pregunta de siempre en la asignatura, quién pagaba, quién competía y quién miraba.'],
 'en': ['The topic spans some fourteen hundred years, from the first centuries of Etruria, c. 900 BC, to the last races in Italy, in AD 549. Etruria left no texts about its games and is known through its painted tombs, whereas Rome left many texts written almost always by the elite, so every piece of data is checked against inscriptions and images. The thread is the passage from the Greek agon to the Roman ludus, the game offered to the public, and the course’s perennial question, who paid, who competed and who watched.']}
P = json.load(open('tools/podcast.json'))
P['4'] = [{'id': 't4_ep1', 'sec': '4', 'lang': 'es', 'dur': 1582, 'src': {'es': 'audio/t4_ep1.m4a?v=1', 'en': 'audio/t4_ep1_en.m4a?v=1'},
  'title': {'es': 'Púgiles con flauta, aurigas millonarios y una grada ordenada', 'en': 'Boxers with Flutes, Millionaire Charioteers and Ordered Stands'},
  'desc': {'es': 'Repaso del Tema 4 en forma de conversación y en el mismo orden que las clases, desde las tumbas pintadas de Etruria, con el pugilato al son de la flauta, las carreras de carros y el phersu, hasta el final de los espectáculos romanos, pasando por ludi y munera, quién pagaba los juegos, la grada ordenada del anfiteatro, los gladiadores, el circo y sus facciones, Diocles, las termas y los juegos de pelota.',
           'en': 'A conversational review of Unit 4 that follows the order of the lectures, from the painted tombs of Etruria, with boxing to the flute, chariot racing and the phersu, to the end of the Roman spectacles, by way of ludi and munera, who paid for the games, the ordered stands of the amphitheatre, gladiators, the circus and its factions, Diocles, the baths and ball games.'},
  'durs': {'es': 1582, 'en': 1762}}]
json.dump(P, open('tools/podcast.json', 'w'), ensure_ascii=False, indent=1)
d['podcast'] = P['4']
# comprobaciones
ids = {f['id'] for f in d['fichas']}; secs = {s['code'] for s in d['sections']}
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
for v in d['videos']:
    for L in 'es', 'en':
        for kk in 'src', 'poster':
            if not os.path.exists(v[kk][L].split('?')[0]): bad.append(v[kk][L])
for f in d['fichas']:
    for im in f['images']:
        if not os.path.exists(im['src']): bad.append(im['src'])
for L in 'es', 'en':
    if not os.path.exists(f'audio/t4_ep1{"" if L == "es" else "_en"}.m4a'): bad.append('audio ' + L)
print('errores:', bad); print('fichas sin EN:', [f['code'] for f in d['fichas'] if not f['body']['en']])
json.dump(d, open('data/tema04.json', 'w'), ensure_ascii=False, indent=1)
print({k: len(d[k]) for k in ['fichas', 'cards', 'glossary', 'timeline', 'sources', 'match', 'myths', 'quiz', 'videos', 'podcast']})
