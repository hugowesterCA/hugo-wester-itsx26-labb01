# 1. Terminalens grunder
## Reflektion: 

• Efter jag trycker enter så skickas kommandot till bash, bash tolkar det och skickar svaret eller utför det som kommandot ska göra.

• När jag testar att skriva in ett kommando eller ord som inte finns körs det ändå eller snarare att bash letar efter kommandot men inte hittar det och svarar blablabla: command not found

• Skillnaden är att i terminalen så navigerar du med hjälp av text medans i grafiska program så klickar du på symboler och är kanske lite mer användar vänligt. Att skriva i terminalen är dock smidigare för ngn som lär sig det och speciellt inom cybersäkerhet då man snabbt kan söka efter en specifik fil eller log eller ord med hjälp av find eller grep och du kan göra egna skripts för återkommande uppgifter.

# 2. Navigering och filsystem

• ls -a

• pwd

• följer instruktionerna i terminalen vilket i detta fallet gav mig två alternativ antingen sudo apt eller sudo snap jag valde apt. Kan också fråga ai eller googla (sudo apt install tree # version 2.3.1-1)

• . syftar på katalogen jag befinner mig i just nu och .. syftar på katalogen ett snäpp upp/före

• cd

• ls visar endast vilka mappar som finns och är skapade av mig medans ls -l listar mer info om varje mapp.

# 3. Filhantering och visning

Reflektionsfrågor:

• Kommandon som är bra för att hantera text är echo, touch, grep, sort, head, tail cat -n, uniq.

• Jag använde först touch för att skapa den första filen, sedan echo "user01" > user.txt efter de fortsatte ja gatt fylla på texten med hjälp av echo "user02" >> user.txt som lägger till text längst ner i filen.

• Finns det något kommando som visar radnummer? cat plus flaggan -n och filens namn

• Vad händer om du försöker ta bort en mapp som inte är tom med rmdir? de komemr upp ett felmeddelande att mappen inte är tom.

• Vad är skillnaden mellan mv fil1 fil2 och cp fil1 fil2? mv så i detta fallet byter du namn på filen medans cp så kopierar du en fil till antingen en helt ny eller en annan redan existerande.

• Hur kan du ångra ett misstag om du tar bort fel fil? Utan en backup så går det inte i linux så däför måste man vara väldigt noggrann.

• Vad gör head -n 5 jämfört med tail -n 5? head -n 5 visar dem första 5 raderna uppifrån medans tail istället tar dem 5 sista raderna.

• Hur kan du söka efter ett ord medan du är inne i less? /user02 i mitt fall men det sökordet du letar efter.

# 4. Hjälp och man-sidor

Reflektionsfrågor:

• Vad är fördelarna med att kunna söka efter hjälp direkt i terminalen? Man får reda på hur man skriver i just denna terminalen, det går snabbt, du kan kolla även utan internetppkoppling, det kanske är för känslig data för att fråga ai.

• Vad menas med "flagga" eller "switch"? Flaggor/switch är en form av precisering av vad du vill att kommandot ska göra elelr om det ska göra något mer än kammandot själv.

• När är det bättre att använda less än cat? när du vill gå in o leta reda på ett specifikt ord  eller om de är en stor fil kan det lätt bli rörigt om allt skrivs ut i terminalen som de görs med cat.

# 5. Skapa första Bash-skriptet

Reflektionsfrågor:

• Varför behövs chmod +x? Chmod +x ger filen man har scriptet på execute rättigheter. Utan chmod +x nekas filen att köras pga rättigheter saknas.
• Vad är skillnaden mellan att köra bash hello.sh och ./hello.sh? ./hello.sh kräver att du har gett filen execute rättigheter för att kunna köras som ett eget program medans med bash ./hello.sh så krävs inga rättigheter då det är bash själv som läser in filen och skriver ut i terminalen.

# 6. Redigera och köra script

Reflektionsfrågor:

• Vad är skillnaden mellan att köra ett skript med ./skript.sh och bash skript.sh? ./skript.sh kräver att du har gett filen execute rättigheter för att kunna köras som ett eget program medans med bash ./script.sh så krävs inga rättigheter då det är bash själv som läser in filen och skriver ut i terminalen.

• Varför fungerar inte ./skript.sh om du inte först kör chmod +x skript.sh? för att det saknas rättigheter att executa det som ett eget program

• När kan det vara en fördel att köra ett skript med bash skript.sh istället för att
göra det körbart? Om du är osäker på vad ett script du får gör kan du testa det med bash innan du kör chmod och ger de några rättigheter i ditt system.

• Hur påverkar en felaktig tolkangivelse på första raden (t.ex. #!/bin/bash) om du
försöker köra skriptet med ./skript.sh? då vet inte systemet hur den ska tolka scriptet om de är bash den ska använda eller python osv.

• Vad händer om du kör ett skript utan att ange ./ framför? Varför fungerar det
ibland och ibland inte?  om man inte använder ./ så tror bash att det är ett komando och kommer därför leta i listan av kommandon medans om du skriver ./ så vet den att det är en fil som ska köras som ett program

• Kan du köra ett skript som ligger i en annan katalog utan att byta katalog? Hur? ja genom att skriva ut hela katalog pathen som i mitt fall blir /home/ubuntu/mittscript.sh

• Vad händer om du kör ett skript med sh skript.sh men skriptet använder
funktioner som inte stöds i sh? det funkar sålänge det är delar som båda sh och bash förstår men så fort det kommer bash specifika delar så kommer scriptet att misslyckas då sh inte förstår allt som bash gör


• Vad betyder det att ett skript körs i en "subshell", och hur kan det påverka
variabler eller miljön i det aktiva terminalfönstret? Variabeln kommer finnas kvar i subshell men du kan inte anropa eller använda det från huvud skalet.

• Vad är skillnaden mellan grep ord fil och grep -i ord fil? grep kommer ta fram det exakta ordet medans grep -i tar även med samma ord oavsett om de är versaler eller inte.

• Hur kan du söka rekursivt i alla filer under en katalog? (grep -r) med hjälp av grep -r "user" som ett exempel så kommer grep att list samtliga filer i katalogen du är i och alla underkataloger där user näms i texten. till skilnad från grep där du endast anger en fil som söks igenom.

# 7. läs och skriv ut alla filer i aktuell mapp

reflektionsfrågor:

• Vad betyder PID i ps? PID= Process id, ett unikt id som varje process får tilldelat av linux.

• Hur hittar du en process som heter python? genom att kombinera ps aux som listar alla processer, skickar vidare listan med "|" och sedan grep python för att filtrera i listan efter ordet python. så "ps aux | grep python"

• Vad händer om du skickar kill -9 PID jämfört med kill PID? med kill pid skcikar du en "snäll" begäran till processen att stänga ner efter den har sparat och avslutat medans  kill -9 pid så skickar du en signal om att stoppa programmet omdedelbart utan att spara. Som i mitt fall där jag stängde datorn under en uppdatering så va jag tvungen att göra en kill -9 PID.

# 8. Arbeta med redirection

reflektionsfrågor: 

• vad är skillnaden på > och >>?  > skapar antingen en ny eller skriver över en fil om den redan finns medans >> lägger till text längst ner i filen.

• Vad händer om du skriver ls > filer.txt flera gånger? Hela filens innehåll kommer ersättas med det nya ls > filer.txt (om du har lagt till eller ändra något).

# 9. Pipe och filter

• Vad är skillnaden mellan | (pipe) och > (redirect)? pipe kopplar ihop program med program (kommandon) medans > redirect skriver in resultatet i en fil.

• När skulle du använda grep i verkligheten? om man letar efter ett specifikt klockslag funkar grep eller om du vet att du letar efter en specifik felkod eller bara ordet error så kan du direkt söka upp just dem orden/siffrorna och slipper scrolla igenom hela filer.

# 10. Organisera filer med Bash-skript

reflektionsfrågor: 

• Hur tar man reda på filändelsen i Bash? i mitt script använde jag mig av en if sats innehållande en jämförelse som såg ut såhär if [[ "$fil" == *.txt ]]. och en elif sats för varje typ av filtyp jag kan tänkas använda.

• Hur kontrollerar man om en mapp finns? tex med en if sats med testet -d tex if [[ -d "mappnamn" ]] för att se om mappen finns.
• Finns det olika sätt att flytta filer? Vad är för- och nackdelar? ja det finns de, du kan antingen använda mv för att enkelt flytta en fil till en annan. en alternativ väg är att kopiera en fil med cp och sen ta bort den gamla med rm. det sist nämnda tar längre tid.

• Hur hanterar du filer med mellanslag? för att hantera filer med mellanslag så citerar du hela filen som den heter exempelvis mv "min fil.txt" minmapp, sålänge allt är inom citat tecken så kommer bash tolka det som ett argument eller ett namn.

• Vad händer om du flyttar en fil som redan finns i målmappen? då ersätter den nya filen som du skriver in den gamla filen.
