"""Datamodellen: läser exporterna och de egna filerna och bygger kort och lådor."""
import csv
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
DATA = ROT / "data"

SEKTIONER = {
    "bocker": "Böcker",
    "film": "Film",
    "tv-serier": "Tv-serier",
    "spel": "Spel",
}
SEKTION_FOR_TYP = {
    "Movie": "film", "TV Movie": "film", "Short": "film", "Video": "film",
    "TV Series": "tv-serier", "TV Mini Series": "tv-serier",
    "TV Episode": "tv-serier", "TV Special": "tv-serier",
    "Video Game": "spel",
}
TYP_SV = {
    "Movie": "Film", "TV Movie": "Tv-film", "Short": "Kortfilm", "Video": "Video",
    "TV Series": "Tv-serie", "TV Mini Series": "Miniserie",
    "TV Episode": "Tv-avsnitt", "TV Special": "Tv-special", "Video Game": "Spel",
}
GENRE_SV = {
    "Drama": "Drama", "Thriller": "Thriller", "Comedy": "Komedi", "Crime": "Kriminal",
    "Mystery": "Mysterium", "Action": "Action", "Adventure": "Äventyr",
    "Romance": "Romantik", "Sci-Fi": "Science fiction", "Biography": "Biografi",
    "Documentary": "Dokumentär", "Fantasy": "Fantasy", "History": "Historia",
    "War": "Krig", "Horror": "Skräck", "Music": "Musik", "Family": "Familj",
    "Animation": "Animation", "Film-Noir": "Film noir", "Western": "Western",
    "Sport": "Sport", "Short": "Kortfilm", "Musical": "Musikal", "News": "Nyheter",
    "Game-Show": "Frågesport", "Talk-Show": "Pratshow", "Reality-TV": "Dokusåpa",
    "Adult": "Vuxen",
}
# Dagar då många poster lades in på en gång (se UNDERLAG.md, avsnitt 5).
BULKDATUM = {
    "bocker": date(2021, 10, 16),
    "imdb": date(2012, 7, 10),
}
MANAD = ["JAN", "FEB", "MAR", "APR", "MAJ", "JUN", "JUL", "AUG", "SEP", "OKT", "NOV", "DEC"]
MANAD_LANG = ["januari", "februari", "mars", "april", "maj", "juni", "juli",
              "augusti", "september", "oktober", "november", "december"]
ARTIKLAR = re.compile(r"^(the|a|an|den|det|de|en|ett)\s+", re.I)
PARTIKLAR = {"de", "del", "della", "der", "di", "da", "du", "van", "von", "la", "le", "dos", "das"}
BINDNING = {"Kindle Edition": "E-bok", "ebook": "E-bok", "Audiobook": "Ljudbok", "Audible Audio": "Ljudbok"}


# ---------------------------------------------------------------- hjälpare

def laga(s):
    """Lagar dubbelkodad UTF-8 (t.ex. 'LindelÃ¶ws') och onödiga mellanslag."""
    s = (s or "").strip()
    if "Ã" in s or "Â" in s:
        try:
            s = s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return " ".join(s.split())


def slug(s):
    s = s.lower().replace("å", "a").replace("ä", "a").replace("ö", "o")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(t for t in s if not unicodedata.combining(t))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "x"


def sorteringsnyckel(s):
    """Svensk sortering med inledande artiklar borttagna."""
    s = ARTIKLAR.sub("", s.strip().strip("\"'«»“”‘’")).lower()
    s = s.replace("å", "ﾡ").replace("ä", "ﾢ").replace("ö", "ﾣ")
    s = s.replace("æ", "ﾢ").replace("ø", "ﾣ").replace("ü", "y")
    s = unicodedata.normalize("NFKD", s)
    return "".join(t for t in s if not unicodedata.combining(t))


def omvand(namn):
    """'Edgar G. Ulmer' → 'Ulmer, Edgar G.', 'Guillermo del Toro' → 'del Toro, Guillermo'."""
    delar = namn.split()
    if len(delar) < 2:
        return namn
    i = len(delar) - 1
    while i > 1 and delar[i - 1].lower() in PARTIKLAR:
        i -= 1
    if delar[-1].rstrip(".") in ("Jr", "Sr", "II", "III") and len(delar) > 2:
        return " ".join(delar[i - 1:-1]) + ", " + " ".join(delar[:i - 1]) + " " + delar[-1]
    return " ".join(delar[i:]) + ", " + " ".join(delar[:i])


def rak(namn_lf):
    """'Edlund, Mårten' → 'Mårten Edlund'."""
    if "," not in namn_lf:
        return namn_lf
    efter, for_ = namn_lf.split(",", 1)
    return f"{for_.strip()} {efter.strip()}"


def datum(s):
    m = re.match(r"(\d{4})[-/](\d{2})[-/](\d{2})", s or "")
    return date(int(m[1]), int(m[2]), int(m[3])) if m else None


def stampel(d, kalla):
    if not d:
        return ""
    if d == BULKDATUM.get(kalla):
        return f"INFÖRD FÖRE {MANAD[d.month - 1]} {d.year}"
    return f"INFÖRD {d.day} {MANAD[d.month - 1]} {d.year}"


def datum_text(d):
    return f"{d.day} {MANAD_LANG[d.month - 1]} {d.year}"


def ar(s):
    m = re.match(r"\s*(\d{3,4})", s or "")
    return int(m[1]) if m else None


def decennium(a):
    return f"{a // 10 * 10}-talet" if a else None


def las_csv(fil, avgransare=","):
    if not fil.exists():
        return []
    with fil.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=avgransare))


# ---------------------------------------------------------------- böcker

SERIE = re.compile(r"\s*\(([^()]*?),?\s*#\s*([\d.\-]+)\)\s*$")


def las_bocker():
    bocker = []
    for r in las_csv(DATA / "goodreads.csv"):
        if r["Exclusive Shelf"] != "read":
            continue
        if not r["Book Id"].isdigit():
            print(f"Varning: hoppar över Goodreads-raden med id {r['Book Id']!r}.")
            continue
        titel = laga(r["Title"])
        serie = serie_nr = ""
        m = SERIE.search(titel)
        if m:
            serie, serie_nr = m[1].strip(), m[2].lstrip("0") or "0"
            titel = titel[: m.start()].strip()
        titel = re.sub(r"\s*\((Swedish|English) Edition\)$", "", titel)
        huvud, under = titel, ""
        if re.search(r":\s", titel):
            huvud, under = [t.strip() for t in re.split(r"\s*:\s+", titel, 1)]
        forfattare = laga(r["Author"])
        okand = forfattare in ("Unknown Author", "")
        isbn = re.sub(r'[="\s]', "", r["ISBN"])
        isbn13 = re.sub(r'[="\s]', "", r["ISBN13"])
        bocker.append({
            "gr_id": r["Book Id"],
            "titel": huvud,
            "undertitel": under,
            "titel_kort": huvud,
            "serie": serie,
            "serie_nr": serie_nr,
            "forfattare": "" if okand else forfattare,
            "forfattare_lf": "" if okand else laga(r["Author l-f"]),
            "isbn": isbn,
            "isbn13": isbn13,
            "betyg": int(float(r["My Rating"] or 0)),
            "forlag": laga(r["Publisher"]),
            "ar_utgava": ar(r["Year Published"]),
            "ar_original": ar(r["Original Publication Year"]),
            "sidor": int(r["Number of Pages"]) if r["Number of Pages"].strip().isdigit() else None,
            "bindning": BINDNING.get(r["Binding"], ""),
            "inford": datum(r["Date Added"]),
        })
    return bocker


def bokgenre(bok, libris, manuellt):
    if bok["gr_id"] in manuellt:
        return [g.strip() for g in manuellt[bok["gr_id"]].split(",") if g.strip()]
    genrer = [g for g in (libris.get("g") or []) if g != "Skönlitteratur"]
    if genrer:
        return genrer
    kod = (libris.get("c") or "").split("=")[0]
    if kod.endswith(".016"):
        return ["Noveller"]
    if kod.endswith(".017"):
        return ["Kåserier"]
    if kod.endswith(".01"):
        return ["Romaner"]
    if bok["sidor"] and bok["sidor"] < 40:
        return ["Noveller"]
    return []


def originaltitel(libris, titel):
    o = (libris.get("o") or "").strip().rstrip(".").strip()
    if not o or o.lower() in ("noveller", "dikter", "berättelser", "essäer") or o.lower() == titel.lower():
        return ""
    return o


# ---------------------------------------------------------------- katalogen

class Katalog:
    def __init__(self, rot=ROT):
        self.rot = Path(rot)
        self.kort = []
        self.efter_id = {}
        self.lador = {}          # slug → låda
        self.grupper = {}        # slug → grupp (t.ex. bocker/forfattare)
        self.forlag = {r["fran"]: r["till"] for r in las_csv(DATA / "normalisering" / "forlag.csv", ";")}
        self.las_bocker()
        self.las_imdb()
        self.las_kopplingar()
        self.las_bilagor()
        self.bygg_lador()

    # -- kort

    def lagg_till(self, k):
        k["url"] = f"kort/{k['slug']}/"
        k.setdefault("kopplingar", [])
        k.setdefault("bilagor", [])
        k["lador"] = []
        self.kort.append(k)
        self.efter_id[k["id"]] = k

    def las_bocker(self):
        libris = {}
        fil = DATA / "libris_berikning.json"
        if fil.exists():
            libris = {str(p["id"]): p for p in json.loads(fil.read_text(encoding="utf-8"))}
        manuellt = {r["goodreads_id"].strip(): r["genre"] for r in las_csv(DATA / "genre_manuellt.csv", ";") if r.get("genre", "").strip()}
        for b in las_bocker():
            lb = libris.get(b["gr_id"], {})
            med_libris = lb.get("m") in ("isbn", "titel")
            oversattare = [laga(t) for t in lb.get("tr") or []] if lb.get("m") == "isbn" else []
            forlag = self.forlag.get(b["forlag"], b["forlag"])
            self.lagg_till({
                **b,
                "id": f"gr:{b['gr_id']}",
                "slug": f"gr{b['gr_id']}",
                "sektion": "bocker",
                "typ": "Bok",
                "typ_sv": "Bok",
                "sv_titel": "",
                "originaltitel": originaltitel(lb, b["titel"]),
                "upphov": [b["forfattare_lf"]] if b["forfattare_lf"] else [],
                "upphov_text": b["forfattare"],
                "oversattare": oversattare,
                "ar": b["ar_original"] or b["ar_utgava"] or ar(lb.get("y")),
                "forlag_norm": forlag,
                "genre": bokgenre(b, lb, manuellt),
                "skala": 5,
                "stampel": stampel(b["inford"], "bocker"),
                "libris": lb.get("m") if med_libris else "",
                "sortering": sorteringsnyckel(b["titel"]),
            })

    def las_imdb(self):
        for r in las_csv(DATA / "imdb.csv"):
            typ = r["Title Type"]
            sektion = SEKTION_FOR_TYP.get(typ)
            if not sektion:
                continue
            if not re.fullmatch(r"tt\d+", r["Const"]):
                print(f"Varning: hoppar över IMDb-raden med id {r['Const']!r}.")
                continue
            original = laga(r["Original Title"]) or laga(r["Title"])
            sv = laga(r["Title"])
            regi = [laga(d) for d in r["Directors"].split(",") if d.strip()]
            genrer = [GENRE_SV.get(g.strip(), g.strip()) for g in r["Genres"].split(",") if g.strip()]
            inford = datum(r["Date Rated"])
            self.lagg_till({
                "id": f"imdb:{r['Const']}",
                "slug": r["Const"],
                "const": r["Const"],
                "sektion": sektion,
                "typ": typ,
                "typ_sv": TYP_SV.get(typ, typ),
                "titel": original,
                "undertitel": "",
                "sv_titel": sv if sv != original else "",
                "originaltitel": "",
                "upphov": [omvand(d) for d in regi],
                "upphov_text": ", ".join(regi),
                "regi": regi,
                "oversattare": [],
                "ar": ar(r["Year"]),
                "minuter": int(r["Runtime (mins)"]) if r["Runtime (mins)"].strip().isdigit() else None,
                "genre": genrer,
                "betyg": int(r["Your Rating"] or 0),
                "skala": 10,
                "inford": inford,
                "stampel": stampel(inford, "imdb"),
                "sortering": sorteringsnyckel(original),
            })
        self.koppla_avsnitt()

    def koppla_avsnitt(self):
        """Tv-avsnitt får egna kort men pekar på sin serie när serien finns i exporten."""
        serier = {}
        for k in self.kort:
            if k["typ"] in ("TV Series", "TV Mini Series"):
                serier.setdefault(slug(k["titel"]), k)
                if k["sv_titel"]:
                    serier.setdefault(slug(k["sv_titel"]), k)
        for k in self.kort:
            if k["typ"] != "TV Episode" or ": " not in k["titel"]:
                continue
            serie, avsnitt = k["titel"].split(": ", 1)
            k["serie"], k["avsnitt"] = serie, avsnitt
            hit = serier.get(slug(serie))
            if not hit and k["sv_titel"] and ": " in k["sv_titel"]:
                hit = serier.get(slug(k["sv_titel"].split(": ", 1)[0]))
            if hit:
                k["serie_id"] = hit["id"]
                hit.setdefault("avsnitt_ids", []).append(k["id"])

    def las_kopplingar(self):
        for r in las_csv(DATA / "kopplingar.csv", ";"):
            bok = self.efter_id.get(f"gr:{r['goodreads_id'].strip()}")
            film = self.efter_id.get(f"imdb:{r['imdb_id'].strip()}")
            if not bok or not film:
                print(f"Varning: kopplingen {r['goodreads_id']} ↔ {r['imdb_id']} pekar på ett kort som saknas.")
                continue
            typ = r.get("typ", "").strip() or "filmatisering"
            bok["kopplingar"].append((film["id"], typ))
            film["kopplingar"].append((bok["id"], typ))

    def las_bilagor(self):
        """bilagor/<kortets slug>/*.md, med en enkel rubrik överst:

            ---
            typ: citat
            bild: bild.jpg
            ---
            Text …
        """
        mapp = self.rot / "bilagor"
        if not mapp.exists():
            return
        efter_slug = {k["slug"]: k for k in self.kort}
        for kortmapp in sorted(p for p in mapp.iterdir() if p.is_dir()):
            k = efter_slug.get(kortmapp.name)
            if not k:
                print(f"Varning: bilagor/{kortmapp.name} motsvarar inget kort.")
                continue
            for fil in sorted(kortmapp.glob("*.md")):
                text = fil.read_text(encoding="utf-8")
                meta = {}
                m = re.match(r"---\s*\n(.*?)\n---\s*\n?", text, re.S)
                if m:
                    for rad in m[1].splitlines():
                        if ":" in rad:
                            nyckel, varde = rad.split(":", 1)
                            meta[nyckel.strip()] = varde.strip()
                    text = text[m.end():]
                k["bilagor"].append({
                    "typ": meta.get("typ", "reflektion"),
                    "bild": meta.get("bild", ""),
                    "text": text.strip(),
                    "mapp": kortmapp,
                })

    # -- lådor

    def lada(self, slug_, sektion, grupp, namn, sortering, ordning=None):
        if slug_ not in self.lador:
            self.lador[slug_] = {
                "slug": slug_, "url": slug_ + "/", "sektion": sektion, "grupp": grupp,
                "namn": namn, "kort": [], "sortering": sortering,
                "ordning": ordning if ordning is not None else sorteringsnyckel(namn),
            }
        return self.lador[slug_]

    def grupp(self, slug_, sektion, namn, kort_namn=None, ordna="namn"):
        self.grupper.setdefault(slug_, {
            "slug": slug_, "url": slug_ + "/", "sektion": sektion, "namn": namn,
            "kort_namn": kort_namn or namn, "ordna": ordna,
        })
        return slug_

    def i_lada(self, k, slug_, *args, **kw):
        lada = self.lada(slug_, *args, **kw)
        if k["id"] not in lada["kort"]:
            lada["kort"].append(k["id"])
            k["lador"].append(slug_)

    def bygg_lador(self):
        unika = defaultdict(dict)   # undviker att två namn får samma slug

        def unik_slug(grupp, namn):
            bas = slug(namn)
            if unika[grupp].get(bas, namn) != namn:
                n = 2
                while f"{bas}-{n}" in unika[grupp] and unika[grupp][f"{bas}-{n}"] != namn:
                    n += 1
                bas = f"{bas}-{n}"
            unika[grupp][bas] = namn
            return f"{grupp}/{bas}"

        for s, namn in SEKTIONER.items():
            self.lada(s, s, None, f"Alla {namn.lower()}" if s != "spel" else "Spel",
                      "y" if s == "bocker" else "r")

        g_forf = self.grupp("bocker/forfattare", "bocker", "Författare", "Alla författare")
        g_overs = self.grupp("bocker/oversattare", "bocker", "Översättare", "Alla översättare")
        g_utg = self.grupp("bocker/utgiven", "bocker", "Först utgiven", "Alla decennier", "tid")
        g_bgenre = self.grupp("bocker/genre", "bocker", "Genre", "Alla genrer", "antal")
        g_forlag = self.grupp("bocker/forlag", "bocker", "Förlag")
        g_bbetyg = self.grupp("bocker/betyg", "bocker", "Betyg 1–5", ordna="betyg")

        for k in self.kort:
            s = k["sektion"]
            self.i_lada(k, s, s, None, "", "")
            maxbetyg = k["betyg"] == k["skala"]
            if maxbetyg:
                self.i_lada(k, "hogsta-betyg", None, None, "Högsta betyg", "r")

            if s == "bocker":
                for f in k["upphov"]:
                    self.i_lada(k, unik_slug(g_forf, f), s, g_forf, f, "y")
                for o in k["oversattare"]:
                    self.i_lada(k, unik_slug(g_overs, o), s, g_overs, o, "y")
                if k["ar"]:
                    d = decennium(k["ar"])
                    self.i_lada(k, f"{g_utg}/{slug(d)}", s, g_utg, d, "y", ordning=k["ar"] // 10)
                for g in k["genre"]:
                    self.i_lada(k, unik_slug(g_bgenre, g), s, g_bgenre, g, "y")
                if k["forlag_norm"]:
                    self.i_lada(k, unik_slug(g_forlag, k["forlag_norm"]), s, g_forlag, k["forlag_norm"], "y")
                if k["betyg"]:
                    self.i_lada(k, f"{g_bbetyg}/{k['betyg']}", s, g_bbetyg, f"Betyg {k['betyg']}", "t", ordning=-k["betyg"])
                if k["kopplingar"]:
                    self.i_lada(k, "bocker/filmatiseringar", s, None, "Filmatiseringar", "y")
                continue

            if s == "spel":
                continue

            g_dec = self.grupp(f"{s}/decennium", s, "Decennium", "Alla decennier", "tid")
            g_genre = self.grupp(f"{s}/genre", s, "Genre", "Alla genrer", "antal")
            g_betyg = self.grupp(f"{s}/betyg", s, "Betyg 1–10", ordna="betyg")
            if k["ar"]:
                d = decennium(k["ar"])
                self.i_lada(k, f"{g_dec}/{slug(d)}", s, g_dec, d, "r", ordning=k["ar"] // 10)
            for g in k["genre"]:
                self.i_lada(k, unik_slug(g_genre, g), s, g_genre, g, "r")
            if k["betyg"]:
                self.i_lada(k, f"{g_betyg}/{k['betyg']}", s, g_betyg, f"Betyg {k['betyg']}", "t", ordning=-k["betyg"])
            if s == "film":
                g_regi = self.grupp("film/regissor", s, "Regissörer A–Ö", "Regissörer A–Ö")
                for r in k["upphov"]:
                    self.i_lada(k, unik_slug(g_regi, r), s, g_regi, r, "y")
            if k["kopplingar"]:
                self.i_lada(k, f"{s}/filmatiseringar", s, None, "Filmatiseringar", "y")

        # Kortets hemlåda: där det hör hemma i sökvägen och där föregående/nästa hämtas.
        for k in self.kort:
            s = k["sektion"]
            if s == "bocker":
                hem = next((l for l in k["lador"] if l.startswith("bocker/forfattare/")), s)
            elif s == "spel":
                hem = s
            else:
                hem = next((l for l in k["lador"] if l.startswith(f"{s}/decennium/")), s)
            k["hem"] = hem

        for lada in self.lador.values():
            lada["kort"] = self.sortera([self.efter_id[i] for i in lada["kort"]], lada["sortering"])

    def sortera(self, kort, hur):
        if hur == "y":
            return sorted(kort, key=lambda k: (k["ar"] or 9999, k["sortering"]))
        if hur == "r":
            return sorted(kort, key=lambda k: (-k["betyg"] / k["skala"], k["sortering"]))
        return sorted(kort, key=lambda k: k["sortering"])

    def lador_i_grupp(self, grupp):
        lador = [l for l in self.lador.values() if l["grupp"] == grupp]
        hur = self.grupper[grupp]["ordna"]
        if hur == "antal":
            return sorted(lador, key=lambda l: (-len(l["kort"]), l["ordning"]))
        return sorted(lador, key=lambda l: l["ordning"])

    # -- siffror till startsidan

    def siffror(self):
        per = {s: sum(1 for k in self.kort if k["sektion"] == s) for s in SEKTIONER}
        imdb = [k["betyg"] for k in self.kort if k["skala"] == 10 and k["betyg"]]
        bok = [k["betyg"] for k in self.kort if k["skala"] == 5 and k["betyg"]]
        tal = lambda n: f"{n:,}".replace(",", " ")
        dec = lambda x: f"{x:.1f}".replace(".", ",")
        return {
            "kort": tal(len(self.kort)),
            "bocker": tal(per["bocker"]),
            "film": tal(per["film"]),
            "tv": tal(per["tv-serier"]),
            "spel": tal(per["spel"]),
            "hogsta": tal(len(self.lador.get("hogsta-betyg", {"kort": []})["kort"])),
            "tior": tal(sum(1 for b in imdb if b == 10)),
            "femmor": tal(sum(1 for b in bok if b == 5)),
            "snitt_film": dec(sum(imdb) / len(imdb)) if imdb else "–",
            "snitt_bok": dec(sum(bok) / len(bok)) if bok else "–",
            "vanligast_film": str(max(set(imdb), key=imdb.count)) if imdb else "–",
            "vanligast_bok": str(max(set(bok), key=bok.count)) if bok else "–",
        }
