#!/usr/bin/env python3
"""Tema 5: palabras del día (wordle) en el bloque WORDS de index.html y copia en tools/wordle_palabras.js (19-11-2026).
Todas las palabras y definiciones salen del texto de pantalla del Tema 5. Ejecutar solo cuando nadie más esté tocando index.html."""
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
ES = [("KEMARI", "Juego de pelota de la corte japonesa en el que entre 6 y 12 jugadores en círculo evitan que la pelota caiga al suelo."),
 ("DAOYIN", "Gimnasia de salud china, «guiar y estirar», que se practicaba para prevenir la vejez y la enfermedad."),
 ("SHAOLIN", "Monasterio chino que pasa por ser la cuna del kung-fu, aunque sus técnicas nacieron después del mito de Bodhidharma."),
 ("CHUIWAN", "Juego chino de palo y bola, «golpear la bola», pasatiempo de la élite en el que se apostaba."),
 ("DOHYO", "Círculo de arcilla cubierto de arena en el que se disputan los combates de sumo."),
 ("GYOJI", "Árbitro del sumo, que viste un traje de corte de la época Heian y da la salida con el gunbai."),
 ("BUSHIDO", "Código de conducta de los samuráis, el «camino del guerrero»."),
 ("SAMURAI", "Guerrero de la clase hereditaria japonesa, de saburau, «servir»."),
 ("SHOGUN", "Jefe militar que gobernó Japón en nombre del emperador desde 1185 d. C."),
 ("CATANA", "Espada curva de acero de filo único que el samurái llevaba siempre como símbolo de su condición."),
 ("TOSHIYA", "Competición de tiro con arco del templo Sanjūsangendō de Kioto, «flechas que pasan»."),
 ("KENDO", "«Camino de la espada», creado para entrenar a los samuráis en el uso de la catana."),
 ("KARATE", "Arte de combatir sin armas nacido en Okinawa, cuyo nombre acabó significando «mano vacía»."),
 ("VARNAS", "Los cuatro órdenes de la sociedad india, que un himno del Rigveda hace nacer del cuerpo de Purusha."),
 ("ASANAS", "Ejercicios posturales y respiratorios del yoga, que se combinan con la meditación."),
 ("AKHARA", "Gimnasio de los luchadores indios, dirigido por un gurú que regula su entrenamiento y su régimen de vida."),
 ("KUSHTI", "Lucha tradicional del norte de la India, sobre un foso de tierra humedecido con aceite y especias."),
 ("GADAS", "Mazas indias que se mueven de forma rítmica alrededor del cuerpo para ganar fuerza."),
 ("KABADDI", "Deporte de equipo indio en el que el explorador debe cantar su nombre sin respirar durante toda la jugada.")]
EN = [("KEMARI", "Ball game of the Japanese court in which 6 to 12 players in a circle keep the ball from touching the ground."),
 ("DAOYIN", "Chinese health gymnastics, 'guiding and stretching', practised to prevent old age and illness."),
 ("SHAOLIN", "Chinese monastery regarded as the cradle of kung fu, although its techniques arose after the Bodhidharma myth."),
 ("CHUIWAN", "Chinese club-and-ball game, 'hitting the ball', an elite pastime on which people bet."),
 ("DOHYO", "Clay circle covered with sand in which sumo bouts are fought."),
 ("GYOJI", "The sumo referee, who wears a Heian court costume and starts the bout with the gunbai."),
 ("BUSHIDO", "The samurai code of conduct, the 'way of the warrior'."),
 ("SAMURAI", "Warrior of Japan's hereditary class, from saburau, 'to serve'."),
 ("SHOGUN", "Military leader who ruled Japan in the emperor's name from AD 1185."),
 ("KATANA", "Curved single-edged steel sword that the samurai always carried as the symbol of his status."),
 ("TOSHIYA", "Archery competition at the Sanjūsangendō temple in Kyoto, 'passing arrows'."),
 ("KENDO", "'Way of the sword', created to train the samurai in the use of the katana."),
 ("KARATE", "Art of unarmed combat born in Okinawa, whose name came to mean 'empty hand'."),
 ("VARNAS", "The four orders of Indian society, which a hymn of the Rigveda has born from the body of Purusha."),
 ("ASANAS", "The postural and breathing exercises of yoga, combined with meditation."),
 ("AKHARA", "The gymnasium of Indian wrestlers, run by a guru who regulates their training and way of life."),
 ("KUSHTI", "Traditional wrestling of northern India, on an earthen pit moistened with oil and spices."),
 ("KABADDI", "Indian team sport in which the raider must chant its name without breathing throughout the raid.")]
h = open('index.html', encoding='utf-8').read()
a = h.index('const WORDS={'); b = h.index(']};', a) + 3
blk = h[a:b]
if ',t:5,' not in blk:
    es = ''.join(f',\n {{w:"{w}",t:5,d:{json.dumps(d, ensure_ascii=False)}}}' for w, d in ES)
    i = blk.index('\n],\nen:[')
    blk = blk[:i].rstrip().rstrip(',') + es + blk[i:]
    en = ''.join(f',\n {{w:"{w}",t:5,d:{json.dumps(d, ensure_ascii=False)}}}' for w, d in EN)
    j = blk.rindex('\n]};')
    blk = blk[:j].rstrip().rstrip(',') + en + blk[j:]
    h = h[:a] + blk + h[b:]
    open('index.html', 'w', encoding='utf-8').write(h)
open('tools/wordle_palabras.js', 'w', encoding='utf-8').write(blk + '\n')
print('ok', blk.count(',t:5,'))
