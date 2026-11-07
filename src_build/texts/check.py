import json,re,sys
p=sys.argv[1]; d=json.load(open(p)); import os; a=json.load(open(os.path.join(os.path.dirname(p),os.path.basename(p).replace('t','assign',1))))
en=' '.join(x['en'] for x in d['paragraphs'])
toks={t.lower() for t in re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?",en)}
toks={t.replace('’',"'") for t in toks}
miss=sorted(toks-set(d['gloss']))
nwords=len(re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?",en))
assigned={x['n'] for x in a['words']}; used=set(d['vocab'].values())
badv=[f for f in d['vocab'] if f not in toks]
print('words',nwords,'paragraphs',len(d['paragraphs']),'assigned used',len(assigned&used),'/',len(assigned),'missing gloss',miss[:40],len(miss),'bad vocab forms',badv)
