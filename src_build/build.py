import json,glob,re,sys
ts=[]
import re as _re
for f in sorted(glob.glob('texts/t*.json')):
  m=_re.fullmatch(r'texts/t(\d+)\.json', f)
  if not m or int(m.group(1))>int(sys.argv[1]): continue
  t=json.load(open(f))
  d={k:t[k] for k in ['id','title_en','title_ru','genre','summary_ru','gloss','vocab']}
  d['level']='B1'
  if t.get('cat'): d['cat']=t['cat']
  import os
  qf=f'texts/quiz/q{t["id"]:02d}.json'
  if os.path.exists(qf): d['quiz']=json.load(open(qf))
  d['paragraphs']=[{k:p[k] for k in ('en','ru','s') if k in p} for p in t['paragraphs']]
  ts.append(d)
ts.sort(key=lambda x:(x['level']!='B1',x['id']))
h=open('tmpl.html').read()
h=h.replace('__TEXTS__',json.dumps(ts,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
open('slova-test.html','w').write(h); print(len(ts),'texts',len(h.encode())//1024,'KB')
