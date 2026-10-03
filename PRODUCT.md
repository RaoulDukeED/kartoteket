# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Främst ägaren själv. Kartoteket är ett personligt arkiv över allt hen läst och sett, och den viktigaste användningen är att snabbt slå upp om en titel finns i katalogen och vilket betyg den fick. Att sajten är publik är en bisak: vänner och okända besökare får bläddra, men ingen funktion byggs i första hand för dem.

## Product Purpose

En publik, personlig katalog över böcker, filmer, tv-serier och spel, byggd helt på egna betyg från Goodreads och IMDb och ordnad som ett gammalt bibliotekskartotek med lådor och kort. Den ska vara enkel att hålla aktuell: ny export in, sajten byggs om, ingen terminal behövs.

Ett lyckat besök är att ägaren hittar rätt kort fort, via sökningen eller en låda, och ser betyget och uppgifterna direkt.

## Positioning

En katalog, inte ett flöde. Kortet följer katalogpraxis (böcker under författaren, filmer under titeln, huvuduppslaget är den version ägaren faktiskt mötte) och en låda är ett urval, inte en plats: samma kort ligger i flera lådor samtidigt. Kopplingar mellan bok och film är handplockade. Inga omslag eller affischer, kortet är bilden.

## Operating Context

- Data kommer från Goodreads-exporten (hyllan *read*, 189 böcker) och IMDb-exporten (2 590 poster), berikade via Libris. Exporterna ersätts alltid i sin helhet; egna filer (`genre_manuellt.csv`, `kopplingar.csv`, senare `bilagor/`) är nycklade på id och skrivs aldrig över.
- Uppdatering sker genom att filerna dras in i `data/` på github.com; GitHub Actions bygger och publicerar på GitHub Pages.
- Ingångar: sökningen, lådorna och *Dra ett kort på måfå*, därefter "Se även". Ingen lista över det senaste och ingen tidslinje (datumen i exporterna räcker inte till det).

## Capabilities and Constraints

- Statisk sajt genererad med ett Python-skript som bara använder standardbiblioteket (`bygg/`), cirka 2 800 kortsidor plus ett JSON-index för sökningen i webbläsaren. Sajten fungerar utan JavaScript; skriptet lägger till sortering, sökning och kort på måfå.
- Sektioner: Böcker, Film, Tv-serier, Spel, plus den tvärgående lådan Högsta betyg. Betyg 1–5 för böcker och 1–10 för övrigt.
- All text på svenska. Svensk sortering, och inledande artiklar ignoreras vid sortering på titel.
- Inga externa anrop från sidorna (typsnitten ligger lokalt).
- Kända datagap som inte får fyllas med gissningar: läsdatum saknas nästan helt, bulkimporterade poster stämplas "INFÖRD FÖRE …", regissör saknas för 403 IMDb-poster, översättare visas bara vid ISBN-träff i Libris.
- Bilagor (citat, reflektioner, bilder per kort) är förberedda men inte byggda.
- Öppet: egen domän, och vilken signatur som eventuellt ska stå på sajten.

## Brand Commitments

- Namnet är **Kartoteket**. Startsidans rubrik är "Läst och sett".
- Diskret avsändare: ett förnamn eller en signatur får förekomma, men aldrig fullständigt namn, bild eller andra personuppgifter. Signaturen är inte vald än.
- Rösten är saklig och lågmäld, som en katalogpost. Startsidans texter är utkast i `texter/startsida.md` och skrivs av ägaren.
- IMDb:s snittbetyg visas inte. Betygen är ägarens egna.

## Evidence on Hand

- Exporterna och de egna filerna i `data/`, Libris-berikningen i `data/libris_berikning.json`, 20 bok–film-kopplingar i `data/kopplingar.csv`.
- Underlaget för bygget i `UNDERLAG.md` och arbetsläget i `ARBETSLÄGE.md`.
- Inga recensioner, citat eller bilagor finns ännu. Sådant får inte hittas på.

## Product Principles

1. **Uppslaget först.** Det som gör det snabbare för ägaren att hitta ett kort och se betyget går före allt som bara är trevligt att bläddra i.
2. **Kortet är sanningen.** Visa det som finns i datan, märk det som är osäkert och fyll aldrig ut luckor med påhitt.
3. **Katalog, inte flöde.** Ingen aktualitet, inga topplistor utöver lådorna; ingångarna är sökning, lådor, slumpen och kopplingar.
4. **Underhållet ska vara tråkigt.** En ny export ska räcka; allt som kräver handpåläggning vid varje uppdatering är en brist.
5. **Ett personligt arkiv med öppen dörr.** Publikt, men diskret om vem som står bakom.

## Accessibility & Inclusion

Kontrast minst 4,5:1 mot respektive bakgrund, klickytor på minst 44 px, synlig tangentbordsfokus och `aria-current` på aktiv låda och avdelning (fastslaget i `UNDERLAG.md`). Responsivt ner till 375 px.
