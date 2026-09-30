#!/usr/bin/env python3
"""Uso: python3 commons.py buscar "consulta" [n]   |   python3 commons.py info "File:Nombre.jpg"
Busca ficheros en Wikimedia Commons y muestra licencia, autor, descripción y tamaño."""
import sys,json,urllib.request,urllib.parse,re,time
UA={"User-Agent":"Historiapp/1.0 (aleiva@ucam.edu) educational"}
API="https://commons.wikimedia.org/w/api.php?"
def get(params):
    for i in range(6):
        try:
            r=urllib.request.urlopen(urllib.request.Request(API+urllib.parse.urlencode(params),headers=UA),timeout=30); return json.load(r)
        except Exception as e: time.sleep(20*(i+1) if '429' in str(e) else 3*(i+1))
    raise SystemExit("error de red")
def clean(x): return re.sub(r"<[^>]+>","",x or "").strip()[:200]
def info(titles):
    d=get({"action":"query","titles":"|".join(titles),"prop":"imageinfo","iiprop":"url|extmetadata|size|mime","format":"json"})
    for p in d["query"]["pages"].values():
        ii=(p.get("imageinfo") or [{}])[0]; m=ii.get("extmetadata",{})
        g=lambda k:clean(m.get(k,{}).get("value",""))
        print(json.dumps({"title":p.get("title"),"licencia":g("LicenseShortName"),"autor":g("Artist"),"fecha":g("DateTimeOriginal"),"desc":g("ImageDescription"),"w":ii.get("width"),"h":ii.get("height"),"mime":ii.get("mime"),"page":ii.get("descriptionurl")},ensure_ascii=False))
if sys.argv[1]=="buscar":
    n=int(sys.argv[3]) if len(sys.argv)>3 else 8
    d=get({"action":"query","list":"search","srsearch":sys.argv[2]+" filetype:bitmap","srnamespace":6,"srlimit":n,"format":"json"})
    t=[x["title"] for x in d["query"]["search"]]
    if t: info(t)
    else: print("sin resultados")
else: info([sys.argv[2]])
