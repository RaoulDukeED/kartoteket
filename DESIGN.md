---
name: Kartoteket
description: Läst och sett, ordnat som ett gammalt bibliotekskartotek.
colors:
  duk: "#E9E5DD"
  manila: "#D9C7A3"
  kort: "#FBF9F4"
  black: "#2B2622"
  dampad: "#655D55"
  dampad-manila: "#4A433C"
  rost: "#B4561F"
  rost-text: "#9A4416"
  rost-hover: "#7A3510"
  vit: "#FFFFFF"
  harlinje: "rgba(43, 38, 34, 0.12)"
  kant: "rgba(43, 38, 34, 0.14)"
typography:
  display:
    fontFamily: "Spectral, Georgia, serif"
    fontSize: "52px"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Spectral, Georgia, serif"
    fontSize: "44px"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Spectral, Georgia, serif"
    fontSize: "18px"
    fontWeight: 600
    lineHeight: 1.5
  body:
    fontFamily: "Spectral, Georgia, serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Spectral, Georgia, serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.4
  card-heading:
    fontFamily: "Courier Prime, Courier New, monospace"
    fontSize: "24px"
    fontWeight: 400
    lineHeight: 1.25
    letterSpacing: "0.04em"
  card-body:
    fontFamily: "Courier Prime, Courier New, monospace"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.5
  stamp:
    fontFamily: "Courier Prime, Courier New, monospace"
    fontSize: "14px"
    fontWeight: 400
    letterSpacing: "0.08em"
rounded:
  sm: "2px"
  hal: "50%"
spacing:
  xxs: "4px"
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  xxl: "32px"
  sektion: "48px"
  botten: "64px"
components:
  button-primary:
    backgroundColor: "{colors.rost}"
    textColor: "{colors.vit}"
    rounded: "{rounded.sm}"
    padding: "0 22px"
    height: "48px"
  button-primary-hover:
    backgroundColor: "{colors.rost-hover}"
    textColor: "{colors.vit}"
  button-secondary:
    backgroundColor: "{colors.kort}"
    textColor: "{colors.black}"
    rounded: "{rounded.sm}"
    padding: "0 16px"
    height: "44px"
  button-secondary-pressed:
    backgroundColor: "{colors.rost}"
    textColor: "{colors.vit}"
  input-search:
    backgroundColor: "{colors.kort}"
    textColor: "{colors.black}"
    typography: "{typography.card-body}"
    rounded: "{rounded.sm}"
    padding: "0 14px"
    height: "48px"
  drawer-front:
    backgroundColor: "{colors.manila}"
    textColor: "{colors.dampad-manila}"
    rounded: "{rounded.sm}"
    padding: "28px 20px 24px"
  drawer-label:
    backgroundColor: "{colors.kort}"
    textColor: "{colors.black}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  drawer-interior:
    backgroundColor: "{colors.manila}"
    rounded: "{rounded.sm}"
    padding: "12px"
  card-row:
    backgroundColor: "{colors.kort}"
    textColor: "{colors.black}"
    rounded: "{rounded.sm}"
    padding: "12px 16px"
  catalog-card:
    backgroundColor: "{colors.kort}"
    textColor: "{colors.black}"
    typography: "{typography.card-body}"
    rounded: "{rounded.sm}"
  rating-box:
    textColor: "{colors.black}"
    size: "40px"
  rating-box-top:
    textColor: "{colors.rost-text}"
  attachment:
    backgroundColor: "{colors.manila}"
    textColor: "{colors.black}"
    rounded: "{rounded.sm}"
    padding: "28px 28px 24px"
---

# Design System: Kartoteket

## Overview

**Creative North Star: "Katalogskåpet"**

Gränssnittet är möbeln i ett biblioteks läsesal. Startsidan är skåpet med sina lådfronter i manila, en låda är en öppnad låda där korten står på kant, och katalogkortet ligger framme på duken med hålet i foten där stången gick. Allt som syns ska gå att peka på i ett riktigt kortkatalogsrum: kartong, kortpapper, en sned stämpel, en rostlinje, en lapp fäst med gem. Det som inte har en motsvarighet där hör inte hemma här.

Stämningen är saklig, torr, lugn och lågmäld. Ingenting kommenterar sig själv, inget blinkar och inget tävlar om uppmärksamheten. Sidan är luftig men inte gles: en låda med hundratals kort ska gå att skumma lika lugnt som en med tre. Gränssnittet ska kännas som pappersark, med tunna kanter och mjuka skiften, så att det är kortet som syns och inte kontrollerna runt det.

Identiteten bärs av manilatonen och av mötet mellan två typsnitt: Spectral för allt som är rummet och Courier Prime för allt som är kortet. Den krämvita bakgrunden med seriff och tegelröd accent är en känd AI-klyscha, och systemet undviker den genom att låta kartongen, inte accenten, ta plats.

**Key Characteristics:**
- Tre papper på varandra: duk, manila och kort.
- Två röster: seriff för rummet, skrivmaskin för kortet.
- En enda accent, rost, som används sparsamt och aldrig dekorativt.
- Nästan raka hörn (2 px) överallt.
- Platt yta med ett enda lyft: katalogkortet och lappen.

## Colors

En varm, nästan oblekt pappersskala med en rostfärgad stämpelton som enda accent.

### Primary
- **Rost** (`rost`): fyllning. Primärknappar, intryckt sortering, kortets rostlinjer och fokusringen. Vit text på rost ger 4,9:1.
- **Rost, text** (`rost-text`): rost som text eller tunn linje. Länkar, aktiv navigering, kortets rubrik, stämpeln, betygsrutan för tior och femmor och registerbokstäverna.
- **Rost, hover** (`rost-hover`): mörkare rost för hover på länkar och knappar.

### Neutral
- **Duk** (`duk`): sidans bakgrund, cirka 60 % av ytan. Också hålet i kortets fot, som "visar" duken genom kortet.
- **Manila** (`manila`): skåpets fronter, lådans insida och bilagelappen, cirka 30 %.
- **Kort** (`kort`): kortpapper. Katalogkortet, kortraderna i lådan, etiketterna på fronterna, sökfältet och sekundärknapparna.
- **Bläck** (`black`): sepiasvart för all brödtext och alla rubriker.
- **Dämpad** (`dampad`): sekundär text på duk och kort, till exempel sökväg, antal, platshållare och metadata.
- **Dämpad på manila** (`dampad-manila`): sekundär text som ligger på manila, där vanlig dämpad inte når 4,5:1.
- **Vit** (`vit`): bara text på rostfyllning.
- **Hårlinje** (`harlinje`): avdelare, sidhuvudets och sidfotens linjer och kortets kant.
- **Kant** (`kant`): kanten runt manilaytor och bilagelappen.

### Named Rules
**Stämpelregeln.** Rosten är bläcket från en stämpel och används bara där en bibliotekarie skulle ha stämplat eller strukit under: på handlingen, på det aktiva valet, på det högsta betyget. Rost som pynt utan funktion är förbjuden.

**Pappersregeln.** Nya ytor väljer bland de tre papperen. Ingen fjärde bakgrundston, inga toningar, ingen transparens över bild.

**Kontrastregeln.** All text når minst 4,5:1 mot sitt eget papper. På manila byts dämpad text alltid mot dämpad på manila.

## Typography

**Display Font:** Spectral (med Georgia, serif)
**Body Font:** Spectral (med Georgia, serif)
**Label/Mono Font:** Courier Prime (med Courier New, monospace)

**Character:** Spectral är en lugn, lite smal boktrycksseriff som låter rubrikerna vara stora utan att bli högljudda. Courier Prime är skrivmaskinen som fyllde i korten. Uppdelningen är strikt: seriffen talar för rummet, maskinstilen för innehållet på papperet.

### Hierarchy
- **Display** (400, 52 px, 1,1): startsidans rubrik "Läst och sett". 44 px under 760 px.
- **Headline** (400, 44 px, 1,1): lådans och sidans rubrik. 36 px under 760 px.
- **Title** (600, 16–18 px, 1,4–1,5): rubriker i sidokolumnen och avsnittet om betygen. Det enda stället där fetstil förekommer, och bara i Spectral.
- **Body** (400, 17 px, 1,55): brödtext. Ingressen är 18 px och som bredast 560 px, avsnittet om betygen som bredast 640 px.
- **Label** (400, 14–15 px): sökväg, antal kort, sortering, sidfot och etiketter till fält. Inget gränssnitt går under 14 px.
- **Card heading** (Courier Prime 400, 24 px, versaler, spärrning 0,04 em, rost): kortets huvuduppslag. 20 px under 760 px.
- **Card body** (Courier Prime 400, 18 px, 1,5): kortets text. 16 px under 760 px. Kortraderna i lådan använder samma stil i 17 px för titeln och 14–15 px för undertitel och meta.
- **Stamp** (Courier Prime 400, 14 px, versaler, spärrning 0,08 em): stämpeln "INFÖRD …".

### Named Rules
**En-viktsregeln.** Courier Prime finns i en enda vikt. Betoning på kortet görs med rost eller indrag, aldrig med fetstil eller kursiv.

**Versalregeln.** Versaler förekommer bara på kortets rubrik och på stämpeln. Inga versala etiketter, knappar eller rubriker i gränssnittet.

## Layout

Innehållet är som bredast 1120 px, centrerat, med 24 px marginal (16 px under 760 px). Sidan är en enda kolumn med sidhuvud, huvudinnehåll och sidfot, med 32 px mellan blocken (24 px på smala skärmar) och 64 px luft i botten. Sidfoten trycks ner till skärmens nederkant.

- **Startsidan:** rubrik och ingress till vänster, sökfältet till höger på samma baslinje. Därunder skåpet, fyra lådfronter som delar raden och bryts till två per rad, och sedan en bred rad med Högsta betyg och knappen för kort på måfå.
- **Lådan:** sidokolumn (cirka 220 px) och kortlista (minst 560 px) bredvid varandra med 40 px mellanrum. Under 760 px staplas sidokolumnen överst som en utfällbar ruta, och dess block läggs i ett rutnät.
- **Kortet:** som bredast 820 px och centrerat, med föregående och nästa kort under, i ett tredelat rutnät med knappen i mitten.
- **Grupper:** ett rutnät av flikar, minst 220 px breda.

Rytmen bygger på 4 och 8 px (4, 6, 8, 12, 16, 24, 32, 48, 64). Brytpunkten är en enda: 760 px. Under den byggs kortraderna om till ett tvåkolumnsrutnät med betygsrutan till höger.

## Elevation & Depth

Systemet är platt med ett enda lyft. Duk, manila och kortraderna ligger i samma plan och skiljs åt med ton och 1 px kant. Bara katalogkortet och bilagelappen lyfter sig från duken, som papper som lagts ovanpå. Manilaytorna får en tunn ljuskant upptill i stället för skugga, som kanten på en kartongskiva.

### Shadow Vocabulary
- **Kortets lyft** (`box-shadow: 0 1px 3px rgba(43, 38, 34, 0.06), 0 12px 32px rgba(43, 38, 34, 0.06)`): bara på katalogkortet.
- **Lappens lyft** (`box-shadow: 0 2px 6px rgba(43, 38, 34, 0.06)`): bilagelappen bakom kortet.
- **Kartongkant** (`box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35)`): lådfronter och lådans insida.
- **Hålet** (`box-shadow: inset 0 1px 2px rgba(43, 38, 34, 0.25)`): hålet i kortets fot.

### Named Rules
**Ett-lyft-regeln.** Bara katalogkortet och det som är fäst vid det har skugga. Ingen skugga är starkare än 0,06, och ingen hover får lyfta något.

## Shapes

Hörnen är nästan raka, 2 px, på allt från knappar och fält till kort och lådor. Det enda runda är hålet i kortets fot. Formerna är rektangulära och avgränsas med 1 px kant, inte med fyllning. Två små avvikelser är medvetna och bär systemets glimt: stämpeln lutar −2° och bilagelappen lutar 1,5° (nästa lapp −1°). Handtaget på lådfronten är en kort mörk stav (52 × 6 px).

## Components

### Buttons
Pappersark med en enda bestämd handling: rost för det man gör, kortpapper för det man väljer.
- **Shape:** nästan raka hörn (2 px).
- **Primary:** rost med vit Spectral 600 i 16 px, minst 48 px hög. Används för Sök, Dra ett kort på måfå och Till katalogskåpet. Den stora varianten är 88 px hög och står bredvid Högsta betyg på startsidan.
- **Hover / Focus:** mörkare rost vid hover. Fokus är en 2 px rostring med 2 px avstånd. Vid tryck sjunker knappen 1 px (bara när rörelse är tillåten).
- **Secondary:** kortpapper med 1 px kant (`rgba(43, 38, 34, 0.3)`) och bläcktext i Spectral 15 px, minst 44 px hög. Används för sortering och Bläddra vidare. Intryckt sortering (`aria-pressed`) fylls med rost.

### Cards / Containers
- **Corner Style:** 2 px.
- **Background:** kortpapper på manila (kortrader) eller på duk (katalogkortet).
- **Shadow Strategy:** bara katalogkortet lyfter, se Elevation & Depth.
- **Border:** 1 px, `rgba(43, 38, 34, 0.1)` på kortraderna, som mörknar till 0,35 vid hover.
- **Internal Padding:** 12 px 16 px på kortraderna, som är minst 64 px höga.

### Inputs / Fields
- **Style:** kortpapper, 1 px kant (`rgba(43, 38, 34, 0.18)`), 2 px hörn, 48 px höjd. Texten skrivs i Courier Prime 16 px, som på ett kort. Etiketten står ovanför i Spectral 15 px, dämpad.
- **Focus:** 2 px rostring med 2 px avstånd. Inne i lådan, på manila, tar ringen rost-text, eftersom rost bara når 2,95:1 mot manila.
- **Filter i lådan:** lådor med fler kort än en bläddring (60) får fältet "Filtrera lådan" bredvid sorteringen, 44 px högt, med etiketten till vänster som "Sortera efter". Det visar alla kort som matchar och antalet, och när inget matchar en länk till sökningen i hela katalogen. Fältet syns bara med javascript.

### Navigation
- **Sidhuvud:** namnet Kartoteket i Spectral 600, 20 px, till vänster. Avdelningarna i 16 px till höger, dämpade, och bläck vid hover. Den aktiva avdelningen är rost och understruken med 6 px avstånd, och markeras med `aria-current`. Hela raden har en hårlinje under sig och bryts på smala skärmar.
- **Sökfältet i sidhuvudet:** längst till höger på alla sidor utom startsidan och söksidan, som har sökfältet i själva sidan. Samma fält som på startsidan men 44 px högt och 240 px brett, med etiketten dold för ögat. En liten tangent "/" i Courier Prime visar kortkommandot på skärmar med mus och försvinner när fältet får fokus. Under 760 px ligger fältet på en egen rad i full bredd under avdelningarna.
- **Sidokolumnen:** listor med lådor i bläck, rost vid hover, varje rad minst 44 px hög. Den aktiva lådan ligger i en liten kortpappersruta med hårlinjekant och rost text. Under 760 px fälls hela kolumnen ihop bakom en rubrik med "+" och "–".
- **Sökvägen:** länkarna har vertikal padding som ger 44 px klickyta utan att raden flyttas.
- **Register:** bokstäver i Courier Prime som 44 × 44 px klickytor, och bokstavsrubriker i rost.

### Lådfronten (signaturkomponent)
Manilaskiva med 1 px kant och ljuskant upptill, minst 196 px hög (132 px och två per rad på smala skärmar, där etiketten fyller frontens bredd). I mitten en etikett i kortpapper med lådans namn i Courier Prime 18 px, under den antalet kort i dämpad på manila och sist handtaget. Vid hover mörknar etikettens kant, inget annat rör sig. Högsta betyg är en bred front med etiketten i rost.

### Lådan och kortraden
Lådans insida är manila med 12 px luft. Korten står i den som rader av kortpapper med 6 px mellanrum. Varje rad har titeln (och svensk titel eller originaltitel under) till vänster, år och upphov i mitten, och längst till höger markeringar och betygsrutan. Markeringen för bok och film är "↔ film" eller "↔ bok" i rost, och bilagor markeras med en gem i dämpad ton.

### Betygsrutan
En kvadrat på 40 × 40 px (44 px på kortet) med 1,5 px bläckkant och siffran i Courier Prime 18 px. Tior och femmor får kant och siffra i rost. Rutan är det enda som "fylls i" på kortet och ska alltid gå att läsa av utan att läsa raden. I lådor och sökresultat är rutan dold för skärmläsare och föregås av dold text, "Betyg 8 av 10". På kortet står "Betyg:" och "av 10" redan synligt.

### Katalogkortet
Kortpapper med hårlinjekant och kortets lyft. Kortets huvud bär typ och id till vänster och stämpeln till höger, och avslutas med en 2 px rostlinje. En lodrät rostlinje (opacitet 0,45) går 56 px in från vänster (28 px på smala skärmar), och texten börjar 72 px in. Huvuduppslaget står i versaler i rost, upphovsuppgifterna indragna 28 px, "Se även" efter en streckad linje och spårningarna sist i dämpad ton. Längst ner sitter hålet. Under kortet står källan, till exempel "Uppgifter från Libris".

### Bilagelappen
Manilalapp som sticker fram bakom kortet, lutad 1,5°, med en större gem i överkanten. Text i Courier Prime 16 px, typ och kommentar i dämpad på manila.

## Do's and Don'ts

### Do:
- **Do** välj bakgrund bland duk, manila och kort, och lägg kortpapper på manila eller duk, aldrig tvärtom.
- **Do** skriv allt som står på ett kort, i en kortrad eller i sökfältet i Courier Prime 400, och allt annat i Spectral.
- **Do** använd 2 px hörn och 1 px kant på varje ny yta.
- **Do** ge varje klickyta minst 44 px höjd och varje fokuserbart element 2 px rostring med 2 px avstånd (rost-text på manila). Undantaget är länkar i kortets löptext, som får 5 px vertikal padding och 1,8 i radavstånd i "Se även".
- **Do** markera aktiv låda och avdelning med `aria-current` och rost text.
- **Do** byt dämpad text mot dämpad på manila så fort den ligger på manila.

### Don't:
- **Don't** använd versaler utanför kortets rubrik och stämpeln.
- **Don't** använd fetstil eller kursiv i Courier Prime. Betoning görs med rost.
- **Don't** ge något annat än katalogkortet och bilagelappen en skugga, och aldrig en skugga starkare än 0,06.
- **Don't** lägg till en andra accentfärg, toningar eller en krämvit seriffyta med tegelröd accent utan manila.
- **Don't** använd mittpunkter som avgränsare, pilar efter länktexter eller piller runt statisk metadata.
- **Don't** visa omslag eller affischer. Kortet är bilden.
- **Don't** låt något hoppa, lyfta eller animeras vid hover. Övergångar är högst 120 ms och gäller kantfärg och bakgrund.
