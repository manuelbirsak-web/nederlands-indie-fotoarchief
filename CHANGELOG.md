# Release notes

## 1.1 — 12 november 2026

### Familieonderzoek en Deep Search
- Nieuwe familierubriek met het aangeleverde Birsak-familieportret en transcriptie van de 14 namen.
- Multi-source Deep Search-ingang voor adres-, plaats-, persoons- en genealogische zoektermen.
- Onderzoeksbronnen toegevoegd: Indisch4ever (2011), genealogische vermeldingen van Ernanie Ernest Birsak en Arnold Willem Birsak, en posthistorische documentatie van Lembangweg 346 in 1940.
- Expliciet onderscheid tussen bronvermelding, hypothese en bewezen identificatie.
- De twee originele aangeleverde beeldbestanden zijn nog niet als repository-assets gepubliceerd.

## 1.0 — 12 november 2026

### Website en zoeken
- Rubrieken voor Nederlands-Indië, Java, Bandoeng/Bandung, KNIL & militair, Bersiap & onafhankelijkheidsstrijd en samenleving.
- Java start met **Heel Java** en biedt plaatsfilters voor Bandoeng, Batavia, Buitenzorg, Semarang, Soerabaja, Djokja, Malang en overig Java.
- Bandoeng-zoekthema's voor Bragaweg, Dago, alun-alun, Technische Hoogeschool, station/spoor en 1946.
- Live Wikimedia Commons-beeldresultaten met historische contextfiltering, duplicaatdetectie, bron-/licentie-informatie en paginering.
- Nationaal Archief- en Rijksmuseum-records zijn geïntegreerd als lokale metadata-snapshots met bronlinks en aanvullende filters.
- De institutionele onderzoeksdirectory maakt onderscheid tussen geïntegreerde datasets en externe zoekingangen.

### Geïntegreerde gegevensbronnen
- **Nationaal Archief:** snapshot schema v2 met 4.000 metadatarecords (peildatum 12 november 2026). De harvester gebruikte acht pagina's van 500 records en bereikte de veiligheidslimiet; de selectie is dus expliciet onvolledig.
- **Rijksmuseum:** snapshot schema v1 met 229 foto-objecten. Van 215 objecten is een expliciete Public Domain Mark 1.0- of CC0 1.0-verklaring op het digitale beeld zelf vastgelegd; 14 records blijven metadata-only.
- **Wikimedia Commons:** live API-zoekbron; licentie en oorspronkelijke bestandspagina worden per bestand getoond.
- KITLV/Leiden, Utrechts Archief, NIMH, Wereldmuseum, Het Nieuwe Instituut, Europeana, Delpher en Atlas of Mutual Heritage zijn externe onderzoeksingangen, geen geïntegreerde datafeeds.

### Historische en rechtenmethodiek
- KNIL en bredere militaire onderwerpen zijn afzonderlijke labels.
- Bersiap is een strikt label dat alleen wordt toegekend wanneer de individuele bronbeschrijving het woord Bersiap expliciet gebruikt.
- Dekolonisatie is een afzonderlijke, bredere classificatie.
- Collectienamen en jaartallen worden niet als zelfstandig bewijs voor een individueel onderwerp gebruikt.
- Upload- en digitaliseringstijdstempels worden niet als opnamedatum gepresenteerd.
- Rijksmuseum-afbeeldingen worden alleen getoond met een expliciete beeldniveauverklaring Public Domain Mark 1.0 of CC0 1.0; objectniveau-metadata wordt niet als beeldlicentie geïnterpreteerd.
- Nationaal Archief-records worden als metadata en Handle-links getoond; er worden geen rechten-onzekere thumbnails hergebruikt.

### Kwaliteitsborging
- GitHub Actions valideert HTML-, interface-, bron- en data-contracten.
- Python-harvesters en tests worden gecompileerd.
- Unit-tests toetsen classificatie, Linked Art-structuren en beeldrechten.
- Inline JavaScript wordt met Node.js op syntax gecontroleerd.
- Methode, beperkingen en bijdragenprocedure staan in METHODOLOGY.md en CONTRIBUTING.md.

### Grenzen van deze release
- De Nationaal Archief-snapshot is een begrensde selectie en bereikte de ingestelde limiet van 4.000 records.
- De Rijksmuseum-snapshot is gebaseerd op een beperkte lijst zoektermen en geselecteerde zoekresultaten; geen volledige collectie-export.
- Externe collectieportalen zijn niet rechtstreeks geïntegreerd.
- Geen volledige record-voor-record historische verificatie, juridische rechtencontrole, onafhankelijke toegankelijkheidsaudit of Lighthouse-performance-audit geclaimd.
