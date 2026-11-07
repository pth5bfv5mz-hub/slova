import sys
p=sys.argv[1]; t=open(p).read()
i=t.index('  view.innerHTML = `<div class="panel">\n    <div class="lbl">Сегодня</div>')
j=t.index('  ${hardN||mineN', i)
t=t[:i]+'  view.innerHTML = `'+t[j:]
a="nb.textContent = n; nb.hidden = !n || !!Q;"; assert t.count(a)==1; t=t.replace(a,"nb.hidden = true;")
open(p,'w').write(t); print('ok')
