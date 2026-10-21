#!/usr/bin/env python3
"""Презентация ЗПТК в PDF, собранная из тех же данных, что и сайт.

Запуск из корня репозитория:
  python3 _build/presentation.py        # пишет _build/out/presentation.html
  node _build/pdf.js                    # печатает zptk-prezentaciya.pdf через Chromium
Плейсхолдеры T(...) в PDF не попадают: пункты с ними пропускаются.
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data import ORG, BLOCKS, DIRECTIONS, PRODUCTS, PARTNER_GROUPS, CASES  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
E = html.escape
TODO = re.compile(r'<em class="todo"[^>]*>(.*?)</em>')


def has_todo(s):
    return bool(TODO.search(s or ""))


def clean(s):
    return TODO.sub(r"\1", s or "")


def keep(items):
    return [x for x in items if not has_todo(x if isinstance(x, str) else " ".join(x))]


def flow(steps):
    cells = []
    for i, (k, t, p) in enumerate(steps):
        cells.append(f'<div class="fs{" core" if i == 1 else ""}"><span class="k">{E(k)}</span><b>{E(t)}</b><p>{clean(p)}</p></div>')
    return '<div class="flow">' + '<i>→</i>'.join(cells) + '</div>'


def slide(inner, dark=False, n=None):
    foot = f'<div class="foot"><span>ЗПТК · инжиниринг полного цикла</span><span>{n:02d}</span></div>' if n else ""
    return f'<section class="slide{" dark" if dark else ""}">{inner}{foot}</section>'


def build():
    s, n = [], 1
    s.append(f'''<section class="slide dark cover"><div class="net"></div>
<img src="../../logo-dark.png" alt="ЗПТК" class="logo">
<span class="eyebrow">Инжиниринговая группа полного цикла · с {ORG["founded"]} года</span>
<h1>Инжиниринг полного цикла для критической инфраструктуры</h1>
<p class="sub">Связь. Логистика. Энергетика. Собственное ПО. ИИ-агенты. EPCM.</p>
<p class="pos">Проектируем, строим и обслуживаем инфраструктуру повышенной отказоустойчивости. Собственные разработки на базе ИИ. EPCM-контракты.</p>
<p class="contacts">{ORG["phone"]} · {ORG["email"]}</p></section>''')
    n += 1
    s.append(slide(f'''<span class="eyebrow">ЗПТК в цифрах</span><h2>Масштаб, который мы уже доказали</h2>
<div class="stats"><div><b>100 000+</b><span>точек учёта в реализованных проектах</span></div>
<div><b>{len(DIRECTIONS)}</b><span>направлений для заказчиков</span></div>
<div><b>№ {ORG["registry_no"]}</b><span>ПТК ЕЦУД в реестре российского ПО</span></div>
<div><b>70+</b><span>крупных проектов с {ORG["founded"]} года</span></div></div>
<p class="note">Ориентиры: Motorola Solutions, Cisco Systems, KNAPP, SSI Schäfer. Заказчики: Россети, ФСК ЕЭС, Мосэнерго, Ростелеком.</p>''', True, n))
    n += 1
    cols = []
    for b in BLOCKS:
        dirs = [d for d in DIRECTIONS if d["block"] == b["key"]]
        cols.append(f'<div class="col"><span class="k">{b["n"]}</span><h3>{b["title"]}</h3><p>{b["text"]}</p><ul>' +
                    "".join(f"<li>{d['title']}</li>" for d in dirs) + '</ul></div>')
    s.append(slide(f'<span class="eyebrow">Структура группы</span><h2>Четыре блока, восемь направлений</h2><div class="cols">{"".join(cols)}</div>', n=n))
    for i, d in enumerate(DIRECTIONS):
        n += 1
        tech = " · ".join(t for t, x in d["tech"])
        res = "".join(f"<li>{r}</li>" for r in keep(d["result"]))
        partners = ", ".join(d["partners"] + d.get("benchmarks", []))
        dk = d.get("deck")
        if dk:
            s.append(slide(f'''<div class="dk"><div class="dkl"><span class="eyebrow">Направление {i + 1:02d} · {E(next(b["title"] for b in BLOCKS if b["key"] == d["block"]))}</span>
<h2>{d["title"]}</h2><p class="slogan">{E(d["slogan"])}</p>
<h4>Проблема клиента</h4><p>{d["problem"]}</p><h4>Технологии</h4><p>{tech}</p>
<h4>Результат для заказчика</h4><ul class="ok">{res}</ul>{f"<h4>Ориентиры и технологии</h4><p>{partners}</p>" if partners else ""}</div>
<figure><img src="../../img/schemes/{dk["n"]:02d}.webp" alt=""></figure></div>''', n=n))
            continue
        s.append(slide(f'''<span class="eyebrow">Направление {i + 1:02d} · {E(next(b["title"] for b in BLOCKS if b["key"] == d["block"]))}</span>
<h2>{d["title"]}</h2><p class="slogan">{E(d["slogan"])}</p>
<div class="two"><div><h4>Проблема клиента</h4><p>{d["problem"]}</p><h4>Технологии</h4><p>{tech}</p></div>
<div><h4>Результат для заказчика</h4><ul class="ok">{res}</ul>{f"<h4>Ориентиры и технологии</h4><p>{partners}</p>" if partners else ""}</div></div>
{flow(d["flow"])}''', n=n))
    n += 1
    prods = ""
    for p in PRODUCTS:
        st = "" if p["status"][0] == "todo" else f'<span class="st">{p["status"][1]}</span>'
        prods += f'<div class="col"><h3>{p["title"]}</h3>{st}<p>{clean(p["lead"])}</p></div>'
    s.append(slide(f'<span class="eyebrow">Собственные разработки</span><h2>ПО в реестре и ИИ-агенты</h2><div class="cols">{prods}</div>', True, n))
    n += 1
    rows = "".join(f'<tr><th>{g}</th><td>{", ".join(x for x, _ in items)}</td></tr>' for g, _, items in PARTNER_GROUPS)
    s.append(slide(f'<span class="eyebrow">Ориентиры и технологии</span><h2>На кого равняемся и на чём строим</h2><table>{rows}</table>', n=n))
    n += 1
    cases = "".join(f'<div class="case"><h3>{c["title"]}</h3><p><b>Задача.</b> {c["task"]}</p><p><b>Решение.</b> {c["solution"]}</p><p><b>Технологии.</b> {c["tech"]}</p>' +
                    ("" if has_todo(c["result"]) else f'<p><b>Результат.</b> {c["result"]}</p>') + '</div>' for c in CASES)
    s.append(slide(f'<span class="eyebrow">Кейсы · заказчики под NDA</span><h2>Задача → решение → результат</h2><div class="cases">{cases}</div>', n=n))
    s.append(f'''<section class="slide dark cover"><div class="net"></div><img src="../../logo-dark.png" alt="ЗПТК" class="logo">
<h1 style="font-size:52px">Обсудим ваш объект</h1>
<p class="pos">{ORG["name"]}<br>{ORG["addr"]}<br>Филиал: {ORG["addr_branch"]}</p>
<p class="contacts" style="font-size:30px">{ORG["phone"]}<br>{ORG["email"]}</p></section>''')
    css = open(os.path.join(os.path.dirname(__file__), "presentation.css"), encoding="utf-8").read()
    doc = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>ЗПТК — презентация</title>
<link rel="stylesheet" href="../../fonts.css"><style>{css}</style></head><body>{"".join(s)}</body></html>'''
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "presentation.html"), "w", encoding="utf-8").write(doc)
    print("Слайдов:", len(s))


if __name__ == "__main__":
    build()
