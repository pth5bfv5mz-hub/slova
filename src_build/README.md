# Исходники приложения «Слова»

Всё, из чего собирается `../index.html` (сайт https://pth5bfv5mz-hub.github.io/slova/).
Сам `index.html` и старое приложение в `../old/` отсюда не трогаются, пока не запустить сборку.

## Как пересобрать

Нужен Python 3.

```bash
cd src_build
./build.sh
```

Скрипт:
1. берёт `template.html` (страница с данными словаря и предложений, место для текстов `__TEXTS__`);
2. по очереди применяет правки `patch_audit.py`, `patch_quiz.py`, `patch_restore.py`, `patch_noday.py`, `patch_cons.py`, `patch_b1.py`;
3. `build.py 100` вставляет тексты из `texts/t1..t100.json` и тесты из `texts/quiz/`, получается `slova-test.html`;
4. `make_index.py` вставляет результат в `../index.html` (PWA-заголовок и офлайн-режим сохраняются).

После этого закоммитить `index.html` и отправить в GitHub — сайт обновится через 1–2 минуты.

## Что где лежит

| Файл / папка | Что это |
|---|---|
| `words_table.xlsx` | исходная таблица слов (652 строки) |
| `ex.py`, `words.json`, `words2.json` | разбор таблицы; `words2.json` — 621 слово без повторов |
| `sent0..3.json` | предложение с переводом для каждого слова (режим «Предложения») |
| `texts/tNN.json` | 100 текстов: абзацы, перевод абзацев и предложений (`s`), перевод слов (`gloss`), слова из словаря (`vocab`) |
| `texts/quiz/qNN.json` | тест из 6 вопросов к каждому тексту |
| `texts/assignNN.json` | тема и список слов, по которым писался текст |
| `texts/check*.py` | проверки: перевод у всех слов, предложения, формат тестов |
| `audit_test.js`, `quiz_test.js` | проверки в браузере (Playwright) |

## Как добавить текст

1. Положить `texts/t101.json` и `texts/quiz/q101.json` в том же формате, что и остальные.
2. Проверить: `cd texts && python3 check.py ./t101.json && python3 check2.py ./t101.json && python3 check3.py quiz/q101.json` (для `check.py` нужен `assign101.json`).
3. В `build.sh` поменять `build.py 100` на `build.py 101` и запустить сборку.
