# -*- coding: utf-8 -*-
"""Buduje poradnik, strony usług, kanał RSS i mapę strony.

Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_poradnik.py
Treść: poradnik_tresc.py (artykuły) i uslugi_tresc.py (strony usług: Sieradz, karty NFC, social media).
Szablonem (nagłówek, menu, kurtyna, stopka) jest polityka-prywatnosci.html.
Karty z cenami na stronach usług kopiuję przy budowaniu z cennik.html — ceny zmieniasz tylko w cenniku.
Na końcu powstają: feed.xml (kanał RSS poradnika) i sitemap.xml (wszystkie strony bez „noindex”;
data zmiany = data ostatniego commita pliku albo dzisiejsza, jeśli plik jest zmieniony).
Folder _zrodla nie jest publikowany przez GitHub Pages (Jekyll pomija foldery z „_”).
"""
import datetime
import email.utils
import glob
import html
import json
import os
import re
import subprocess
import sys

import markdown

sys.path.insert(0, os.path.dirname(__file__))
from poradnik_tresc import ARTYKULY, PORADNIK, DATA, NA_STARCIE, NA_USLUGACH  # noqa: E402
from uslugi_tresc import USLUGI  # noqa: E402

B = 'https://marcelgraphicsite.pl/'
TODAY = datetime.date.today().isoformat()
MIESIACE = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']
ORG = {'@type': 'ProfessionalService', '@id': B + '#firma', 'name': 'Marcel GraphicSite',
       'alternateName': ['Marcel Struszczak — strony internetowe', 'marcelgraphicsite.pl', 'marcel.graphicsite'], 'url': B,
       'logo': B + 'assets/img/apple-touch-icon.png', 'image': B + 'assets/img/og.jpg',
       'telephone': '+48 511 808 498', 'email': 'marcel.graphicsite@gmail.com', 'priceRange': '60–3000+ zł',
       'address': {'@type': 'PostalAddress', 'addressLocality': 'Sieradz', 'postalCode': '98-200', 'addressRegion': 'łódzkie', 'addressCountry': 'PL'}}
PER = {'@type': 'Person', '@id': B + '#marcel', 'name': 'Marcel Struszczak', 'url': B + 'o-mnie',
       'jobTitle': 'Projektant stron internetowych', 'homeLocation': {'@type': 'City', 'name': 'Sieradz'},
       'brand': {'@type': 'Brand', 'name': 'Marcel GraphicSite', 'url': B}}
BY_SLUG = {a['slug']: a for a in ARTYKULY}
PL_MAP = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')
BLOK = re.compile(r'^\[\[blok:(\w+)\]\]\s*$', re.M)


def esc(s):
    return html.escape(s, quote=True)


def slugify(s):
    s = re.sub(r'<[^>]+>', '', s).translate(PL_MAP).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:60].rstrip('-')


def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def pl_date(iso):
    d = datetime.date.fromisoformat(iso)
    return '%d %s %d' % (d.day, MIESIACE[d.month - 1], d.year)


def pub(a):
    return a.get('data', DATA)


def mod(a):
    return a.get('zmiana', pub(a))


def md_to_html(md, seen, toc):
    out = markdown.markdown(md, extensions=['tables', 'sane_lists'])
    out = out.replace('<table>', '<div class="tbl"><table>').replace('</table>', '</table></div>')

    def label_cells(m):
        # na telefonie tabela zamienia się w karty: każda komórka dostaje podpis z nagłówka kolumny
        tbl = m.group(0)
        heads = [strip_tags(h) for h in re.findall(r'<th[^>]*>(.*?)</th>', tbl, re.S)]

        def row(rm):
            cells = iter(heads)
            return re.sub(r'<td([^>]*)>', lambda cm: '<td%s data-label="%s">' % (cm.group(1), esc(next(cells, ''))), rm.group(0))
        return re.sub(r'<tr>.*?</tr>', row, tbl, flags=re.S)
    out = re.sub(r'<table>.*?</table>', label_cells, out, flags=re.S)

    def add_id(m):
        level, inner = m.group(1), m.group(2)
        sid = slugify(inner)
        while sid in seen:
            sid += '-2'
        seen.add(sid)
        if level == '2':
            toc.append((sid, strip_tags(inner)))
        return '<h%s id="%s">%s</h%s>' % (level, sid, inner, level)
    return re.sub(r'<h([23])>(.*?)</h\1>', add_id, out)


def render_body(md):
    """Dzieli treść na fragmenty Markdown i bloki [[blok:nazwa]]. Zwraca (lista segmentów, spis treści)."""
    seen, toc, segs, pos = {'pytania'}, [], [], 0
    for m in BLOK.finditer(md):
        segs.append(('html', md_to_html(md[pos:m.start()], seen, toc)))
        segs.append(('blok', m.group(1)))
        pos = m.end()
    segs.append(('html', md_to_html(md[pos:], seen, toc)))
    return segs, toc


def minutes(*parts):
    words = len(strip_tags(' '.join(parts)).split())
    return max(3, round(words / 200))


def card(slug, mins, heading='h3'):
    a = BY_SLUG[slug]
    return ('<a class="guide reveal" href="%s" data-cursor><span class="tag">%s</span><%s class="guide__t">%s</%s>'
            '<p class="guide__p">%s</p><span class="guide__m"><span>%d min czytania</span><i aria-hidden="true">→</i></span></a>'
            % (slug, esc(a['og_kicker']), heading, a['headline'], heading, a['excerpt'], mins))


CTA = '''<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-card reveal" data-dark>
      <div>
        <p class="tag"><span data-i18n="work.ctaEyebrow">Twoja firma</span></p>
        <p class="pc__big" style="margin-top:22px" data-i18n="work.ctaBig">Tu może być <em>Twoja strona.</em></p>
        <p class="pc__txt" data-i18n="work.ctaText">Pokażę Ci ją za darmo — zanim wydasz złotówkę. Wystarczy nazwa firmy i link do Facebooka.</p>
      </div>
      <div class="cta"><a href="kontakt" class="btn btn--paper mag" data-cursor><span data-i18n="hero.b1">Zamów darmowy projekt</span><span class="nudge" aria-hidden="true">→</span></a></div>
    </div>
  </div>
</section>'''

AUTHOR = ('<aside class="author"><span class="author__mark" aria-hidden="true">MS</span><div><p><b>Marcel Struszczak</b> · Marcel GraphicSite</p>'
          '<p>Projektant stron internetowych z Sieradza. Projektuję strony, prowadzę social media i wdrażam karty NFC do opinii Google '
          'dla firm z całej Polski. <a href="o-mnie">Więcej o mnie</a> · <a href="poradnik">Wszystkie poradniki</a></p></div></aside>')


def phead(h1, lead, side_html):
    return '''<section class="phead">
  <span class="phead__num" aria-hidden="true">06</span>
  <div class="wrap">
    <div class="phead__top">
      <p class="tag reveal">(06) <span data-i18n="guide.tag">Poradnik</span></p>
      <p class="crumb reveal"><a href="./" data-i18n="nav.home2">Start</a> / <a href="poradnik" data-i18n="guide.tag">Poradnik</a></p>
    </div>
    <h1 class="display phead__h phead__h--q" data-split>%s</h1>
    <div class="phead__bottom">
      <p class="lead reveal" style="--d:.12s">%s</p>
      <div class="phead__side reveal" style="--d:.2s">%s</div>
    </div>
  </div>
</section>''' % (h1, lead, side_html)


def phead_svc(h1, lead, side_html, crumb):
    return '''<section class="phead">
  <span class="phead__num" aria-hidden="true">02</span>
  <div class="wrap">
    <div class="phead__top">
      <p class="tag reveal">(02) <span data-i18n="nav.services">Usługi</span></p>
      <p class="crumb reveal"><a href="./" data-i18n="nav.home2">Start</a> / <a href="uslugi" data-i18n="nav.services">Usługi</a> / <span>%s</span></p>
    </div>
    <h1 class="display phead__h" data-split>%s</h1>
    <div class="phead__bottom">
      <p class="lead reveal" style="--d:.12s">%s</p>
      <div class="phead__side reveal" style="--d:.2s">%s</div>
    </div>
  </div>
</section>''' % (esc(crumb), h1, lead, side_html)


def faq_html(faq):
    qa = ''.join(
        '<div class="qa"><h3><button type="button" aria-expanded="false" aria-controls="gq%d" id="gqb%d"><span>%s</span><i aria-hidden="true">+</i></button></h3>'
        '<div class="qa__a" id="gq%d" role="region" aria-labelledby="gqb%d"><div><p>%s</p></div></div></div>' % (i, i, esc(q), i, i, esc(ans))
        for i, (q, ans) in enumerate(faq, 1))
    return '<section class="faq-mini" aria-labelledby="pytania"><h2 id="pytania">Najczęstsze pytania</h2>%s</section>' % qa


def related_html(slugs, mins_by, label='Czytaj też'):
    return '''<section class="sec rule">
  <div class="wrap">
    <p class="tag reveal" style="margin-bottom:22px">%s</p>
    <div class="guides">%s</div>
  </div>
</section>''' % (label, ''.join(card(r, mins_by[r]) for r in slugs))


def set_current(s, slug):
    """aria-current="page" w stopce tylko przy linku do bieżącej strony."""
    i = s.find('<div class="foot__cols">')
    j = s.find('<div class="foot__bottom">', i)
    if i < 0 or j < 0:
        return s
    part = s[i:j].replace(' aria-current="page"', '')
    part = re.sub(r'<a href="%s"' % re.escape(slug), '<a href="%s" aria-current="page"' % slug, part)
    return s[:i] + part + s[j:]


def build_page(shell, page, main_html, ld, og_type='website', article_meta='', num='06'):
    s = shell
    slug, url = page['slug'], B + page['slug']
    og_img = B + 'assets/img/og/%s.jpg' % slug
    s = re.sub(r'<html lang="pl" data-page="[^"]*" data-bg="[^"]*">',
               '<html lang="pl" data-page="%s" data-bg="%s">' % (slug, page['bg']), s, count=1)
    reps = [
        (r'<title>[^<]*</title>', '<title>%s</title>' % esc(page['title'])),
        (r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % esc(page['description'])),
        (r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'),
        (r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url),
        (r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="%s">' % og_type),
        (r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url),
        (r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % esc(page['og_title'])),
        (r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % esc(page['description'])),
        (r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%s">' % og_img),
        (r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="%s">' % esc(page['og_title'])),
        (r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="%s">' % esc(page['og_title'])),
        (r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="%s">' % esc(page['description'])),
        (r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="%s">' % og_img),
    ]
    for pat, rep in reps:
        s, n = re.subn(pat, lambda m, r=rep: r, s, count=1)
        assert n == 1, pat
    if article_meta:
        s = s.replace('<meta property="og:image:height" content="630">', '<meta property="og:image:height" content="630">\n' + article_meta, 1)
    ld_json = json.dumps({'@context': 'https://schema.org', '@graph': ld}, ensure_ascii=False, separators=(',', ':'))
    s, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">%s</script>' % ld_json, s, count=1, flags=re.S)
    assert n == 1
    t_pl, s_pl, t_en, s_en = page['curtain']
    cur = ('<p class="curtain__n">(%s)</p><p class="curtain__t%s" data-en="%s">%s</p><p class="curtain__s" data-en="%s">%s</p>'
           % (num, ' is-long' if len(t_pl) > 9 else '', esc(t_en), esc(t_pl), esc(s_en), esc(s_pl)))
    s, n = re.subn(r'<p class="curtain__n">[^<]*</p><p class="curtain__t[^"]*" data-en="[^"]*">[^<]*</p><p class="curtain__s" data-en="[^"]*">[^<]*</p>', lambda m: cur, s, count=1)
    assert n == 1
    s, n = re.subn(r'<main id="main">.*?</main>', lambda m: '<main id="main">\n\n' + main_html + '\n\n</main>', s, count=1, flags=re.S)
    assert n == 1
    return set_current(s, slug)


def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


# ---------- bloki z cennika (karty z cenami) ----------
def balanced_div(s, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        depth += -1 if m.group(0) == '</div>' else 1
        if depth == 0:
            return s[start:start + m.end()]
    raise ValueError('niezamknięty <div>')


def pricing_blocks():
    s = open('cennik.html', encoding='utf-8').read()

    def panel(pid):
        div = balanced_div(s, s.index('<div class="tp" id="%s"' % pid))
        return div[div.index('>') + 1:div.rindex('</div>')]

    def clean(h):
        h = re.sub(r'\s*<p class="tp-more">.*?</p>', '', h, flags=re.S)
        h = re.sub(r'<h3 class="tintro__h"([^>]*)>(.*?)</h3>', r'<h2 class="tintro__h"\1>\2</h2>', h, flags=re.S)
        return h.strip()
    www = panel('tp-www')
    plans = balanced_div(www, www.index('<div class="plans">'))
    notes = balanced_div(www, www.index('<div class="foot-notes">'))
    return {'www': plans + '\n' + notes, 'nfc': clean(panel('tp-nfc')), 'social': clean(panel('tp-social'))}


def svc_block(inner):
    return '<section class="sec svc-block" style="padding-top:8px">\n  <div class="wrap">\n%s\n  </div>\n</section>' % inner


PROSE_OPEN = '<section class="sec" style="padding-top:8px">\n  <div class="wrap">\n    <div class="prose">\n'
PROSE_CLOSE = '\n    </div>\n  </div>\n</section>'


def update_cards(fname, slugs, mins_by):
    s = open(fname, encoding='utf-8').read()
    cards = ''.join(card(sl, mins_by[sl]) for sl in slugs)
    s2, n = re.subn(r'<!-- poradnik:start -->.*?<!-- poradnik:end -->', lambda m: '<!-- poradnik:start -->' + cards + '<!-- poradnik:end -->', s, count=1, flags=re.S)
    if n and s2 != s:
        open(fname, 'w', encoding='utf-8').write(s2)
        print('zaktualizowano karty poradnika na', fname)


# ---------- kanał RSS i mapa strony ----------
def rss_date(iso):
    d = datetime.datetime.fromisoformat(iso + 'T09:00:00+02:00')
    return email.utils.format_datetime(d)


def build_feed():
    items = sorted(ARTYKULY, key=lambda a: (mod(a), pub(a)), reverse=True)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', '<channel>',
           '  <title>Poradnik dla firm — Marcel GraphicSite</title>',
           '  <link>%sporadnik</link>' % B,
           '  <description>%s</description>' % esc(PORADNIK['description']),
           '  <language>pl</language>',
           '  <lastBuildDate>%s</lastBuildDate>' % rss_date(max(mod(a) for a in ARTYKULY)),
           '  <atom:link href="%sfeed.xml" rel="self" type="application/rss+xml"/>' % B]
    for a in items:
        out += ['  <item>',
                '    <title>%s</title>' % esc(a['headline']),
                '    <link>%s%s</link>' % (B, a['slug']),
                '    <guid isPermaLink="true">%s%s</guid>' % (B, a['slug']),
                '    <pubDate>%s</pubDate>' % rss_date(pub(a)),
                '    <description>%s</description>' % esc(a['description']),
                '    <category>%s</category>' % esc(a['og_kicker'].split('·')[-1].strip()),
                '  </item>']
    out += ['</channel>', '</rss>', '']
    open('feed.xml', 'w', encoding='utf-8').write('\n'.join(out))
    print('zbudowano feed.xml —', len(items), 'artykułów')


PRIORITY = {'': '1.0', 'cennik': '0.9', 'kontakt': '0.9', 'strony-internetowe-sieradz': '0.9', 'uslugi': '0.8', 'prace': '0.8',
            'karty-nfc-opinie-google': '0.8', 'prowadzenie-social-media': '0.8', 'ile-kosztuje-strona-internetowa': '0.8',
            'poradnik': '0.7', 'o-mnie': '0.6', 'polityka-prywatnosci': '0.3'}


def git_lastmod(f):
    try:
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', f], capture_output=True, text=True).stdout.strip()
        if dirty:
            return TODAY
        d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', f], capture_output=True, text=True).stdout.strip()
        return d or TODAY
    except OSError:
        return TODAY


def build_sitemap():
    rows = []
    for f in sorted(glob.glob('*.html')):
        s = open(f, encoding='utf-8').read()
        if re.search(r'<meta name="robots" content="[^"]*noindex', s):
            continue
        can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not can or not can.group(1).startswith(B):
            continue
        url = can.group(1)
        path = url[len(B):]
        imgs = re.findall(r'<meta property="og:image" content="([^"]+)"', s)
        if path == 'prace':
            imgs = [B + 'assets/img/%s-1200.webp' % p for p in ('luxe', 'vesper', 'zar')]
        rows.append((0 if path == '' else 1, path, url, git_lastmod(f), imgs))
    rows.sort(key=lambda r: (r[0], -float(PRIORITY.get(r[1], '0.7')), r[1]))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for _, path, url, lastmod, imgs in rows:
        img = ''.join('<image:image><image:loc>%s</image:loc></image:image>' % i for i in imgs)
        out.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority>%s</url>' % (url, lastmod, PRIORITY.get(path, '0.7'), img))
    out += ['</urlset>', '']
    open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(out))
    print('zbudowano sitemap.xml —', len(rows), 'adresów')


# ---------- budowanie ----------
def main():
    root = os.path.join(os.path.dirname(__file__), '..')
    os.chdir(root)
    shell = open('polityka-prywatnosci.html', encoding='utf-8').read()
    blocks = pricing_blocks()

    mins_by, built = {}, {}
    for a in ARTYKULY:
        segs, toc = render_body(a['body'])
        body = ''.join(h for kind, h in segs if kind == 'html')
        faq_txt = ' '.join(q + ' ' + ans for q, ans in a['faq'])
        mins_by[a['slug']] = minutes(a['lead'], ' '.join(a['tldr']), body, faq_txt)
        built[a['slug']] = (body, toc)

    # artykuły
    for a in ARTYKULY:
        slug, url = a['slug'], B + a['slug']
        body, toc = built[slug]
        mins = mins_by[slug]
        toc_html = ''.join('<li><a href="#%s">%s</a></li>' % (sid, esc(t)) for sid, t in toc) + '<li><a href="#pytania">Najczęstsze pytania</a></li>'
        side = '<p>Marcel Struszczak</p><p><time datetime="%s">%s</time></p><p>%d min czytania</p>' % (mod(a), pl_date(mod(a)), mins)
        main_html = phead(a['h1'], a['lead'], side) + '''

<section class="sec" style="padding-top:8px">
  <div class="wrap">
    <article class="prose">
      <p class="prose__en" data-i18n="guide.en"></p>
      <div class="tldr reveal"><p class="tag">W skrócie</p><ul>%s</ul></div>
      <nav class="toc reveal" aria-label="Spis treści"><p class="tag">Spis treści</p><ol>%s</ol></nav>
%s
      %s
      %s
    </article>
  </div>
</section>

%s

%s''' % (''.join('<li>%s</li>' % li for li in a['tldr']), toc_html, body, faq_html(a['faq']), AUTHOR, CTA,
         related_html(a['related'], mins_by))
        words = len(strip_tags(a['lead'] + ' ' + body).split())
        img = B + 'assets/img/og/%s.jpg' % slug
        ld = [
            {'@type': 'BlogPosting', '@id': url + '#artykul', 'headline': a['headline'], 'description': a['description'],
             'datePublished': pub(a), 'dateModified': mod(a), 'inLanguage': 'pl-PL', 'mainEntityOfPage': {'@id': url + '#strona'},
             'author': PER, 'publisher': ORG, 'image': {'@type': 'ImageObject', 'url': img, 'width': 1200, 'height': 630},
             'articleSection': 'Poradnik', 'keywords': a['keywords'], 'wordCount': words, 'timeRequired': 'PT%dM' % mins,
             'isPartOf': {'@id': B + 'poradnik#strona'}, 'about': {'@id': B + '#firma'},
             'abstract': ' '.join(strip_tags(li) for li in a['tldr'])},
            {'@type': 'WebPage', '@id': url + '#strona', 'url': url, 'name': a['headline'], 'description': a['description'], 'inLanguage': 'pl-PL',
             'isPartOf': {'@id': B + '#strona'}, 'datePublished': pub(a), 'dateModified': mod(a), 'primaryImageOfPage': {'@type': 'ImageObject', 'url': img},
             'breadcrumb': crumbs([('Start', B), ('Poradnik', B + 'poradnik'), (a['og_title'], url)])},
            {'@type': 'FAQPage', '@id': url + '#pytania', 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in a['faq']]},
        ]
        art_meta = '\n'.join(['<meta property="article:published_time" content="%sT09:00:00+02:00">' % pub(a),
                              '<meta property="article:modified_time" content="%sT09:00:00+02:00">' % mod(a),
                              '<meta property="article:author" content="%so-mnie">' % B,
                              '<meta property="article:section" content="Poradnik">']
                             + ['<meta property="article:tag" content="%s">' % esc(k) for k in a['keywords'][:4]])
        out = build_page(shell, a, main_html, ld, og_type='article', article_meta=art_meta)
        open(slug + '.html', 'w', encoding='utf-8').write(out)
        print('zbudowano', slug, '— %d min, %d słów, %d sekcji' % (mins, words, len(toc)))

    # strony usług
    for p in USLUGI:
        slug, url = p['slug'], B + p['slug']
        segs, toc = render_body(p['body'])
        toc_html = ''.join('<li><a href="#%s">%s</a></li>' % (sid, esc(t)) for sid, t in toc) + '<li><a href="#pytania">Najczęstsze pytania</a></li>'
        side = ''.join('<p>%s</p>' % esc(x) for x in p['side'])
        parts = [phead_svc(p['h1'], p['lead'], side, p['crumb'])]
        if p.get('blok_gora'):
            parts.append(svc_block(blocks[p['blok_gora']]))
        parts.append(PROSE_OPEN + '      <p class="prose__en" data-i18n="svcpage.en"></p>\n'
                     '      <div class="tldr reveal"><p class="tag">W skrócie</p><ul>%s</ul></div>\n'
                     '      <nav class="toc reveal" aria-label="Spis treści"><p class="tag">Spis treści</p><ol>%s</ol></nav>\n'
                     % (''.join('<li>%s</li>' % li for li in p['tldr']), toc_html))
        for kind, h in segs:
            if kind == 'html':
                parts.append(h)
            else:
                parts.append(PROSE_CLOSE + '\n\n' + svc_block(blocks[h]) + '\n\n' + PROSE_OPEN)
        parts.append('\n      %s\n      %s' % (faq_html(p['faq']), AUTHOR) + PROSE_CLOSE)
        parts.append('\n\n' + CTA + '\n\n' + related_html(p['related'], mins_by, 'Z poradnika'))
        main_html = '\n'.join(parts)
        img = B + 'assets/img/og/%s.jpg' % slug
        service = {'@type': 'Service', '@id': url + '#usluga', 'url': url, 'provider': ORG}
        service.update(p['service'])
        ld = [
            {'@type': 'WebPage', '@id': url + '#strona', 'url': url, 'name': p['og_title'], 'description': p['description'], 'inLanguage': 'pl-PL',
             'isPartOf': {'@id': B + '#strona'}, 'about': {'@id': url + '#usluga'}, 'datePublished': pub(p), 'dateModified': mod(p),
             'primaryImageOfPage': {'@type': 'ImageObject', 'url': img, 'width': 1200, 'height': 630}, 'keywords': p['keywords'],
             'breadcrumb': crumbs([('Start', B), ('Usługi', B + 'uslugi'), (p['name'], url)])},
            service,
        ]
        for pid, name, desc, price in p.get('produkty', []):
            ld.append({'@type': 'Product', '@id': url + '#' + pid, 'name': name, 'description': desc, 'image': img,
                       'brand': {'@type': 'Brand', 'name': 'Marcel Struszczak'}, 'category': 'Karty NFC do opinii Google',
                       'offers': {'@type': 'Offer', 'price': price, 'priceCurrency': 'PLN', 'availability': 'https://schema.org/InStock',
                                  'itemCondition': 'https://schema.org/NewCondition', 'url': url, 'seller': {'@id': B + '#firma'}}})
        ld.append({'@type': 'FAQPage', '@id': url + '#pytania', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in p['faq']]})
        out = build_page(shell, p, main_html, ld, num='02')
        open(slug + '.html', 'w', encoding='utf-8').write(out)
        print('zbudowano', slug, '— %d sekcji, bloki: %s' % (len(toc), ', '.join([p.get('blok_gora') or ''] + [h for k, h in segs if k == 'blok']).strip(', ')))

    # strona Poradnik
    pg = PORADNIK
    side = '<p>Strony internetowe</p><p>Social media</p><p>Opinie Google</p>'
    main_html = phead(pg['h1'], pg['lead'], side) + '''

<section class="sec" style="padding-top:8px">
  <div class="wrap">
    <p class="prose__en" data-i18n="guide.en"></p>
    <div class="guides">%s</div>
  </div>
</section>

%s''' % (''.join(card(a['slug'], mins_by[a['slug']], 'h2') for a in ARTYKULY), CTA)
    url = B + 'poradnik'
    ld = [
        {'@type': 'CollectionPage', '@id': url + '#strona', 'url': url, 'name': 'Poradnik dla firm', 'description': pg['description'],
         'inLanguage': 'pl-PL', 'isPartOf': {'@id': B + '#strona'}, 'about': {'@id': B + '#firma'}, 'dateModified': max(mod(a) for a in ARTYKULY),
         'breadcrumb': crumbs([('Start', B), ('Poradnik', url)]),
         'mainEntity': {'@type': 'ItemList', 'itemListElement': [
             {'@type': 'ListItem', 'position': i + 1, 'url': B + a['slug'], 'name': a['headline']} for i, a in enumerate(ARTYKULY)]}},
    ]
    out = build_page(shell, pg, main_html, ld)
    open('poradnik.html', 'w', encoding='utf-8').write(out)
    print('zbudowano poradnik')

    # karty „Z poradnika” na stronie głównej i na stronie Usługi
    update_cards('index.html', NA_STARCIE, mins_by)
    update_cards('uslugi.html', NA_USLUGACH, mins_by)

    build_feed()
    build_sitemap()


if __name__ == '__main__':
    main()
