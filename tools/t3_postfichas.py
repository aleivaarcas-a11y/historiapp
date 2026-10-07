#!/usr/bin/env python3
"""Tema 3: títulos de diapositivas sin título en las notas, reconstrucción de fichas e infografías ES/EN (07-10-2026)."""
import re,json,os,subprocess,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/..'
os.chdir(H)
es=json.load(open('tools/fuentes/t3_slides.json')); en=json.load(open(os.path.expanduser('~/t3en_slides.json')))
OWN={12,15,16,43,50,59,65,102}
def fix(path,sl):
    t=open(path,encoding='utf-8').read()
    for s in sl:
        if s['title']: continue
        n=s['slide']; tt=(s['paras'][0] if n in OWN else '(cont.)')
        t=re.sub(rf"^### Diapositiva {n} ·[^\n]*$",f"### Diapositiva {n} · {tt}",t,flags=re.M)
    open(path,'w',encoding='utf-8').write(t)
if '--titulos' in sys.argv:
    fix('tools/fuentes/t3_notas.md',es); fix('tools/fuentes/t3_notas_en.md',en)
INF={"s21_1":"relevo_egipto_creta","s24_1":"relevo_creta_olimpia","s31_1":"sociedad_ateniense","s38_2":"elide_pisa","s42_1":"olimpia_antes_juegos","s43_1":"origen_juegos_hipotesis","s52_1":"circuito_panhelenico","s54_1":"gobierno_olimpia","s55_1":"calendario_juegos","s57_1":"mapa_elide_olimpia","s63_2":"valor_premios","s66_1":"pruebas_cronologia","s67_1":"programa_juegos","s77_1":"cuadro_carreras","s79_1":"pentatlon_regla","s80_1":"pentatlon_gillet","s93_1":"cuadro_combate","s103_1":"mujer_olimpia","s109_1":"final_juegos"}
ONE={"s22_2":"linea_creta_micenas","s29_1":"periodos_grecia","s65_1":"pruebas_olimpia"}
def conv(src,dst):
    im=Image.open(src).convert('RGBA'); bg=Image.new('RGB',im.size,'white'); bg.paste(im,mask=im.split()[-1]); bg.thumbnail((1600,1600)); bg.save(dst,quality=82,optimize=True)
def find(d,k):
    for f in os.listdir(d):
        if f.split('.')[0]==k: return os.path.join(d,f)
for k,n in INF.items():
    conv(find(os.path.expanduser('~/t3img_es'),k),f'img/t3/{n}.jpg'); conv(find(os.path.expanduser('~/t3img_en'),k),f'img/t3/{n}_en.jpg')
for k,n in ONE.items(): conv(find(os.path.expanduser('~/t3img_es'),k),f'img/t3/{n}.jpg')
subprocess.run(['cp','tools/tema03_vacio.json','data/tema03.json'])
subprocess.run([sys.executable,'tools/construir_fichas.py','tools/fuentes/t3_slides.json','data/tema03.json','img/t3','tools/imgmap.json','tools/fuentes/t3_notas.md','tools/fuentes/t3_notas_en.md'],check=True)
d=json.load(open('data/tema03.json'))
d['fichas']=[f for f in d['fichas'] if not all(110<=x<=114 for x in f['slides'])]
for k,f in enumerate(d['fichas'],1): f['code']=f"H3·{k:02d}"
for f in d['fichas']:
    for sn in f['slides']:
        for k,n in INF.items():
            if int(k[1:].split('_')[0])==sn:
                f['images'].append({"src":f"img/t3/{n}.jpg","caption":{},"lang":"es"}); f['images'].append({"src":f"img/t3/{n}_en.jpg","caption":{},"lang":"en"})
        for k,n in ONE.items():
            if int(k[1:].split('_')[0])==sn: f['images'].append({"src":f"img/t3/{n}.jpg","caption":{}})
import construir_fichas as CF
ENS={x['slide']:x for x in en}
for f in d['fichas']:
    if not f['body']['en']:
        ps=[]
        for sn in f['slides']:
            ps+= [p.strip() for p in ENS[sn]['paras'] if len(p.strip())>3 and not CF.is_ref(p.strip()) and p.strip().lower()!=f['title']['en'].lower() and not p.strip().isdigit()]
        f['body']['en']=ps
json.dump(d,open('data/tema03.json','w'),ensure_ascii=False,indent=1)
for f in d['fichas']: print(f['code'],f['slides'],f['title']['es'][:38],'|',f['title']['en'][:34],len(f['images']),len(f['body']['es']),len(f['body']['en']))
