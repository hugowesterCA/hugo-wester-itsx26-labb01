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
