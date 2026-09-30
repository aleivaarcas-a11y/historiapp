# Construye efe_09.json y efe_10.json (efemérides de septiembre y octubre)
import json, re, os
H = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(H, '..', '..', 'data', 'enciclopedia.json')))['entries']
EN = {}
for x in E:
    for a, b in zip(x['refs'], x['refs_en']):
        EN[a] = b
def R(prefix, strip_suffix=False):
    """Devuelve (es, en) de la ficha cuya referencia empieza por prefix."""
    for a, b in EN.items():
        if a.startswith(prefix):
            if strip_suffix:
                a = re.sub(r'\(s\. f\.-[a-z]\)', '(s. f.)', a); b = re.sub(r'\(n\.d\.-[a-z]\)', '(n.d.)', b)
            return (a, b)
    raise SystemExit('Falta ref: ' + prefix)
LEV_ES = 'En D. Levinson y K. Christensen (Eds.), *Encyclopedia of world sport: From ancient times to the present*'
LEV_EN = 'In D. Levinson & K. Christensen (Eds.), *Encyclopedia of world sport: From ancient times to the present*'
MH_ES = 'En J. A. Mangan y F. Hong (Eds.), *Sport in Asian society: Past and present*'
MH_EN = 'In J. A. Mangan & F. Hong (Eds.), *Sport in Asian society: Past and present*'
REC_ES = 'Recuperado el 30 de septiembre de 2026 de '
REC_EN = 'Retrieved September 30, 2026, from '
def lev(a, t, pp):
    return (f'{a} (1999). {t}. {LEV_ES} ({pp}). Oxford University Press.', f'{a} (1999). {t}. {LEV_EN} ({pp}). Oxford University Press.')
def mh(a_es, a_en, t, pp):
    return (f'{a_es} (2003). {t}. {MH_ES} ({pp}). Frank Cass.', f'{a_en} (2003). {t}. {MH_EN} ({pp}). Frank Cass.')
def oly(suf, title, url):
    return (f'Olympedia. (s. f.{suf}). *{title}*. {REC_ES}{url}', f'Olympedia. (n.d.{suf}). *{title}*. {REC_EN}{url}')

GUT04 = R('Guttmann, A. (2004)'); GUT91 = R('Guttmann, A. (1991)'); GT01 = R('Guttmann, A., y Thompson, L. (2001)')
VAM = R('Vamplew, W. (2021). *Games'); COL = R('Collins, T. (2019)'); DUN = R('Dunning, E., y Sheard, K. (2005)')
GEMS = R('Gems, G. R.'); MOR = R('Morrow, D., y Wamsley'); BRI = R('Brittain, I. (2016)'); HUMS = R('Hums, M. A.')
HA = R('Ha, N.-G., y Mangan')
MARS = lev('Mars, M.', 'Drugs and drug testing', 'pp. 109-112')
MOTT = lev('Mott, M.', 'Hockey, ice', 'pp. 168-170')
BARNEY = lev('Barney, R. K.', 'Olympic Games, modern', 'pp. 277-285')
CRAW = R('Crawford, S. J. (1999). Parachuting')
MAJ = mh('Majumdar, B.', 'Majumdar, B.', 'Cricket in colonial India: The Bombay Pentangular, 1892-1946', 'pp. 129-154')
HONGX = mh('Hong, F., y Xiong, X.', 'Hong, F., & Xiong, X.', 'Communist China: Sport, politics and diplomacy', 'pp. 258-276')
HORT = mh('Horton, P. A.', 'Horton, P. A.', 'Shackling the lion: Sport and modern Singapore', 'pp. 198-224')
WOL = ('Wolbring, G. (2018). Prostheses and other equipment: The issue of the cyborg athlete. Interrogating the media coverage of the Cybathlon 2016 event. En I. Brittain y A. Beacom (Eds.), *The Palgrave handbook of Paralympic studies* (pp. 439-459). Palgrave Macmillan.',
       'Wolbring, G. (2018). Prostheses and other equipment: The issue of the cyborg athlete. Interrogating the media coverage of the Cybathlon 2016 event. In I. Brittain & A. Beacom (Eds.), *The Palgrave handbook of Paralympic studies* (pp. 439-459). Palgrave Macmillan.')

def e(d, year, es, en, refs, enc=None):
    return {'d': d, 'year': year, 'es': es, 'en': en, 'refs': [r[0] for r in refs], 'refs_en': [r[1] for r in refs], 'enc': enc}

OCT = [
e('10-01', 1973,
 'El 1 de octubre de 1973 nació el Singapore Sports Council, fruto de la fusión del National Sports Promotion Board y de la National Stadium Corporation. Como organismo público, fue la voz y el brazo ejecutor del Gobierno en toda la política de deporte y recreación, y durante sus primeros veinte años se volcó en extender el programa «Sport for All» (Horton, 2003, p. 207).',
 'On 1 October 1973 the Singapore Sports Council was born from the merger of the National Sports Promotion Board and the National Stadium Corporation. As a statutory body it was the government\'s mouthpiece and its arms and legs in all sport and recreation policy, and for its first twenty years it concentrated on expanding the «Sport for All» programme (Horton, 2003, p. 207).',
 [HORT]),
e('10-02', 1968,
 'El 2 de octubre de 1968, diez días antes de la inauguración de los Juegos Olímpicos de México, las autoridades reprimieron una concentración estudiantil en la plaza de las Tres Culturas de Tlatelolco, donde murieron más de 250 personas según Olympedia. Los Juegos se abrieron el 12 de octubre, y aquella matanza quedó asociada desde entonces a su memoria (Olympedia, s. f.).',
 'On 2 October 1968, ten days before the opening of the Mexico City Olympic Games, the authorities suppressed a student demonstration in the Square of the Three Cultures at Tlatelolco, where more than 250 people were killed according to Olympedia. The Games opened on 12 October, and the massacre has been linked to their memory ever since (Olympedia, n.d.).',
 [oly('', '1968 Summer Olympics overview', 'https://www.olympedia.org/editions/17')]),
e('10-03', 1990,
 'El 3 de octubre de 1990 se fundó en Pekín, durante los XI Juegos Asiáticos, la Federación Internacional de Wushu. Aquellos Juegos fueron los primeros que incluyeron el wushu en su programa, y la nueva federación, que organizó en 1991 el primer Campeonato del Mundo, dio al arte marcial chino una estructura deportiva de alcance internacional (International Wushu Federation, s. f.-a, s. f.-b).',
 'On 3 October 1990 the International Wushu Federation was founded in Beijing, during the 11th Asian Games. Those Games were the first to include wushu in their programme, and the new federation, which held the first World Championships in 1991, gave the Chinese martial art a sporting structure of international reach (International Wushu Federation, n.d.-a, n.d.-b).',
 [R('International Wushu Federation. (s. f.-a)'), R('International Wushu Federation. (s. f.-b)')], 'sanda'),
e('10-04', 1891,
 'El 4 de octubre de 1891 se disputó en The Scalp, en el condado irlandés de Wicklow, el primer partido de polo en bicicleta, entre los Rathclaren Rovers y el club ciclista Ohne Hast. En 1901 se formó en Londres la primera asociación, y en 1908 el juego fue deporte de exhibición en los Juegos de Londres (National Museum of Ireland, s. f.; Olympedia, s. f.).',
 'On 4 October 1891 the first game of bicycle polo was played at The Scalp, in County Wicklow, Ireland, between the Rathclaren Rovers and the Ohne Hast cycling club. In 1901 the first association was formed in London, and in 1908 the game was a demonstration sport at the London Olympic Games (National Museum of Ireland, n.d.; Olympedia, n.d.).',
 [R('National Museum of Ireland. (s. f.). *Cycling'), R('Olympedia. (s. f.). *Bicycle polo')], 'bike-polo'),
e('10-05', 1967,
 'El 5 de octubre de 1967, en los 48.º Juegos Nacionales de Corea del Sur, el presidente Park Chung-hee afirmó que el atajo hacia la reunificación del país pasaba por aumentar la fuerza nacional, y que esa fuerza empezaba por la condición física. Park veía en el deporte y en las artes marciales una vía para reforzar la moral y la defensa nacional (Ha y Mangan, 2003, p. 185).',
 'On 5 October 1967, at the 48th National Games of South Korea, President Park Chung-hee claimed that the short cut to the reunification of the nation was an increase in national strength, and that national strength began with physical fitness. He saw sport and the martial arts as a means of raising morale and strengthening the defence of the nation (Ha & Mangan, 2003, p. 185).',
 [HA]),
e('10-06', 1975,
 'El 6 de octubre de 1975 la nadadora de larga distancia Diana Nyad dio la vuelta a la isla de Manhattan en siete horas y cincuenta y siete minutos, un tiempo récord. La hazaña ocupó la portada del New York Times y reportajes en revistas de todo tipo, en unos años en que las cadenas de televisión empezaban a contratar a mujeres para la información deportiva (Guttmann, 1991, p. 215).',
 'On 6 October 1975 the distance swimmer Diana Nyad swam around Manhattan Island in a record seven hours and fifty-seven minutes. Her feat made the front page of the New York Times and was featured in sports, general and women\'s magazines, at a time when the television networks were beginning to hire women for their sports coverage (Guttmann, 1991, p. 215).',
 [GUT91]),
e('10-07', 1728,
 'El 7 de octubre de 1728 el Daily Post de Londres publicó el desafío de Ann Field, una arriera, a Elisabeth Stokes para pelear por una bolsa de diez libras. Las mujeres de clase baja acudían en masa a los combates de boxeo del siglo XVIII, y aunque eran pocas las que subían al cuadrilátero, sus desafíos llegaban a la prensa (Guttmann, 2004, p. 73).',
 'On 7 October 1728 the London Daily Post published a notice from Ann Field, an ass-driver, challenging Elisabeth Stokes to fight for a stake of ten pounds. Lower-class women flocked to eighteenth-century prize fights, and although few of them entered the ring themselves, their challenges reached the press (Guttmann, 2004, p. 73).',
 [GUT04]),
e('10-08', 2016,
 'El 8 de octubre de 2016 se celebró en Zúrich el Cybathlon, presentado como unos «Juegos Olímpicos cíborg» para deportistas con discapacidad, con carreras de prótesis motorizadas de brazo y de pierna, exoesqueletos, sillas de ruedas motorizadas e interfaces cerebro-ordenador. Wolbring estudió la escasa cobertura que le dio la prensa y lo que el acontecimiento anunciaba para el futuro del movimiento paralímpico (Wolbring, 2018, pp. 444-445).',
 'On 8 October 2016 the Cybathlon was held in Zurich, billed as a «Cyborg Olympics» for athletes with disabilities, with races for powered arm and leg prostheses, exoskeletons, powered wheelchairs and brain-computer interfaces. Wolbring examined the scant press coverage it received and what the event suggested about the future of the Paralympic Movement (Wolbring, 2018, pp. 444-445).',
 [WOL]),
e('10-09', 2009,
 'El 9 de octubre de 2009 la 121.ª sesión del Comité Olímpico Internacional, reunida en Copenhague, aprobó por 81 votos contra 8 la inclusión del rugby a siete en el programa olímpico. La modalidad debutó en Río de Janeiro 2016 con doce equipos masculinos y doce femeninos, un escaparate en el que hombres y mujeres compitieron en igualdad de condiciones (World Rugby, s. f.).',
 'On 9 October 2009 the 121st Session of the International Olympic Committee, meeting in Copenhagen, approved the inclusion of rugby sevens in the Olympic programme by 81 votes to 8. The discipline made its debut at Rio de Janeiro 2016 with twelve men\'s and twelve women\'s teams, a showcase in which men and women competed on equal terms (World Rugby, n.d.).',
 [R('World Rugby. (s. f.-b)', True)], 'rugby-7'),
e('10-10', 1931,
 'El 10 de octubre de 1931 veintidós clubes constituyeron la Suomen Pesäpalloliitto, la federación finlandesa de pesäpallo, y ese mismo año se disputaron el primer campeonato de liga y el primer campeonato femenino. El juego fue deporte de exhibición en los Juegos de Helsinki de 1952, no tuvo campeonato del mundo hasta 1992 y ha seguido siendo ante todo una seña de identidad nacional finlandesa (Pesäpalloliitto, s. f.).',
 'On 10 October 1931 twenty-two clubs founded the Suomen Pesäpalloliitto, the Finnish pesäpallo federation, and in the same year the first league championship and the first women\'s championship were held. The game was a demonstration sport at the 1952 Helsinki Olympic Games, had no world championship until 1992 and has remained above all a mark of Finnish national identity (Pesäpalloliitto, n.d.).',
 [R('Pesäpalloliitto')], 'pesapallo'),
e('10-11', 1884,
 'El 11 de octubre de 1884 Michael Cusack publicó en The Irishman y en United Ireland su artículo «A Word about Irish Athletics», que llamaba a los irlandeses a tomar en sus manos la gestión de sus propios juegos. Cusack había abandonado el rugby y el críquet por los que consideraba deportes tradicionales de Irlanda, y se veía como el equivalente deportivo de los nacionalistas culturales (Collins, 2019, pp. 99-100).',
 'On 11 October 1884 Michael Cusack published his article «A Word about Irish Athletics» in The Irishman and United Ireland, calling on the Irish to take the management of their games into their own hands. Cusack had abandoned rugby and cricket for what he regarded as traditional Irish sports, and saw himself as the sporting equivalent of the cultural nationalists (Collins, 2019, pp. 99-100).',
 [COL]),
e('10-12', 1968,
 'El 12 de octubre de 1968, en la ceremonia de apertura de los Juegos Olímpicos de México, la vallista Enriqueta Basilio se convirtió en la primera mujer que encendía el fuego olímpico. Aquel mismo año compitió en los 80 metros vallas, los 400 metros y el relevo de 4 × 100, y más tarde fue miembro del Comité Olímpico Mexicano y diputada federal (Olympedia, s. f.-a, s. f.-b).',
 'On 12 October 1968, at the opening ceremony of the Mexico City Olympic Games, the hurdler Enriqueta Basilio became the first woman to light the Olympic flame at the Games. That same year she competed in the 80 metres hurdles, the 400 metres and the 4 × 100 relay, and she later became a member of the Mexican Olympic Committee and a federal deputy (Olympedia, n.d.-a, n.d.-b).',
 [oly('-a', '1968 Summer Olympics overview', 'https://www.olympedia.org/editions/17'), oly('-b', 'Enriqueta Basilio', 'https://www.olympedia.org/athletes/73431')]),
e('10-13', 2019,
 'El 13 de octubre de 2019, un día después de que Eliud Kipchoge bajara de las dos horas en Viena, la keniana Brigid Kosgei batió en Chicago por 81 segundos una marca femenina que llevaba dieciséis años en pie. Los dos calzaban las Vaporfly de Nike, pensadas para devolver parte de la energía de cada zancada, y las de Kosgei aún no estaban a la venta (Vamplew, 2021, p. 155).',
 'On 13 October 2019, a day after Eliud Kipchoge ran a marathon in under two hours in Vienna, the Kenyan Brigid Kosgei broke by 81 seconds, in Chicago, a women\'s mark that had stood for sixteen years. Both were wearing Nike Vaporfly shoes, designed to return some of the energy of each stride, and Kosgei\'s were a version not yet available to the public (Vamplew, 2021, p. 155).',
 [VAM]),
e('10-14', 1922,
 'El 14 de octubre de 1922 el británico Harold Searles Thornton solicitó la primera patente documentada del futbolín, que se publicó el 1 de noviembre de 1923. Su aparato tenía barras capaces de desplazarse a lo largo y de girar en parte, de las que colgaban las figuras de los jugadores, y un tío suyo, Louis P. Thornton, patentó el juego en Estados Unidos en 1927 (Thornton, 1923; Workman, 2013).',
 'On 14 October 1922 the Briton Harold Searles Thornton filed the first documented patent for table football, which was published on 1 November 1923. His apparatus had rods able to slide lengthwise and partly rotate, from which the players\' figures hung, and his uncle, Louis P. Thornton, patented the game in the United States in 1927 (Thornton, 1923; Workman, 2013).',
 [R('Thornton, H. S. (1923)'), R('Workman, D. (2013')], 'futbolin'),
e('10-15', 1966,
 'El 15 de octubre de 1966 la pista de hōlua de Keauhou, en la isla de Hawái, entró en el Registro Nacional de Lugares Históricos de Estados Unidos. Por estas pistas construidas a propósito los hawaianos descendían las colinas sobre un trineo estrecho, y hoy se consideran parte del patrimonio de la identidad hawaiana (National Park Service, s. f.).',
 'On 15 October 1966 the Keauhou hōlua slide, on the island of Hawaii, was listed in the National Register of Historic Places of the United States. On these purpose-built tracks Hawaiians raced downhill on a narrow sled, and today the slides are regarded as part of the heritage of Hawaiian identity (National Park Service, n.d.).',
 [R('National Park Service. (s. f.). *Keauhou')], 'holua'),
e('10-16', 2023,
 'El 16 de octubre de 2023 el Comité Olímpico Internacional aprobó el regreso del lacrosse a los Juegos Olímpicos en Los Ángeles 2028, en la modalidad de seis jugadores. El juego, de origen indígena norteamericano, cuenta en los torneos de su federación internacional con la selección de la Confederación Haudenosaunee, que compite con identidad propia (World Lacrosse, s. f., 2023).',
 'On 16 October 2023 the International Olympic Committee approved the return of lacrosse to the Olympic Games at Los Angeles 2028, in the six-a-side format. The game, of Native North American origin, includes in its international federation\'s tournaments the team of the Haudenosaunee Confederacy, which competes under its own identity (World Lacrosse, n.d., 2023).',
 [R('World Lacrosse. (s. f.)'), R('World Lacrosse. (2023')], 'lacrosse'),
e('10-17', 1986,
 'El 17 de octubre de 1986, en la 91.ª sesión del Comité Olímpico Internacional celebrada en Lausana, Barcelona obtuvo los Juegos Olímpicos de 1992, con 47 votos frente a los 23 de París en la última ronda. Muchos interpretaron la elección como un homenaje al presidente del COI, Juan Antonio Samaranch, nacido en la ciudad condal (Olympedia, s. f.).',
 'On 17 October 1986, at the 91st Session of the International Olympic Committee in Lausanne, Barcelona was awarded the 1992 Olympic Games, with 47 votes to Paris\'s 23 in the final round. Many saw the choice as a tribute to the IOC President, Juan Antonio Samaranch, a native of the city (Olympedia, n.d.).',
 [oly('', '1992 Summer Olympics overview', 'https://www.olympedia.org/editions/23')]),
e('10-18', 1968,
 'El 18 de octubre de 1968 el estadounidense Bob Beamon saltó 8,90 metros en la final de longitud de los Juegos de México y fue el primero en superar los 28 y los 29 pies. A 2.134 metros de altitud, el aire enrarecido favoreció a los velocistas y castigó a los fondistas, y su récord del mundo resistió hasta 1991 (Olympedia, s. f.-a, s. f.-b).',
 'On 18 October 1968 the American Bob Beamon jumped 8.90 metres in the long jump final at the Mexico City Games, more than two feet ahead of the runner-up, becoming the first man to clear both 28 and 29 feet. At 2,134 metres of altitude the thin air favoured sprinters and punished distance runners, and his world record lasted until 1991 (Olympedia, n.d.-a, n.d.-b).',
 [oly('-a', '1968 Summer Olympics overview', 'https://www.olympedia.org/editions/17'), oly('-b', 'Bob Beamon', 'https://www.olympedia.org/athletes/78091')]),
e('10-19', 1969,
 'El 19 de octubre de 1969 representantes de ocho clubes fundaron la Asociación Europea de Senderismo, presidida por Georg Fahrbach, en el refugio del Schwäbischer Albverein en el Raichberg, en Alemania. El 16 de julio de 1972 se inauguraron en Constanza los primeros senderos europeos de gran recorrido, el E1 y el E5, que unían por caminos a pie países distintos (ERA, s. f.).',
 'On 19 October 1969 representatives of eight clubs founded the European Ramblers\' Association, chaired by Georg Fahrbach, at the Schwäbischer Albverein hut on the Raichberg, in Germany. On 16 July 1972 the first European long-distance paths, the E1 and the E5, were opened in Konstanz, linking different countries by footpath (ERA, n.d.).',
 [R('ERA. (s. f.)')], 'senderismo'),
e('10-20', 2004,
 'El 20 de octubre de 2004 responsables deportivos de veintidós países constituyeron, en el centro de conferencias de la Academia Olímpica Nacional de Irán, la International Zurkhaneh Sports Federation. La práctica tradicional iraní de la zurkhaneh, con sus ejercicios de fuerza y su lucha, adoptaba así la forma de una federación deportiva internacional (International Zurkhaneh Sports and Koshti Pahlavani Federation, s. f.).',
 'On 20 October 2004 sports officials from twenty-two countries set up the International Zurkhaneh Sports Federation at the conference centre of the National Olympic Academy of Iran. The traditional Iranian practice of the zurkhaneh, with its strength exercises and its wrestling, thus took the form of an international sports federation (International Zurkhaneh Sports and Koshti Pahlavani Federation, n.d.).',
 [R('International Zurkhaneh Sports and Koshti Pahlavani Federation. (s. f.-b)', True)], 'zurkhaneh'),
e('10-21', 2000,
 'El 21 de octubre de 2000 la selección española de baloncesto para deportistas con discapacidad intelectual ganó el oro paralímpico en Sídney ante Rusia. A finales de noviembre, uno de sus jugadores, periodista de la revista Capital, reveló que diez de los doce campeones no tenían discapacidad alguna, y el escándalo dejó a estos deportistas fuera de los Juegos hasta Londres 2012 (Brittain, 2016, pp. 198, 204).',
 'On 21 October 2000 Spain\'s intellectually disabled basketball team won the gold medal at the Sydney Paralympic Games, beating Russia 87-63 in the final. In late November one of its players, a journalist with the magazine Capital, revealed that ten of the twelve champions had no disability at all, and the scandal kept these athletes out of the Paralympic Games until London 2012 (Brittain, 2016, pp. 198, 204).',
 [BRI]),
e('10-22', 1797,
 'El 22 de octubre de 1797 el francés André-Jacques Garnerin se lanzó desde su globo sobre París, a unos seiscientos metros de altura, en el primer salto en paracaídas bien documentado. El paso a la competición llegó mucho después, y en la Unión Soviética de los años treinta se organizaban ya concursos de precisión en el aterrizaje (Crawford, 1999, p. 289; Fédération Aéronautique Internationale, s. f.).',
 'On 22 October 1797 the Frenchman André-Jacques Garnerin leapt from his balloon over Paris, from some six hundred metres, in the first well-documented parachute jump. Competition came much later, and in the Soviet Union of the 1930s accuracy landing contests were already being organised (Crawford, 1999, p. 289; Fédération Aéronautique Internationale, n.d.).',
 [CRAW, R('Fédération Aéronautique Internationale. (s. f.)')], 'paracaidismo'),
e('10-23', 1725,
 'El 23 de octubre de 1725 el Mist\'s Journal contaba que numerosos caballeros de la pequeña nobleza habían acudido a una carrera de dos muchachas con la esperanza de verlas correr desnudas, y que al final corrieron con chaleco y calzones blancos, descalzas. En estas carreras inglesas, que premiaban a la ganadora con una camisa o una cinta, el deporte femenino se mezclaba con el voyeurismo (Guttmann, 1991, p. 72).',
 'On 23 October 1725 Mist\'s Journal reported that great numbers of the lower gentry had attended a race between two young women hoping to see them run naked, and that in the end they ran in white waistcoats and drawers, barefoot. In these English races, which rewarded the winner with a smock or a ribbon, women\'s sport was mixed with voyeurism (Guttmann, 1991, p. 72).',
 [GUT91]),
e('10-24', 1985,
 'El 24 de octubre de 1985 los lanzadores de los Yomiuri Giants, dirigidos por Oh Sadaharu, no le lanzaron a Randy Bass ni un solo strike en cinco turnos. El estadounidense de los Hanshin Tigers amenazaba con sus 54 jonrones el récord de Oh, que negó después haber dado esa orden, y el episodio mostró los recelos del béisbol japonés ante los extranjeros (Guttmann y Thompson, 2001, p. 189).',
 'On 24 October 1985 the pitchers of the Yomiuri Giants, managed by Oh Sadaharu, did not throw Randy Bass a single strike in five at-bats. The American slugger of the Hanshin Tigers threatened Oh\'s record with his 54 home runs, Oh later denied having ordered it, and the episode showed Japanese baseball\'s suspicion of foreign players (Guttmann & Thompson, 2001, p. 189).',
 [GT01]),
e('10-25', 1940,
 'El 25 de octubre de 1940 se constituyó en Sudáfrica el organismo nacional del jukskei, que la federación designa con las siglas SAJR. Desde entonces el juego, en el que se lanzan clavijas de madera contra una estaca y cuyo nombre procede de la clavija que se sacaba del yugo de los bueyes, se transformó en un deporte con reglamento propio (Jukskei SA, s. f.).',
 'On 25 October 1940 the national jukskei body, which the federation refers to by the initials SAJR, was founded in South Africa. From then on the game, in which wooden pegs are thrown at a stake and whose name comes from the peg taken from the oxen\'s yoke, became a sport with its own rules (Jukskei SA, n.d.).',
 [R('Jukskei SA')], 'jukskei'),
e('10-26', 1863,
 'El 26 de octubre de 1863 representantes de una docena de clubes londinenses fundaron en la Freemasons\' Tavern la Football Association, a propuesta del abogado Ebenezer Morley. El 19 de diciembre se jugó el primer partido con sus reglas, entre Barnes y Richmond, y del nombre de la asociación derivó la palabra soccer (FIFA, 2017; Guttmann, 2004, p. 106).',
 'On 26 October 1863 representatives of a dozen London clubs founded the Football Association at the Freemasons\' Tavern, on the proposal of the solicitor Ebenezer Morley. On 19 December the first match under its laws was played between Barnes and Richmond, and the word soccer derives from the name of the Association (FIFA, 2017; Guttmann, 2004, p. 106).',
 [R('FIFA. (2017'), GUT04], 'futbol'),
e('10-27', 1931,
 'El 27 de octubre de 1931, en el estadio del santuario Meiji de Tokio, los japoneses Oda Mikio y Nanbu Chūhei establecieron los récords del mundo de triple salto y de salto de longitud. Japón llegó así a los Juegos de Los Ángeles de 1932 con dos plusmarquistas mundiales, en un equipo de 131 deportistas, 115 hombres y 16 mujeres (Guttmann y Thompson, 2001, pp. 122-123).',
 'On 27 October 1931, at the Meiji Shrine Stadium in Tokyo, the Japanese jumpers Oda Mikio and Nanbu Chūhei set the world records for the triple jump and the long jump. Japan thus came to the 1932 Los Angeles Games with two world-record holders, in a team of 131 athletes, 115 men and 16 women (Guttmann & Thompson, 2001, pp. 122-123).',
 [GT01]),
e('10-28', 1860,
 'El 28 de octubre de 1860 nació en la actual prefectura de Hyōgo Kanō Jigorō, creador del judo, siete años antes de que el régimen feudal japonés cediera el paso a los modernizadores de la era Meiji. Kanō, que hizo una larga carrera de educador, concibió el judo ante todo como una disciplina espiritual en la que debían dominar las virtudes confucianas (Guttmann y Thompson, 2001, p. 101).',
 'On 28 October 1860 Kanō Jigorō, the creator of judo, was born in what is now Hyōgo Prefecture, seven years before Japan\'s feudal regime gave way to the modernisers of the Meiji era. Kanō, who had a long career as an educator, conceived judo above all as a spiritual discipline in which Confucian virtues should dominate (Guttmann & Thompson, 2001, p. 101).',
 [GT01]),
e('10-29', 1917,
 'El 29 de octubre de 1917 el berlinés Max Heiser presentó, con Karl Schelenz y Erich König, unas reglas de balonmano para las secciones femeninas del Berliner Turnrat. Durante la Primera Guerra Mundial Heiser había ideado para las trabajadoras de la fábrica Siemens un juego al aire libre, competitivo, inspirado en el fútbol y sin contacto corporal (Román Seco, 2015, pp. 22-25).',
 'On 29 October 1917 the Berliner Max Heiser, together with Karl Schelenz and Erich König, presented handball rules for the women\'s sections of the Berliner Turnrat. During the First World War Heiser had devised for the women workers of the Siemens factory an outdoor competitive game, inspired by football and without bodily contact (Román Seco, 2015, pp. 22-25).',
 [R('Román Seco')], 'balonmano'),
e('10-30', 1740,
 'El 30 de octubre de 1740 el plantador virginiano William Byrd II anotó en su diario que, tras la comida, había ganado veinte chelines en una carrera de caballos a la que no asistió. Las carreras permitían a la élite de plantadores exhibir su posición, mientras mujeres, pequeños agricultores, sirvientes y esclavos miraban a distancia (Gems et al., 2008, pp. 19-20).',
 'On 30 October 1740 the Virginia planter William Byrd II noted in his diary that, after dinner, he had won twenty shillings on a horse race he did not attend. Racing allowed the planter elite to display their status, while women, poorer planters, servants and slaves watched from a distance (Gems et al., 2008, pp. 19-20).',
 [GEMS]),
e('10-31', 1921,
 'El 31 de octubre de 1921, cinco meses después de que los juegos de Montecarlo demostraran que las competiciones internacionales femeninas eran viables, Alice Milliat fundó la Fédération Sportive Féminine Internationale. Milliat, que había presidido la federación francesa de sociedades deportivas femeninas, organizó al año siguiente en París unos juegos internacionales con once pruebas (Guttmann, 1991, p. 167).',
 'On 31 October 1921, five months after the Monte Carlo games had shown that international competitions for women were viable, Alice Milliat founded the Fédération Sportive Féminine Internationale. Milliat, who had been president of the French federation of women\'s sports societies, organised international games in Paris the following year with eleven events (Guttmann, 1991, p. 167).',
 [GUT91]),
]

SEP = [
e('09-01', 1880,
 'El 1 de septiembre de 1880 se disputó en el Staten Island Cricket and Baseball Club el primer torneo de tenis sobre hierba de Estados Unidos, a propuesta de Eugenius H. Outerbridge. Su hermana Mary Ewing Outerbridge había llevado el juego a aquel club en 1874, y el torneo condujo en 1881 a la fundación de la asociación nacional de tenis (Gems et al., 2008, pp. 168-169).',
 'On 1 September 1880 the first lawn tennis tournament in the United States was held at the Staten Island Cricket and Baseball Club, at the suggestion of Eugenius H. Outerbridge. His sister Mary Ewing Outerbridge had introduced the game to the club in 1874, and the tournament led in 1881 to the founding of the national lawn tennis association (Gems et al., 2008, pp. 168-169).',
 [GEMS]),
e('09-02', 1962,
 'El 2 de septiembre de 1962 la República Popular China anunció su pleno apoyo a los Juegos de las Nuevas Fuerzas Emergentes (GANEFO). Sus expertos entendían que el COI, dominado por las potencias imperialistas, negaba sus derechos a los países recién independizados de Asia, África y América Latina, y que los nuevos juegos darían a Pekín un escenario para mostrar su influencia sobre ellos (Hong y Xiong, 2003, p. 265).',
 'On 2 September 1962 the People\'s Republic of China announced its full support for the Games of the New Emerging Forces (GANEFO). Its experts held that the IOC, dominated by the imperialist powers, denied the rights of the newly independent countries of Asia, Africa and Latin America, and that the new games would give Beijing a stage to show its influence over them (Hong & Xiong, 2003, p. 265).',
 [HONGX]),
e('09-03', 1983,
 'El 3 de septiembre de 1983 se fundó en Chiasso, en Suiza, la Confederazione Boccistica Internazionale, durante el primer campeonato del mundo por equipos, con delegados de veinte naciones entre las que figuraban Argentina, Brasil, Uruguay, Perú, Estados Unidos y Canadá. Aquella composición reflejaba la huella de la emigración italiana, que desde finales del siglo XIX llevó el juego a todas partes (Confederazione Boccistica Internazionale, s. f.; Impiglia, 2004).',
 'On 3 September 1983 the Confederazione Boccistica Internazionale was founded in Chiasso, Switzerland, during the first team world championship, with delegates from twenty nations including Argentina, Brazil, Uruguay, Peru, the United States and Canada. That membership reflected the imprint of Italian emigration, which from the late nineteenth century carried the game all over the world (Confederazione Boccistica Internazionale, n.d.; Impiglia, 2004).',
 [R('Confederazione Boccistica'), R('Impiglia, M. (2004)')], 'bochas'),
e('09-04', 1931,
 'El 4 de septiembre de 1931 delegados de siete países fundaron en Lwów, entonces ciudad polaca y hoy Leópolis, la Fédération Internationale de Tir à l\'Arc (FITA), que entre sus objetivos tenía devolver el tiro con arco al programa olímpico, cosa que logró en 1972. En 1961 eligió presidenta a la británica Inger Frith, una de las primeras mujeres al frente de una federación internacional (World Archery, s. f.).',
 'On 4 September 1931 delegates from seven countries founded the Fédération Internationale de Tir à l\'Arc (FITA) in Lwów, then a Polish city and today Lviv, with the aim, among others, of returning archery to the Olympic programme, which it achieved in 1972. In 1961 it elected Inger Frith of Great Britain as president, one of the first women to head an international federation (World Archery, n.d.).',
 [R('World Archery. (s. f.-a)', True)], 'tiro-con-arco'),
e('09-05', 1972,
 'El 5 de septiembre de 1972 un comando palestino de la organización Septiembre Negro entró en la Villa Olímpica de Múnich, mató a los israelíes que se le resistieron y tomó rehenes del equipo de Israel. Los Juegos que Alemania Occidental había querido presentar como la imagen opuesta a los de Berlín de 1936 quedaron unidos para siempre al terrorismo (Barney, 1999, p. 282; Vamplew, 2021, p. 289).',
 'In the early hours of 5 September 1972 a Palestinian commando of the Black September organisation entered the Munich Olympic village, killed the Israelis who resisted and took members of the Israeli team hostage. The Games that West Germany had wished to present as the opposite of Berlin 1936 were linked to terrorism for ever (Barney, 1999, p. 282; Vamplew, 2021, p. 289).',
 [BARNEY, VAM]),
e('09-06', 1950,
 'El 6 de septiembre de 1950 la Federación Rumana de Oina, fundada en 1932, se constituyó de nuevo bajo la presidencia del ministro de Educación, N. Popescu Doreanu. La oina, un juego de pelota y bate que folcloristas y educadores reivindicaron desde el siglo XIX como propio, ha estado ligada a la escuela y a la afirmación de la identidad nacional rumana (Federația Română de Oină, s. f.).',
 'On 6 September 1950 the Romanian Oină Federation, founded in 1932, was constituted again under the presidency of the Minister of Education, N. Popescu Doreanu. Oină, a bat-and-ball game that folklorists and educators had claimed as Romania\'s own since the nineteenth century, has been tied to the school and to the affirmation of Romanian national identity (Federația Română de Oină, n.d.).',
 [R('Federația Română de Oină')], 'oina'),
e('09-07', 1846,
 'El 7 de septiembre de 1846 una asamblea de alumnos mayores de la escuela de Rugby, el llamado Bigside levée, ratificó con pequeños cambios las treinta y siete reglas de fútbol que hasta entonces tenían carácter provisional. Desde ese momento los prefectos ya no pudieron dictar a su antojo las reglas del juego, que había subido en la escala de valores de la escuela (Dunning y Sheard, 2005, p. 67).',
 'On 7 September 1846 a meeting of the senior boys of Rugby School, the so-called Bigside levée, ratified with minor changes the thirty-seven football rules that had until then been experimental. From that moment the prefects could no longer dictate the rules of the game at will, a game that had risen in the school\'s hierarchy of values (Dunning & Sheard, 2005, p. 67).',
 [DUN]),
e('09-08', 1888,
 'El 8 de septiembre de 1888 comenzó la Football League, fundada en abril por clubes de Lancashire y de los Midlands. Sus equipos se eligieron con criterios empresariales, uno por ciudad y con estadios bien comunicados, y en su primera temporada atrajo a 602.000 espectadores, de modo que el fútbol profesional inglés se organizó desde el principio como un negocio (Collins, 2019, p. 61).',
 'On 8 September 1888 the Football League kicked off, founded that April by clubs from Lancashire and the Midlands. Its teams were chosen on strict business criteria, one per town and with easily accessible grounds, and in its first season it attracted 602,000 spectators, so that English professional football was organised from the outset as a business (Collins, 2019, p. 61).',
 [COL]),
e('09-09', 1998,
 'El 9 de septiembre de 1998 una mujer arbitró por primera vez un partido de la primera división de la Japan Basketball League. Dos meses después había ya ocho árbitras en la liga, frente a 160 hombres, y ese mismo año Takahara Sumiko se había convertido en la primera mujer al frente de la Liga Central del béisbol profesional japonés (Guttmann y Thompson, 2001, p. 240).',
 'On 9 September 1998 a woman refereed a first-division game of the Japan Basketball League for the first time. Two months later there were eight women referees in the league, alongside 160 men, and earlier that year Takahara Sumiko had become the first woman to chair the Central League of Japanese professional baseball (Guttmann & Thompson, 2001, p. 240).',
 [GT01]),
e('09-10', 1935,
 'El 10 de septiembre de 1935 nueve países europeos fundaron en Praga la Fédération Internationale de Danse pour Amateurs, primera organización internacional del baile deportivo, que un año después celebró su primer campeonato del mundo en Bad Nauheim, en Alemania. La federación suspendió su actividad en 1956, tras veinte años marcados por la guerra y por los conflictos entre aficionados y profesionales (World DanceSport Federation, s. f.).',
 'On 10 September 1935 nine European countries founded the Fédération Internationale de Danse pour Amateurs in Prague, the first international organisation of dancesport, which a year later held its first world championship in Bad Nauheim, Germany. The federation suspended its activities in 1956, after twenty years marked by the war and by conflicts between amateurs and professionals (World DanceSport Federation, n.d.).',
 [R('World DanceSport Federation. (s. f.-b)', True)], 'baile-deportivo'),
e('09-12', 1892,
 'El 12 de septiembre de 1892 el Gobierno de Bombay autorizó las parcelas que lord Harris había asignado junto al mar a los clubes de críquet de hindúes, musulmanes y parsis, por doce rupias al año. El reparto los situaba en pie de igualdad con los europeos del Bombay Gymkhana, si bien dejó organizado desde el principio el críquet de la ciudad por comunidades (Majumdar, 2003, p. 135).',
 'On 12 September 1892 the Bombay government authorised the seafront plots that Lord Harris had allotted to the cricket clubs of the Hindus, the Muslims and the Parsees, for a rent of twelve rupees a year. The allocation placed them on equal terms with the Europeans of the Bombay Gymkhana, although it organised the city\'s cricket along communal lines from the very beginning (Majumdar, 2003, p. 135).',
 [MAJ]),
e('09-13', 1893,
 'El 13 de septiembre de 1893 nueve clubes reunidos en Southsea, cerca de Portsmouth, fundaron la Badminton Association, la primera asociación nacional de bádminton del mundo. Aprobó un reglamento común, reunió catorce clubes en su primer año y en 1899 organizó en Londres los primeros campeonatos All England (The Badminton Museum, s. f.).',
 'On 13 September 1893 nine clubs meeting at Southsea, near Portsmouth, founded the Badminton Association, the first national badminton association in the world. It approved common rules, gathered fourteen clubs in its first year and in 1899 staged the first All England Championships in London (The Badminton Museum, n.d.).',
 [R('The Badminton Museum')], 'badminton'),
e('09-14', 1919,
 'El 14 de septiembre de 1919 se fundó en Torrelavega la Federación Bolística Montañesa, que en 1920 organizó en la misma ciudad el primer campeonato regional de bolo palma. Los bolos cántabros se encauzaban así hacia la organización federativa del deporte moderno, que culminó en 1941 con la creación de la Federación Cántabra y de la Federación Española de Bolos (Federación Cántabra de Bolos, s. f.).',
 'On 14 September 1919 the Federación Bolística Montañesa was founded in Torrelavega, and in 1920 it organised the first regional bolo palma championship in the same town. Cantabrian skittles were thus drawn into the federative organisation of modern sport, which culminated in 1941 with the creation of the Cantabrian Federation and the Spanish Bowling Federation (Federación Cántabra de Bolos, n.d.).',
 [R('Federación Cántabra de Bolos')], 'bolo-palma'),
e('09-15', 2002,
 'El 15 de septiembre de 2002 se fundó la federación internacional de racketlon, un deporte que combina en un solo encuentro cuatro deportes de raqueta, el tenis de mesa, el bádminton, el squash y el tenis. El primer torneo internacional, el Gothenburg Racketlon World Open, se había jugado en noviembre de 2001 con participantes de seis países (FIR, s. f.).',
 'On 15 September 2002 the international racketlon federation was founded, for a sport that combines four racket sports in a single match, table tennis, badminton, squash and tennis. The first international tournament, the Gothenburg Racketlon World Open, had been played in November 2001 with participants from six countries (FIR, n.d.).',
 [R('FIR. (s. f.)')], 'racketlon'),
e('09-16', 1953,
 'El 16 de septiembre de 1953 el decreto n.º 17.468, firmado por Juan Domingo Perón, declaró el pato deporte nacional de Argentina, condición que la Ley 27.368 reguló en 2017. El juego de los gauchos, con reglamento desde 1937-1938 y federación desde 1941, quedaba así convertido en emblema de la nación, si bien nunca rivalizó en arraigo popular con el fútbol (Gobierno de Argentina, s. f.; Guttmann, 2004, p. 170).',
 'On 16 September 1953 Decree No. 17,468, signed by Juan Domingo Perón, declared pato the national sport of Argentina, a status regulated by Law 27,368 in 2017. The old gaucho game, with rules since 1937-1938 and a federation since 1941, thus became a national emblem, although it never rivalled football in popular roots (Gobierno de Argentina, n.d.; Guttmann, 2004, p. 170).',
 [R('Gobierno de Argentina'), GUT04], 'pato'),
e('09-17', 1854,
 'El 17 de septiembre de 1854 Alfred Wills subió al Wetterhorn, la ascensión con la que los primeros historiadores británicos del alpinismo fijaron el nacimiento de este deporte. Peter Donnelly considera esa fecha un mito de origen, comparable al que atribuye a Abner Doubleday la invención del béisbol (Donnelly, 1999, pp. 262-263).',
 'On 17 September 1854 Alfred Wills climbed the Wetterhorn, the ascent with which the first British historians of mountaineering fixed the birth of the sport. Peter Donnelly regards that date as an origin myth, comparable to the one that credits Abner Doubleday with the invention of baseball (Donnelly, 1999, pp. 262-263).',
 [R('Donnelly, P. (1999). Mountain')], 'alpinismo'),
e('09-18', 1990,
 'El 18 de septiembre de 1990, en la 96.ª sesión del Comité Olímpico Internacional reunida en Tokio, Atlanta obtuvo los Juegos del centenario con 51 votos frente a los 35 de Atenas. Los griegos se sintieron despojados y llegaron a pensar en un boicot, y hubo quien acusó a la ciudad y a Coca-Cola, patrocinadora olímpica con sede en Atlanta, de haber comprado los Juegos (Olympedia, s. f.).',
 'On 18 September 1990, at the 96th Session of the International Olympic Committee in Tokyo, Atlanta won the Centennial Games with 51 votes to Athens\'s 35. The Greeks felt the Games had been stolen from them and briefly considered a boycott, and some accused the city and Coca-Cola, an Olympic sponsor based in Atlanta, of buying the Olympics (Olympedia, n.d.).',
 [oly('', '1996 Summer Olympics overview', 'https://www.olympedia.org/editions/24')]),
e('09-19', 1783,
 'El 19 de septiembre de 1783 los hermanos Joseph y Jacques Étienne Montgolfier, hijos de un fabricante de papel de Annonay, lanzaron un globo con una oveja, un gallo y un pato a bordo. Construían sus globos de papel y tafetán y los llenaban con el humo de paja húmeda, convencidos de que era el humo lo que los elevaba (Ludwig, 1999, p. 26).',
 'On 19 September 1783 the brothers Joseph and Jacques Étienne Montgolfier, sons of a paper manufacturer from Annonay, launched a balloon carrying a sheep, a cockerel and a duck. They built their balloons of paper and taffeta and filled them with smoke from damp straw, convinced that the smoke was what lifted them (Ludwig, 1999, p. 26).',
 [R('Ludwig, R. P. (1999)')], 'aerostacion'),
e('09-20', 1973,
 'El 20 de septiembre de 1973 Billie Jean King venció a Bobby Riggs por 6-4, 6-3 y 6-3 ante más de 30.000 espectadores en el Astrodome de Houston y unos cuarenta millones de telespectadores. Riggs, que se proclamaba el machista número uno del mundo, había derrotado meses antes a Margaret Court, y King quiso reparar aquella derrota en un partido convertido en espectáculo (Guttmann, 1991, p. 210).',
 'On 20 September 1973 Billie Jean King beat Bobby Riggs 6-4, 6-3, 6-3 before more than 30,000 spectators in the Houston Astrodome and some forty million television viewers. Riggs, who called himself the number-one male chauvinist in the world, had beaten Margaret Court months earlier, and King set out to redeem that defeat in a match turned into a show (Guttmann, 1991, p. 210).',
 [GUT91]),
e('09-21', 1933,
 'El 21 de septiembre de 1933 Salvador Lutteroth González fundó la Empresa Mexicana de Lucha Libre, hoy Consejo Mundial de Lucha Libre. Lutteroth había visto este espectáculo en 1929 en El Paso, en Texas, y reunió a un grupo de emprendedores para implantarlo en México, donde aquel producto fronterizo e importado acabó convertido en seña de identidad nacional (Consejo Mundial de Lucha Libre, s. f.).',
 'On 21 September 1933 Salvador Lutteroth González founded the Empresa Mexicana de Lucha Libre, today the Consejo Mundial de Lucha Libre. Lutteroth had watched the spectacle in 1929 in El Paso, Texas, and gathered a group of entrepreneurs to establish it in Mexico, where that imported border product eventually became a mark of national identity (Consejo Mundial de Lucha Libre, n.d.).',
 [R('Consejo Mundial de Lucha Libre')], 'lucha-libre-mexicana'),
e('09-22', 1989,
 'El 22 de septiembre de 1989 quedó fundado el Comité Paralímpico Internacional, al término de una asamblea general celebrada en Düsseldorf. La nueva organización iba a llamarse International Confederation of Sports Organisations for the Disabled, pero una votación impuso el nombre de International Paralympic Committee, con el derecho exclusivo a organizar los Juegos Paralímpicos (Brittain, 2016, p. 40; Hums y Pate, 2018, p. 173).',
 'On 22 September 1989 the International Paralympic Committee was founded at the end of a general assembly held in Düsseldorf. The new organisation was to have been called the International Confederation of Sports Organisations for the Disabled, but a vote chose the name International Paralympic Committee, with the sole right to organise the Paralympic Games (Brittain, 2016, p. 40; Hums & Pate, 2018, p. 173).',
 [BRI, HUMS]),
e('09-23', 1845,
 'El 23 de septiembre de 1845 se organizó en Nueva York el Knickerbocker Base Ball Club, con la participación de Alexander Joy Cartwright. Sus socios, hombres de la clase mercantil, jugaban con las reglas del llamado juego de Nueva York, y desde 1856 los clubes de estibadores, carreteros y albañiles hicieron del béisbol un deporte de las clases trabajadoras urbanas (Guttmann, 2004, p. 128).',
 'On 23 September 1845 the Knickerbocker Base Ball Club was organised in New York, with the participation of Alexander Joy Cartwright. Its members, men of the mercantile class, played by the rules of the so-called New York game, and from 1856 clubs of dockworkers, teamsters and bricklayers turned baseball into a sport of the urban working classes (Guttmann, 2004, p. 128).',
 [GUT04], 'beisbol'),
e('09-24', 1988,
 'El 24 de septiembre de 1988 el canadiense Ben Johnson ganó los 100 metros de los Juegos de Seúl con un récord del mundo de 9,79 segundos, ante unos 2.000 millones de telespectadores. Dos días después fue descalificado por consumo de estanozolol, y su caso se convirtió en el punto de inflexión del uso moderno de esteroides y en una humillación nacional para Canadá (Mars, 1999, p. 110).',
 'On 24 September 1988 the Canadian Ben Johnson won the 100 metres at the Seoul Games in a world record time of 9.79 seconds, before some two billion television viewers. Two days later he was disqualified for using stanozolol, and his case became the watershed of modern steroid use and a national embarrassment for Canada (Mars, 1999, p. 110).',
 [MARS]),
e('09-25', 1904,
 'El 25 de septiembre de 1904 el Motocycle-Club de France organizó en Dourdan, al suroeste de París, una Copa Internacional con pilotos de Alemania, Austria, Dinamarca, Francia y Gran Bretaña. Los desacuerdos sobre las condiciones de la carrera llevaron a esos cinco países a fundar en diciembre la Federación Internacional de Clubes Motociclistas, antecesora de la actual FIM (FIM, s. f.).',
 'On 25 September 1904 the Motocycle-Club de France organised an International Cup at Dourdan, south-west of Paris, with riders from Austria, Denmark, France, Germany and Great Britain. Disagreements over the racing conditions led these five countries to found in December the Fédération Internationale des Clubs Motocyclistes, forerunner of today\'s FIM (FIM, n.d.).',
 [R('FIM. (s. f.)')], 'motociclismo'),
e('09-26', 1861,
 'El 26 de septiembre de 1861 se celebró en Nagasaki una extravagante regata con botes de cuatro remeros, sampanes japoneses y casas flotantes, con la que al parecer comenzaron los deportes acuáticos de estilo occidental en Japón. El remo a la manera europea y estadounidense llegó en 1866, cuando los extranjeros residentes en Yokohama importaron una embarcación (Guttmann y Thompson, 2001, p. 75).',
 'On 26 September 1861 an outlandish regatta of four-oared gigs, Japanese sampans and houseboats was held in Nagasaki, and with it Western-style aquatic sports seem to have begun in Japan. Rowing in the European and American style arrived in 1866, when foreigners living in Yokohama imported a boat (Guttmann & Thompson, 2001, p. 75).',
 [GT01]),
e('09-27', 1958,
 'El 27 de septiembre de 1958, en el sexto congreso de la Confederación Internacional de Pesca Deportiva celebrado en Bruselas, diez federaciones nacionales de buceo acordaron crear una federación mundial propia. En enero de 1959 nació en Mónaco la Confédération Mondiale des Activités Subaquatiques, que eligió como primer presidente a Jacques-Yves Cousteau (Foret, 2024).',
 'On 27 September 1958, at the sixth congress of the International Confederation of Sport Fishing held in Brussels, ten national diving federations agreed to create a world federation of their own. In January 1959 the Confédération Mondiale des Activités Subaquatiques was founded in Monaco, and it elected Jacques-Yves Cousteau as its first president (Foret, 2024).',
 [R('Foret, A. (2024)')], 'actividades-subacuaticas'),
e('09-28', 1972,
 'El 28 de septiembre de 1972 Paul Henderson marcó, a treinta y cuatro segundos del final, el gol que dio a Canadá, en Moscú, la «Serie del Siglo» de hockey sobre hielo contra la Unión Soviética. Los profesionales de la NHL, que esperaban un triunfo fácil, habían sufrido derrotas humillantes, y el país volvió con la certeza de que su juego debía mejorar (Mott, 1999, p. 169).',
 'On 28 September 1972 Paul Henderson scored, with thirty-four seconds left, the goal in Moscow that gave Canada the ice hockey «Series of the Century» against the Soviet Union. The NHL professionals, who had expected an easy triumph, had suffered humiliating defeats, and the country came home aware that its game had to improve (Mott, 1999, p. 169).',
 [MOTT]),
e('09-29', 1961,
 'El 29 de septiembre de 1961 recibió la sanción real en Canadá la ley C-131, «An Act to Encourage Fitness and Amateur Sport». La norma simbolizó un compromiso nuevo, y a la vez renovado, del Gobierno federal con la administración del deporte y, en menor medida, con la condición física de la población (Morrow y Wamsley, 2010, p. 191).',
 'On 29 September 1961 Bill C-131, «An Act to Encourage Fitness and Amateur Sport», received royal assent in Canada. The law symbolised a new, and renewed, commitment by the federal government to involve itself in the administration of sport and, to a lesser extent, of the population\'s fitness (Morrow & Wamsley, 2010, p. 191).',
 [MOR]),
e('09-30', 1981,
 'El 30 de septiembre de 1981 Seúl obtuvo los Juegos Olímpicos de 1988. El proyecto, anunciado en 1979 junto con la candidatura a los Juegos Asiáticos de 1986, había nacido bajo el régimen de Park Chung-hee, y la organización de ambos acontecimientos aceleró de manera notable el deporte de élite en Corea del Sur (Ha y Mangan, 2003, pp. 189, 196).',
 'On 30 September 1981 Seoul was awarded the 1988 Olympic Games. The project, announced in 1979 together with the bid for the 1986 Asian Games, had been launched under Park Chung-hee\'s regime, and hosting both events greatly accelerated the momentum of elite sport in South Korea (Ha & Mangan, 2003, pp. 189, 196).',
 [HA]),
]

BAD = ['—', ' sino ', 'crucial', 'fascinante', ' clave', 'cabe destacar']
for mes, L in (('10', OCT), ('09', SEP)):
    for x in L:
        for lang in ('es', 'en'):
            n = len(x[lang].split())
            if not 35 <= n <= 70: print('PALABRAS', x['d'], lang, n)
        for b in BAD:
            if b in x['es'] or b in x['en']: print('ESTILO', x['d'], b)
        if not str(x['year']) in x['es']: print('AÑO', x['d'])
    L.sort(key=lambda x: x['d'])
    json.dump(L, open(os.path.join(H, f'efe_{mes}.json'), 'w'), ensure_ascii=False, indent=1)
    print(mes, len(L), 'guardadas')
