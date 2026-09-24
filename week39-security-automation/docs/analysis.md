## Rådata:

| Filsökväg | Loggrad |
|---|---|
| data/auth.log | 2026-09-24T08:15:03Z auth Failed login user=admin src=203.0.113.15 |
| data/auth.log | 2026-09-24T08:15:07Z auth Failed login user=root src=203.0.113.15 |
| data/auth.log | 2026-09-24T08:15:12Z auth Failed login user=admin src=203.0.113.15 |
| data/firewall.log | 2026-09-24T08:16:22Z DENY src=203.0.113.15 dst=10.0.0.10 port=22 |
| data/access.log | 2026-09-24T08:21:02Z src=203.0.113.15 method=GET path=/login status=401 |
| data/access.log | 2026-09-24T08:21:06Z src=203.0.113.15 method=POST path=/login status=401 |
| data/suspicious_ips.txt | 203.0.113.15 |

Raderna från auth.log och firewall.log är hämtade av programmet.

Raderna från access.log hittade jag vid manuell granskning, eftersom programmet
inte analyserar den filen.

## Observation:

- Det jag la märke till var att programmet listade adressen "203.0.113.15" 3 gånger inom loppet av 9 sekunder i auth.log både som root och admin. Sen såg jag att i firewall fick den deny på port 22 som används för fjärrstyrning. Detta väckte misstankar så jag valde att manuellt granska access.log filen. Där har samma adress gjort först en GET förfrågan och sen en POST förfrågan men fått felkod 401 alltså nekad åtkomst inom loppet av 4 sekunder.

## Slutsats: 

- Detta skulle kunna tyda på ett brute force-försök. Det jag tycker är udda är att samma IP-adress gör flera försök mot olika användarnamn på så kort tid samt att adressen förekommer i samtliga loggfiler samt suspicious_ips.txt.

## Osäkerhet: 

- Programmet räknar enbart misslyckade inloggningsförsök och anslutningar, så utan manuell granskning ser jag inte om adressen fick en lyckad anslutning eller inloggning. Oklart om IP-adressen är en person eller ett automatiserat program/skript. Jag vet heller inte varför just denna IP-adress är listad i IOC-listan. Analysen omfattar bara den period loggarna täcker, och vad som hänt innan eller efter har jag ingen aning om, men det skulle vara intressant att veta om adressen dyker upp fler gånger.

## Alternativ förklaring:

- En alternativ förklaring till att adressen dyker upp på så många ställen skulle kunna vara att det är ett auktoriserat pentesting försök som ju faktiskt kan se identiskt ut med ett vanligt bruteforce försök.

## Säkerhetsbetydelse:

- Att samma adress dyker upp i alla tre loggfilerna inom sex minuter, och dessutom finns i IOC-listan, gör det här mer värt att titta på än en enstaka misslyckad inloggning. Att försöken riktades mot admin och root, alltså konton med höga behörigheter, och att adressen även testade port 22 för fjärrstyrning gör att det bör prioriteras relativt högt.

- För att komma vidare skulle jag vilja veta om adressen förekommer utanför den period loggarna täcker, om något försök från den lyckades och om ett auktoriserat säkerhetstest var inbokat vid dehär tillfället. Det sista skulle förklara hela mönstret utan att något olagligt hänt.

- Jag skulle inte blockera adressen direkt utifrån det här underlaget. Om det är ett pentest eller en intern tjänst med gamla inloggningsuppgifter kan en blockering ställa till mer problem än den löser. En träff i IOC-listan är ett skäl att undersöka närmare, inte ett bevis.