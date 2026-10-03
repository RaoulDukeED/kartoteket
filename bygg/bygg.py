"""Bygger Kartoteket till mappen _site/.

    python bygg/bygg.py

Miljövariabeln KARTOTEK_BAS anger sajtens sökväg på servern (t.ex. "/kartoteket/").
Den används bara av 404-sidan, alla andra länkar är relativa.
"""
import json
import os
import re
import shutil
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kartotek  # noqa: E402
import sidor  # noqa: E402

ROT = kartotek.ROT
UT = ROT / "_site"
STATISKT = ROT / "statiskt"
ORD = {1: "etta", 2: "tvåa", 3: "trea", 4: "fyra", 5: "femma", 6: "sexa", 7: "sjua", 8: "åtta", 9: "nia", 10: "tia"}


def skriv(sokvag, text):
    fil = UT / sokvag
    fil.parent.mkdir(parents=True, exist_ok=True)
    fil.write_text(text, encoding="utf-8")


def las_texter(K):
    """texter/startsida.md: stycken under ## rubriker, med siffror ifyllda."""
    fil = ROT / "texter" / "startsida.md"
    delar = {}
    aktuell = None
    for rad in fil.read_text(encoding="utf-8").splitlines():
        m = re.match(r"##\s+(.+)", rad)
        if m:
            aktuell = m[1].strip().lower()
            delar[aktuell] = []
        elif aktuell:
            delar[aktuell].append(rad)
    siffror = K.siffror()
    siffror["vanligast_film_ord"] = ORD.get(int(siffror["vanligast_film"]), siffror["vanligast_film"]) if siffror["vanligast_film"].isdigit() else "–"
    siffror["vanligast_bok_ord"] = ORD.get(int(siffror["vanligast_bok"]), siffror["vanligast_bok"]) if siffror["vanligast_bok"].isdigit() else "–"

    def fyll(text):
        return re.sub(r"\{(\w+)\}", lambda m: siffror.get(m[1], m[0]), text)

    def stycken(namn):
        text = fyll("\n".join(delar.get(namn, [])).strip())
        return "".join(f"<p>{escape(p.strip())}</p>" for p in re.split(r"\n\s*\n", text) if p.strip())

    return {
        "rubrik": fyll("\n".join(delar.get("rubrik", ["Läst och sett"])).strip()) or "Läst och sett",
        "ingress": stycken("ingress"),
        "om betygen": stycken("om betygen"),
        "beskrivning": fyll(" ".join(delar.get("beskrivning", [])).strip()),
    }


def sokindex(K):
    poster = []
    for k in K.kort:
        under = k["originaltitel"] if k["sektion"] == "bocker" else k["sv_titel"]
        post = {"u": k["url"], "t": k["titel"], "k": k["typ_sv"], "r": k["betyg"], "x": k["skala"]}
        if under:
            post["s"] = under
        if k["upphov_text"]:
            post["a"] = k["upphov_text"]
        if k["ar"]:
            post["y"] = k["ar"]
        extra = [kartotek.rak(o) for o in k["oversattare"]] + ([k["serie"]] if k.get("serie") else [])
        if extra:
            post["o"] = " ".join(extra)
        if k["genre"]:
            post["g"] = ", ".join(g.lower() for g in k["genre"])
        # Upphovet till kopplade verk, så att "chandler" också hittar filmatiseringarna.
        kopplade = []
        for annat_id, _ in k["kopplingar"]:
            a = K.efter_id[annat_id]
            kopplade += [a["upphov_text"]] + a["upphov"]
        kopplade = [x for x in dict.fromkeys(kopplade) if x]
        if kopplade:
            post["c"] = " ".join(kopplade)
        poster.append(post)
    return json.dumps(poster, ensure_ascii=False, separators=(",", ":"))


def main():
    K = kartotek.Katalog()
    uppdaterad = date.today()
    bas = os.environ.get("KARTOTEK_BAS", "/")
    if not bas.endswith("/"):
        bas += "/"

    if UT.exists():
        shutil.rmtree(UT)
    UT.mkdir()

    shutil.copytree(STATISKT, UT, dirs_exist_ok=True)
    (UT / ".nojekyll").write_text("", encoding="utf-8")
    if (ROT / "CNAME").exists():
        shutil.copy(ROT / "CNAME", UT / "CNAME")

    texter = las_texter(K)
    # Kortet som "Dra ett kort på måfå" leder till utan javascript byts varje byggdag.
    reserv = K.kort[uppdaterad.toordinal() % len(K.kort)]["url"]
    skriv("index.html", sidor.start_sida(K, texter, uppdaterad, reserv))
    skriv("sok/index.html", sidor.sok_sida(uppdaterad, reserv))
    skriv("404.html", sidor.saknas_sida(uppdaterad, bas))
    skriv("sok.json", sokindex(K))

    for lada in K.lador.values():
        skriv(f"{lada['slug']}/index.html", sidor.lada_sida(K, lada, uppdaterad))
    for grupp in K.grupper:
        skriv(f"{grupp}/index.html", sidor.grupp_sida(K, grupp, uppdaterad))
    for k in K.kort:
        skriv(f"{k['url']}index.html", sidor.kort_sida(K, k, uppdaterad))
        for b in k["bilagor"]:
            if b["bild"] and (b["mapp"] / b["bild"]).exists():
                shutil.copy(b["mapp"] / b["bild"], UT / k["url"] / b["bild"])

    sidantal = sum(1 for _ in UT.rglob("*.html"))
    print(f"Klart: {len(K.kort)} kort, {len(K.lador)} lådor, {sidantal} sidor i {UT.relative_to(ROT)}/.")


if __name__ == "__main__":
    main()
