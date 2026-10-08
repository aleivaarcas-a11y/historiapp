import unicodedata,sys,glob,re
n=lambda s:''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
files=sorted(glob.glob('ppt_texto/*.txt'))+['../../data/efemerides.json']+sorted(glob.glob('lote_*.json'))+sorted(glob.glob('reemplazos_*.json'))
T={f:n(open(f).read()) for f in files}
for k in sys.argv[1:]:
  kk=n(k); hits=[(f.split('/')[-1],T[f].count(kk)) for f in files if kk in T[f]]
  print(k,'->',hits)
