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

<img width="561" height="347" alt="image" src="https://github.com/user-attachments/assets/563bad53-297a-4e33-8410-b654c4240035" />

---
## 2. Linux-kommandon
| Kommando | Vad visar det? | CIA-koppling |
|-----------|-----------|-----------|
| whoami | visar vilken användare du är inloggad som|Konfidalitet eftersom det berättar vem du är inlogad som |
| hostname | Berättar vart du kör din vm alternativt server | konfidalitet då det ger information om systemet |
| pwd | Talar om i vilken mapp du befinner dig i | Konfidalitet då den visar mappstrukturen och filsystemet |
| uname -a | Talar om vilket os du använder, vad din vm heter, vilken verision av linux kärnan (kernel) som körs, när uppdateringen till kärnan släpptes, vilken processortyp som används (x86_64), berättar at de är linux kärnan som används ihop med GNU som är ett program med verktyg och program för att använda linux | Konfidalitet då den avslöjar kärn verision|
| uptime | Klockslag nu, hur länge din VM varit igång sen senaste start samt load average | tillgänglighet, visar hur länge systemet varit igång och hur belastningen ser ut vilket jag kopplar direkt till tillgänglighet|
---
## 3. Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
| identitet och behörigheter | Risken med behörigheter skulle kunna vara att du ser att en användare har mer rättigheter än vad som behöver och därmed skapas risken att något förstörs eller tas bort av misstag|kontrollerade användare och grupper med whoami, id, groups i terminalen | Jag såg att användaren va ubuntu vilket jag vet sen tidigare samt att grupperna va även där dem jag förväntade mig| Integritet|
| Fil rättigheter |Att man ger fel rättigheter till fel grupp vilket kan resultera i data förlust eller förendring | Skapade en fil, kollade rättigheterna, ändrade rättigheterna, verifierade att rättigheterna stämde | Jag skrev ls -l test.txt och kollade efter jag ändrade | Integritet |
| Systemuppdateringar | Gamla versioner kan ha kända buggar som angripare utnytjar | körde sudo apt update för att se tillgängliga uppdateringar, sedan sudo apt --upgradable för att se exakt vilka updateringar det gällde | Jag såg att det fanns en kernel uppdatering så efter så kollade jag verisionen på den och den va då den senaste | Integritet |
| Proccesser | Att det ligger en skadlig proccess igång i bakrunden som jag annars inte är medveten om | listade dem 10 första processerna som kördes denna sessionen | kollade procceser med ps aux | head och granskade proccesserna samt PID numrerna och dem steg i stegrande ordning. | Tillgänglighet |
---
## 4. Recovery-plan

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
### VM-instans
### Diskar
### Backuper
### Publika IP-adresser
### GitHub-evidens
---
## 7. CIA-reflektion
### Konfidentialitet
### Integritet
### Tillgänglighet
---
## 8. Reflektion
### Vad fungerade bra?
### Vad var svårt?
### Vad lärde jag mig?
