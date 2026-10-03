# Arbetsläge – 3 oktober 2026

## Filer

| Fil | Vad den gör |
|---|---|
| `UNDERLAG.md` | Underlaget för bygget |
| `data/` | Exporter och egna filer (se UNDERLAG.md, avsnitt 2) |
| `data/normalisering/forlag.csv` | Normalisering av förlagsnamn (`fran;till`). Ny i dag |
| `data/kopplingar.csv` | 20 kopplingar. Två nya i dag: Cathedral och Grannar ↔ Short Cuts |
| `bygg/kartotek.py` | Datamodellen: läser och rensar exporterna och bygger kort, lådor och kopplingar |
| `bygg/sidor.py` | HTML-mallar för startsida, låda, grupp (t.ex. alla författare), kort, sök och 404 |
| `bygg/bygg.py` | Bygger sajten till `_site/` och skriver sökindexet `sok.json` |
| `bygg/lankkoll.py` | Kontrollerar alla interna länkar i `_site/` |
| `bygg/libris.py` | Slår upp nya böcker i Libris och skriver `rapport/att_fylla_i.csv` |
| `statiskt/stil.css` | Det visuella systemet "Manila" |
| `statiskt/kartotek.js` | Sortering, "Bläddra vidare", sökning och kort på måfå. Sajten fungerar utan skriptet |
| `statiskt/ikon.svg` | Flikikon |
| `statiskt/typsnitt/` | Spectral 400/600 och Courier Prime 400 (latin och latin-ext) med licenserna. Inga anrop till Google Fonts |
| `texter/startsida.md` | Rubrik, ingress, "Om betygen" och beskrivning. Siffror inom `{}` fylls i vid bygget |
| `.github/workflows/bygg.yml` | GitHub Actions med bara GitHubs egna actions: Libris, bygge, länkkontroll och publicering på Pages |

`_site/` byggs om varje gång och ligger inte i git.

## Bygga och förhandsgranska

```bash
python bygg/bygg.py
```

```bash
python -m http.server 8123 --directory _site
```

Öppna sedan http://localhost:8123/. Bara Pythons standardbibliotek behövs, och bygget tar ungefär 5 sekunder.

`python bygg/libris.py` slår upp böcker som saknas i `libris_berikning.json`. I dag saknas inga, så skriptet gör inga anrop. Det har inte körts i sin helhet mot Libris. Bara själva uppslagningen är provad, mot ett ISBN.

## Klart

- Alla sidor i underlaget: startsida, sektioner, lådor, grupper, katalogkort, sök, kort på måfå och 404.
- Lådorna: Böcker (författare, översättare, först utgiven, genre, förlag, betyg, filmatiseringar), Film (decennium, genre, regissör, betyg, filmatiseringar), Tv-serier (decennium, genre, betyg, filmatiseringar), Spel och Högsta betyg (48 kort).
- Datafällorna i avsnitt 5: rensat ISBN, utbrutna serienamn, lagad dubbelkodning (LindelÃ¶ws), stämpeln "INFÖRD FÖRE …" för bulkdatumen och översättare bara från Libris. Översättare visas bara vid ISBN-träff, eftersom en titelträff kan gälla en annan översättning.
- Bilagor läses från `bilagor/<slug>/*.md`, där slug är t.ex. `gr26902092` eller `tt0037101`. Mappen finns inte än.
- De sex besluten i avsnitt 13:
  - Namnet är Kartoteket.
  - Tv-avsnitten får egna kort som länkar till sin serie när serien finns i exporten (fungerar för 18 av 32).
  - IMDb:s snittbetyg visas inte.
  - Stämpeln för bulkdatumen är "INFÖRD FÖRE OKT 2021" respektive "INFÖRD FÖRE JUL 2012".
  - Startsidans texter är utkast i `texter/startsida.md`.
  - Ingen egen domän ännu. En fil `CNAME` i roten följer med till sajten om den läggs dit.

## Inför publiceringen

- **Behörigheter:** workflowet har ingen behörighet som standard. Byggjobbet får bara läsa repot, och publiceringsjobbet får bara `pages: write` och `id-token: write`.
- **Libris:** eftersom inget jobb får skriva till repot sparas Libris-uppslagningen inte där, till skillnad från vad UNDERLAG.md, avsnitt 12, beskriver. Nya böcker slås upp vid varje bygge.
  - Listan över böcker utan genre syns i körningens sammanfattning under Actions.
  - Den uppdaterade `libris_berikning.json` kan laddas ner som artefakten `libris-och-rapport` och läggas in för hand.
- **Escaping:** all text och alla URL:er escapas i mallarna. Sökresultaten byggs med `createElement` och `textContent`, utan `innerHTML`. Id:n som inte ser ut som `tt123…` eller som är rena siffror hoppas över vid bygget.
- **Rensat:** den privata länken till designytan är borttagen ur UNDERLAG.md. Historiken är omskriven, så att varken länken eller den gamla författaruppgiften finns kvar i någon commit.

## Mobilfixen

Problemen: på smala skärmar hamnade stämpeln över kortets rostlinje, betygsrutan tog en egen rad i lådorna, och sökfältet på söksidan fick ett stort tomrum under sig (`flex-basis` verkade på höjden).

Rättat i `statiskt/stil.css` och `bygg/sidor.py`:
- Rostlinjerna är nu en kant på kortets huvud och ett nytt omslag, `.kort-falt`, så de följer innehållet.
- Lådraderna är ett rutnät på mobil.
- Söksidans formulär har `flex: none`.

Kort, lådor och söksidan har kontrollerats i 375 px bredd.

## Kommandon som inte gick som tänkt

- Det första bygget kördes med `du -sh _site` efteråt. Själva bygget tog 5 sekunder, men storleksmätningen över 4 400 filer på Windows drog över gränsen på 2 minuter. Kommandot flyttades till bakgrunden och blev klart där. Skippa `du` eller mät en enda fil.
- `preview_start` med namnet `kartoteket` hittade inte `.claude/launch.json`, eftersom verktyget letade i sessionens ursprungliga arbetsmapp. Lösningen blev att starta `http.server` för hand och öppna adressen direkt.
- Länkkontrollen är nu skriptet `bygg/lankkoll.py`. Det slår upp länkarna i en mängd med de byggda filerna och hittade 4 459 unika länkmål och 0 trasiga. Första körningen direkt efter ett bygge tog 2 minuter, och en andra körning tog 1 sekund. Det som tar tid är alltså första läsningen av nyskrivna filer, troligen för att antivirusprogrammet skannar dem, inte själva skriptet. Kör det med `timeout` eller i bakgrunden direkt efter ett bygge.

## Återstår

1. Kör `bygg/libris.py` på riktigt när en ny bok har tillkommit.
2. Pusha till github.com/RaoulDukeED/kartoteket och slå på Pages med källan "GitHub Actions" (Settings › Pages). Workflowet är oprövat.
3. Läs igenom och skriv om texterna i `texter/startsida.md`.
4. Kontrollera kopplingen Den röda anteckningsboken ↔ Smoke, om "Auggie Wren's Christmas Story" ingår i den svenska utgåvan.
