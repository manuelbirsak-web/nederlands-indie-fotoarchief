# Indisch Beeldarchief — project- en technische documentatie

Een onafhankelijk digitaal startpunt voor historisch beeldmateriaal over Nederlands-Indië, Java en Bandoeng/Bandung.

## Website

- Publicatie: https://manuelbirsak-web.github.io/nederlands-indie-fotoarchief/
- Repository: https://github.com/manuelbirsak-web/nederlands-indie-fotoarchief
- Hosting: GitHub Pages via GitHub Actions.
- Techniek: statische HTML, CSS en vanilla JavaScript. Geen framework, build-tool of externe font-download.

## Structuur en functionaliteit

- Overzicht Nederlands-Indië, Java, Bandoeng/Bandung, KNIL/militair en samenleving.
- Plaatsgerichte ingangen voor Bandoeng, Batavia, Buitenzorg, Semarang, Soerabaja, Djokja, Malang en overig Java.
- Bandoeng-zoekthema's: Bragaweg, Dago, alun-alun, Technische Hoogeschool, spoor/station en 1946.
- Live beeldzoekfunctie via Wikimedia Commons.
- Dateringfilter op herkenbare jaartallen in de objectmetadata; niet-gedateerde records kunnen apart worden getoond.
- Onderwerpsfilter als zoektermverfijning; dit is geen gecontroleerde archiefclassificatie.
- Paginering via de continuation-parameters van de MediaWiki API.
- Foto's bewaren in lokale browseropslag.
- Per record bronpagina, maker, datering, credit (waar aanwezig) en licentie-informatie (waar aanwezig).
- Responsive presentatie, toetsenbordfocus, skiplink, laad-/foutstatus en lazy-loaded afbeeldingen.

## Historische en inhoudelijke betrouwbaarheid

Een zoekresultaat is geen zelfstandig bewijs voor plaats, datum, persoon, eenheid of gebeurtenis. De website onderscheidt daarom metadata die de bron aanbiedt van gegevens die niet zijn ingevuld. Gebruikers moeten voor verificatie de oorspronkelijke bestands- of archiefpagina raadplegen.

De website is een doorzoekbare startcatalogus, geen complete digitale reproductie van alle collecties over Nederlands-Indië. Resultaten kunnen onvolledig, verkeerd getagd of foutief beschreven zijn. Historische spellingen, alternatieve plaatsnamen en zoektermen zijn nodig voor een betere dekking.

## Bronnen en integratiegrenzen

- Wikimedia Commons: live API voor de huidige galerij.
- Nationaal Archief: collectieportaal en open-data-initiatieven. De beeld-/metadata-API is volgens de geraadpleegde documentatie tijdelijk niet beschikbaar; er is daarom nog geen directe live API-integratie. Open scans en metadata zijn deels via Commons te vinden.
- Leiden University Libraries / KITLV: collectieportaal; IIIF wordt bij onderdelen van de digitale collecties ondersteund. Er is nog geen complete, doorzoekbare manifestindex geïntegreerd.
- Rijksmuseum: publiek doorzoekbare collectie en Search API voor museumobjecten; dit omvat niet alle archieven of bibliotheekcollecties.
- Europeana: een API-sleutel is vereist voor Search API-integratie; die is niet in deze repository opgenomen.
- Geheugen van Nederland / Delpher: externe zoekingangen, nog geen geïntegreerde record-API.

## Performance en privacy

De site gebruikt geen frontend-framework en geen externe font-CDN. Foto's worden pas via de zoekresultaten opgehaald en laden lazy. De galerij communiceert rechtstreeks met Wikimedia Commons; laden is daarom mede afhankelijk van de beschikbaarheid en responstijd van die externe dienst. Er zijn nog geen onafhankelijke Lighthouse-, WebPageTest- of veldmetingen uitgevoerd. Er worden geen bezoekersaccounts of server-side gebruikersprofielen bijgehouden. Opgeslagen favorieten blijven in de lokale browseropslag.

## Teststatus (12 november 2026)

| Onderdeel | Status | Bewijs / beperking |
|---|---|---|
| GitHub Pages deployment | Geslaagd | GitHub Actions-run 43286730748; deploy-job en alle relevante stappen completed/success |
| Bronbestanden en versiebeheer | Gecontroleerd | Main-branch commit en bestanden uit GitHub opgehaald |
| Functionele code-inspectie | Uitgevoerd | Zoekopbouw, filters, paginering, metadata en DOM-rendering beoordeeld |
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
3. Records uit Nationaal Archief/Commons, Leiden/KITLV en Rijksmuseum systematisch ontsluiten waar API- en gebruiksvoorwaarden dat toestaan.
4. Bandoeng uitbreiden met gecontroleerde fotoreeksen en recordmetadata; per foto bron, fotograaf, datum, locatie, collectie-ID en rechten vastleggen.
5. Een beheerde domeinnaam koppelen zodra de domeinnaam en DNS-toegang beschikbaar zijn.
6. Curatoriële controle toevoegen om verkeerd getagde, dubbel opgenomen of foutief gedateerde foto's te markeren.

