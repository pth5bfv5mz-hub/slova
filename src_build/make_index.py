# Вставляет собранную страницу slova-test.html в ../index.html (сохраняя PWA-заголовок и service worker).
import os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'slova-test.html'), encoding='utf-8').read()
idx = os.path.join(here, '..', 'index.html')
t = open(idx, encoding='utf-8').read()
i = t.index('<title>'); j = t.rindex('<script>if("serviceWorker"')
open(idx, 'w', encoding='utf-8').write(t[:i] + src + '\n' + t[j:])
print('index.html обновлён')
