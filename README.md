# zptk-site

Сайт ООО «ЗПТК» — статический HTML, публикуется через GitHub Pages.

## Как устроено

Готовые страницы лежат в корне и в `napravleniya/`. Их **не правят руками**: они собираются скриптом из исходников в `_build/`.

| Файл | Что в нём |
|---|---|
| `_build/data.py` | Тексты: позиционирование, 8 направлений, разработки, ориентиры, кейсы, реквизиты |
| `_build/build.py` | Каркас страниц (шапка, подвал, SEO, микроразметка), главная, презентация; настройки `BASE_URL` и `METRIKA_ID` |
| `_build/pages_more.py` | Разделы: направления, разработки, партнёры, проекты, о компании, 404 |
| `_build/legacy/*.html` | Содержимое прежних страниц (услуги/ЕЦУД, проекты, IT-деятельность, контакты, политика) |
| `_build/presentation.py`, `presentation.css`, `pdf.js` | PDF-презентация `zptk-prezentaciya.pdf` из тех же данных |
| `assets/site.css`, `assets/site.js` | Общие стили (токены цветов, вечерняя тема) и скрипты |

## Сборка

```bash
python3 _build/build.py                 # страницы, sitemap.xml, robots.txt, _build/TODO.md
python3 _build/presentation.py && node _build/pdf.js   # PDF (нужен playwright)
python3 _build/build.py                 # ещё раз, чтобы на кнопке был размер нового PDF
```

## Плейсхолдеры

Факты, которых пока нет, отмечены в `data.py` функцией `T("...")`: на сайте они подсвечены жёлтым, в PDF не попадают. Полный список — в `_build/TODO.md`.

## Яндекс.Метрика

Впишите номер счётчика в `METRIKA_ID` в `_build/build.py` и пересоберите. Подключатся счётчик на всех страницах, цели `pdf_download`, `direction_click`, `email_click`, `phone_click`, а в политике конфиденциальности появится абзац о cookie.
