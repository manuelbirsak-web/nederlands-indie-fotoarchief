# Indisch Beeldarchief

**Een digitaal onderzoeksstartpunt voor de geschiedenis van Nederlands-Indië en Indonesië.**

Het Indisch Beeldarchief brengt historische foto's, bronbeschrijvingen en betrouwbare onderzoeksingangen samen. Het project besteedt extra aandacht aan Java en Bandoeng/Bandung, militaire geschiedenis en de dekolonisatieperiode.

## Open het archief

- **Website:** https://manuelbirsak-web.github.io/nederlands-indie-fotoarchief/
- **Repository:** https://github.com/manuelbirsak-web/nederlands-indie-fotoarchief

## Inhoud

| Rubriek | Inhoud |
|---|---|
| Nederlands-Indië | Historische beeldresultaten uit de voormalige archipel |
| Java | Een overzicht van Java en plaatsfilters voor Bandoeng, Batavia, Buitenzorg, Semarang, Soerabaja, Djokja, Malang en overig Java |
| Bandoeng / Bandung | Gerichte zoekthema's zoals Bragaweg, Dago, alun-alun, Technische Hoogeschool, station/spoor en 1946 |
| KNIL & militair | Militairen, eenheden, uniformen, wapens, kazernes en militaire onderwerpen |
| Bersiap & onafhankelijkheidsstrijd | Bronnen over de Indonesische revolutie en de dekolonisatieperiode, met een strikt onderscheid tussen het label Bersiap en bredere oorlogscontext |
| Samenleving | Dagelijks leven, onderwijs, werk, gezinnen en cultuur |

De standaard fotoperiode is 1800–1959. Relevante ongedateerde beelden kunnen worden getoond wanneer de bronbeschrijving of metadata de historische context ondersteunt.

## Bronnen en integratie

### Rechtstreeks geïntegreerd

- **Wikimedia Commons:** live API voor beeldbestanden en metadata. De website toont per resultaat de bronpagina, beschikbare maker-/creditgegevens en licentie-informatie. Commons is een aggregator; de oorspronkelijke instelling en bestandspagina blijven leidend.
- **Nationaal Archief:** lokale metadata-index op basis van de publieke linked-open-data-fotocollectie. De huidige snapshot bevat **180 records** met permanente Handle-links en automatisch afgeleide onderwerp- en plaatslabels. De nieuwe harvester kan geordend maximaal 4.000 records ophalen; het actuele aantal wordt pas na een succesvolle verversing verhoogd. Er worden geen thumbnails uit deze index getoond zolang de rechtenstatus niet is beoordeeld.

### Externe onderzoeksingangen

De website bevat ook directe links naar primaire of institutionele collecties:

- [Leiden University Libraries · KITLV beeldcollectie](https://digitalcollections.universiteitleiden.nl/imagecollection-kitlv)
- [Het Utrechts Archief · ruim 5.000 foto's uit voormalig Nederlands-Indië](https://hetutrechtsarchief.nl/over-ons/nieuws/ruim-5-000-fotos-uit-voormalig-nederlands-indie-online-beschikbaar)
- [NIMH Beeldbank](https://beeldbank.nimh.nl/)
- [Wereldmuseum · NMVW-collectie](https://collectie.wereldmuseum.nl/)
- [Het Nieuwe Instituut · collectiezoekportaal](https://zoeken.nieuweinstituut.nl/nl/zoeken-op-het-portaal)
- [Rijksmuseum Search API](https://data.rijksmuseum.nl/docs/search)
- [Europeana](https://www.europeana.eu/en/search)
- [Delpher · kranten Nederlands-Indië](https://www.delpher.nl/nl/kranten/results?query=Nederlands-Indi%C3%AB)
- [Atlas of Mutual Heritage](https://www.atlasofmutualheritage.nl/)

**Belangrijk:** dit zijn op dit moment externe zoekingangen, geen rechtstreekse data-integraties in de fotogalerij. De website toont die grens expliciet.

## Historische betrouwbaarheid

Een zoekresultaat is geen zelfstandig bewijs voor datering, plaats, identiteit, eenheid of gebeurtenis. De website maakt onderscheid tussen gegevens die een bron expliciet vermeldt, automatisch afgeleide zoeklabels en gegevens die niet bekend of niet ingevuld zijn.

De classificatie wordt afgeleid uit de tekst van het individuele archiefrecord. De collectienaam wordt niet gebruikt om een onderwerp aan alle records binnen een collectie toe te kennen.

**KNIL is niet hetzelfde als militair.** Het KNIL-label wordt alleen toegepast als de beschrijving KNIL expliciet noemt of een herkenbare volledige naamvariant bevat.

**Bersiap is niet hetzelfde als de hele onafhankelijkheidsstrijd.** Het specifieke label Bersiap verschijnt alleen wanneer de oorspronkelijke beschrijving het woord Bersiap gebruikt. De bredere term dekolonisatieperiode is een afzonderlijke classificatie. Een jaartal tussen 1945 en 1950 is op zichzelf geen inhoudelijk bewijs.

Zie [METHODOLOGY.md](METHODOLOGY.md) voor het bronnenbeleid, datering, classificatie en beperkingen.

## Beeldrechten

Een vindbare afbeelding is niet automatisch vrij herbruikbaar.

- Controleer de oorspronkelijke bronpagina, licentie, maker, bronvermelding en voorwaarden.
- De aanduiding CNE / Copyright Not Evaluated betekent dat de rechtenstatus niet is beoordeeld; behandel dit niet als een vrije licentie.
- De Nationaal Archief-index bevat metadata en Handle-links, geen herpubliceerde thumbnails.
- De website kopieert niet zonder noodzaak beeldbestanden naar de repository.

Het project verleent geen auteursrechtelijke toestemming. Zie [METHODOLOGY.md](METHODOLOGY.md#5-beeldrechten-en-hergebruik) en [CONTRIBUTING.md](CONTRIBUTING.md).

## Techniek

- Statische HTML, CSS en vanilla JavaScript.
- Hosting via GitHub Pages.
- Live Wikimedia Commons API.
- Lokale JSON-metadata-index Nationaal Archief (assets/nationaal-archief.json, schemaVersion 2).
- Python-harvester (scripts/harvest_nationaal_archief.py).
- Wekelijkse verversingsworkflow (.github/workflows/refresh-archive-index.yml).
- Pre-deployment validatie en classificatie-unit-tests via GitHub Actions.
- Favorieten worden lokaal in de browser opgeslagen; er zijn geen bezoekersaccounts of server-side profielen.

## Kwaliteitscontroles

Bij elke publicatie voert GitHub Actions uit:

1. HTML-, interface- en archiefcontractchecks (scripts/validate_site.py);
2. unit-tests voor de onderwerp- en plaatsclassificatie (scripts/test_archive.py);
3. JavaScript-syntaxcontrole (node --check).

Dit zijn geautomatiseerde technische controles. Ze bewijzen niet dat elke historische beschrijving, foto-identificatie, datering of licentie inhoudelijk juist is. Live browserinteractie, toegankelijkheid, performance en record-voor-record verificatie worden als afzonderlijke controles behandeld.

## Projectdocumentatie

- [Curatoriële methode en gegevensbeleid](METHODOLOGY.md)
- [Bijdragen en correcties](CONTRIBUTING.md)
- [Release notes](CHANGELOG.md)

## Roadmap

1. De Nationaal Archief-harvester uitbreiden en de nieuwe snapshot na uitvoering valideren.
2. Live beeldcollecties verder ontsluiten, te beginnen met bronnen waarvoor stabiele publieke API's of IIIF-manifests beschikbaar zijn.
3. De Bandoeng-collectie verdiepen met controleerbare reeksen en recordniveau-metadata.
4. KNIL- en dekolonisatiebronnen uitbreiden zonder brede of onjuiste onderwerplabels te gebruiken.
5. Onafhankelijke toegankelijkheids- en performance-audits uitvoeren.
6. Een eigen domeinnaam koppelen wanneer de eigenaar een domein en DNS-toegang beschikbaar stelt.

## Status en afbakening

Het Indisch Beeldarchief is een werkende openbare onderzoekswebsite en een groeiende startcatalogus. Het is **geen complete inventaris van alle historische foto's over Nederlands-Indië**. De huidige 180 Nationaal Archief-records zijn een selecte metadata-snapshot, geen weergave van de volledige collectie. Een volledige historische, juridische en curatoriële verificatie van alle resultaten is nog niet uitgevoerd.

Laatste inhoudelijke release: **12 november 2026**.
