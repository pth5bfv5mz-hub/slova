import sys
p = sys.argv[1]; t = open(p).read()
def R(a, b, cnt=1):
    global t
    assert t.count(a) == cnt, (t.count(a), a[:90]); t = t.replace(a, b)

# settings: allow count 'all' and the old filter again
R("let cfg = {dir:'er', mode:'type', input:'no', blocks:[], count:20, perDay:10, voice:'on'};",
  "let cfg = {dir:'er', mode:'type', input:'no', blocks:[], count:20, perDay:10, voice:'on', filter:'smart'};")
R("if(![10,20,30,50].includes(cfg.count)) cfg.count = 20;",
  "if(![10,20,30,50,'all'].includes(cfg.count)) cfg.count = 20;\nif(!['smart','new','weak','all'].includes(cfg.filter)) cfg.filter = 'smart';")

# custom quiz = old behaviour (filters + count incl. «Все»)
i = t.index("/* тренировка по номерам"); j = t.index("\n}\n", t.index("function customQuiz(){")) + 3
t = t[:i] + r"""/* тест по настройкам: диапазон номеров, что спрашивать, сколько вопросов */
function pool(){ return cfg.blocks.length ? WORDS.filter(w => cfg.blocks.some(i => w.n>=BLOCKS[i][0] && w.n<=BLOCKS[i][1])) : WORDS; }
function customQuiz(){
  const items = [];
  for(const w of pool()){
    if(cfg.mode==='sent' && !sentOf(w)) continue;
    const dir = dirFor(), r = peek(w.key,dir);
    let weight;
    if(cfg.filter==='new'){ if(r) continue; weight=1; }
    else if(cfg.filter==='weak'){ if(!r || status(w.key,dir)!==3) continue; weight=1+r.x; }
    else if(cfg.filter==='all') weight = 1;
    else weight = !r ? 2.5 : r.s>=MASTER ? 0.35 : 1 + r.x*1.2 - r.s*0.25 + Math.min(3,(Date.now()-r.t)/DAY/3);
    items.push({w, dir, weight:Math.max(.05,weight)});
  }
  const n = cfg.count==='all' ? items.length : Math.min(cfg.count, items.length);
  const out = [];
  while(out.length<n && items.length){
    let tot = items.reduce((a,b)=>a+b.weight,0), r = Math.random()*tot, i = 0;
    for(; i<items.length-1; i++){ r -= items[i].weight; if(r<=0) break; }
    const x = items.splice(i,1)[0]; out.push({w:x.w, dir:x.dir});
  }
  return out;
}
""" + t[j:]

# home: keep «Сегодня», restore the old settings panel exactly
i = t.index("  <div class=\"panel\">\n    <div class=\"group\"><div class=\"lbl\">Направление</div>")
j = t.index("  view.querySelectorAll('.chip').forEach(c => c.onclick = () => {", i)
t = t[:i] + r"""  <div class="panel">
    <div class="group"><div class="lbl">Направление</div><div class="chips">
      ${chip('dir','er','Английский → русский',cfg.dir==='er')}${chip('dir','re','Русский → английский',cfg.dir==='re')}${chip('dir','mix','Вперемешку',cfg.dir==='mix')}</div></div>
    <div class="group"><div class="lbl">Что тренировать</div><div class="chips">
      ${chip('mode','type','Слова',cfg.mode==='type')}${chip('mode','sent','Предложения',cfg.mode==='sent')}</div>${cfg.mode==='sent'?'<div class="hint">Каждое слово в своём предложении, нужное слово подчёркнуто.</div>':''}</div>
    <div class="group"><div class="lbl">Как отвечать</div><div class="chips">
      ${chip('input','no','Вспомнить и нажать «Проверить»',cfg.input==='no')}${chip('input','yes','Писать ответ',cfg.input==='yes')}</div>
      <div class="hint">${cfg.input==='no'?'Переводишь в уме, жмёшь «Проверить», видишь правильный ответ и отмечаешь «Верно» или «Неверно».':'Пишешь перевод, потом видишь правильный ответ и отмечаешь «Верно» или «Неверно».'}</div></div>
    <div class="group"><div class="lbl">Озвучка</div><div class="chips">
      ${chip('voice','on','Включена',cfg.voice==='on')}${chip('voice','off','Выключена',cfg.voice==='off')}</div>
      <div class="hint">${TTS?'Слово или предложение читается вслух, когда появляется, и ответ после «Проверить». Если звука нет, проверь беззвучный режим и громкость.':'Этот браузер не умеет читать вслух.'}</div></div>
    <div class="group"><div class="lbl">Какие слова (номера по таблице)</div><div class="chips">
      ${chip('blk','all','Все 1–652',!cfg.blocks.length)}${BLOCKS.map((b,i)=>chip('blk',i,b[0]+'–'+b[1],cfg.blocks.includes(i))).join('')}</div>
      <div class="hint">В выбранных: ${pool().length} слов, выучено ${pool().filter(w => status(w.key, cfg.dir==='re'?'re':'er')===2).length}. Можно отметить несколько диапазонов.</div></div>
    <div class="group"><div class="lbl">Что спрашивать</div><div class="chips">
      ${chip('filter','smart','Умный подбор',cfg.filter==='smart')}${chip('filter','new','Только новые',cfg.filter==='new')}${chip('filter','weak','Только ошибки',cfg.filter==='weak')}${chip('filter','all','Все подряд',cfg.filter==='all')}</div>
      <div class="hint">${{smart:'Чаще спрашивает слова с ошибками и те, что давно не повторялись.',new:'Слова, которых ещё не было в тестах в этом направлении.',weak:'Слова, где последний ответ был неверным.',all:'Случайные слова без учёта прогресса.'}[cfg.filter]}</div></div>
    <div class="group"><div class="lbl">Сколько вопросов</div><div class="chips">
      ${[10,20,30,50].map(n=>chip('count',n,n,cfg.count===n)).join('')}${chip('count','all','Все',cfg.count==='all')}</div></div>
    <button class="big" id="custom">Начать тест</button>
    <div class="hint" id="startmsg"></div>
  </div>`;
""" + t[j:]
R("    else if(g==='count'||g==='perDay') cfg[g] = +v;", "    else if(g==='count') cfg.count = v==='all' ? 'all' : +v;\n    else if(g==='perDay') cfg.perDay = +v;")
R("  document.getElementById('moreSet').ontoggle = e => { moreOpen = e.target.open; };\n", "")
R("  on('custom', () => startQuiz(customQuiz()));",
  "  on('custom', () => { const items = customQuiz(); if(!items.length){ document.getElementById('startmsg').textContent = cfg.filter==='weak' ? 'Ошибок в этих словах пока нет. Выбери другой режим.' : cfg.filter==='new' ? 'Новых слов в этом диапазоне не осталось.' : 'Нет слов для теста.'; return; } startQuiz(items); });")
# «новых слов в день» moves into the «Сегодня» card as one compact row
R("""    <div class="hint">После верного ответа слово вернётся через 1, 3, 7, 16 и 30 дней. После ошибки повторится в этой же тренировке и завтра.</div>""",
  """    <div class="hint">После верного ответа слово вернётся через 1, 3, 7, 16 и 30 дней. После ошибки повторится в этой же тренировке и завтра.</div>
    <div class="group"><div class="lbl">Новых слов в день</div><div class="chips">${[5,10,15,20].map(n=>chip('perDay',n,n,cfg.perDay===n)).join('')}</div></div>""")
open(p, 'w').write(t)
print('ok')
