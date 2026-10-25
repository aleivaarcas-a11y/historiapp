#!/usr/bin/env python3
"""Tema 4: palabras del día (wordle) en el bloque WORDS de index.html y copia en tools/wordle_palabras.js (25-10-2026).
Todas las palabras y definiciones salen del texto de pantalla del Tema 4 y del Topic 4."""
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
ES = [("ARENA", "Cubría el espacio central del anfiteatro (harena) y dio nombre al lugar de los combates."),
 ("CIRCO", "Recinto de las carreras de carros, con las carceres en el extremo recto y la spina en el eje."),
 ("MUNUS", "Significaba a la vez «deber» y «regalo»; el combate de gladiadores que un particular ofrecía al pueblo."),
 ("LUDUS", "El juego ofrecido al público, frente al agón griego, y también la escuela de gladiadores a cargo de un lanista."),
 ("RUDIS", "Espada de madera que servía para entrenar y simbolizaba la licencia del gladiador."),
 ("MAPPA", "Pañuelo blanco que dejaba caer quien pagaba los juegos para dar la salida de la carrera."),
 ("SPINA", "Muro bajo que corría por el eje del circo y dividía la pista en dos."),
 ("TERMAS", "Casas de baño en las que también se hacía ejercicio; la entrada costaba un cuadrante."),
 ("FOLLIS", "Pelota grande de piel inflada, muy ligera, propia de niños y ancianos."),
 ("PHERSU", "Enmascarado de la Tumba de los Augures; su nombre significa probablemente «máscara»."),
 ("AURIGA", "Conductor del carro; en Roma, esclavo, liberto o romano de muy baja condición."),
 ("FLAUTA", "La del músico que acompaña casi siempre al pugilato etrusco y que, según Thuillier, marcaba el ritmo."),
 ("LANISTA", "Empresario que compraba, entrenaba y alquilaba gladiadores."),
 ("INFAMIA", "Mancha legal y moral de quien vendía o exhibía su cuerpo para el disfrute de otros."),
 ("FACCION", "Empresa identificada con un color que organizaba los equipos de carreras del circo."),
 ("DIOCLES", "Liberto de Lusitania que corrió de 122 a 146 d. C. y ganó 1.462 de sus 4.257 carreras."),
 ("ETRURIA", "Primera gran civilización de la península itálica, organizada en doce ciudades-estado.")]
EN = [("ARENA", "The sand (harena) covering the centre of the amphitheatre, which gave its name to the place of combat."),
 ("CIRCUS", "The venue for chariot races, with the carceres at the straight end and the spina along its axis."),
 ("MUNUS", "It meant both «duty» and «gift»; the gladiatorial combat a private individual offered to the people."),
 ("RUDIS", "Wooden sword used for training, the symbol of a gladiator's discharge."),
 ("MAPPA", "White cloth dropped by whoever paid for the games to start the race."),
 ("BATHS", "The thermae, where bathing was combined with exercise; entry cost a quadrans."),
 ("FOLLIS", "Large ball of inflated skin, very light, suited to children and the elderly."),
 ("PHERSU", "Masked figure in the Tomb of the Augurs; the name probably means «mask»."),
 ("LANISTA", "Entrepreneur who bought, trained and hired out gladiators."),
 ("INFAMIA", "Legal and moral stain on those who sold or displayed their bodies for the enjoyment of others."),
 ("FACTION", "Company identified with a colour that organised the racing teams of the circus."),
 ("DIOCLES", "Freedman from Lusitania who raced from AD 122 to 146 and won 1,462 of his 4,257 races.")]
h = open('index.html', encoding='utf-8').read()
a = h.index('const WORDS={'); b = h.index(']};', a) + 3
blk = h[a:b]
if ',t:4,' not in blk:
    es = ''.join(f',\n {{w:"{w}",t:4,d:{json.dumps(d, ensure_ascii=False)}}}' for w, d in ES)
    i = blk.index('\n],\nen:[')
    blk = blk[:i].rstrip().rstrip(',') + es + blk[i:]
    en = ''.join(f',\n {{w:"{w}",t:4,d:{json.dumps(d, ensure_ascii=False)}}}' for w, d in EN)
    j = blk.rindex('\n]};')
    blk = blk[:j].rstrip().rstrip(',') + en + blk[j:]
    h = h[:a] + blk + h[b:]
    open('index.html', 'w', encoding='utf-8').write(h)
open('tools/wordle_palabras.js', 'w', encoding='utf-8').write(blk + '\n')
print('ok', blk.count(',t:4,'))
