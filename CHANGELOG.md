# Release notes

## 1.0 — 12 november 2026

### Website en zoeken
- Hoofdrubrieken voor Nederlands-Indië, Java, Bandoeng/Bandung, KNIL & militair, Bersiap & onafhankelijkheidsstrijd en samenleving.
- Java heeft een standaardkeuze **Heel Java** en plaatsfilters voor Bandoeng, Batavia, Buitenzorg, Semarang, Soerabaja, Djokja, Malang en overig Java.
- Bandoeng-zoekthema's voor onder meer Bragaweg, Dago, alun-alun, Technische Hoogeschool en station/spoor.
- Live fotozoekfunctie via Wikimedia Commons met duplicaatcontrole, filteren op historische context, bron- en licentieverwijzingen en paginering.
- Nationaal Archief-records worden als beschrijvingen en permanente Handle-links getoond. Rechten-onzekere thumbnails worden niet gereproduceerd.
- Nationaal Archief-resultaten kunnen in porties worden uitgebreid via **Meer archiefrecords tonen**.

### Bronnetwerk
- Instellingsportalen en documentatie toegevoegd voor Nationaal Archief, KITLV/Leiden, Het Utrechts Archief, NIMH, Wereldmuseum, Het Nieuwe Instituut, Rijksmuseum, Europeana, Delpher, Atlas of Mutual Heritage en Wikimedia Commons.
- De website maakt zichtbaar onderscheid tussen geïntegreerde bronnen en externe onderzoeksingangen.

### Datakwaliteit
- Metadata schema v2: expliciete onderwerp- en plaatslabels op basis van de afzonderlijke bronbeschrijving.
- Collectienamen worden niet gebruikt als bewijs voor een individuele recordclassificatie.
- KNIL en breder militair zijn onderscheiden.
- Bersiap is een strikt label dat alleen volgt wanneer het woord expliciet in de bronbeschrijving staat; dekolonisatie is een afzonderlijk, breder label.
- Datering wordt niet afgeleid uit upload- of digitaliseringstijdstempels.

### Kwaliteitsborging
- GitHub Actions voert vóór publicatie HTML- en interfacecontractchecks uit, classificatie-unit-tests en JavaScript-syntaxcontrole.
- De methode, beperkingen en bijdragenprocedure zijn gedocumenteerd in `METHODOLOGY.md` en `CONTRIBUTING.md`.

### Grenzen van deze release
- Wikimedia Commons levert live beeldresultaten; Nationaal Archief en Rijksmuseum zijn geïntegreerd via lokale metadata-snapshots.
- De Nationaal Archief-snapshot bevat bij deze release 2.250 records. De Rijksmuseum-snapshot bevat 229 foto-objecten; uitsluitend records met expliciete beeldrechten PD Mark 1.0 of CC0 1.0 tonen een afbeelding.
- Andere genoemde collectieportalen zijn externe zoekingangen, geen rechtstreekse imports.
- De release is geen volledige inventaris van Nederlands-Indië-fotografie en bevat geen record-voor-record juridische of historische certificering.
