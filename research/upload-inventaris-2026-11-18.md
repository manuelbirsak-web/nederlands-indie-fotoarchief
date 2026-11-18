# Uploadinventaris en herverdeling — 18 november 2026

## 1. Resultaat van de GitHub-inventarisatie

Alle bestanden in de volledige `main`-boom zijn geïnventariseerd. De nieuwe CBG-scans stonden in `assets/family/`, hoewel het paspoortaanvragen zijn. Ze zijn verplaatst naar `assets/paspoortaanvragen/originelen/`. Twee niet-paspoortscans zijn apart gezet. Exacte duplicaten zijn verwijderd; de originele bytes van de behouden bestanden zijn niet aangepast.

| Bestandssoort | Nieuwe locatie | Resultaat |
|---|---|---|
| CBG Indisch Oud-Paspoortarchief | `assets/paspoortaanvragen/originelen/` | 16 unieke scans, manifest en webgalerij toegevoegd |
| Ambtenarenstamkaarten, toegang 2.10.36.21 | `assets/ambtenaren/` | Scan apart geplaatst; persoonskoppeling nog controleren |
| Burgerlijke stand, toegang 0335-01 | `assets/burgerlijke-stand/` | Scan apart geplaatst; persoon/akte nog identificeren |
| Alternatieve ambtenarenkaartweergave | `assets/ambtenaren/varianten/` | `NL-HaNA_2.10.36.21_17_0151-groot.jpg` behouden als variant; niet als tweede archiefstuk geteld |
| Familiefoto's | `assets/family/` | De twee eerder opgeslagen originele familiefoto's blijven hier |
| KNIL/internerings- en transportdocumenten Hubert | `assets/hubert-birsak/` | Bestaande originele scans blijven hier |

## 2. CBG-scans

Er zijn 16 unieke CBG-scanbestanden behouden en verplaatst. De CBG-code is een bron-/scanidentificatie, niet automatisch een persoonsidentificatie.

- B13305 — Arnold Wilhelm Birsak (gekoppeld vanuit CBG-vermelding)
- B13369 — Wilhelmina Johanna “Mien” Takken (gekoppeld vanuit CBG-vermelding)
- B13299, B13307, B13311, B13317, B13323, B13325, B13333, B13361, S05373, S18889, S18895, S18925, S19075 en T02255 — nog niet aan personen gekoppeld.

Vier alternatieve bestandsnamen bleken exacte duplicaten van een canoniek bestand: B13333 2, B13369 2, S18889 2 en S18925 2. Ze zijn niet als extra documenten meegeteld. Zeven CBG-bestanden stonden daarnaast als exacte kopieën in de repository-root; die rootkopieën zijn verwijderd nadat de bestanden in de juiste map waren geplaatst.

Zie `assets/paspoortaanvragen/manifest.json` en de [paspoortgalerij](paspoortaanvragen.html).

## 3. Nieuwe bestanden die in deze chat zijn aangeleverd

| Bestand | Inhoud / behandeling | GitHub-status |
|---|---|---|
| `IMG_7918.jpeg` | Paspoortkaart die visueel “Birsak, Ernanie Ernest” lijkt te vermelden; 10-07-1877, Djokjakarta; twee portretfoto's. Rapport koppelt dit aan BD 2262 / paspoort 904643. | Transcriptie-/onderzoeksnotitie verwerkt; originele binaire upload nog niet naar GitHub overgebracht |
| `IMG_5110.jpeg` | Tweede, afzonderlijke kleurenfamiliefoto met 16 genummerde personen; bijschrift getranscribeerd in genealogisch dossier | Transcriptie verwerkt; origineel nog niet naar GitHub overgebracht |
| `IMG_7922.jpeg` | Screenshot Janssen's Indisch Repertorium, versie 2016, Birsak/Birzak-index | Leesbare verwijzingen verwerkt in genealogisch dossier; screenshot zelf niet in repository |
| `IMG_4160.png` | Google AI-overzicht over stamboeknummer 123508 | Alleen als zoekspoor geregistreerd; niet als bewijs gepubliceerd |
| `IMG_4161.png` | Screenshot van officiële Nationaal Archief-inventaris 2.13.108 | Officiële archieflink opgenomen; screenshot zelf niet in repository |
| `NL-HaNA_2.13.108_13_0030.jpeg` | Exacte kopie van `IMG_4163.jpeg` | Geen tweede bestand aangemaakt |
| `NL-HaNA_2.13.108_13_0031.jpeg` | Exacte kopie van `IMG_4162.jpeg` | Geen tweede bestand aangemaakt |
| `IMG_7919(1).jpeg` | Byte-identieke kopie van `IMG_7919.jpeg` | Niet als tweede scan toegevoegd |
| `Archiefonderzoek_Familie_Birsak.pdf` | Rapport over E.E. Birsak, paspoortnummers 904642/904643/904645, familie en archiefvindplaatsen | Inhoud verwerkt; oorspronkelijke PDF niet naar GitHub overgebracht |
| `pdfcoffee.com_nederlandsche-krijgsgevangenen-pdf-pdf-free.pdf` | Historische namenopgave met H.M. Birsak 123508 en andere Birsak-vermeldingen | Transcriptie en bronkritiek verwerkt in `research/krijgsgevangenen-bronnen.md`; oorspronkelijke PDF niet naar GitHub overgebracht |

## 4. Afgeleide werkbestanden — niet als originelen publiceren

De volgende bestanden zijn afgeleide contactbladen, uitsneden, zoombeelden of presentaties en worden niet als origineel archiefstuk gepresenteerd:

- `contact.jpg`
- `hubert-birsak-documenten-overzicht.jpg`
- `hubert-birsak-documenten-overzicht-small.jpg`
- `passport-top-zoom.png`
- `ernest-ernest-birsak-krantenfragment.jpg`
- `ernest_ernest_birsak_detail.png`
- `ernest_ernest_birsak_krantenknipsel.png`
- `ernest_ernest_birsak_uitgelicht.png`

Deze werkbestanden zijn niet als nieuwe originele documenten in de repository opgenomen.

## 5. Nieuwe bronbevindingen

### Krijgsgevangenenlijst

De aangeleverde PDF *Nederlandsche krijgsgevangenen* bevat:
- PDF p.18 (gedrukte p.8): Jacobus Marinus Birsak — 57511 — Soldaat.
- PDF p.27: H.M. Birsak — 123508; J.M. Birsak — 57512; F.A. Birsak — 24812; L.F.W. Birsak — 97757; W.I. Birsak — 96687.
- Op p.27 staat 57515 bij M. Reehorst, niet bij Birsak.

De afwijking 57511/57512 blijft onopgelost.

### Janssen's Indisch Repertorium

De Birsak-verwijzingen uit de screenshot zijn getranscribeerd in `research/familie-birsak-genealogie.html`. Eén slecht leesbare extra verwijzing rond p.142 is bewust niet overgenomen.

### Familieportret met 16 personen

Het bijschrift van `IMG_5110.jpeg` is overgenomen in het genealogische dossier. De namen zijn geen automatische gezichtsidentificaties. Datum, plaats en verwantschappen zijn nog niet vastgesteld.

## 6. Technische beperking bij de laatste uploadstap

De GitHub-verbinding in deze sessie kan repositorybestanden lezen, verplaatsen en tekstbestanden schrijven, maar biedt hier geen binaire uploadactie voor de lokaal aangeleverde JPEG/PNG/PDF-bestanden. Daarom zijn `IMG_7918.jpeg`, `IMG_5110.jpeg`, de screenshots en de twee PDF's inhoudelijk verwerkt waar mogelijk, maar niet als binaire bestanden in GitHub geplaatst. Er zijn geen niet-werkende afbeeldingslinks aangemaakt en er wordt niet beweerd dat deze bestanden al online staan.

## 7. Validatie

Na de herverdeling moeten de volgende controles slagen:
- alle 16 CBG-scans bestaan op hun nieuwe locatie;
- alle 16 worden in de paspoortgalerij getoond;
- geen CBG-scan staat nog in `assets/family/` of de repository-root;
- de twee bestaande familiefoto's blijven intact;
- de twee transportlijsten blijven intact en in de juiste volgorde;
- alle lokale HTML-afbeeldingspaden bestaan;
- GitHub Pages-deploy slaagt;
- browser- en WCAG-audit slaagt.
