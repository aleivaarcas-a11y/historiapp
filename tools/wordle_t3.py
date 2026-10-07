#!/usr/bin/env python3
"""Tema 3: añade las palabras del día (wordle) a tools/wordle_palabras.js y vuelca el bloque WORDS en index.html (07-10-2026)."""
import os,re,json
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
ES=[("SALTO","El de la taurocatapsia, sobre un toro vivo y a la carrera; Younger (1995) ve en el salto en picado su esquema más frecuente."),
 ("CRETA","Isla montañosa entre Grecia, Egipto y Asia Menor cuya civilización minoica floreció hacia 1950-1450 a. C."),
 ("CNOSO","Palacio principal de Creta, excavado por Evans; de él proceden casi todas las imágenes del salto del toro."),
 ("RITON","Vaso para las libaciones; el de Hagia Triada muestra púgiles y el salto del toro en cuatro bandas."),
 ("PUGIL","Combatiente del pugilato; los de Micenas eran púgiles pagados que animaban los banquetes y funerales del señor."),
 ("PATIO","El central de los palacios cretenses medía entre un cuarto y un tercio de estadio y acogía público tras barreras de madera."),
 ("POLIS","Ciudad-estado griega con sus tierras y sus magistraturas; la victoria del atleta era también la de su polis."),
 ("ELIDE","Polis que administraba Olimpia, nombraba a los jueces y acogía el mes de concentración de los atletas."),
 ("OLIVO","De él era la corona, único premio material que daba el santuario de Olimpia al vencedor."),
 ("KLEOS","La gloria eterna que el noble griego buscaba con la victoria y que sobrevivía a su muerte."),
 ("ARETE","«Excelencia», el valor más alto de la sociedad griega, al que daba acceso la victoria olímpica."),
 ("DIETA","Hacia 500 a. C. se impuso una rica en carne, que daba ventaja en la lucha, el pugilato y el pancracio."),
 ("PISTA","La del estadio de Olimpia medía 192,27 metros entre las líneas de salida y llegada."),
 ("DISCO","Prueba del pentatlón; en Olimpia todos lanzaban el mismo el mismo día."),
 ("PLOMO","Material de las tablillas con maldiciones contra los rivales halladas en Nemea."),
 ("ZANES","Estatuas de Zeus pagadas con las multas, con el nombre del infractor grabado en el pedestal.")]
EN=[("CRETE","Mountainous island between Greece, Egypt and Asia Minor whose Minoan civilisation flourished c. 1950-1450 BC."),
 ("TRUCE","The ekecheiria, proclaimed by heralds before each edition; it protected Elis and the pilgrims, not all of Greece."),
 ("NAKED","How athletes competed after Orsippos of Megara ran so in 720 BC; nudity took over a century to spread."),
 ("TUNIC","The perizoma, the small tunic tied like a loincloth worn in the first Olympic editions."),
 ("OLIVE","The wreath made of it was the only material prize the sanctuary of Olympia gave the victor."),
 ("CROWN","Kyniska won it in 396 BC because in the equestrian events it went to the owner of the horses."),
 ("PRIZE","At the Panathenaia the stadion winner's one was probably 80 amphorae of oil, about 1,247 drachmas."),
 ("GLORY","Kleos, the eternal fame the Greek noble sought through victory."),
 ("THONG","The ankyle, a leather one wound round the javelin shaft to make it spin."),
 ("JUDGE","Achilles acts as one at Patroclus's games; at Olympia the Hellanodikai of Elis did so."),
 ("FINES","For bribery they paid for the Zanes, statues of Zeus by the stadium entrance."),
 ("CURSE","Athletes inscribed them on lead tablets, like those from Nemea, against their rivals.")]
p='tools/wordle_palabras.js'; s=open(p,encoding='utf-8').read()
if '"CNOSO",t:3' not in s:
    es=''.join(f' {{w:"{w}",t:3,d:{json.dumps(d,ensure_ascii=False)}}},\n' for w,d in ES)
    s=s.replace('\n],\nen:[\n','\n'+es.rstrip('\n')+'\n],\nen:[\n',1)
    en=',\n'.join(f' {{w:"{w}",t:3,d:{json.dumps(d,ensure_ascii=False)}}}' for w,d in EN)
    assert s.rstrip().endswith(']};')
    s=s.rstrip()[:-3].rstrip()+',\n'+en+'\n]};\n'
    open(p,'w',encoding='utf-8').write(s)
blk=s.strip()
h=open('index.html',encoding='utf-8').read()
a=h.index('const WORDS={'); b=h.index(']};',a)+3
h=h[:a]+blk+h[b:]
open('index.html','w',encoding='utf-8').write(h)
print('ok', blk.count('t:3'))
