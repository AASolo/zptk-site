#!/usr/bin/env python3
"""Сборка статического сайта ЗПТК.

Запуск из корня репозитория:  python3 _build/build.py
Скрипт перезаписывает HTML-страницы в корне и в napravleniya/, sitemap.xml,
robots.txt и _build/TODO.md. Править нужно файлы в _build/, а не готовый HTML.
"""
import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from data import (HIDE_TODO, ORG, POSITIONING, BLOCKS, DIRECTIONS, PRODUCTS, PARTNER_GROUPS,  # noqa: E402
                  CASES, STATS_MAIN, T)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD = os.path.dirname(os.path.abspath(__file__))

# Адрес, по которому сайт опубликован. Используется в canonical, og:url и sitemap.
BASE_URL = "https://aasolo.github.io/zptk-site/"
# Номер счётчика Яндекс.Метрики. Пока пусто — счётчик не подключается.
METRIKA_ID = ""
PDF_FILE = "zptk-prezentaciya.pdf"

E = html.escape
TODAY = date.today().isoformat()
BLOCK_BY_KEY = {b["key"]: b for b in BLOCKS}
DIR_BY_SLUG = {d["slug"]: d for d in DIRECTIONS}

# ---------------------------------------------------------------- иконки
# Единый стиль: контур 2px, скруглённые концы, поле 40×40.
_IC = {
    "grid": '<rect x="6" y="6" width="11" height="11" rx="2"/><rect x="23" y="6" width="11" height="11" rx="2"/><rect x="6" y="23" width="11" height="11" rx="2"/><rect x="23" y="23" width="11" height="11" rx="2"/>',
    "code": '<path d="M14 12 L6 20 L14 28 M26 12 L34 20 L26 28 M23 8 L17 32"/>',
    "pulse": '<path d="M4 22 H11 L15 10 L21 32 L25 18 L28 22 H36"/>',
    "layers": '<path d="M20 5 L36 13 L20 21 L4 13 Z M4 20 L20 28 L36 20 M4 27 L20 35 L36 27"/>',
    "signal": '<circle cx="20" cy="28" r="3"/><path d="M13 21 A10 10 0 0 1 27 21 M8 16 A17 17 0 0 1 32 16 M20 31 V36"/>',
    "box": '<path d="M20 4 L35 12 V28 L20 36 L5 28 V12 Z M5 12 L20 20 L35 12 M20 20 V36"/>',
    "meter": '<rect x="6" y="5" width="28" height="30" rx="3"/><path d="M12 22 A8 8 0 0 1 28 22 M20 22 L25 16 M12 29 H28"/>',
    "shield": '<path d="M20 4 L33 9 V19 C33 27 27 33 20 36 C13 33 7 27 7 19 V9 Z"/><path d="M21 12 L16 21 H22 L19 28"/>',
    "server": '<rect x="7" y="5" width="26" height="9" rx="2"/><rect x="7" y="16" width="26" height="9" rx="2"/><rect x="7" y="27" width="26" height="9" rx="2"/><path d="M12 9.5 H13 M12 20.5 H13 M12 31.5 H13"/>',
    "spark": '<path d="M20 4 L23 16 L35 20 L23 24 L20 36 L17 24 L5 20 L17 16 Z"/><path d="M32 5 V11 M29 8 H35"/>',
    "coins": '<ellipse cx="16" cy="12" rx="10" ry="4"/><path d="M6 12 V20 C6 22 10 24 16 24 M26 12 V16"/><ellipse cx="25" cy="23" rx="10" ry="4"/><path d="M15 23 V30 C15 32 19 34 25 34 C31 34 35 32 35 30 V23"/>',
    "doc": '<path d="M9 4 H24 L31 11 V36 H9 Z M24 4 V11 H31 M14 19 H26 M14 25 H26 M14 31 H21"/>',
    "chart": '<path d="M5 35 H35 M9 30 V20 M17 30 V12 M25 30 V17 M33 30 V7"/>',
    "download": '<path d="M20 5 V26 M11 17 L20 26 L29 17 M6 34 H34"/>',
    "check": '<path d="M8 21 L16 29 L32 11"/>',
    "users": '<circle cx="14" cy="13" r="5"/><path d="M4 33 C4 26 8 22 14 22 C20 22 24 26 24 33"/><circle cx="28" cy="15" r="4"/><path d="M26 22 C32 22 36 26 36 32"/>',
    "map": '<path d="M20 36 C20 36 8 24 8 15 A12 12 0 0 1 32 15 C32 24 20 36 20 36 Z"/><circle cx="20" cy="15" r="4"/>',
    "award": '<circle cx="20" cy="15" r="9"/><path d="M14 22 L11 36 L20 31 L29 36 L26 22"/>',
}


def icon(name, size=40, cls="ico"):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 40 40" aria-hidden="true" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{_IC[name]}</svg>')


ARR = '<span class="arr" aria-hidden="true">→</span>'

# ---------------------------------------------------------------- компоненты


def flow(steps, light=False, label="Схема"):
    arrow = ('<div class="flow__arr" aria-hidden="true"><svg viewBox="0 0 56 20"><path d="M2 10 H46"/>'
             '<path class="head" d="M42 4 L50 10 L42 16"/></svg></div>')
    parts = []
    for i, (k, t, p) in enumerate(steps):
        core = " flow__step--core" if i == 1 else ""
        parts.append(f'<div class="flow__step{core}"><span class="flow__k">{E(k)}</span>'
                     f'<span class="flow__t">{E(t)}</span><p>{p}</p></div>')
    return (f'<div class="flow{" flow--light" if light else ""}" role="group" aria-label="{E(label)}">'
            + arrow.join(parts) + '</div>')


def stats(items, light=False):
    out = []
    for count, shown, suffix, label in items:
        if count:
            dd = f'<span data-count="{count}">{shown}</span>{suffix}'
            cls = ""
        else:
            dd, cls = shown, ' class="sm"'
        out.append(f'<div><dt>{label}</dt><dd{cls}>{dd}</dd></div>')
    return f'<dl class="stats{" stats--light" if light else ""}">' + "".join(out) + '</dl>'


def emblem():
    """Анимированная эмблема ЗПТК с прежней главной страницы."""
    chips = [("Связь", "left:2%;top:14%", "0s"), ("Энергетика", "right:0;top:26%", "-1.5s"),
             ("Логистика", "left:6%;bottom:18%", "-3s"), ("ИИ-агенты", "right:6%;bottom:8%", "-4s")]
    chip_html = "".join(
        f'<span class="z-chip" style="animation-delay:{d};position:absolute;{pos};font-family:var(--mono);font-size:13px;'
        f'background:rgba(10,42,66,.85);border:1px solid #2D6087;color:#E3EEF6;padding:8px 12px;border-radius:40px">{t}</span>'
        for t, pos, d in chips)
    return f'''<div class="z-rise" style="animation-delay:.2s;position:relative;width:100%;max-width:500px;aspect-ratio:1/1">
<svg viewBox="0 0 520 520" width="100%" height="100%" role="img" aria-label="Эмблема ЗПТК: ядро с молнией и три орбиты" style="display:block;overflow:visible">
<circle cx="260" cy="260" r="200" fill="#0F3654" opacity="0.55"/>
<circle class="z-rip" cx="260" cy="260" r="52" fill="none" stroke="#3DB4F0" stroke-width="1.5"/>
<circle class="z-rip z-rip2" cx="260" cy="260" r="52" fill="none" stroke="#3DB4F0" stroke-width="1.5"/>
<circle class="z-rip z-rip3" cx="260" cy="260" r="52" fill="none" stroke="#3DB4F0" stroke-width="1.5"/>
<g class="z-orbits">
<ellipse cx="260" cy="260" rx="230" ry="88" fill="none" stroke="#3DB4F0" stroke-width="2.5" opacity="0.75"/>
<ellipse cx="260" cy="260" rx="230" ry="88" fill="none" stroke="#3DB4F0" stroke-width="2.5" opacity="0.75" transform="rotate(60 260 260)"/>
<ellipse cx="260" cy="260" rx="230" ry="88" fill="none" stroke="#3DB4F0" stroke-width="2.5" opacity="0.75" transform="rotate(120 260 260)"/>
<circle class="z-e z-e1" r="8" fill="#FFFFFF"/><circle class="z-e z-e2" r="8" fill="#FFFFFF"/><circle class="z-e z-e3" r="8" fill="#FFFFFF"/>
</g>
<g class="z-core"><circle cx="260" cy="260" r="56" fill="#008DD2"/><circle cx="260" cy="260" r="56" fill="none" stroke="#FFFFFF" stroke-width="3"/>
<path d="M270 220 L242 266 H262 L250 302 L282 250 H262 Z" fill="#FFFFFF"/></g>
</svg>{chip_html}</div>'''


def ai_net():
    """Фоновый узор «нейросеть» для тёмных блоков."""
    pts = [(80, 60), (220, 30), (360, 90), (520, 40), (640, 130), (140, 190), (300, 220), (460, 200),
           (600, 260), (60, 320), (220, 360), (400, 330), (560, 380), (680, 350)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (1, 6), (2, 6), (2, 7), (3, 7), (4, 8), (5, 6), (6, 7),
             (7, 8), (5, 9), (6, 10), (6, 11), (7, 11), (8, 12), (9, 10), (10, 11), (11, 12), (12, 13), (8, 13)]
    lines = "".join(f'<line class="l" x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}"/>' for a, b in edges)
    nodes = "".join(f'<circle class="n{" p" if i % 3 == 0 else ""}" cx="{x}" cy="{y}" r="{4 if i % 4 else 6}" '
                    f'style="animation-delay:{-i * 0.4:.1f}s"/>' for i, (x, y) in enumerate(pts))
    return f'<svg class="ai-net" viewBox="0 0 720 420" aria-hidden="true">{lines}{nodes}</svg>'


def dark_bg():
    return '<div class="ai-bg" aria-hidden="true"></div>' + ai_net()


def chips(names, mono=False):
    cls = "chip chip--mono" if mono else "chip"
    return '<ul class="chips">' + "".join(f'<li class="{cls}">{n}</li>' for n in names) + '</ul>'


def page_hero(crumbs, eyebrow, h1, lead="", extra=""):
    cr = []
    for href, title in crumbs:
        cr.append(f'<a href="{href}">{E(title)}</a>' if href else f'<span aria-current="page">{E(title)}</span>')
    nav = '<nav class="crumbs" aria-label="Хлебные крошки">' + '<span aria-hidden="true">/</span>'.join(cr) + '</nav>'
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'''<section class="hero page-hero">{dark_bg()}
<div class="wrap hero__in">{nav}
<span class="eyebrow">{eyebrow}</span>
<h1 class="h1" style="max-width:1000px">{h1}</h1>{lead_html}{extra}</div></section>'''


def pdf_size():
    p = os.path.join(ROOT, PDF_FILE)
    if os.path.exists(p):
        return f"PDF, {os.path.getsize(p) / 1024 / 1024:.1f} МБ".replace(".", ",")
    return "PDF"


def pdf_button(prefix="", cls="btn btn--primary btn--lg", text="Скачать презентацию"):
    return (f'<a class="{cls}" href="{prefix}{PDF_FILE}" download>{icon("download", 20, "")}{text} '
            f'<small>{pdf_size()}</small></a>')


def cta_presentation(prefix=""):
    return f'''<section class="sec sec--tight"><div class="wrap"><div class="cta reveal">{dark_bg()}
<div class="stack" style="max-width:640px"><span class="eyebrow">Презентация</span>
<h2 class="h2">Вся группа ЗПТК в одном файле</h2>
<p>Направления, собственные разработки, ориентиры и схемы решений. Удобно переслать коллегам и приложить к запросу.</p></div>
<div class="actions">{pdf_button(prefix)}<a class="btn btn--ghost btn--lg" href="mailto:{ORG["email"]}">{ORG["email"]}</a></div>
</div></div></section>'''


# ---------------------------------------------------------------- разметка Schema.org


def org_ld():
    return {
        "@context": "https://schema.org", "@type": "Organization", "@id": BASE_URL + "#org",
        "name": ORG["name"], "alternateName": ["ЗПТК", ORG["short"]], "url": BASE_URL,
        "logo": BASE_URL + "logo.png", "email": ORG["email"], "telephone": ORG["phone"],
        "foundingDate": ORG["founded"], "taxID": ORG["inn"],
        "description": POSITIONING,
        "address": [
            {"@type": "PostalAddress", "streetAddress": "Красный проспект, д. 200, оф. 914", "addressLocality": "Новосибирск",
             "postalCode": "630049", "addressCountry": "RU"},
            {"@type": "PostalAddress", "streetAddress": "ул. Вавилова, д. 69/75, оф. 719", "addressLocality": "Москва",
             "postalCode": "117335", "addressCountry": "RU"}],
        "areaServed": "RU",
        "knowsAbout": [d["title"] for d in DIRECTIONS],
    }


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": BASE_URL + url}
        for i, (url, name) in enumerate(items)]}


# ---------------------------------------------------------------- каркас страницы

NAV = [
    ("o-kompanii.html", "О компании"),
    ("napravleniya.html", "Направления"),
    ("razrabotki.html", "Разработки"),
    ("partnery.html", "Ориентиры"),
    ("proekty.html", "Проекты"),
    ("kontakty.html", "Контакты"),
]
NAV_ACTIVE = {  # какие страницы подсвечивают пункт меню
    "napravleniya.html": "napravleniya.html", "uslugi.html": "razrabotki.html",
    "it.html": "o-kompanii.html",
}


def metrika():
    if not METRIKA_ID:
        return "<!-- Яндекс.Метрика: укажите METRIKA_ID в _build/build.py, и счётчик подключится на всех страницах -->"
    return f'''<script>window.ZPTK_YM={METRIKA_ID};(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})
(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
ym({METRIKA_ID},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{METRIKA_ID}" style="position:absolute;left:-9999px" alt=""></div></noscript>'''


def header(path, prefix):
    active = NAV_ACTIVE.get(path, path)
    if path.startswith("napravleniya/"):
        active = "napravleniya.html"

    def link(href, title, mobile=False):
        cur = ' aria-current="page"' if href == active else ""
        return f'<a href="{prefix}{href}"{cur}>{title}</a>'
    desk = "\n".join(link(h, t) for h, t in NAV)
    mob = "\n".join(link(h, t, True) for h, t in NAV)
    return f'''<a class="skip" href="#main">К содержанию</a>
<header class="hdr"><div class="wrap hdr__in">
<a class="hdr__logo" href="{prefix}index.html" aria-label="ЗПТК — на главную"><img class="z-logo-d" src="{prefix}logo.png" alt="ЗПТК — Завод программно-технических комплексов" width="169" height="44"><img class="z-logo-n" src="{prefix}logo-dark.png" alt="ЗПТК — Завод программно-технических комплексов" width="169" height="44"></a>
<nav class="hdr__nav" aria-label="Основное меню">
{desk}
</nav>
<div class="hdr__side">
<a class="hdr__phone" href="tel:{ORG["phone_href"]}">{ORG["phone"]}</a>
<button type="button" data-z="theme" class="tbtn" aria-label="Переключить дневную / вечернюю тему" title="Дневная / вечерняя тема"><svg class="z-ic-moon" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg><svg class="z-ic-sun" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
<button type="button" data-z="sound" class="tbtn" aria-pressed="false" aria-label="Звук электричества" title="Звук электричества"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path class="z-ic-wave" d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path class="z-ic-mute" d="M16 9.5l5 5M21 9.5l-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
<button type="button" class="tbtn burger" aria-label="Меню" aria-expanded="false" aria-controls="zMnav" id="zBurger"><span class="z-ic-close" hidden><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M5 5 L17 17 M17 5 L5 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span><span class="z-ic-open"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M3 6 H19 M3 11 H19 M3 16 H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span></button>
</div></div>
<nav hidden id="zMnav" class="mnav" aria-label="Мобильное меню">
{mob}
<a href="tel:{ORG["phone_href"]}" class="mono">{ORG["phone"]}</a>
</nav>
</header>'''


def footer(prefix):
    dirs_col = "".join(f'<a href="{prefix}napravleniya/{d["slug"]}.html">{d["title"]}</a>' for d in DIRECTIONS)
    return f'''<footer class="ftr"><div class="wrap ftr__in">
<div><div class="ftr__h" data-zk>{ORG["name"]} ({ORG["short"]})</div>
<p>Инжиниринговая группа полного цикла: связь, логистика, энергетика, собственное ПО и EPCM.</p>
<p class="mono" style="font-size:13px;margin-top:10px">ИНН {ORG["inn"]} · КПП {ORG["kpp"]} · ОГРН {ORG["ogrn"]}</p>
<p style="margin-top:10px"><a href="tel:{ORG["phone_href"]}" class="mono">{ORG["phone"]}</a><br><a href="mailto:{ORG["email"]}" class="mono">{ORG["email"]}</a></p></div>
<nav aria-label="Направления"><div class="ftr__h">Направления</div>{dirs_col}</nav>
<nav aria-label="Компания"><div class="ftr__h">Компания</div>
<a href="{prefix}o-kompanii.html">О компании</a><a href="{prefix}razrabotki.html">Собственные разработки</a>
<a href="{prefix}partnery.html">Ориентиры и технологии</a><a href="{prefix}proekty.html">Проекты и кейсы</a>
<a href="{prefix}prezentaciya.html">Презентация (PDF)</a><a href="{prefix}it.html">Сведения об IT-деятельности</a>
<a href="{prefix}kontakty.html">Контакты и реквизиты</a></nav>
</div>
<div class="ftr__bar"><div class="wrap"><span>© 2005–{date.today().year} {ORG["short"]}</span><a href="{prefix}politika.html">Политика конфиденциальности</a></div></div>
</footer>'''


def layout(path, title, description, body, ld=(), extra_head="", og_title=None):
    depth = path.count("/")
    prefix = "../" * depth
    url = BASE_URL + ("" if path == "index.html" else path)
    lds = [org_ld()] + list(ld)
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    og_title = og_title or title
    return f'''<!doctype html>
<!--
  Design & development: kapa
  Страница собрана скриптом _build/build.py — правьте исходники в _build/.
-->
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta name="author" content="kapa">
<link rel="canonical" href="{url}">
<link rel="preload" href="{prefix}plex-sans-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}fonts.css">
<link rel="stylesheet" href="{prefix}assets/site.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ЗПТК">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{E(og_title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}og-zptk.jpg">
<meta property="og:image:alt" content="ЗПТК — инжиниринг полного цикла для критической инфраструктуры">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A2A42">
<link rel="icon" href="{prefix}favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png">
<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
<script>(function(){{var t=null;try{{t=localStorage.getItem('zptk-theme')}}catch(e){{}}if(t!=='day'&&t!=='night'){{var h=new Date().getHours();t=(h>=7&&h<19)?'day':'night'}}document.documentElement.classList.add('z-'+t);}})();</script>
{ld_html}
{extra_head}
{metrika()}
</head>
<body>
<div class="z-root">
{header(path, prefix)}
<main id="main">
{body}
</main>
{footer(prefix)}
</div>
<script src="{prefix}assets/site.js" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- страницы

PAGES = {}  # path -> html


def add(path, html_text):
    PAGES[path] = html_text


def page_index():
    blocks = []
    for b in BLOCKS:
        dirs = [d for d in DIRECTIONS if d["block"] == b["key"]]
        lis = "".join(f'<li><a href="napravleniya/{d["slug"]}.html">{d["title"]}</a></li>' for d in dirs)
        blocks.append(f'''<article class="card block reveal">{icon(b["icon"])}
<span class="block__num">{b["n"]} · {len(dirs)} {"направление" if len(dirs) == 1 else "направления" if len(dirs) in (2, 3, 4) else "направлений"}</span>
<h3 class="h3">{b["title"]}</h3><p>{b["text"]}</p><ul class="block__list">{lis}</ul></article>''')
    products = []
    for p in PRODUCTS:
        products.append(f'''<a class="card card--dark reveal" href="razrabotki.html#{p["id"]}">{status(p["status"])}
<h3 class="h3" style="color:#fff">{p["title"]}</h3><p>{p["lead"]}</p><span class="card__more">Подробнее {ARR}</span></a>''')
    cases = "".join(f'''<a class="card reveal" href="proekty.html#case-{i + 1}"><span class="card__tag">Кейс {i + 1:02d} · {DIR_BY_SLUG[c["dir"]]["title"]}</span>
<h3 class="h3" style="font-size:21px">{c["title"]}</h3><span class="card__more">Подробнее {ARR}</span></a>''' for i, c in enumerate(CASES))
    partners = ["Motorola Solutions", "Cisco Systems", "KNAPP", "SSI Schäfer", "ГК «FIRST»", "AXELOT", "МТС", "Ростелеком",
                "Сервионика", "Прософт-Системы", "ИНБРЭС", "Bechtel", "Fluor"]
    body = f'''<section class="hero" id="top">{dark_bg()}
<div class="wrap hero__in"><div class="hero__row">
<div class="hero__text">
<span class="hero__badge z-rise"><span class="dot z-live"></span>Инжиниринговая группа полного цикла · с 2005 года</span>
<h1 class="h1 z-rise" style="animation-delay:.12s">Инжиниринг полного цикла для критической инфраструктуры</h1>
<p class="hero__sub z-rise" style="animation-delay:.2s">Связь. Логистика. Энергетика. Собственное&nbsp;ПО. ИИ-агенты. EPCM.</p>
<p class="lead z-rise" style="animation-delay:.28s">Проектируем, строим и обслуживаем инфраструктуру повышенной отказоустойчивости. Развиваем собственные разработки на базе ИИ и ведём проекты по EPCM-контрактам.</p>
<div class="actions z-rise" style="animation-delay:.36s">{pdf_button()}<a class="btn btn--ghost btn--lg" href="napravleniya.html">8 направлений {ARR}</a></div>
</div>
<div class="hero__art">{emblem()}</div>
</div>
<div class="z-rise" style="animation-delay:.5s">{stats(STATS_MAIN)}</div>
</div></section>

<section class="sec" id="napravleniya"><div class="wrap stack-lg">
<div class="sec-head reveal"><div><span class="eyebrow">Чем мы занимаемся</span>
<h2 class="h2">Четыре блока, восемь направлений</h2>
<p class="lead">От проекта и стройки до собственного ПО и сервиса: одна группа отвечает за весь жизненный цикл объекта.</p></div>
<a class="link-arr" href="napravleniya.html">Все направления {ARR}</a></div>
<div class="grid-4">{"".join(blocks)}</div>
</div></section>

<section class="sec sec--dark">{dark_bg()}<div class="wrap stack-lg" style="position:relative">
<div class="sec-head reveal"><div><span class="eyebrow">Как работают наши решения</span>
<h2 class="h2">Сигнал → решение → действие</h2>
<p class="lead">Каждая система, которую мы строим, замыкает этот контур: данные с объекта превращаются в действие раньше, чем отказ превратится в убыток.</p></div></div>
{flow([("Сигнал", "Данные с объекта", "Приборы учёта, каналы связи, складская автоматика, журналы событий"),
       ("Решение", "Собственное ПО и ИИ", "ЕЦУД, предиктивная аналитика и ИИ-агенты в защищённом контуре"),
       ("Действие", "Результат для заказчика", "Резерв включён, потери найдены, бригада выехала до аварии")], label="Схема сигнал, решение, действие")}
</div></section>

<section class="sec sec--dark" style="padding-top:0"><div class="wrap stack-lg" style="position:relative">
<div class="sec-head reveal"><div><span class="eyebrow">Собственные разработки</span>
<h2 class="h2">ПО в реестре и ИИ-агенты</h2></div>
<a class="link-arr" href="razrabotki.html">Все разработки {ARR}</a></div>
<div class="grid-4">{"".join(products)}</div></div></section>

<section class="sec sec--tight"><div class="wrap stack">
<div class="sec-head reveal"><div><span class="eyebrow">Ориентиры</span>
<h2 class="h2">Равняемся на лидеров рынка</h2></div>
<a class="link-arr" href="partnery.html">Все ориентиры и технологии {ARR}</a></div>
{chips(partners)}
</div></section>

<section class="sec sec--alt"><div class="wrap stack-lg">
<div class="sec-head reveal"><div><span class="eyebrow">Проекты</span>
<h2 class="h2">Кейсы: задача → решение → результат</h2>
<p class="lead">Более 70 крупных проектов для сетевых, генерирующих и телеком-компаний. Названия заказчиков в кейсах скрыты по NDA.</p></div>
<a class="link-arr" href="proekty.html">Все проекты {ARR}</a></div>
<div class="grid-4">{cases}</div></div></section>

{cta_presentation()}'''
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "ЗПТК", "url": BASE_URL, "inLanguage": "ru"}]
    add("index.html", layout("index.html",
                             "ЗПТК — инжиниринг полного цикла: связь, логистика, энергетика, АИИС КУЭ, EPCM",
                             "Инжиниринговая группа ЗПТК: связь, логистические центры, АИИС КУЭ и энергосервис, ЦОД, собственное ПО в реестре РФ, ИИ-агенты, предиктивный сервис и EPCM-контракты. С 2005 года.",
                             body, ld))


def status(st):
    kind, label = st
    if kind == "todo":
        return "" if HIDE_TODO else f'<span class="status">{T(label)}</span>'
    return f'<span class="status status--{kind}">{label}</span>'


def page_presentation():
    body = page_hero([("index.html", "Главная"), (None, "Презентация")], "Презентация ЗПТК",
                     "Скачать презентацию",
                     "Позиционирование, 8 направлений, собственные разработки, ориентиры и кейсы — в одном PDF-файле.",
                     f'<div class="actions">{pdf_button()}<a class="btn btn--ghost btn--lg" href="napravleniya.html">Смотреть направления на сайте {ARR}</a></div>')
    sections = [("01", "Позиционирование", "Инжиниринговая группа полного цикла для критической инфраструктуры"),
                ("02", "4 блока и 8 направлений", "Инфраструктура, собственные разработки, сервис, EPCM"),
                ("03", "Схемы решений", "Сигнал → решение → действие для каждого направления"),
                ("04", "Собственные разработки", "ПТК ЕЦУД в реестре, ИИ-агенты, анализ потерь, финансовый радар"),
                ("05", "Ориентиры и технологии", "Связь, логистика, сервис, ИИ-агенты, EPCM"),
                ("06", "Кейсы и контакты", "Задача, решение, технологии, результат")]
    cards = "".join(f'<div class="card"><span class="block__num">{n}</span><h3 class="h3" style="font-size:20px">{t}</h3><p>{d}</p></div>'
                    for n, t, d in sections)
    body += f'''<section class="sec"><div class="wrap stack-lg">
<div class="sec-head"><div><span class="eyebrow">Что внутри</span><h2 class="h2">Содержание презентации</h2></div></div>
<div class="grid">{cards}</div>
<p class="muted">Нужна презентация в другом формате или под конкретный объект? Напишите на <a href="mailto:{ORG["email"]}">{ORG["email"]}</a>.</p>
</div></section>'''
    add("prezentaciya.html", layout("prezentaciya.html", "Презентация ЗПТК (PDF) — инжиниринг полного цикла",
                                    "Скачайте презентацию ЗПТК: инжиниринг полного цикла, 8 направлений, собственное ПО в реестре РФ, ИИ-агенты, EPCM-контракты.",
                                    body, [crumbs_ld([("index.html", "Главная"), ("prezentaciya.html", "Презентация")])]))


# ---------------------------------------------------------------- прежние страницы

LEGACY = {
    "uslugi.html": ("ПТК ЕЦУД, ЕЦУД-аналитик и УСПД — собственные разработки ЗПТК",
                    [("index.html", "Главная"), ("razrabotki.html", "Разработки"), (None, "ЕЦУД и УСПД подробно")]),
    "proekty.html": (None, [("index.html", "Главная"), (None, "Проекты")]),
    "it.html": (None, [("index.html", "Главная"), ("o-kompanii.html", "О компании"), (None, "Сведения об IT-деятельности")]),
    "kontakty.html": ("Контакты и реквизиты — ЗПТК", [("index.html", "Главная"), (None, "Контакты")]),
    "politika.html": (None, [("index.html", "Главная"), (None, "Политика конфиденциальности")]),
}


def legacy_page(path, before="", after=""):
    src = open(os.path.join(BUILD, "legacy", path), encoding="utf-8").read()
    title = re.search(r"<!--title: (.*?)-->", src).group(1)
    desc = re.search(r"<!--description: (.*?)-->", src).group(1)
    styles = "".join(re.findall(r"<style>.*?</style>\s*", src, re.S))
    main = re.sub(r"<!--(title|description): .*?-->\s*", "", src)
    main = re.sub(r"<style>.*?</style>\s*", "", main, flags=re.S)
    new_title, crumbs = LEGACY[path]
    title = new_title or title
    # Текстовые «Главная / …» заменяем на ссылки
    cr = []
    for href, name in crumbs:
        cr.append(f'<a href="{href}" style="color:#A6C0D4">{E(name)}</a>' if href else E(name))
    main = re.sub(r'(<span style="font-family: \'IBM Plex Mono\', monospace; font-size: 13px; color: #A6C0D4;">)Главная / [^<]*(</span>)',
                  lambda m: m.group(1).replace("<span", '<nav aria-label="Хлебные крошки"').replace("</span>", "") + " / ".join(cr) + "</nav>",
                  main, count=1)
    # ссылки на прежние якоря форм больше не нужны: формы убраны
    main = main.replace('href="#form"', 'href="mailto:office@zptk.ru"').replace('href="kontakty.html#form"', 'href="mailto:office@zptk.ru"')
    if path == "politika.html" and METRIKA_ID:
        main = main.replace("Сайт не использует файлы cookie, системы веб-аналитики и счётчики.",
                            "Сайт использует сервис веб-аналитики Яндекс.Метрика (ООО «Яндекс»), который с помощью файлов cookie собирает обезличенные сведения о посещениях: просмотренные страницы, тип устройства, источник перехода. Эти сведения используются только для улучшения сайта. Вы можете отключить cookie в настройках браузера.")
    ld = [crumbs_ld([(h or path, n) for h, n in crumbs])]
    add(path, layout(path, title, desc, before + main + after, ld, extra_head=styles))


# ---------------------------------------------------------------- вспомогательные файлы


def write_all():
    for path, text in PAGES.items():
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(text)
    urls = sorted(PAGES)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        if p == "404.html":
            continue
        loc = BASE_URL + ("" if p == "index.html" else p)
        prio = "1.0" if p == "index.html" else ("0.8" if p.startswith("napravleniya") or p in ("razrabotki.html", "napravleniya.html") else "0.6")
        sm.append(f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {BASE_URL}sitemap.xml\n")
    # Список плейсхолдеров (в публичной сборке они скрыты, поэтому список не перезаписываем)
    if HIDE_TODO:
        print(f"Собрано страниц: {len(PAGES)}, плейсхолдеры скрыты (HIDE_TODO), список в _build/TODO.md")
        return
    rows = []
    for path in urls:
        for m in re.finditer(r'<em class="todo"[^>]*>(.*?)</em>', PAGES[path]):
            rows.append(f"- `{path}`: {re.sub('<[^>]+>', '', m.group(1))}")
    draft_slogans = {html.escape(d["slogan"]) for d in DIRECTIONS if d.get("slogan_draft")}
    seen, uniq = set(), []
    for r in rows:
        if r.split(": ", 1)[1] in draft_slogans:
            continue
        if r not in seen:
            seen.add(r)
            uniq.append(r)
    drafts = [f"- `napravleniya/{d['slug']}.html`: слоган-черновик «{d['slogan']}»" for d in DIRECTIONS if d.get("slogan_draft")]
    open(os.path.join(BUILD, "TODO.md"), "w", encoding="utf-8").write(
        "# Что уточнить у ЗПТК\n\nФайл собирается автоматически из плейсхолдеров `T(...)` в `_build/data.py`.\n\n"
        "## Плейсхолдеры на страницах\n\n" + ("\n".join(uniq) or "— нет") +
        "\n\n## Слоганы-черновики (заменить слоганами из презентации)\n\n" + ("\n".join(drafts) or "— нет") + "\n")
    print(f"Собрано страниц: {len(PAGES)}, плейсхолдеров: {len(uniq)}")


def main():
    page_index()
    page_presentation()
    import pages_more  # noqa: F401  — разделы второго этапа, если есть
    pages_more.build(sys.modules[__name__])
    for path in LEGACY:
        if path not in PAGES:
            legacy_page(path)
    write_all()


if __name__ == "__main__":
    main()
