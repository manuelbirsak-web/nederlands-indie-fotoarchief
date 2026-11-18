# Release notes

## 1.4 — 18 november 2026

### Correctie persoonsidentificatie Hubert Manuel Birsak
- Nieuwe grafregistratie (online-begraafplaatsen.nl, graf-ID 1526078, St. Petrus Kerk Bergen) toont Hubert M. Birsak, geboren 09-05-1908 en overleden 12-07-1970.
- De gekoppelde registratie noemt echtgenote Theresia Atjih (15-05-1927 – 17-06-1998), waarmee de familiekoppeling wordt ondersteund.
- “Wilbert” wordt niet langer als geldige naamvariant of zoeknaam gebruikt. De eerdere transcriptie van paspoortkaart/rapport wordt als vermoedelijke lees- of transcriptiefout aangemerkt; de originele paspoortkaart moet opnieuw worden gecontroleerd.
- De geboortedatum 09-05-1908 wordt ondersteund door zowel de grafregistratie als de Japanse registratiekaart; de oude rapportdatum 08-05-1908 wordt als vermoedelijke transcriptiefout gemarkeerd.
- De aangeleverde screenshot IMG_7921 is inhoudelijk verwerkt; het binaire origineel is nog niet naar GitHub overgebracht.

## 1.3 — 18 november 2026

### Nieuwe primaire bronnen Hubert Manuel en E.E. Birsak
- Japanse registratiekaart IMG_7923 inhoudelijk gelezen: getypte “Birsak, H.M.”, handgeschreven “Hubert Manuel”, stamboeknummer 123508, vader “Birsak, E.E.” en eenheidsaantekening die lijkt te lezen “Inf. XV Bandoeng”.
- De bronvariant “Wilbert Manuel” op paspoortkaart 904645 en in het onderzoeksrapport is niet verwijderd of stilzwijgend gecorrigeerd. De naam- en geboortedatumafwijkingen (8 versus 9 mei 1908) zijn als open bronconflict gedocumenteerd.
- Haagsche Courant van 14 juni 1906, nr. 7143, PDF-pagina 2: E.E. Birsak wordt genoemd als klerk bij de S.S. op Java, benoemd tot telegraafopzichter en geplaatst op de Westerlijnen.
- Uploadinventaris aangevuld met IMG_7923 en resolve.pdf. Beide originelen zijn nog niet als binaire GitHub-assets geplaatst.
- Genealogisch en militair dossier uitgebreid met de nieuwe bronlezingen.

## 1.2 — 18 november 2026

### Archiefstructuur en nieuwe bronnen
- Alle mappen van de hoofdbranch geïnventariseerd; 16 unieke CBG-scans verplaatst van de familiefotomap naar `assets/paspoortaanvragen/originelen/`.
- Vier exacte dubbele CBG-bestandskopieën en zeven identieke rootkopieën verwijderd; originele bytes van de behouden scans zijn ongewijzigd.
- CBG-manifest, mapinstructies en een galerij met alle 16 originele scans toegevoegd. Alleen B13305 (Arnold Wilhelm Birsak) en B13369 (Wilhelmina Johanna Takken) zijn voorlopig aan personen gekoppeld. Per scan moet de openbare CBG-beschikbaarheid en privacytoestemming nog individueel worden gecontroleerd voordat herpublicatie als definitief vrijgegeven geldt.
- Scan uit Nationaal Archief 2.10.36.21 apart geplaatst in `assets/ambtenaren/`; scan uit toegang 0335-01 apart geplaatst in `assets/burgerlijke-stand/`. Persoons-/akte-identificaties blijven open.
- Nieuwe 16-persoonsfamiliefoto (IMG_5110) en aanvullende paspoortkaart Ernanie (IMG_7918) inhoudelijk verwerkt; de originele binaire uploads zijn nog niet naar GitHub overgebracht.
- Janssen's Indisch Repertorium-verwijzingen toegevoegd aan het genealogische dossier.
- Historische namenopgave *Nederlandsche krijgsgevangenen* getranscribeerd: H.M. Birsak 123508, J.M. Birsak 57512, F.A. Birsak 24812, L.F.W. Birsak 97757, W.I. Birsak 96687; Jacobus Marinus Birsak 57511 op een andere pagina. Het conflict 57511/57512 blijft expliciet open.
- Uploadinventaris en bronkritische transcriptie toegevoegd.

### Validatie en kwaliteit
- Statische validatie uitgebreid met controles op de 16 CBG-bestanden, manifest, beeldpaden en nieuwe Birsak-bronvermeldingen.
- Browseraudit aangepast zodat lazy-loaded familiefoto's eerst in beeld worden geladen voordat ze worden gecontroleerd.
- Live publicatie en browseraudit moeten na deze commit opnieuw worden bevestigd.

## 1.1 — 12 november 2026

### Familieonderzoek en Deep Search
- Nieuwe familierubriek met het aangeleverde Birsak-familieportret en transcriptie van de 14 namen.
- Multi-source Deep Search-ingang voor adres-, plaats-, persoons- en genealogische zoektermen.
- Onderzoeksbronnen toegevoegd: Indisch4ever (2011), genealogische vermeldingen van Ernanie Ernest Birsak en Arnold Willem Birsak, en posthistorische documentatie van Lembangweg 346 in 1940.
- Expliciet onderscheid tussen bronvermelding, hypothese en bewezen identificatie.
- De twee originele familiefoto's zijn opgenomen in `assets/family/`; latere aanvullende familiefoto's blijven apart geregistreerd zolang de binaire upload nog niet is uitgevoerd.

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
