# Del A: miljö och metod
• OCI: Oracle cloud instans med Canonical Ubuntu 26.04

• Jag valde att fånga ens3 interfacet därför att det står som default route och har status UP. Det är genom detta interface som all internet trafik går igenom när den ska till min instans.

• Jag valde att använda egen fångst då jag har möjligheten och jag får en chans att lära mig hur det fungerar.

• Jag begränsade fångsten i tid genom att använda kommandot "sudo timeout 30 tcpdump -i ens3 -s 0 -w traffic_week38.pcap" där timeout 3o sätter en begränsning för fångsten på 30 sec.

• pcap beskrivning finns i mappen evidense i vecka38_evidens.md. råpcap hålls lokalt.

• Förklara relevanta skillnader mot lärarens OCI-demonstration

# Del B: paketets väg

Jag valde att följa ett HTTPS-anrop mot example.com för att beskriva paketets väg från applikation till destination.

Min klient (10.0.0.80) skickar paketet/förfrågan via interfacet ens3. Innan själva anropet kan ske görs ett DNS-uppslag: paket 271 frågar efter en ipv4 adress (A) för example.com, och paket 272 svarar med IP-adresserna 172.66.147.243 och 104.20.23.154. Klienten valde att ansluta till 104.20.23.154 som syns i tcp handskakningen sedan med paket 290.

Trafiken lämnar sedan min instans via default route, som pekar mot gatewayen 10.0.0.1 på ens3. Både min klient-IP (10.0.0.80) och gatewayen (10.0.0.1) är privata adresser (inom 10.x.x.x-spannet), adresserna för destination var 172.66.147.243 och 104.20.23.154.

Eftersom min avsändaradress är privat måste en NAT-översättning (troligen med PAT) ske innan paketet går ut på internet för att byta ut min privata IP mot en publik adress som svaret kan hitta tillbaka till. Detta syns inte direkt i min pcap eftersom fångsten sker på klientsidan av NAT och inte själva översättningen så detta är inte något jag kan bevisa med pcap utan bara något som bör finnas.

På vägen ut skulle trafiken principiellt kunna stoppas av en brandvägg på minst två nivåer, dels en lokal brandvägg på min egen instans, OCIs egna säkerhetsregler. om det inte skulle vara OCI hade detta varit vid routern vid inkommande och utgående trafik. Eftersom anropet lyckades vet jag att port 443 utgående är tillåten på båda dessa nivåer, men jag ser inte reglerna själva i min pcap data.

Transportprotokollet var enbart TCP, med en komplett 3-vägs handskakning synlig i paket 290 (SYN, från klient till server), 291 (SYN/ACK, server till klient) och 292 (ACK, klient → server). Klientporten var 34230, serverporten 443.

Applikationsprotokollet var TLS. I paket 293 (Client Hello) syns en server_name-extension (SNI) som avslöjar domännamnet example.com i klartext, resten av anslutningen är krypterad.

# Del C: protokollinventering

| Protokoll | Paket nummer |Vad visar paketen | Svar på analysfrågan |
|-----|-----|-----|-----|
| DNS | Paket nr. 271/272 | Visar en förfrågan till DNS servern om rätt IP-adress, samt ett svar från server till klient med rätt IP adresser. | Namnet som efterfrågas är example.com och som svar får klienten två ipv4 adresser att välja mellan vilket betyder att det är upp till klienten att välja. Jag skulle gissa på att det är två servrar för example.com som förmodligen är till för att last balansera och backup (tillgänglighet) om den ena lägger av. |
| ICMP | 122/123 | Paketen visar att en ping skickas från min lokala ip (Type 8) till google.com (8.8.8.8) som svarar med en ping reply (Type 0).| Trafiken visar att servern 8.8.8.8 är nåbar på nätverks nivå men vad man inte helt kan veta är om webbservern funkar. |
| TCP | 71/72/73 | Paketen visar att min klient skickas en syn (paket 71) förfrågan om att öppna en anslutning, tjänsten svarar med paket 72, en syn,ack "jag vill också öppna en anslutning, nu är den skapad. Sedan paket 73 (Ack) från min klient till tjänsten som en bekräftelse om att den också är ansluten.|  Just detta paket var inte en del av trafikmix skriptet utan en bakgrunds tjänst där OCI regelbundet frågar om metadata. Endpoints var 10.0.0.80 (min klient) port 41026 och OCI endpointen va 169.254.169.254 med port 80. |
|HTTP| 280/283 | Paketen visar GET /HTTP/1.1 mot example.com med helt läsbara headers som host, user-agent och accept. Responsen visar HTTP/1.1 200 OK med headers som content-type,server och last modified. | När det gäller http så är inget krypterat vilket gör att all data i dessa paket är fullt läsabara för den som kan få tag på paketen. Detta påverkar konfidentialiteten och kan användas av angripare. |
| TLS/HTTPS | 293/295/297 | Här ser man att min privata IP skapar en förfrågan (Client Hello) till destenationen 104.20.23.154 (samma adress som dns tog fram innan) Här kan man även se SNI=example.com då detta är innan krypteringen har skett. server IPn svarar med server hello, change cipher spec, application data, min ip svarar med change cipher, appliaction data. Nu har båda sidorna bekräftat att dem är redo att gå över till krypterad data och därför heter resten av paketen application data. | Den enda metadatan som syns är först meddelandet, SNI=example.com, TLS-version, vilka krypterings metoder som klienten stödjer, Session ID. detta är läsbart eftersom krypteringen har inte skett än.

# Del D: fördjupad analys av två flöden

| Del i flödet| DNS flöde | TCP flöde |
|-----|-----|-----|
|Paketnummer| 271- request, 272- reply| syn-71, syn ack-72, 73-ack|
|källa, destination, port och protokoll|Källa=10.0.0.80,src port=50657, destination=169.254.169.254, port=53, protokoll=DNS | Källa=10.0.0.80, src port=41026, destination=169.254.169.254, port=80, protokoll=TCP|
|händelseordning| Min host IP skickar en förfrågan till destinations ip om ip adressen till example.com i form av A som är en vanlig ipv4. DNS uppslaget svarar då med två olika ipv4 adresser till detta domännamnet.| Här skickar min ip en syn förfrågan "hej jag vill öppna en anslutning till dig, destinations IPn svarar med en syn ack" jag med, nu är anslutningen igång". Sedan skickar min IP en ack till destinations IPn som en bekräftelse på att den också är ansluten.|
|förväntat beteende| En DNS-fråga skickas till DNS-servern, som svarar med en IP-adress för det efterfrågade domännamnet| En standard 3-vägs handskakning: SYN från klienten, SYN/ACK från servern, ACK från klienten som bekräftelse.|
|faktisk observation| DNS svaret innehöll två IPv4 adresser istället för bara en (172.66.147.243 och 104.20.23.154),en liten skillnad från vad jag tänkte men rimligt om jag tänker efter.| TCP paketen/anslutingen hände så som jag tänkt mig med den klassiska 3-vägs handskakningen.|
|eventuell avvikelse, timeout, reset eller retransmission| Inga avvikelser skedde vad jag kan se.| Inga avvikelser skedde vad jag kan se. |
|alternativa förklaringar| Att det finns två IP adresser till example.com skulle också kunna vara att det är två olika serverplatser geografiskt och att det är upp till klienten att välja den närmaste. | Jag konstaterade tidigare att paketen 71-72-73 inte va en del av trafikmix skriptet och en förklaring till det skulle kunna vara att det är automatisk förfrågan för att uppdatera systemet om förendringar sker men en alternativ förklaring skulle kunna vara att förfrågan triggades av någon händelse på instansen om nätverket ändrades eller någon annan förendring skedde i bakrunden på instansen|
|vad mer som skulle behövas för en säkrare slutsats| För att veta varför example.com har två ipadresser skulle man kunna se om deras nätverksarkitektur finns dokumenterad någonstans. | För att se varför denna tcp anslutningen skedde automatiskt av OCI skulle jag kunna gå till instansens egna loggar, eller jämföra om de finns något mönster i pcap om den dyker upp efter en viss tid liknande.|

# Del E: krypterat och okrypterat

| Aspekt| HTTP | TLS/HTTPS |
|-----|-----|-----|
| Synlig metadata| På HTTP protokollen saknas kryptering helt vilket betyder att vem som helst som fångar dessa paket kan läsa fullständig metadata som exempel vilken domän eller webbplats, exakt vilket verktyg och version klienten använde, vilket format klienten accepterar, vilket typ av innehåll paketet har, senaste förändring på sidan, tidsstämpel för svaret.| Här kan du bara se meta data före krypteringen sker så i första förfrågan från klienten kan man se SNI=domännamn, Session ID,TLS-version som föreslås, vilka krypteringsmetoder klienten stödjer, från server hello paketet kan man se vilken kryptering som faktiskt användes. du ka näven se ip adresser, portar, paketstorlek. Innehållet av paketen är däremot krypterade.|
| Läsbar applicationsdata| På http kan du se hela innehållet av paketet, tex kunde jag se hela HTML sidan på ett paket.| Om jag försöker se applikations datan på TLS står det bara Encryptet application data och innehållet finns men är helt oläsbart pga krypteringen. |
| Felsöknings värde | HTTP gör felsökningen väldigt smidig då du kan se allt innehåll som serverns status eller andra fel.| Här blir det svårare att felsöka då allt är krypterat, de enda du kan se är om anslutningen lyckades, och vilken kryptering som användes. |
|Konfidentialitetsrisk| HTTP är läsbart för vem som helst som får tillgång till paketen och då ser dem min privata ip, serverns ip. Framför allt ser dem exakt vad jag bad om och vilket verktyg jag använde och vilken sida jag försökte komma åt.| På TLS ser du mindre men fortfarande SNI=domännamnet och detta kan hjälpa angripare kartlägga vilka sidor du besöker men också avgöra om det är värt att försöka av kryptera datan eller börja gå andra vägar för att angripa dig på andra sätt|

# Del F: brandvägg och hardening

• Flödet jag väljer att titta på är HTTPS anropet mot example.com med destinations port:443. Den brandväggs regel som rent principiellt hade kunnat påverka denna anslutning hade varit en som tillåter utgående trafik från port 443. Eftersom TCP är "stateful" så känner brandväggen igen trafiken som från början kom från mig och då släpper den igenom trafik från samma anslutning.
• En tjänst som lyssnar lokalt säger bara att just den tjänsten är redo att ta emot förfrågningar lokalt men om den tjänstens mål är att ta emot trafik från nätverket eller internet så kommer brandväggen med största sannolikhet blockera all den trafiken såvida inte det finns en specifik regel som säger till att släppa igenom trafik på den porten som tjänsten är kopplad till. Så detta är egentligen två enskilda saker som båda måste sättas upp för att fungera tillsammans.
• Förr använda man inte default deny principen vilket var väldigt riskfyllt, då allt va öppet om du inte valde själv att blockera något medans idag använder man default deny som säger att allt ska vara stängt om inte annat anges vilket är mycket säkrare för då minimerar man alla attackytor och öppnar bara dem som är nödvändiga för din använding (detta brukar kallas least privilege).
• Först har vi trafikmix skriptet som skapade, ICMP, DNS uppslag, http och HTTPs. Alla här är såklart nödvändiga för att testa funktionerna och nätverksfunktioner. Sedan fann jag lite bakrundstjänster som gick utan att jag visste det innan jag gjorde pcap fångsten. Då hittade jag ssh anslutningen som hela tiden lyssnar efter mina anrop vilket är väldigt nödvändigt då jag styr min VM utifrån det. Sedan fann jag att OCIs metadata tjänst kontinuerligt skickar HTTP GET anrop till min instans vilket innebär att den metadata skickas okrypterat men eftersom informationen stannar på deras interna nätverk och inte vidare på internet vad jag ha kunnat se så är risken låg att någon får tag på informationen. Då skulle någon behöva komma åt deras interna nätverk så risken är då mindre. Sammanfattningsvis så tycker jag att dem tjänster o flöden som finns och jag hittat är rimliga för min labbmiljö där jag ska testa just det som jag hittat, om jag ska påpeka något så skulle det vara att man hade kunnat köra labben lokalt för att utesluta att meta data hamnar på OCI som jag hittade men då får jag inte lära mig att använda VM instanser som används av majoriteten företag idag.

# Del G: CIA och evidens

| Område| Svar |
|-----|-----|
| Konfidentialitet | Information i pcap som bör skyddas är speciellt JSON filen jag hittade som skickas från min instans  till OCI alltså det skickas internt inom deras nätverk, den filen innehöll exakt data om min VM, innehållet bestod av identifierare till min instans, hostname, id, geografisk plats, shape, tenantID och meta data. .I detta fall så handlar det om vad man kan läsa datapaketen som skickades och finns det en svaghet med HTTP paketen där allt innehåll är helt blottat, vilket verktyg jag använde, vilken domän jag sökte efter och hela innehållet för html sidan. Men också i TLS fallet där man i första anropet kunde utläsa SNI=example.com som tidigare nämt kan avgöra för angripare om det är värt eller inte att fortsätta angripa personen. |
| Integritet |  |
| Tillgänglighet |  |
| Evidenskvalitet |  |
