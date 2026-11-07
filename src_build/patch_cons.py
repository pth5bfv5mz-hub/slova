import sys
p=sys.argv[1]; t=open(p).read()
def R(a,b):
    global t
    assert t.count(a)==1,a[:80]; t=t.replace(a,b)
R("""<div class="chips">${chip('lvl','all','Все',textLvl==='all')}${chip('lvl','B1','B1',textLvl==='B1')}${chip('lvl','A2','A2–B1',textLvl==='A2')}</div>""",
  """<div class="chips">${chip('lvl','all','Все',textLvl==='all')}${TEXTS.some(x=>x.cat==='cons')?chip('lvl','cons','Конспирология',textLvl==='cons'):''}${chip('lvl','B1','B1',textLvl==='B1')}${chip('lvl','A2','A2–B1',textLvl==='A2')}</div>""")
R("""${TEXTS.filter(tx=> textLvl==='all' || (textLvl==='B1') === (tx.level==='B1')).map(tx=>card(tx)).join('')}""",
  """${TEXTS.filter(tx=> textLvl==='all' || (textLvl==='cons' ? tx.cat==='cons' : (textLvl==='B1') === (tx.level==='B1'))).map(tx=>card(tx)).join('')}""")
open(p,'w').write(t); print('ok')
