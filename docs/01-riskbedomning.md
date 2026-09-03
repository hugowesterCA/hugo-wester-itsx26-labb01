# 01 Riskbedömning

## Instruktion

Välj minst tre observationer från labben. Beskriv varje observation, koppla den till CIA-triaden och föreslå en rimlig åtgärd.

Jag gjorde riskbedömningen utifrån main.py

| Observation | Påverkan på CIA | Riskbeskrivning | Föreslagen åtgärd | Prioritet |
|---|---|---|---|---|
| ValueError vid fel indata skriver ut fullständig traceback | Konfidentialitet | Tracebacken skriver ut fullständig filsökväg, radnummer och den exakta kod raden, en eventuell anfallare bör inte få se detta | Lägg till try/except i koden för att skriva ut ett mer generellt meddelande istället för hela tracebacken | Medel |
| Anrops begränsning | Tillgänglighet | I programmet saknas en anrops begränsning vilket gör den öppen för DoS attacker som skulle kunna krascha servern eller programmet som scriptet befinner sig på | Implementera en anrops begränsning | Låg |
| Ingen logning av anrop/fel | Integritet | Det saknas en log funktion som visar vad som angav av vem eller vr ett fel uppstod, vanliga loggar på maskinen visar inte denna typ av log | Skriv in en del i scriptet som skapar loggar och lagrar | Låg |
|  |  |  |  |  |

## Reflektion

Beskriv kort hur du prioriterade riskerna.

Risk 1: Angav jag som medel då det inte akut utsätter systemet för fara eller ger ut väldigt känslig data men det kan ge angripare en aning om hur koden är uppbyggd och på så sett kan de ge ideer om vart dem ska fortsätta sin attack.

Risk 2: Då skriptet nu är isolerad på min dator och ingen annan än jag kan komma åt den är risken väldigt liten men skulle detta va en del av ett större program och internet kopplat kan en attack utifrån få systemet att krascha.

Risk 3: Vid omstart eller krasch av programmet kommer alla loggar i kommando rutan försvinna och då finns det inga logar och ingen spårbarhet om varför kraschen hände om de kan berått på exempelvis en dos attack eller vad som matades in i service_name därför finns noll spårbarhet om scriptet. Viss loggning finns i maskinen själv men anger inte detaljerat om vad som matats in i skriptet därför satte jag risken som låg.
