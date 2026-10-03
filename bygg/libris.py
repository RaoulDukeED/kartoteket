"""Berikar nya böcker med uppgifter från Libris.

Slår bara upp böcker som saknas i data/libris_berikning.json och lägger till dem
där. Böcker som fortfarande saknar genre skrivs till rapport/att_fylla_i.csv.

    python bygg/libris.py
"""
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kartotek  # noqa: E402

ROT = Path(__file__).resolve().parent.parent
BERIKNING = ROT / "data" / "libris_berikning.json"
RAPPORT = ROT / "rapport" / "att_fylla_i.csv"

SOK = "https://libris.kb.se/find.jsonld?q="
PAUS = 0.7
VANTA_VID_HTML = [3, 6, 9, 12]
MEDIATERMER = {"Talböcker", "Ljudböcker", "E-böcker"}


def hamta(fraga):
    """Hämtar en sökning. Libris svarar med HTML när det är för många anrop."""
    url = SOK + urllib.parse.quote(fraga)
    for vanta in [0] + VANTA_VID_HTML:
        if vanta:
            time.sleep(vanta)
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/ld+json"})
            with urllib.request.urlopen(req, timeout=30) as svar:
                text = svar.read().decode("utf-8")
        except (urllib.error.URLError, TimeoutError):
            continue
        if text.lstrip().startswith("{"):
            return json.loads(text)
    return None


def som_lista(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def utgavor(svar):
    """Utgåvor i svaret, både direkt och via bestånd (Item › itemOf)."""
    for post in (svar or {}).get("items", []):
        if "instanceOf" in post:
            yield post
        elif "instanceOf" in (post.get("itemOf") or {}):
            yield post["itemOf"]


def isbn_i(utgava):
    return {
        re.sub(r"[^0-9X]", "", str(i.get("value", "")).upper())
        for i in som_lista(utgava.get("identifiedBy"))
        if i.get("@type") == "ISBN"
    }


def plocka(utgava, bok_id, metod):
    verk = utgava.get("instanceOf") or {}
    post = {"id": bok_id, "m": metod}

    genrer = []
    for kat in som_lista(verk.get("category")) + som_lista(verk.get("genreForm")):
        kid = kat.get("@id", "") if isinstance(kat, dict) else ""
        if "/term/saogf/" not in kid:
            continue
        namn = kat.get("prefLabel") or urllib.parse.unquote(kid.rsplit("/", 1)[-1])
        if namn not in MEDIATERMER and namn not in genrer:
            genrer.append(namn)
    if genrer:
        post["g"] = genrer

    oversattare = []
    for bidrag in som_lista(verk.get("contribution")):
        roller = [r.get("@id", "") + " " + str(r.get("code", "")) for r in som_lista(bidrag.get("role"))]
        if not any("translator" in r or r.strip().endswith("trl") for r in roller):
            continue
        agent = bidrag.get("agent") or {}
        if agent.get("familyName"):
            namn = agent["familyName"] + (", " + agent["givenName"] if agent.get("givenName") else "")
        else:
            namn = agent.get("name", "")
        if namn:
            oversattare.append(namn)
    if oversattare:
        post["tr"] = oversattare

    for original in som_lista(verk.get("translationOf")):
        for titel in som_lista(original.get("hasTitle")):
            if titel.get("mainTitle"):
                post["o"] = str(som_lista(titel["mainTitle"])[0])
                break
        if "o" in post:
            break

    for klass in som_lista(verk.get("classification")):
        if (klass.get("inScheme") or {}).get("code") == "kssb" and klass.get("code"):
            post["c"] = klass["code"]
            break

    if utgava.get("responsibilityStatement"):
        post["r"] = str(som_lista(utgava["responsibilityStatement"])[0])
    for titel in som_lista(utgava.get("hasTitle")):
        if titel.get("mainTitle"):
            post["t"] = str(som_lista(titel["mainTitle"])[0])
            break
    for pub in som_lista(utgava.get("publication")):
        if pub.get("year"):
            post["y"] = str(pub["year"])
            break
    return post


def jamfor(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(t for t in s if not unicodedata.combining(t))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def sla_upp(bok):
    if bok["isbn"]:
        svar = hamta(bok["isbn"])
        for utgava in utgavor(svar):
            if bok["isbn"] in isbn_i(utgava) or bok["isbn13"] in isbn_i(utgava):
                return plocka(utgava, int(bok["gr_id"]), "isbn")
        time.sleep(PAUS)

    titel = jamfor(bok["titel_kort"])
    efternamn = jamfor(bok["forfattare_lf"].split(",")[0]) if bok["forfattare_lf"] else ""
    svar = hamta(f"{bok['titel_kort']} {bok['forfattare']}")
    for utgava in utgavor(svar):
        titlar = [jamfor(str(som_lista(t.get("mainTitle"))[0])) for t in som_lista(utgava.get("hasTitle")) if t.get("mainTitle")]
        ansvar = jamfor(json.dumps(utgava.get("responsibilityStatement", "")) + json.dumps(utgava.get("instanceOf", {}).get("contribution", []), ensure_ascii=False))
        if titel in titlar and (not efternamn or efternamn in ansvar):
            return plocka(utgava, int(bok["gr_id"]), "titel")
    return {"id": int(bok["gr_id"]), "m": "none"}


def main():
    berikning = json.loads(BERIKNING.read_text(encoding="utf-8")) if BERIKNING.exists() else []
    kanda = {str(p["id"]) for p in berikning}
    bocker = kartotek.las_bocker()
    nya = [b for b in bocker if b["gr_id"] not in kanda]

    for i, bok in enumerate(nya, 1):
        print(f"Libris {i}/{len(nya)}: {bok['titel']}")
        berikning.append(sla_upp(bok))
        time.sleep(PAUS)

    if nya:
        BERIKNING.write_text(json.dumps(berikning, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # Rapport över böcker som inte fått någon genre.
    katalog = kartotek.Katalog(ROT)
    saknas = [k for k in katalog.kort if k["sektion"] == "bocker" and not k["genre"]]
    RAPPORT.parent.mkdir(exist_ok=True)
    with RAPPORT.open("w", encoding="utf-8-sig", newline="") as f:
        f.write("goodreads_id;titel;forfattare;genre\n")
        for k in saknas:
            f.write(f"{k['gr_id']};{k['titel']};{k['upphov_text']};\n")
    print(f"{len(nya)} nya böcker slagna i Libris. {len(saknas)} saknar genre.")


if __name__ == "__main__":
    main()
