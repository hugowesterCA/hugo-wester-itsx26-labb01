## Syfte

Syftet med det här programmet är att kunna ange loggfiler och på ett automatiserat
sätt få ut en rapport med viktiga observationer.

Programmet söker igenom filerna efter IP adresser i src=-fältet och räknar två
saker, misslyckade inloggningar (rader med "Failed login") i auth.log, och
blockerade anslutningar (DENY och DROP) i firewall.log. Där båda sammanställs med
frekvens per IP-adress, så att man ser vilka adresser som är vanligt återkommande.

Skulle en rad ha fel format eller sakna src=-fält hoppar programmet över den
och loggar den som skipped istället för att krascha eller tyst hoppa över raden.

Programmet jämför också de observerade IP-adresserna mot listan i
suspicious_ips.txt och redovisar vilka som finns med där.

Allting sammanställs i en rapport under output/ för lättillgänglighet och
granskning. Värt att veta är att rapportfilen skrivs över efter varje körning av programmet.

Rapporten bör användas för vidare analys och inte en bedömning av om en incident
har inträffat. Att en IP-adress finns i IOC-listan eller förekommer ofta betyder
inte i sig att den är en angripare utan gör adressen värd att undersöka närmare.

## Datasetval:

Dataset A: Basic, programmet analyserar filerna auth.log, firewall.log och suspicious_ips.txt, access.log analyseras inte.

## Pythonversion: 3.14.7

## Körinstruktion:

1. Kommandot måste köras från roten "week39-security-automation".
2. Skriv python src/security_report.py (python3 src/security_report.py om du kör på mac eller linux).
3. Du får en bekräftelse i terminalen om allt gått rätt och du hittar sedan rapporten under output/security_report.txt.

## Projektstruktur:

```
week39-security-automation/
├── README.md
├── data/
│   ├── auth.log
│   ├── firewall.log
│   └── ...
├── src/
│   └── security_report.py
├── output/
│   └── security_report.txt
└── docs/
    └── analysis.md
```

## Testfall 1: Känt positivt fall

För att göra samtliga testfall måste man byta filsökvägen i AUTH_LOG. I security_report.py finns en rad högst upp i programmet där du sätter den till den filen som ska används för respektive test.

AUTH_LOG = "data/test_auth.log"

Jag gjorde en egen testfil, test_auth.log, med två misslyckade inloggningar från samma IP-adress, en lyckad inloggning och en rad utan src=. Innan jag körde testet skrev jag ner vad jag väntade mig. 2 misslyckade, 2 unika IP-adresser och 1 skipped. Programmet svarade 1 unik IP-adress, och då insåg jag att jag hade tänkt fel, programmet räknar bara ip adresser från Failed login-rader, så den lyckade inloggningen kommer aldrig med. Resten stämde och testfallet blev positivt bortsett från min förväntan.

## Testfall 2: Formatfel/saknat fält

AUTH_LOG= "data/test_malformed.log"

Här ville jag testa den trasiga raden(raden utan "src="), så jag gjorde en egen fil som heter test_malformed.log med en korrekt Failed login rad och en rad som bara innehöll text utan src=. Jag väntade mig 1 misslyckad inloggning, 1 unik IP-adress och 1 skipped, och det stämde. Det viktiga var att programmet inte kraschade på den trasiga raden utan räknade den som hoppad, så att den syns i rapporten i stället för att försvinna utan loggning.

AUTH_LOG= "data/test_no_hits.log"

## Test 3: Noll träffar
I sista testfallet ville jag se vad som händer när det inte finns något att räkna. Jag gjorde test_no_hits.log filen med fyra rader som alla var successful login. Jag väntade mig 0 på alla rader och det blev det, 0 misslyckade, 0 unika IP-adresser och 0 skipped och ingen krasch.

## Manuell kontroll av auth.log

Här vill jag kontrollera så att programmet security_report.py faktiskt räknar rätt i auth.log filen. Jag räknade innan körningen till 4 failed login, 2 unika ip adresser, 203.0.113.15 står för 3 av försöken och 198.51.100.44 förekommer 1 gång. En rad utan "src=" så skipped borde bli 1. Det stämmde med det programmet räknade så kontrollen är godkänd.

Efter testerna har körts ska "AUTH_LOG" återställas till data/auth.log