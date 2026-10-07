#!/usr/bin/env python3
"""Historiapp: ajuste para iPad de 13 pulgadas (07-10-2026). A partir de 1000 px de ancho amplía un 12 % el contenido
y la barra inferior; a partir de 1200 px (13" en horizontal) la cabecera y la barra ocupan todo el ancho.
Idempotente: si el bloque ya está, lo sustituye. Copia previa: tools/index_antes_ipad13.html"""
import os,re,shutil
R=os.path.dirname(os.path.abspath(__file__))+'/..'
p=os.path.join(R,'index.html')
if not os.path.exists(os.path.join(R,'tools/index_antes_ipad13.html')): shutil.copy(p,os.path.join(R,'tools/index_antes_ipad13.html'))
CSS='''/* iPad13-INI */
@media (min-width:1000px){
  #app main{zoom:1.12}
  #tabbar{zoom:1.1}
}
@media (min-width:1200px){
  #app{max-width:none}
  #tabbar{max-width:none}
  main>*{max-width:1080px}
}
/* iPad13-FIN */
'''
s=open(p,encoding='utf-8').read()
s=re.sub(r'/\* iPad13-INI \*/.*?/\* iPad13-FIN \*/\n','',s,flags=re.S)
assert s.count('</style>')==1
s=s.replace('</style>',CSS+'</style>',1)
open(p,'w',encoding='utf-8').write(s); print('ok')
