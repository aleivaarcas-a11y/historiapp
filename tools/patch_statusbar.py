#!/usr/bin/env python3
"""iOS 26+: con status-bar-style «black-translucent» el sistema pinta un difuminado (Liquid Glass) sobre la cabecera
de la app instalada, y ningún CSS lo quita. Se pasa a «default»: la barra de estado es opaca (color de theme-color)
y la página empieza debajo. Se retira el relleno de reserva de patch_safe.py, que ya no hace falta.
Uso: python3 tools/patch_statusbar.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
s = s.replace('<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
              '<meta name="apple-mobile-web-app-status-bar-style" content="default">')
s = s.replace('  if(ios&&standalone&&portrait&&h<20) h = H>=874?62 : H>=852?59 : H>=812?50 : 20;\n', '')
assert 'content="default"' in s and 'H>=874' not in s
open(p, 'w', encoding='utf-8').write(s)
print('ok')
