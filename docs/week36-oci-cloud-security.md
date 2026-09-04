# Week 36 OCI Cloud Security Lab
## 1. Min linux/oracle cloud miljö
- Tenancy: hugowester
- Compartment: hugowester (root)
- Region: eu-stockholm-1
- Availability Domain: AD-1
- VM-namn: instance-20260831-1327
- Operativsystem: Canonical Ubuntu 26.04
- Shape: VM.Standard.E2.1.Micro
- Inloggningsmetod: Secure Shell

<img width="477" height="350" alt="image" src="https://github.com/user-attachments/assets/96e005e5-dbaa-4394-81d7-423c248a11a6" />

---
## 2. Linux-kommandon
| Kommando | Vad visar det? | CIA-koppling |
|-----------|-----------|-----------|
| whoami | (Ubuntu)visar vilken användare du är inloggad som| Konfidentialitet eftersom det berättar vem du är inloggad som och därmed vad du har tillgång att läsa |
| hostname | (instance-20260831-1327) Namn på den instans du kör ditt linux system på | Konfidentialitet då det ger information om systemet och kan bidra till kartläggning av systemet |
| pwd | Talar om i vilken mapp du befinner dig i | Konfidentialitet då den visar mappstrukturen och filsystemet |
| uname -a | Talar om vilket os du använder, vad din vm heter, vilken veision av linux kärnan (kernel) som körs, när uppdateringen till kärnan släpptes, vilken processortyp som används (x86_64), berättar at de är linux kärnan som används ihop med GNU som är ett program med verktyg och program för att använda linux | Konfidentialitet då den avslöjar kärn version|
| uptime | Klockslag nu, hur länge din VM varit igång sen senaste start samt load average | tillgänglighet, visar hur länge systemet varit igång och hur belastningen ser ut vilket jag kopplar direkt till tillgänglighet|
| ls -la | listar alla mappar, -l listar detaljerad info, -a visar även gömda mappar (mappar som börjar på "."| Konfidentialitet då den visar mappar och vilka rättigheter som krävs|
|date| visar dagens datum och klockslag| Integritet, om klockan är felinställd blir loggarnas tidsstämplar opålitliga |

---
## 3. Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
| identitet och behörigheter | Risken med behörigheter skulle kunna vara att du ser att en användare har mer rättigheter än vad som behöver och därmed skapas risken att något förstörs eller tas bort av misstag|kontrollerade användare och grupper med whoami, id, groups i terminalen | Jag såg att användaren va ubuntu vilket jag vet sen tidigare samt att grupperna va även där dem jag förväntade mig| Integritet|
| Fil rättigheter |Att man ger fel rättigheter till fel grupp vilket kan resultera i data förlust eller förendring | Skapade en fil, kollade rättigheterna, ändrade rättigheterna, verifierade att rättigheterna stämde | Jag skrev ls -l test.txt och kollade efter jag ändrade | Integritet |
| Systemuppdateringar | Gamla versioner kan ha kända buggar som angripare utnytjar | körde sudo apt update för att se tillgängliga uppdateringar, sedan sudo apt --upgradable för att se exakt vilka updateringar det gällde | Jag såg att det fanns en kernel uppdatering så efter så kollade jag versionen på den och den va då den senaste | Integritet |
| Proccesser | Att det ligger en skadlig proccess igång i bakrunden som jag annars inte är medveten om | listade dem 10 första processerna som kördes denna sessionen | kollade procceser med ps aux head och granskade proccesserna samt PID numrerna och dem steg i stegrande ordning. | Tillgänglighet |
---
## 4. Recovery-plan

recovery workshop uppgift (OCI miljö) 

steg 1: Går till storage på min instance -> boot-volume -> backups -> create boot volume backup (Backup type: Full)

<img width="471" height="373" alt="image" src="https://github.com/user-attachments/assets/a2287988-2351-4d2f-bb06-4853243d9224" />

Steg 2:  Nu skapar jag en fil på linux som inte finns på backupen för att senare verifiera att backupen funkar sedan gick jag till boot volume -> backups -> valde den ursprungliga backupen klickade restore boot volume.

Steg 3: storage på instansen -> replace boot volume -> valde den den nya återställda volumen

<img width="437" height="76" alt="image" src="https://github.com/user-attachments/assets/ca1b841f-5a3a-470c-959c-6501e61958a2" />

<img width="476" height="373" alt="image" src="https://github.com/user-attachments/assets/678d6fdb-a05d-4b10-adce-18d146a79f3b" />

steg 4: Här verifierar jag att backupen fungerar som den är tänkt. efter den nya boot volumen från backupen är tilldelad min instans testar jag att logga in för att verifiera detta. Filen är borta systemet funkar som det är tänkt.

Skulle backupen inte fungera, kan jag utgå från inspelade lektioner om instance setupen samt all dokumentation på allt arbete finns på github för att försöka återskapa den miljön jag hade.

### Hur du upptäcker problemet 

Brandväggs regler: Skulle du exempel vis blockerat för många portar och just 22 som man använder för ssh anlutning, du märker ganska fort att det skulle stå connection refused eller något i den stilen. 

### Vad kontrollerar jag först?

Brandvägg: kolla först att internet uppkoppling finns, kolla så din instance faktiskt är igång, kolla över brandväggs reglerna (VNIC/security) om de finns något där som kan vara problemet.

### Vilken information du behöver samla in

Internet uppkopplings status, vm/instance status (är den ens på?), samla ihop samtliga brandväggs regler.

### Hur du skulle få hjälp?

Skulle det vara så att man inte har tillgång till moln servern/hanteringen får man be ägaren om den om hjälp eller om man är osäker på vilken av alla brandväggs regler det kan vara som blockar så man inte bara tar bort alla regler och släpper in all trafik. känner man sig väldigt okunnig på detta, fråga ai om de är generella koncept och frågor eller googla, fråga klasskompis eller lärare.

### Hur skulle du kunna återskapa miljön?

I just detta fallet om det skulle bero på brandväggs konfiguration så räcker det troligtvis att ta bort en regel där. Skulle det vara så att du verkligen inte kommer in igen så finns det förhoppningsvis en backup som återställer miljön innan du la till brandväggen. Har du inte det heller får du utgå från i detta fallet github repot och gamla lektions inspelningar som visar steg för steg hur du sätter upp din labb miljö.

---
## 5. Backup
### Vad händer om VM:n försvinner?

Skulle din vm försvinna så är den borta det går sällan att ångra.

### Vad finns kvar i GitHub?


Eftersom min VM och github är två helt separata system så skulle all dokumentation finnas kvar på github.

### Vad kan återskapas?

I mitt fall har jag nu en full backup på min VM men skulle inte de finnas  får man försöka starta en ny och göra så likt man kan utifrån dokumentationen på github och lektions inspelnings materialet.

### Vad går inte att återskapa?

Det som inte går att återskapa är det som hänt efter jag gjorde en backup men också det jag inte har dokumenterat i github.

---
## 6. Cleanup
### VM-instans- Stopped (så ja ginte kör slut på free tier usage eller om jag skulle haft en betal plan kanske de ligger och kostar massa pengar i onödan). Jag har inte satt upp några brandväggsregler annars skulle man tagit bort dem.

### Diskar- En boot volume "attached" med 50gb utrymme totalt. resten är raderade som är gamla eller oanvändbara

### Backuper- en backup skapad på oracle cloud Sep 02, 2026, 06:37:53 UTC, inga ändringar gjorda sen dess.

### Publika IP-adresser

public ip-address 158.179.204.87 (Ephemeral= byts ut när vm tas bort eller stoppas)

### GitHub-evidens

https://github.com/hugowesterCA/hugo-wester-itsx26-labb01/edit/main/docs/week36-oci-cloud-security.md

Hur vet du att du inte har lämnat kvar resurser som kostar pengar? jag har stoppat min instans samt tagit bort överflödiga backups och boot volumes som va det enda som kunde dra usage och jag har free tier abonnemang, jag har inga betal uppgifter inlagda.

---
## 7. CIA-reflektion
### Konfidentialitet

I denna labb har jag dels använt linux kommandon som whoami, hostname, pwd och uname -a som alla främst rör konfidentialitet då man ser vem användaren är vart man är vilka som har tillgång till filer och dokument. Jag har även gjort hardening och säkrat upp systemet genom rättighets ändring med hjälp av chmod 600 som ser till att endast ägaren kan läsa skriva i mapparna (jag syftar på läs rättigheterna när de kommer till konfidentialitet).

### Integritet

Jag har även här gjort hardening delar som främst vidrör integriteten. Chmod 600 ändrade som sagt så att endast ägaren kan skriva i mapparna. Uppdaterade linux till senaste uppdateringen med sudo apt update och upgrade så att inte anfallare använder sig av redan kända buggar eller hål för att komma in i systemet och ändra eller ta bort filer.

### Tillgänglighet

 Systemuppdateringen påverkar även tillgänglighet då angripare skulle kunna komma in i systemet och stänga ner allting.
 Jag använde ps aux som listar alla processer som körs på datorn och därmed ser till att inget program som ser skadligt ut körs eller att något skadligt program snor prestanda eller i värsta fall leder till att systemet kraschar. Jag har skapat en backup till min VM på oracle cloud så om en krasch eller borttagning av min vm skulle ske så kan jag snabbare återställa systemet och se till att allt funkar igen. Under cleanup delen så såg jag till att min VM var avstängd när jag inte använde den så att det inte drar massa usage i onödan, detta skulle kunna leda till att jag måste betala mer för att köra min VM vilket kan göra den otillgänglig.
 
---
## 8. Reflektion
### Vad fungerade bra?

Efter att jag väl fått igång oracle cloud och loggade in på min VM så tycker jag det har gått bra och man fick lite mer struktur efter man läste inlämningsuppgiften vars instruktioner var tydliga.

### Vad var svårt?

Att få igång oracle cloud och förstå hur man skapar en vm samt att logga in med ssh nyckel då jag inte gjort det innan. Råkade stänga ner datorn under en linux uppdatering vilket ledde till att den uppdaterings processen stoppade mig från att slutföra uppdateringen för den låg och låste i bakrunden, löste det genom att gå in i ett annat fönster och stoppa den processen manuellt.

### Vad lärde jag mig?

Jag har lärt mig mycket under denna labb. Blivit säkrare på linux systemet och hur det funkar då jag aldrig använt det förut. Jag har lärt mig att hela tiden utgå från CIA triaden i allt som rör it. Hur man skapar en instance på oracle cloud. Jag förstår nu även hur jag ansluter till en VM med hjälp av SSH-nyckel. Att man kan stoppa en process som körs i bakrunden genom att gå in i ett annat fönster.
