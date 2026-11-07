import sys, re
p = sys.argv[1]; t = open(p).read()
def R(a, b, cnt=1):
    global t
    assert t.count(a) == cnt, (t.count(a), a[:80]); t = t.replace(a, b)
def between(start, end, new, keep_end=True):
    global t
    i = t.index(start); j = t.index(end, i)
    t = t[:i] + new + t[j:]

# ---------- CSS ----------
R(".sync{font-size:12px;color:var(--muted)}", """.sync{font-size:13px;color:var(--muted)}
.nb{display:inline-block;min-width:18px;padding:0 5px;margin-left:4px;border-radius:9px;background:var(--mark);color:#1a1400;font:700 11px/18px var(--f-body);vertical-align:1px}
.today{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.today div{background:var(--paper);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:2px;min-width:0}
.today b{font:700 26px var(--f-display);font-variant-numeric:tabular-nums}
.today span{font-size:12px;color:var(--muted)}
.quick{display:flex;gap:8px;flex-wrap:wrap}.quick>*{flex:1 1 150px}
details>summary{cursor:pointer;color:var(--accent);font-weight:600;font-size:15px;list-style:none;padding:4px 0}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:'▸ ';}details[open]>summary::before{content:'▾ ';}
details[open]>summary{margin-bottom:12px}
details .group+.group{margin-top:14px}
.pill{font:600 11px var(--f-body);padding:3px 8px;border-radius:999px;white-space:nowrap}
.p-new{background:var(--paper);color:var(--muted);border:1px solid var(--line)}
.p-learning{background:var(--mid-bg);color:var(--ink)}
.p-learned{background:var(--good-bg);color:var(--good)}
.p-hard{background:var(--bad-bg);color:var(--bad)}
.dl{cursor:pointer}
.dd{padding:4px 0 14px;display:flex;flex-direction:column;gap:10px}
.dd .ex{background:var(--paper);border-radius:10px;padding:10px 12px;font-size:15px;line-height:1.45}
.dd mark{background:none;color:inherit;font-weight:600;text-decoration:underline;text-decoration-color:var(--mark);text-decoration-thickness:2px;text-underline-offset:5px}
.dd .ex small{display:block;color:var(--muted);margin-top:4px;font-size:14px}
.sm{padding:8px 12px;font-size:14px;flex:0 0 auto}
.acts{display:flex;gap:8px;flex-wrap:wrap}
.tw.m{text-decoration:underline;text-decoration-color:var(--accent);text-decoration-thickness:2px;text-underline-offset:5px}
.tcard.cont{border-color:var(--accent)}
.ovr{height:12px;background:var(--line);border-radius:6px;overflow:hidden;display:flex}
.ovr i{display:block;height:100%}
textarea.paste{width:100%;min-height:80px;background:var(--paper);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:10px;font:13px var(--f-mono)}""")

# ---------- header / nav ----------
R("""    <div class="sync" id="sync">Прогресс сохраняется на этом устройстве</div>
""", "")
R("""    <button id="tab-test" role="tab" aria-selected="true" data-tab="test">Тест</button>
    <button id="tab-texts" role="tab" aria-selected="false" data-tab="texts">Тексты</button>
    <button id="tab-stats" role="tab" aria-selected="false" data-tab="stats">Статистика</button>
    <button id="tab-dict" role="tab" aria-selected="false" data-tab="dict">Словарь</button>""",
"""    <button id="tab-test" role="tab" aria-selected="true" data-tab="test">Учить<span class="nb" id="dueBadge" hidden></span></button>
    <button id="tab-texts" role="tab" aria-selected="false" data-tab="texts">Тексты</button>
    <button id="tab-dict" role="tab" aria-selected="false" data-tab="dict">Словарь</button>
    <button id="tab-stats" role="tab" aria-selected="false" data-tab="stats">Прогресс</button>""")

# ---------- storage ----------
R("const blank = () => ({v:1, updated:0, words:{}, days:{}, sessions:[], read:{}});",
  "const blank = () => ({v:1, updated:0, words:{}, days:{}, sessions:[], read:{}, mine:{}, flag:{}, lastRead:0});")
R("read:x.read&&typeof x.read==='object'?x.read:{}}; }",
  "read:x.read&&typeof x.read==='object'?x.read:{}, mine:x.mine&&typeof x.mine==='object'?x.mine:{}, flag:x.flag&&typeof x.flag==='object'?x.flag:{}, lastRead:+x.lastRead||0}; }")
R("function setSync(t){ document.getElementById('sync').textContent = t; }",
  "let SYNC = 'Прогресс хранится на этом устройстве.';\nfunction setSync(t){ SYNC = t; }\nlet lazyT = null; function saveLazy(){ clearTimeout(lazyT); lazyT = setTimeout(save, 1500); }")

# ---------- record with spaced repetition ----------
R("""function record(key,dir,ok){
  const r = rec(key,dir); if(ok){ r.c++; r.s++; } else { r.x++; r.s=0; } r.t = Date.now();
  const d = S.days[today()] ||= {r:0,w:0,q:0}; ok ? d.r++ : d.w++;
  save();
}""", """function record(key,dir,ok){
  const isNew = !peek(key,dir);
  const r = rec(key,dir), b0 = isNew ? 0 : boxOf(r); if(ok){ r.c++; r.s++; } else { r.x++; r.s=0; } r.t = Date.now(); srs(r, ok, b0);
  const d = S.days[today()] ||= {r:0,w:0,q:0}; ok ? d.r++ : d.w++; if(isNew) d.nw = (d.nw||0)+1;
  save();
}
/* общее состояние слова: new | learning | learned | hard */
function wstate(w){
  if(S.flag[w.key]) return 'hard';
  const rs = [peek(w.key,'er'), peek(w.key,'re')].filter(Boolean);
  if(!rs.length) return 'new';
  if(rs.some(r => r.x>0 && r.s<2)) return 'hard';
  if(rs.every(r => r.s>=MASTER)) return 'learned';
  return 'learning';
}
function markKnown(w){
  for(const d of ['er','re']){ const r = rec(w.key,d); r.s = Math.max(r.s,MASTER); r.b = Math.max(boxOf(r),4); r.d = dayStart()+INTERVALS[r.b]*DAY; r.t = Date.now(); }
  delete S.flag[w.key]; save();
}
function plural(n,a,b,c){ const m=n%10, h=n%100; return m===1&&h!==11?a : m>=2&&m<=4&&(h<12||h>14)?b : c; }""")

# ---------- settings / SRS / quiz builders ----------
between("/* ---------- настройки и подбор вопросов ---------- */", "/* ---------- экраны ---------- */", r"""/* ---------- настройки, интервальное повторение, подбор карточек ---------- */
const SET_KEY = 'slova-test-settings';
let cfg = {dir:'er', mode:'type', input:'no', blocks:[], count:20, perDay:10, voice:'on'};
try{ Object.assign(cfg, JSON.parse(localStorage.getItem(SET_KEY)||'{}')); }catch(e){}
if(cfg.mode!=='type' && cfg.mode!=='sent') cfg.mode = 'type';
if(cfg.input!=='yes') cfg.input = 'no';
if(cfg.voice!=='off') cfg.voice = 'on';
if(!['er','re','mix'].includes(cfg.dir)) cfg.dir = 'er';
if(![5,10,15,20].includes(cfg.perDay)) cfg.perDay = 10;
if(![10,20,30,50].includes(cfg.count)) cfg.count = 20;
if(!Array.isArray(cfg.blocks)) cfg.blocks = [];
function saveCfg(){ try{ localStorage.setItem(SET_KEY, JSON.stringify(cfg)); }catch(e){} }

const DAY = 864e5;
const INTERVALS = [0,1,3,7,16,30]; // через сколько дней слово вернётся после верного ответа
function dayStart(t=Date.now()){ const d=new Date(t); d.setHours(0,0,0,0); return d.getTime(); }
function boxOf(r){ return r.b ?? Math.min(5, r.s||0); }
function dueOf(r){ return r.d ?? ((r.t||0) + INTERVALS[boxOf(r)]*DAY); }
function srs(r, ok, b0=boxOf(r)){ const b = ok ? Math.min(5, b0+1) : 0; r.b = b; r.d = b ? dayStart()+INTERVALS[b]*DAY : Date.now(); }

/* свои слова, сохранённые из текстов */
function mineWords(){ return Object.entries(S.mine).map(([key,m]) => ({n:0, key, en:m.en, ru:m.ru, mine:true, sent: m.se ? {en:m.se, ru:m.sr||'', ek:m.f||m.en, rk:''} : null})); }
function allWords(){ return WORDS.concat(mineWords()); }
function sentOf(w){ return w.sent || SENT[w.n] || null; }
function numTag(w){ return w.mine ? 'мои' : w.n; }
function dirFor(){ return cfg.dir==='mix' ? (Math.random()<.5?'er':'re') : cfg.dir; }
function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }

/* план на сегодня: слова, которым пора повториться, и немного новых */
const MAX_REVIEW = 40;
function plan(){
  const now = Date.now(), dirs = cfg.dir==='mix' ? ['er','re'] : [cfg.dir], due = [], cand = [];
  for(const w of allWords()){
    if(cfg.mode==='sent' && !sentOf(w)) continue;
    const lack = [];
    for(const d of dirs){ const r = peek(w.key,d); if(!r) lack.push(d); else if(dueOf(r)<=now) due.push({w, dir:d, b:boxOf(r)}); }
    if(lack.length) cand.push({w, dir:lack[Math.floor(Math.random()*lack.length)], seen:!!S.words[w.key]});
  }
  cand.sort((a,b) => (b.w.mine?1:0)-(a.w.mine?1:0) || (a.seen?1:0)-(b.seen?1:0) || a.w.n-b.w.n);
  const nw = S.days[today()]?.nw || 0;
  const freshLeft = due.length >= MAX_REVIEW ? 0 : Math.max(0, cfg.perDay - nw);
  shuffle(due).sort((a,b) => a.b-b.b);
  return {due:due.slice(0,MAX_REVIEW), dueTotal:due.length, fresh:cand.slice(0,freshLeft), cand};
}
function quizFromWords(ws, limit=1e9){
  return shuffle(ws.filter(w => cfg.mode!=='sent' || sentOf(w))).slice(0,limit).map(w => ({w, dir:dirFor()}));
}
/* тренировка по номерам: чаще попадаются слова с ошибками и давно не виденные */
function customQuiz(){
  const base = cfg.blocks.length ? WORDS.filter(w => cfg.blocks.some(i => w.n>=BLOCKS[i][0] && w.n<=BLOCKS[i][1])) : WORDS;
  const items = [];
  for(const w of base){
    if(cfg.mode==='sent' && !sentOf(w)) continue;
    const dir = dirFor(), r = peek(w.key,dir);
    const weight = !r ? 2.5 : r.s>=MASTER ? 0.35 : 1 + r.x*1.2 - r.s*0.25 + Math.min(3,(Date.now()-r.t)/DAY/3);
    items.push({w, dir, weight:Math.max(.05,weight)});
  }
  const out = [];
  while(out.length<cfg.count && items.length){
    let tot = items.reduce((a,b)=>a+b.weight,0), r = Math.random()*tot, i = 0;
    for(; i<items.length-1; i++){ r -= items[i].weight; if(r<=0) break; }
    const x = items.splice(i,1)[0]; out.push({w:x.w, dir:x.dir});
  }
  return out;
}

""")

# ---------- render() ----------
R("""function render(){
  document.querySelectorAll('nav button').forEach(b => b.setAttribute('aria-selected', b.dataset.tab===tab));""",
"""function render(){
  window.onscroll = null;
  document.querySelectorAll('nav button').forEach(b => b.setAttribute('aria-selected', b.dataset.tab===tab));
  const P = plan(), nb = document.getElementById('dueBadge'), n = P.due.length + P.fresh.length;
  nb.textContent = n; nb.hidden = !n || !!Q;""")

# ---------- home ----------
between("function renderSetup(){", "function renderQuestion(){", r"""let moreOpen = false;
function renderSetup(){
  const P = plan(), total = P.due.length + P.fresh.length;
  const td = S.days[today()], answered = (td?.r||0)+(td?.w||0);
  const ws = allWords(), hardN = ws.filter(w => wstate(w)==='hard').length, mineN = Object.keys(S.mine).length;
  const streak = streakDays();
  view.innerHTML = `<div class="panel">
    <div class="lbl">Сегодня</div>
    <div class="today"><div><b>${P.dueTotal}</b><span>повторить</span></div><div><b>${P.fresh.length}</b><span>${plural(P.fresh.length,'новое слово','новых слова','новых слов')}</span></div><div><b>${streak}</b><span>${plural(streak,'день','дня','дней')} подряд</span></div></div>
    ${total ? `<button class="big" id="go">Начать · ${total} ${plural(total,'карточка','карточки','карточек')}</button>`
      : `<div class="fb ok">На сегодня всё повторено.${answered?` Ответов сегодня: ${answered}.`:''}</div>${P.cand.length?`<button class="ghost" id="more10">Выучить ещё ${Math.min(10,P.cand.length)} новых слов</button>`:''}`}
    <div class="hint">После верного ответа слово вернётся через 1, 3, 7, 16 и 30 дней. После ошибки повторится в этой же тренировке и завтра.</div>
  </div>
  ${hardN||mineN ? `<div class="quick">${hardN?`<button class="ghost" id="qhard">Сложные слова · ${hardN}</button>`:''}${mineN?`<button class="ghost" id="qmine">Мои слова · ${mineN}</button>`:''}</div>` : ''}
  <div class="panel">
    <div class="group"><div class="lbl">Направление</div><div class="chips">${chip('dir','er','EN → RU',cfg.dir==='er')}${chip('dir','re','RU → EN',cfg.dir==='re')}${chip('dir','mix','Вперемешку',cfg.dir==='mix')}</div></div>
    <div class="group"><div class="lbl">Карточки</div><div class="chips">${chip('mode','type','Слова',cfg.mode==='type')}${chip('mode','sent','Предложения',cfg.mode==='sent')}</div></div>
    <div class="group"><div class="lbl">Ответ</div><div class="chips">${chip('input','no','Вспомнить в уме',cfg.input==='no')}${chip('input','yes','Написать',cfg.input==='yes')}</div></div>
    <details id="moreSet"${moreOpen?' open':''}><summary>Ещё настройки</summary>
      <div class="group"><div class="lbl">Новых слов в день</div><div class="chips">${[5,10,15,20].map(n=>chip('perDay',n,n,cfg.perDay===n)).join('')}</div></div>
      <div class="group"><div class="lbl">Озвучка</div><div class="chips">${chip('voice','on','Включена',cfg.voice==='on')}${chip('voice','off','Выключена',cfg.voice==='off')}</div>${TTS?'':'<div class="hint">Этот браузер не умеет читать вслух.</div>'}</div>
      <div class="group"><div class="lbl">Тренировка по номерам из таблицы</div>
        <div class="chips">${chip('blk','all','Все',!cfg.blocks.length)}${BLOCKS.map((b,i)=>chip('blk',i,b[0]+'–'+b[1],cfg.blocks.includes(i))).join('')}</div>
        <div class="chips">${[10,20,30,50].map(n=>chip('count',n,n+' слов',cfg.count===n)).join('')}</div>
        <button class="ghost" id="custom">Начать тренировку по номерам</button>
        <div class="hint">Дополнительная практика, план на сегодня не меняет. Чаще попадаются слова с ошибками.</div></div>
    </details>
  </div>`;
  view.querySelectorAll('.chip').forEach(c => c.onclick = () => {
    const g=c.dataset.g, v=c.dataset.v;
    if(g==='blk'){ if(v==='all') cfg.blocks=[]; else { const i=+v; cfg.blocks = cfg.blocks.includes(i)?cfg.blocks.filter(x=>x!==i):[...cfg.blocks,i].sort((a,b)=>a-b); } }
    else if(g==='count'||g==='perDay') cfg[g] = +v;
    else cfg[g]=v;
    saveCfg(); render();
  });
  document.getElementById('moreSet').ontoggle = e => { moreOpen = e.target.open; };
  const on = (id,f) => { const el=document.getElementById(id); if(el) el.onclick=f; };
  on('go', () => startQuiz(shuffle([...P.due, ...P.fresh]).map(({w,dir})=>({w,dir}))));
  on('more10', () => startQuiz(P.cand.slice(0,10).map(({w,dir})=>({w,dir}))));
  on('qhard', () => startQuiz(quizFromWords(ws.filter(w=>wstate(w)==='hard'), 30)));
  on('qmine', () => startQuiz(quizFromWords(mineWords(), 30)));
  on('custom', () => startQuiz(customQuiz()));
}
function startQuiz(items){
  if(!items.length) return;
  Q = {items, i:0, right:0, wrong:[], mode:cfg.mode, input:cfg.input==='yes', started:Date.now(), answered:false};
  (S.days[today()] ||= {r:0,w:0,q:0}).q++; save();
  closeSheet(); tab='test'; render(); window.scrollTo(0,0);
}
""")

# ---------- quiz screen tweaks ----------
R("  if(!it.opts && Q.mode==='choice') it.opts = options(w,dir);\n", "")
R("  const sent = Q.mode==='sent' && SENT[w.n];", "  const sent = Q.mode==='sent' && sentOf(w);")
R("<span class=\"dirtag\">${DIRS[dir]} · №${w.n}</span>", "<span class=\"dirtag\">${DIRS[dir]} · ${w.mine?'мои слова':'№'+w.n}${it.re?' · повтор':''}</span>")
R("""      : Q.mode==='choice'
        ? `<div class="opts">${it.opts.map((o,k)=>`<button class="opt" data-k="${k}"><b>${k+1}</b><span>${esc(o.label)}</span></button>`).join('')}</div>`
        : `<form""", """      : `<form""")
R("""  } else if(Q.mode==='choice'){
    view.querySelectorAll('.opt').forEach(b => b.onclick = () => answerChoice(+b.dataset.k));
  } else {""", "  } else {")
R("""<div class="row"><button class="ghost" id="quit">Закончить тест</button></div>""", """<div class="row"><button class="ghost" id="quit">Закончить</button></div>""")
R("function correctText(w,dir){ return dir==='er' ? w.ru : w.en; }\n", "")
R("  const nb = document.getElementById('next'); nb.onclick = next; if(Q.mode==='choice') nb.focus({preventScroll:true});",
  "  const nb = document.getElementById('next'); nb.onclick = next;")
R("function score(ok,it){ Q.answered = true; record(it.w.key,it.dir,ok); if(ok) Q.right++; else Q.wrong.push(it); }",
  "/* ошибку повторяем ещё раз в конце этой же тренировки */\nfunction requeue(it){ if(!it.re) Q.items.push({w:it.w, dir:it.dir, re:true}); }\nfunction score(ok,it){ Q.answered = true; record(it.w.key,it.dir,ok); if(!ok) requeue(it); if(it.re) return; if(ok) Q.right++; else Q.wrong.push(it); }")
i = t.index("function answerChoice(k){"); j = t.index("function answerType(val){")
t = t[:i] + t[j:]
R("function scoreSent(it, ok, wordOk){ Q.answered = true; record(it.w.key, it.dir, wordOk); if(ok) Q.right++; else Q.wrong.push(it); }",
  "function scoreSent(it, ok, wordOk){ Q.answered = true; record(it.w.key, it.dir, wordOk); if(!ok) requeue(it); if(it.re) return; if(ok) Q.right++; else Q.wrong.push(it); }")
t = t.replace("SENT[w.n]", "sentOf(w)").replace("function sentOf(w){ return w.sent || sentOf(w) || null; }", "function sentOf(w){ return w.sent || SENT[w.n] || null; }")
R("""    <div class="row">${Q.wrong.length?'<button class="big" id="redo">Повторить ошибки</button>':''}<button class="${Q.wrong.length?'ghost':'big'}" id="again">Новый тест</button></div>
  </div>`;
  const redo = document.getElementById('redo'); if(redo) redo.onclick = () => { const ws = Q.wrong.map(x=>x.w); Q=null; startQuiz(ws); };
  document.getElementById('again').onclick = () => { Q=null; render(); };""",
"""    <div class="row"><button class="big" id="again">Готово</button>${Q.wrong.length?'<button class="ghost" id="redo">Ещё раз ошибки</button>':''}</div>
  </div>`;
  const redo = document.getElementById('redo'); if(redo) redo.onclick = () => { const ws = Q.wrong.map(x=>x.w); Q=null; startQuiz(quizFromWords(ws)); };
  document.getElementById('again').onclick = () => { Q=null; render(); window.scrollTo(0,0); };""")
R("""${Q.wrong.map(({w})=>`<div class="li"><div class="w"><span class="num">${w.n}</span>""", """${Q.wrong.map(({w})=>`<div class="li"><div class="w"><span class="num">${numTag(w)}</span>""")
R("""  if(Q.mode==='choice' && !Q.answered && /^[1-4]$/.test(e.key)) answerChoice(+e.key-1);
  else if(!Q.input""", "  if(!Q.input")

# ---------- progress ----------
between("/* ---------- статистика ---------- */", "/* ---------- тексты ---------- */", r"""/* ---------- прогресс ---------- */
function streakDays(){ let n=0; const d=new Date(); if(!S.days[today(d)]?.r && !S.days[today(d)]?.w) d.setDate(d.getDate()-1);
  for(;;){ const k=today(d); const x=S.days[k]; if(x && (x.r+x.w)>0){ n++; d.setDate(d.getDate()-1);} else break; } return n; }
let pendingImport = null;
function renderStats(){
  let R=0,W=0; for(const k in S.days){ R+=S.days[k].r||0; W+=S.days[k].w||0; }
  const tot=R+W, acc = tot?Math.round(R/tot*100):0;
  const ws = allWords(), c = {new:0,learning:0,learned:0,hard:0}; ws.forEach(w => c[wstate(w)]++);
  const dirM = d => WORDS.filter(w => status(w.key,d)===2).length;
  const days=[]; for(let i=13;i>=0;i--){ const d=new Date(); d.setDate(d.getDate()-i); const k=today(d); days.push({k, d, r:S.days[k]?.r||0, w:S.days[k]?.w||0}); }
  const max = Math.max(10, ...days.map(x=>x.r+x.w)); const nice = Math.ceil(max/10)*10;
  const Wd=380,H=170,L=30,B=24,T=10, bw=(Wd-L-6)/14;
  const y = v => T + (H-T-B)*(1-v/nice);
  let svg = `<svg viewBox="0 0 ${Wd} ${H}" role="img" aria-label="Ответы за 14 дней">`;
  for(const t of [0,nice/2,nice]){ svg+=`<line x1="${L}" x2="${Wd}" y1="${y(t)}" y2="${y(t)}" stroke="var(--line)"/><text x="${L-6}" y="${y(t)+4}" text-anchor="end" font-size="12" fill="var(--muted)" font-family="JetBrains Mono,monospace">${t}</text>`; }
  days.forEach((x,i)=>{ const cx=L+i*bw+3, w=bw-6;
    if(x.r) svg+=`<rect x="${cx}" y="${y(x.r)}" width="${w}" height="${y(0)-y(x.r)}" rx="2" fill="var(--good)"><title>${x.k}: верно ${x.r}</title></rect>`;
    if(x.w) svg+=`<rect x="${cx}" y="${y(x.r+x.w)}" width="${w}" height="${y(x.r)-y(x.r+x.w)}" rx="2" fill="var(--bad)"><title>${x.k}: ошибок ${x.w}</title></rect>`;
    if(i%3===1||i===13) svg+=`<text x="${cx+w/2}" y="${H-6}" text-anchor="middle" font-size="12" fill="${i===13?'var(--ink)':'var(--muted)'}" font-family="JetBrains Mono,monospace">${x.d.getDate()}.${String(x.d.getMonth()+1).padStart(2,'0')}</text>`;
  });
  svg+='</svg>';
  const readN = TEXTS.filter(x=>S.read[x.id]?.done).length;
  const fmt = t => new Date(t).toLocaleString('ru-RU',{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'});
  const pct = n => (n/ws.length*100).toFixed(2)+'%';
  view.innerHTML = `<div class="panel">
    <div class="today"><div><b>${c.learned}</b><span>выучено из ${ws.length}</span></div><div><b>${c.learning+c.hard}</b><span>в изучении</span></div><div><b>${streakDays()}</b><span>дней подряд</span></div></div>
    <div class="ovr" aria-label="Выучено ${c.learned}, в изучении ${c.learning}, сложных ${c.hard}"><i style="width:${pct(c.learned)};background:var(--good)"></i><i style="width:${pct(c.learning)};background:var(--mark)"></i><i style="width:${pct(c.hard)};background:var(--bad)"></i></div>
    <div class="legend" style="flex-wrap:wrap"><span><i style="background:var(--good)"></i>выучено</span><span><i style="background:var(--mark)"></i>изучаю</span><span><i style="background:var(--bad)"></i>сложные · ${c.hard}</span></div>
    <div class="hint">Всего ответов: ${tot}, верных ${acc}%. Выучено с английского: ${dirM('er')}, с русского: ${dirM('re')}. Прочитано текстов: ${readN} из ${TEXTS.length}. Слово считается выученным после ${MASTER} верных ответов подряд.</div>
    ${c.hard?`<button class="ghost" id="openHard">Открыть сложные слова (${c.hard})</button>`:''}
  </div>
  <div class="panel">
    <div class="lbl">Последние 14 дней</div>
    <div class="chart">${svg}</div>
    <div class="legend"><span><i style="background:var(--good)"></i>верно</span><span><i style="background:var(--bad)"></i>ошибки</span></div>
  </div>
  <div class="panel">
    <div class="lbl">Прогресс по номерам таблицы</div>
    <div class="blocks">${BLOCKS.map(([a,b])=>{ const bw2=WORDS.filter(w=>w.n>=a&&w.n<=b); let m=0,s=0,e=0; bw2.forEach(w=>{ const st=wstate(w); if(st==='learned')m++; else if(st==='hard')e++; else if(st==='learning')s++; }); const T2=bw2.length||1;
      return `<div class="blk"><span>${a}–${b}</span><span class="track"><i style="width:${m/T2*100}%;background:var(--good)"></i><i style="width:${s/T2*100}%;background:var(--mark)"></i><i style="width:${e/T2*100}%;background:var(--bad)"></i></span><span style="text-align:right">${Math.round(m/T2*100)}%</span></div>`; }).join('')}</div>
  </div>
  <div class="panel">
    <details><summary>История тренировок</summary>
    ${S.sessions.length?`<div class="list">${S.sessions.slice(0,20).map(s=>`<div class="li"><div class="w">${fmt(s.t)}<small>${s.dir==='mix'?'вперемешку':DIRS[s.dir]} · ${s.mode==='sent'?'предложения':'слова'}</small></div><div class="n">${s.r} / ${s.n}<br>${Math.round(s.r/s.n*100)}%</div></div>`).join('')}</div>`:'<div class="empty">Здесь будут результаты каждой тренировки.</div>'}
    </details>
  </div>
  <div class="panel">
    <div class="lbl">Резервная копия</div>
    <div class="hint">${esc(SYNC)} Сохрани копию в «Файлы» или iCloud, чтобы перенести прогресс на другой телефон или восстановить его.</div>
    <div class="acts"><button class="ghost sm" id="exp">Сохранить файл</button><button class="ghost sm" id="cpy">Скопировать текстом</button><button class="ghost sm" id="imp">Загрузить из файла</button></div>
    <input type="file" id="impFile" accept=".json,application/json,text/plain" hidden>
    <details><summary>Восстановить из текста</summary><textarea class="paste" id="pasteBox" placeholder="Вставь сюда скопированный текст резервной копии"></textarea><button class="ghost sm" id="pasteGo" style="margin-top:8px">Восстановить</button></details>
    <div id="bkMsg" class="hint"></div>
  </div>
  <div class="panel">
    <details><summary>Сбросить прогресс</summary>
      <div class="hint">Удаляет весь прогресс, статистику и мои слова. Отменить нельзя.</div>
      <div class="row" id="resetrow" style="margin-top:10px"><button class="ghost" id="reset">Сбросить</button></div>
    </details>
  </div>`;
  const msg = t => { document.getElementById('bkMsg').textContent = t; };
  const oh = document.getElementById('openHard'); if(oh) oh.onclick = () => { dfilt='hard'; dq=''; tab='dict'; render(); window.scrollTo(0,0); };
  document.getElementById('exp').onclick = () => {
    try{ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([JSON.stringify(S)],{type:'application/json'})); a.download=`slova-progress-${today()}.json`; document.body.appendChild(a); a.click(); a.remove();
      msg('Файл подготовлен. Если он не сохранился, нажми «Скопировать текстом» и сохрани текст в Заметках.'); }catch(e){ msg('Не получилось сохранить файл. Нажми «Скопировать текстом».'); }
  };
  document.getElementById('cpy').onclick = () => {
    const txt = JSON.stringify(S);
    const fallback = () => { const box=document.getElementById('pasteBox'); box.closest('details').open=true; box.value=txt; box.select(); msg('Текст выделен в поле ниже: скопируй его вручную.'); };
    try{ navigator.clipboard.writeText(txt).then(()=>msg('Скопировано. Вставь текст в Заметки и сохрани.'), fallback); }catch(e){ fallback(); }
  };
  const askImport = (raw) => {
    let d; try{ d = JSON.parse(raw); }catch(e){ msg('Это не похоже на резервную копию: текст не читается.'); return; }
    if(!d || typeof d!=='object' || !d.words){ msg('В файле нет прогресса слов.'); return; }
    pendingImport = sane(d);
    document.getElementById('bkMsg').innerHTML = `Заменить текущий прогресс копией (${Object.keys(pendingImport.words).length} слов с историей)? <span class="acts" style="margin-top:8px"><button class="big sm" id="impYes">Заменить</button><button class="ghost sm" id="impNo">Отмена</button></span>`;
    document.getElementById('impYes').onclick = () => { S = pendingImport; pendingImport=null; save(); renderStats(); document.getElementById('bkMsg').textContent='Прогресс восстановлен.'; };
    document.getElementById('impNo').onclick = () => { pendingImport=null; msg(''); };
  };
  document.getElementById('imp').onclick = () => document.getElementById('impFile').click();
  document.getElementById('impFile').onchange = e => { const f=e.target.files[0]; if(!f) return; const r=new FileReader(); r.onload=()=>askImport(String(r.result)); r.readAsText(f); };
  document.getElementById('pasteGo').onclick = () => askImport(document.getElementById('pasteBox').value);
  document.getElementById('reset').onclick=()=>{ document.getElementById('resetrow').innerHTML='<button class="big" id="yes" style="background:var(--bad)">Да, удалить всё</button><button class="ghost" id="no">Отмена</button>';
    document.getElementById('yes').onclick=()=>{ S=blank(); save(); renderStats(); }; document.getElementById('no').onclick=renderStats; };
}

""")

# ---------- texts ----------
between("function renderTexts(){", "/* ---------- словарь ---------- */", r"""function renderTexts(){
  const done = TEXTS.filter(t=>S.read[t.id]?.done).length;
  const cont = TEXTS.find(t => t.id===S.lastRead && !S.read[t.id]?.done);
  const card = (tx, extra='') => { const r=S.read[tx.id]; const wc=wordCount(tx);
    return `<button class="tcard${extra?' cont':''}" data-id="${tx.id}"><span class="meta">${extra?`<span class="badge go">${extra}</span>`:''}<span class="g">${esc(tx.genre)}</span><span class="lvl">${tx.level==='B1'?'B1':'A2–B1'}</span><span>${Math.max(1,Math.round(wc/120))} мин</span>${!extra&&r?.done?'<span class="badge done">Прочитано</span>':!extra&&r?'<span class="badge go">Начато</span>':''}</span>
      <span class="t" lang="en">${esc(tx.title_en)}</span><span class="tr2">${esc(tx.title_ru)}</span>${extra?'':`<span class="s">${esc(tx.summary_ru)}</span>`}</button>`; };
  view.innerHTML = `<div class="tlist">
    <div class="hint">Нажми на слово, чтобы увидеть перевод и сохранить его в «Мои слова». Нажми «|» после предложения, чтобы перевести его целиком. Прочитано: ${done} из ${TEXTS.length}.</div>
    ${cont ? card(cont, 'Продолжить') : ''}
    <div class="chips">${chip('lvl','all','Все',textLvl==='all')}${chip('lvl','B1','B1',textLvl==='B1')}${chip('lvl','A2','A2–B1',textLvl==='A2')}</div>
    ${TEXTS.filter(tx=> textLvl==='all' || (textLvl==='B1') === (tx.level==='B1')).map(tx=>card(tx)).join('')}
  </div>`;
  view.querySelectorAll('[data-g=lvl]').forEach(c => c.onclick = () => { textLvl = c.dataset.v; renderTexts(); });
  view.querySelectorAll('.tcard').forEach(c => c.onclick = () => { reading = +c.dataset.id; render(); });
}
const tkey = s => s.toLowerCase().replace(/’/g,"'");
function twHtml(tx,str){ return tokenize(str).map((s,k)=> { if(!(k%2)) return esc(s); const key=tkey(s); return `<span class="tw${tx.vocab[key]?' v':''}${S.mine['u:'+key]?' m':''}">${esc(s)}</span>`; }).join(''); }
function tokenize(s){ return s.split(/([A-Za-z]+(?:['’][A-Za-z]+)*)/); }
function renderReader(){
  const tx = TEXTS.find(t=>t.id===reading); if(!tx){ reading=null; return renderTexts(); }
  const st = S.read[tx.id] ||= {t:Date.now()}; S.lastRead = tx.id; save();
  const words = [...new Set(Object.values(tx.vocab))].map(n=>BYNUM[n]).filter(Boolean);
  view.innerHTML = `<article class="reader" id="art">
    <div class="row" style="flex-wrap:nowrap"><button class="ghost" id="back" style="flex:0 0 auto">← Все тексты</button></div>
    <div class="group"><span class="g" style="font:600 11px var(--f-mono);letter-spacing:.04em;text-transform:uppercase;color:var(--accent)">${esc(tx.genre)} · ${tx.level==='B1'?'B1':'A2–B1'}</span><h1 lang="en">${esc(tx.title_en)}</h1><div class="hint" style="font-size:15px">${esc(tx.title_ru)}</div></div>
    ${tx.paragraphs.map((p,i)=>`<div class="para" data-i="${i}"><p lang="en">${(p.s&&p.s.length ? p.s : [[p.en,p.ru]]).map((s,j)=>`<span class="sent" id="s${i}_${j}">${twHtml(tx,s[0])}</span><button class="sb" data-p="${i}" data-s="${j}" aria-label="Перевод предложения">|</button>`).join(' ')}</p></div>`).join('')}
    <div class="panel" id="endp">
      <div class="row"><button class="big" id="trainTx">Тренировать слова текста</button><button class="ghost" id="doneTx">${st.done?'Прочитано ✓':'Отметить прочитанным'}</button></div>
      <details><summary>Слова из словаря в этом тексте (${words.length})</summary>
      <div class="list">${words.map(w=>`<div class="li"><div class="w"><span class="num">${w.n}</span>${esc(w.en)}<small>${esc(w.ru)}</small></div><div class="n"><span class="pill p-${wstate(w)}">${STATE_LABEL[wstate(w)]}</span></div></div>`).join('')}</div></details>
    </div>
  </article>`;
  const art = document.getElementById('art');
  art.addEventListener('click', e => {
    const tw = e.target.closest('.tw'); if(tw){ e.stopPropagation(); showWord(tx, tw); return; }
    const sb = e.target.closest('.sb'); if(sb){ e.stopPropagation(); showSentence(tx, +sb.dataset.p, +sb.dataset.s, sb); }
  });
  document.getElementById('back').onclick = () => { closeSheet(); reading=null; render(); window.scrollTo(0,0); };
  const markDone = () => { if(st.done) return; st.done = true; st.d = Date.now(); save(); const b=document.getElementById('doneTx'); if(b) b.textContent='Прочитано ✓'; };
  document.getElementById('doneTx').onclick = markDone;
  const twords = words.concat(mineWords().filter(m => S.mine[m.key].tx===tx.id));
  document.getElementById('trainTx').onclick = () => startQuiz(quizFromWords(twords, 30));
  // вернуться туда, где остановился
  if(st.p>0){ const el = art.querySelector(`.para[data-i="${st.p}"]`); if(el) requestAnimationFrame(()=>el.scrollIntoView({block:'start'})); } else window.scrollTo(0,0);
  let tick = 0;
  window.onscroll = () => { const now=Date.now(); if(now-tick<400) return; tick=now;
    const ps = art.querySelectorAll('.para'); let cur = 0;
    for(const p of ps){ if(p.getBoundingClientRect().bottom > 90){ cur = +p.dataset.i; break; } }
    if(cur!==st.p){ st.p = cur; saveLazy(); }
    if(innerHeight + scrollY >= document.documentElement.scrollHeight - 260) markDone();
  };
}
const SAY_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z" fill="currentColor"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>`;
let sheetEl = null, selEl = null;
let selS = [];
function closeSheet(){ if(sheetEl){ sheetEl.remove(); sheetEl=null; } if(selEl){ selEl.classList.remove('sel'); selEl=null; } selS.forEach(x=>x.classList.remove('on')); selS=[]; }
function showSentence(tx, i, j, btn){
  closeSheet();
  const p = tx.paragraphs[i]; const s = (p.s&&p.s.length ? p.s : [[p.en,p.ru]])[j];
  const span = document.getElementById(`s${i}_${j}`); selS = [btn, span].filter(Boolean); selS.forEach(x=>x.classList.add('on'));
  sheetEl = document.createElement('div'); sheetEl.className = 'sheet';
  sheetEl.innerHTML = `<div class="in"><div class="row1"><span class="sen" style="flex:1;min-width:0" lang="en">${esc(s[0])}</span>${TTS?`<button class="say" id="sheetSay" aria-label="Прослушать предложение">${SAY_SVG}</button>`:''}<button class="x" id="sheetX" aria-label="Закрыть">×</button></div>
    <div class="gl">${esc(s[1])}</div></div>`;
  document.body.appendChild(sheetEl);
  document.getElementById('sheetX').onclick = closeSheet;
  const sb = document.getElementById('sheetSay'); if(sb) sb.onclick = () => speak(s[0],'en',true);
}
function sentenceOf(tx, el){
  const sp = el.closest('.sent'); const m = sp && sp.id.match(/^s(\d+)_(\d+)$/); if(!m) return null;
  const p = tx.paragraphs[+m[1]]; return (p.s&&p.s.length ? p.s : [[p.en,p.ru]])[+m[2]];
}
function showWord(tx, el){
  closeSheet();
  const raw = el.textContent, key = tkey(raw);
  const g = tx.gloss[key] || tx.gloss[key.replace(/'s$/,'')] || '';
  const n = tx.vocab[key]; const w = n && BYNUM[n];
  const mkey = 'u:'+key;
  selEl = el; el.classList.add('sel');
  sheetEl = document.createElement('div'); sheetEl.className = 'sheet';
  const actLabel = () => w ? (S.flag[w.key] ? '★ В сложных' : '☆ Отметить сложным') : (S.mine[mkey] ? '✓ В моих словах' : '+ В мои слова');
  sheetEl.innerHTML = `<div class="in"><div class="row1"><span class="wd" lang="en">${esc(raw)}</span>${TTS?`<button class="say" id="sheetSay" aria-label="Произнести">${SAY_SVG}</button>`:''}<button class="x" id="sheetX" aria-label="Закрыть">×</button></div>
    <div class="gl">${esc(g||'нет перевода')}</div>${w?`<div class="dv">Из твоего словаря, №${w.n}: ${esc(w.en)} — ${esc(w.ru)} · ${STATE_LABEL[wstate(w)]}</div>`:''}
    ${w||g?`<div class="acts"><button class="ghost sm" id="sheetAct">${actLabel()}</button></div>`:''}</div>`;
  document.body.appendChild(sheetEl);
  document.getElementById('sheetX').onclick = closeSheet;
  const sb = document.getElementById('sheetSay'); if(sb) sb.onclick = () => speak(raw,'en',true);
  const act = document.getElementById('sheetAct');
  if(act) act.onclick = () => {
    if(w){ if(S.flag[w.key]) delete S.flag[w.key]; else S.flag[w.key]=1; }
    else if(S.mine[mkey]) delete S.mine[mkey];
    else { const s = sentenceOf(tx, el); S.mine[mkey] = {en:key, ru:g, se:s?.[0]||'', sr:s?.[1]||'', f:raw, tx:tx.id, t:Date.now()}; }
    save(); act.textContent = actLabel();
    if(!w) document.querySelectorAll('#art .tw').forEach(x => { if(tkey(x.textContent)===key) x.classList.toggle('m', !!S.mine[mkey]); });
  };
  speak(raw,'en');
}
document.addEventListener('click', e => { if(sheetEl && !sheetEl.contains(e.target) && !e.target.closest('.tw') && !e.target.closest('.sb')) closeSheet(); });

""")
R("let reading = null, textLvl = 'all';", "let reading = null, textLvl = 'all';\nconst STATE_LABEL = {new:'Новое', learning:'Изучаю', learned:'Выучено', hard:'Сложное'};")

# ---------- dictionary ----------
between("/* ---------- словарь ---------- */", "/* ---------- клавиатура ---------- */", r"""/* ---------- словарь ---------- */
let dq = '', dfilt = 'all', dopen = null;
function renderDict(){
  const ws = allWords(), st = new Map(ws.map(w => [w.key, wstate(w)]));
  const c = {new:0,learning:0,learned:0,hard:0}; st.forEach(v => c[v]++);
  const mineN = Object.keys(S.mine).length;
  const F = [['all','Все',ws.length],['new','Новые',c.new],['learning','Изучаю',c.learning],['learned','Выучено',c.learned],['hard','Сложные',c.hard]];
  if(mineN) F.push(['mine','Мои слова',mineN]);
  view.innerHTML = `<div class="panel">
    <input class="inp" id="search" type="search" placeholder="Поиск по-английски, по-русски или по номеру" value="${esc(dq)}" autocomplete="off" style="font-size:16px">
    <div class="chips">${F.map(([v,l,n])=>chip('df',v,`${l} · ${n}`,dfilt===v)).join('')}</div>
    <div id="dtrain"></div>
    <div class="list" id="dlist"></div>
  </div>`;
  view.querySelectorAll('[data-g=df]').forEach(b => b.onclick = () => { dfilt = b.dataset.v; dopen = null; renderDict(); });
  const list = () => { const q = norm(dq);
    return ws.filter(w => (dfilt==='all' || (dfilt==='mine' ? w.mine : st.get(w.key)===dfilt)) && (!q || norm(w.en).includes(q) || norm(w.ru).includes(q) || String(w.n)===q)); };
  const detail = w => { const s = sentOf(w), state = st.get(w.key);
    return `<div class="dd">${s?`<div class="ex" lang="en">${hl(s.en, s.ek)}<small>${esc(s.ru)}</small></div>`:''}
      <div class="acts">${TTS?`<button class="ghost sm" data-act="say">Слушать</button>`:''}${state!=='learned'?`<button class="ghost sm" data-act="know">Знаю</button>`:''}<button class="ghost sm" data-act="flag">${S.flag[w.key]?'★ Убрать из сложных':'☆ Сложное'}</button>${w.mine?`<button class="ghost sm" data-act="del">Удалить</button>`:''}</div></div>`; };
  const fill = () => { const L = list();
    document.getElementById('dtrain').innerHTML = dfilt!=='all' && L.length ? `<button class="big" id="dgo">Тренировать · ${Math.min(30,L.length)} ${plural(Math.min(30,L.length),'слово','слова','слов')}</button>` : '';
    const g = document.getElementById('dgo'); if(g) g.onclick = () => startQuiz(quizFromWords(L, 30));
    document.getElementById('dlist').innerHTML = L.length ? L.map(w => { const s = st.get(w.key);
      return `<div class="li dl" data-k="${esc(w.key)}"><div class="w"><span class="num">${numTag(w)}</span>${esc(w.en)}${w.tr?` <span class="hint">[${esc(w.tr)}]</span>`:''}<small>${esc(w.ru)}</small></div><div class="n"><span class="pill p-${s}">${STATE_LABEL[s]}</span></div></div>${dopen===w.key?detail(w):''}`; }).join('')
      : `<div class="empty">${dfilt==='hard'?'Сложных слов пока нет. Сюда попадают слова с ошибками и те, что ты отметишь сложными.':dfilt==='mine'?'Своих слов пока нет. Добавляй их из текстов: нажми на слово и «+ В мои слова».':'Ничего не найдено.'}</div>`;
  };
  document.getElementById('dlist').onclick = e => {
    const a = e.target.closest('[data-act]');
    if(a){ const w = ws.find(x => x.key===dopen); if(!w) return;
      if(a.dataset.act==='say') speak(w.en,'en',true);
      else if(a.dataset.act==='know'){ markKnown(w); st.set(w.key, wstate(w)); fill(); }
      else if(a.dataset.act==='flag'){ if(S.flag[w.key]) delete S.flag[w.key]; else S.flag[w.key]=1; save(); st.set(w.key, wstate(w)); fill(); }
      else if(a.dataset.act==='del'){ delete S.mine[w.key]; delete S.words[w.key]; delete S.flag[w.key]; save(); dopen=null; renderDict(); }
      return; }
    const row = e.target.closest('.dl'); if(!row) return;
    dopen = dopen===row.dataset.k ? null : row.dataset.k; fill();
  };
  const s = document.getElementById('search');
  s.oninput = () => { dq = s.value; dopen = null; fill(); };
  fill();
}

""")

# old dead code
R("""function options(w,dir){""", """function _unused_options(w,dir){""") if "function options(w,dir){" in t else None
open(p, 'w').write(t)
print('ok')
