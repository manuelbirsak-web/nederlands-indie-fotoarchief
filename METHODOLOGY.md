# Curatoriële methode en gegevensbeleid

**Project:** Indisch Beeldarchief  
**Versie:** 1.0  
**Datum:** 13 november 2026

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
- De Nationaal Archief-snapshot van 13 november 2026 bevat 4.000 records. Alle 4.000 records voeren in deze linked-open-data-snapshot de rechtenstatus **CNE / Copyright Not Evaluated**. Deze records worden uitsluitend als metadata met permanente Handle-links getoond; er wordt geen afbeelding uit deze snapshot gereproduceerd.
- CNE betekent dat de rechtenstatus niet is beoordeeld. Behandel dit niet als een vrije licentie. Een afzonderlijke officiële fotopagina kan voor een individueel beeld wél expliciet publiek domein of rechtenvrij hergebruik vermelden; die status mag alleen na controle van die specifieke pagina worden vastgelegd en mag niet automatisch op andere records worden toegepast.
- De Rijksmuseum-snapshot bevat 229 foto-objecten: 215 digitale beelden met een expliciete Public Domain Mark 1.0- of CC0 1.0-verklaring op het beeld zelf en 14 metadata-only objecten. De validatie controleert ieder beeldrecord afzonderlijk tegen deze allowlist.
- Wikimedia Commons-thumbnails worden alleen getoond wanneer de API een expliciete, herbruikbare licentie-URL teruggeeft: CC0 1.0, Public Domain Mark 1.0, CC BY of CC BY-SA (versies 1.0, 2.0, 2.5, 3.0 of 4.0). Ontbrekende licenties en rechtenverklaringen zoals CNE worden niet als toestemming behandeld en leiden niet tot beeldweergave.
- De bron- en licentiepagina blijft per getoonde afbeelding rechtstreeks bereikbaar. Maker en bronvermelding worden getoond wanneer de bronmetadata die aanlevert; een ontbrekende maker wordt niet ingevuld of geraden.
- Andere instellingen kunnen downloads beperken of verschillende toegangs- en hergebruikvoorwaarden hanteren.
- Bij twijfel wordt geen beeld gekopieerd of gepubliceerd; de bezoeker wordt naar het oorspronkelijke record verwezen.

Dit document is geen juridisch oordeel en verleent geen toestemming voor hergebruik.

## 6. KNIL-bewapeningsindex

De snapshot van 13 november 2026 bevat 905 records met het automatische label KNIL. Binnen de 4.000 opgehaalde records zijn 148 KNIL-records gevonden waarvan de afzonderlijke bronbeschrijving een wapen, voertuig of bewapeningsgerelateerd onderwerp noemt; deze selectie bevat 115 verschillende beschrijvingen. De selectie is opgenomen in `assets/knil-bewapening.json`.

De categorieën (pantserwagens en tanks, machinegeweren en machinepistolen, artillerie en mortieren, geweren en handwapens, overige bewapening) zijn uitsluitend zoekhulpen die uit de beschrijving zijn afgeleid. Ze vormen geen zelfstandige identificatie van het gefotografeerde model. De exacte tekst, datum en permanente Handle worden ongewijzigd aan de bronmetadata ontleend. Duplicaatbeschrijvingen blijven als afzonderlijke archiefrecords behouden wanneer de Handle verschilt.

Alle 148 geselecteerde records hebben in de snapshot CNE als rechtenstatus. De website toont daarom uitsluitend de beschrijving, de categorie als zoekhulp en een link naar het oorspronkelijke record; geen van deze 148 foto's wordt vanuit de snapshot herpubliceerd. Wanneer een individuele Nationaal Archief-fotopagina elders expliciet publiek domein vermeldt, moet die afzonderlijke status apart worden vastgelegd voordat het beeld wordt gebruikt.

## 7. Gegevensmodel

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

## 8. Verversing en foutafhandeling

De metadata-harvester bevraagt de publieke SPARQL-service van het Nationaal Archief in geordende pagina's van maximaal 500 records, met een veiligheidslimiet van acht pagina's (maximaal 4.000 opgehaalde records). De wekelijkse GitHub Actions-workflow probeert de snapshot te verversen; een wijziging aan de harvester start ook een verversing. Bij een mislukte of te kleine respons blijft de bestaande snapshot behouden en wordt de workflow als mislukt gemarkeerd. Een geslaagde technische verversing is geen curatoriële kwaliteitscontrole.

De huidige snapshot is een begrensde zoekselectie, geen volledige export van de circa 400.000 foto's die het Nationaal Archief op zijn informatiepagina vermeldt. De actuele recordtelling en peildatum staan in `assets/nationaal-archief.json`.

## 9. Correcties

Een inhoudelijke correctie moet waar mogelijk bevatten:

- link naar het oorspronkelijke object- of archiefrecord;
- veld dat volgens de melder onjuist is;
- onderbouwing uit een primaire bron of gedocumenteerd onderzoek;
- onderscheid tussen vaststaand gegeven, bronclaim en hypothese.

Wijzig een plaats, datum, persoon, eenheid of gebeurtenis niet uitsluitend op basis van gelijkenis, vermoedens of een onderschrift uit een andere kopie.

## 10. Bekende beperkingen

- Wikimedia Commons levert live beeldresultaten. Nationaal Archief en Rijksmuseum leveren lokale metadata-snapshots; bij het Rijksmuseum worden uitsluitend beelden getoond met expliciete beeldlicentie PD Mark 1.0 of CC0 1.0.
- KITLV, Utrechts Archief, NIMH, Wereldmuseum, Het Nieuwe Instituut, Europeana, Delpher en Atlas of Mutual Heritage zijn als externe onderzoeksingangen opgenomen. Een koppeling is geen API-integratie.
- De automatische labels moeten worden beoordeeld en verfijnd; ze zijn geen vervanging van menselijke geschiedkundige controle.
- De volledigheid van de beeldcollectie is niet vastgesteld.
- De 4.000 Nationaal Archief-records en 229 Rijksmuseum-objecten vormen begrensde zoekselecties. De 148 KNIL-bewapeningsrecords zijn controleerbaar terug te voeren op de exacte bronmetadata-snapshot, maar hun visuele inhoud en wapentypen zijn niet allemaal onafhankelijk aan de originele scan getoetst. De website presenteert ze daarom niet als onafhankelijk vastgestelde identificaties.
- Voor de 4.000 Nationaal Archief-records is geen beeldrechtenvrijgave afgegeven; alle 4.000 blijven metadata-only. De 14 Rijksmuseum-records zonder beeldlicentie blijven eveneens metadata-only. De 215 overige Rijksmuseum-beelden en de live Commons-resultaten worden alleen getoond wanneer de expliciete rechtenallowlist slaagt.
- De geautomatiseerde responsive browsercontrole, axe-core WCAG 2.1 A/AA-controle en mobiele Lighthouse-gates zijn op 13 november 2026 geslaagd; dit is geen onafhankelijke menselijke toegankelijkheidsaudit.

Deze beperkingen worden bewust zichtbaar gehouden om schijnzekerheid te voorkomen.
