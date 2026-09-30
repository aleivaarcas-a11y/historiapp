#!/usr/bin/env python3
"""Uso: python3 getimg.py MM-DD "File:Nombre.jpg"  -> descarga img/MM-DD.jpg (1200 px de ancho, JPEG)"""
import sys,json,urllib.request,urllib.parse,io,time
from PIL import Image
UA={"User-Agent":"Historiapp/1.0 (aleiva@ucam.edu) educational"}
k,t=sys.argv[1],sys.argv[2]
q="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":t,"prop":"imageinfo","iiprop":"url","iiurlwidth":1200,"format":"json"})
for i in range(6):
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(q,headers=UA),timeout=30)); break
    except Exception as e: time.sleep(20*(i+1) if '429' in str(e) else 3)
ii=list(d["query"]["pages"].values())[0]["imageinfo"][0]; u=ii.get("thumburl") or ii["url"]
for i in range(4):
    try: data=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read(); break
    except Exception as e: time.sleep(20*(i+1) if '429' in str(e) else 4*(i+1))
im=Image.open(io.BytesIO(data)).convert("RGB")
if im.width>1200: im=im.resize((1200,int(im.height*1200/im.width)))
import os; D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../img/efe"); os.makedirs(D,exist_ok=True); im.save(f"{D}/{k}.jpg","JPEG",quality=82,optimize=True)
print("ok",k,im.size,ii["descriptionurl"] if "descriptionurl" in ii else "")
