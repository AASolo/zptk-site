# Разделы сайта: направления, разработки, партнёры, проекты, о компании.
from data import ORG, BLOCKS, DIRECTIONS, PRODUCTS, PARTNER_GROUPS, CASES, T


def build(b):
    E, ARR, icon, flow, chips, add, layout = b.E, b.ARR, b.icon, b.flow, b.chips, b.add, b.layout
    page_hero, crumbs_ld, cta, status = b.page_hero, b.crumbs_ld, b.cta_presentation, b.status
    BASE = b.BASE_URL

    # ------------------------------------------------ Направления: хаб
    groups = []
    for blk in BLOCKS:
        dirs = [d for d in DIRECTIONS if d["block"] == blk["key"]]
        cards = "".join(f'''<a class="card reveal" href="napravleniya/{d["slug"]}.html">{icon(d["icon"])}
<span class="card__tag">{DIRECTIONS.index(d) + 1:02d}</span><h3 class="h3">{d["title"]}</h3><p>{d["short"]}</p>
<span class="card__more">Подробнее {ARR}</span></a>''' for d in dirs)
        groups.append(f'''<div class="stack" id="{blk["key"]}"><div class="sec-head"><div><span class="eyebrow">Блок {blk["n"]}</span>
<h2 class="h2" style="font-size:clamp(26px,3vw,38px)">{blk["title"]}</h2><p class="lead">{blk["text"]}</p></div></div>
<div class="grid">{cards}</div></div>''')
    anchors = "".join(f'<a href="#{blk["key"]}">{blk["title"]}</a>' for blk in BLOCKS)
    body = page_hero([("index.html", "Главная"), (None, "Направления")], "12 направлений · 4 блока",
                     "Направления ЗПТК",
                     "Связь, логистика, энергетика, собственное ПО, ИИ-агенты, сервис и EPCM. Каждое направление — отдельная команда и законченный цикл работ.",
                     f'<div class="anchor-nav">{anchors}</div>')
    body += f'<section class="sec"><div class="wrap stack-lg">{"".join(groups)}</div></section>' + cta()
    ld = [crumbs_ld([("index.html", "Главная"), ("napravleniya.html", "Направления")]),
          {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "name": d["title"], "url": BASE + f'napravleniya/{d["slug"]}.html'}
              for i, d in enumerate(DIRECTIONS)]}]
    add("napravleniya.html", layout("napravleniya.html", "Направления ЗПТК: связь, логистика, энергетика, ИИ, EPCM",
                                    "12 направлений ЗПТК в 4 блоках: инфраструктура связи, логистические центры, АИИС КУЭ, РЗА, ЦОД, собственное ПО, ИИ-агенты, сервис, энергосервис, EPCM.",
                                    body, ld))

    # ------------------------------------------------ 12 подстраниц
    for i, d in enumerate(DIRECTIONS):
        blk = b.BLOCK_BY_KEY[d["block"]]
        path = f'napravleniya/{d["slug"]}.html'
        slogan = d["slogan"] + ("" if not d.get("slogan_draft") else "")
        slogan_html = f'<p class="slogan" style="color:#fff;max-width:900px">{E(slogan)}</p>'
        if d.get("slogan_draft"):
            slogan_html = f'<p class="slogan" style="color:#fff;max-width:900px">{T(E(slogan))}</p>'
        hero = page_hero([("../index.html", "Главная"), ("../napravleniya.html", "Направления"), (None, d["title"])],
                         f'Направление {i + 1:02d} · {blk["title"]}', d["h1"], "",
                         slogan_html + f'<div class="actions">{b.pdf_button("../")}</div>')
        pains = "".join(f"<li>{p}</li>" for p in d["pains"])
        tech = "".join(f'<div class="card"><h3 class="h3" style="font-size:20px">{t}</h3><p>{x}</p></div>' for t, x in d["tech"])
        result = "".join(f"<li>{r}</li>" for r in d["result"])
        partners_html = ""
        if d["partners"] or d.get("benchmarks"):
            rows = []
            if d["partners"]:
                rows.append(f'<div class="stack" style="gap:12px"><span class="muted mono" style="font-size:13px">ТЕХНОЛОГИИ И ПАРТНЁРЫ</span>{chips(d["partners"])}</div>')
            if d.get("benchmarks"):
                rows.append(f'<div class="stack" style="gap:12px"><span class="muted mono" style="font-size:13px">ОРИЕНТИРЫ</span>{chips(d["benchmarks"])}</div>')
            partners_html = f'''<section class="sec sec--tight"><div class="wrap stack">
<span class="eyebrow">Ориентиры и партнёры</span><h2 class="h2" style="font-size:clamp(26px,3vw,38px)">С кем и на чём работаем</h2>
{"".join(rows)}<a class="link-arr" href="../partnery.html">Все технологии и партнёры {ARR}</a></div></section>'''
        proof = (f'<div class="panel panel--accent"><span class="eyebrow">Из практики</span><p style="margin-top:8px">{d["proof"]}</p>'
                 f'<a class="link-arr" style="margin-top:12px" href="../proekty.html">Все проекты {ARR}</a></div>') if d.get("proof") else ""
        more = f'<a class="btn btn--ghost" href="../{d["more"][0]}">{d["more"][1]} {ARR}</a>' if d.get("more") else ""
        prev_d, next_d = DIRECTIONS[i - 1], DIRECTIONS[(i + 1) % len(DIRECTIONS)]
        body = hero + f'''
<section class="sec"><div class="wrap split">
<div class="stack"><span class="eyebrow">Проблема клиента</span><h2 class="h2" style="font-size:clamp(26px,3vw,38px)">Что мешает заказчику</h2>
<p class="lead">{d["problem"]}</p></div>
<div class="panel"><ul class="checks">{pains}</ul></div>
</div></section>

<section class="sec sec--alt"><div class="wrap stack-lg">
<div class="sec-head"><div><span class="eyebrow">Технологии</span><h2 class="h2" style="font-size:clamp(26px,3vw,38px)">Из чего складывается решение</h2></div></div>
<div class="grid">{tech}</div></div></section>

<section class="sec sec--dark">{b.dark_bg()}<div class="wrap stack-lg" style="position:relative">
<div class="sec-head"><div><span class="eyebrow">Схема</span><h2 class="h2" style="font-size:clamp(26px,3vw,38px)">Сигнал → решение → действие</h2></div></div>
{flow(d["flow"], label="Схема решения: " + d["title"])}</div></section>
{partners_html}
<section class="sec{" sec--alt" if partners_html else ""}"><div class="wrap split">
<div class="stack"><span class="eyebrow">Результат для заказчика</span><h2 class="h2" style="font-size:clamp(26px,3vw,38px)">Что получает заказчик</h2>
<ul class="checks" style="margin-top:8px">{result}</ul>{f'<div class="actions" style="margin-top:12px">{more}</div>' if more else ""}</div>
<div class="stack">{proof}</div>
</div></section>

<section class="sec sec--tight"><div class="wrap"><nav class="pager" aria-label="Другие направления">
<a href="{prev_d["slug"]}.html"><span>← Предыдущее направление</span>{prev_d["title"]}</a>
<a href="{next_d["slug"]}.html"><span>Следующее направление →</span>{next_d["title"]}</a></nav></div></section>
''' + cta("../")
        ld = [crumbs_ld([("index.html", "Главная"), ("napravleniya.html", "Направления"), (path, d["title"])]),
              {"@context": "https://schema.org", "@type": "Service", "name": d["title"], "serviceType": d["title"],
               "description": d["description"], "url": BASE + path, "areaServed": "RU",
               "provider": {"@id": BASE + "#org"}}]
        add(path, layout(path, f'{d["h1"]} — ЗПТК', d["description"], body, ld))

    # ------------------------------------------------ Собственные разработки
    blocks = []
    for p in PRODUCTS:
        pts = "".join(f"<li>{x}</li>" for x in p["points"])
        links = "".join(f'<a class="btn btn--ghost" href="{h}">{t} {ARR}</a>' for h, t in p["links"])
        blocks.append(f'''<article class="stack-lg" id="{p["id"]}" style="scroll-margin-top:100px;padding:56px 0;border-top:1px solid var(--line)">
<div class="split"><div class="stack">{status(p["status"])}<h2 class="h2" style="font-size:clamp(28px,3.2vw,42px)">{p["title"]}</h2>
<p class="lead">{p["lead"]}</p><div class="actions">{links}</div></div>
<div class="panel"><ul class="checks">{pts}</ul></div></div>
{flow(p["flow"], light=True, label="Схема: " + p["title"])}</article>''')
    anchors = "".join(f'<a href="#{p["id"]}">{p["title"].split(" «")[0] if p["id"] == "ii-agenty" else p["title"]}</a>' for p in PRODUCTS)
    body = page_hero([("index.html", "Главная"), (None, "Собственные разработки")], "Наше конкурентное преимущество",
                     "Собственные разработки",
                     f'ПО в реестре российского ПО, ИИ-агенты и аналитика, которые мы создаём сами и внедряем в проектах. Статусы: <span class="status status--reg" style="vertical-align:middle">в реестре</span> <span class="status status--pilot" style="vertical-align:middle">пилот</span> <span class="status status--rnd" style="vertical-align:middle">R&amp;D</span>',
                     f'<div class="anchor-nav">{anchors}</div>')
    body += f'<section class="sec" style="padding-top:24px"><div class="wrap">{"".join(blocks)}</div></section>' + cta()
    ld = [crumbs_ld([("index.html", "Главная"), ("razrabotki.html", "Собственные разработки")]),
          {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "ПТК ЕЦУД",
           "applicationCategory": "BusinessApplication", "operatingSystem": "Linux, Windows",
           "description": PRODUCTS[0]["lead"], "url": BASE + "razrabotki.html#ecud",
           "publisher": {"@id": BASE + "#org"},
           "offers": {"@type": "Offer", "availability": "https://schema.org/InStock", "priceCurrency": "RUB",
                      "seller": {"@id": BASE + "#org"}}}]
    for p in PRODUCTS[1:]:
        ld.append({"@context": "https://schema.org", "@type": "Product", "name": p["title"].replace("ИИ-агенты ", ""),
                   "description": b.re.sub("<[^>]+>", "", p["lead"]), "url": BASE + f'razrabotki.html#{p["id"]}',
                   "brand": {"@type": "Brand", "name": "ЗПТК"}, "manufacturer": {"@id": BASE + "#org"}})
    add("razrabotki.html", layout("razrabotki.html", "Собственные разработки ЗПТК: ПТК ЕЦУД, ИИ-агенты, анализ потерь",
                                  "ПТК ЕЦУД в реестре российского ПО (№ 29851), ИИ-агенты «Цифровой инженер» и «Страх качества», ИИ-анализ потерь и «Финансовый радар».",
                                  body, ld))

    # ------------------------------------------------ Технологии и партнёры
    rows = []
    for name, slug, items in PARTNER_GROUPS:
        lis = "".join(f'<li><b>{n}</b><span>{s or "&nbsp;"}</span></li>' for n, s in items)
        d = b.DIR_BY_SLUG[slug]
        rows.append(f'''<div class="partner-group reveal"><div class="stack" style="gap:10px"><h2 class="h3">{name}</h2>
<a class="link-arr" style="font-size:15px" href="napravleniya/{slug}.html">{d["title"]} {ARR}</a></div>
<ul class="wordmarks">{lis}</ul></div>''')
    body = page_hero([("index.html", "Главная"), (None, "Технологии и партнёры")], "Технологии и партнёры",
                     "Технологии и партнёры",
                     "Производители, платформы и компании-ориентиры, с которыми мы строим решения. " + T("Статусы партнёрства (сертифицированный партнёр, дистрибьютор, интегратор) и логотипы — уточнить."))
    body += f'''<section class="sec"><div class="wrap">{"".join(rows)}
<p class="muted" style="margin-top:24px;font-size:15px">Пометка «ориентир» означает компанию, на практики которой мы равняемся. Товарные знаки принадлежат их правообладателям.</p></div></section>''' + cta()
    add("partnery.html", layout("partnery.html", "Технологии и партнёры ЗПТК: Motorola, Cisco, KNPP, SSI Schäfer, ГОСАН",
                                "Партнёры и технологии ЗПТК: связь (Motorola Solutions, Cisco), логистика (KNPP, SSI Schäfer, FIRST, Axelot), сервис, проектный контроль, EPCM.",
                                body, [crumbs_ld([("index.html", "Главная"), ("partnery.html", "Технологии и партнёры")])]))

    # ------------------------------------------------ Проекты: кейсы + прежний список
    case_html = []
    for i, c in enumerate(CASES):
        d = b.DIR_BY_SLUG[c["dir"]]
        case_html.append(f'''<article class="stack reveal" id="case-{i + 1}" style="scroll-margin-top:100px">
<span class="card__tag">Кейс {i + 1:02d} · <a href="napravleniya/{d["slug"]}.html">{d["title"]}</a> · заказчик под NDA</span>
<h3 class="h3">{c["title"]}</h3>
<div class="case"><div><h4>Задача</h4><p>{c["task"]}</p></div><div><h4>Решение</h4><p>{c["solution"]}</p></div>
<div><h4>Технологии</h4><p>{c["tech"]}</p></div><div><h4>Результат</h4><p>{c["result"]}</p></div></div></article>''')
    before = f'''<section class="sec" style="padding-bottom:56px"><div class="wrap stack-lg">
<div class="sec-head"><div><span class="eyebrow">Кейсы</span><h2 class="h2">Задача → решение → технологии → результат</h2>
<p class="lead">Названия заказчиков скрыты по NDA. Ниже — реализованные проекты для крупнейших энергетических и телеком-компаний.</p></div></div>
{"".join(case_html)}</div></section>'''
    # кейсы вставляем после первого экрана прежней страницы
    b.legacy_page("proekty.html")
    page = b.PAGES["proekty.html"]
    marker = "</section>"
    idx = page.index('<main id="main">')
    cut = page.index(marker, idx) + len(marker)
    page = page[:cut] + before + page[cut:]
    page = page.replace("<title>Наши проекты — ЗПТК</title>", "<title>Проекты и кейсы ЗПТК: АИИС КУЭ, связь, логистика, РЗА</title>")
    b.PAGES["proekty.html"] = page

    # ------------------------------------------------ О компании
    history = [("2005", "Старт", "Выходим на рынок инжиниринга в энергетике. Новосибирск."),
               ("70+", "Крупные проекты", "Россети, ФСК ЕЭС, Мосэнерго, Ростелеком, Газпром энергохолдинг."),
               ("2025", "ЕЦУД в реестре", "Наше ПО в реестре российского ПО, запись № 29851."),
               ("2026", "Инжиниринговая группа", "12 направлений, ИИ-агенты и EPCM-контракты.")]
    hist = "".join(f'<div class="card"><span class="mono" style="font-size:34px;font-weight:600;color:var(--accent)">{y}</span><h3 class="h3" style="font-size:20px">{t}</h3><p>{x}</p></div>' for y, t, x in history)
    team = [("Богданов Антон Владимирович", "Генеральный директор"),
            ("Сергеев Илья", "Заместитель генерального директора — директор по развитию"),
            ("Котляревский Антон", "Коммерческий директор")]
    team_html = "".join(f'<div class="card">{icon("users", 32)}<h3 class="h3" style="font-size:20px">{n}</h3><p>{r}</p></div>' for n, r in team)
    team_html += f'<div class="card">{icon("users", 32)}<h3 class="h3" style="font-size:20px">{T("Ключевые эксперты")}</h3><p>{T("главный инженер, руководители направлений, архитектор ЕЦУД — ФИО, роль, опыт")}</p></div>'
    geo = ["Новосибирск — головной офис", "Москва — филиал", "Красноярский край", "Алтайский край", "Республика Дагестан",
           "Краснодарский край", "Саратовская, Владимирская, Орловская области", "Республика Хакасия"]
    body = page_hero([("index.html", "Главная"), (None, "О компании")], f"С {ORG['founded']} года",
                     "О компании",
                     "ЗПТК — инжиниринговая группа полного цикла. Проектируем, строим и обслуживаем инфраструктуру повышенной отказоустойчивости: связь, логистика, энергетика. Собственные разработки на базе ИИ. EPCM-контракты.",
                     '<div class="anchor-nav"><a href="#history">История и миссия</a><a href="#team">Команда</a><a href="#licenses">Лицензии и сертификаты</a><a href="#reestr">Реестр ПО</a><a href="#geo">География</a><a href="#rekvizity">Реквизиты</a></div>')
    body += f'''
<section class="sec" id="history"><div class="wrap stack-lg">
<div class="split"><div class="stack"><span class="eyebrow">История и миссия</span><h2 class="h2">От точного учёта — к умной энергетике</h2></div>
<div class="stack"><p class="lead">Мы начинали с инжиниринга в энергетике: системы учёта, телемеханика, релейная защита. Сегодня ЗПТК — группа, которая отвечает за весь жизненный цикл критической инфраструктуры: от проекта и стройки до собственного ПО, ИИ-агентов и сервиса.</p>
<p><b>Миссия:</b> {T("сформулировать миссию компании")}</p></div></div>
<div class="grid-4">{hist}</div></div></section>

<section class="sec sec--alt" id="team"><div class="wrap stack-lg">
<div class="sec-head"><div><span class="eyebrow">Команда</span><h2 class="h2">Руководство и ключевые эксперты</h2>
<p class="lead">ПИР, поставка, СМР, ПНР и сервис выполняем штатным персоналом, без генподрядчика между нами и заказчиком. Численность: {T("сколько сотрудников и инженеров")}.</p></div></div>
<div class="grid">{team_html}</div></div></section>

<section class="sec" id="licenses"><div class="wrap split">
<div class="stack"><span class="eyebrow">Лицензии и сертификаты</span><h2 class="h2">Допуски и членство в СРО</h2>
<p class="lead">Документы, которые подтверждают право выполнять проектные, строительно-монтажные и пусконаладочные работы.</p></div>
<div class="panel"><ul class="checks">
<li>Членство в СРО (проектирование): {T("номер и название СРО")}</li>
<li>Членство в СРО (строительство): {T("номер и название СРО")}</li>
<li>Лицензии: {T("ФСТЭК, ФСБ, МЧС — если есть")}</li>
<li>Сертификаты менеджмента: {T("ISO 9001 и другие — если есть")}</li>
<li>Аккредитация IT-компании: <a href="it.html">сведения об IT-деятельности</a></li>
</ul></div></div></section>

<section class="sec sec--dark" id="reestr">{b.dark_bg()}<div class="wrap split" style="position:relative">
<div class="stack"><span class="eyebrow">Реестр российского ПО</span><h2 class="h2">ПТК ЕЦУД — запись № {ORG["registry_no"]}</h2>
<p class="lead">Запись от {ORG["registry_date"]}, класс 12.06, правообладатель ООО «ЗПТК».</p>
<div class="actions"><a class="btn btn--primary" href="{ORG["registry_url"]}" target="_blank" rel="noopener">Открыть реестр Минцифры {ARR}</a><a class="btn btn--ghost" href="razrabotki.html#ecud">О ПТК ЕЦУД</a></div></div>
<div class="stack" style="justify-content:center">{b.stats([(None, "№ " + ORG["registry_no"], "", "запись в реестре российского ПО"), (None, ORG["registry_date"], "", "дата включения")])}</div>
</div></section>

<section class="sec" id="geo"><div class="wrap split">
<div class="stack"><span class="eyebrow">География</span><h2 class="h2">Работаем по всей России</h2>
<p class="lead">Головной офис в Новосибирске, филиал в Москве. Объекты — от Северного Кавказа до Сибири.</p></div>
<div class="panel">{chips(geo)}</div></div></section>

<section class="sec sec--alt" id="rekvizity"><div class="wrap split">
<div class="stack"><span class="eyebrow">Реквизиты</span><h2 class="h2">{ORG["short"]}</h2>
<p class="lead">{ORG["name"]}</p><p><a class="link-arr" href="kontakty.html">Контакты и банковские реквизиты {ARR}</a></p></div>
<dl class="kv"><dt>ИНН / КПП</dt><dd>{ORG["inn"]} / {ORG["kpp"]}</dd><dt>ОГРН</dt><dd>{ORG["ogrn"]}</dd>
<dt>ОКПО</dt><dd>{ORG["okpo"]}</dd><dt>ОКВЭД</dt><dd>62.01 — разработка ПО</dd>
<dt>Юридический адрес</dt><dd>{ORG["addr"]}</dd><dt>Филиал</dt><dd>{ORG["addr_branch"]}</dd>
<dt>E-mail</dt><dd><a href="mailto:{ORG["email"]}">{ORG["email"]}</a></dd><dt>Телефон</dt><dd>{ORG["phone"]}</dd></dl>
</div></section>
''' + cta()
    add("o-kompanii.html", layout("o-kompanii.html", "О компании ЗПТК: история, команда, реестр ПО, реквизиты",
                                  "ООО «ЗПТК» — инжиниринговая группа полного цикла с 2005 года. История, команда, лицензии и СРО, реестр российского ПО, география работ, реквизиты.",
                                  body, [crumbs_ld([("index.html", "Главная"), ("o-kompanii.html", "О компании")])]))

    # ------------------------------------------------ 404
    body = page_hero([("index.html", "Главная"), (None, "Страница не найдена")], "Ошибка 404", "Такой страницы нет",
                     "Возможно, она переехала после обновления сайта.",
                     f'<div class="actions"><a class="btn btn--primary" href="index.html">На главную</a><a class="btn btn--ghost" href="napravleniya.html">Направления {ARR}</a></div>')
    add("404.html", layout("404.html", "Страница не найдена — ЗПТК", "Страница не найдена.", body))
