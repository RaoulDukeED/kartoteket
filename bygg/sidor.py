"""HTML för sajtens sidor. Alla länkar är relativa, så sajten fungerar oavsett adress."""
from html import escape

from kartotek import SEKTIONER, datum_text, rak

VISNING = 60  # så många rader visas innan "Bläddra vidare"

GEM = ('<svg class="gem" width="18" height="22" viewBox="0 0 18 22" fill="none" stroke="currentColor" '
       'stroke-width="1.6" stroke-linecap="round" role="img" aria-label="Har bilagor">'
       '<path d="M12 6v9a3 3 0 0 1-6 0V4.5a2 2 0 0 1 4 0V14a1 1 0 0 1-2 0V7"/></svg>')
GEM_STOR = ('<svg class="bilaga-gem" width="22" height="44" viewBox="0 0 22 44" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" aria-hidden="true">'
            '<path d="M15 10v22a5 5 0 0 1-10 0V7a4 4 0 0 1 8 0v24a2 2 0 0 1-4 0V12"/></svg>')

e = escape


def tal(n):
    return f"{n:,}".replace(",", " ")


def kort_ord(n):
    return f"{tal(n)} kort"


# ---------------------------------------------------------------- ramen

def sida(titel, kropp, djup, uppdaterad, aktiv=None, beskrivning=""):
    R = "../" * djup
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{R}{s}/"{cur if s == aktiv else ""}>{namn}</a>'
        for s, namn in SEKTIONER.items()
    )
    beskr = f'<meta name="description" content="{e(beskrivning)}">' if beskrivning else ""
    return f"""<!doctype html>
<html lang="sv" data-rot="{R}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
{beskr}
<link rel="preload" href="{R}typsnitt/spectral-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{R}typsnitt/courier-prime-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{R}stil.css">
<link rel="icon" href="{R}ikon.svg" type="image/svg+xml">
<script src="{R}kartotek.js" defer></script>
</head>
<body>
<a class="hoppa" href="#innehall">Hoppa till innehållet</a>
<div class="sida">
<header class="topp">
<a class="namn" href="{R}./">Kartoteket</a>
<nav aria-label="Avdelningar">{nav}</nav>
</header>
<main id="innehall">
{kropp}
</main>
<footer class="fot">
<p>Uppdaterad {datum_text(uppdaterad)}. Betygen kommer från Goodreads och IMDb, bokuppgifterna från Libris.</p>
<p><a href="{R}sok/">Sök i katalogen</a></p>
</footer>
</div>
</body>
</html>
"""


def sokvag(R, delar):
    """delar: [(text, url eller None)]"""
    lankar = [f'<a href="{R}./">Kartoteket</a>']
    for text, url in delar:
        lankar.append(f'<a href="{R}{url}">{e(text)}</a>' if url else e(text))
    return f'<nav class="sokvag" aria-label="Sökväg">{" / ".join(lankar)}</nav>'


def slumpknapp(R, reserv, klass="knapp"):
    return f'<a class="{klass}" href="{R}{e(reserv)}" data-slump>Dra ett kort på måfå</a>'


# ---------------------------------------------------------------- rader i lådan

def betygsruta(k, klass="betyg"):
    hog = " hog" if k["betyg"] == k["skala"] else ""
    return (f'<span class="{klass}{hog}" aria-label="Betyg {k["betyg"]} av {k["skala"]}">'
            f'{k["betyg"] or "–"}</span>')


def rad(k, R, visa_upphov=True, visa_sektion=False):
    if k["sektion"] == "bocker":
        under = f'orig. {k["originaltitel"]}' if k["originaltitel"] else ""
    else:
        under = f'sv. {k["sv_titel"]}' if k["sv_titel"] else ""
    meta = []
    if visa_sektion:
        meta.append(k["typ_sv"])
    if k["ar"]:
        meta.append(str(k["ar"]))
    if visa_upphov and k["upphov_text"]:
        meta.append(k["upphov_text"])
    elif k["sektion"] == "bocker" and k.get("ar_utgava") and k["ar_utgava"] != k["ar"]:
        meta.append(f'utg. {k["ar_utgava"]}')
    markeringar = ""
    if k["bilagor"]:
        markeringar += GEM
    if k["kopplingar"]:
        markeringar += f'<span class="koppling">↔ {"film" if k["sektion"] == "bocker" else "bok"}</span>'
    r = round(k["betyg"] * 10 / k["skala"], 2)
    return (
        f'<li data-t="{e(k["sortering"])}" data-y="{k["ar"] or 9999}" data-r="{r}">'
        f'<a href="{R}{e(k["url"])}">'
        f'<span class="rad-titel"><span class="t">{e(k["titel"])}</span>'
        + (f'<span class="u">{e(under)}</span>' if under else "")
        + f'</span><span class="rad-meta">{e(", ".join(meta))}</span>'
        f'<span class="rad-mark">{markeringar}{betygsruta(k)}</span></a></li>'
    )


def kortlista(kort, R, sortering, visa_upphov=True, visa_sektion=False, sektion=None):
    ar_namn = "Originalår" if sektion == "bocker" else "År"
    knappar = "".join(
        f'<button type="button" data-sort="{kod}" aria-pressed="{"true" if kod == sortering else "false"}">{namn}</button>'
        for kod, namn in (("t", "Titel"), ("y", ar_namn), ("r", "Betyg"))
    )
    rader = "".join(rad(k, R, visa_upphov, visa_sektion) for k in kort)
    return f"""<div class="lista">
<div class="sortering" role="group" aria-label="Sortering"><span>Sortera efter</span>{knappar}</div>
<div class="lada-innehall">
<ul class="kortlista" data-visa="{VISNING}">{rader}</ul>
<div class="bladdra" hidden><span></span><button type="button">Bläddra vidare</button></div>
</div>
</div>"""


# ---------------------------------------------------------------- sidokolumnen

def lank(R, lada, aktuell, visa_antal=True, text=None):
    namn = e(text or lada["namn"])
    antal = f' <span class="antal">{tal(len(lada["kort"]))}</span>' if visa_antal else ""
    cur = ' aria-current="page"' if lada["slug"] == aktuell else ""
    return f'<li><a href="{R}{e(lada["url"])}"{cur}>{namn}{antal}</a></li>'


def block(K, R, grupp, aktuell, max_antal=None):
    lador = K.lador_i_grupp(grupp)
    if not lador:
        return ""
    if K.grupper[grupp]["ordna"] == "namn":   # de största först i sidokolumnen
        urval = sorted(lador, key=lambda l: -len(l["kort"]))
    else:
        urval = list(lador)
    if max_antal and len(urval) > max_antal:
        visade = urval[:max_antal]
        aktuell_lada = K.lador.get(aktuell)
        if aktuell_lada and aktuell_lada["grupp"] == grupp and aktuell_lada not in visade:
            visade.append(aktuell_lada)
    else:
        visade = urval
    rader = "".join(lank(R, l, aktuell) for l in visade)
    g = K.grupper[grupp]
    if max_antal and len(urval) > max_antal:
        rader += f'<li><a class="alla" href="{R}{e(g["url"])}">{e(g["kort_namn"])}</a></li>'
    return f'<div class="block"><h2>{e(g["namn"])}</h2><ul>{rader}</ul></div>'


def fler(K, R, aktuell, poster):
    rader = ""
    for slug_, text in poster:
        if slug_ in K.lador:
            rader += lank(R, K.lador[slug_], aktuell, text=text)
        elif slug_ in K.grupper:
            g = K.grupper[slug_]
            cur = ' aria-current="page"' if slug_ == aktuell else ""
            rader += f'<li><a href="{R}{e(g["url"])}"{cur}>{e(text)}</a></li>'
    return f'<div class="block"><h2>Fler lådor</h2><ul>{rader}</ul></div>' if rader else ""


def sidokolumn(K, R, sektion, aktuell):
    if sektion == "bocker":
        delar = [
            block(K, R, "bocker/forfattare", aktuell, 5),
            block(K, R, "bocker/oversattare", aktuell, 4),
            block(K, R, "bocker/utgiven", aktuell),
            block(K, R, "bocker/genre", aktuell, 6),
            fler(K, R, aktuell, [("bocker", "Alla böcker"), ("bocker/forlag", "Förlag"),
                                 ("bocker/betyg", "Betyg 1–5"), ("bocker/filmatiseringar", "Filmatiseringar"),
                                 ("hogsta-betyg", "Högsta betyg")]),
        ]
    elif sektion in ("film", "tv-serier"):
        delar = [
            block(K, R, f"{sektion}/decennium", aktuell),
            block(K, R, f"{sektion}/genre", aktuell, 8),
            fler(K, R, aktuell, [(sektion, f"Alla {SEKTIONER[sektion].lower()}"),
                                 ("film/regissor" if sektion == "film" else "", "Regissörer A–Ö"),
                                 (f"{sektion}/betyg", "Betyg 1–10"),
                                 (f"{sektion}/filmatiseringar", "Filmatiseringar"),
                                 ("hogsta-betyg", "Högsta betyg")]),
        ]
    elif sektion == "spel":
        delar = [fler(K, R, aktuell, [("spel", "Alla spel"), ("hogsta-betyg", "Högsta betyg")])]
    else:
        rader = "".join(lank(R, K.lador[s], aktuell, text=n) for s, n in SEKTIONER.items())
        delar = [f'<div class="block"><h2>Avdelningar</h2><ul>{rader}</ul></div>',
                 fler(K, R, aktuell, [("hogsta-betyg", "Högsta betyg")])]
    namn = SEKTIONER.get(sektion, "katalogen")
    return (f'<details class="sidokolumn" open><summary>Lådor i {e(namn)}</summary>'
            f'<div class="block-rad">{"".join(delar)}</div></details>')


# ---------------------------------------------------------------- sidor

def lada_sida(K, lada, uppdaterad):
    djup = lada["slug"].count("/") + 1
    R = "../" * djup
    s = lada["sektion"]
    delar = []
    if s and lada["slug"] != s:
        delar.append((SEKTIONER[s], f"{s}/"))
    if lada["grupp"]:
        delar.append((K.grupper[lada["grupp"]]["namn"], K.grupper[lada["grupp"]]["url"]))
    rubrik = SEKTIONER[s] if lada["slug"] == s else lada["namn"]
    delar.append((rubrik, None))
    antal = f'{kort_ord(len(lada["kort"]))}' + (f' i {SEKTIONER[s]}' if s and lada["slug"] != s else "")
    visa_upphov = not (lada["grupp"] == "bocker/forfattare")
    kropp = f"""<div class="rubrikrad">
{sokvag(R, delar)}
<div class="rubrik"><h1>{e(rubrik)}</h1><span class="antal-kort">{antal}</span></div>
</div>
<div class="lada-layout">
{sidokolumn(K, R, s, lada["slug"])}
{kortlista(lada["kort"], R, lada["sortering"], visa_upphov, visa_sektion=s is None, sektion=s)}
</div>"""
    titel = f"{rubrik} | Kartoteket" if lada["slug"] == s or not s else f"{rubrik}, {SEKTIONER[s]} | Kartoteket"
    return sida(titel, kropp, djup, uppdaterad, aktiv=s)


def grupp_sida(K, grupp, uppdaterad):
    g = K.grupper[grupp]
    djup = grupp.count("/") + 1
    R = "../" * djup
    s = g["sektion"]
    lador = K.lador_i_grupp(grupp)
    if g["ordna"] == "namn" and len(lador) > 40:
        bokstaver = {}
        for l in lador:
            forsta = l["ordning"][:1].upper()
            forsta = {"ﾡ": "Å", "ﾢ": "Ä", "ﾣ": "Ö"}.get(l["ordning"][:1], forsta)
            if not forsta.isalpha():
                forsta = "#"
            bokstaver.setdefault(forsta, []).append(l)
        register = "".join(f'<a href="#b-{e(b)}">{e(b)}</a>' for b in bokstaver)
        innehall = f'<nav class="register" aria-label="Bokstäver">{register}</nav>' + "".join(
            f'<section class="bokstav" id="b-{e(b)}"><h2>{e(b)}</h2><ul class="flikar">'
            + "".join(lank(R, l, None) for l in ls) + "</ul></section>"
            for b, ls in bokstaver.items()
        )
    else:
        innehall = '<ul class="flikar">' + "".join(lank(R, l, None) for l in lador) + "</ul>"
    kropp = f"""<div class="rubrikrad">
{sokvag(R, [(SEKTIONER[s], f"{s}/"), (g["namn"], None)])}
<div class="rubrik"><h1>{e(g["namn"])}</h1><span class="antal-kort">{tal(len(lador))} lådor i {SEKTIONER[s]}</span></div>
</div>
<div class="lada-layout">
{sidokolumn(K, R, s, grupp)}
<div class="lista">{innehall}</div>
</div>"""
    return sida(f"{g['namn']}, {SEKTIONER[s]} | Kartoteket", kropp, djup, uppdaterad, aktiv=s)


# ---------------------------------------------------------------- katalogkortet

def lada_lank(K, R, slug_, text=None):
    l = K.lador.get(slug_)
    if not l:
        return ""
    return f'<a href="{R}{e(l["url"])}">{e(text or l["namn"])}</a> ({tal(len(l["kort"]))})'


def lador_for(k, prefix):
    return [l for l in k["lador"] if l.startswith(prefix)]


def kort_sida(K, k, uppdaterad):
    R = "../../"
    s = k["sektion"]
    rader = []
    if s == "bocker":
        rubrik = (k["upphov"][0] if k["upphov"] else k["titel"]).upper()
        if k["isbn"] or k["isbn13"]:
            huvud = f'Bok, ISBN {k["isbn"] or k["isbn13"]}'
        else:
            huvud = f'Bok, Goodreads {k["gr_id"]}'
        titel = k["titel"] + (f' : {k["undertitel"]}' if k["undertitel"] else "")
        ansvar = f' / {e(k["upphov_text"])}' if k["upphov_text"] else ""
        if k["oversattare"]:
            ansvar += " ; övers. av " + e(" och ".join(rak(o) for o in k["oversattare"]))
        utg = []
        if k["forlag_norm"] or k["ar_utgava"]:
            utg.append(", ".join(x for x in (e(k["forlag_norm"]), str(k["ar_utgava"] or "")) if x))
        if k["sidor"]:
            utg.append(f'{k["sidor"]} s')
        if k["bindning"]:
            utg.append(k["bindning"])
        beskr = f'{e(titel)}{ansvar}.' + "".join(f" – {x}." for x in utg)
        rader.append(f'<div class="indrag">{beskr}</div>')
        if k["serie"]:
            rader.append(f'<div class="indrag">Serie: {e(k["serie"])}, {e(k["serie_nr"])}.</div>')
        orig = []
        if k["originaltitel"]:
            orig.append(f'Originaltitel: {e(k["originaltitel"])}.')
        if k["ar_original"] and (k["ar_original"] != k["ar_utgava"] or k["originaltitel"]):
            orig.append(f'Först utgiven {k["ar_original"]}.')
        if orig:
            rader.append(f'<div class="indrag">{" ".join(orig)}</div>')
        stycke1 = "".join(rader)
    else:
        rubrik = k["titel"].upper()
        huvud = f'{k["typ_sv"]}, {k["const"]}'
        regi_lankar = []
        for namn_lf in k["upphov"]:
            hit = next((l for l in lador_for(k, "film/regissor/") if K.lador[l]["namn"] == namn_lf), None)
            regi_lankar.append(f'<a href="{R}{e(K.lador[hit]["url"])}">{e(namn_lf)}</a>' if hit else e(namn_lf))
        if regi_lankar:
            rader.append(f'<div>{" ; ".join(regi_lankar)}.</div>')
        beskr = e(k["titel"])
        if k.get("regi"):
            beskr += f' / regi {e(" och ".join(k["regi"]))}'
        beskr += "."
        if k["ar"]:
            beskr += f' – {k["ar"]}.'
        if k.get("minuter") and k["typ"] not in ("TV Series", "TV Mini Series", "Video Game"):
            beskr += f' – {k["minuter"]} min.'
        rader.append(f'<div class="indrag">{beskr}</div>')
        if k["sv_titel"]:
            rader.append(f'<div class="indrag">Sv. titel: {e(k["sv_titel"])}</div>')
        if k.get("serie_id"):
            serie = K.efter_id[k["serie_id"]]
            rader.append(f'<div class="indrag">Avsnitt i: <a href="{R}{e(serie["url"])}">{e(serie["titel"])}</a>.</div>')
        elif k.get("serie"):
            rader.append(f'<div class="indrag">Avsnitt i: {e(k["serie"])}.</div>')
        stycke1 = "".join(rader)

    genre = f'<div>Genre: {e(", ".join(g.lower() for g in k["genre"]))}.</div>' if k["genre"] else ""
    betyg = (f'<div class="betygsrad"><span>Betyg:</span>{betygsruta(k, "betyg stor")}'
             f'<span class="dampad">av {k["skala"]}</span></div>')

    # Se även
    se = []
    for annat_id, typ in k["kopplingar"]:
        a = K.efter_id[annat_id]
        fri = " (fri tolkning)" if typ == "fri tolkning" else ""
        if s == "bocker":
            se.append(f'<a href="{R}{e(a["url"])}">{e(a["titel"])} ({a["ar"]})</a>{fri}, betyg {a["betyg"]} av {a["skala"]}.')
        else:
            namn = f'{a["upphov"][0]}. ' if a["upphov"] else ""
            se.append(f'<a href="{R}{e(a["url"])}">{e(namn)}{e(a["titel"])}. – {a["ar"]}.</a>{fri} Betyg {a["betyg"]} av {a["skala"]}.')
    se_rader = []
    if se:
        etikett = "Filmatiseringar" if s == "bocker" else ("Bok" if len(se) == 1 else "Böcker")
        se_rader.append(f'<div class="indrag">{etikett}: {" ".join(se)}</div>')
    if k.get("avsnitt_ids"):
        avs = [K.efter_id[i] for i in k["avsnitt_ids"]]
        avs.sort(key=lambda a: (a["ar"] or 0, a["sortering"]))
        se_rader.append('<div class="indrag">Avsnitt: ' + ", ".join(
            f'<a href="{R}{e(a["url"])}">{e(a.get("avsnitt") or a["titel"])}</a>' for a in avs) + ".</div>")
    if s == "bocker":
        lador = lador_for(k, "bocker/forfattare/") + lador_for(k, "bocker/oversattare/") + \
            [(l, "Först utgiven " + K.lador[l]["namn"]) for l in lador_for(k, "bocker/utgiven/")] + \
            lador_for(k, "bocker/genre/")
    elif s == "spel":
        lador = ["spel"]
    else:
        lador = lador_for(k, f"{s}/decennium/") + lador_for(k, f"{s}/genre/")
    lador_text = ", ".join(
        lada_lank(K, R, *(l if isinstance(l, tuple) else (l,))) for l in lador
    )
    if lador_text:
        se_rader.append(f'<div class="indrag">Lådor: {lador_text}.</div>')
    se_aven = f'<div class="se-aven"><div>Se även:</div>{"".join(se_rader)}</div>' if se_rader else ""

    # Spårningar längst ner på kortet
    spar = []
    if s == "bocker":
        spar += k["upphov"]
        spar += [f"{o.rstrip('.')}, övers" for o in k["oversattare"]]
        if k["kopplingar"]:
            spar.append("Filmatiserade böcker")
    else:
        spar += k["upphov"]
        for annat_id, _ in k["kopplingar"]:
            a = K.efter_id[annat_id]
            if a["upphov"]:
                spar.append(f'{a["upphov"][0]} – filmatiseringar')
    sparning = " ".join(f"{i}. {e(t)}." for i, t in enumerate(dict.fromkeys(spar), 1))
    sparning = f'<div class="sparning">{sparning}</div>' if sparning else ""

    stampel = f'<span class="stampel">{e(k["stampel"])}</span>' if k["stampel"] else ""
    kort_html = f"""<article class="kort" aria-labelledby="kortrubrik">
<div class="kort-huvud"><span>{e(huvud)}</span>{stampel}</div>
<div class="kort-falt">
<div class="kort-kropp">
<h1 id="kortrubrik">{e(rubrik)}</h1>
<div>{stycke1}</div>
{genre}
{betyg}
{se_aven}
</div>
{sparning}
</div>
<div class="hal" aria-hidden="true"></div>
</article>"""

    kalla = ""
    if s == "bocker" and k["libris"]:
        kalla = "Uppgifter från Libris." if k["libris"] == "isbn" else \
            "Uppgifter från Libris, hämtade på titel. Utgåvan kan skilja sig från den jag läste."
        kalla = f'<p class="kalla">{kalla}</p>'

    bilagor = "".join(bilaga_html(b, i) for i, b in enumerate(k["bilagor"], 1))

    # Föregående och nästa i hemlådan
    hem = K.lador[k["hem"]]
    i = next(n for n, x in enumerate(hem["kort"]) if x["id"] == k["id"])
    fore = hem["kort"][i - 1] if i > 0 else None
    nasta = hem["kort"][i + 1] if i + 1 < len(hem["kort"]) else None
    bladdra = '<nav class="kort-nav" aria-label="Bläddra i lådan">'
    bladdra += (f'<a class="fore" href="{R}{e(fore["url"])}"><span>Föregående kort</span>'
                f'<span class="kt">{e(fore["titel"])}</span></a>') if fore else "<span></span>"
    bladdra += slumpknapp(R, k["url"])
    bladdra += (f'<a class="nasta" href="{R}{e(nasta["url"])}"><span>Nästa kort</span>'
                f'<span class="kt">{e(nasta["titel"])}</span></a>') if nasta else "<span></span>"
    bladdra += "</nav>"

    delar = [(SEKTIONER[s], f"{s}/")]
    if hem["grupp"]:
        delar.append((hem["namn"], hem["url"]))
    delar.append((k["titel"], None))

    kropp = f"""{sokvag(R, delar)}
<div class="kort-yta">
{kort_html}
{kalla}
{bilagor}
</div>
{bladdra}"""
    if s == "bocker" and k["upphov_text"]:
        titel = f'{k["titel"]}, {k["upphov_text"]} | Kartoteket'
    else:
        ar_text = f' ({k["ar"]})' if k["ar"] else ""
        titel = f'{k["titel"]}{ar_text} | Kartoteket'
    beskrivning = f'{k["typ_sv"]}: {k["titel"]}' + (f', {k["upphov_text"]}' if k["upphov_text"] else "") + \
        f'. Betyg {k["betyg"]} av {k["skala"]}.'
    return sida(titel, kropp, 2, uppdaterad, aktiv=s, beskrivning=beskrivning)


def bilaga_html(b, nr):
    typ = {"citat": "Citat", "reflektion": "Reflektion", "bild": "Bild"}.get(b["typ"], b["typ"].capitalize())
    stycken = "".join(f"<p>{e(p.strip())}</p>".replace("\n", "<br>") for p in b["text"].split("\n\n") if p.strip())
    if b["typ"] == "citat" and stycken:
        stycken = f"<blockquote>{stycken}</blockquote>"
    bild = f'<img src="{e(b["bild"])}" alt="" loading="lazy">' if b["bild"] else ""
    return f"""<aside class="bilaga" aria-label="Bilaga {nr}">{GEM_STOR}
<div class="bilaga-typ">Bilaga {nr}, {e(typ.lower())}</div>{bild}{stycken}</aside>"""


# ---------------------------------------------------------------- startsidan, sök, 404

def start_sida(K, texter, uppdaterad, reserv):
    R = ""
    fronter = "".join(
        f'<a class="front" href="{s}/"><span class="etikett">{namn}</span>'
        f'<span class="antal">{kort_ord(len(K.lador[s]["kort"]))}</span><span class="handtag" aria-hidden="true"></span></a>'
        for s, namn in SEKTIONER.items()
    )
    hogsta = K.lador.get("hogsta-betyg", {"kort": []})
    kropp = f"""<section class="intro">
<div class="intro-text">
<h1>{e(texter["rubrik"])}</h1>
{texter["ingress"]}
</div>
<form class="sok" action="sok/" role="search">
<label for="sok">Sök i katalogen</label>
<input id="sok" name="q" type="search" placeholder="t.ex. Chandler eller 1947" autocomplete="off">
</form>
</section>
<section class="skap" aria-label="Katalogskåpet">{fronter}</section>
<section class="skap-rad">
<a class="front bred" href="hogsta-betyg/"><span class="etikett rost">Högsta betyg</span><span class="antal">{kort_ord(len(hogsta["kort"]))}, alla tior och femmor</span></a>
{slumpknapp(R, reserv, "knapp stor")}
</section>
<section class="om">
<h2>Om betygen</h2>
<div>{texter["om betygen"]}</div>
</section>"""
    return sida(f"{texter['rubrik']} | Kartoteket", kropp, 0, uppdaterad, beskrivning=texter["beskrivning"])


def sok_sida(uppdaterad):
    R = "../"
    kropp = f"""<div class="rubrikrad">
{sokvag(R, [("Sök", None)])}
<div class="rubrik"><h1>Sök i katalogen</h1></div>
</div>
<form class="sok sok-sida" action="./" role="search">
<label for="sok">Titel, upphov, översättare eller år</label>
<div class="sok-falt"><input id="sok" name="q" type="search" autocomplete="off"><button class="knapp" type="submit">Sök</button></div>
</form>
<p class="sok-status" aria-live="polite"></p>
<div class="lada-innehall sok-resultat" hidden><ul class="kortlista"></ul></div>
<noscript><p>Sökningen behöver javascript. Bläddra i lådorna i stället.</p></noscript>"""
    return sida("Sök | Kartoteket", kropp, 1, uppdaterad)


def saknas_sida(uppdaterad, bas):
    kropp = f"""<div class="rubrikrad"><div class="rubrik"><h1>Kortet finns inte</h1></div></div>
<p class="ingress">Det här kortet finns inte i kartoteket, eller så har det flyttats.</p>
<p><a class="knapp" href="{bas}">Till katalogskåpet</a></p>"""
    html = sida("Kortet finns inte | Kartoteket", kropp, 0, uppdaterad)
    # 404-sidan kan visas på vilken adress som helst, så den länkar från sajtens rot.
    return html.replace('data-rot=""', f'data-rot="{bas}"').replace('href="stil.css"', f'href="{bas}stil.css"') \
        .replace('src="kartotek.js"', f'src="{bas}kartotek.js"').replace('href="ikon.svg"', f'href="{bas}ikon.svg"') \
        .replace('href="./"', f'href="{bas}"').replace('href="sok/"', f'href="{bas}sok/"') \
        .replace('href="bocker/"', f'href="{bas}bocker/"').replace('href="film/"', f'href="{bas}film/"') \
        .replace('href="tv-serier/"', f'href="{bas}tv-serier/"').replace('href="spel/"', f'href="{bas}spel/"')
