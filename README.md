# Indisch Beeldarchief — project- en technische documentatie

Een onafhankelijk digitaal startpunt voor historisch beeldmateriaal over Nederlands-Indië, Java en Bandoeng/Bandung.

## Website

- Publicatie: https://manuelbirsak-web.github.io/nederlands-indie-fotoarchief/
- Repository: https://github.com/manuelbirsak-web/nederlands-indie-fotoarchief
- Hosting: GitHub Pages via GitHub Actions.
- Techniek: statische HTML, CSS en vanilla JavaScript. Geen framework, build-tool of externe font-download.

## Structuur en functionaliteit

- Overzicht Nederlands-Indië, Java, Bandoeng/Bandung, KNIL/militair, Bersiap & onafhankelijkheidsstrijd en samenleving.
- Plaatsgerichte ingangen voor Bandoeng, Batavia, Buitenzorg, Semarang, Soerabaja, Djokja, Malang en overig Java.
- Bandoeng-zoekthema's: Bragaweg, Dago, alun-alun, Technische Hoogeschool, spoor/station en 1946.
- Live beeldzoekfunctie via Wikimedia Commons; automatisch doorzoeken van maximaal vier resultaatpagina's wanneer irrelevante resultaten worden weggefilterd.
- Duplicaatdetectie tijdens paginering; afbeeldingen openen op volledige grootte in een nieuw tabblad.
- Afzonderlijke rubriek Bersiap & onafhankelijkheidsstrijd met bronkritische formulering.
- Standaardperiode 1800–1959; ongedateerde foto's worden toegelaten wanneer titel, beschrijving of Commons-categorieën aantoonbaar verwijzen naar Nederlands-Indië, de koloniale periode, Bersiap, KNIL of een historische fotoreeks.
- Extra relevantiefilter per rubriek: titel en beschrijving moeten aantoonbaar bij het gekozen onderwerp/gebied passen.
- Niet-fotografische resultaten zoals logo's, kaarten, ranginsignes, boekomslagen, tijdschriften, kranten en posters worden uitgesloten.
- Onderwerpsfilter als zoektermverfijning; dit is geen gecontroleerde archiefclassificatie.
- Paginering via de continuation-parameters van de MediaWiki API.
- Foto's bewaren in lokale browseropslag.
- Per Commons-record bronpagina, maker, opnamedatering uit expliciete metadata, credit (waar aanwezig) en licentie-informatie (waar aanwezig).
- Afzonderlijke metadata-index met 180 records uit de linked-open-data fotocollectie van het Nationaal Archief; bronbeschrijvingen worden zonder beeldpreview getoond zolang de rechtenstatus niet is beoordeeld.
- Automatische wekelijkse verversing van de Nationaal Archief-index via GitHub Actions (`refresh-archive-index.yml`).
- Responsive presentatie, toetsenbordfocus, skiplink, laad-/foutstatus en lazy-loaded afbeeldingen.

## Historische en inhoudelijke betrouwbaarheid

Een zoekresultaat is geen zelfstandig bewijs voor plaats, datum, persoon, eenheid of gebeurtenis. Ongedateerde beelden worden niet automatisch afgewezen: ze worden alleen getoond als titel of beschrijving een expliciete historische context noemt. Een plaatsnaam alleen is geen bewijs dat een foto uit de koloniale periode komt. De website onderscheidt metadata die de bron aanbiedt van gegevens die niet zijn ingevuld. Gebruikers moeten voor verificatie de oorspronkelijke bestands- of archiefpagina raadplegen.

De website is een doorzoekbare startcatalogus, geen complete digitale reproductie van alle collecties over Nederlands-Indië. Resultaten kunnen onvolledig, verkeerd getagd of foutief beschreven zijn. Historische spellingen, alternatieve plaatsnamen en zoektermen zijn nodig voor een betere dekking.

## Bronnen en integratiegrenzen

- Wikimedia Commons: live API voor de huidige galerij.
- Nationaal Archief: een lokale metadata-snapshot uit de publieke linked-open-data/SPARQL-fotocollectie. De index bevat beschrijvingen en permanente Handle-links, geen afbeeldingsbestanden. De records vermelden vaak RightsStatements CNE (Copyright Not Evaluated); daarom worden geen thumbnails hergepubliceerd en moet de rechtenstatus per record worden gecontroleerd.
- Leiden University Libraries / KITLV: collectieportaal; IIIF wordt bij onderdelen van de digitale collecties ondersteund. Er is nog geen complete, doorzoekbare manifestindex geïntegreerd.
- Rijksmuseum: publiek doorzoekbare collectie en Search API voor museumobjecten; dit omvat niet alle archieven of bibliotheekcollecties.
- Europeana: een API-sleutel is vereist voor Search API-integratie; die is niet in deze repository opgenomen.
- Geheugen van Nederland / Delpher: externe zoekingangen, nog geen geïntegreerde record-API.

## Performance en privacy

De site gebruikt geen frontend-framework en geen externe font-CDN. Foto's worden pas via de zoekresultaten opgehaald en laden lazy. De galerij communiceert rechtstreeks met Wikimedia Commons; laden is daarom mede afhankelijk van de beschikbaarheid en responstijd van die externe dienst. Er zijn nog geen onafhankelijke Lighthouse-, WebPageTest- of veldmetingen uitgevoerd. Er worden geen bezoekersaccounts of server-side gebruikersprofielen bijgehouden. Opgeslagen favorieten blijven in de lokale browseropslag.

## Teststatus (12 november 2026)

| Onderdeel | Status | Bewijs / beperking |
|---|---|---|
| GitHub Pages deployment | Geslaagd | GitHub Actions-run 43291694240; validatie en deploy completed/success |
| Bronbestanden en versiebeheer | Gecontroleerd | Main-branch commit en bestanden uit GitHub opgehaald |
| Functionele code-inspectie | Uitgevoerd | Zoekopbouw, datering 1800–1959, inhoudelijk relevante ongedateerde beelden, rubriekrelevantie, uitsluiting van niet-foto's, paginering en metadata beoordeeld |
| HTML- en JavaScript-validatie | Geslaagd | GitHub Actions validate-job: HTML-contractcheck en `node --check` geslaagd |
| Live gepubliceerde HTML | Gecontroleerd | De gepubliceerde pagina bevat de standaardperiode 1800–1959, toelating van inhoudelijk relevante ongedateerde beelden en bronkritische datering; dynamische browserinteractie is niet via DOM-automatisering getest |
| Nationaal Archief-index | Geïntegreerd | 180 metadatarecords, zonder previews vanwege onzekere rechten; wekelijkse refresh-workflow toegevoegd |
| Live browserinteractie | Niet onafhankelijk getest | Geen beschikbare browserautomatisering in deze uitvoering |
| Werkelijke laadtijd / Core Web Vitals | Niet gemeten | Geen Lighthouse/WebPageTest/veldmeting uitgevoerd |
| Compleetheid archiefmateriaal | Niet bewezen | Alleen Wikimedia live geïntegreerd; overige bronnen grotendeels externe ingangen |
| Feitelijke juistheid per foto | Niet volledig bewezen | Vereist record-voor-record broncontrole en curatoriële verificatie |
| Custom domain | Geblokkeerd | Vereist een domein dat de eigenaar beheert en DNS-configuratie; GitHub Pages' standaard-URL bevat de gebruikersnaam |

## Beeldrechten

De website kopieert geen afbeeldingen naar de repository. Open de oorspronkelijke bestands-/collectiepagina en controleer licentie, maker, bron, naamsvermelding en eventuele beperkingen voordat materiaal wordt hergebruikt. Een Commons-vermelding is niet automatisch een garantie dat elk gebruik vrij is.

## Publicatie

Een push naar `main` activeert `.github/workflows/pages.yml`. De actuele publicatie loopt via GitHub Actions en `actions/deploy-pages`.

## Openstaande verbeterpunten

1. Onafhankelijke browser- en apparaat-test uitvoeren; Lighthouse meten (LCP, INP, CLS, TBT, transfer size).
2. Eenheidstests toevoegen voor zoekcompositie, dateringextractie, filters, continuations en foutafhandeling.
3. Leiden/KITLV en Rijksmuseum systematisch ontsluiten waar API- en gebruiksvoorwaarden dat toestaan.
4. Bandoeng uitbreiden met gecontroleerde fotoreeksen en recordmetadata; per foto bron, fotograaf, datum, locatie, collectie-ID en rechten vastleggen.
5. Een beheerde domeinnaam koppelen zodra de domeinnaam en DNS-toegang beschikbaar zijn.
6. Curatoriële controle toevoegen om verkeerd getagde, dubbel opgenomen of foutief gedateerde foto's te markeren.

