# 4. Del A: miljöbeskrivning

Jag kör  Canonical Ubuntu Version 26.04 och har oracle cloud som min moln leveranter och det är dem som kör min VM. min vm har regionen stockholm. min vm är av typen VM.Standard.E2.1.Micro. Jag kör alltså en riktig linux maskin genom oracle cloud vilket ger mig samma förutsättningar som att ha linux på min egna dator

## Nätverksinterface

Jag har två typer av nätverks interface på min linux maskin. lo och ens3

lo är loopback delen som används när datorn behöver kommunicera med sig själv och går aldrig ut på internetet eller nätverket.

ens3 är det interface som används för att nå andra enheter på nätverket men också internet. Den har funktionen att skicka broadcast till nätverket och specifika grupper om det behövs. här finns det en riktig ethernet adress som ser ut ungefär såhär MAC-adress- 01:00:11:01:x1:x1 brd (broadcast) ff:ff:ff:ff:ff:ff. inet 10.x.x.x/24 som är min privata ipv4 adress. inet6v som är ipv6 adressen ser ut ungefär såhär xx80::17xx:xxxx:x94x/64.

Min dators publika ip adress ser ut såhär 78.xx.xxx.xxx
Ip adressen för servern (min VM på oracle cloud) 158.xxx.xxx.xx.

### Hur skiljer sig dem olika ip adresserna?

lokal ip adress används bara för att kommunicera på din dator/enhet den kan inte kontakta någon utanför den med denna ip adress.

privat ip adress är ett steg upp i ordningen och denna kan kommunicera med andra enheter inom samma subnätverk.

Om du sedan vill gå ut och kommunicera på internet så går förfrågan från en enhet till routern som med hjälp av NAT omvandlar din privata ip adress till sin egna publika ip adress som syns utåt.

### Begränsningar: 

Jag bör inte ha några begränsningar sett till just denna uppgiften då jag använder oracle cloud som uppgiften utgår ifrån och.

# 5. Del B: manuella observationer

| Konrollområde | Input| Resultat/förklaring |
|-----------|-----------|-----------|
| ip | Hostname -I | Hostname skriver i grunden ut systemet/hosten du kör systemet på men med flaggan -I listast endast ip adresser som är kopplad till hosten. jag fick då fram min egen ip som va enligt förväntan för det är den enda som ska vara kopplad till min VM |
| Interface | ip address | Här får jag upp 2 interfaces. lo och ens3. under lo finns 4 adresser inet 127.0.0.1/8 och inet6 ::1/128 det är alltså en ipv4 adress och en ipv6 adress, sen står det även en mac och en broadcast adress men de används inte på lo. Under ens3 interface finns även där 4 adresser en ipv4 och en ipv6 men ens3 är adresser som fungerar på nätverket. en mac adress och en brd adress |
| Routing | ip route | Standard är via gatewayen 10.0.0.1 och genom dev ens3 som interface. |
| DNS | getent hosts | Ja. Med hjälp av getent hosts example.com så skickades en förfrågan till en DNS server som i sin tur skickade tillbaka två ipv6 adresser som är kopplade till example.com |
| Portar och tjänster | ss -tuln | På min vm är det totalt 6 adresser som lyssnar men det är dubbelt då 22 och 111 lyssnar på både ipv4 och ipv6 och så är det dubbla på dns resolvern. port 22 är ssh och används för att fjärrstyra en enhet. 111 är rpcbind och betyder att du kan anropa en annan dator om funktioner eller program som om den vore din egen. port 53 är dns resolvern som lyssnar efter förfrågningar och det den gör är att ge dig ip adresser på dem domännamn du frågar efter. |
| Lokal tjänst | curl http://localhost:8080 | Ja servern går att nå. när jag kör curl kommandot så hämtas en fillista som finns i den mappen jag hostade servern på, i detta fall min egen mapp. |
| Process eller systemstatus | ps aux \| grep ssh | här får jag först upp alla processer som körs just nu på min VM och med hjälp av pipelinen grep ssh listas endast dem som har ordet ssh.Då får jag upp 3 processer en listener som lyssnar efter inkommande ssh ansluningsförsök, två session rader PID 1894 och 1971 som är kopplade till min egen ssh anslutning. |

# 8. Del D: testning

| Test | Förväntat resultat | Faktiskt resultat | slutsats |
|-----------|-----------|-----------|-----------|
| Normalfall 1: loop för DNS kontroll | DNS uppslag fungerar och scriptet loggar OK| Scriptet loggade status OK för example.com google.com och github.com | Loopen och DNS kontrollen fungerar som tänkt med flera domännamn i samma körning. |
| Felfall 1: TEST_PORT tom | Skriptet bör upptäcka att värdet är tomt och avbryta  utan krasch och logga det som en FAIL | Scriptet loggade FAIL "TEST_PORT är inte definierad" och fortsatte med resten av scriptet | Tack vare kontrollen i scriptet som kollar om värdet för port kollen är tom så undviker jag att felkoder eller krascher sker.
| Felfall 2: Ingen tjänst på porten | Skulle det vara så att lokala servern som jag måste starta själv inte är igång eller inte nås av scriptet bör jag få felkoden "FAIL" "Lokal tjänst på port $TEST_PORT är inte tillgänglig" | Skriptet loggade FAIL "Lokal tjänst på port 8080 är inte tillgänglig" | Felhanteringen i scriptet fungerar vid uppkommna fel |
| Normalfall 2: lokal test tjänst svarar? | Om jag nu har startat test servern innan jag kör scriptet borde det loggas som OK med port numret |  Skriptet loggade OK "Lokal tjänst på port 8080 är tillgänglig", och port 8080 syns i LISTEN-läge i 
port översikten| Lokal tjänstekontroll delen i skriptet fungerar som det ska om lokaltjänsten är igång. |

# 9. Del E: CIA-analys

###Konfidentialitet:

nätverksutdata som kan vara känsliga enligt mig var samtliga ip-adresser, mac adresser, vilka portar som är öppna, hostname eller instans namn. I rapporten har jag valt att sanera ip adresserna då det bara är strukturen och typen av ip adress som är relevant. Medans i skriptet valde jag att ta med bara ip adresserna med grep "inet" men inte mac adressen.Mac adresen har ingen större nytta för läsaren eller personen som använder scriptet och relativt begränsad nytta för en angripare så jag valde att inte ta med det alls i skriptet. Vilka portar som är öppna kan vara en säkerhetsrisk men det är också hela poängen med skriptet att se själv vilka som är öppna så därav måste dem vara med.

### Integritet:

I detta skript finns det en log funktion inbyggt i skriptet vilket gör att resultatet sparas och går att granskas i efterhand. Det finns även Github evidens i form av commits som visar hur scriptet har byggts upp och även en "backup" på github om skriptet på vscode eller min VM skulle försvinna. Testerna är automatiserade vilket gör att alla kontroller genomförs och du kommer inte av misstag glömma en av kontrollerna som skulle kunna bli en säkerhetsrisk. Skriptet har även tydliga OK eller FAIL statusar som gör att man kan lägga in räkninefunktioner där bash räknar ihop hur många fel de är och om man vill läsa i loggen så kan man söka efter ordet FAIL vilket påskyndar processen av felsökning.

### Tillgänglighet: 

i skriptet används getent hosts för att hämta IP-adresserna till domännamn och får jag tillbaka ip adresser så ser jag att den funktionen fungerar och är nåbar. ip route används för att visa standard vägen ut på internet skulle inte den vara tillgänglig eller finnas så kommer jag inte kunna ha kontakt med internet alls. När jag har igång lokal servern/tjänsten används curl kommandot för att hämta information därifrån och får jag information tillbaka bevisar detta att servern svarar och är igång. Port kontrollen visar vilka portar som är öppna och lyssnar efter inkommande kommandon/frågor och de berättar i sin tur vilka tjänster som är tillgängliga. Exempel på det kan vara att jag ser att port 22 är på listen och då tyder det på att min VM är öppen och lyssnar efter nya anslutningar.

### Avvägning: 

En säkerhetsåtgärd som skulle kunna göra min VM i detta fallet helt onåbar hade varit att konfigurera brandväggen med för hårda krav, att stänga av port 22 alltså ssh anslutningen då det är så jag styr min vm.

# 10. Del F: reflektion och förbättring

Spontant känns ss -tuln (port översikten) mest värdefull. Att kontrollera till exempel domännamn via DNS är ingen direkt säkerhetsåtgärd i sig, snarare ett sätt att se om en funktion är tillgänglig. Port översikten däremot visar saker som jag inte kanske har full koll på annars, till exempel vilka portar som är öppna i onödan för om jag ändå inte använder en port så är det en onödig del av attack ytan för angripare.

miljöskillnad: jag skulle inte säga att jag har blivit påverkad av någon miljöskillnad då jag använder oci som det är menat att man ska göra. Dock är de lite tröttsamt att Jag varje gång måste gå in och starta min VM och sedan logga in via ssh som känns väldigt upprepande.

Svårtolkat fel: jag fick syntax error flera gånger men en av dem var på en if sats som jag inte förstod då felet var på rad 30 enligt men jag hittade inget fel för jag hade satt fi för att avsluta if satsen. Med hjälp av ai såg jag att det berodde på att jag hade en if sats i if satsen så det behövdes två st fi i slutet av skriptet vilket jag själv hade missat.

Version 2 förbättring: I version 2 skulle jag först lägga till en del i skriptet som tar med tidsstämplar på loggen för att underlätta granskningen och integriteten i skriptet. Jag skulle även göra så den lokala servern automatiskt startar upp så jag slipper göra det, och om jag automatiserar uppstart av servern vill jag lägga till nedstängning som en del av cleanupen.

Verklig drift eller säkerhetsprocess: Jag tänker att man skulle kunna ha detta script schemalagt som en rutin varje gång datorn startas upp eller när den har varit igång en stund som en säkerställning att nätverksfunktioner fungerar. Det skulle också kunna vara en del av rutinen om en dator kraschar att scriptet körs för att säkerställa att de mest grundläggande nätverksfunktioner funkar vid start igen. Viktigt är att det inte används för att scanna hela nätverk eller andra datorer än din egen.
