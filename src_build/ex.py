import openpyxl,sys,re,json
wb=openpyxl.load_workbook(sys.argv[1],data_only=True); ws=wb.active
items=[]
for row in ws.iter_rows(values_only=True):
  row=list(row)
  for i,c in enumerate(row):
    if isinstance(c,str) and re.match(r'^\s*\d+\s*\.',c):
      ru=row[i+1] if i+1<len(row) else None
      m=re.match(r'^\s*(\d+)\s*\.\s*(.*)$',c)
      n=int(m.group(1)); en=m.group(2).strip()
      tr=None
      t=re.search(r'\s*\(([^)]*)\)\s*$',en)
      if t and re.search('[а-яё]',t.group(1),re.I): tr=t.group(1).strip(); en=en[:t.start()].strip()
      items.append([n,en,(ru or '').strip(),tr])
items.sort()
fix={'healting':'healing','shoud':'should','pensil':'pencil','accesible':'accessible'}
rufix={413:('mist',None),340:(None,'тайна'),565:(None,'передавать (чувства, мысли)'),514:(None,'крах/рухнуть')}
out=[]
for n,en,ru,tr in items:
  en=fix.get(en,en)
  if n in rufix:
    a,b=rufix[n]; en=a or en; ru=b or ru
  ru=re.sub(r'\s+',' ',ru)
  ru=ru[0].lower()+ru[1:] if ru else ru
  en=en[0].lower()+en[1:]
  d={'n':n,'en':en,'ru':ru}
  if tr: d['tr']=tr
  out.append(d)
print(len(out),[x['n'] for x in out][:3], max(x['n'] for x in out), file=sys.stderr)
nums=[x['n'] for x in out]; print('missing',sorted(set(range(1,653))-set(nums)),'dups',[k for k in set(nums) if nums.count(k)>1],file=sys.stderr)
from collections import Counter
c=Counter(x['en'].lower() for x in out); print('dup en',[k for k,v in c.items() if v>1],file=sys.stderr)
print('empty',[x for x in out if not x['ru']],file=sys.stderr)
json.dump(out,open('words.json','w'),ensure_ascii=False,separators=(',',':'))
