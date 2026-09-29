# uso: python3 ~/enc/getimg2.py <id> "<File title sin File:>"  -> descarga a img/enc/<id>.jpg|png e imprime el crédito en JSON
import sys,json,urllib.request,urllib.parse,re,os
UA={'User-Agent':'Historiapp/1.0 (aleiva@ucam.edu) educational'}
D=os.path.expanduser("~/mnt/ASIGNATURAS/Claude outputs/Historiapp/img/enc"); os.makedirs(D,exist_ok=True)
sid,title=sys.argv[1],sys.argv[2].replace('File:','')
u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',titles='File:'+title,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=900,format='json'))
pg=list(json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))['query']['pages'].values())[0]
ii=pg['imageinfo'][0]; m=ii['extmetadata']; src=ii.get('thumburl') or ii['url']
data=urllib.request.urlopen(urllib.request.Request(src,headers=UA),timeout=60).read()
ext='.png' if src.lower().endswith('.png') else '.jpg'
for e in ('.jpg','.png'):
  if os.path.exists(f"{D}/{sid}{e}") and e!=ext: os.rename(f"{D}/{sid}{e}",f"{D}/{sid}{e}.old")
open(f"{D}/{sid}{ext}",'wb').write(data)
st=lambda h: re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',h or '')).strip()
print(json.dumps({"src":f"img/enc/{sid}{ext}","autor_commons":st(m.get('Artist',{}).get('value'))[:150],"licencia_commons":st(m.get('LicenseShortName',{}).get('value')),"url":ii['descriptionurl'],"kb":len(data)//1024},ensure_ascii=False))
