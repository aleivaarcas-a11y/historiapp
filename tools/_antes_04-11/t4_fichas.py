#!/usr/bin/env python3
"""Tema 4 (Etruria y Roma) en Historiapp, 25-10-2026: fichas ES/EN desde el texto de pantalla.
Cuerpo en castellano: texto de las diapositivas de «TEMAS NUEVOS/TEMA 4. Etruria y Roma.pptx» (95, 22-10).
Cuerpo en inglés: texto de las mismas diapositivas en «NEW TOPICS/Topic 4. Etruria and Rome.pptx».
No se usan las notas del orador. Imágenes en img/t4 (tools/t4_imgsel.json); infografías con versión ES y EN.
Uso: python3 tools/t4_fichas.py"""
import json, os, re, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
import construir_fichas as CF

SEC_EN = {'4.1': 'Sport in Etruscan culture', '4.2': 'Sport in Ancient Rome', '4.2.1': 'Historical introduction',
          '4.2.2': 'Sporting spectacles in Rome', '4.2.3': 'The amphitheatre, gladiators and other games',
          '4.2.4': 'The circus and chariot racing', '4.2.5': 'Baths, ball games and athletics', '4.2.6': 'The end of the spectacles'}
se = json.load(open('tools/secciones_en.json')); se.update(SEC_EN)
json.dump(se, open('tools/secciones_en.json', 'w'), ensure_ascii=False, indent=1)

SEL = json.load(open('tools/t4_imgsel.json')); PH, INF = SEL['PH'], SEL['INF']
im = json.load(open('tools/imgmap.json')); im['t4'] = PH
json.dump(im, open('tools/imgmap.json', 'w'), ensure_ascii=False, indent=1)

base = json.load(open('tools/tema03_vacio.json'))
base.update({'id': 't4', 'num': 4, 'title': {'es': 'Etruria y Roma', 'en': 'Etruria and Rome'}})
json.dump(base, open('data/tema04.json', 'w'), ensure_ascii=False, indent=1)
CF.main('tools/fuentes/t4_slides.json', 'data/tema04.json', 'img/t4', 'tools/imgmap.json')

es = {x['slide']: x for x in json.load(open('tools/fuentes/t4_slides.json'))}
en = {x['slide']: x for x in json.load(open('tools/fuentes/t4_slides_en.json'))}
KW = {'bailarines_triclinio': 'Bailarines', 'tumba_bigas_espectadores': 'Mujeres espectadoras', 'discobolo_olimpiadas': 'Lanzador', 'luchadores_augures': 'Luchadores ·',
      'olpe_pugilato': 'Olpe', 'luchadores_mona': 'ante un juez', 'saltador_pertiga': 'pértiga', 'carrera_casuccini': 'Casuccini', 'accidente_olimpiadas': 'accidente',
      'bocado_etrusco': 'Bocado', 'jinete_bronce': 'Jinete', 'desultor_bronce': 'Desultor', 'oinochoe_tragliatella': 'Oinochoe', 'kottabos_nadador': 'kottabos', 'candelabro_etrusco': 'Candelabro',
      'mapa_imperio': 'máxima extensión', 'anfiteatro_pula': 'Pula', 'anfiteatro_el_djem': 'El Djem', 'anfiteatro_pompeya': 'Pompeya', 'anfiteatro_italica': 'Itálica',
      'cuartel_pompeya_patio': 'Patio porticado', 'cuartel_pompeya_portico': 'Pórtico y puerta', 'ben_hur': 'Ben-Hur, de', 'ben_hur_rodaje': 'Rodaje',
      'pila_paganica': 'paganica', 'follis_dibujo': 'follis', 'jugadores_pelota': 'Jugadores de pelota', 'circo_maximo': 'Reconstrucción histórica', 'circo_maximo_bell': 'según Bell',
      'saltador_caza_pesca': 'Caza y la Pesca', 'tumba_nadador': 'Tumba del Nadador', 'zliten_venationes': 'Zliten', 'venator_merida': 'Venator', 'estadio_domiciano_recon': 'Estadio de Domiciano',
      'coliseo': 'conocido como Coliseo', 'phersu': 'phersu', 'muchachas_bikini': 'bikini'}
CAP = re.compile(r'\s·\s')
def limpio(paras, title):
    out = []
    for p in paras:
        p = p.strip()
        if len(p) < 4 or CF.is_ref(p) or p.isdigit() or p.lower() == (title or '').lower(): continue
        if CAP.search(p) and len(p) < 260: continue                      # pie de imagen
        if len(p) < 70 and not p.endswith(('.', ':', '?')): continue      # lugar y fecha, rótulos de gráfico
        if len(p) < 75 and re.search(r'(a|d)\.\s?C\.$', p): continue      # lugar y fecha que acaban en a. C. / d. C.
        out.append(p)
    return out
def captions(paras):
    return [p.strip() for p in paras if CAP.search(p) and len(p) < 260 and not CF.is_ref(p)]

d = json.load(open('data/tema04.json'))
for f in d['fichas']:
    tes = f['title']['es']; f['title']['en'] = (en[f['slides'][0]].get('title') or '').strip().rstrip(':.')
    if not f['title']['en']:
        p0 = en[f['slides'][0]]['paras']; f['title']['en'] = p0[0] if p0 else ''
    bes, ben = [], []
    for sn in f['slides']:
        bes += limpio(es[sn]['paras'], tes); ben += limpio(en[sn]['paras'], f['title']['en'])
    f['body'] = {'es': bes, 'en': ben}; f['slide'] = {'es': [], 'en': []}; f['source'] = 'diapositiva'
    # pies: cada foto toma el pie de su diapositiva que contiene su palabra clave (KW); si la diapositiva tiene una sola foto y un solo pie, ese
    for sn in f['slides']:
        mine = [x for x in f['images'] if any(x['src'] == f'img/t4/{PH[k]}.jpg' for k in PH if k.startswith(f's{sn:02d}_'))]
        ce, cn = captions(es[sn]['paras']), captions(en[sn]['paras'])
        if len(ce) != len(cn): continue
        for x in mine:
            nm = x['src'].split('/')[-1][:-4]
            if nm in KW:
                hit = [i for i, c in enumerate(ce) if KW[nm] in c]
                if hit: x['caption'] = {'es': ce[hit[0]], 'en': cn[hit[0]]}
            elif len(mine) == 1 and len(ce) == 1:
                x['caption'] = {'es': ce[0], 'en': cn[0]}
    for sn in f['slides']:
        for k, n in INF.items():
            if int(k[1:].split('_')[0]) == sn and k != 's05_1':
                f['images'].append({'src': f'img/t4/{n}.jpg', 'caption': {}, 'lang': 'es'})
                f['images'].append({'src': f'img/t4/{n}_en.jpg', 'caption': {}, 'lang': 'en'})
CAPX = {'anfiteatro_pula': ('Anfiteatro de Pula, Croacia', 'Amphitheatre of Pula, Croatia'), 'anfiteatro_el_djem': ('Anfiteatro de El Djem, Túnez', 'Amphitheatre of El Djem, Tunisia'),
        'anfiteatro_pompeya': ('Anfiteatro de Pompeya, Italia', 'Amphitheatre of Pompeii, Italy'), 'anfiteatro_italica': ('Anfiteatro de Itálica, España', 'Amphitheatre of Italica, Spain'),
        'anfiteatro_madera': ('Reconstrucción del primer anfiteatro en el Foro Romano según Mañas Bastida (2011)', 'Reconstruction of the first amphitheatre in the Roman Forum after Mañas Bastida (2011)'),
        'gladiador_kourion': ('Gladiador, mosaico de la casa de los gladiadores · Siglo III d. C. · Kourion (Chipre)', 'Gladiator, mosaic from the House of the Gladiators · 3rd century AD · Kourion (Cyprus)'),
        'gladius_pompeya': ('Espadas de tipo gladius · Pompeya, cuartel de los gladiadores, siglo I d. C.', 'Swords of the type known as gladius · Pompeii, gladiators\' barracks, 1st century AD'),
        'casco_murmillo': ('Casco de murmillo · Pompeya, cuartel de los gladiadores, siglo I d. C.', 'Murmillo helmet · Pompeii, gladiators\' barracks, 1st century AD'),
        'greba_tracio': ('Greba alta de tracio · Pompeya, cuartel de los gladiadores, siglo I d. C.', 'High greave of a Thracian · Pompeii, gladiators\' barracks, 1st century AD'),
        'caracalla_actual': ('Termas de Caracalla, estado actual · Roma', 'Baths of Caracalla, present state · Rome'), 'caracalla_planta': ('Termas de Caracalla, reconstrucción moderna de la planta', 'Baths of Caracalla, modern reconstruction of the plan'),
        'caracalla_interior': ('Termas de Caracalla, reconstrucción del interior', 'Baths of Caracalla, reconstruction of the interior'), 'pila_paganica': ('Reconstrucción de una pila paganica', 'Reconstruction of a pila paganica'),
        'estadio_domiciano_arcos': ('Estadio de Domiciano, arcos del graderío original', 'Stadium of Domitian, arches of the original stands')}
for f in d['fichas']:
    for x in f['images']:
        nm = x['src'].split('/')[-1][:-4]
        if nm in CAPX: x['caption'] = {'es': CAPX[nm][0], 'en': CAPX[nm][1]}
# diapositiva 5, la línea de Etruria (solo gráfico y Fuente), con ficha propia tras la introducción
if not any(5 in f['slides'] for f in d['fichas']):
    i = [k for k, f in enumerate(d['fichas']) if 4 in f['slides']][0]
    d['fichas'].insert(i + 1, {'id': 'etruria-en-el-tiempo', 'sec': '4.1', 'title': {'es': 'Etruria en el tiempo', 'en': 'Etruria through time'},
        'slides': [5], 'images': [{'src': 'img/t4/linea_etruria.jpg', 'caption': {}, 'lang': 'es'}, {'src': 'img/t4/linea_etruria_en.jpg', 'caption': {}, 'lang': 'en'}],
        'source': 'diapositiva', 'essay': {'es': [], 'en': []}, 'body': {'es': [], 'en': []}, 'slide': {'es': [], 'en': []},
        'refs': [p for p in es[5]['paras'] if CF.is_ref(p)]})
# el gráfico final del relevo (diap. 87, sin título) va con las funciones del deporte romano
for f in d['fichas']:
    if 86 in f['slides']:
        f['images'] += [{'src': 'img/t4/relevo_creta_roma.jpg', 'caption': {}, 'lang': 'es'}, {'src': 'img/t4/relevo_creta_roma_en.jpg', 'caption': {}, 'lang': 'en'}]
for f in d['fichas']:
    if f['id'] == 'tipos-de-gladiadores-i': f['id'] = 'tipos-de-gladiadores'; f['title'] = {'es': 'Tipos de gladiadores', 'en': 'Types of gladiator'}
for k, f in enumerate(d['fichas'], 1): f['code'] = f"H4·{k:02d}"
def tipos(paras):
    out, head = [], None
    for p in paras:
        p = p.strip()
        if CF.is_ref(p) or CAP.search(p): continue
        if len(p) < 60 and not p.endswith('.'): head = p; continue
        out.append((head + '. ' + p) if head else p); head = None
    return out
for f in d['fichas']:
    if 52 in f['slides']:
        f['body'] = {'es': sum((tipos(es[n]['paras']) for n in f['slides']), []), 'en': sum((tipos(en[n]['paras']) for n in f['slides']), [])}
        for x in f['images']:
            nm = x['src'].split('/')[-1][:-4]
            x['caption'] = {'es': {'murmillo': 'Murmillo', 'tracio': 'Tracio (thraex)', 'hoplomaco': 'Hoplómaco (hoplomachus)', 'secutor': 'Secutor', 'reciario': 'Reciario (retiarius)', 'scissor': 'Scissor', 'provocator': 'Provocador (provocator)', 'eques': 'Ecuestre (eques)', 'esedario': 'Esedario (essedarius)', 'sagittarius': 'Arquero (sagittarius)', 'dimachaerus': 'Dimaquero (dimachaerus)'}.get(nm, ''),
                            'en': {'murmillo': 'Murmillo', 'tracio': 'Thracian (thraex)', 'hoplomaco': 'Hoplomachus', 'secutor': 'Secutor', 'reciario': 'Retiarius', 'scissor': 'Scissor', 'provocator': 'Provocator', 'eques': 'Horseman (eques)', 'esedario': 'Essedarius', 'sagittarius': 'Archer (sagittarius)', 'dimachaerus': 'Dimachaerus'}.get(nm, '')}
CU = json.load(open('tools/t4_cuadros.json')) if os.path.exists('tools/t4_cuadros.json') else {}
for f in d['fichas']:
    if f['id'] in CU: f['body'] = CU[f['id']]
json.dump(d, open('data/tema04.json', 'w'), ensure_ascii=False, indent=1)
for f in d['fichas']:
    print(f['code'], f['id'], f['slides'], f['title']['es'][:40], '|', f['title']['en'][:36], len(f['images']), len(f['body']['es']), len(f['body']['en']))
