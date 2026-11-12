# Curatoriële methode en gegevensbeleid

**Project:** Indisch Beeldarchief  
**Versie:** 1.0  
**Datum:** 12 november 2026

## 1. Doel en afbakening

Indisch Beeldarchief is een doorzoekbaar onderzoeksstartpunt voor historisch beeldmateriaal over Nederlands-Indië en de Indonesische archipel. De standaardperiode in de fotogalerij is 1800–1959. Relevante ongedateerde beelden kunnen worden getoond wanneer hun bronbeschrijving of bestandsmetadata een aantoonbare historische context bevat.

Het archief is geen volledige nationale beeldbank, geen officiële catalogus van een erfgoedinstelling en geen vervanging van de oorspronkelijke collectie. De hoeveelheid gevonden resultaten is afhankelijk van de dekking, beschrijvingen, API's en toegangsrechten van aangesloten bronnen.

## 2. Bronnenhiërarchie

Bij onderzoek en correctie geldt deze voorkeursvolgorde:

1. **Oorspronkelijk object- of archiefrecord van de beherende instelling.** Dit is de primaire referentie voor inventarisnummer, beschrijving, fotograaf, datering, collectie en rechten.
2. **Gepubliceerde catalogus- of collectiegegevens van de instelling.** Gebruik deze als context, maar controleer waar mogelijk het objectrecord.
3. **Geaggregeerde databronnen**, zoals Wikimedia Commons of Europeana. Deze kunnen waardevolle toegang bieden, maar kunnen verkorte, gewijzigde of foutieve metadata bevatten.
4. **Secundaire publicaties en zoekresultaten.** Gebruik deze om zoektermen of context te ontdekken, niet als zelfstandig bewijs voor een objectgegeven.

Een kopie op Wikimedia Commons maakt de Commons-beschrijving niet automatisch tot de oorspronkelijke instellingstekst.

## 3. Datering

- Een datum wordt als opname- of objectdatum weergegeven wanneer de bron deze expliciet als zodanig aanbiedt en het veld daarvoor bedoeld is.
- Technische metadata zoals uploadtijd, scanmoment, wijzigingsdatum of publicatiedatum wordt niet als opnamedatum gepresenteerd.
- Een datum uit een bijschrift blijft een bronvermelding en wordt niet onafhankelijk bevestigd door het archief.
- Als betrouwbare datering ontbreekt, blijft het beeld als ongedateerd vermeld. Een contextuele schatting wordt niet als feit weergegeven.
- De datumfilter op de website is een praktische selectie, geen bewijs dat alle resultaten binnen een gekozen jaargrens daadwerkelijk in dat jaar zijn gemaakt.

## 4. Plaats- en onderwerpclassificatie

De automatische labels in de Nationaal Archief-snapshot worden uitsluitend afgeleid uit de tekst van het afzonderlijke record. De naam van een fotocollectie wordt niet gebruikt om elk record in die collectie hetzelfde onderwerp toe te kennen.

De labels zijn hulpmiddelen om te zoeken, geen officiële classificaties van het Nationaal Archief en geen curatoriële bevestiging. Ze kunnen trefwoorden missen of te ruim matchen. Bij een twijfelachtig label moet het oorspronkelijke record leidend zijn.

### KNIL en militair

Het label **KNIL** wordt alleen toegekend wanneer de beschrijving expliciet KNIL of een herkenbare volledige naamvariant vermeldt. Het bredere label **militair** kan ook worden toegekend aan een beschrijving met militairen, eenheden, wapens, voertuigen of militaire handelingen. Een militair onderwerp is niet automatisch KNIL.

### Bersiap en dekolonisatie

Het label **Bersiap** wordt uitsluitend gebruikt wanneer de oorspronkelijke bronbeschrijving het woord *Bersiap* expliciet bevat. Een jaartal, plaatsnaam, geweldsvermelding of algemeen oorlogsbegrip is op zichzelf onvoldoende.

Het bredere label **dekolonisatieperiode** wordt gebruikt voor beschrijvingen die expliciete termen bevatten zoals TNI, pemoeda, Indonesische onafhankelijkheidsstrijd, de Indonesische revolutie of politionele acties. Dat label betekent niet dat de gebeurtenis of foto zelfstandig als Bersiap is vastgesteld.

De periodefilter 1945–1950 is een tijdsselectie en geen inhoudelijke classificatie.

### Java en Bandoeng

Historische schrijfwijzen en moderne plaatsnamen worden waar mogelijk als zoekaliassen gebruikt, bijvoorbeeld Bandoeng/Bandung, Batavia/Jakarta en Buitenzorg/Bogor. Een vermelding in het bijschrift blijft broninformatie; de website bevestigt de exacte opnamelocatie niet zelfstandig.

## 5. Beeldrechten en hergebruik

- Een vindbare afbeelding is niet automatisch vrij herbruikbaar.
- De Nationaal Archief-index op deze website bevat metadata en permanente Handle-links. Er worden geen thumbnails uit records met onduidelijke of niet-beoordeelde rechtenstatus gereproduceerd.
- Een aanduiding zoals **CNE / Copyright Not Evaluated** betekent dat de rechtenstatus niet is beoordeeld. Behandel dit niet als een vrije licentie.
- Bij Wikimedia Commons moeten de licentie, licentieversie, maker, bronvermelding en eventuele voorwaarden op de oorspronkelijke bestandspagina worden gecontroleerd.
- Andere instellingen kunnen downloads beperken of verschillende toegangs- en hergebruikvoorwaarden hanteren.
- Bij twijfel wordt geen beeld gekopieerd of gepubliceerd; de bezoeker wordt naar het oorspronkelijke record verwezen.

Dit document is geen juridisch oordeel en verleent geen toestemming voor hergebruik.

## 6. Gegevensmodel

De Nationaal Archief-snapshot gebruikt schemaVersion 2. De Rijksmuseum-snapshot gebruikt schemaVersion 1 en bevat objectidentificatie, bron- en zoekprovenance, beschrijving, datering, maker, classificatielabels en eventuele expliciete rechteninformatie op het digitale beeld zelf. Een record kan onder meer bevatten:

| Veld | Betekenis |
|---|---|
| `uri` | Permanente Handle-link naar het oorspronkelijke record |
| `description` | Door de bron aangeleverde beschrijving |
| `date` | Door de bron aangeleverde datum; niet automatisch geverifieerd |
| `collection` | Collectienaam zoals aangeleverd door de bron |
| `creator` | Maker/fotograaf indien beschikbaar |
| `rights` | Rechteninformatie zoals aangeleverd door de bron |
| `topics` | Automatisch afgeleide zoeklabels |
| `places` | Automatisch afgeleide plaatslabels |

Het overzicht `topicCounts` en `placeCounts` is een telling van de labels in de actuele snapshot. Het is geen telling van alle foto's die een instelling bezit.

## 7. Verversing en foutafhandeling

De metadata-harvester bevraagt de publieke SPARQL-service van het Nationaal Archief in geordende pagina's van maximaal 500 records, met een veiligheidslimiet van acht pagina's (maximaal 4.000 opgehaalde records). De wekelijkse GitHub Actions-workflow probeert de snapshot te verversen; een wijziging aan de harvester start ook een verversing. Bij een mislukte of te kleine respons blijft de bestaande snapshot behouden en wordt de workflow als mislukt gemarkeerd. Een geslaagde technische verversing is geen curatoriële kwaliteitscontrole.

De huidige snapshot is een begrensde zoekselectie, geen volledige export van de circa 400.000 foto's die het Nationaal Archief op zijn informatiepagina vermeldt. De actuele recordtelling en peildatum staan in `assets/nationaal-archief.json`.

## 8. Correcties

Een inhoudelijke correctie moet waar mogelijk bevatten:

- link naar het oorspronkelijke object- of archiefrecord;
- veld dat volgens de melder onjuist is;
- onderbouwing uit een primaire bron of gedocumenteerd onderzoek;
- onderscheid tussen vaststaand gegeven, bronclaim en hypothese.

Wijzig een plaats, datum, persoon, eenheid of gebeurtenis niet uitsluitend op basis van gelijkenis, vermoedens of een onderschrift uit een andere kopie.

## 9. Bekende beperkingen

- Wikimedia Commons levert live beeldresultaten. Nationaal Archief en Rijksmuseum leveren lokale metadata-snapshots; bij het Rijksmuseum worden uitsluitend beelden getoond met expliciete beeldlicentie PD Mark 1.0 of CC0 1.0.
- KITLV, Utrechts Archief, NIMH, Wereldmuseum, Het Nieuwe Instituut, Europeana, Delpher en Atlas of Mutual Heritage zijn als externe onderzoeksingangen opgenomen. Een koppeling is geen API-integratie.
- De automatische labels moeten worden beoordeeld en verfijnd; ze zijn geen vervanging van menselijke geschiedkundige controle.
- De volledigheid van de beeldcollectie is niet vastgesteld.
- Er is nog geen volledige record-voor-record verificatie, onafhankelijke toegankelijkheidsaudit, Lighthouse-meting of juridische rechtencontrole van alle beelden uitgevoerd.

Deze beperkingen worden bewust zichtbaar gehouden om schijnzekerheid te voorkomen.
