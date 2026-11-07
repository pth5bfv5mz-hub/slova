import json,sys
p=sys.argv[1]; d=json.load(open(p)); bad=[]
if len(d)!=6: bad.append(f'need 6 questions, got {len(d)}')
for i,q in enumerate(d):
  for k in ('q','q_ru','options','options_ru','answer','explain_ru'):
    if k not in q: bad.append((i,'missing',k))
  if len(q.get('options',[]))!=4 or len(q.get('options_ru',[]))!=4: bad.append((i,'need 4 options + 4 options_ru'))
  if not isinstance(q.get('answer'),int) or not 0<=q.get('answer',-1)<4: bad.append((i,'answer must be 0-3'))
  if len(set(o.strip().lower() for o in q.get('options',[])))<4: bad.append((i,'duplicate options'))
ans=[q.get('answer') for q in d]
print(p,'questions',len(d),'answers',ans,'problems',bad)
