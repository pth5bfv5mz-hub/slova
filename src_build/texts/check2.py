import json,re,sys
p=sys.argv[1]; d=json.load(open(p)); bad=[]
N=lambda s:re.sub(r'\s+',' ',s).strip()
for i,par in enumerate(d['paragraphs']):
  s=par.get('s')
  if not s or not all(isinstance(x,list) and len(x)==2 and x[0].strip() and x[1].strip() for x in s): bad.append((i,'missing/empty s')); continue
  if N(' '.join(x[0] for x in s))!=N(par['en']): bad.append((i,'sentences do not rebuild paragraph'))
print('paragraphs',len(d['paragraphs']),'sentences',sum(len(x.get('s') or []) for x in d['paragraphs']),'problems',bad[:10],len(bad))
