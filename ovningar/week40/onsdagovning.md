## Fakta:

* Mailet välskrivet.
* Ber mottagaren att öppna en länk.
* Mailet skickat till skoladmistrationen.

## Antaganden:

* Att det faktiskt var en angripare som skickade mailet.
* Att någon klickade på länken.
* Att perosnen angav sina inloggningsuppgifter
* Att angriparen fick tillgång till kontot.


## Tillgångar:

* Adminkonton
* Elevkonton
* E-postsystem
* Betygsystem

## händelsesteg:

1. Mailet skickas från okänd part.
2. Någon tar emot mailet och kollar på det.
3. Någon klickar på länken i mailet.(antagande)
4. Kommer in på inloggningssida som verkar betrodd och anger sina uppgifter.(antagande)
5. Angriparen får tillgång till kontot.(antagande)

## CIA

Konfidentialitet: Inloggningsuppgifter till personens konto, om personen har klickat på länken.

Integritet: Det är inte verifierat om kontot som skickade länken faktiskt är den den utger sig för att vara, den skulle kunna vara ett spoofat konto eller ett kapat konto.

Tillgänglighet: Kontot i fråga kommer förmodligen behövas stängas av och utredas. Och det kommer med största sannolikhet störa ut skolans admistriva processer.

## Risk och osäkerhet: 

* Risk: Det finns en risk att mejlet är falskt och att någon försöker lura personalen. Om någon klickar på länken kan bedragaren stjäla lösenord och få tillgång till skolans information, till exempel elevuppgifter och betyg.

* Osäkerhet: Vi vet inte säkert vem som har skickat mejlet eller om det verkligen kommer från skolans it-avdelning. Vi vet inte heller om länken är falsk eller om någon försöker stjäla lösenord och personuppgifter. Det är också osäkert om AI har använts för att skapa mejlet. Därför behöver vi kontrollera mejlet och avsändaren innan vi klickar på länken.

## Central tillgång: 

* skolans epostsystem.

Viktig CIA dimension: 