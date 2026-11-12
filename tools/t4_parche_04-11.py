#!/usr/bin/env python3
"""Tema 4, 04-11-2026: ajusta modos, mapa y vídeos de Historiapp al Tema 4 rehecho por Alex (04-11, 95 diapositivas).
Retira lo que ya no está en pantalla (espada de madera, cuerpo del gladiador, apostar y maldecir, crítica a los espectáculos,
Gérôme, delatores, Campania y Foro Boario, auctoramentum, Capua, evergetismo, mappa, naufragia, oficios de la facción, etc.)
y reescribe lo que cambió. Se ejecuta una sola vez sobre las copias de tools/_antes_04-11/ y después tools/t4_integrar.py."""
import json, os, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for f in ('t4_modos.json', 't4_mapa.json', 'videos_t4.json'):
    if os.path.exists('_antes_04-11/' + f): shutil.copy('_antes_04-11/' + f, f)
M = json.load(open('t4_modos.json')); MP = json.load(open('t4_mapa.json')); V = json.load(open('videos_t4.json'))
def E(es, en): return {'es': es, 'en': en}
def find(lst, key, pref):
    r = [x for x in lst if x[key]['es'].startswith(pref)]
    assert len(r) == 1, (key, pref, len(r)); return r[0]
def drop(lst, key, pref): lst.remove(find(lst, key, pref))

# ---------- tarjetas
drop(M['cards'], 'claim', 'La imagen que hoy se tiene del espectáculo de gladiadores')
drop(M['cards'], 'claim', 'Las tablillas de maldición')
drop(M['cards'], 'claim', 'Los moralistas paganos condenaban')
find(M['cards'], 'claim', 'Desde el palco, el emperador')['explain'] = E(
 'El público aprovechaba su presencia para reclamar a gritos lo que necesitaba, como una rebaja del precio del grano o de los impuestos, y el emperador tenía que responder allí mismo ante decenas de miles de testigos, de modo que cada respuesta reforzaba o desgastaba su prestigio.',
 'The public took advantage of his presence to clamour for what it needed, such as a reduction in the price of grain or in taxes, and the emperor had to answer there and then before tens of thousands of witnesses, so each answer strengthened or wore down his prestige.')
find(M['cards'], 'claim', 'El primer combate de gladiadores documentado')['explain'] = E(
 'En un principio el combate era un acto privado y religioso que organizaba la familia del difunto como munus, la obligación de un hijo con su padre muerto, y su fin era honrar al muerto, de ahí su escala reducida, con solo tres parejas en el primero celebrado en Roma, en 264 a. C.',
 "At first the combat was a private and religious act organised by the family of the deceased as a munus, a son's obligation to his dead father, and its purpose was to honour the dead, hence its small scale, with only three pairs in the first one held in Rome, in 264 BC.")
find(M['cards'], 'claim', 'El Ludus Magnus')['explain'] = E(
 'En Roma las grandes escuelas pasaron a ser imperiales, mientras que las privadas pertenecían a un lanista, el empresario que compraba, entrenaba y alquilaba gladiadores, un oficio despreciado porque se lucraba con el cuerpo de otros.',
 'In Rome the great schools became imperial, while private schools belonged to a lanista, the entrepreneur who bought, trained and hired out gladiators, a despised trade because he profited from the bodies of others.')
c = find(M['cards'], 'claim', 'En un combate como el del mosaico de Nennig')
c['claim'] = E('En un combate como el del mosaico de Nennig, un árbitro, el summa rudis, vigilaba el duelo.',
               'In a combat like the one in the Nennig mosaic, a referee, the summa rudis, watched over the duel.')
c['explain'] = E('El duelo duraba entre 10 y 15 minutos según los ensayos de Junkelmann (2000) con réplicas del equipo, y el gladiador que mostraba pasividad o cobardía podía ser azotado o quemado con un hierro al rojo vivo por los incitadores.',
                 "The duel lasted between 10 and 15 minutes according to Junkelmann's (2000) tests with replicas of the equipment, and a gladiator who showed passivity or cowardice could be whipped or burnt with a red-hot iron by the attendants who urged them on.")
find(M['cards'], 'claim', 'Este casco procede del cuartel')['explain'] = E(
 'En el mismo cuartel se conservan además espadas de tipo gladius y una greba alta de tracio.',
 'The same barracks also preserved swords of the gladius type and a high greave of a Thracian.')
c = find(M['cards'], 'claim', 'La inscripción del relieve de Halicarnaso')
c['claim'] = E('La inscripción del relieve de Halicarnaso recuerda que las dos gladiadoras fueron indultadas.',
               'The inscription on the Halicarnassus relief records that the two female gladiators were reprieved.')
c['explain'] = E('Amazona y Achillia luchan a cara descubierta, de modo que el público sabía que eran mujeres, y en el año 200 un decreto imperial prohibió combatir a todas las mujeres.',
                 'Amazon and Achillia fight bare-headed, so the public knew they were women, and in AD 200 an imperial decree forbade all women to fight.')
find(M['cards'], 'claim', 'Los venatores, como el de esta pintura')['explain'] = E(
 'Los venatores eran cazadores profesionales y bien equipados que abatían a las fieras. Quienes morían en la arena eran los condenados a las fieras (damnati ad bestias), siempre humildes, otra de las cuatro modalidades de venatio.',
 'The venatores were professional, well-equipped hunters who killed the beasts. Those who died in the arena were the men condemned to the beasts (damnati ad bestias), always humble people, another of the four forms of venatio.')
find(M['cards'], 'claim', 'En las carreras corrían casi siempre cuadrigas')['explain'] = E(
 'Había también bigas, de dos caballos, y trigas, de tres, y se conocen carreras con hasta diez caballos.',
 'There were also bigae, with two horses, and trigae, with three, and races with up to ten horses are known.')
find(M['cards'], 'claim', 'La palabra factio designaba')['explain'] = E(
 'Las facciones (factiones) eran las empresas que organizaban los equipos de carreras, cada una identificada con un color (blanco, rojo, verde o azul) que vestían sus aurigas. Domiciano añadió durante un tiempo el dorado y el púrpura.',
 'The factions (factiones) were the companies that organised the racing teams, each identified with a colour (white, red, green or blue) worn by its charioteers. Domitian added for a time gold and purple.')
find(M['cards'], 'claim', 'Este mosaico se tomó al principio')['explain'] = E(
 'Junto a la carrera de muchachas de los Juegos Capitolinos y a las luchadoras de la arena, muestra que las mujeres sí compitieron en Roma, aunque casi siempre en contextos privados o como rareza del programa, y con las pruebas del atletismo griego, la carrera, el salto y el disco.',
 "Together with the girls' race at the Capitoline Games and the female fighters of the arena, it shows that women did compete in Rome, although almost always in private settings or as a rarity on the programme, and in the events of Greek athletics, the foot race, the jump and the discus.")

# ---------- glosario
for t in ('Auctoramentum', 'Rudiarius', 'Naufragia', 'Defixio', 'NICA'): drop(M['glossary'], 'term', t)
find(M['glossary'], 'term', 'Summa rudis')['def'] = E('Árbitro del combate de gladiadores, que vigilaba el duelo.', 'Referee of the gladiatorial combat, who watched over the duel.')
find(M['glossary'], 'term', 'Factio')['def'] = E('Empresa que organizaba un equipo de carreras, identificada con un color (blanco, rojo, verde o azul) que vestían sus aurigas.',
                                                  'Company that organised a racing team, identified with a colour (white, red, green or blue) worn by its charioteers.')
g = find(M['glossary'], 'term', 'Summa rudis')
M['glossary'].insert(M['glossary'].index(g) + 1, {'term': E('Rudis', 'Rudis'), 'def': E('Espada de madera que simbolizaba la licencia del gladiador que se retiraba.', 'Wooden sword that symbolised the discharge of a retiring gladiator.'), 'sec': '4.2.3'})

# ---------- cronologías
tr = find(M['timeline'], 'title', 'Roma, de la Monarquía')
for it in list(tr['items']):
    if it['year'] == 395: it['label'] = E('Muerte de Teodosio y división del Imperio en Oriente y Occidente', 'Death of Theodosius and division of the Empire into East and West')
    if it['year'] == 410: tr['items'].remove(it)
    if it['year'] == 476: it['label'] = E('Un jefe germano depone al último emperador y cae el Imperio de Occidente', 'A Germanic chieftain deposes the last emperor and the Western Empire falls')
te = find(M['timeline'], 'title', 'Los espectáculos en Roma')
for it in list(te['items']):
    if it['year'] == -264: it['label'] = E('Primer combate de gladiadores celebrado en Roma, con tres parejas', 'First gladiatorial combat held in Rome, with three pairs')
    if it['year'] in (-65, 107): te['items'].remove(it)
    if it['year'] == -46: it['label'] = E('Primera naumaquia, la de Julio César', 'First naumachia, that of Julius Caesar')
tf = find(M['timeline'], 'title', 'El final de los espectáculos')
tf['items'] = [it for it in tf['items'] if not it['label']['es'].startswith('Tertuliano')]

# ---------- fuentes
s = find(M['sources'], 'text', '«ser quemados')
s.update({'text': E('«hordearii» («comedores de cebada»)', "'hordearii' ('barley-eaters')"),
 'question': E('¿A quiénes se llamaba así y por qué?', 'Who were called this, and why?'),
 'options': [E('A los gladiadores, por su dieta de cebada y legumbres, barata y rica en energía', 'Gladiators, because of their diet of barley and pulses, cheap and rich in energy'),
             E('A los aurigas, por la ración que les daba su facción', 'Charioteers, because of the ration their faction gave them'),
             E('A los legionarios, porque cobraban parte de la paga en grano', 'Legionaries, because part of their pay was in grain'),
             E('A la plebe de Roma, por el grano público que recibía', 'The plebs of Rome, because of the public grain it received')],
 'answer': 0,
 'explain': E('La dieta de los gladiadores se basaba en cebada y legumbres, con poca carne, y los huesos del cementerio de gladiadores de Éfeso la confirman y revelan un aporte de calcio superior al del resto de la ciudad (Lösch et al., 2014).',
              "The gladiators' diet was based on barley and pulses, with little meat, and the bones from the gladiator cemetery at Ephesus confirm it and reveal a calcium intake higher than that of the rest of the city (Lösch et al., 2014).")})
for p in ('«no puedan correr', '«NICA»', '«¡Mátalo'): drop(M['sources'], 'text', p)

# ---------- relacionar
for p in find(M['match'], 'title', 'Ludi y munera')['pairs']:
    if p['a']['es'] == 'Edicta munerum': p.update({'a': E('Munera gladiatoria', 'Munera gladiatoria'), 'b': E('Nombre que acabaron recibiendo todos los combates de gladiadores en los anfiteatros', 'Name eventually given to all gladiatorial combats in the amphitheatres')})
for p in find(M['match'], 'title', 'Palabras de la carrera del gladiador')['pairs']:
    if p['a']['es'] == 'Auctoramentum': p.update({'a': E('Ludus', 'Ludus'), 'b': E('Escuela de gladiadores, a la vez cuartel, centro de entrenamiento y negocio', 'Gladiatorial school, at once barracks, training centre and business')})
for p in find(M['match'], 'title', 'El circo, el edificio y la carrera')['pairs']:
    if p['a']['es'] == 'Mappa': p.update({'a': E('Porta triumphalis', 'Porta triumphalis'), 'b': E('Puerta triunfal, en el extremo curvo', 'Triumphal gate, at the curved end')})
    elif p['a']['es'] == 'Naufragia': p.update({'a': E('Cuadriga', 'Quadriga'), 'b': E('Carro de cuatro caballos, el más habitual en las carreras', 'Four-horse chariot, the most common in the races')})
find(M['match'], 'title', 'Los oficios de una facción').update({'title': E('Las facciones y sus aurigas', 'The factions and their charioteers'), 'pairs': [
 {'a': E('Factiones', 'Factiones'), 'b': E('Empresas que organizaban los equipos de carreras', 'Companies that organised the racing teams')},
 {'a': E('Dominus factionis', 'Dominus factionis'), 'b': E('Dueño de la facción, un caballero con cientos de empleados', 'Owner of the faction, an eques with hundreds of employees')},
 {'a': E('Stabula', 'Stabula'), 'b': E('Cuadras de la facción en Roma', "The faction's stables in Rome")},
 {'a': E('Miliarios', 'Miliarii'), 'b': E('Aurigas que alcanzaron las mil victorias', 'Charioteers who reached a thousand victories')},
 {'a': E('Diocles', 'Diocles'), 'b': E('Liberto de Lusitania, quizá el deportista mejor pagado de la historia', 'Freedman from Lusitania, perhaps the best-paid sportsman in history')}]})

# ---------- verdadero o falso
find(M['myths'], 'claim', 'Tito y Trajano').update({'claim': E('El emperador evitaba asistir a los juegos que pagaba y los dejaba en manos de los magistrados.', 'The emperor avoided attending the games he paid for and left them in the hands of the magistrates.'), 'answer': False,
 'explain': E('El emperador asistía en persona a los juegos que pagaba, y desde el palco ejercía tres papeles, el de editor, el de intermediario entre la ciudad y los dioses y el de árbitro que concedía o negaba lo que se le pedía, de modo que los juegos fueron el principal lugar en el que emperador y pueblo se encontraban cara a cara.',
              'The emperor attended in person the games he paid for, and from the imperial box he played three roles, that of editor, that of intermediary between the city and the gods and that of arbiter who granted or refused what was asked of him, so the games were the main place where emperor and people met face to face.')})
find(M['myths'], 'claim', 'Todos los gladiadores eran esclavos')['explain'] = E(
 'Los gladiadores procedían de tres grupos, pues junto a los esclavos, comprados o alquilados por sus dueños, había condenados, ad gladium o ad ludum, y hombres libres que se vendían voluntariamente a un lanista, empujados por las deudas o la desesperación.',
 'Gladiators came from three groups, since alongside slaves, bought or hired out by their owners, there were the condemned, ad gladium or ad ludum, and free men who sold themselves voluntarily to a lanista, driven by debt or despair.')
find(M['myths'], 'claim', 'Todo gladiador acababa muriendo')['explain'] = E(
 'Los epitafios dan de media de diez a quince combates por gladiador y, para el siglo I d. C., Ville (1981) calcula unas diecinueve muertes por cada cien combates. La retirada llegaba con la rudis, que simbolizaba la licencia, o con la libertad, y algunos veteranos, atraídos por la fama y el dinero, volvían a combatir.',
 'Epitaphs give an average of ten to fifteen combats per gladiator and, for the 1st century AD, Ville (1981) calculates some nineteen deaths per hundred combats. Retirement came with the rudis, which symbolised discharge, or with freedom, and some veterans, drawn by fame and money, returned to fight.')
find(M['myths'], 'claim', 'El término gladiatrix').update({'claim': E('Las mujeres no llegaron a combatir nunca en la arena romana.', 'Women never fought in the Roman arena.'), 'answer': False,
 'explain': E('Las mujeres humildes sí llegaron a combatir, aunque siempre como una rareza del programa, ya que las fuentes literarias las mencionan menos de diez veces hasta el año 200 d. C., y el relieve de Halicarnaso muestra a Amazona y Achillia luchando a cara descubierta.',
              'Humble women did fight, although always as a rarity on the programme, since the literary sources mention them fewer than ten times up to AD 200, and the Halicarnassus relief shows Amazon and Achillia fighting bare-headed.')})
find(M['myths'], 'claim', 'Los gladiadores formaban familias')['explain'] = E(
 'A pesar del impedimento legal de contraer matrimonio, en Hispania un 40 % de los gladiadores fallecidos conocidos tenía mujer, cuya procedencia en la mayoría de los casos era libre o liberta.',
 'Despite the legal bar on marriage, in Hispania 40% of the known dead gladiators had a wife, who in most cases was freeborn or a freedwoman.')
find(M['myths'], 'claim', 'El mosaico de las «muchachas en bikini»')['explain'] = E(
 'La escena se lee hoy como una competición atlética (Pensabene y Gallocchio, 2011) y, junto a la carrera de muchachas de los Juegos Capitolinos y a las luchadoras de la arena, muestra que las mujeres sí compitieron en Roma, aunque casi siempre en contextos privados o como rareza del programa.',
 "The scene is read today as an athletic competition (Pensabene & Gallocchio, 2011) and, together with the girls' race at the Capitoline Games and the female fighters of the arena, it shows that women did compete in Rome, although almost always in private settings or as a rarity on the programme.")

# ---------- test
q = find(M['quiz'], 'q', '¿Qué hacía el público ante el emperador')
q['q'] = E('¿Qué hacía el público aprovechando la presencia del emperador en los juegos?', "What did the public do, taking advantage of the emperor's presence at the games?")
q['options'][q['answer']] = E('Reclamar a gritos lo que necesitaba, como una rebaja del precio del grano o de los impuestos', 'Clamour for what it needed, such as a reduction in the price of grain or in taxes')
q['explain'] = E('El emperador tenía que responder allí mismo ante decenas de miles de testigos, y cada respuesta reforzaba o desgastaba su prestigio, de modo que los juegos se convirtieron en un espacio de comunicación política entre el emperador y el pueblo.',
                 'The emperor had to answer there and then before tens of thousands of witnesses, and each answer strengthened or wore down his prestige, so the games became a space of political communication between the emperor and the people.')
find(M['quiz'], 'q', '¿De dónde llegaron a Roma los combates').update({'q': E('¿Qué carácter tuvieron en un principio los combates de gladiadores en Roma?', 'What was the original character of gladiatorial combats in Rome?'),
 'options': [E('Un acto privado y religioso, organizado por la familia del difunto para honrarlo', 'A private and religious act, organised by the family of the deceased to honour him'),
             E('Un espectáculo del emperador para celebrar las victorias militares', 'A spectacle given by the emperor to celebrate military victories'),
             E('Un arma electoral de los candidatos a las magistraturas', 'An electoral weapon of the candidates for office'),
             E('Un entrenamiento de las legiones abierto al público', 'Training for the legions open to the public')], 'answer': 0,
 'explain': E('Lo organizaba la familia del difunto como munus, la obligación de un hijo con su padre muerto, de ahí su escala reducida, como muestran las tres parejas del primer combate celebrado en Roma, en 264 a. C. Después pasó a exhibir el prestigio del linaje, fue arma electoral en el siglo I a. C. y, con el Imperio, competencia exclusiva del emperador.',
              "It was organised by the family of the deceased as a munus, a son's obligation to his dead father, hence its small scale, as the three pairs of the first combat held in Rome, in 264 BC, show. Later it came to display the prestige of the lineage, was an electoral weapon in the 1st century BC and, under the Empire, the exclusive preserve of the emperor.")})
find(M['quiz'], 'q', '¿Qué consecuencias legales tenía la infamia')['explain'] = E(
 'La infamia era una mancha legal y moral que el derecho imponía a quienes vendían o exhibían su cuerpo para el disfrute de otros, aunque no estaba reñida con la admiración popular, y el pueblo trataba al gladiador como a un héroe «a la vez famoso e infame» (Bell, 2020).',
 "Infamia was a legal and moral stain that the law imposed on those who sold or displayed their bodies for the enjoyment of others, although it was not at odds with popular admiration, and the people treated the gladiator as a hero 'at once famous and infamous' (Bell, 2020).")
find(M['quiz'], 'q', '¿Cómo era la relación económica entre el gladiador').update({'q': E('Según la ley de 177 d. C., ¿qué parte de lo que cobraba el lanista por un combate correspondía al gladiador?', 'Under the law of AD 177, what share of what the lanista was paid for a combat went to the gladiator?'),
 'options': [E('La cuarta parte si era libre y la quinta si era esclavo', 'A quarter if he was free and a fifth if he was a slave'),
             E('La mitad, fuera libre o esclavo', 'Half, whether he was free or a slave'),
             E('Nada, porque todo el dinero era del lanista', 'Nothing, because all the money belonged to the lanista'),
             E('Todo, porque el lanista cobraba aparte del editor', 'All of it, because the lanista was paid separately by the editor')], 'answer': 0,
 'explain': E('Si volvía vivo, el editor pagaba al lanista solo un alquiler, en torno a una quinta parte de lo que valía el gladiador, y de ese dinero la ley reservaba al gladiador la cuarta parte si era libre y la quinta si era esclavo, unos 600-750 sestercios por combate en el caso de uno de primera.',
              'If he came back alive, the editor paid the lanista only a hire fee, around a fifth of what the gladiator was worth, and of that money the law reserved for the gladiator a quarter if he was free and a fifth if he was a slave, some 600-750 sesterces per combat in the case of a first-class gladiator.')})
find(M['quiz'], 'q', '¿Por qué pagaba un rico el coste de un munus').update({'q': E('¿Con qué fin último pagaba el editor el coste de un munus?', 'What was the ultimate aim of the editor in paying for a munus?'),
 'options': [E('Lograr el reconocimiento del público ofreciéndole ocio y distracción gratuitos', 'To win the recognition of the public by offering it free leisure and entertainment'),
             E('Recuperar el gasto con los impuestos de las provincias', 'To recover the outlay through provincial taxes'),
             E('Cobrar una parte de los premios de los gladiadores', "To collect a share of the gladiators' prizes"),
             E('Cumplir una ley que le obligaba a dar juegos cada año a toda la plebe', 'To comply with a law obliging him to give games to the whole plebs every year')], 'answer': 0,
 'explain': E('El dinero salía de la summa honoraria, la cantidad fija que cada magistrado entregaba a la ciudad al tomar posesión de su cargo y que solía gastarse en juegos, de lo que el editor ponía de su bolsillo y, a veces, de los fondos públicos.',
              'The money came from the summa honoraria, the fixed sum that each magistrate paid to the city on taking up office and that was usually spent on games, from what the editor added out of his own pocket and, at times, from public funds.')})
find(M['quiz'], 'q', '¿Qué simbolizaba la rudis')['explain'] = E(
 'La retirada llegaba con la rudis, que simbolizaba la licencia, o con la libertad, y algunos veteranos siguieron en el mundo de la arena como árbitros, instructores o incluso lanistas, mientras que otros, atraídos por la fama y el dinero, volvían a combatir.',
 'Retirement came with the rudis, which symbolised discharge, or with freedom, and some veterans remained in the world of the arena as referees, instructors or even lanistae, while others, drawn by fame and money, returned to fight.')
q = find(M['quiz'], 'q', '¿Con qué se pagó el Anfiteatro Flavio')
q['options'][q['answer']] = E('Con el botín de la guerra de Judea y el saqueo del templo de Jerusalén', 'With the spoils of the Judaean war and the plunder of the Temple in Jerusalem')
find(M['quiz'], 'q', '¿Qué eran las facciones del circo')['explain'] = E(
 'Cada facción se identificaba con un color que vestían sus aurigas, y al frente estaba su dueño, el dominus factionis, un caballero que dirigía a varios cientos de empleados.',
 'Each faction was identified with a colour worn by its charioteers, and at its head was its owner, the dominus factionis, an eques who ran several hundred employees.')
find(M['quiz'], 'q', '¿Por qué los dueños de las facciones').update({'q': E('¿Cómo competía una facción en la pista?', 'How did a faction compete on the track?'),
 'options': [E('Como un equipo, con hasta tres carros por carrera que se ayudaban entre sí', 'As a team, with up to three chariots per race that helped one another'),
             E('Con un solo carro por carrera, sorteado entre sus aurigas', 'With a single chariot per race, drawn by lot among its charioteers'),
             E('Con aurigas alquilados a las otras facciones', 'With charioteers hired from the other factions'),
             E('Con carros de colores distintos para confundir a los rivales', 'With chariots of different colours to confuse its rivals')], 'answer': 0,
 'explain': E('Uno de los carros buscaba la victoria y los otros le marcaban el ritmo o cerraban el paso a los rivales en la cuerda y en los giros, y por eso las inscripciones de los aurigas distinguen entre ganar en cabeza, remontar desde atrás o arrebatar la victoria en la última recta.',
              "One of the chariots went for victory and the others set the pace for him or blocked the rivals on the inside line and at the turns, which is why the charioteers' inscriptions distinguish between winning from the front, coming from behind or snatching victory in the final straight.")})

# ---------- mapa conceptual
def nodo(code, t):
    r = [x for x in MP['ramas'] if x['code'] == code][0]
    n = [x for x in r['nodos'] if x['t']['es'] == t]; assert len(n) == 1, (code, t); return r, n[0]
def X(*items): return {'es': [{'k': k, 'v': es} for k, es, en in items], 'en': [{'k': k, 'v': en} for k, es, en in items]}
def setx(n, i, k, es, en): n['x']['es'][i] = {'k': k, 'v': es}; n['x']['en'][i] = {'k': k, 'v': en}
def delx(n, i): del n['x']['es'][i]; del n['x']['en'][i]
r, n = nodo('4.1', 'El phersu y el legado a Roma'); n['fs'] = ['el-phersu' if f == 'el-phersu-y-los-gladiadores' else f for f in n['fs']]
r, n = nodo('4.2.1', 'Monarquía, República e Imperio')
i = [j for j, x in enumerate(n['x']['es']) if 'Arcadio' in x['v']][0]
setx(n, i, 'concepto', 'A la muerte de Teodosio, en 395 d. C., el Imperio quedó dividido en Oriente y Occidente, porque un territorio tan extenso resultaba muy difícil de gobernar desde un solo centro, y la mitad occidental cayó en 476 d. C., mientras que la oriental, con capital en Constantinopla, siguió en pie casi mil años más.',
 'On the death of Theodosius, in AD 395, the Empire was divided into East and West, because such a vast territory was very difficult to govern from a single centre, and the western half fell in AD 476, while the eastern half, with its capital at Constantinople, survived for almost a thousand years more.')
r, n = nodo('4.2.2', 'Del agón al ludus'); delx(n, [j for j, x in enumerate(n['x']['es']) if 'Gérôme' in x['v']][0])
r, n = nodo('4.2.2', 'El emperador en la grada')
n['d'] = E('La presencia del emperador formaba parte del espectáculo, porque desde el palco ejercía tres papeles, el de editor, el de intermediario entre la ciudad y los dioses y el de árbitro, y los juegos se convirtieron en el principal lugar en el que emperador y pueblo se encontraban cara a cara.',
           'The emperor\'s presence was part of the spectacle, because from the imperial box he played three roles, that of editor, that of intermediary between the city and the gods and that of arbiter, and the games became the main place where emperor and people met face to face.')
setx(n, 0, 'concepto', 'El público aprovechaba la presencia del emperador para reclamar a gritos lo que necesitaba, como una rebaja del precio del grano o de los impuestos, y él tenía que responder allí mismo ante decenas de miles de testigos.',
 "The public took advantage of the emperor's presence to clamour for what it needed, such as a reduction in the price of grain or in taxes, and he had to answer there and then before tens of thousands of witnesses.")
setx(n, 1, 'concepto', 'Cada respuesta reforzaba o desgastaba su prestigio, de modo que los juegos fueron un espacio de comunicación política entre el emperador y el pueblo.',
 'Each answer strengthened or wore down his prestige, so the games were a space of political communication between the emperor and the people.')
r, n = nodo('4.2.3', 'Del funeral aristocrático al espectáculo imperial')
n['d'] = E('Los combates de gladiadores pasaron de ser un acto privado y religioso de la familia del difunto a exhibir el prestigio del linaje, fueron arma electoral en el siglo I a. C. y, con el Imperio, competencia exclusiva del emperador, que los usó para celebrar sus victorias.',
           'Gladiatorial combats went from being a private and religious act of the family of the deceased to displaying the prestige of the lineage, were an electoral weapon in the 1st century BC and, under the Empire, became the exclusive preserve of the emperor, who used them to celebrate his victories.')
n['x'] = X(('ejemplo', 'El primer combate celebrado en Roma, en 264 a. C., tuvo solo tres parejas, porque su fin era honrar al muerto.', 'The first combat held in Rome, in 264 BC, had only three pairs, because its purpose was to honour the dead.'),
           ('concepto', 'Los herederos aplazaban y agrandaban los munera, ya que un funeral espectacular mostraba a toda la ciudad la riqueza y el rango de la familia.', 'Heirs postponed the munera and made them bigger, since a spectacular funeral showed the whole city the wealth and rank of the family.'),
           ('concepto', 'En el siglo I a. C. los magistrados y los candidatos los financiaban para ganarse el voto, y el Senado tuvo que limitar el número de gladiadores y prohibir los combates en vísperas de las elecciones.', 'In the 1st century BC magistrates and candidates paid for them to win votes, and the Senate had to limit the number of gladiators and forbid combats on the eve of elections.'),
           ('concepto', 'Una vez que el pueblo dejó de votar, los grandes combates fueron competencia exclusiva del emperador y celebraban las victorias militares y los acontecimientos de la dinastía.', 'Once the people no longer voted, the great combats became the exclusive preserve of the emperor and celebrated military victories and the events of the dynasty.'))
r, n = nodo('4.2.3', 'Quiénes eran los gladiadores')
n['fs'] = ['los-gladiadores-y-la-infamia', 'la-vida-de-los-gladiadores', 'esposas-companeros-y-retirada']
n['d'] = E('Esclavos, condenados y hombres libres que se vendían a un lanista compartían la infamia, una mancha legal y moral que no estaba reñida con la admiración popular, y vivían y entrenaban en el ludus, una escuela que era a la vez cuartel, centro de entrenamiento y negocio.',
           'Slaves, the condemned and free men who sold themselves to a lanista shared infamia, a legal and moral stain that was not at odds with popular admiration, and lived and trained in the ludus, a school that was at once barracks, training centre and business.')
setx(n, 0, 'concepto', 'El infame no podía votar, ocupar una magistratura, testificar en un juicio ni contraer un matrimonio legal.', 'The infamis could not vote, hold a magistracy, testify in a trial or contract a legal marriage.')
setx(n, 2, 'ejemplo', 'En Hispania, un 40 % de los gladiadores fallecidos conocidos tenía mujer, en la mayoría de los casos libre o liberta.', 'In Hispania, 40% of the known dead gladiators had a wife, in most cases freeborn or a freedwoman.')
r, n = nodo('4.2.3', 'La jornada del munus y los tipos de gladiador')
n['fs'] = [f for f in n['fs'] if f != 'la-espada-de-madera']
i = [j for j, x in enumerate(n['x']['es']) if 'Ulpiano' in x['v']][0]
setx(n, i, 'concepto', 'La retirada llegaba con la rudis, la espada de madera que simbolizaba la licencia, o con la libertad, y algunos veteranos siguieron como árbitros, instructores o incluso lanistas.',
 'Retirement came with the rudis, the wooden sword that symbolised discharge, or with freedom, and some veterans carried on as referees, instructors or even lanistae.')
r, n = nodo('4.2.3', 'Mujeres, cacerías y naumaquias')
i = [j for j, x in enumerate(n['x']['es']) if '11.000' in x['v']][0]
setx(n, i, 'ejemplo', 'En la inauguración del Coliseo, en 80 d. C., murieron 5.000 animales en un solo día.', 'At the inauguration of the Colosseum, in AD 80, 5,000 animals died in a single day.')
i = [j for j, x in enumerate(n['x']['es']) if 'Fucino' in x['v']][0]
setx(n, i, 'ejemplo', 'En la naumaquia de Claudio en el lago Fucino (52 d. C.) lucharon 19.000 hombres, y en ninguna de las conocidas combatió una flota romana, algo que Coleman (1993) atribuye al riesgo de que Roma perdiera, aunque fuera de mentira.',
 "In Claudius' naumachia on the Fucine Lake (AD 52) 19,000 men fought, and in none of the known ones did a Roman fleet fight, something Coleman (1993) attributes to the risk that Rome might lose, even in make-believe.")
r, n = nodo('4.2.4', 'El circo y el Circo Máximo')
i = [j for j, x in enumerate(n['x']['es']) if 'Olimpia' in x['v']][0]
setx(n, i, 'concepto', 'Fuera de Roma se conocen menos de sesenta circos, y junto al anfiteatro y al teatro formaba la tríada de grandes edificios que una ciudad importante debía tener para entretener al pueblo.',
 'Fewer than sixty circuses are known outside Rome, and together with the amphitheatre and the theatre the circus formed the triad of great buildings that an important city had to have to entertain the people.')
r, n = nodo('4.2.4', 'La carrera de carros')
for j, x in enumerate(list(n['x']['es'])):
    if 'arrastrado' in x['v']: setx(n, j, 'concepto', 'El auriga conducía con las riendas atadas a la cintura, de modo que dominaba el carro con el peso del cuerpo, y llevaba un cuchillo para cortarlas si volcaba, además de un casco acolchado, una túnica con bandas de cuero en el pecho, vendas en las piernas y botas altas de cuero.',
        'The charioteer drove with the reins tied round his waist, so that he controlled the chariot with the weight of his body, and carried a knife to cut them if he overturned, as well as a padded helmet, a tunic with leather bands across the chest, bandages on the legs and high leather boots.')
    if 'mappa' in x['v']: setx(n, j, 'ejemplo', 'Quien pagaba los juegos daba la salida dejando caer un pañuelo blanco desde una tribuna sobre las carceres, dispuestas en arco para que ningún carro partiera con ventaja.',
        'Whoever paid for the games gave the start by dropping a white cloth from a platform above the carceres, which were arranged in an arc so that no chariot started with an advantage.')
    if '35 km/h' in x['v']: setx(n, j, 'concepto', 'Se daban siete vueltas, unos 5 km, en ocho o nueve minutos, y las bigas alcanzarían 40-45 km/h y las cuadrigas hasta 60 km/h.',
        'The race was seven laps, some 5 km, in eight or nine minutes, and bigae would reach 40-45 km/h and quadrigae up to 60 km/h.')
r, n = nodo('4.2.4', 'Las facciones')
n['d'] = E('Las facciones eran empresas identificadas con un color que organizaban los equipos de carreras, dirigidas por un caballero con varios cientos de empleados, y en la pista competían como un equipo.',
           'The factions were companies identified with a colour that organised the racing teams, run by an eques with several hundred employees, and on the track they competed as a team.')
n['x'] = X(('concepto', 'Cada facción se identificaba con el blanco, el rojo, el verde o el azul, que vestían sus aurigas, y Domiciano añadió durante un tiempo el dorado y el púrpura.', 'Each faction was identified with white, red, green or blue, worn by its charioteers, and Domitian added for a time gold and purple.'),
           ('concepto', 'Al frente estaba el dominus factionis, un caballero que dirigía a varios cientos de empleados, desde quienes cuidaban, sujetaban o alimentaban a los caballos hasta veterinarios, mecánicos y carpinteros.', 'At the head was the dominus factionis, an eques who ran several hundred employees, from those who looked after, held or fed the horses to vets, mechanics and carpenters.'),
           ('ejemplo', 'La facción mantenía sus cuadras (stabula) en Roma, abastecidas por yeguadas de Hispania, Sicilia, Tesalia, el norte de África y Capadocia, y en los últimos siglos del Imperio pasó al control del emperador.', 'The faction kept its stables (stabula) in Rome, supplied by stud farms in Hispania, Sicily, Thessaly, North Africa and Cappadocia, and in the last centuries of the Empire it came under the control of the emperor.'),
           ('concepto', 'Cada facción podía inscribir hasta tres carros por carrera, de modo que uno buscaba la victoria y los otros le marcaban el ritmo o cerraban el paso a los rivales.', 'Each faction could enter up to three chariots in a race, so that one went for victory and the others set the pace for him or blocked the rivals.'))
r, n = nodo('4.2.4', 'Los aurigas y su fortuna')
for j, x in enumerate(list(n['x']['es'])):
    if x['v'].startswith('Diocles'): setx(n, j, 'ejemplo', 'Diocles, un liberto de Lusitania, corrió de 122 a 146 d. C. en 4.257 carreras, con 1.462 victorias, y su inscripción recoge que gracias a él su facción ganó 35.863.120 sestercios en premios.',
        'Diocles, a freedman from Lusitania, raced from AD 122 to 146 in 4,257 races, with 1,462 victories, and his inscription records that thanks to him his faction won 35,863,120 sesterces in prizes.')
    if x['v'].startswith('Vamplew'): setx(n, j, 'autor', 'A Diocles le llegó una décima parte, unos tres millones y medio (Vamplew, 2023), casi 3.000 años de paga de un legionario, y Bell (2014) lo considera quizá el deportista mejor pagado de la historia.',
        "Diocles received a tenth of it, some three and a half million (Vamplew, 2023), almost 3,000 years of a legionary's pay, and Bell (2014) considers him perhaps the best-paid sportsman in history.")
    if x['v'].startswith('Crescens'): setx(n, j, 'ejemplo', 'Crescens ganó su primera carrera a los trece años y murió a los veintidós, y Escorpo murió a los veintisiete con más de dos mil victorias.',
        'Crescens won his first race at thirteen and died at twenty-two, and Scorpus died at twenty-seven after more than two thousand victories.')
r, n = nodo('4.2.4', 'Apostar y maldecir'); r['nodos'].remove(n)
r, n = nodo('4.2.5', 'El recorrido del bañista')
n['d'] = E('El bañista dejaba la ropa en el apodyterium, hacía ejercicio en la palestra, sudaba en el laconicum y pasaba por el caldarium, el tepidarium y el frigidarium.',
           'The bather left his clothes in the apodyterium, exercised in the palaestra, sweated in the laconicum and went through the caldarium, the tepidarium and the frigidarium.')
setx(n, 0, 'concepto', 'La ropa se dejaba en pequeños nichos del apodyterium, el vestuario, vigilados por un esclavo.', 'Clothes were left in small niches in the apodyterium, the changing room, watched over by a slave.')
r, n = nodo('4.2.5', 'El deporte femenino')
n['d'] = E('El ejercicio de la mujer fuera de casa se tenía por impropio, y el mosaico de las «muchachas en bikini» de Piazza Armerina, junto a la carrera de muchachas de los Juegos Capitolinos y a las luchadoras de la arena, muestra que las mujeres sí compitieron en Roma, aunque casi siempre en contextos privados o como rareza del programa.',
           "Women's exercise outside the home was considered improper, and the «girls in bikinis» mosaic at Piazza Armerina, together with the girls' race at the Capitoline Games and the female fighters of the arena, shows that women did compete in Rome, although almost always in private settings or as a rarity on the programme.")
i = [j for j, x in enumerate(n['x']['es']) if 'conocía desde hacía siglos' in x['v']][0]
setx(n, i, 'concepto', 'Sus pruebas eran las del atletismo griego, la carrera, el salto y el disco.', 'Their events were those of Greek athletics, the foot race, the jump and the discus.')
r, n = nodo('4.2.6', 'Dos críticas')
n.update({'t': E('Los críticos de los espectáculos', 'The critics of the spectacles'), 'f': 'como-se-apagaron-los-espectaculos', 'fs': ['como-se-apagaron-los-espectaculos'],
 'd': E('Los moralistas paganos, como Cicerón y Séneca, condenaban la crueldad con quien no podía defenderse y pedían al hombre culto que no se dejara arrastrar por la masa, y los escritores cristianos, como Tertuliano, rechazaban los espectáculos por idolatría.',
        'Pagan moralists, such as Cicero and Seneca, condemned cruelty towards those who could not defend themselves and urged the educated man not to let himself be carried away by the crowd, and Christian writers, such as Tertullian, rejected the spectacles as idolatry.'),
 'x': X(('concepto', 'Los moralistas paganos condenaban la crueldad con quien no podía defenderse y pedían al hombre culto que no se dejara arrastrar por la masa.', 'Pagan moralists condemned cruelty towards those who could not defend themselves and urged the educated man not to let himself be carried away by the crowd.'),
        ('concepto', 'Los escritores cristianos los rechazaban por idolatría, ya que todo en ellos estaba consagrado a los dioses paganos.', 'Christian writers rejected them as idolatry, since everything in them was consecrated to the pagan gods.'),
        ('autor', 'Jiménez Sánchez (2002) juzga exagerado el peso del cristianismo en el final de los espectáculos y pone por delante el coste, y Stocking (2021) coincide en que no fue la causa principal.', 'Jiménez Sánchez (2002) considers the weight of Christianity in the end of the spectacles exaggerated and puts cost first, and Stocking (2021) agrees that it was not the main cause.'))})
r, n = nodo('4.2.6', 'Las funciones del deporte romano y su herencia')
for j, x in enumerate(list(n['x']['es'])):
    if 'evergetismo' in x['v']: setx(n, j, 'concepto', 'Servía al poder porque la élite ofrecía los juegos gratuitos a la plebe para ganarse su favor, el rico recibía reconocimiento y el emperador se mostraba en la grada como quien daba los juegos.',
        'It served power because the elite offered free games to the plebs to win its favour, the rich man received recognition and the emperor showed himself in the stands as the one who gave the games.')
    if 'asociaciones' in x['v']: setx(n, j, 'concepto', 'Era un rito, puesto que los ludi pertenecían al calendario religioso y el circo siguió siendo un espacio sagrado, y el ejercicio cotidiano servía a la salud en las termas, abiertas a cualquiera por un precio simbólico, y en los juegos de pelota, cuyos beneficios defendió Galeno.',
        'It was a rite, since the ludi belonged to the religious calendar and the circus remained a sacred space, and everyday exercise served health in the baths, open to anyone for a token price, and in ball games, whose benefits Galen defended.')

# ---------- vídeos: fuera los dos cuyo contenido ya no está en el PPT (los ficheros se conservan)
V = [v for v in V if v['id'] not in ('t4_11', 't4_14')]

json.dump(M, open('t4_modos.json', 'w'), ensure_ascii=False, indent=1)
json.dump(MP, open('t4_mapa.json', 'w'), ensure_ascii=False, indent=1)
json.dump(V, open('videos_t4.json', 'w'), ensure_ascii=False, indent=1)
print('modos', {k: len(v) for k, v in M.items()}, 'mapa', sum(len(r['nodos']) for r in MP['ramas']), 'vídeos', len(V))
