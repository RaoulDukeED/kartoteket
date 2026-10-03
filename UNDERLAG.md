# Kartoteket – underlag för bygget

En publik, personlig katalog över allt jag läst och sett: böcker, filmer, tv-serier och spel. Den är ordnad som ett gammalt bibliotekskartotek med lådor och kort. Allt bygger på mina egna betyg från Goodreads och IMDb. Sajten ska vara enkel att uppdatera: ny export in, sajten byggs om.

Arbetsnamn: **Kartoteket**. Designskisser finns på ytan *Katalogkortet* i Claude.

---

## 1. Grundprinciper

- **En låda är ett urval, inte en plats.** Samma kort ligger samtidigt i 1940-talet, Film noir och Högsta betyg.
- **Inget flöde.** Ingen lista över det senaste och ingen tidslinje. Man kommer in via lådorna, sökningen eller *Dra ett kort på måfå* och följer sedan ”Se även”.
- **Katalogpraxis.** Böcker katalogiseras under författaren och filmer under titeln. Huvuduppslaget är den version jag mötte: för böcker utgåvans titel med originaltiteln under, för filmer originaltiteln med den svenska titeln under.
- **Inga omslag eller affischer.** Kortet är bilden.
- **Exporterna ersätts alltid i sin helhet.** Det jag skriver själv ligger i egna filer, nycklat på id, och skrivs aldrig över.

## 2. Datakällor

| Fil | Källa | Hur den uppdateras |
|---|---|---|
| `data/goodreads.csv` | Goodreads-export (My Books › Import and Export) | Ersätts helt |
| `data/imdb.csv` | IMDb-export (Your Ratings › Export) | Ersätts helt |
| `data/libris_berikning.json` | Libris, slagen per bok | Kompletteras automatiskt för nya böcker |
| `data/genre_manuellt.csv` | Mina egna genreval | För hand |
| `data/kopplingar.csv` | Bok ↔ film | För hand |
| `bilagor/` (senare) | Citat, reflektioner, bilder per kort | För hand |

**Företräde:** manuellt › Libris › export.

Läget den 3 oktober 2026: 189 lästa böcker och 2 590 IMDb-poster. Alla 189 böcker har genre via Libris eller `genre_manuellt.csv`. `kopplingar.csv` har 18 kopplingar som startlista.

## 3. Sektioner

| Sektion | Innehåll | Antal |
|---|---|---|
| Böcker | Goodreads, hyllan *read* (to-read och currently-reading visas inte) | 189 |
| Film | IMDb: Movie, TV Movie, Short, Video | 2 140 |
| Tv-serier | IMDb: TV Series, TV Mini Series, TV Episode, TV Special | 442 |
| Spel | IMDb: Video Game | 8 |

Tvärgående låda: **Högsta betyg**, med alla tior och femmor (23 + 25 = 48 kort).

## 4. Datamodell

Varje kort har ett stabilt id som aldrig ändras mellan exporter:
- bok: `gr:<Book Id>`, till exempel `gr:26902092`
- film, tv eller spel: `imdb:<Const>`, till exempel `imdb:tt0037101`

Fält per kort:

```
id, sektion, typ (Movie, TV Series …)
titel            – bok: utgåvans titel · film: originaltitel
sv_titel         – film: IMDb "Title" om den skiljer sig från originaltiteln
originaltitel    – bok: från Libris (translationOf)
upphov           – bok: författare (Efternamn, Förnamn) · film: regissör(er)
oversattare[]    – bok: från Libris
ar_original      – bok: Original Publication Year · film: Year
utgava           – bok: förlag och år (Publisher, Year Published) och sidor
genre[]          – bok: manuellt › Libris · film: IMDb Genres översatta till svenska
betyg, skala     – 1–5 för böcker, 1–10 för övriga
inford           – bok: Date Added · film: Date Rated
isbn             – rensat från Excel-formatet ="…"
lador[]          – beräknas
kopplingar[]     – från kopplingar.csv, åt båda hållen
bilagor[]        – senare
```

## 5. Kända datafällor

- **Goodreads Date Read** är tomt för nästan alla böcker, och 53 böcker lades in samma dag (16 okt 2021). Därför går det inte att göra någon tidslinje över läsandet.
- **IMDb**: 289 betyg har datumet 10 juli 2012, troligen en import. *Förslag:* stämpeln visar ”Införd före juli 2012” för dem, och på motsvarande sätt ”Införd före okt 2021” för bulkimporten i Goodreads.
- **ISBN** i Goodreads ligger som `="9100452734"`. Ta bort `=` och citattecknen.
- **Additional Authors** i Goodreads blandar översättare, illustratörer, uppläsare och förordsskribenter. Använd den inte som översättare. Översättare kommer från Libris.
- **Förlagsnamn** stavas olika (Bonnier, Bonniers, Albert Bonniers Förlag, Aldus/Bonniers). Använd en normaliseringstabell, `data/normalisering/forlag.csv`.
- **Serienamn** står i titeln, till exempel `(Philip Marlowe, #5)`. Bryt ut dem till ett eget fält.
- **IMDb Directors** saknas för 403 poster, mest tv.
- **Libris-träffar på titel** (31 böcker) kan gälla en annan utgåva än den jag läste. Genre och originaltitel gäller verket, men översättaren kan skilja sig åt om boken översatts flera gånger.

IMDb-genrer på svenska: Drama, Thriller, Komedi (Comedy), Kriminal (Crime), Mysterium (Mystery), Action, Äventyr (Adventure), Romantik (Romance), Science fiction (Sci-Fi), Biografi, Dokumentär, Fantasy, Historia, Krig (War), Skräck (Horror), Musik, Familj, Animation, Film noir (Film-Noir), Western, Sport, Kortfilm (Short), Musikal, Nyheter (News), Frågesport (Game-Show).

## 6. Lådor och sortering

**Böcker:** Författare · Översättare · Först utgiven (decennium) · Genre · Förlag · Betyg 1–5 · Filmatiseringar
**Film:** Decennium · Genre · Regissör · Betyg 1–10 · Filmatiseringar
**Tv-serier:** Decennium · Genre · Betyg
**Spel:** en enda låda
**Tvärgående:** Högsta betyg

Varje låda visar antal kort. Sortering sker efter titel, år (originalår för böcker) eller betyg. Vid sortering på titel ignoreras inledande artiklar: The, A, An, Den, Det, De, En och Ett. Använd svensk sortering, `localeCompare(…, 'sv')`.

## 7. Sidor

1. **Startsida.** Rubrik (”Läst och sett”), en kort ingress, sökfält, katalogskåpet med fyra lådfronter (Böcker, Film, Tv-serier, Spel med antal), lådan Högsta betyg, knappen *Dra ett kort på måfå* och en kort text om betygen. Texterna skriver jag själv.
2. **Låda.** Sökväg, rubrik och antal kort. En sidokolumn med andra lådor och de val som går att filtrera på. Sorteringsknappar. Själva lådan visar kortens överkant: titel, svensk titel eller originaltitel, år och upphov, betyg samt markeringar (↔ bok/film, gem för bilagor).
3. **Kort.** Hela katalogkortet, en plats för bilagor (manilalapp med gem) och navigering till föregående och nästa kort i lådan samt *Dra ett kort på måfå*.

Layouten är responsiv. Innehållet är som bredast 1120 px med 24 px marginal. Sidokolumnen staplas ovanför lådan på smala skärmar. Kortraderna bryts.

## 8. Katalogkortet

**Filmkort**
```
FILM, tt0037101                         [INFÖRD 4 SEP 2024]
─────────────────────────────────────────────── (rostlinje)
MURDER, MY SWEET                        (rubrik, versaler)
Dmytryk, Edward.
    Murder, My Sweet / regi Edward Dmytryk. – 1944. – 95 min.
    Sv. titel: Mord, min älskling!
Genre: film noir, kriminal, mysterium.
Betyg: [8] av 10
Se även: Bok: Chandler, Raymond. Mord min älskling. – 1940.
         Lådor: 1940-talet (41), Film noir (52).
1. Film noir. 2. Chandler, Raymond – filmatiseringar.
```

**Bokkort**
```
BOK, ISBN 91-0-045273-4                 [INFÖRD 7 OKT 2024]
CHANDLER, RAYMOND                       (rubrik = författaren)
    Mord min älskling / Raymond Chandler ; övers. av Mårten Edlund.
    – Bonnier, 1981. – 212 s.
    Originaltitel: Farewell, my lovely. Först utgiven 1940.
Genre: romaner, deckare.
Betyg: [5] av 5
Se även: Filmatiseringar: Murder, My Sweet (1944) 8 av 10;
         Farewell, My Lovely (1975) 8 av 10.
1. Chandler, Raymond. 2. Edlund, Mårten, övers.
Uppgifter från Libris.
```

Tior och femmor har betygsrutan i rost. Stämpeln visar införd-datumet.

## 9. Visuellt system – ”Manila”

| Roll | Färg |
|---|---|
| Duk (bakgrund, 60 %) | `#E9E5DD` |
| Låda och skåpsfronter, manila (30 %) | `#D9C7A3` |
| Kort | `#FBF9F4` |
| Bläck, sepiasvart | `#2B2622` |
| Dämpad text | `#655D55` (på manila `#4A433C`) |
| Rost, fyllning: knappar och kortlinje | `#B4561F` |
| Rost, text: länkar, aktiv navigering, tior | `#9A4416` (hover `#7A3510`) |
| Hårlinje | `rgba(43,38,34,0.12)` |
| Fokus | 2 px `#B4561F`, offset 2 px |

Kontrasten mot respektive bakgrund är kontrollerad till minst 4,5:1. Vit text på `#B4561F` ger 4,9:1.

**Typografi**
- Spectral 400/600 för all text utanför korten. Brödtext 16–18 px, sekundär text 14–15 px, meta 12 px (bara meta), rubriker 44–52 px med radavstånd 1,1.
- Courier Prime 400 för korten och kortkanterna, i en enda vikt. Betoning görs med rosten, inte med fetstil.
- Inga versaler i gränssnittet. Versaler förekommer bara på kortets rubrik och på stämpeln.

**Ytor**
- Lådor och fronter: manila, 1 px kant och en svag inre ljuskant upptill.
- Kort: 1 px kant och mjuk skugga med högst 0,06 i styrka. Inga hårda skuggor.

**Regler** (från designskillsen): en enda accentfärg, fördelningen 60-30-10, inga mittpunkter som avgränsare, inga pilar efter länktexter, inga piller runt statisk metadata, klickytor på minst 44 px, synlig tangentbordsfokus och `aria-current` på aktiv låda och avdelning. Undvik krämvit bakgrund med seriff och tegelröd accent, som är en typisk AI-klyscha. Det är manilatonen som bär identiteten.

## 10. Bilagor (förberett, inte i version 1)

- Filer i `bilagor/<kort-id>/` (markdown med typen citat, reflektion eller bild, plus eventuella bilder).
- Visas som en manilalapp fäst med gem bakom kortet. I lådan markeras kortet med en gemikon.
- Citat hålls korta och kommenteras alltid. Inga sångtexter.

## 11. Libris-berikning

- Slagning: `https://libris.kb.se/find.jsonld?q=<ISBN>`. Utan ISBN söks titel och författare, med normaliserad jämförelse av titel och efternamn.
- Svaret innehåller både bestånd (`Item`) och utgåvor. Ta poster med `instanceOf` eller `itemOf.instanceOf`, och välj den vars `identifiedBy` innehåller ISBN-numret.
- Fält:
  - genre/form: `instanceOf.category` där `@id` innehåller `/term/saogf/`. Filtrera bort mediatermer: Talböcker, Ljudböcker, E-böcker.
  - översättare: `instanceOf.contribution` med rollen translator.
  - originaltitel: `instanceOf.translationOf[].hasTitle[].mainTitle`.
  - klassifikation: `instanceOf.classification`, schema `kssb`.
  - fullständig upphovsuppgift: `responsibilityStatement`.
- Reservregler när genre saknas, verifierade på mina data:
  - KSSB-kod som slutar på `.01` → Romaner (51 av 51)
  - `.016` → Noveller (36 av 36)
  - `.017` → Kåserier
  - under 40 sidor → Noveller
- Libris begränsar antalet anrop. Kör slagningarna en i taget med 0,7 s mellanrum. Om svaret är HTML i stället för JSON, vänta 3, 6, 9 och 12 s och försök igen.
- Slå bara upp böcker som saknas i `libris_berikning.json`. Det som fortfarande saknar genre skrivs till `rapport/att_fylla_i.csv`.

## 12. Uppdateringsflöde

1. Exportera från Goodreads och IMDb.
2. Dra in filerna i `data/` på github.com, med samma namn som tidigare, och spara.
3. GitHub Actions kör bygget: läser data, berikar nya böcker via Libris, genererar sajten och publicerar på GitHub Pages.
4. Om nya böcker saknar genre syns de i `rapport/att_fylla_i.csv`. Fyll i dem i `genre_manuellt.csv`.

Ingen terminal behövs för uppdateringar.

**Förslag på teknik:** ett byggskript i Python eller Node som genererar statiska HTML-sidor per låda och per kort (cirka 2 800 kort), plus ett litet JSON-index för sökningen i webbläsaren. Plattformen är GitHub Pages, samma som Atlas över ingenstans.

## 13. Öppna beslut

- Slutligt namn.
- Tv-avsnitt (32 st): egna kort, eller bilagda till sin serie?
- Ska IMDb:s snittbetyg visas på filmkortet?
- Stämpeln för importdatumen (se 5).
- Texterna till startsidan och ”Om betygen”.
- Domän.
