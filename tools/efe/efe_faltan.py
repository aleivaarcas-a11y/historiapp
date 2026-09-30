import json
R="Recuperado el 30 de septiembre de 2026 de "; RE="Retrieved September 30, 2026, from "
N={
"03-30":dict(year=2001,enc="natacion",
 es="El 30 de marzo de 2001, en los campeonatos nacionales de primavera de Estados Unidos, celebrados en Austin, Michael Phelps ganó los 200 metros mariposa en 1:54.92 y rebajó el récord del mundo de Tom Malchow (1:55.18). Tenía quince años y fue el hombre más joven en batir un récord mundial de natación; la plusmarca de la prueba siguió en sus manos hasta 2019 (Lohn, 2021).",
 en="On 30 March 2001, at the United States Spring Nationals in Austin, Michael Phelps won the 200 metres butterfly in 1:54.92 and lowered Tom Malchow's world record (1:55.18). He was fifteen, the youngest man ever to break a world swimming record, and the record for the event stayed in his hands until 2019 (Lohn, 2021).",
 u="https://www.swimmingworldmagazine.com/news/on-this-date-15-year-old-michael-phelps-sets-first-world-record/",
 r="Lohn, J. ({d}). *On this date: 15-year-old Michael Phelps sets first world record*. Swimming World. ", d=("2021, 30 de marzo","2021, March 30")),
"04-30":dict(year=1993,enc="tenis",
 es="El 30 de abril de 1993, en los cuartos de final del torneo de Hamburgo, un espectador apuñaló por la espalda a Monica Seles, número uno del mundo, cuando ganaba a Magdalena Maleeva por 6-4 y 4-3. Seles tardó más de dos años en volver a competir, en agosto de 1995, y todavía ganó el Abierto de Australia de 1996, su noveno y último título de Grand Slam (Drucker, 2021).",
 en="On 30 April 1993, in the quarter-finals of the Hamburg tournament, a spectator stabbed Monica Seles, the world number one, in the back while she was leading Magdalena Maleeva 6-4, 4-3. Seles took more than two years to return to competition, in August 1995, and still won the 1996 Australian Open, her ninth and last Grand Slam title (Drucker, 2021).",
 u="https://www.tennis.com/news/articles/tbt-1993-hamburg-monica-seles-stabbing-changes-tennis-history",
 r="Drucker, J. ({d}). *TBT, 1993 Hamburg: Monica Seles' stabbing changes tennis history*. Tennis.com. ", d=("2021, 9 de abril","2021, April 9")),
"09-11":dict(year=2022,enc="tenis",
 es="El 11 de septiembre de 2022 el murciano Carlos Alcaraz ganó el US Open a Casper Ruud por 6-4, 2-6, 7-6 y 6-3. Con diecinueve años sumaba su primer título de Grand Slam y pasaba a ser el número uno más joven desde que existe la clasificación informática del tenis masculino (Trollope, 2022).",
 en="On 11 September 2022 Carlos Alcaraz, from Murcia, beat Casper Ruud 6-4, 2-6, 7-6, 6-3 to win the US Open. At nineteen he claimed his first Grand Slam title and became the youngest men's world number one since computer rankings began (Trollope, 2022).",
 u="https://ausopen.com/articles/news/alcaraz-arrives-us-open-champion-and-youngest-ever-world-no1",
 r="Trollope, M. ({d}). *Alcaraz arrives: US Open champion and youngest ever world No.1*. Australian Open. ", d=("2022, 12 de septiembre","2022, September 12")),
"12-03":dict(year=1967,enc="atletismo",
 es="El 3 de diciembre de 1967, en el maratón de Fukuoka (Japón), el australiano Derek Clayton corrió en 2:09:36 y fue el primer hombre en bajar de las dos horas y diez minutos, más de dos minutos por debajo del récord del japonés Morio Shigematsu (2:12:00, 1965). En 1969 volvió a rebajarlo, y aquella marca aguantó hasta que Rob de Castella la superó en 1981 (Hurst, 2009).",
 en="On 3 December 1967, at the Fukuoka marathon in Japan, the Australian Derek Clayton ran 2:09:36 and became the first man to break two hours and ten minutes, more than two minutes inside the record of Japan's Morio Shigematsu (2:12:00, 1965). He lowered it again in 1969, and that mark stood until Rob de Castella beat it in 1981 (Hurst, 2009).",
 u="https://worldathletics.org/news/news/on-40th-anniversary-of-first-sub-209-pioneeri",
 r="Hurst, M. ({d}). *On 40th anniversary of first sub-2:09, pioneering Clayton looks back on his marathon world records*. World Athletics. ", d=("2009, 30 de mayo","2009, May 30")),
"12-11":dict(year=1981,enc="boxeo",
 es="El 11 de diciembre de 1981, en un campo de béisbol de Nassau (Bahamas), Muhammad Ali, con treinta y nueve años, perdió por decisión a los diez asaltos ante Trevor Berbick en el último combate de su carrera. La velada, anunciada como «Drama in the Bahamas», estuvo tan mal organizada que hubo que conseguir a última hora un cencerro para marcar los asaltos (Hannigan, 2021).",
 en="On 11 December 1981, at a baseball field in Nassau (Bahamas), Muhammad Ali, aged thirty-nine, lost a ten-round decision to Trevor Berbick in the last fight of his career. The event, billed as the 'Drama in the Bahamas', was so poorly organised that a cowbell had to be found at the last minute to mark the rounds (Hannigan, 2021).",
 u="https://www.irishtimes.com/sport/other-sports/muhammad-ali-s-last-stand-and-the-sad-sorry-tale-of-trevor-berbick-s-demise-1.4750414",
 r="Hannigan, D. ({d}). *Muhammad Ali's last stand and the sad, sorry tale of Trevor Berbick's demise*. The Irish Times. ", d=("2021, 11 de diciembre","2021, December 11")),
"12-13":dict(year=1954,enc="futbol",
 es="El 13 de diciembre de 1954, bajo los focos recién instalados de Molineux y con la segunda parte en directo por la BBC, el Wolverhampton remontó un 0-2 ante el Honvéd de Budapest y ganó 3-2. La prensa británica llamó a los Wolves «campeones del mundo»; Gabriel Hanot, de *L'Équipe*, replicó que antes tendrían que medirse con los grandes clubes del continente, y de aquella polémica nació la Copa de Europa (Wolverhampton Wanderers FC, 2024).",
 en="On 13 December 1954, under Molineux's new floodlights and with the second half shown live by the BBC, Wolverhampton came back from 0-2 down against Honvéd of Budapest to win 3-2. The British press hailed Wolves as 'champions of the world'; Gabriel Hanot of *L'Équipe* replied that they would first have to face the great clubs of the continent, and the European Cup grew out of that dispute (Wolverhampton Wanderers FC, 2024).",
 u="https://www.wolves.co.uk/news/features/20241213-honved-54-the-night-european-football-was-born-at-molineux/",
 r="Wolverhampton Wanderers FC. ({d}). *Honved '54: The night European football was born at Molineux*. ", d=("2024, 13 de diciembre","2024, December 13")),
"12-24":dict(year=1914,enc="surf",
 es="El 24 de diciembre de 1914 el nadador hawaiano Duke Kahanamoku hizo una exhibición de surf en la playa de Freshwater, en Sídney, que la memoria australiana convirtió en el nacimiento del surf en el país. Osmond (2011) ha mostrado que en Sídney ya se montaban olas con tabla antes de su visita y que el relato fundacional agranda su papel por razones culturales.",
 en="On 24 December 1914 the Hawaiian swimmer Duke Kahanamoku gave a surfing exhibition at Freshwater beach in Sydney, which Australian memory turned into the birth of surfing in the country. Osmond (2011) has shown that surfboard riding already existed in Sydney before his visit and that the foundation story magnifies his role for cultural reasons.",
 ref="Osmond, G. (2011). Myth-making in Australian sport history: Re-evaluating Duke Kahanamoku's contribution to surfing. *Australian Historical Studies, 42*(2), 260-276. https://doi.org/10.1080/1031461X.2010.529922"),
"12-29":dict(year=2022,enc="futbol",
 es="El 29 de diciembre de 2022 murió en São Paulo, a los ochenta y dos años, Pelé, ganador de tres Copas del Mundo (1958, 1962 y 1970), la primera con diecisiete años. La UNESCO, que en 1994 lo había nombrado Campeón del Deporte, recordó su empeño en promover el deporte como herramienta de paz (Naciones Unidas, 2022).",
 en="On 29 December 2022 Pelé died in São Paulo, aged eighty-two, winner of three World Cups (1958, 1962 and 1970), the first at seventeen. UNESCO, which had named him a Champion for Sport in 1994, recalled his work to promote sport as a tool for peace (United Nations, 2022).",
 u="https://news.un.org/en/story/2022/12/1132087",
 r="{org}. ({d}). *UNESCO 'deeply saddened' over death of football legend, Pelé*. UN News. ", d=("2022, 29 de diciembre","2022, December 29"), org=("Naciones Unidas","United Nations")),
}
p="data/efemerides.json"; D=json.load(open(p,encoding="utf-8"))
for k,v in N.items():
    if "ref" in v: rs,re_=[v["ref"]],[v["ref"]]
    else:
        o=v.get("org",("",""))
        rs=[v["r"].format(d=v["d"][0],org=o[0])+R+v["u"]]; re_=[v["r"].format(d=v["d"][1],org=o[1])+RE+v["u"]]
    assert k not in D
    D[k]=dict(year=v["year"],es=v["es"],en=v["en"],refs=rs,refs_en=re_,enc=v["enc"])
D=dict(sorted(D.items()))
json.dump(D,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(D)); print(D["12-29"]["refs"], D["12-29"]["refs_en"])
