#!/usr/bin/env python3
"""Tema 5 en Historiapp (24-11-2026): ajusta los modos al PPT vigente del Tema 5 (cambios de Alex del 23-24/11 en las
diapositivas 15, 30, 42 y 43): Bodhidharma deja de fecharse en 480 d. C. (la diapositiva dice finales del siglo V d. C. y
fundación del monasterio hacia 495 d. C.), y salen el sumo femenino de 1873, las 82 técnicas, los primeros combates del
siglo VII y el yokozuna de 1909, que ya no están en las diapositivas. Uso: python3 tools/t5_parche_modos_24-11.py"""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
d = json.load(open('data/tema05.json'))
def rp(obj, lang, a, b):
    assert a in obj[lang], (a, obj[lang][:80]); obj[lang] = obj[lang].replace(a, b)
c = d['cards']
rp(c[8]['claim'], 'es', 'hacia el año 480 d. C.', 'a finales del siglo V d. C.')
rp(c[8]['claim'], 'en', 'around AD 480', 'in the late 5th century AD')
rp(c[29]['explain'], 'es', 'Los primeros combates datan del siglo VII d. C., dentro de rituales agrícolas para pedir buenas cosechas.', 'A la vez, el sumo formaba parte de los ritos de los santuarios para pedir buenas cosechas.')
rp(c[29]['explain'], 'en', 'The first bouts date from the 7th century AD, within agricultural rituals to ask for good harvests.', 'At the same time, sumo formed part of the shrine rites to ask for good harvests.')
for o in (c[30]['explain'], d['myths'][10]['explain']):
    rp(o, 'es', ' Thompson (1998) muestra lo mismo con el yokozuna, que la tradición remonta al siglo XVII d. C. y que no fue un rango oficial hasta 1909 d. C.', '')
    rp(o, 'en', ' Thompson (1998) shows the same with the yokozuna, which tradition traces back to the 17th century AD and which was not an official rank until AD 1909.', '')
d['glossary'] = [g for g in d['glossary'] if g['term']['es'] != 'Yokozuna']
d['timeline'][3]['items'][1] = {'label': {'es': 'Se funda el monasterio budista de Shaolin', 'en': 'The Buddhist monastery of Shaolin is founded'}, 'year': 495, 'date': {'es': 'H. 495 d. C.', 'en': 'c. AD 495'}}
d['timeline'][3]['items'].sort(key=lambda x: x['year'])
rp(d['myths'][0]['claim'], 'es', 'hacia el año 480 d. C.', 'a finales del siglo V d. C.')
rp(d['myths'][0]['claim'], 'en', 'around AD 480', 'in the late 5th century AD')
q = d['quiz']
rp(q[8]['options'][1], 'es', 'hacia el año 480 d. C.', 'a finales del siglo V d. C.')
rp(q[8]['options'][1], 'en', 'around AD 480', 'in the late 5th century AD')
q[20]['options'][1] = {'es': 'Servía para elegir a los mejores soldados del ejército imperial, que después luchaban en la guardia de palacio',
                       'en': 'It served to select the best soldiers of the imperial army, who then fought in the palace guard'}
v = d['videos'][8]['more']
rp(v, 'es', ', y Thompson (1998) muestra lo mismo con el yokozuna, que la tradición remonta al siglo XVII d. C.', '')
rp(v, 'en', ', and Thompson (1998) shows the same for the yokozuna, which tradition traces back to the 17th century AD', '')
R = d['mapa']['ramas']
n6 = R[0]['nodos'][6]['x']
rp(n6['es'][0], 'v', 'Según el mito, Bodhidharma, un monje indio llegado hacia el año 480 d. C., enseñó', 'Según la tradición, Bodhidharma, un monje indio de finales del siglo V d. C., enseñó')
rp(n6['en'][0], 'v', 'According to the myth, Bodhidharma, an Indian monk who arrived around AD 480, taught', 'According to tradition, Bodhidharma, an Indian monk of the late 5th century AD, taught')
n2 = R[1]['nodos'][2]
rp(n2['d'], 'es', ', y el sumo femenino se convirtió en un espectáculo de pago para un público masculino.', '.')
rp(n2['d'], 'en', ", and women's sumo became a paid spectacle for a male audience.", '.')
for L in ('es', 'en'):
    n2['x'][L] = [x for x in n2['x'][L] if '1873' not in x['v']]
n11 = R[1]['nodos'][11]
rp(n11['d'], 'es', ' y en rituales agrícolas, y se convirtió en un arte marcial de 82 técnicas cuyo fin es', ' y en los ritos de los santuarios, y su fin es')
rp(n11['d'], 'en', ' and in agricultural rituals, and it became a martial art of 82 techniques whose aim is', ' and in shrine rites, and its aim is')
for L, t in (('es', 'Las crónicas oficiales, escritas en 720 d. C., sitúan su origen en un combate legendario ante el emperador, y a la vez el sumo formaba parte de los ritos de los santuarios para pedir buenas cosechas.'),
             ('en', 'The official chronicles, written in AD 720, place its origin in a legendary bout before the emperor, and at the same time sumo formed part of the shrine rites to ask for good harvests.')):
    xs = n11['x'][L]; i = [k for k, x in enumerate(xs) if '82' in x['v']][0]; xs[i]['v'] = t
n12 = R[1]['nodos'][12]
rp(n12['d'], 'es', ', y la misma lógica explica el yokozuna, que no fue un rango oficial hasta 1909 d. C.', '')
rp(n12['d'], 'en', ', and the same logic explains the yokozuna, which was not an official rank until AD 1909', '')
for L in ('es', 'en'):
    for x in n12['x'][L]:
        x['v'] = x['v'].replace(', y Thompson (1998) muestra lo mismo con el yokozuna, que la tradición remonta al siglo XVII d. C. y que no fue un rango oficial hasta 1909 d. C.', '.').replace(', and Thompson (1998) shows the same with the yokozuna, which tradition traces back to the 17th century AD and which was not an official rank until AD 1909.', '.')
json.dump(d, open('data/tema05.json', 'w'), ensure_ascii=False, indent=1)
s = json.dumps(d, ensure_ascii=False)
print('quedan:', [w for w in ('1873', ' 82 ', 'AD 480', '480 d. C.', 'yokozuna', '1909') if w in s])
