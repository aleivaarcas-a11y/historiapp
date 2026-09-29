import sys,json,urllib.request,urllib.parse,re,time
UA={'User-Agent':'Historiapp/1.0 (aleiva@ucam.edu) educational'}
def api(**p):
  p.update(format='json'); u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)
  return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
def strip(h): return re.sub(r'<[^>]+>','',h or '').strip()[:80]
for q in sys.argv[1:]:
  r=api(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=6,prop='imageinfo',iiprop='url|size|extmetadata')
  print('##',q)
  for pg in sorted(r.get('query',{}).get('pages',{}).values(),key=lambda x:x.get('index',0)):
    ii=pg['imageinfo'][0]; m=ii.get('extmetadata',{})
    print(f" {pg['title'][5:]} | {ii['width']}x{ii['height']} | {strip(m.get('LicenseShortName',{}).get('value'))} | {strip(m.get('Artist',{}).get('value'))}")
  time.sleep(1)
