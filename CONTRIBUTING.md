# Bijdragen en correcties

Indisch Beeldarchief is een onderzoeksstartpunt. Bijdragen moeten herleidbaar, controleerbaar en zorgvuldig met beeldrechten omgaan.

## Een fout melden

Meld bij voorkeur:
1. de directe URL van het oorspronkelijke archief- of objectrecord;
2. de huidige tekst of het huidige label dat fout lijkt;
3. de gewenste correctie;
4. de primaire bron of toelichting waarop de correctie berust.

Geef bij onzekere gegevens aan dat het om een hypothese gaat. Vermeld geen persoonsnaam, eenheid, datum of exacte locatie als die niet uit het record of onafhankelijk bewijs volgt.

## Een afbeelding toevoegen

Voeg geen bestand toe voordat is vastgesteld:
- waar het oorspronkelijke bestand wordt beheerd;
- wie de maker is, voor zover bekend;
- welke licentie of rechtenverklaring geldt;
- welke naamsvermelding vereist is;
- of downloaden, tonen en herpubliceren zijn toegestaan.

Een record met CNE / Copyright Not Evaluated of een vergelijkbare aanduiding is niet automatisch rechtenvrij. Link in dat geval naar het origineel en publiceer geen kopie of thumbnail.

## Metadata en classificatie

- Behoud de oorspronkelijke beschrijving als bronbeschrijving; herschrijf die niet alsof zij een neutrale, geverifieerde conclusie is.
- Houd opnamejaar, publicatiejaar, scanjaar en uploadjaar uit elkaar.
- Ken KNIL alleen toe wanneer de bronbeschrijving dat ondersteunt.
- Ken Bersiap alleen toe wanneer de bronbeschrijving de term expliciet gebruikt. Een jaar tussen 1945 en 1950 is op zichzelf geen bewijs.
- Gebruik historische plaatsnamen en moderne aliassen om zoeken te verbeteren, maar markeer een plaats niet als bewezen opnamelocatie zonder onderbouwing.
- Verwijder dubbele records op basis van de permanente objectidentificatie, niet alleen op basis van gelijke titels.

## Technische bijdrage

Voorstelprocedure:
1. wijzig code of metadata in een afzonderlijke commit;
2. voeg een reproduceerbare test toe voor nieuw gedrag;
3. voer de validatie en unit tests uit;
4. controleer de live weergave op desktop en mobiel;
5. controleer de oorspronkelijke bronlink en rechteninformatie.

De GitHub Actions-workflow voert vóór publicatie de statische contractchecks, classificatietests en JavaScript-syntaxcontrole uit. Een groene workflow bewijst niet dat alle historische claims of gebruiksrechten zijn geverifieerd.
