# Variablar för att hålla koll på loggfilen, söktermen,
# Antalet hoppade rader och antalet misslyckade inloggningar och frekvens per ip adress.
LOG_PATH = "data/auth.log"
SEARCH_TERM = "Failed login"
skipped = 0
ip_counts = {}
fail_count = 0

#läs logg filen och analysera den rad för rad. Avkoda med utf-8. Referera filen som log_file.
# Ta varje rad i loggfilen och dela upp den i "fält" med hjälp av split().
# Source_fields skapar en lista med alla fält som börjar med src=.
with open(LOG_PATH, encoding="utf-8") as log_file:
    for line in log_file:
        fields = line.split()
        source_fields = [f for f in fields if f.startswith("src=")]
        #om source_fields är tom alltså det finns ingen src= i raden ska den hoppa över till
        # nästa rad och öka skipped med 1. Utan denna kontroll skulle programmet längre ner
        #  i koden försöka hämta ip adressen men eftersom listan skulle vara tom så hade programmet kraschat.
        if not source_fields:
            skipped += 1
            continue
        #om söktermen (Failed login) inte finns i raden ska den hoppa över till nästa rad.
        if SEARCH_TERM not in line:
            continue
        # Om raden passerar både src= och sökterm kontrollen ska fail_count ökas med 1.
        fail_count += 1
        # här defineras ip_address = source_fields hämtar den "element" som är nummer 0 och klipper
        # vid "=", 1an är en säkerhetsåtgärd ifall de skulle finas fler = så ska den bara klippa max 1 gång
        # [1] betyder att vi väljer bara element 1 som i detta fallet är ip adressen och element 0 är src.
        # ip_counts tar den ip adress vi fick ut och använder "get" för att hämta värdet från dictioneryt jag satte längst upp
        # och svarar med 0 om ip adressen inte dykt upp innan, sedan plus 1 för att öka antalet
        # skulle ip adressen ha dykt upp innan så kommer get svara med den siffran och plusa på med 1 istället.
        ip_address = source_fields[0].split("=", 1)[1]
        ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1

# print skriver ut texten i parantesen i terminalen. f berättar att {} ska räknas ut och i detta fall
# är det len(ip_counts) som räknar hur många unika nycklar (ip-adresser) det finns.
print(f"Antal unika ip-adresser: {len(ip_counts)}")

# Här plockar den ut innehållet i ip_counts som par (IP adress, antal) och sortera dem,
# så att utskriften blir i samma ordning varje gång. För varje par läggs
# IP-adressen i ip_address och antalet i count, och en rad skrivs ut.
for ip_address, count in sorted(ip_counts.items()):
    print(f"Antal misslyckade inloggningar från {ip_address}: {count}")

# här skriver den ut antal skipped. f betyder att pyhton ska räkna ut det som står i {} alltså hur många rader som är skippade 
# samma med sista rade nsom skriver ut hur många misslyckade inloggningar den räknade till.
print(f"Skipped: {skipped}")
print(f"Antal misslyckade inloggningar: {fail_count}")