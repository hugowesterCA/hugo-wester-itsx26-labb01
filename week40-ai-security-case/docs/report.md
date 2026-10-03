# AI Security Case Investigation – Case B: Prompt injection i ett vårdrelaterat AI-system

## 1. Executive summary

Personal har upptäckt att outputen har förändrats sedan assistenten tog emot ett externt dokument med en dold text med instruktioner. Risken i detta sammanhang är att patientuppgifter kan ha kommit med i sammanfattningen av ett dokument, i samband med att ai-assistenten skulle sammanfatta dokumentet åt personalen, men någon exponering är inte bekräftad. Det finns just nu inte någon tillgång till kartlagd loggning eller kartlagda behörigheter kring ai-assistenten så det är svårt att fastställa omfattningen av incidenten. Orsaken är alltså inte fastställd ännu och incidenten har tre möjliga förklaringar, en dold instruktion i det externa dokumentet, en för bred fråga från personalen, eller innehåll som assistenten genererat utan underlag. Konkreta säkerhetsåtgärder har rekommenderats samt en rekommendation om att pausa användandet av ai-assistenten tills saken är utredd och åtgärdad. Högst prioriterat är loggning då det är grunden för all framtida felsökning. Integriteten är den dimension som är mest hotad och påverkad i detta fall, då man inte längre kan lita på ai-assistentens sammanfattningar av dokumenten.

## 2. Fakta, hypoteser och scope

### Fakta:

• AI-assistenten sammanfattar dokument.

• Dokument kommer från flera källor.

• Ett externt dokument har laddats upp.

• Dokumentet innehåller avvikande instruktioner.

• Assistentens output har förändrats.

• Behörigheter och loggning är inte fullständigt kartlagda av organisationen.

• Det finns ingen bekräftad dataexponering.

• Orsakssambandet är ännu inte verifierat.

### Antaganden: 

* Att assistenten påverkades av den dolda instruktionen.
* Att det kan finnas fler liknande dokument i systemet om antagande 1 stämmer.
* Att det externa dokumentet kom från en okänd part.
* Att ai-assistenten har mer behörigheter än den enskilda användaren.
* Att liknande händelser redan kan ha skett men inte upptäckts.
* Att verksamheten regelbundet tar emot externa dokument. (sannolikhet men inte bekräftat)

### Kunskapsluckor: 

* Vi vet inte exakt vilken åtkomst assistenten har till andra dokument eller system. 
  
* vi vet inte om data exponering faktiskt har skett då det saknas loggning som skulle kunna bekräfta detta.
  
* vi vet inte vart ifrån dokumentet fakitiskt kom ifrån mer än externt.

### Avgränsning/scope: 

Den här rapporten fokuserar på säkerhetsanalysen av händelsen, inte på hur prompt injection tekniskt fungerar inne i språkmodellen. Jag går alltså inte in på detaljer om hur modellen tolkar eller viktar instruktioner, utan behandlar det som ett känt angreppssätt på systemnivå.

Jag gör inte heller en full juridisk bedömning enligt patientdatalagen eller GDPR. Eftersom det handlar om en vårdorganisation är det ändå värt att nämna att sådana lagar skulle bli relevanta i en fullständig utredning, men det ligger utanför vad den här rapporten går igenom.

## 3. Tillgångar och beroenden

* Information: Rutindokument och eventuell övrig patient dokumentation samt externa dokument som har laddats upp.
* System: ai-assistenten, interna system för dokumentation.
* Identiteter: Personalen som laddar upp dokumenten till ai assitenten är en identitet, ai assistenten har förmodligen en egen identitet och egna rättigheter separerade från personalen. Den externa parten som laddade upp ett dokument är en identitet.
* Processer: Personalen använder ai-assistenten för att sammanfatta tidigare patient dokumentation och sammanställa ny dokumentation om patienten. Vad som inte anges i scenariot är om det sker någon form av granskning av externa dokument innan dem laddas upp till systemet och ai assistenten.
* Förtroende: Personalens arbetsprocess bygger på ett förtroende  till att ai-assistenten sammanställer rutin okumentationen korrekt och att den ger tillbaka den sammanställda dokumentationen om patienten korrekt. Dehär förtroendet kan skadas direkt när assistenten ger information som inte stämmer eller som inte hör till dokumentet oavsett om det har skett en dataläcka eller manipulation av datan.

* Beroenden: Personalens process är beroende av att AI-systemet är tillförlitligt. AI-systemet är i sin tur beroende av att externa dokument inte förändrar innehållet eller outputen som assistenten skickar till personalen. Assistenten är också beroende av att den har nödvändiga rättigheter till de interna dokumentsystemen. Just nu är rättigheterna inte kartlagda av organisationen, vilket gör det svårt att verifiera omfattningen av situationen. Skulle förtroendet för AI-assistenten undergrävas rasar hela processkedjan.

## 4. Händelsekedja och alternativa förklaringar

* AI-assistenten tar emot ett externt dokument från okänd part.
* Dokumentet blir tillgängligt för assistenten att använda som underlag.
* Personalen ställer en fråga till ai-assistenten.
* Assistenten läser in det externa dokumentet och påverkas av den dolda instruktionen(antagande).
* Personalen noterar att svaren inte verkar höra till det valda dokumentet.
* När någon tittar närmare på det externa dokumentet upptäcks dold text med instruktioner om att frångå de vanliga instruktionerna.

Alternativa förklaringar: Att outputen blev annat än tänkt skulle också kunna bero på vad personalen gav för input då vi inte kan verifiera vad inputen var. Assistenten kan ha genererat innehåll som inte kommer från något underlag alls, utan är påhittat men som passar in i texten och ändå låter trovärdigt.

För att sortera bort alternativa förklaringar skulle det behövas loggar över vilken input som gavs, vilken output som kom från assistenten och vilka källor och dokument den använde för sitt svar. Eftersom organisationens loggning inte är kartlagd är det dock oklart om sådana loggar finns, vilket gör att ingen av förklaringarna kan bekräftas eller avfärdas just nu.

## 5. CIA- och fördjupad riskanalys

### Konfidentialitet:
 Konsekvensen för konfidentialiteten i detta fallet är att information kan ha gått till en person utan rätt behörighet. Men eftersom det saknas kartläggning över behörigheterna och loggar så kan jag inte bedöma omfattningen.

### Integritet: 
Outputen har förändrats och innehåller material som inte tycks höra till dokumentet. Dessutom har dolda instruktioner till ai-assistenten upptäckts. Sammantaget gör det att man inte längre kan lita på assistentens svar förrän orsaken är utredd och åtgärdad. Om vi utgår från antagandet att det var den dolda texten i det externa dokumentet som påverkade assistentens beteende kan vi inte utesluta att fler liknande dokument finns och de bör därför granskas. Förtroendeskadan finns alltså redan nu oavsett vad felet beror på.

### Tillgänglighet: 
Oavsett vad felet beror på finns nu en förtroende skada mot ai-assistenten. Det medför att verksamheten förmodligen behöver pausa användandet under utredningen. Skulle den ändå fortsätta att användas kommer personalen troligtvis ha svårt att lita på svaren och väljer därför att läsa dokumenten manuellt, vilket bromsar verksamhetens effektivitet.

Integritet är den mest kritiska i det här fallet. Att assistentens output har förändrats är fakta, medan en eventuell exponering av information (konfidentialitet) fortfarande bygger på antaganden som inte går att verifiera just nu. Integritet är dessutom orsaken till de övriga konsekvenserna och det är just för att svaren inte går att lita på som verksamheten behöver pausa eller dubbelkontrollera assistentens arbete. Skadan kvarstår dessutom tills orsaken är utredd, vilket i sin tur kräver loggning som inte är kartlagd ännu.

### Upptäckbarhet: 
att detta upptäcktes var pågrund av att personal tyckte svaret såg konstigt ut jämfört med vad som brukar komma som output eller om personen redan visste vad dokumentet innehöll. Skulle tillförlitligheten vara för stor till ai assistenten så skulle problemet aldrig tagits upp och personal hade fortsatt arbetet med fel data som grund. Upptäckbarheten därför låg.

### Sannolikhet: 
Beroende på hur ofta verksamheten tar emot dokument från externa parter är sannolikheten hög att detta upprepas. Det framgår inte om externa dokument granskas innan de laddas upp, och saknas en sådan kontroll finns inget som hindrar att liknande dokument når assistenten igen.

### Konsekvens: 
Konsekvensen bedömer jag som medel till hög. Bedömningen bygger på att personal kan ha fått felaktigt underlag i ett vårdsammanhang, där underlaget potentiellt skulle kunna påverka beslut om patienter. Bedömningen beror dock på vilken förklaring som visar sig stämma. Om innehållet var påhittat handlar det om felaktigt underlag, medan om det faktiskt handlar om att andra dokument har blandats in i ai sammanfattningen vore betydligt allvarligare. Utan tillgång till loggning går det inte att avgöra, och konsekvensen bedöms därför i det högre spannet tills motsatsen kan visas.

### Befintliga kontroller:
Av den informationen jag har fått så kan jag inte se att någon kontroll finns mer än personalens egna eventuella kontroll av svaret dem får från ai-assistenten, det är dock ingen rutin kontroll utan något som råkade finnas här. 
  
### Osäkerhet: 
Osäkerheten i det här fallet ligger i om det faktiskt var den dolda instruktionen i det externa dokumentet som påverkade svaret från ai-assistenten, samt om det finns loggning att tillgå för att undersöka saken vidare. Det påverkar bedömningen direkt då konsekvensen blir betydligt allvarligare om assistenten faktiskt hämtat in annan information än om innehållet var påhittat. Utan loggning går den skillnaden inte att avgöra.

### Residualrisk: 
Om man skulle inför loggning, kartläggning över rättigheter och inför kontroller över externa dokument så skulle man minska attack ytan men residualrisken skulle fortfarande vara att dolda instruktioner kommer med då man fortsatt måste ta emot externa dokument, men betydligt lättare att granska i efterhand med loggar och kartläggning av behörigheterna.

## 6. CIS-mappning och bortval

### Valda cis kontroller från listan "CIS Control V8.1": 

* CIS 6 skulle behövas då jag i nuläget inte har någon uppfattning om vilka rättigheter ai-assistenten har vilket gör det svårt att kartlägga omfattningen av vilka dokument den har haft tillgång till att ta information från
  
* CIS 8 vilket innebär att kartlagd loggning finns, det kan vara så att loggar finns men dem är inte tillgängliga  och kartlagda vilket gör de svårt att granska vad som faktiskt har hänt i efterhand

* CIS 14 som innebär att utbilda personalen, alltså att kunna känna igen när något inte ser rätt ut och att i detta fallet kunna verifiera outputen från ai-assistenten.
  
* CIS 16 Alltså säker ai design i detta fallet där input och output hantering finns men eftersom den själv inte kontrollerar vad som kommer i input(externa dokument) och den verifierar inte heller sin egna output så skulle just denna cis kontrollen vara väldigt viktig för organisationen.

### Bortvalda: 

* CIS 5 prioriterar jag lågt därför att i detta fallet är det bristen på behörighetskartläggning alltså cis 6 som är mer aktuellt. Kontonas livscykel och förvaltning är inte något som blockerar utredningen just nu. CIS kontroll 5 skulle dock kunna vara aktuellt senare så därför är den inte helt bortplockad.
  
* CIS 17 är lågt prioriterat därför att den bygger på att CIS 8 finns med loggar för utan det så blir det svår att jobba med.

## 7. Prioriterad förbättringsplan

Först skulle jag prioritera att få upp ett systematiskt loggnings system för att underlätta incident hantering i efterhand.

* Beroende: inte beroende av något då loggning är utgångspunkten och första steg, för eventuellt incidentrespond team är dem beroende av loggning.
* Ansvarstyp: IT-avdeldning samt system ägare
* Verifiering: ta en fråga personalen ställde och kolla i loggsystemet vilka källor ai assistenten använde sig av och se exakt vad input och output blev

Kartläggning över rättigheter på konton inom organisationen samt tillsätta zero trust i så hög utsträckning det går.

* Beroende: Inget beroende utan kan göras direkt, För att tillämpa zero trust eller least privilage krävs först denna kartläggning.
* Ansvarstyp: IT-avdelning samt systemägare.
* Verifiering: Man ska tydligt se vem som har behörighet till vad och testa att komma åt något som kontona inte ska ha behörighet för att fastställa är behörigheterna funkar i praktiken.

Jag skulle titta på att förbättra Ai designen så att det finns något som granskar input och output på assistenten.

* Beroende: Denna åtgärd kräver att organisationen vet vem som äger assistenten alltså vilken typ av ai det är, är det en extern tjänst så kan det vara svårare att konfigurera beroende på vad leverantören kan erbjuda. Är det en egen lösning alltså en ai på lokal server så blir det lättare att genomföra konfigueringen. Det framgår inte helt i scenariot vilken av dem det gäller i detta fallet.
* Ansvarstyp: Systemägaren är den som ansvarar för beslutet medan utförandet ligger antingen hos ai leverantören eller it avdelningen beroende på vilken lösning det är organisationen har valt.
* Verifiering: Ett kontrollerat test i en testmiljö där man skickar in ett eget externt dokument och försöker manipulera outputen för att se om just denna incident går att förhindra i framtiden men det garanterar inte att framtida manipulerings försök förhindras. Viktigt att detta test inte görs med riktig patient data.

Utbilda personalen inom ai användning eftersom det nu används i organisationen, samt följa upp efter ett tag och säkerställa att personalen har den kunskap som behövs vid ai användning.

* Beroende: För att utbildningen faktiskt ska ge något så krävs det en rutin samt rapporterings system så dem faktiskt kan agera om en incident har skett.
* Ansvarstyp: Chef eller HR, IT- avdelning håller förmodligen i utbildningen eller bidrar med kunskap och ihopsättning av rutin och utbildning.
* Verifiering: Litet kunskapstest efter utbildningen. Skicka ett dokument med dold instruktion i en kontrollerad övning och se om någon rapporterar det som en del av rutinen.

## 8. Teknisk verifieringsplan

* Loggar över input och output hos AI-assistenten, samt över vilka källor och dokument den hämtade in för att bygga sitt svar. Loggarna behövs för att kunna utesluta att det var inputen som påverkade svaret, men framför allt för att se om assistenten faktiskt hämtade in material utanför det uppladdade dokumentet.
* Kartläggning av assistentens behörigheter, för att fastställa omfattningen av vad den eventuellt har kommit åt och vilka dokument som kan ha exponerats.
* Det externa dokumentet självt, för att ta reda på exakt vad den dolda texten innehöll och bedöma om instruktionen kan ha varit orsaken till den förändrade outputen.
* Information om varifrån och från vem det externa dokumentet kom. Är avsändaren en känd och betrodd part kan dokumentet ha blivit komprometterat i ett tidigare led, och då kan fler mottagare behöva varnas. Är avsändaren okänd talar det snarare för ett riktat försök.

### Hur evidensen tolkas

* Visar loggen att assistenten hämtade in andra dokument än det uppladdade talar det för att instruktionen fick den effekt som var tänkt av angriparen. Alternativt att ai-assistenten är fel konfigurerad.
* Visar loggen att frågan från personalen var bred eller otydlig talar det mer för att det var inputen i sig som var svaret på varför outputen såg konstig ut.
* Visar loggen att inget dokument hämtades utan det begärda från personalen men att svaret ändå innehöll information som inte verkar höra till dokumentet kan det tala för att assistenten har genererat innehåll som inte hade med dokumentet att göra (Hallucinerat).
* Skulle det vara så att loggning inte finns så går det inte att bekräfta eller avfärda någon av förklaringarna.

## 9. Två målgrupper

* IT-avdelnings version: Användningen av ai-assistenten bör pausas till saken är utredd och åtgärdad. Prioritera att få loggning på plats och kartlagd först för att kunna utreda input, output och vilka dokument som samlas in av assistenten vid förfrågningar. Loggarna används sedan för att skilja mellan de möjliga förklaringarna, alltså om orsaken var en dold instruktion, en för bred fråga från personalen eller innehåll som assistenten genererat utan underlag (Hallucination). Tillämpa sedan least privilege på ai-assistenten för att minimera skadorna om en liknande attack skulle ske igen. Granskning av input och output i assistenten kan kräva att leverantören till ai-assistenten finns tillgänglig. Skulle det handla om prompt injection kan det inte uteslutas att flera dokument med dolda instruktioner redan finns i systemet.

* Ledningsanpassad version: Assistenten har gett svar som innehöll information som inte hörde till det dokument personalen frågade om. Användningen bör pausas tills incidenten är utredd, eftersom svaren kan ha manipulerats eller i alla fall inte är pålitliga. Saken ska utredas och åtgärdas, men tills vidare pausas rutinen att använda assistenten. Under tiden får personalen läsa och sammanfatta dokument manuellt, vilket kommer att minska effektiviteten och ta längre tid. Det är inte bekräftat om uppgifter från interna dokument har läckt, men det kan inte heller uteslutas i nuläget utan vidare undersökning.
  
## 10. English Security Summary

Se `docs/english_security_summary.md`.

## 11. AI- och källredovisning

Se `ai_usage.md` samt `docs/references.md`.

## 12. Slutsats

Användningen av AI-assistenten bör pausas eftersom det inte går att lita på outputen längre. Utan kartlagd loggning och kartlagda behörigheter går det inte att fastställa exakt vad som orsakade incidenten, och det är den centrala osäkerheten i den här bedömningen. Det som däremot kan fastställas är att ett externt dokument innehöll dolda instruktioner, och att assistentens output har förändrats. Integriteten är den mest påverkade dimensionen, och åtgärder bör därför göras enligt avsnitt 7, "Prioriterad förbättringsplan". Oavsett vilka åtgärder som vidtas kvarstår en residualrisk, eftersom verksamheten fortsatt måste ta emot externa dokument och ingen granskning fångar allt. Med loggning på plats och kartlagda behörigheter kan dock en incident upptäckas och utredas betydligt snabbare.