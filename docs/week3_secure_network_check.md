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

| ip | Hostname -I | Hostname skriver i grunden ut systemet/hosten du kör systemet på men med flaggan -I listast endast ip adresser som är kopplad till hosten. jag fick då fram min egen ip som va enligt förväntan för det är den enda som ska vara kopplad till min VM |
| Interface | ip address | Här får jag upp 2 interfaces. lo och ens3. under lo finns 4 adresser inet 127.0.0.1/8 och inet6 ::1/128 det är alltså en ipv4 adress och en ipv6 adress, sen står det även en mac och en broadcast adress men de används inte på lo. Under ens3 interface finns även där 4 adresser en ipv4 och en ipv6 men ens3 är adresser som fungerar på nätverket. en mac adress och en brd adress |
| Routing | ip route | Standard är via gatewayen 10.0.0.1 och genom dev ens3 som interface. |
| DNS | getent hosts | Ja. Med hjälp av getent hosts example.com så skickades en förfrågan till en DNS server som i sin tur skickade tillbaka två ipv6 adresser som är kopplade till example.com |
| Portar och tjänster | ss -tuln | På min vm är det totalt 6 adresser som lyssnar men det är dubbelt då 22 och 111 lyssnar på både ipv4 och ipv6 och så är det dubbla på dns resolvern. port 22 är ssh och används för att fjärrstyra en enhet. 111 är rpcbind och betyder att du kan anropa en annan dator om funktioner eller program som om den vore din egen. port 53 är dns resolvern som lyssnar efter förfrågningar och det den gör är att ge dig ip adresser på dem domännamn du frågar efter. |
| Lokal tjänst | curl http://localhost:8080 | Ja servern går att nå. när jag kör curl kommandot så hämtas en fillista som finns i den mappen jag hostade servern på, i detta fall min egen mapp. |
| Process eller systemstatus | ps aux "|" grep ssh | här får jag först upp alla processer som körs just nu på min VM och med hjälp av pipelinen grep ssh listas endast dem som har ordet ssh.Då får jag upp 3 processer en listener som lyssnar efter inkommande ssh ansluningsförsök, två session rader PID 1894 och 1971 som är kopplade till min egen anslutning. |
