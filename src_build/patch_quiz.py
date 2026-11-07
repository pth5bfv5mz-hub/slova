import sys
p = sys.argv[1]; t = open(p).read()
def R(a, b, cnt=1):
    global t
    assert t.count(a) == cnt, (t.count(a), a[:90]); t = t.replace(a, b)

# CSS
R(".tcard.cont{border-color:var(--accent)}", """.tcard.cont{border-color:var(--accent)}
.tq .qtext{font:500 21px/1.35 var(--f-body)}
.tq .qru{font-size:15px;color:var(--muted)}
.opt small{display:block;color:var(--muted);font-size:13px;margin-top:3px}
.opt span{min-width:0}
.qsum{display:flex;flex-direction:column;gap:6px;padding:10px 0;border-top:1px solid var(--line);font-size:15px}
.qsum:first-child{border-top:0}
.qsum .ok{color:var(--good)} .qsum .no{color:var(--bad)}""")

# routing
R("  else if(tab==='texts') reading ? renderReader() : renderTexts();",
  "  else if(tab==='texts') reading ? (TQ && TQ.id===reading ? renderTQ() : renderReader()) : renderTexts();")

# list badge
R("""${!extra&&r?.done?'<span class="badge done">Прочитано</span>':!extra&&r?'<span class="badge go">Начато</span>':''}""",
  """${!extra&&r?.done?'<span class="badge done">Прочитано</span>':!extra&&r?'<span class="badge go">Начато</span>':''}${!extra&&r?.quiz?`<span class="badge ${r.quiz.best>=5?'done':'go'}">Тест ${r.quiz.best}/6</span>`:''}""")

# reader end panel: quiz button first
R("""      <div class="row"><button class="big" id="trainTx">Тренировать слова текста</button><button class="ghost" id="doneTx">${st.done?'Прочитано ✓':'Отметить прочитанным'}</button></div>""",
  """      ${tx.quiz?`<div class="group"><button class="big" id="quizTx">Тест на понимание · 6 вопросов</button>${st.quiz?`<div class="hint">Лучший результат: ${st.quiz.best} из 6.</div>`:'<div class="hint">Проверь, всё ли понял в истории.</div>'}</div>`:''}
      <div class="row"><button class="${tx.quiz?'ghost':'big'}" id="trainTx">Тренировать слова текста</button><button class="ghost" id="doneTx">${st.done?'Прочитано ✓':'Отметить прочитанным'}</button></div>""")
R("""  document.getElementById('trainTx').onclick = () => startQuiz(quizFromWords(twords, 30));""",
  """  document.getElementById('trainTx').onclick = () => startQuiz(quizFromWords(twords, 30));
  const qb = document.getElementById('quizTx'); if(qb) qb.onclick = () => startTQ(tx);""")

# quiz engine
R("const SAY_SVG = ", r"""/* ---------- тест на понимание текста ---------- */
let TQ = null;
function startTQ(tx){
  closeSheet(); markRead(tx);
  TQ = {id:tx.id, i:0, right:0, ans:[], tr:false,
    qs: tx.quiz.map(q => { const ord = shuffle([0,1,2,3]); return {...q, ord}; })};
  render(); window.scrollTo(0,0);
}
function markRead(tx){ const st = S.read[tx.id] ||= {t:Date.now()}; if(!st.done){ st.done = true; st.d = Date.now(); save(); } }
function renderTQ(){
  const tx = TEXTS.find(t=>t.id===TQ.id);
  const head = `<div class="row" style="flex-wrap:nowrap"><button class="ghost" id="tqBack" style="flex:0 0 auto">← К тексту</button></div>
    <div class="group"><span class="g" style="font:600 11px var(--f-mono);letter-spacing:.04em;text-transform:uppercase;color:var(--accent)">Тест на понимание</span><h1 lang="en" style="font:500 22px/1.25 var(--f-display);margin:0">${esc(tx.title_en)}</h1></div>`;
  if(TQ.i >= TQ.qs.length){
    const n = TQ.qs.length, r = TQ.right;
    const st = S.read[tx.id] ||= {t:Date.now()};
    if(!TQ.saved){ TQ.saved = true; st.quiz = {best: Math.max(st.quiz?.best||0, r), last:r, t:Date.now()}; save(); }
    view.innerHTML = `<div class="panel tq">${head}
      <div class="res">${r} / ${n}<small>${r===n?'Всё понял правильно!':r>=4?'Хорошее понимание текста.':'Стоит перечитать трудные места.'}</small></div>
      <div class="list">${TQ.qs.map((q,k)=>{ const ok = TQ.ans[k]===q.answer;
        return `<div class="qsum"><div lang="en"><b class="${ok?'ok':'no'}">${ok?'✓':'✗'}</b> ${esc(q.q)}</div>${ok?'':`<div class="hint">Правильно: <span lang="en">${esc(q.options[q.answer])}</span> (${esc(q.options_ru[q.answer])})</div><div class="hint">${esc(q.explain_ru)}</div>`}</div>`; }).join('')}</div>
      <div class="row"><button class="big" id="tqList">К списку текстов</button><button class="ghost" id="tqAgain">Пройти ещё раз</button></div></div>`;
    document.getElementById('tqList').onclick = () => { TQ=null; reading=null; render(); window.scrollTo(0,0); };
    document.getElementById('tqAgain').onclick = () => startTQ(tx);
    document.getElementById('tqBack').onclick = () => { TQ=null; render(); };
    return;
  }
  const q = TQ.qs[TQ.i], picked = TQ.ans[TQ.i];
  const done = picked !== undefined;
  view.innerHTML = `<div class="panel tq" style="gap:14px">${head}
    <div class="qtop"><span>Вопрос ${TQ.i+1} из ${TQ.qs.length}</span><span>Верно: ${TQ.right}</span></div>
    <div class="bar"><i style="width:${TQ.i/TQ.qs.length*100}%"></i></div>
    <div class="qtext" lang="en">${esc(q.q)}</div>
    ${TQ.tr?`<div class="qru">${esc(q.q_ru)}</div>`:''}
    <div class="opts" style="grid-template-columns:1fr">${q.ord.map((oi,k)=>`<button class="opt${done&&oi===q.answer?' ok':''}${done&&oi===picked&&oi!==q.answer?' no':''}" data-o="${oi}"${done?' disabled':''}><b>${'ABCD'[k]}</b><span lang="en">${esc(q.options[oi])}${TQ.tr?`<small>${esc(q.options_ru[oi])}</small>`:''}</span></button>`).join('')}</div>
    ${done?`<div class="fb ${picked===q.answer?'ok':'no'}">${picked===q.answer?'Верно!':'Неверно.'} <strong>${esc(q.explain_ru)}</strong></div><button class="big" id="tqNext">${TQ.i+1<TQ.qs.length?'Дальше':'Результат'}</button>`
      :`<button class="ghost" id="tqTr">${TQ.tr?'Скрыть перевод':'Показать перевод'}</button>`}
  </div>`;
  document.getElementById('tqBack').onclick = () => { TQ=null; render(); };
  view.querySelectorAll('.opt').forEach(b => b.onclick = () => { if(TQ.ans[TQ.i]!==undefined) return; const o=+b.dataset.o; TQ.ans[TQ.i]=o; if(o===q.answer) TQ.right++; renderTQ(); document.getElementById('tqNext')?.scrollIntoView({block:'nearest'}); });
  const tr = document.getElementById('tqTr'); if(tr) tr.onclick = () => { TQ.tr = !TQ.tr; renderTQ(); };
  const nx = document.getElementById('tqNext'); if(nx) nx.onclick = () => { TQ.i++; renderTQ(); window.scrollTo(0,0); };
}
const SAY_SVG = """)
# leaving texts tab or list resets the quiz
R("closeSheet(); if(b.dataset.tab==='texts' && tab==='texts') reading=null;", "closeSheet(); if(b.dataset.tab==='texts' && tab==='texts'){ reading=null; TQ=null; }")
R("  const markDone = () => { if(st.done) return; st.done = true; st.d = Date.now(); save(); const b=document.getElementById('doneTx'); if(b) b.textContent='Прочитано ✓'; };",
  "  const markDone = () => { if(st.done) return; markRead(tx); const b=document.getElementById('doneTx'); if(b) b.textContent='Прочитано ✓'; };")

# progress line
R("Прочитано текстов: ${readN} из ${TEXTS.length}.", "Прочитано текстов: ${readN} из ${TEXTS.length}${quizN?`, тестов по текстам пройдено: ${quizN}, средний результат ${quizAvg} из 6`:''}.")
R("  const readN = TEXTS.filter(x=>S.read[x.id]?.done).length;",
  "  const readN = TEXTS.filter(x=>S.read[x.id]?.done).length;\n  const qz = TEXTS.map(x=>S.read[x.id]?.quiz).filter(Boolean), quizN = qz.length, quizAvg = quizN ? (qz.reduce((a,b)=>a+b.best,0)/quizN).toFixed(1) : 0;")
open(p, 'w').write(t)
print('ok')
