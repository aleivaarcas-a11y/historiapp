import sys,re,unicodedata
def n(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
name,pat=sys.argv[1],sys.argv[2]; ctx=int(sys.argv[3]) if len(sys.argv)>3 else 150; mx=int(sys.argv[4]) if len(sys.argv)>4 else 15
P=open(f'/root/enc/{name}.txt'.replace('/root',__import__('os').path.expanduser('~')),errors='ignore').read().split('\f')
k=0
for i,p in enumerate(P,1):
  t=re.sub(r'\s+',' ',p); nt=n(t)
  for m in re.finditer(n(pat),nt):
    print(f"[fís {i}] …{t[max(0,m.start()-ctx):m.end()+ctx]}…"); k+=1
    if k>=mx: sys.exit()
