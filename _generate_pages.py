# -*- coding: utf-8 -*-
"""One-shot generator for service / city / rental pages."""
from __future__ import annotations

import json
import html as html_lib
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CRITICAL_CSS = (ROOT / "assets" / "css" / "critical.css").read_text(encoding="utf-8").strip()

HEAD_ASSETS = f"""<style>{CRITICAL_CSS}</style>
<link rel="preload" href="assets/css/main.css" as="style"/>
<link rel="preload" href="assets/fonts/nwpStKy2OAdR1K-IwhWudF-R3wsaZfrc.woff2" as="font" type="font/woff2" crossorigin/>
<link rel="stylesheet" href="assets/css/fonts.css" media="print" onload="this.media='all'"/>
<link rel="stylesheet" href="assets/css/main.css" media="print" onload="this.media='all'"/>
<noscript><link rel="stylesheet" href="assets/css/fonts.css"/><link rel="stylesheet" href="assets/css/main.css"/></noscript>"""

HEAD_COMMON = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<script>document.documentElement.classList.add("js");</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta http-equiv="x-ua-compatible" content="ie=edge"/>
<title>{title}</title>
<meta name="description" content="{description}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<meta name="googlebot" content="index,follow"/>
<meta name="yandex" content="index,follow"/>
<meta name="format-detection" content="telephone=yes"/>
<meta name="geo.region" content="RU-VLA"/>
<meta name="geo.placename" content="{geo_place}"/>
<meta name="author" content="HimchistkaDoma"/>
<link rel="canonical" href="https://himchistkadoma.ru/{slug}"/>
<meta property="og:type" content="website"/>
<meta property="og:locale" content="ru_RU"/>
<meta property="og:site_name" content="HimchistkaDoma"/>
<meta property="og:url" content="https://himchistkadoma.ru/{slug}"/>
<meta property="og:title" content="{og_title}"/>
<meta property="og:description" content="{description}"/>
<meta property="og:image" content="https://himchistkadoma.ru/assets/img/og-image.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="{og_title}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{og_title}"/>
<meta name="twitter:description" content="{description}"/>
<meta name="twitter:image" content="https://himchistkadoma.ru/assets/img/og-image.jpg"/>
<meta name="theme-color" content="#F0B429"/>
<link rel="icon" href="assets/favicon/favicon.ico" type="image/x-icon"/>
<link rel="icon" href="assets/favicon/favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="assets/favicon/favicon_32x32.png" sizes="32x32" type="image/png"/>
<link rel="apple-touch-icon" href="assets/favicon/favicon_180x180.png" sizes="180x180"/>
<link rel="manifest" href="site.webmanifest"/>
{head_assets}
</head>
<body>
"""

HEADER = """
<header class="site-header">
  <div class="header-shell">
    <div class="header-inner">
      <a class="logo" href="index.html">
        <div class="logo-icon">ХМ</div>
        <div>
          <div class="logo-main">HimchistkaDoma</div>
          <div class="logo-sub">Владимир · Ковров · Доброград</div>
        </div>
      </a>
      <nav class="nav-desktop" aria-label="Основное меню">
        <a href="himchistka-divanov.html">Диваны</a>
        <a href="himchistka-matrasov.html">Матрасы</a>
        <a href="himchistka-kovrov.html">Ковры</a>
        <a href="himchistka-kresel-i-stulev.html">Кресла</a>
        <a href="index.html#price">Цены</a>
      </nav>
      <div class="header-right">
        <div class="header-time">Пн–Вс 9:00–21:00</div>
        <a class="header-phone" href="tel:+79157548115">8&nbsp;915&nbsp;754-81-15</a>
        <a class="btn btn-primary btn-small header-cta" href="#form-block">Заявка</a>
      </div>
      <button aria-label="Открыть меню" aria-expanded="false" class="burger" id="burger" type="button">
        <div class="burger-lines"><span></span><span></span><span></span></div>
      </button>
    </div>
  </div>
  <div class="mobile-menu" id="mobile-menu">
    <div class="mobile-menu-nav">
      <a href="index.html">Главная</a>
      <a href="himchistka-divanov.html">Химчистка диванов</a>
      <a href="himchistka-matrasov.html">Химчистка матрасов</a>
      <a href="himchistka-kovrov.html">Химчистка ковров</a>
      <a href="himchistka-kresel-i-stulev.html">Кресла и стулья</a>
      <a href="index.html#price">Цены</a>
      <a href="#form-block">Заявка</a>
      <a href="#contacts">Контакты</a>
    </div>
    <div class="mobile-menu-footer">
      <a class="mobile-menu-phone" href="tel:+79157548115">8&nbsp;915&nbsp;754-81-15</a>
      <div class="mobile-menu-time">Пн–Вс 9:00–21:00</div>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer class="site-footer">
  <div class="container footer-inner">
    <div>© <span id="year"></span> HimchistkaDoma — химчистка мягкой мебели и ковров.</div>
    <div class="footer-links">
      <a href="privacy.html">Политика конфиденциальности</a>
      <a href="tel:+79157548115">8&nbsp;915&nbsp;754-81-15</a>
    </div>
  </div>
</footer>
<div class="mobile-call-bar">
  <a class="mobile-call-btn" href="tel:+79157548115">Позвонить</a>
</div>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""

FORM_SECTION = """
<section class="section-alt" id="form-block">
  <div class="container">
    <div class="section-header">
      <span class="section-eyebrow">Заявка</span>
      <h2 class="section-title">Оставить заявку</h2>
      <p class="section-sub">Пришлите фото — назовём точную цену до выезда. Перезвоним за 15–30 минут.</p>
    </div>
    <div class="contact-grid">
      <div class="contact-block">
        <div class="contact-row">
          <span class="contact-label">Телефон</span>
          <span class="contact-value"><a href="tel:+79157548115">8&nbsp;915&nbsp;754-81-15</a></span>
        </div>
        <div class="contact-row">
          <span class="contact-label">Мессенджеры</span>
          <span class="contact-value">
            <a href="https://wa.me/79157548115" target="_blank" rel="noopener">WhatsApp</a> ·
            <a href="https://t.me/himchistka_33" target="_blank" rel="noopener">Telegram</a> ·
            <a href="https://vk.com/kovrov_himchistka33" target="_blank" rel="noopener">VK</a>
          </span>
        </div>
        <div class="contact-row">
          <span class="contact-label">График</span>
          <span class="contact-value">Ежедневно 9:00–21:00</span>
        </div>
      </div>
      <div class="contact-block">
        <form enctype="multipart/form-data" id="request-form" onsubmit="return handleSubmit(event)">
          <div class="field">
            <label for="name">Имя</label>
            <input id="name" name="name" placeholder="Как к вам обращаться?" required type="text" autocomplete="name"/>
          </div>
          <div class="field">
            <label for="phone">Телефон</label>
            <div class="phone-input-wrap">
              <span class="phone-prefix">+7</span>
              <input id="phone" name="phone" placeholder="915 754-81-15" required type="tel" autocomplete="tel" inputmode="tel"/>
            </div>
          </div>
          <div class="field">
            <label for="comment">Что нужно почистить?</label>
            <textarea id="comment" name="comment" placeholder="{comment_placeholder}"></textarea>
          </div>
          <div class="field">
            <label class="visually-hidden" for="photos">Фото</label>
            <div class="upload-area" id="upload-area">
              <span class="upload-text">Перетащите или загрузите фото</span>
              <span class="upload-subtext">Можно несколько файлов</span>
            </div>
            <input accept="image/*" id="photos" multiple name="photos" style="display:none;" type="file"/>
            <div class="upload-info" id="upload-info">Файлы не выбраны</div>
          </div>
          <button class="btn btn-accent btn-block" type="submit">Отправить заявку</button>
          <div class="form-note">Нажимая кнопку, вы соглашаетесь с <a href="privacy.html">обработкой персональных данных</a>.</div>
          <div class="form-success" id="form-success">Заявка отправлена. Мы свяжемся с вами в ближайшее время.</div>
          <div class="form-error" id="form-error">Пожалуйста, укажите имя и корректный номер телефона.</div>
        </form>
      </div>
    </div>
  </div>
</section>
"""

CONTACTS = """
<section id="contacts">
  <div class="container">
    <div class="section-header">
      <span class="section-eyebrow">Связь</span>
      <h2 class="section-title">Контакты</h2>
    </div>
    <div class="contact-grid">
      <div class="contact-block">
        <div class="contact-row">
          <span class="contact-label">Телефон</span>
          <span class="contact-value"><a href="tel:+79157548115">8&nbsp;915&nbsp;754-81-15</a></span>
        </div>
        <div class="contact-row">
          <span class="contact-label">Зона работы</span>
          <span class="contact-value">Владимир, Ковров, Доброград и радиус 100&nbsp;км от Коврова.</span>
        </div>
        <div class="contact-row">
          <span class="contact-label">График</span>
          <span class="contact-value">Ежедневно с 9:00 до 21:00</span>
        </div>
      </div>
      <div class="contact-block">
        <p style="font-size:14px;color:var(--text-muted);margin-bottom:14px;">Присылайте фото — подскажем, что реально удалить, и озвучим честную цену.</p>
        <a class="btn btn-primary" href="#form-block">Оставить заявку</a>
      </div>
    </div>
  </div>
</section>
"""


def esc(s: str) -> str:
    return html_lib.escape(s, quote=True)


def render_faq(items: list[dict]) -> str:
    parts = ['<div class="faq-list">']
    for it in items:
        parts.append(
            f"<details><summary>{esc(it['q'])}</summary><p>{esc(it['a'])}</p></details>"
        )
    parts.append("</div>")
    return "\n".join(parts)


def render_faq_jsonld(items: list[dict]) -> str:
    entities = []
    for it in items:
        entities.append(
            {
                "@type": "Question",
                "name": it["q"],
                "acceptedAnswer": {"@type": "Answer", "text": it["a"]},
            }
        )
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>"
    )


SAME_AS = [
    "https://vk.com/kovrov_himchistka33",
    "https://t.me/himchistka_33",
    "https://wa.me/79157548115",
]


def render_business_jsonld(
    name: str,
    city: str | None = None,
    *,
    page_url: str | None = None,
    service_type: str | None = None,
    price: str | None = None,
) -> str:
    area = [
        {"@type": "City", "name": "Владимир"},
        {"@type": "City", "name": "Ковров"},
        {"@type": "City", "name": "Доброград"},
    ]
    if city:
        area = [{"@type": "City", "name": city}] + [
            a for a in area if a["name"] != city
        ]
    data: dict = {
        "@context": "https://schema.org",
        "@type": "CleaningService",
        "@id": (page_url or "https://himchistkadoma.ru/") + "#business",
        "name": name,
        "url": page_url or "https://himchistkadoma.ru/",
        "telephone": "+7-915-754-81-15",
        "image": "https://himchistkadoma.ru/assets/img/og-image.jpg",
        "logo": "https://himchistkadoma.ru/assets/favicon/favicon_512x512.png",
        "priceRange": "₽₽",
        "currenciesAccepted": "RUB",
        "paymentAccepted": "Cash, Card",
        "description": "Выездная химчистка мягкой мебели и ковров на дому во Владимире, Коврове и Доброграде.",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city or "Ковров",
            "addressRegion": "Владимирская область",
            "addressCountry": "RU",
        },
        "areaServed": area,
        "sameAs": SAME_AS,
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            "opens": "09:00",
            "closes": "21:00",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+7-915-754-81-15",
            "contactType": "customer service",
            "areaServed": "RU",
            "availableLanguage": ["Russian"],
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "201",
            "bestRating": "5",
            "worstRating": "1",
        },
    }
    if service_type and price:
        data["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": service_type,
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": service_type,
                        "serviceType": service_type,
                        "provider": {"@id": data["@id"]},
                    },
                    "priceCurrency": "RUB",
                    "price": price,
                    "availability": "https://schema.org/InStock",
                    "url": page_url or "https://himchistkadoma.ru/",
                }
            ],
        }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>"
    )


def render_breadcrumbs(items: list[tuple[str, str]]) -> tuple[str, str]:
    """items: (href, label). Last item may use empty href for current page."""
    crumbs = []
    ld_items = []
    for i, (href, label) in enumerate(items, start=1):
        if href:
            crumbs.append(f'<a href="{esc(href)}">{esc(label)}</a>')
            item_url = (
                f"https://himchistkadoma.ru{href}" if href.startswith("/") else href
            )
            ld_items.append(
                {
                    "@type": "ListItem",
                    "position": i,
                    "name": label,
                    "item": item_url,
                }
            )
        else:
            crumbs.append(f'<span aria-current="page">{esc(label)}</span>')
            ld_items.append({"@type": "ListItem", "position": i, "name": label})
    nav = (
        '<nav class="breadcrumbs" aria-label="Хлебные крошки">'
        + '<span class="breadcrumbs-sep"> / </span>'.join(crumbs)
        + "</nav>"
    )
    ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": ld_items,
    }
    script = (
        '<script type="application/ld+json">\n'
        + json.dumps(ld, ensure_ascii=False, indent=2)
        + "\n</script>"
    )
    return nav, script


def render_cards(cards: list[dict]) -> str:
    parts = ['<div class="cards-grid">']
    for c in cards:
        link_open = f'<a class="card-link" href="{esc(c["href"])}">' if c.get("href") else '<div class="card-link">'
        link_close = "</a>" if c.get("href") else "</div>"
        tag = f'<div class="card-tag">{esc(c["tag"])}</div>' if c.get("tag") else ""
        parts.append(
            f"""<article class="card">
          {link_open}
            <div class="card-top">
              <div class="card-icon" aria-hidden="true">{c.get("icon", "•")}</div>
              {tag}
            </div>
            <h3 class="card-title">{esc(c["title"])}</h3>
            <p class="card-text">{esc(c.get("text", ""))}</p>
            <div class="card-price">{c["price"]} <small>{esc(c.get("unit", ""))}</small></div>
          {link_close}
        </article>"""
        )
    parts.append("</div>")
    return "\n".join(parts)


def related_block(
    links: list[tuple[str, str, str]],
    *,
    eyebrow: str = "Ещё услуги",
    title: str = "Смотрите также",
    section_id: str = "related",
    alt: bool = True,
) -> str:
    section_class = ' class="section-alt"' if alt else ""
    parts = [
        f'<section{section_class} id="{section_id}">',
        '<div class="container">',
        f'<div class="section-header"><span class="section-eyebrow">{esc(eyebrow)}</span><h2 class="section-title">{esc(title)}</h2></div>',
        '<div class="related-grid">',
    ]
    for href, title, sub in links:
        parts.append(
            f'<a class="related-link" href="{esc(href)}">{esc(title)}<span>{esc(sub)}</span></a>'
        )
    parts += ["</div></div></section>"]
    return "\n".join(parts)


SOFA_FAQ = [
    {
        "q": "Сколько стоит химчистка дивана?",
        "a": "Цена зависит от размера (прямой/угловой), материала, количества подушек и степени загрязнения. Перед началом работ называем итоговую стоимость.",
    },
    {
        "q": "Сколько времени занимает химчистка?",
        "a": "Обычно 1–2 часа: осмотр, обработка пятен, основная чистка и экстракция.",
    },
    {
        "q": "Сколько сохнет диван после химчистки?",
        "a": "В среднем 4–8 часов. Скорость зависит от ткани, вентиляции и температуры.",
    },
    {
        "q": "Убираете ли запах мочи и запах животных?",
        "a": "Да, используем средства для нейтрализации запаха и глубокую экстракцию. В сложных случаях может потребоваться повторная обработка.",
    },
    {
        "q": "Безопасно ли для детей и животных?",
        "a": "Используем профессиональные средства для бытовых условий. После чистки проветрите помещение и дождитесь полного высыхания.",
    },
    {
        "q": "Выезд платный?",
        "a": "Выезд по Коврову бесплатный. По району и в другие города — по договорённости.",
    },
]

MATTRESS_FAQ = [
    {
        "q": "Сколько стоит химчистка матраса?",
        "a": "Ориентир — от 1 500 ₽ за сторону. Итоговая цена зависит от размера и загрязнения.",
    },
    {
        "q": "Можно ли чистить матрас с двух сторон?",
        "a": "Да, чистим обе стороны. Рекомендуем, если матрас давно не обрабатывали.",
    },
    {
        "q": "Убираете запахи и клеща?",
        "a": "Да, глубокая чистка помогает убрать запахи, пыль и снизить количество аллергенов.",
    },
    {
        "q": "Сколько сохнет матрас?",
        "a": "Обычно 8–12 часов. Ускоряет проветривание и вентилятор.",
    },
    {
        "q": "Нужно ли снимать чехол?",
        "a": "Если чехол съёмный — лучше снять заранее. Если нет — чистим как есть.",
    },
]

CARPET_FAQ = [
    {
        "q": "Сколько стоит химчистка ковра?",
        "a": "От 350 ₽ за м². Цена зависит от ворса, загрязнения и материала.",
    },
    {
        "q": "Нужно ли вывозить ковёр?",
        "a": "Нет, чистим на дому без вывоза.",
    },
    {
        "q": "Убираете запахи и шерсть животных?",
        "a": "Да, убираем шерсть, запахи и бытовые загрязнения.",
    },
    {
        "q": "Сколько сохнет ковёр?",
        "a": "Обычно 6–12 часов в зависимости от ворса и вентиляции.",
    },
]

CHAIR_FAQ = [
    {
        "q": "Сколько стоит химчистка кресла или стула?",
        "a": "От 300 ₽ за единицу. Для комплектов — выгоднее.",
    },
    {
        "q": "Чистите офисные кресла?",
        "a": "Да, выезжаем в офисы, кафе и салоны. Возможно безналичное закрытие.",
    },
    {
        "q": "Сколько сохнет?",
        "a": "Обычно 3–6 часов.",
    },
    {
        "q": "Можно ли почистить несколько стульев за раз?",
        "a": "Да, при комплексном заказе действует скидка до 15%.",
    },
]

SERVICES = {
    "himchistka-divanov.html": {
        "title": "Химчистка диванов на дому — цены | Владимир, Ковров",
        "description": "Химчистка диванов на дому во Владимире, Коврове и Доброграде. Удаляем пятна и запахи. Выезд бесплатно, оплата после результата. От 3 500 ₽.",
        "h1": "Выездная химчистка диванов — Владимир, Ковров, Доброград",
        "subtitle": "Прямые и угловые, выкатные, со спальным местом. Удаляем пятна от еды, напитков, животных. Цена по фото — фиксированная.",
        "price_from": "от 3&nbsp;500&nbsp;₽",
        "offer_price": "3500",
        "service_type": "Химчистка диванов",
        "cards": [
            {"icon": "🛋", "tag": "Хит", "title": "Прямой диван", "text": "2–3 посадочных места, стандартная чистка с экстракцией.", "price": "от 3&nbsp;500&nbsp;₽", "unit": "за диван"},
            {"icon": "🛋", "tag": "Популярно", "title": "Угловой диван", "text": "Угловые и П-образные. Учитываем подушки и спальное место.", "price": "от 4&nbsp;500&nbsp;₽", "unit": "за диван"},
            {"icon": "🛋", "title": "Диван-кровать", "text": "Выкатные и раскладные модели. Чистим сиденье и спальную зону.", "price": "от 4&nbsp;000&nbsp;₽", "unit": "за диван"},
            {"icon": "✨", "title": "Локальная чистка пятен", "text": "Точечная обработка сложных пятен без полной мойки всего изделия.", "price": "от 1&nbsp;500&nbsp;₽", "unit": "за зону"},
        ],
        "faq": SOFA_FAQ,
        "seo_paras": [
            "Если на диване появились пятна от еды и напитков, следы домашних животных или неприятный запах — не обязательно покупать новую мебель. Мы делаем химчистку дивана на дому: приезжаем в удобное время, подбираем химию под ткань и степень загрязнения, выполняем глубокую очистку и экстракцию.",
            "Что удаляем: пятна от кофе, чая, вина и еды; запахи (в том числе животных); шерсть и следы лап; пыль, аллергены и бытовые загрязнения.",
            "Итоговая цена зависит от размера, материала, количества подушек и сложности пятен. Перед началом работ оцениваем объём и называем стоимость. Оплата — после результата.",
        ],
        "city_links": [
            ("/himchistka-divana-vladimir.html", "Химчистка диванов во Владимире", "Выезд на дом"),
            ("/himchistka-divana-kovrov.html", "Химчистка диванов в Коврове", "Выезд бесплатно"),
            ("/himchistka-divana-dobrograd.html", "Химчистка диванов в Доброграде", "Ковровский район"),
        ],
        "related": [
            ("/himchistka-matrasov.html", "Химчистка матрасов", "от 1 500 ₽"),
            ("/himchistka-kovrov.html", "Химчистка ковров", "от 350 ₽/м²"),
            ("/himchistka-kresel-i-stulev.html", "Кресла и стулья", "от 300 ₽"),
        ],
        "comment": "Например: угловой диван, Ковров",
        "city": None,
        "service_name": "Химчистка диванов HimchistkaDoma",
    },
    "himchistka-matrasov.html": {
        "title": "Химчистка матрасов на дому — цены | Владимир, Ковров",
        "description": "Химчистка матрасов на дому во Владимире, Коврове и Доброграде. Удаляем пятна, запахи и аллергены. Безопасно для детей. От 1 500 ₽.",
        "h1": "Выездная химчистка матрасов — Владимир, Ковров, Доброград",
        "subtitle": "Глубокая чистка с обеззараживанием. Боремся с запахами и пылевым клещом — подходит детям и аллергикам.",
        "price_from": "от 1&nbsp;500&nbsp;₽",
        "offer_price": "1500",
        "service_type": "Химчистка матрасов",
        "cards": [
            {"icon": "🛏", "tag": "Стандарт", "title": "Одна сторона", "text": "Чистка рабочей стороны матраса любой жёсткости.", "price": "от 1&nbsp;500&nbsp;₽", "unit": "за сторону"},
            {"icon": "🛏", "tag": "Рекомендуем", "title": "Две стороны", "text": "Полная обработка матраса с двух сторон.", "price": "от 2&nbsp;800&nbsp;₽", "unit": "за матрас"},
            {"icon": "🛏", "title": "Детский матрас", "text": "Мягкая химия, аккуратная сушка. Для детских и подростковых.", "price": "от 1&nbsp;200&nbsp;₽", "unit": "за сторону"},
            {"icon": "✨", "title": "Удаление запахов", "text": "Нейтрализация запахов и глубокая экстракция проблемных зон.", "price": "от 2&nbsp;000&nbsp;₽", "unit": "за матрас"},
        ],
        "faq": MATTRESS_FAQ,
        "seo_paras": [
            "Химчистка матраса на дому помогает убрать пятна, запахи, пыль и аллергены без вывоза. Подбираем химию под тип наполнителя и чехла.",
            "После чистки матрас обычно сохнет 8–12 часов. Рекомендуем проветрить комнату.",
        ],
        "city_links": [
            ("/himchistka-matrasa-vladimir.html", "Химчистка матрасов во Владимире", "Выезд на дом"),
            ("/himchistka-matrasa-kovrov.html", "Химчистка матрасов в Коврове", "Выезд бесплатно"),
            ("/himchistka-matrasa-dobrograd.html", "Химчистка матрасов в Доброграде", "Ковровский район"),
        ],
        "related": [
            ("/himchistka-divanov.html", "Химчистка диванов", "от 3 500 ₽"),
            ("/himchistka-kovrov.html", "Химчистка ковров", "от 350 ₽/м²"),
            ("/himchistka-kresel-i-stulev.html", "Кресла и стулья", "от 300 ₽"),
        ],
        "comment": "Например: матрас 160×200, обе стороны",
        "city": None,
        "service_name": "Химчистка матрасов HimchistkaDoma",
    },
    "himchistka-kovrov.html": {
        "title": "Химчистка ковров на дому — цены за м² | Владимир, Ковров",
        "description": "Химчистка ковров и паласов на дому во Владимире, Коврове и Доброграде без вывоза. От 350 ₽/м². Выезд бесплатно, оплата после результата.",
        "h1": "Выездная химчистка ковров — Владимир, Ковров, Доброград",
        "subtitle": "Чистим ковры и паласы на дому без вывоза. Убираем запахи, шерсть животных и сложные загрязнения.",
        "price_from": "от 350&nbsp;₽/м²",
        "offer_price": "350",
        "service_type": "Химчистка ковров",
        "cards": [
            {"icon": "🧼", "tag": "Ковры", "title": "Ковёр с коротким ворсом", "text": "Стандартная чистка с экстракцией.", "price": "от 350&nbsp;₽", "unit": "за м²"},
            {"icon": "🧼", "title": "Длинный ворс / шегги", "text": "Более тщательная проработка и сушка.", "price": "от 450&nbsp;₽", "unit": "за м²"},
            {"icon": "🧼", "title": "Палас / дорожка", "text": "Чистка без вывоза, аккуратно по краям.", "price": "от 350&nbsp;₽", "unit": "за м²"},
            {"icon": "✨", "title": "Сложные пятна", "text": "Локальная обработка пятен и запахов.", "price": "по оценке", "unit": ""},
        ],
        "faq": CARPET_FAQ,
        "seo_paras": [
            "Химчистка ковра на дому экономит время: не нужно сворачивать и везти изделие. Приезжаем с оборудованием, чистим и оставляем рекомендации по сушке.",
            "Цена зависит от площади, высоты ворса и степени загрязнения. Точную стоимость назовём по фото или на месте до начала работ.",
        ],
        "city_links": [
            ("/himchistka-kovrov-vladimir.html", "Химчистка ковров во Владимире", "Выезд на дом"),
            ("/himchistka-kovrov-kovrov.html", "Химчистка ковров в Коврове", "Выезд бесплатно"),
            ("/himchistka-kovrov-dobrograd.html", "Химчистка ковров в Доброграде", "Ковровский район"),
        ],
        "related": [
            ("/himchistka-divanov.html", "Химчистка диванов", "от 3 500 ₽"),
            ("/himchistka-matrasov.html", "Химчистка матрасов", "от 1 500 ₽"),
            ("/arenda-ekstraktora-dlya-mebeli-i-kovrov.html", "Аренда экстрактора", "самостоятельно"),
        ],
        "comment": "Например: ковёр 2×3 м, Ковров",
        "city": None,
        "service_name": "Химчистка ковров HimchistkaDoma",
    },
    "himchistka-kresel-i-stulev.html": {
        "title": "Химчистка кресел и стульев на дому — цены | Ковров",
        "description": "Химчистка кресел и стульев на дому и в офисе во Владимире, Коврове и Доброграде. От 300 ₽. Выезд бесплатно, оплата после результата.",
        "h1": "Выездная химчистка кресел и стульев — Владимир, Ковров, Доброград",
        "subtitle": "Обновим посадочные места, подлокотники и спинки. Для дома, кафе и офисов.",
        "price_from": "от 300&nbsp;₽",
        "offer_price": "300",
        "service_type": "Химчистка кресел и стульев",
        "cards": [
            {"icon": "🪑", "tag": "Дом", "title": "Стул мягкий", "text": "Сиденье и спинка. Идеально для комплектов.", "price": "от 300&nbsp;₽", "unit": "за шт."},
            {"icon": "🪑", "title": "Кресло домашнее", "text": "Посадочное место, подлокотники, спинка.", "price": "от 800&nbsp;₽", "unit": "за шт."},
            {"icon": "🪑", "tag": "Офис", "title": "Офисное кресло", "text": "Ткань или сетка. Выезд в офис возможен.", "price": "от 700&nbsp;₽", "unit": "за шт."},
            {"icon": "✨", "title": "Комплект от 6 шт.", "text": "Скидка на комплексную чистку стульев.", "price": "скидка до 15%", "unit": ""},
        ],
        "faq": CHAIR_FAQ,
        "seo_paras": [
            "Химчистка кресел и стульев возвращает свежий вид посадочным местам без замены обивки. Работаем дома, в офисах, кафе и салонах.",
            "При заказе нескольких изделий действует скидка. Возможна безналичная оплата для организаций.",
        ],
        "city_links": [
            ("/himchistka-kresel-i-stulev-vladimir.html", "Кресла и стулья во Владимире", "Выезд на дом"),
            ("/himchistka-kresel-i-stulev-kovrov.html", "Кресла и стулья в Коврове", "Выезд бесплатно"),
            ("/himchistka-kresel-i-stulev-dobrograd.html", "Кресла и стулья в Доброграде", "Ковровский район"),
        ],
        "related": [
            ("/himchistka-divanov.html", "Химчистка диванов", "от 3 500 ₽"),
            ("/himchistka-matrasov.html", "Химчистка матрасов", "от 1 500 ₽"),
            ("/himchistka-kovrov.html", "Химчистка ковров", "от 350 ₽/м²"),
        ],
        "comment": "Например: 6 стульев + кресло, офис",
        "city": None,
        "service_name": "Химчистка кресел и стульев HimchistkaDoma",
    },
}

CITY_PAGES = [
    # (filename, service_key, city_name, h1, title, description)
    ("himchistka-divana-vladimir.html", "sofa", "Владимир", "Химчистка диванов во Владимире", "Химчистка диванов во Владимире на дому — цены", "Химчистка диванов на дому во Владимире. Удаляем пятна и запахи. Выезд, оплата после результата. Тел.: +7 915 754-81-15."),
    ("himchistka-divana-kovrov.html", "sofa", "Ковров", "Химчистка диванов в Коврове и Ковровском районе", "Химчистка диванов в Коврове — цены с выездом", "Химчистка диванов в Коврове на дому. Выезд бесплатно. Удаляем пятна и запахи. Оплата после результата. От 3 500 ₽."),
    ("himchistka-divana-dobrograd.html", "sofa", "Доброград", "Химчистка диванов в Доброграде и Ковровском районе", "Химчистка диванов в Доброграде на дому", "Химчистка диванов в Доброграде на дому. Выезд из Коврова. Удаляем пятна и запахи. Оплата после результата."),
    ("himchistka-matrasa-vladimir.html", "mattress", "Владимир", "Химчистка матрасов во Владимире", "Химчистка матрасов во Владимире на дому — цены", "Химчистка матрасов на дому во Владимире. Удаляем пятна, запахи и аллергены. Безопасно для детей. От 1 500 ₽."),
    ("himchistka-matrasa-kovrov.html", "mattress", "Ковров", "Химчистка матрасов в Коврове и Ковровском районе", "Химчистка матрасов в Коврове — цены с выездом", "Химчистка матрасов в Коврове на дому. Выезд бесплатно. От 1 500 ₽ за сторону. Оплата после результата."),
    ("himchistka-matrasa-dobrograd.html", "mattress", "Доброград", "Химчистка матрасов в Доброграде", "Химчистка матрасов в Доброграде на дому", "Химчистка матрасов в Доброграде на дому. Выезд из Коврова. Удаляем пятна и запахи. От 1 500 ₽."),
    ("himchistka-kovrov-vladimir.html", "carpet", "Владимир", "Химчистка ковров во Владимире", "Химчистка ковров во Владимире на дому — цены", "Химчистка ковров на дому во Владимире без вывоза. От 350 ₽/м². Выезд, оплата после результата."),
    ("himchistka-kovrov-kovrov.html", "carpet", "Ковров", "Химчистка ковров в Коврове и Ковровском районе", "Химчистка ковров в Коврове — цены за м²", "Химчистка ковров в Коврове на дому без вывоза. Выезд бесплатно. От 350 ₽/м². Оплата после результата."),
    ("himchistka-kovrov-dobrograd.html", "carpet", "Доброград", "Химчистка ковров в Доброграде", "Химчистка ковров в Доброграде на дому", "Химчистка ковров в Доброграде на дому без вывоза. Выезд из Коврова. От 350 ₽/м²."),
    ("himchistka-kresel-i-stulev-vladimir.html", "chair", "Владимир", "Химчистка кресел и стульев во Владимире", "Химчистка кресел и стульев во Владимире", "Химчистка кресел и стульев на дому и в офисе во Владимире. От 300 ₽. Выезд, оплата после результата."),
    ("himchistka-kresel-i-stulev-kovrov.html", "chair", "Ковров", "Химчистка кресел и стульев в Коврове и Ковровском районе", "Химчистка кресел и стульев в Коврове — цены", "Химчистка кресел и стульев в Коврове. Выезд бесплатно. От 300 ₽. Оплата после результата."),
    ("himchistka-kresel-i-stulev-dobrograd.html", "chair", "Доброград", "Химчистка кресел и стульев в Доброграде", "Химчистка кресел и стульев в Доброграде", "Химчистка кресел и стульев в Доброграде на дому. Выезд из Коврова. От 300 ₽."),
]

SERVICE_META = {
    "sofa": {
        "hub": "/himchistka-divanov.html",
        "hub_label": "Химчистка диванов",
        "faq": SOFA_FAQ,
        "price": "от 3&nbsp;500&nbsp;₽",
        "noun": "диванов",
        "what": "диван",
        "comment": "Например: угловой диван",
    },
    "mattress": {
        "hub": "/himchistka-matrasov.html",
        "hub_label": "Химчистка матрасов",
        "faq": MATTRESS_FAQ,
        "price": "от 1&nbsp;500&nbsp;₽",
        "noun": "матрасов",
        "what": "матрас",
        "comment": "Например: матрас 160×200",
    },
    "carpet": {
        "hub": "/himchistka-kovrov.html",
        "hub_label": "Химчистка ковров",
        "faq": CARPET_FAQ,
        "price": "от 350&nbsp;₽/м²",
        "noun": "ковров",
        "what": "ковёр",
        "comment": "Например: ковёр 2×3 м",
    },
    "chair": {
        "hub": "/himchistka-kresel-i-stulev.html",
        "hub_label": "Кресла и стулья",
        "faq": CHAIR_FAQ,
        "price": "от 300&nbsp;₽",
        "noun": "кресел и стульев",
        "what": "кресла/стулья",
        "comment": "Например: 4 стула + кресло",
    },
}


def write_service_page(slug: str, data: dict) -> None:
    cards_html = render_cards(data["cards"])
    city_links = related_block(
        data["city_links"],
        eyebrow="Города",
        title="Химчистка по городам",
        section_id="cities",
        alt=True,
    )
    related = related_block(
        data["related"],
        eyebrow="Ещё услуги",
        title="Смотрите также",
        section_id="related",
        alt=False,
    )
    faq = render_faq(data["faq"])
    seo = "\n".join(f"<p>{esc(p)}</p>" for p in data["seo_paras"])
    form = FORM_SECTION.format(comment_placeholder=esc(data["comment"]))
    breadcrumb_nav, breadcrumb_ld = render_breadcrumbs(
        [("/", "Главная"), ("", data.get("service_type", data["h1"]))]
    )

    body = f"""
<main>
  <section class="page-hero">
    <div class="container">
      {breadcrumb_nav}
      <span class="section-eyebrow">Услуга</span>
      <h1 class="section-title" style="margin-top:10px;">{esc(data["h1"])}</h1>
      <p class="section-sub" style="max-width:640px;">{esc(data["subtitle"])}</p>
      <div class="hero-cta" style="margin-top:20px;">
        <a class="btn btn-primary" href="#form-block">Заказать · {data["price_from"]}</a>
        <a class="btn btn-outline" href="tel:+79157548115">Позвонить</a>
      </div>
    </div>
  </section>

  <section class="section-alt" id="price">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Цены</span>
        <h2 class="section-title">Виды и стоимость</h2>
        <p class="section-sub">Точную цену фиксируем по фото до выезда.</p>
      </div>
      {cards_html}
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Процесс</span>
        <h2 class="section-title">Как мы работаем</h2>
      </div>
      <div class="steps-grid">
        <div class="step"><div class="step-num">01</div><div class="step-title">Заявка и фото</div><div class="step-text">Оцениваем стоимость и время по фото.</div></div>
        <div class="step"><div class="step-num">02</div><div class="step-title">Выезд</div><div class="step-text">Приезжаем вовремя, подтверждаем цену.</div></div>
        <div class="step"><div class="step-num">03</div><div class="step-title">Чистка</div><div class="step-text">Химия под ткань + экстракция.</div></div>
        <div class="step"><div class="step-num">04</div><div class="step-title">Оплата</div><div class="step-text">Платите после результата.</div></div>
      </div>
    </div>
  </section>

  {form}

  <section id="seo-text">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Подробнее об услуге</h2>
      </div>
      <div class="seo-text" style="max-width:820px;">{seo}</div>
    </div>
  </section>

  <section class="section-alt" id="faq">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">FAQ</span>
        <h2 class="section-title">Частые вопросы</h2>
      </div>
      {faq}
    </div>
  </section>

  {city_links}
  {related}
  {CONTACTS}
</main>
"""
    page = (
        HEAD_COMMON.format(
            title=esc(data["title"]),
            description=esc(data["description"]),
            slug=slug,
            og_title=esc(data["h1"]),
            geo_place="Владимир, Ковров, Доброград",
            head_assets=HEAD_ASSETS,
        )
        + HEADER
        + body
        + render_business_jsonld(
            data["service_name"],
            page_url=f"https://himchistkadoma.ru/{slug}",
            service_type=data.get("service_type"),
            price=data.get("offer_price"),
        )
        + "\n"
        + render_faq_jsonld(data["faq"])
        + "\n"
        + breadcrumb_ld
        + "\n"
        + FOOTER
    )
    (ROOT / slug).write_text(page, encoding="utf-8")
    print("wrote", slug, (ROOT / slug).stat().st_size)


def write_city_page(filename: str, key: str, city: str, h1: str, title: str, description: str) -> None:
    meta = SERVICE_META[key]
    faq_raw = []
    for item in meta["faq"]:
        q = item["q"]
        if "Коврове" in q or "коврове" in q.lower():
            q = q.replace("в Коврове", f"в {city[:-1] + 'е' if city.endswith('в') else 'в ' + city}")
            # simpler: append city mention for cost questions
        if q.startswith("Сколько стоит") and city not in q:
            q = q.rstrip("?") + f" в {city}?"
        if "Выезд" in q:
            a = (
                "Выезд по Коврову бесплатный. По району и в другие города — по договорённости."
                if city == "Ковров"
                else f"Выезд в {city} — по договорённости. Точную стоимость выезда уточним при заявке."
            )
            faq_raw.append({"q": q, "a": a})
        else:
            faq_raw.append({"q": q, "a": item["a"]})

    faq = render_faq(faq_raw)
    form = FORM_SECTION.format(comment_placeholder=esc(f"{meta['comment']}, {city}"))
    related = related_block(
        [
            (meta["hub"], meta["hub_label"], "Все цены и виды"),
            ("/", "На главную", "Все услуги"),
            ("/#rent", "Аренда оборудования", "Экстрактор и пар"),
        ]
    )
    seo = f"""
      <p>Профессиональная химчистка {esc(meta['noun'])} на дому в городе {esc(city)}. Приезжаем с оборудованием, подбираем химию под материал и степень загрязнения, выполняем глубокую очистку и экстракцию.</p>
      <p>Цена — {meta['price']}. Точную стоимость называем до начала работ по фото или на месте. Оплата только после результата.</p>
      <p>Работаем ежедневно с 9:00 до 21:00. Безопасно для детей и животных. Зона обслуживания: {esc(city)} и ближайшие населённые пункты Владимирской области.</p>
    """
    offer_map = {
        "sofa": ("3500", "Химчистка диванов"),
        "mattress": ("1500", "Химчистка матрасов"),
        "carpet": ("350", "Химчистка ковров"),
        "chair": ("300", "Химчистка кресел и стульев"),
    }
    offer_price, service_type = offer_map[key]
    breadcrumb_nav, breadcrumb_ld = render_breadcrumbs(
        [
            ("/", "Главная"),
            (meta["hub"], meta["hub_label"]),
            ("", h1),
        ]
    )
    body = f"""
<main>
  <section class="page-hero">
    <div class="container">
      {breadcrumb_nav}
      <span class="section-eyebrow">{esc(city)}</span>
      <h1 class="section-title" style="margin-top:10px;">{esc(h1)}</h1>
      <p class="section-sub" style="max-width:640px;">Выездная химчистка {esc(meta['noun'])} на дому в {esc(city)}. Удаляем пятна и запахи. Цена по фото — фиксированная.</p>
      <div class="hero-cta" style="margin-top:20px;">
        <a class="btn btn-primary" href="#form-block">Заказать · {meta['price']}</a>
        <a class="btn btn-outline" href="tel:+79157548115">Позвонить</a>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-header">
        <span class="section-eyebrow">Преимущества</span>
        <h2 class="section-title">Почему заказывают у нас</h2>
      </div>
      <div class="benefits-grid">
        <div class="benefit"><div class="benefit-num">01</div><div><div class="benefit-title">Выезд на дом</div><div class="benefit-text">Чистим у вас — без перевозки мебели.</div></div></div>
        <div class="benefit"><div class="benefit-num">02</div><div><div class="benefit-title">Цена до работы</div><div class="benefit-text">Фиксируем стоимость по фото.</div></div></div>
        <div class="benefit"><div class="benefit-num">03</div><div><div class="benefit-title">Безопасная химия</div><div class="benefit-text">Подходит для семей с детьми и животными.</div></div></div>
        <div class="benefit"><div class="benefit-num">04</div><div><div class="benefit-title">Оплата после результата</div><div class="benefit-text">Если результата нет — не берём оплату.</div></div></div>
      </div>
    </div>
  </section>

  {form}

  <section id="seo-text">
    <div class="container">
      <div class="section-header"><h2 class="section-title">Химчистка {esc(meta['noun'])} в {esc(city)}</h2></div>
      <div class="seo-text" style="max-width:820px;">{seo}</div>
    </div>
  </section>

  <section class="section-alt" id="faq">
    <div class="container">
      <div class="section-header"><span class="section-eyebrow">FAQ</span><h2 class="section-title">Частые вопросы</h2></div>
      {faq}
    </div>
  </section>

  {related}
  {CONTACTS}
</main>
"""
    page = (
        HEAD_COMMON.format(
            title=esc(title),
            description=esc(description),
            slug=filename,
            og_title=esc(h1),
            geo_place=city,
            head_assets=HEAD_ASSETS,
        )
        + HEADER
        + body
        + render_business_jsonld(
            f"Химчистка {meta['noun']} в {city} — HimchistkaDoma",
            city,
            page_url=f"https://himchistkadoma.ru/{filename}",
            service_type=f"{service_type} в {city}",
            price=offer_price,
        )
        + "\n"
        + render_faq_jsonld(faq_raw)
        + "\n"
        + breadcrumb_ld
        + "\n"
        + FOOTER
    )
    (ROOT / filename).write_text(page, encoding="utf-8")
    print("wrote", filename, (ROOT / filename).stat().st_size)


RENTALS = {
    "arenda-ekstraktora-dlya-mebeli-i-kovrov.html": {
        "title": "Аренда экстрактора в Коврове — моющий пылесос",
        "description": "Аренда экстрактора для химчистки мебели и ковров в Коврове. Насадки в комплекте, инструктаж при выдаче. Тел.: +7 915 754-81-15.",
        "h1": "Аренда экстрактора (моющего пылесоса) в Коврове",
        "service_type": "Аренда экстрактора",
        "offer_price": "1000",
        "subtitle": "Подойдёт для диванов, кресел, ковров и ковролина. В комплекте — шланги и насадки, при выдаче проводим короткий инструктаж.",        "cards": [
            {"icon": "🔧", "tag": "Для чего", "title": "Диваны и кресла", "text": "Ткань и велюр. Базовый алгоритм чистки покажем при выдаче.", "price": "аренда", "unit": "от 1 дня"},
            {"icon": "🔧", "title": "Ковры и ковролин", "text": "Мощная экстракция грязи и раствора.", "price": "аренда", "unit": "от 1 дня"},
            {"icon": "🔧", "title": "Матрасы", "text": "Аккуратно, без переувлажнения. Подскажем режим.", "price": "аренда", "unit": "от 1 дня"},
            {"icon": "📦", "title": "Комплект", "text": "Экстрактор, шланги, насадки и рекомендации по химии.", "price": "входит", "unit": "в аренду"},
        ],
        "faq": [
            {"q": "Сколько стоит аренда экстрактора в Коврове?", "a": "Стоимость зависит от срока аренды и комплектации. Уточним цену по телефону и подтвердим наличие."},
            {"q": "Что входит в комплект?", "a": "Экстрактор, шланги, насадки и базовые рекомендации по химии и режиму работы."},
            {"q": "Можно ли почистить диван самостоятельно?", "a": "Да. Покажем базовый алгоритм: предварительная обработка, промывка и экстракция. Важно не заливать ткань водой."},
            {"q": "Нужна ли химия?", "a": "Для лучшего результата обычно нужна подходящая химия. Подскажем, что выбрать."},
            {"q": "Нужен ли залог?", "a": "Залог не берём. Клиент отвечает за сохранность техники."},
            {"q": "Что делать, если не получается?", "a": "Подскажем по телефону или в мессенджере."},
        ],
        "seo": [
            "Аренда моющего пылесоса (экстрактора) в Коврове помогает сделать уборку самостоятельно, без ожидания мастера. Выдаём оборудование, проводим короткий инструктаж и подсказываем, как получить хороший результат.",
            "Если нужен гарантированный результат — закажите профессиональную химчистку мебели и ковров под ключ.",
        ],
        "comment": "Аренда экстрактора, даты",
    },
    "arenda-paroochistitelya.html": {
        "title": "Аренда пароочистителя в Коврове — на сутки",
        "description": "Аренда пароочистителя в Коврове для уборки дома: плитка, швы, сантехника, кухня. Насадки в комплекте, инструктаж. Тел.: +7 915 754-81-15.",
        "h1": "Аренда пароочистителя в Коврове",
        "service_type": "Аренда пароочистителя",
        "offer_price": "800",
        "subtitle": "Для сложных пятен, стыков и труднодоступных мест. Можно использовать вместе с экстрактором или отдельно.",
        "cards": [
            {"icon": "♨️", "tag": "Кухня", "title": "Плитка и фартук", "text": "Пар помогает убрать жир и налёт.", "price": "аренда", "unit": "от 1 дня"},
            {"icon": "♨️", "title": "Ванная", "text": "Кафель, душевая, смесители, швы.", "price": "аренда", "unit": "от 1 дня"},
            {"icon": "♨️", "title": "Швы и уголки", "text": "Насадка для швов — для трудных мест.", "price": "аренда", "unit": "от 1 дня"},
            {"icon": "📦", "title": "Комплект", "text": "Пароочиститель и набор насадок + инструктаж.", "price": "входит", "unit": "в аренду"},
        ],
        "faq": [
            {"q": "Сколько стоит аренда пароочистителя в Коврове?", "a": "Цена зависит от срока аренды. Напишите или позвоните — скажем стоимость и свободные даты."},
            {"q": "Что входит в комплект?", "a": "Пароочиститель и набор насадок. При выдаче — короткий инструктаж."},
            {"q": "Можно ли чистить паром духовку и вытяжку?", "a": "Да, но аккуратно: не направляйте пар на электронику. Покажем, как безопаснее."},
            {"q": "Подойдёт ли для швов и уголков?", "a": "Да, как раз для этого чаще всего и берут."},
            {"q": "Нужно ли добавлять химию?", "a": "Обычно достаточно воды и пара. При сильных загрязнениях подскажем средства."},
            {"q": "Это безопасно?", "a": "Пар очень горячий. Работайте в перчатках и не направляйте на кожу."},
        ],
        "seo": [
            "Аренда пароочистителя в Коврове удобна для генеральной уборки кухни и ванной: плитка, швы, сантехника и труднодоступные места.",
            "Выдаём оборудование в Коврове, проводим инструктаж. Если нужен результат «под ключ» — закажите профессиональную химчистку.",
        ],
        "comment": "Аренда пароочистителя, даты",
    },
}


def write_rental(slug: str, data: dict) -> None:
    cards = render_cards(data["cards"])
    faq = render_faq(data["faq"])
    form = FORM_SECTION.format(comment_placeholder=esc(data["comment"]))
    seo = "\n".join(f"<p>{esc(p)}</p>" for p in data["seo"])
    related = related_block(
        [
            ("/arenda-ekstraktora-dlya-mebeli-i-kovrov.html", "Аренда экстрактора", "Мебель и ковры"),
            ("/arenda-paroochistitelya.html", "Аренда пароочистителя", "Кухня и ванная"),
            ("/", "Химчистка под ключ", "Если нужен результат"),
        ]
    )
    breadcrumb_nav, breadcrumb_ld = render_breadcrumbs(
        [("/", "Главная"), ("", data["h1"])]
    )
    body = f"""
<main>
  <section class="page-hero">
    <div class="container">
      {breadcrumb_nav}
      <span class="section-eyebrow">Аренда</span>
      <h1 class="section-title" style="margin-top:10px;">{esc(data["h1"])}</h1>
      <p class="section-sub" style="max-width:640px;">{esc(data["subtitle"])}</p>
      <div class="hero-cta" style="margin-top:20px;">
        <a class="btn btn-primary" href="#form-block">Оставить заявку</a>
        <a class="btn btn-outline" href="tel:+79157548115">Позвонить</a>
      </div>
    </div>
  </section>
  <section class="section-alt" id="price">
    <div class="container">
      <div class="section-header"><span class="section-eyebrow">Возможности</span><h2 class="section-title">Для каких задач</h2></div>
      {cards}
    </div>
  </section>
  {form}
  <section id="seo-text">
    <div class="container">
      <div class="section-header"><h2 class="section-title">Подробнее</h2></div>
      <div class="seo-text" style="max-width:820px;">{seo}</div>
    </div>
  </section>
  <section class="section-alt" id="faq">
    <div class="container">
      <div class="section-header"><span class="section-eyebrow">FAQ</span><h2 class="section-title">Частые вопросы</h2></div>
      {faq}
    </div>
  </section>
  {related}
  {CONTACTS}
</main>
"""
    page = (
        HEAD_COMMON.format(
            title=esc(data["title"]),
            description=esc(data["description"]),
            slug=slug,
            og_title=esc(data["h1"]),
            geo_place="Ковров",
            head_assets=HEAD_ASSETS,
        )
        + HEADER
        + body
        + render_business_jsonld(
            data["h1"] + " — HimchistkaDoma",
            "Ковров",
            page_url=f"https://himchistkadoma.ru/{slug}",
            service_type=data.get("service_type", data["h1"]),
            price=data.get("offer_price"),
        )
        + "\n"
        + render_faq_jsonld(data["faq"])
        + "\n"
        + breadcrumb_ld
        + "\n"
        + FOOTER
    )
    (ROOT / slug).write_text(page, encoding="utf-8")
    print("wrote", slug, (ROOT / slug).stat().st_size)


def main() -> None:
    for slug, data in SERVICES.items():
        write_service_page(slug, data)
    for item in CITY_PAGES:
        write_city_page(*item)
    for slug, data in RENTALS.items():
        write_rental(slug, data)
    print("ALL DONE")


if __name__ == "__main__":
    main()
