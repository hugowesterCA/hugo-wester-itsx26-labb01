# Week 36 OCI Cloud Security Lab
## 1. Min OCI-miljö
- Tenancy: hugowester
- Compartment: hugowester (root)
- Region: eu-stockholm-1
- Availability Domain: AD-1
- VM-namn: instance-20260831-1327
- Operativsystem: Canonical Ubuntu 26.04
- Shape: VM.Standard.E2.1.Micro
- Inloggningsmetod: Secure Shell
---
## 2. Linux-kommandon
| Kommando | Vad visar det? | CIA-koppling |
|-----------|-----------|-----------|
| whoami | cisar vilken användare du är inloggad som|Konfidalitet eftersom det berättar vem du är inlogad som |
| hostname | Berättar vart du kör din vm alternativt server | konfidalitet då det ger information om systemet |
| pwd | Talar om i vilken mapp du befinner dig i | Konfidalitet då den visar mappstrukturen och filsystemet |
| uname -a | Talar om vilket os du använder, vad din vm heter, vilken verision av linux kärnan (kernel) som körs, när uppdateringen till kärnan släpptes, vilken processortyp som används (x86_64), berättar at de är linux kärnan som används ihop med GNU som är ett program med verktyg och program för att använda linux | Konfidalitet då den avslöjar kärn verision|
| uptime | Klockslag nu, hur länge din VM varit igång sen senaste start samt load average | tillgänglighet, visar hur länge systemet varit igång och hur belastningen ser ut vilket jag kopplar direkt till tillgänglighet|
---
## 3. Hardening
| Kontroll | Risk | Vad gjorde jag? | Hur verifierade jag? | CIA |
|-----------|-----------|-----------|-----------|-----------|
| | | | | |
---
## 4. Recovery-plan
### Vad kan gå fel?
### Hur upptäcker jag problemet?
### Vad kontrollerar jag först?
### Hur återställer jag åtkomst?
### När behöver jag hjälp?
---
## 5. Backup
### Vad har jag sparat?
### Vad finns i GitHub?
### Vad kan återskapas?
### Vad går inte att återskapa?
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
