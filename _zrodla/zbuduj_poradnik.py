# -*- coding: utf-8 -*-
"""Buduje strony poradnika z poradnik_tresc.py.

Uruchom z katalogu repozytorium:  python3 _zrodla/zbuduj_poradnik.py
Szablonem (nagłówek, menu, kurtyna, stopka) jest polityka-prywatnosci.html.
Folder _zrodla nie jest publikowany przez GitHub Pages (Jekyll pomija foldery z „_”).
"""
import html
import json
import os
import re
import sys

import markdown

sys.path.insert(0, os.path.dirname(__file__))
from poradnik_tresc import ARTYKULY, PORADNIK, DATA, DATA_TXT  # noqa: E402

B = 'https://marcelgraphicsite.pl/'
ORG = {'@type': 'ProfessionalService', '@id': B + '#firma', 'name': 'Marcel Struszczak — strony internetowe i social media',
       'url': B, 'logo': B + 'assets/img/apple-touch-icon.png', 'telephone': '+48 511 808 498', 'email': 'marcel.graphicsite@gmail.com'}
PER = {'@type': 'Person', '@id': B + '#marcel', 'name': 'Marcel Struszczak', 'url': B + 'o-mnie', 'jobTitle': 'Projektant stron internetowych'}
BY_SLUG = {a['slug']: a for a in ARTYKULY}
PL_MAP = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')


def esc(s):
    return html.escape(s, quote=True)


def slugify(s):
    s = re.sub(r'<[^>]+>', '', s).translate(PL_MAP).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:60].rstrip('-')


def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def md_to_html(md):
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
    toc, seen = [], set()

    def add_id(m):
        level, inner = m.group(1), m.group(2)
        sid = slugify(inner)
        while sid in seen:
            sid += '-2'
        seen.add(sid)
        if level == '2':
            toc.append((sid, strip_tags(inner)))
        return '<h%s id="%s">%s</h%s>' % (level, sid, inner, level)
    out = re.sub(r'<h([23])>(.*?)</h\1>', add_id, out)
    return out, toc


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


def build_page(shell, page, main_html, ld, og_type='website', article_meta=''):
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
    cur = ('<p class="curtain__n">(06)</p><p class="curtain__t%s" data-en="%s">%s</p><p class="curtain__s" data-en="%s">%s</p>'
           % (' is-long' if len(t_pl) > 9 else '', esc(t_en), esc(t_pl), esc(s_en), esc(s_pl)))
    s, n = re.subn(r'<p class="curtain__n">[^<]*</p><p class="curtain__t[^"]*" data-en="[^"]*">[^<]*</p><p class="curtain__s" data-en="[^"]*">[^<]*</p>', lambda m: cur, s, count=1)
    assert n == 1
    s, n = re.subn(r'<main id="main">.*?</main>', lambda m: '<main id="main">\n\n' + main_html + '\n\n</main>', s, count=1, flags=re.S)
    assert n == 1
    s = s.replace('<li><a href="poradnik" data-i18n="foot.guides">Poradnik</a></li>',
                  '<li><a href="poradnik"%s data-i18n="foot.guides">Poradnik</a></li>' % (' aria-current="page"' if slug == 'poradnik' else ''), 1)
    return s


def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def main():
    root = os.path.join(os.path.dirname(__file__), '..')
    os.chdir(root)
    shell = open('polityka-prywatnosci.html', encoding='utf-8').read()
    shell = shell.replace('<li><a href="poradnik" aria-current="page" data-i18n="foot.guides">', '<li><a href="poradnik" data-i18n="foot.guides">')
    mins_by = {}
    built = {}
    for a in ARTYKULY:
        body, toc = md_to_html(a['body'])
        faq_txt = ' '.join(q + ' ' + ans for q, ans in a['faq'])
        mins = minutes(a['lead'], ' '.join(a['tldr']), a['body'], faq_txt)
        mins_by[a['slug']] = mins
        built[a['slug']] = (body, toc, mins)

    for a in ARTYKULY:
        slug, url = a['slug'], B + a['slug']
        body, toc, mins = built[slug]
        toc_html = ''.join('<li><a href="#%s">%s</a></li>' % (sid, esc(t)) for sid, t in toc) + '<li><a href="#pytania">Najczęstsze pytania</a></li>'
        qa = ''.join(
            '<div class="qa"><h3><button type="button" aria-expanded="false" aria-controls="gq%d" id="gqb%d"><span>%s</span><i aria-hidden="true">+</i></button></h3>'
            '<div class="qa__a" id="gq%d" role="region" aria-labelledby="gqb%d"><div><p>%s</p></div></div></div>' % (i, i, esc(q), i, i, esc(ans))
            for i, (q, ans) in enumerate(a['faq'], 1))
        side = '<p>Marcel Struszczak</p><p><time datetime="%s">%s</time></p><p>%d min czytania</p>' % (DATA, DATA_TXT, mins)
        main_html = phead(a['h1'], a['lead'], side) + '''

<section class="sec" style="padding-top:8px">
  <div class="wrap">
    <article class="prose">
      <p class="prose__en" data-i18n="guide.en"></p>
      <div class="tldr reveal"><p class="tag">W skrócie</p><ul>%s</ul></div>
      <nav class="toc reveal" aria-label="Spis treści"><p class="tag">Spis treści</p><ol>%s</ol></nav>
%s
      <section class="faq-mini" aria-labelledby="pytania"><h2 id="pytania">Najczęstsze pytania</h2>%s</section>
      <aside class="author"><span class="author__mark" aria-hidden="true">MS</span><div><p><b>Marcel Struszczak</b></p><p>Projektuję strony internetowe, prowadzę social media i wdrażam karty NFC do opinii Google dla firm z całej Polski. <a href="o-mnie">Więcej o mnie</a> · <a href="poradnik">Wszystkie poradniki</a></p></div></aside>
    </article>
  </div>
</section>

%s

<section class="sec rule">
  <div class="wrap">
    <p class="tag reveal" style="margin-bottom:22px">Czytaj też</p>
    <div class="guides">%s</div>
  </div>
</section>''' % (''.join('<li>%s</li>' % li for li in a['tldr']), toc_html, body, qa, CTA,
                  ''.join(card(r, mins_by[r]) for r in a['related']))
        words = len(strip_tags(a['lead'] + ' ' + a['body']).split())
        ld = [
            {'@type': 'BlogPosting', '@id': url + '#artykul', 'headline': a['headline'], 'description': a['description'],
             'datePublished': DATA, 'dateModified': DATA, 'inLanguage': 'pl-PL', 'mainEntityOfPage': {'@id': url + '#strona'},
             'author': PER, 'publisher': ORG, 'image': {'@type': 'ImageObject', 'url': B + 'assets/img/og/%s.jpg' % slug, 'width': 1200, 'height': 630},
             'articleSection': 'Poradnik', 'keywords': a['keywords'], 'wordCount': words, 'timeRequired': 'PT%dM' % mins,
             'isPartOf': {'@id': B + 'poradnik#strona'}, 'about': {'@id': B + '#firma'},
             'abstract': ' '.join(strip_tags(li) for li in a['tldr'])},
            {'@type': 'WebPage', '@id': url + '#strona', 'url': url, 'name': a['headline'], 'description': a['description'], 'inLanguage': 'pl-PL',
             'isPartOf': {'@id': B + '#strona'}, 'datePublished': DATA, 'dateModified': DATA, 'primaryImageOfPage': {'@type': 'ImageObject', 'url': B + 'assets/img/og/%s.jpg' % slug},
             'breadcrumb': crumbs([('Start', B), ('Poradnik', B + 'poradnik'), (a['og_title'], url)])},
            {'@type': 'FAQPage', '@id': url + '#pytania', 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in a['faq']]},
        ]
        art_meta = '\n'.join(['<meta property="article:published_time" content="%sT09:00:00+02:00">' % DATA,
                              '<meta property="article:modified_time" content="%sT09:00:00+02:00">' % DATA,
                              '<meta property="article:author" content="%so-mnie">' % B,
                              '<meta property="article:section" content="Poradnik">']
                             + ['<meta property="article:tag" content="%s">' % esc(k) for k in a['keywords'][:4]])
        out = build_page(shell, a, main_html, ld, og_type='article', article_meta=art_meta)
        open(slug + '.html', 'w', encoding='utf-8').write(out)
        print('zbudowano', slug, '— %d min, %d słów, %d sekcji' % (mins, words, len(toc)))

    p = PORADNIK
    side = '<p>Strony internetowe</p><p>Social media</p><p>Opinie Google</p>'
    main_html = phead(p['h1'], p['lead'], side) + '''

<section class="sec" style="padding-top:8px">
  <div class="wrap">
    <p class="prose__en" data-i18n="guide.en"></p>
    <div class="guides">%s</div>
  </div>
</section>

%s''' % (''.join(card(a['slug'], mins_by[a['slug']], 'h2') for a in ARTYKULY), CTA)
    url = B + 'poradnik'
    ld = [
        {'@type': 'CollectionPage', '@id': url + '#strona', 'url': url, 'name': 'Poradnik dla firm', 'description': p['description'],
         'inLanguage': 'pl-PL', 'isPartOf': {'@id': B + '#strona'}, 'about': {'@id': B + '#firma'}, 'dateModified': DATA,
         'breadcrumb': crumbs([('Start', B), ('Poradnik', url)]),
         'mainEntity': {'@type': 'ItemList', 'itemListElement': [
             {'@type': 'ListItem', 'position': i + 1, 'url': B + a['slug'], 'name': a['headline']} for i, a in enumerate(ARTYKULY)]}},
    ]
    out = build_page(shell, p, main_html, ld)
    open('poradnik.html', 'w', encoding='utf-8').write(out)
    print('zbudowano poradnik')

    # karty artykułów na stronie Usługi (między znacznikami poradnik:start / poradnik:end)
    u = open('uslugi.html', encoding='utf-8').read()
    cards = ''.join(card(a['slug'], mins_by[a['slug']]) for a in ARTYKULY)
    u, n = re.subn(r'<!-- poradnik:start -->.*?<!-- poradnik:end -->', lambda m: '<!-- poradnik:start -->' + cards + '<!-- poradnik:end -->', u, count=1, flags=re.S)
    if n:
        open('uslugi.html', 'w', encoding='utf-8').write(u)
        print('zaktualizowano karty na uslugi.html')


if __name__ == '__main__':
    main()
