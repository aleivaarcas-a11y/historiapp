import sys,re,os
P=open(os.path.expanduser(f'~/enc/{sys.argv[1]}.txt'),errors='ignore').read().split('\f')
a,b=int(sys.argv[2]),int(sys.argv[3])
for i in range(a,b+1):
  t=re.sub(r'https?://\S+','[url]',P[i-1]); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
  print(f"=== p.{i}\n{t.strip()}")
