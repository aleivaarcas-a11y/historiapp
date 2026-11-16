# -*- coding: utf-8 -*-
"""Genera repaso/clase_en_data.js: secuencia fija de la clase de repaso en pantalla
(1.º Inglés, Temas 1-3). v3 (15-11-2026, noche): correcciones de los dos jueces externos y
partida alargada a unos 40 minutos de juego (82 preguntas).
Lee los bancos ya curados de repaso/jugar.html (constante D) y data/tema01-03.json.
Uso: python3 build_data.py <carpeta Historiapp>"""
import json, re, random, sys, os
from collections import Counter

H = sys.argv[1]
s = open(os.path.join(H, 'repaso/jugar.html'), encoding='utf-8').read()
D = json.loads(re.search(r'const D=(\{.*?\});\n', s, re.S).group(1))
T1 = json.load(open(os.path.join(H, 'data/tema01.json'), encoding='utf-8'))
T3 = json.load(open(os.path.join(H, 'data/tema03.json'), encoding='utf-8'))
rnd = random.Random(1611)
def bi(en, es): return {'en': en, 'es': es}

ROUNDS = [
 {'icon': '🔥', 't': bi('Topic 1', 'Tema 1'), 'mode': 'speed', 'd': bi('Warm-up with Topic 1: concepts, theories, sources and Prehistory.', 'Calentamiento con el Tema 1: conceptos, teorías, fuentes y Prehistoria.')},
 {'icon': '⚖️', 't': bi('Topics 1-3', 'Temas 1-3'), 'mode': 'speed', 'd': bi('True or false? Some questions come with an image.', '¿Verdadero o falso? Algunas preguntas llevan imagen.')},
 {'icon': '🔍', 't': bi('Topics 2-3', 'Temas 2-3'), 'mode': 'speed', 'd': bi('A detail from an exam image. The picture zooms out second by second: the sooner you answer, the more you score.', 'Un detalle de una imagen del examen. La imagen se abre segundo a segundo: cuanto antes respondas, más puntos.')},
 {'icon': '🔤', 't': bi('Glossary 1-3', 'Glosario 1-3'), 'mode': 'word', 'd': bi('A definition from the glossary and four hidden terms. Letters appear every few seconds.', 'Una definición del glosario y cuatro términos ocultos. Cada pocos segundos aparece una letra.')},
 {'icon': '🏺', 't': bi('Exam part C', 'Parte C del examen'), 'mode': 'speed', 'd': bi('Four exam images, three questions each: what it is, how to describe it and what it cannot prove.', 'Cuatro imágenes del examen y tres preguntas por imagen: qué es, cómo se describe y qué no permite afirmar.')},
 {'icon': '🐂', 't': bi('Topic 2', 'Tema 2'), 'mode': 'exam', 'd': bi('Egypt, Persia and Phoenicia with the rules of the exam test.', 'Egipto, Persia y Fenicia con las reglas del test del examen.')},
 {'icon': '🏛️', 't': bi('Topic 3', 'Tema 3'), 'mode': 'exam', 'd': bi('Crete and Greece with the rules of the exam test.', 'Creta y Grecia con las reglas del test del examen.')},
 {'icon': '🏆', 't': bi('Topics 1-3', 'Temas 1-3'), 'mode': 'final', 'd': bi('Double points and exam rules. It ends with the relay: put the events in order.', 'Puntos dobles y reglas del examen. Se cierra con el relevo: ordena los sucesos.')},
]
for i, R in enumerate(ROUNDS): R['n'] = bi('Round %d' % (i + 1), 'Ronda %d' % (i + 1))

S = []
def add(r, q, opts, ans, ex, k='mcq', sec=20, **kw):
    o = list(enumerate(opts)); rnd.shuffle(o)
    st = {'r': r, 'k': k, 'q': q, 'opts': [x for _, x in o], 'ans': [i for i, _ in o].index(ans), 'ex': ex, 'sec': sec}
    st.update({a: b for a, b in kw.items() if b is not None}); S.append(st)
def bank(r, qb, sec=20, **over):
    """pregunta de un banco; over permite cambiar q, opts (lista completa, la correcta en q['answer']), ex, quote"""
    opts = over.pop('opts', None) or qb['options']
    add(r, over.pop('q', None) or qb.get('question') or qb.get('q'), opts, qb['answer'], over.pop('ex', None) or qb.get('explain'), sec=sec, **over)
def tf(c, r, sec=15, **over):
    st = {'r': r, 'k': 'tf', 'q': over.get('q') or c['claim'], 'ans': 0 if c['answer'] else 1, 'ex': over.get('ex') or c['explain'], 'sec': sec}
    if c.get('img'): st['img'] = c['img']; st['cap'] = c['caption']
    S.append(st)
def gl(arr, term_en): return next(g for g in arr if g['term']['en'] == term_en)
def glq(r, arr, term, others, q=None, quote=None, ex=None, sec=20):
    g = gl(arr, term); o = [g] + [gl(arr, x) for x in others]
    add(r, q or bi('Which concept matches this definition?', '¿Qué concepto corresponde a esta definición?'), [x['term'] for x in o], 0,
        ex or bi(g['term']['en'] + '. ' + g['def']['en'], g['term']['es'] + '. ' + g['def']['es']), sec=sec, quote=quote or g['def'])

# ---------- Ronda 1 · Tema 1 (rapidez) ----------
q = D['t1quiz']
bank(0, T1['quiz'][0])
bank(0, q[1], opts=[q[1]['options'][0], q[1]['options'][1], bi('Individual, collective and tribal', 'Individual, colectivo y tribal'), bi('Erotic, magical and warlike', 'Erótico, mágico y guerrero')])
bank(0, q[2], opts=[bi('The pedagogical theory', 'La teoría pedagógica'), bi('The cultural theory', 'La teoría cultural'), bi('The Marxist theory', 'La teoría marxista'), bi('The biological or instinct theory', 'La teoría biológica o del instinto')])
bank(0, T1['quiz'][1])
bank(0, q[3], opts=[bi('Achievement; discipline and fitness; popular festivity', 'Rendimiento; disciplina y forma física; fiesta popular'), bi('Ritual; record and quantification; spectacle', 'Rito; récord y cuantificación; espectáculo'), bi('Elite sport; discipline and drill; popular entertainment', 'Deporte de élite; disciplina e instrucción; entretenimiento popular'), bi('Play; exercise and training; competitive sport', 'Juego; ejercicio y entrenamiento; deporte de competición')])
g = gl(D['t1gloss'], 'Controlled de-controlling')
add(0, bi('Which concept matches this definition?', '¿Qué concepto corresponde a esta definición?'),
    [bi('Controlled decontrolling', 'Descontrol controlado'), gl(D['t1gloss'], 'Magic circle')['term'], gl(D['t1gloss'], 'Ethnographic analogy')['term'], gl(D['t1gloss'], 'Biological or instinct theory')['term']], 0,
    bi('The more restrained a society is, the more it needs places where excitement is permitted: sport works as a controlled decontrolling of emotions (Elias and Dunning).',
       'Cuanto más contenida es una sociedad, más necesita espacios donde la excitación esté permitida: el deporte funciona como un descontrol controlado de las emociones (Elias y Dunning).'),
    quote=bi('According to Elias and Dunning, the function of sport in societies that have lowered their tolerance of violence: a place where excitement is permitted.', g['def']['es']))
bank(0, T1['quiz'][2])
bank(0, q[6])
bank(0, q[9], q=bi(q[9]['q']['en'] if 'q' in q[9] else q[9]['question']['en'], '¿Qué compara Guttmann para saber qué tiene de moderno el deporte moderno?'))
glq(0, D['t1gloss'], 'Record', ['Quantification', 'Rationalisation', 'Bureaucratisation'])
bank(0, q[7])

# ---------- Ronda 2 · Verdadero o falso (rapidez) ----------
c = D['t1myths'][0]; tf(c, 1, ex=bi('They had four different terms: agon, athlos, gymnastike and paidia.', 'Tenían cuatro términos distintos: agón, athlos, gymnastiké y paidiá.'))
tf(D['t1myths'][7], 1)
tf(D['t1myths'][2], 1)
tf(D['t2cards'][45], 1)
tf(D['t2cards'][4], 1, q=bi('The raising of the Djed pillar, shown here, was one of the acts of the Heb-Sed ceremonial.', 'El izado del pilar Djed, que muestra la imagen, era uno de los actos del ceremonial del Heb-Sed.'),
   ex=bi('The ceremonial included a double coronation, arrows shot towards the four cardinal points and the raising of the Djed pillar, the backbone of Osiris and symbol of the stability of the state.',
         'El ceremonial incluía la doble coronación, el tiro de flechas hacia los cuatro puntos cardinales y el izado del pilar Djed, columna vertebral de Osiris y símbolo de la estabilidad del Estado.'))
tf(D['t1myths'][8], 1)
tf(D['t2cards'][36], 1)
tf(D['t2cards'][42], 1)
tf(D['t2cards'][32], 1)
tf(D['t3cards'][42], 1, q=bi('In Greek boxing, a fighter raised his index finger to concede defeat.', 'En el pugilato griego, el combatiente levantaba el índice para abandonar.'))
tf(D['t3myths'][10], 1)
tf(D['t3myths'][4], 1)

# ---------- Ronda 3 · El detalle ----------
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
 'I2-n03': bi('Bird hunting with a throwing stick. Theban tomb, Sheikh Abd el-Qurna. 18th Dynasty, c. 1400 BC', 'Caza de aves con bastón arrojadizo. Tumba tebana de Sheikh Abd el-Qurna. XVIII dinastía, hacia 1400 a. C.'),
 'I2-n04': bi('Stick fencing (tahtib). Tomb of Neferhotep (TT49), Thebes. 18th Dynasty, c. 1330 BC', 'Esgrima de bastón (tahtib). Tumba de Neferhotep (TT49), Tebas. XVIII dinastía, hacia 1330 a. C.'),
 'I2-n08': bi('Nefertari playing senet. Her tomb (QV66), Valley of the Queens. 19th Dynasty, c. 1255 BC', 'Nefertari jugando al senet. Su tumba (QV66), Valle de las Reinas. XIX dinastía, hacia 1255 a. C.'),
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
              'crop': crop, 'cap': DETCAP[did], 'opts': [x[1] for x in o], 'ans': [x[0] for x in o].index(did), 'ex': DETCAP[did], 'sec': 20})

# ---------- Ronda 4 · Palabra oculta ----------
WORDS = [('t2gloss', 'Pharao ludens', bi('Concept for a ruler whose office is exercised, in part, through play.', 'Concepto que designa a un soberano cuya función se ejerce, en parte, jugando.')),
         ('t3gloss', 'Kalokagathia', None), ('t1gloss', 'Bipedalism', None),
         ('t2gloss', 'Paradeisos', bi('Enclosed park stocked with animals for the Persian royal hunt.', 'Parque cercado y abastecido de animales para la caza real persa.')),
         ('t3gloss', 'Ekecheiria', None), ('t2gloss', 'Zurkhaneh', None), ('t3gloss', 'Periodonikes', None),
         ('t3gloss', 'Kleos', None), ('t3gloss', 'Arete', None)]
POOL = {'t1gloss': ['Secularism', 'Quantification', 'Rationalisation', 'Bureaucratisation', 'Gymnastike', 'Deportare'],
        't2gloss': ['Victor perpetuus', 'Pahlavan', 'Khopesh', 'Tahtib', 'Buzkashi', 'Chovgan', 'Jereed', 'Strigil'],
        't3gloss': ['Hellanodikai', 'Spondophoroi', 'Hoplitodromos', 'Paidotribes', 'Mastigophoroi', 'Aidos', 'Gymnasiarch', 'Perizoma', 'Polis', 'Agon', 'Stadion', 'Pale']}
for src, term, quote in WORDS:
    g = gl(D[src], term)
    pool = [x for x in POOL[src] if x != term]; rnd.shuffle(pool)
    pool.sort(key=lambda x: abs(len(x) - len(term)))
    ch = pool[:3]
    if all(len(x) < len(term) for x in ch):
        lon = [x for x in pool if len(x) >= len(term)]
        if lon: ch = ch[:2] + [lon[0]]
    o = [g] + [gl(D[src], x) for x in ch]; rnd.shuffle(o)
    qd = quote or g['def']
    S.append({'r': 3, 'k': 'word', 'q': bi('Which term matches this definition?', '¿Qué término corresponde a esta definición?'),
              'quote': qd, 'opts': [x['term'] for x in o], 'ans': o.index(g),
              'ex': bi(g['term']['en'] + '. ' + qd['en'], g['term']['es'] + '. ' + qd['es']), 'sec': 25})

# ---------- Ronda 5 · Ojo de arqueólogo (textos de EXÁMENES 26_27/_trabajo/imagenes_C, traducidos) ----------
QSHOW = bi('What does this image show?', '¿Qué muestra esta imagen?')
QC1 = bi('Which sentence DESCRIBES the image (C1) instead of interpreting it?', '¿Qué frase DESCRIBE la imagen (C1) en lugar de interpretarla?')
QC3 = bi('Which claim goes beyond what this image and the topic allow you to state (C3)?', '¿Qué afirmación va más allá de lo que permiten sostener esta imagen y el tema (C3)?')
EYE = [
 {'img': 'repaso/img/I2-n02.jpg', 'cap': bi('Hatshepsut running beside the Apis bull in the Heb-Sed. Red Chapel, Karnak. 18th Dynasty, c. 1464 BC', 'Hatshepsut corriendo junto al toro Apis en el Heb-Sed. Capilla Roja, Karnak. XVIII dinastía, hacia 1464 a. C.'),
  'qs': [
   (QSHOW, [bi('Hatshepsut running beside the Apis bull in the Heb-Sed', 'Hatshepsut corriendo junto al toro Apis en el Heb-Sed'),
     bi('Amenhotep II training his horses beside the Great Sphinx', 'Amenofis II entrenando sus caballos junto a la Gran Esfinge'),
     bi('Seti I raising a Djed pillar during the Heb-Sed ceremonial', 'Seti I levantando un pilar Djed durante el ceremonial del Heb-Sed'),
     bi('The Assyrian king Ashurbanipal hunting a lion on foot', 'El rey asirio Asurbanipal cazando un león a pie')],
    bi('Hatshepsut runs beside the Apis bull in the Heb-Sed, Red Chapel of Karnak, year 16 of her reign.', 'Hatshepsut corre junto al toro Apis en el Heb-Sed, Capilla Roja de Karnak, año 16 de su reinado.')),
   (QC1, [bi('A figure in profile strides to the right with a tall crown, a short kilt and an object in each hand.', 'Una figura de perfil avanza hacia la derecha con corona alta, faldellín corto y un objeto en cada mano.'),
     bi('Queen Hatshepsut runs the Heb-Sed course beside the sacred bull Apis to renew her power.', 'La reina Hatshepsut recorre la pista del Heb-Sed junto al toro sagrado Apis para renovar su poder.'),
     bi('The relief records the run of the Heb-Sed, the jubilee festival that renewed the power of the Egyptian king.', 'El relieve documenta la carrera del Heb-Sed, la fiesta del jubileo que renovaba el poder del rey egipcio.'),
     bi('A weakened king endangered his role as guarantor of world order, and the rite restored him.', 'Un rey debilitado comprometía su papel de garante del orden del mundo, y el rito lo restituía.')],
    bi('C1 describes only what you see: figure, crown, kilt and the objects in the hands. Naming Hatshepsut or the Heb-Sed is already interpretation (C2).', 'El C1 describe solo lo que se ve: figura, corona, faldellín y los objetos de las manos. Nombrar a Hatshepsut o el Heb-Sed ya es interpretar (C2).')),
   (QC3, [bi('That Egyptian women in general took part in running races', 'Que las mujeres egipcias en general practicaban la carrera'),
     bi('That a woman reigning as pharaoh had to show physical strength', 'Que una mujer que reinaba como faraón debía exhibir fuerza física'),
     bi('That the Heb-Sed run was a rite that renewed the royal power', 'Que la carrera del Heb-Sed era un rito que renovaba el poder real'),
     bi('That the Apis bull could accompany the ruler in the royal run', 'Que el toro Apis podía acompañar al soberano en la carrera real')],
    bi('The scene shows a queen ruling as pharaoh: the obligation came from the royal office, not from being a woman.', 'La escena retrata a una reina que ejercía como faraón: la obligación derivaba de esa función regia, no de ser mujer.'))]},
 {'img': 'repaso/img/I3-n02.jpg', 'cap': bi('Bull-Leaping Fresco. Palace of Knossos, c. 1450-1375 BC. Heraklion Archaeological Museum', 'Fresco del salto del toro. Palacio de Cnoso, hacia 1450-1375 a. C. Museo Arqueológico de Heraclión'),
  'qs': [
   (QSHOW, [bi('The Bull-Leaping Fresco from the palace of Knossos', 'El fresco del salto del toro del palacio de Cnoso'),
     bi('The Boxing Boys fresco from Akrotiri, on Thera', 'El fresco de los niños púgiles de Akrotiri, en Tera'),
     bi('A Mycenaean fresco with warriors in a chariot', 'Un fresco micénico con guerreros en carro'),
     bi('The capture of a bull on the gold cups from Vapheio', 'La captura de un toro en las tazas de oro de Vafio')],
    bi('Bull-Leaping Fresco, palace of Knossos, c. 1450-1375 BC.', 'Fresco del salto del toro, palacio de Cnoso, hacia 1450-1375 a. C.')),
   (QC1, [bi('A red-skinned figure is upside down above the back of a large spotted bull.', 'Una figura de piel roja aparece cabeza abajo sobre el lomo de un gran toro moteado.'),
     bi('Since almost all such images come from Knossos, the leap became an emblem of its power.', 'Como casi todas estas imágenes proceden de Cnoso, el salto se convirtió en emblema de su poder.'),
     bi('The fresco shows a rite of passage that young members of the elite had to complete.', 'El fresco muestra un rito de paso que debían superar los jóvenes de la élite.'),
     bi('The leapers were young members of the elite, judging by their clothes and jewellery.', 'Los saltadores eran jóvenes de la élite, a juzgar por sus vestimentas y sus joyas.')],
    bi('Only the sentence about the red-skinned figure and the spotted bull describes what is painted; the others interpret it with knowledge from the topic (C2).', 'Solo la frase sobre la figura de piel roja y el toro moteado describe lo pintado; las demás lo interpretan con lo aprendido en el tema (C2).')),
   (QC3, [bi('That the leap ended with the death or sacrifice of the bull', 'Que el salto terminaba con la muerte o el sacrificio del toro'),
     bi('That the bull shown was a domestic animal, not an aurochs', 'Que el toro representado era doméstico y no un uro'),
     bi('That the leapers belonged to the elite, judging by their dress', 'Que los saltadores pertenecían a la élite, a juzgar por su vestimenta'),
     bi('That red-skinned and white-skinned figures took part in the leap', 'Que en el salto intervenían figuras de piel roja y de piel blanca')],
    bi('The scene does not show that ending, and Minoan images do not link the leap with the death of the animal.', 'La escena no muestra ese final y las imágenes minoicas no unen el salto con la muerte del animal.'))]},
 {'img': 'repaso/img/I3-n10.jpg', 'cap': bi('Pentathlon events on a Panathenaic amphora attributed to the Euphiletos Painter, c. 530-520 BC. British Museum', 'Pruebas del pentatlón en un ánfora panatenaica atribuida al Pintor de Eufileto, hacia 530-520 a. C. Museo Británico'),
  'qs': [
   (QSHOW, [bi('Pentathlon events on a Panathenaic amphora', 'Pruebas del pentatlón en un ánfora panatenaica'),
     bi('Stadion runners racing on a black-figure Attic vase', 'Corredores del estadio en un vaso ático de figuras negras'),
     bi('A hoplite race on a black-figure vase', 'Una carrera de hoplitas en un vaso de figuras negras'),
     bi('Greek boxers and their judge on a vase', 'Púgiles griegos y su juez en un vaso')],
    bi('Pentathlon events on a Panathenaic amphora attributed to the Euphiletos Painter, c. 530-520 BC.', 'Pruebas del pentatlón en un ánfora panatenaica atribuida al Pintor de Eufileto, hacia 530-520 a. C.')),
   (QC1, [bi('Four naked figures in different poses; one lifts a disc and two hold long poles.', 'Cuatro figuras desnudas en posturas distintas; una levanta un disco y dos sostienen varas largas.'),
     bi('Pentathletes train with the discus and the javelin for the Panathenaia of Athens.', 'Unos pentatletas entrenan el disco y la jabalina para las Panateneas de Atenas.'),
     bi('At Olympia the jump, javelin and discus were held only within the pentathlon.', 'En Olimpia el salto, la jabalina y el disco solo se disputaban dentro del pentatlón.'),
     bi('The Greeks admired the pentathlon because it rewarded versatility across five different events.', 'Los griegos admiraban el pentatlón porque premiaba la versatilidad en cinco pruebas distintas.')],
    bi('Only the sentence about the four naked figures stays with what the painter drew; the others bring in knowledge from the topic (C2).', 'Solo la frase de las cuatro figuras desnudas se queda en lo que dibujó el pintor; las demás aportan conocimiento del tema (C2).')),
   (QC3, [bi('That the scene shows a competition held at Olympia', 'Que la escena muestra una competición de Olimpia'),
     bi('That pentathletes competed naked in this period', 'Que los pentatletas competían desnudos en esta época'),
     bi('That the discus and the javelin were pentathlon events', 'Que el disco y la jabalina eran pruebas del pentatlón'),
     bi('That the amphora is linked to the Panathenaia of Athens', 'Que el ánfora se vincula a las Panateneas de Atenas')],
    bi('Nothing in the image places it at Olympia; as a Panathenaic amphora it is linked to the Panathenaia of Athens.', 'Nada en la imagen la sitúa en Olimpia; como ánfora panatenaica, se vincula a las Panateneas de Atenas.'))]},
 {'img': 'repaso/img/I3-n13.jpg', 'cap': bi("Roman copy of Myron's Discobolus, c. AD 140. National Roman Museum", 'Copia romana del Discóbolo de Mirón, hacia 140 d. C. Museo Nacional Romano'),
  'qs': [
   (QSHOW, [bi("A Roman copy of Myron's Discobolus", 'Una copia romana del Discóbolo de Mirón'),
     bi('Milo of Croton, the sculpture by Pierre Puget', 'Milón de Crotona, la escultura de Pierre Puget'),
     bi('A statue attributed to Koroibos of Elis', 'Una estatua atribuida a Corebo de Élide'),
     bi('A copy of the statue of Zeus at Olympia', 'Una copia de la estatua de Zeus de Olimpia')],
    bi("Roman copy of Myron's Discobolus, c. AD 140. National Roman Museum.", 'Copia romana del Discóbolo de Mirón, hacia 140 d. C. Museo Nacional Romano.')),
   (QC1, [bi('A naked young man twists his trunk forward, right arm stretched back, a disc in his hand.', 'Un joven desnudo gira el tronco hacia delante, con el brazo derecho estirado hacia atrás y un disco en la mano.'),
     bi('The statue records the discus throw (diskos), one of the five events of the ancient pentathlon.', 'La escultura documenta el lanzamiento de disco (diskos), una de las cinco pruebas del pentatlón antiguo.'),
     bi('The thrower stands on the balbis and loads his weight onto his right leg before the release.', 'El lanzador se sitúa en la balbís y carga el peso sobre la pierna derecha antes de soltar.'),
     bi('At Olympia equality was ensured with the three pentathlon discs kept in the sanctuary itself.', 'En Olimpia la igualdad se garantizaba con los tres discos del pentatlón guardados en el santuario.')],
    bi('Only the first sentence stays with the marble: body, pose, arm and disc. Naming the event, the balbis or Olympia is interpretation (C2).', 'Solo la primera frase se queda en el mármol: cuerpo, postura, brazo y disco. Nombrar la prueba, la balbís u Olimpia es interpretar (C2).')),
   (QC3, [bi('That the statue copies a throw seen in a real competition', 'Que la estatua copia un lanzamiento visto en una competición real'),
     bi('That the discus throw was one of the events of the pentathlon', 'Que el lanzamiento de disco era una prueba del pentatlón'),
     bi('That the thrower twisted his trunk to throw the discus', 'Que el lanzador torcía el tronco para lanzar el disco'),
     bi('That Greek discus throwers competed without clothes', 'Que los discóbolos griegos competían sin ropa')],
    bi('It is a Roman copy, c. AD 140, of a work of art: the pose is the one the sculptor chose, not a record of a real throw.', 'Es una copia romana de hacia 140 d. C. de una obra artística: la postura es la que eligió el escultor, no el registro de un lanzamiento real.'))]},
]
for e in EYE:
    for qq, opts, ex in e['qs']:
        add(4, qq, opts, 0, ex, img=e['img'], cap=e['cap'], sec=30, eye=True)

# ---------- Ronda 6 · Tema 2 (reglas del examen) ----------
q2 = D['t2quiz']
bank(5, q2[0])
bank(5, q2[3])
bank(5, q2[1])
bank(5, q2[5])
bank(5, q2[4], opts=[q2[4]['options'][0], q2[4]['options'][1], bi('In the Middle Kingdom, at the time of Beni Hasan', 'En el Imperio Medio, en tiempos de Beni Hasan'), bi('Under Persian rule, in the Late Period', 'Bajo dominio persa, en la Baja Época')])
add(5, bi('What was the kap?', '¿Qué era el kap?'),
    [bi('A palace enclosure where princes and nobles\' sons grew up', 'Un recinto palaciego donde se criaban príncipes e hijos de nobles'),
     bi('A military camp where young peasant recruits were trained', 'Un campamento militar donde se instruía a los reclutas campesinos'),
     bi('A temple school where scribes learnt to read and write', 'Una escuela de templo donde los escribas aprendían a leer'),
     bi('A vaulted gymnasium with a central pit in the bazaar', 'Un gimnasio abovedado con un foso central en el bazar')], 0,
    gl(D['t2gloss'], 'Kap')['def'])
bank(5, q2[9])
bank(5, q2[15], q=bi('What led the Persians to put the education of the young in the hands of the state?', '¿Qué llevó a los persas a poner la educación de los jóvenes en manos del Estado?'))
bank(5, q2[11], opts=[bi('Abbas I', 'Abbás I'), bi('Cyrus II', 'Ciro II'), bi('Darius I', 'Darío I'), bi('Xerxes I', 'Jerjes I')])
glq(5, D['t2gloss'], 'Chovgan', ['Jereed', 'Buzkashi', 'Pahlavan'], q=bi('Which practice matches this definition?', '¿Qué práctica corresponde a esta definición?'))
add(5, bi('Why do we have hardly any record of Phoenician sport?', '¿Por qué apenas tenemos testimonios del deporte fenicio?'),
    [bi('No state, king or common sanctuary wrote it down', 'Ningún Estado, rey ni santuario común lo registró'),
     bi('Their religion forbade displaying the naked body', 'Su religión prohibía exhibir el cuerpo desnudo'),
     bi('They practised only the sports of Egypt', 'Solo practicaban los deportes de Egipto'),
     bi('Their merchants had no time for any leisure', 'Sus mercaderes no tenían tiempo para el ocio')], 0,
    bi('What is missing is above all a type of source, which in no way proves the absence of practice; at Kharayeb we find children with balls, trained dogs and youths with strigils.',
       'Falta sobre todo un tipo de fuente, lo que no prueba la ausencia de práctica; en Kharayeb aparecen niños con pelotas, perros adiestrados y jóvenes con estrígilos.'))

# ---------- Ronda 7 · Tema 3 (reglas del examen) ----------
q3 = T3['quiz']
bank(6, q3[0])
bank(6, q3[1])
bank(6, q3[2], opts=[q3[2]['options'][0], q3[2]['options'][1], q3[2]['options'][2], bi('The great houses', 'Las grandes casas')])
bank(6, q3[5], ex=bi(re.sub(r'judges', 'staff', q3[5]['explain']['en']), re.sub(r'jueces', 'personal', q3[5]['explain']['es'])))
add(6, bi('Who were the judges of the Games, who supervised the candidates for 30 days at Elis?', '¿Quiénes eran los jueces de los Juegos, que supervisaban a los candidatos durante 30 días en Élide?'),
    [bi('The hellanodikai', 'Los helanódicas'), bi('The spondophoroi', 'Los espondóforos'), bi('The gymnasiarchs', 'Los gimnasiarcas'), bi('The mastigophoroi', 'Los mastigóforos')], 0,
    bi('Every candidate lived at Elis for 30 days with his trainer under the supervision of the hellanodikai, the judges of the Games.', 'Cada candidato vivía 30 días en Élide con su entrenador bajo la supervisión de los helanódicas, los jueces de los Juegos.'))
bank(6, q3[6], opts=[q3[6]['options'][0], bi('A diet rich in meat for wrestlers', 'Una dieta rica en carne para luchadores'), q3[6]['options'][2], q3[6]['options'][3]])
bank(6, q3[10], opts=[q3[10]['options'][0], q3[10]['options'][1], bi('All five of the events', 'Las cinco pruebas'), q3[10]['options'][3]])
bank(6, q3[12], q=bi('Which pankratiast died in the Olympic final and was crowned as victor?', '¿Qué pancraciasta murió en la final olímpica y fue coronado vencedor?'))
bank(6, q3[13], q=bi('Which woman was proclaimed Olympic victor in the four-horse chariot race, although women were barred from Olympia?', '¿Qué mujer fue proclamada vencedora olímpica en la cuadriga, aunque las mujeres tenían vetada Olimpia?'),
     opts=[bi('Kyniska, a Spartan princess', 'Cinisca, princesa espartana'), bi('Kallipateira of Rhodes', 'Calipátira de Rodas'), bi('The priestess of Demeter Chamyne', 'La sacerdotisa de Deméter Camine'), bi('A winner of the Heraia', 'Una vencedora de las Hereas')])
src = D['t3sources'][0]; bank(6, src, sec=25, quote=src['text'], opts=[src['options'][0], bi('An Olympic judge crowning a stadion victor with an olive wreath', 'Un juez de Olimpia al coronar con olivo a un vencedor del estadio'), src['options'][2], src['options'][3]])
src = D['t3sources'][5]; bank(6, src, sec=25, quote=src['text'])
bank(6, q3[16], q=bi('Why did the Games at Olympia end, according to current research?', '¿Por qué terminaron los Juegos de Olimpia, según la investigación actual?'),
     opts=[q3[16]['options'][0], bi('Because of a law of Theodosius I that banned pagan cults and festivals in AD 393', 'Por una ley de Teodosio I que prohibió los cultos y fiestas paganos en el 393 d. C.'), q3[16]['options'][2], q3[16]['options'][3]])
src = D['t3sources'][3]; bank(6, src, sec=25, quote=src['text'])

# ---------- Ronda 8 · Final (doble) y relevo ----------
bank(7, D['t1quiz'][0])
bank(7, q2[13], opts=[bi("Because of the horse's head carved on the bow", 'Por la cabeza de caballo tallada en la proa'), bi('Because of their speed', 'Por su velocidad'), bi('Because of their home port', 'Por su puerto de origen'), bi('Because they carried horses for the Assyrian army', 'Porque llevaban caballos para el ejército asirio')])
glq(7, D['t2gloss'], 'Victor perpetuus', ['Pharao ludens', 'Śḫmḫ-ib (sekhemekh-ib)', 'Heb-Sed'], q=bi('Which principle matches this definition?', '¿Qué principio corresponde a esta definición?'))
bank(7, q3[3], opts=[bi("Homer's Iliad", 'La Ilíada de Homero'), q3[3]['options'][1], q3[3]['options'][2], q3[3]['options'][3]])
bank(7, q3[11], opts=[q3[11]['options'][0], bi('By knocking the opponent out', 'Dejando fuera de combate al rival'), q3[11]['options'][2], q3[11]['options'][3]])
glq(7, D['t1gloss'], 'Ethnographic analogy', ['Magic circle', 'Body cultures', 'Labour-war or Marxist theory'])
add(7, bi('How were the Zanes paid for?', '¿Cómo se pagaban los zanes?'),
    [bi('With the fines paid by offenders', 'Con las multas de los infractores'), bi('With ticket sales', 'Con la venta de entradas'), bi('With the treasury of Elis', 'Con el tesoro de Élide'), bi('With donations left by the victors', 'Con donaciones de los vencedores')], 0,
    q3[14]['explain'])
TL = D['timelines']
desert = next(i for tl in TL['1'] for i in tl['items'] if i['label']['en'] == 'Desert kites')
pick = [bi('Pentathlon and wrestling enter Olympia', 'Pentatlón y lucha entran en Olimpia'), bi('Schöningen spears', 'Lanzas de Schöningen'),
        bi('Eruption of the Thera volcano', 'Erupción del volcán de Tera'), bi('First desert kites', 'Primeras cometas del desierto')]
years = [-708, -200000, -1628, desert['year']]
chron = sorted(range(4), key=lambda i: years[i])
S.append({'r': 7, 'k': 'ord', 'q': bi('The relay: tap the four events in chronological order, oldest first.', 'El relevo: toca los cuatro sucesos en orden cronológico, del más antiguo al más reciente.'),
          'opts': pick, 'ans': int(''.join(str(i + 1) for i in chron)),
          'ex': bi('Schöningen spears (c. 200,000 BC) → desert kites (%s) → eruption of Thera (c. 1628 BC) → pentathlon and wrestling at Olympia (708 BC).' % desert['date']['en'],
                   'Lanzas de Schöningen (h. 200.000 a. C.) → cometas del desierto (%s) → erupción de Tera (h. 1628 a. C.) → pentatlón y lucha en Olimpia (708 a. C.).' % desert['date']['es']), 'sec': 40})

# ---------- comprobaciones y salida ----------
S.sort(key=lambda x: x['r'])
for st in S:
    if st['k'] in ('mcq', 'det', 'word'):
        assert len(st['opts']) == 4 and 0 <= st['ans'] < 4, st
js = '/* Clase de repaso en pantalla · 1.º Inglés · Temas 1-3 (generado por tools/repaso_en/build_data.py, v3) */\n'
js += 'const ROUNDS=' + json.dumps(ROUNDS, ensure_ascii=False) + ';\n'
js += 'const STEPS=' + json.dumps(S, ensure_ascii=False) + ';\n'
open(os.path.join(H, 'repaso/clase_en_data.js'), 'w', encoding='utf-8').write(js)
tot = sum((6 if x.get('img') else 5) + x['sec'] + 3 for x in S)
print('pasos', len(S), dict(Counter(x['r'] for x in S)), 'juego puro ≈ %.1f min' % (tot / 60), 'letra correcta', dict(Counter(x['ans'] for x in S if x['k'] != 'ord')))
for st in S:
    if st['k'] in ('mcq', 'det', 'word'):
        L = [len(o['en']) for o in st['opts']]
        if L[st['ans']] == max(L) and L.count(max(L)) == 1: print('LARGA', st['r'], st['q']['en'][:60], L)
