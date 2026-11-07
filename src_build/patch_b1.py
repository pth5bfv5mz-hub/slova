import sys
p=sys.argv[1]; t=open(p).read()
a="${chip('lvl','B1','B1',textLvl==='B1')}${chip('lvl','A2','A2–B1',textLvl==='A2')}"
assert t.count(a)==1; t=t.replace(a,"")
open(p,'w').write(t); print('ok')
