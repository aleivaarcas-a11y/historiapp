# -*- coding: utf-8 -*-
"""Genera repaso/clase_en_data.js: secuencia fija de la clase de repaso en pantalla
(1.º Inglés, Temas 1-3). Lee los bancos ya curados de repaso/jugar.html (constante D)
y data/tema03.json. Uso: python3 build_data.py <carpeta Historiapp>"""
import json, re, random, sys, os

H = sys.argv[1]
s = open(os.path.join(H, 'repaso/jugar.html'), encoding='utf-8').read()
D = json.loads(re.search(r'const D=(\{.*?\});\n', s, re.S).group(1))
T3 = json.load(open(os.path.join(H, 'data/tema03.json'), encoding='utf-8'))
rnd = random.Random(1611)

def bi(en, es): return {'en': en, 'es': es}
def mcq(q, r, sec=20, quote=None, img=None, cap=None):
    o = list(enumerate(q['options'])); rnd.shuffle(o)
    st = {'r': r, 'k': 'mcq', 'q': q.get('question') or q.get('q'), 'opts': [x for _, x in o],
          'ans': [i for i, _ in o].index(q['answer']), 'ex': q.get('explain'), 'sec': sec}
    if quote: st['quote'] = quote
    if img: st['img'] = img; st['cap'] = cap
    return st
def tf(c, r, sec=15):
    st = {'r': r, 'k': 'tf', 'q': c['claim'], 'ans': 0 if c['answer'] else 1, 'ex': c['explain'], 'sec': sec}
    if c.get('img'): st['img'] = c['img']; st['cap'] = c['caption']
    return st
def gl(arr, term_en):
    return next(g for g in arr if g['term']['en'] == term_en)

ROUNDS = [
 {'n': bi('Origins', 'El origen'), 'icon': '🔥', 't': bi('Topic 1', 'Tema 1'), 'mode': 'speed',
  'd': bi('Warm-up with Topic 1: concepts, theories and Prehistory.', 'Calentamiento con el Tema 1: conceptos, teorías y Prehistoria.')},
 {'n': bi('Myth or fact', 'Mito o realidad'), 'icon': '⚖️', 't': bi('Topics 1-3', 'Temas 1-3'), 'mode': 'speed',
  'd': bi('True or false? Look at the image before you answer.', '¿Verdadero o falso? Mira la imagen antes de responder.')},
 {'n': bi('The detail', 'El detalle'), 'icon': '🔍', 't': bi('Topics 2-3', 'Temas 2-3'), 'mode': 'speed',
  'd': bi('A detail from an exam image. The picture zooms out second by second: the sooner you answer, the more you score.', 'Un detalle de una imagen del examen. La imagen se abre segundo a segundo: cuanto antes respondas, más puntos.')},
 {'n': bi('Hidden word', 'Palabra oculta'), 'icon': '🔤', 't': bi('Glossary 1-3', 'Glosario 1-3'), 'mode': 'word',
  'd': bi('A definition from the glossary and four hidden terms. Letters appear every few seconds.', 'Una definición del glosario y cuatro términos ocultos. Cada pocos segundos aparece una letra.')},
 {'n': bi("Archaeologist's eye", 'Ojo de arqueólogo'), 'icon': '🏺', 't': bi('Exam part C', 'Parte C del examen'), 'mode': 'speed',
  'd': bi('Three exam images, three questions each: what it is, what it describes and what it cannot prove.', 'Tres imágenes del examen y tres preguntas por imagen: qué es, qué describe y qué no permite afirmar.')},
 {'n': bi('Heb-Sed', 'Heb-Sed'), 'icon': '🐂', 't': bi('Topic 2', 'Tema 2'), 'mode': 'exam',
  'd': bi('Egypt, Persia and Phoenicia with the rules of the exam test.', 'Egipto, Persia y Fenicia con las reglas del test del examen.')},
 {'n': bi('Olympia', 'Olimpia'), 'icon': '🏛️', 't': bi('Topic 3', 'Tema 3'), 'mode': 'exam',
  'd': bi('Crete and Greece with the rules of the exam test.', 'Creta y Grecia con las reglas del test del examen.')},
 {'n': bi('The final', 'La final'), 'icon': '🏆', 't': bi('Topics 1-3', 'Temas 1-3'), 'mode': 'final',
  'd': bi('Double points and exam rules. It ends with the relay: put the events in order.', 'Puntos dobles y reglas del examen. Se cierra con el relevo: ordena los sucesos.')},
]

S = []
# 0 · Origins
q = D['t1quiz']
for i in [1, 2, 3, 6, 9, 7]: S.append(mcq(q[i], 0))
# definición -> término (glosario T1)
g = gl(D['t1gloss'], 'Controlled de-controlling')
alt = [gl(D['t1gloss'], x) for x in ['Magic circle', 'Ethnographic analogy', 'Biological or instinct theory']]
o = [g] + alt; rnd.shuffle(o)
S.insert(3, {'r': 0, 'k': 'mcq', 'q': bi('Which concept matches this definition?', '¿Qué concepto corresponde a esta definición?'),
  'quote': g['def'], 'opts': [x['term'] for x in o], 'ans': o.index(g),
  'ex': bi('Controlled de-controlling (Elias and Dunning). ' + g['def']['en'], 'Descontrol controlado (Elias y Dunning). ' + g['def']['es']), 'sec': 20})

# 1 · Myth or fact
# (sin imágenes que salgan después en El detalle u Ojo de arqueólogo)
S += [tf(D['t1myths'][0], 1), tf(D['t1myths'][7], 1), tf(D['t2cards'][45], 1), tf(D['t2cards'][4], 1),
      tf(D['t2cards'][42], 1), tf(D['t3cards'][42], 1), tf(D['t3myths'][4], 1)]

# 2 · The detail
DET = [
 ('I2-n03', [.22, 0, .58, .3], bi('Bird-hunting stick', 'Bastón arrojadizo para aves')),
 ('I2-n04', [.22, 0, .82, .36], bi('Fencing sticks (tahtib)', 'Bastones de esgrima (tahtib)')),
 ('I2-n08', [.48, .5, 1, .8], bi('Senet board and pieces', 'Tablero y piezas del senet')),
 ('I3-n11', [.33, .22, .82, .58], bi('Halteres for the jump', 'Halteras para el salto')),
 ('I3-n12', [.33, .33, .72, .72], bi('Javelin thong, the ankyle', 'Correa de la jabalina (ankýle)')),
 ('I3-n15', [.6, .03, 1, .78], bi("The judge's rod", 'Vara del juez')),
 ('I3-n01', [.32, .18, .88, .56], bi("Boxer's glove on one hand", 'Guante de púgil en una mano')),
]
DETCAP = {
 'I2-n03': bi('Bird hunting with a throwing stick. Theban tomb, Sheikh Abd el-Qurna. 18th Dynasty, c. 1400 BC', 'Caza de aves con bastón arrojadizo. Tumba tebana de Sheikh Abd el-Qurna. 18ª dinastía, hacia 1400 a. C.'),
 'I2-n04': bi('Stick fencing (tahtib). Tomb of Neferhotep (TT49), Thebes. 18th Dynasty, c. 1330 BC', 'Esgrima de bastón (tahtib). Tumba de Neferhotep (TT49), Tebas. 18ª dinastía, hacia 1330 a. C.'),
 'I2-n08': bi('Nefertari playing senet. Her tomb (QV66), Valley of the Queens. 19th Dynasty, c. 1255 BC', 'Nefertari jugando al senet. Su tumba (QV66), Valle de las Reinas. 19ª dinastía, hacia 1255 a. C.'),
 'I3-n11': bi('Jumper with halteres. c. 470 BC. Archaeological Museum, Palermo', 'Saltador con halteras. Hacia 470 a. C. Museo Arqueológico de Palermo'),
 'I3-n12': bi('Javelin thrower with the thong wound round the shaft', 'Lanzador de jabalina con la correa enrollada en el asta'),
 'I3-n15': bi('Pankratiasts and judge with his rod. c. 500 BC. Metropolitan Museum, New York', 'Pancratistas y juez con la vara. Hacia 500 a. C. Museo Metropolitano, Nueva York'),
 'I3-n01': bi('Boxing Boys fresco. Akrotiri, Thera. Late 17th century BC', 'Fresco de los niños púgiles. Akrotiri, Tera. Finales del siglo XVII a. C.'),
}
order = DET[:]; rnd.shuffle(order)
for did, crop, lab in order:
    others = [d for d in DET if d[0] != did]; rnd.shuffle(others)
    if all(len(d[2]['en']) < len(lab['en']) for d in others[:3]):
        lon = [d for d in others if len(d[2]['en']) >= len(lab['en'])]
        if lon: others = [lon[0]] + [d for d in others if d is not lon[0]]
    o = [(did, lab)] + [(d[0], d[2]) for d in others[:3]]; rnd.shuffle(o)
    S.append({'r': 2, 'k': 'det', 'q': bi('What is this detail?', '¿Qué es este detalle?'), 'img': 'repaso/img/%s.jpg' % did,
              'crop': crop, 'cap': DETCAP[did], 'opts': [x[1] for x in o], 'ans': [x[0] for x in o].index(did),
              'ex': DETCAP[did], 'sec': 20})

# 3 · Hidden word (definición del glosario, cuatro términos enmascarados)
WORDS = [('t2gloss', 'Pharao ludens'), ('t3gloss', 'Kalokagathia'), ('t1gloss', 'Bipedalism'),
         ('t2gloss', 'Paradeisos'), ('t3gloss', 'Ekecheiria'), ('t3gloss', 'Periodonikes')]
POOL = {'t1gloss': ['Secularism', 'Quantification', 'Rationalisation', 'Bureaucratisation', 'Gymnastike', 'Deportare'],
        't2gloss': ['Victor perpetuus', 'Pahlavan', 'Zurkhaneh', 'Khopesh', 'Paradeisos', 'Pharao ludens', 'Tahtib'],
        't3gloss': ['Hellanodikai', 'Spondophoroi', 'Hoplitodromos', 'Paidotribes', 'Mastigophoroi', 'Kalokagathia', 'Ekecheiria', 'Periodonikes']}
for src, term in WORDS:
    g = gl(D[src], term)
    pool = [x for x in POOL[src] if x != term]; rnd.shuffle(pool)
    # distractores de longitud parecida, para que la longitud no delate la respuesta
    pool.sort(key=lambda x: abs(len(x) - len(term)))
    o = [g] + [gl(D[src], x) for x in pool[:3]]; rnd.shuffle(o)
    S.append({'r': 3, 'k': 'word', 'q': bi('Which term matches this definition?', '¿Qué término corresponde a esta definición?'),
              'quote': g['def'], 'opts': [x['term'] for x in o], 'ans': o.index(g),
              'ex': bi(g['term']['en'] + '. ' + g['def']['en'], g['term']['es'] + '. ' + g['def']['es']), 'sec': 25})

# 4 · Archaeologist's eye (textos de EXÁMENES 26_27/_trabajo/imagenes_C, traducidos)
EYE = [
 {'img': 'repaso/img/I2-n02.jpg',
  'cap': bi('Red Chapel, Karnak. 18th Dynasty', 'Capilla Roja, Karnak. 18ª dinastía'),
  'qs': [
   (bi('What does this image show?', '¿Qué muestra esta imagen?'),
    [bi('Hatshepsut running beside the Apis bull in the Heb-Sed', 'Hatshepsut corriendo junto al toro Apis en el Heb-Sed'),
     bi('Amenhotep II training his horses beside the Great Sphinx', 'Amenofis II entrenando sus caballos junto a la Gran Esfinge'),
     bi('Seti I raising a Djed pillar during the Heb-Sed ceremonial', 'Seti I levantando un pilar Djed durante el ceremonial del Heb-Sed'),
     bi('The Assyrian king Ashurbanipal hunting a lion on foot', 'El rey asirio Asurbanipal cazando un león a pie')], 0,
    bi('Hatshepsut runs beside the Apis bull in the Heb-Sed, Red Chapel of Karnak, year 16 of her reign (c. 1464 BC).',
       'Hatshepsut corre junto al toro Apis en el Heb-Sed, Capilla Roja de Karnak, año 16 de su reinado (hacia 1464 a. C.).')),
   (bi('Which sentence DESCRIBES the image (C1) instead of interpreting it?', '¿Qué frase DESCRIBE la imagen (C1) en lugar de interpretarla?'),
    [bi('A figure in profile strides to the right with a tall crown, a short kilt and an object in each hand.', 'Una figura de perfil avanza hacia la derecha con corona alta, faldellín corto y un objeto en cada mano.'),
     bi('The relief records the run of the Heb-Sed, the jubilee festival that renewed the power of the Egyptian king.', 'El relieve documenta la carrera del Heb-Sed, la fiesta del jubileo que renovaba el poder del rey egipcio.'),
     bi('The run was compulsory, and its out-and-back course symbolised the union of the two kingdoms.', 'La carrera era obligada y su recorrido de ida y vuelta simbolizaba la unión de los dos reinos.'),
     bi('A weakened king endangered his role as guarantor of world order, and the rite restored him.', 'Un rey debilitado comprometía su papel de garante del orden del mundo, y el rito lo restituía.')], 0,
    bi('C1 describes only what you see: figure, crown, kilt, objects, the bull below. The other three are interpretations (C2).',
       'El C1 describe solo lo que se ve: figura, corona, faldellín, objetos y el toro debajo. Las otras tres son interpretaciones (C2).')),
   (bi('Which claim does this image NOT allow you to make (C3)?', '¿Qué afirmación NO permite hacer esta imagen (C3)?'),
    [bi('That Egyptian women in general took part in running races', 'Que las mujeres egipcias en general practicaran la carrera'),
     bi('That a woman reigning as pharaoh had to show physical strength', 'Que una mujer que reinaba como faraón debía exhibir fuerza física'),
     bi('That the Heb-Sed run was a rite that renewed the royal power', 'Que la carrera del Heb-Sed era un rito que renovaba el poder real'),
     bi('That the Apis bull could accompany the ruler in the royal run', 'Que el toro Apis podía acompañar al soberano en la carrera real')], 0,
    bi('The scene shows a queen ruling as pharaoh: the obligation came from the royal office, not from being a woman.',
       'La escena retrata a una reina que ejercía como faraón: la obligación derivaba de esa función regia, no de ser mujer.'))]},
 {'img': 'repaso/img/I3-n02.jpg',
  'cap': bi('Heraklion Archaeological Museum', 'Museo Arqueológico de Heraclión'),
  'qs': [
   (bi('What does this image show?', '¿Qué muestra esta imagen?'),
    [bi('The Bull-Leaping Fresco from the palace of Knossos', 'El fresco del salto del toro del palacio de Cnoso'),
     bi('The Boxing Boys fresco from Akrotiri, on Thera', 'El fresco de los niños púgiles de Akrotiri, en Tera'),
     bi('A Mycenaean fresco with warriors in a chariot', 'Un fresco micénico con guerreros en carro'),
     bi('The capture of a bull on the gold cups from Vapheio', 'La captura de un toro en las tazas de oro de Vafio')], 0,
    bi('Bull-Leaping Fresco, palace of Knossos, c. 1450-1375 BC.', 'Fresco del salto del toro, palacio de Cnoso, hacia 1450-1375 a. C.')),
   (bi('Which sentence DESCRIBES the image (C1) instead of interpreting it?', '¿Qué frase DESCRIBE la imagen (C1) en lugar de interpretarla?'),
    [bi('A red-skinned figure somersaults over the back of a large spotted bull at full gallop.', 'Una figura de piel roja da una voltereta sobre el lomo de un gran toro moteado lanzado al galope.'),
     bi('The fresco records bull-leaping, the practice most often depicted in the art of Minoan Crete.', 'El fresco documenta el salto del toro, la práctica más representada en el arte de la Creta minoica.'),
     bi('Since almost all such images come from Knossos, the leap became an emblem of its power.', 'Como casi todas estas imágenes proceden de Cnoso, el salto se convirtió en emblema de su poder.'),
     bi('The leapers were young members of the elite, judging by their clothes and jewellery.', 'Los saltadores eran jóvenes de la élite, a juzgar por sus vestimentas y sus joyas.')], 0,
    bi('Only the first sentence describes what is painted. The others interpret it with knowledge from the topic (C2).',
       'Solo la primera frase describe lo que está pintado. Las otras lo interpretan con lo aprendido en el tema (C2).')),
   (bi('Which claim does this image NOT allow you to make (C3)?', '¿Qué afirmación NO permite hacer esta imagen (C3)?'),
    [bi('That the leap ended with the death or sacrifice of the bull', 'Que el salto terminara con la muerte o el sacrificio del toro'),
     bi('That the leap was a spectacle watched at community festivals', 'Que el salto era un espectáculo que se veía en fiestas de la comunidad'),
     bi('That the leapers belonged to the elite, judging by their dress', 'Que los saltadores pertenecían a la élite, a juzgar por su vestimenta'),
     bi('That bull-leaping became an emblem of the palace of Knossos', 'Que el salto del toro se convirtió en emblema del palacio de Cnoso')], 0,
    bi('The scene does not show that ending, and Minoan images do not link the leap with the death of the animal.',
       'La escena no muestra ese final y las imágenes minoicas no unen el salto con la muerte del animal.'))]},
 {'img': 'repaso/img/I3-n10.jpg',
  'cap': bi('Attributed to the Euphiletos Painter. British Museum, London', 'Atribuida al Pintor de Eufileto. Museo Británico, Londres'),
  'qs': [
   (bi('What does this image show?', '¿Qué muestra esta imagen?'),
    [bi('Pentathlon events on a Panathenaic amphora', 'Pruebas del pentatlón en un ánfora panatenaica'),
     bi('Stadion runners racing on a black-figure Attic vase', 'Corredores del estadio en un vaso ático de figuras negras'),
     bi('A hoplite race on a black-figure vase', 'Una carrera de hoplitas en un vaso de figuras negras'),
     bi('Greek boxers and their judge on a vase', 'Púgiles griegos y su juez en un vaso')], 0,
    bi('Pentathlon events on a Panathenaic amphora attributed to the Euphiletos Painter, c. 530-520 BC.', 'Pruebas del pentatlón en un ánfora panatenaica atribuida al Pintor de Eufileto, hacia 530-520 a. C.')),
   (bi('Which sentence DESCRIBES the image (C1) instead of interpreting it?', '¿Qué frase DESCRIBE la imagen (C1) en lugar de interpretarla?'),
    [bi('Four naked athletes in different poses; one lifts a disc and two hold long javelins.', 'Cuatro atletas desnudos en posturas distintas; uno levanta un disco y dos sostienen jabalinas.'),
     bi('The amphora records the pentathlon, a contest that brought together five events.', 'El ánfora documenta el pentatlón, una competición que reunía cinco pruebas.'),
     bi('At Olympia the jump, javelin and discus were held only within the pentathlon.', 'En Olimpia el salto, la jabalina y el disco solo se disputaban dentro del pentatlón.'),
     bi('The Greeks admired the pentathlon because it rewarded versatility across five different events.', 'Los griegos admiraban el pentatlón porque premiaba la versatilidad en cinco pruebas distintas.')], 0,
    bi('The first sentence stays with what the painter drew. The others bring in knowledge from the topic (C2).',
       'La primera frase se queda en lo que dibujó el pintor. Las otras aportan conocimiento del tema (C2).')),
   (bi('Which claim does this image NOT allow you to make (C3)?', '¿Qué afirmación NO permite hacer esta imagen (C3)?'),
    [bi('That the scene shows a competition held at Olympia', 'Que la escena muestre una competición de Olimpia'),
     bi('That the pentathlon combined five different events', 'Que el pentatlón combinaba cinco pruebas distintas'),
     bi('That the discus and the javelin were pentathlon events', 'Que el disco y la jabalina eran pruebas del pentatlón'),
     bi('That pentathletes competed naked in this period', 'Que los pentatletas competían desnudos en esta época')], 0,
    bi('The vase does not name the contest, and as a Panathenaic amphora it is linked to the Panathenaia of Athens.',
       'La pieza no indica el certamen y, como ánfora panatenaica, se vincula a las Panateneas de Atenas.'))]},
]
for e in EYE:
    for q, opts, a, ex in e['qs']:
        o = list(enumerate(opts)); rnd.shuffle(o)
        S.append({'r': 4, 'k': 'mcq', 'q': q, 'opts': [x for _, x in o], 'ans': [i for i, _ in o].index(a), 'ex': ex,
                  'img': e['img'], 'cap': e['cap'], 'sec': 30, 'eye': True})

# 5 · Heb-Sed (Tema 2, reglas del examen)
for i in [0, 3, 5, 9, 15, 12]: S.append(mcq(D['t2quiz'][i], 5))
# 6 · Olympia (Tema 3, reglas del examen)
for i in [1, 2, 5, 8, 13, 16]: S.append(mcq(T3['quiz'][i], 6))
src = D['t3sources'][3]
S.append(mcq(src, 6, sec=25, quote=src['text']))
# 7 · The final (doble, reglas del examen) y relevo de cronología
S.append(mcq(D['t1quiz'][0], 7))
S.append(mcq(D['t2quiz'][13], 7))
S.append(mcq(T3['quiz'][3], 7))
S.append(mcq(T3['quiz'][14], 7))
TL = D['timelines']
pick = [TL['1'][0]['items'][0], TL['2'][0]['items'][2], TL['3'][0]['items'][1], TL['3'][2]['items'][3]]
items = pick[:]; rnd.shuffle(items)
chron = sorted(range(4), key=lambda i: items[i]['year'])
S.append({'r': 7, 'k': 'ord', 'q': bi('The relay: tap the four events in chronological order, oldest first.', 'El relevo: toca los cuatro sucesos en orden cronológico, del más antiguo al más reciente.'),
          'opts': [x['label'] for x in items], 'ans': int(''.join(str(i + 1) for i in chron)),
          'ex': bi(' → '.join(items[i]['label']['en'] + ' (' + items[i]['date']['en'] + ')' for i in chron),
                   ' → '.join(items[i]['label']['es'] + ' (' + items[i]['date']['es'] + ')' for i in chron)), 'sec': 40})

# orden final por ronda y comprobaciones
S.sort(key=lambda x: x['r'])
for st in S:
    if st['k'] in ('mcq', 'det', 'word'):
        assert len(st['opts']) == 4 and 0 <= st['ans'] < 4, st
js = '/* Clase de repaso en pantalla · 1.º Inglés · Temas 1-3 (generado por tools/repaso_en/build_data.py) */\n'
js += 'const ROUNDS=' + json.dumps(ROUNDS, ensure_ascii=False) + ';\n'
js += 'const STEPS=' + json.dumps(S, ensure_ascii=False) + ';\n'
open(os.path.join(H, 'repaso/clase_en_data.js'), 'w', encoding='utf-8').write(js)
from collections import Counter
print('pasos', len(S), Counter(x['r'] for x in S), 'respuesta correcta por letra', Counter(x['ans'] for x in S if x['k'] != 'ord'))
for st in S:
    if st['k'] in ('mcq', 'det', 'word'):
        L = [len(o['en']) for o in st['opts']]
        if L[st['ans']] == max(L) and L.count(max(L)) == 1: print('LARGA', st['r'], st['q']['en'][:60])
