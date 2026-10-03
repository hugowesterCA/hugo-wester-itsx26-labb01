# AI-användning och källredovisning

## Claude (Anthropic)

**Användningsområde**

Bollplank för analysen: motfrågor på mina resonemang, förklaring av begrepp jag inte kunde (residualrisk, skillnaden mellan CIS 5 och CIS 6), samt språklig genomgång. Även översättningsstöd och kontroll av den engelska sammanfattningen.

**Verifiering**

Kontrollerat påståenden mot scenariot och mot kursmaterialet. CIS-kontrollernas namn och innebörd har jag dubbelkollat mot primärkällan på cisecurity.org. OWASP:s sida om prompt injection har jag läst översiktligt för att bekräfta klassificeringen LLM01, men inte stämt av i detalj.

**Upptäckta fel och egna korrigeringar**

* Påstod felaktigt att jag avfärdat Integrity på fel grund i ett övningscase, när instruktionen i det caset faktiskt bara bad om att hämta innehåll.
* Påstod först att det fanns lite belagt stöd för adaptiva AI-attacker, vilket motsägs av kursmaterialet (10. Olika AI-hot).
* Invände mot en formulering om kartläggning och loggar som visade sig vara korrekt skriven.
* Ett tidigt utkast till den engelska sammanfattningen byggde på ledningsversionen och saknade tre av de fem obligatoriska delarna. Skrev om utifrån kraven i stället.

## Egen bedömning

Analysen, bedömningarna, valet av CIS-kontroller och bortvalen är mina egna. AI har använts som motpart för att pröva resonemangen, inte för att producera slutsatserna. AI har även använts för att stämma av att rätt inehåll finns med.