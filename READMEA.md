## Hvordan kjøre filen ved innlevering. 

Hele prosjektet mitt er 'prosjekt.ipynb', også fikser jeg sample filen i 'preprocessed.ipynb'. 

Jeg har laget den slik at den kan kjøres fra topp til bunn uten problemer. 
Prosessen blir da i rekkefølgen: 
- Leser inn data.
- Optimalisering.
- Visualisering.
- Fylle inn NaN-verdir.
    1. Fylle inn NMAR.
    2. Fylle inn MAR.
     - Gridsearch for beste imputasjon.
     - For denne har jeg gjort hyper parameter tuning først (med en enkel imputasjon for NaN), men for at det skal bli i riktig rekkefølge 
     med tanke på innlevering har jeg lagt den inn her for å samle prosessene. Slik hvis det er en annen imputasjon enn mean som er bedre, så velger jeg den.
- Hyperparameter-tuning.
- Velger ut de 3 beste modellene.
- Variabelutvinning.
- Står igjen med den beste modellen. 

Kan kjøre hele tiden, enda man setter en if-setning til True/False hvis man vil prøve forskjellie variabelutvinninger sammen. 
Har samlet koden, slik den blir fordelt på 9 hovedoverskrifter i filen. 

Hvis man ønsker oppnåde resultater som i rapporten må du sette behold_sykdomskategori=False, i starten. Deretter blir
denne skrudd på igjen når man kommer til 5.0.1 variabelutvinning, og kan derfra bli skrudd på. I rapporten skriver jeg om 
denne prosessen. Derfra er resterende if-setninger som jeg anvender skrudd på og tatt i bruk riktig. 

I tillegg har jeg kun tatt med de viktigste hyper parameterene under kjøring, slik den tar kortere tid å kjøre. 