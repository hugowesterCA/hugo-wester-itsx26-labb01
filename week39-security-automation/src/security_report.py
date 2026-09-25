# Här anger jag filsökvägar för filer som ska användas i skriptet.
AUTH_LOG= "data/auth.log" 
FIREWALL_LOG= "data/firewall.log"
SUS_IP= "data/suspicious_ips.txt"
SEARCH_TERM= "Failed login"
# Här skapar jag ett tomt set för ioc och tomma dictionerys som fylls med ip adresser och antal.
suspicious_ips= set()
ip_counts = {}
firewall_counts= {}
# Här sätter jag räkne variablerna till noll så att den börjar räkna från noll och inget annat.
firewall_skipped= 0
fail_count= 0
skipped= 0
deny_count= 0
allow_count= 0
drop_count= 0
report_lines = []

# report_lines.append för att skriva datan i rapoorten och append säger att fylla på längst ned i texten.
report_lines.append(f"Källor: {AUTH_LOG}, {FIREWALL_LOG}, {SUS_IP}")
report_lines.append("")

# Ett try block för att försöka utföra innehållet men om det inte går används except för att skriva ut en varning att innehållet saknas i rapporten.
# I try blocket öppnas  och läser filen AUTH_LOG och avkodas med utf-8 och kallar den för auth_file i resten av blocket.
# Sen definieras vad fields är alltså dela upp text raden i olika element. Source fields definieras av att elementet börjar med src=.
try:
        with open(AUTH_LOG, encoding="utf-8") as auth_file:
         for line in auth_file:
                fields = line.split()
                source_fields = [f for f in fields if f.startswith("src=")]

                # src=-kontrollen ligger före söktermsfiltret så att felformaterade rader räknas som skipped i stället för att sorteras bort tyst.
                if not source_fields:
                                skipped += 1
                                continue
                
                if SEARCH_TERM not in line:
                                continue
                # denna rad räknar failed count om raden kommer igenom de två föregående kontrollerna.
                fail_count += 1
                # IP-adress plockas ut ur src=-fältet och räknas upp med 1 i ip_counts.
                # get() ger 0 om adressen inte setts förut, annars nuvarande antal.
                ip_address = source_fields[0].split("=", 1)[1]
                ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1
except FileNotFoundError:
        print(f"Kunde inte hitta {AUTH_LOG}")
        report_lines.append(f"VARNING: {AUTH_LOG} kunde inte läsas. Siffrorna nedan saknar auth-data.")

# denna rad skriver antalet unika adresser i rapporten med hjälp av{len(ip_counts)} som räknar hur många unika ip adresser det finns i ip counts.
report_lines.append(f"Antal unika ip-adresser i auth.log: {len(ip_counts)}")

report_lines.append(f"Skippade i auth.log: {skipped}")

# Skriver en rad per IP-adress i rapporten. items() ger par av adress och antal,och sorted gör att ordningen blir densamma vid varje körning.
for ip_address, count in sorted(ip_counts.items()):
    report_lines.append(f"Antal misslyckade inloggningar från {ip_address}: {count}")

report_lines.append(f"Antal misslyckade totalt: {fail_count}")

report_lines.append("")

# Detta block fungerar i princip likadant som auth blocket fast modifierat så den räknar allow,deny,drop istället för failed_login. 
# Även denna har felhantering med try/except. och räknar ip adresserna som dyker upp.
# ALLOW räknas men sorteras bort med continue, så firewall_counts bara innehåller adresser vars trafik blockerades eller droppas.
try:
        with open(FIREWALL_LOG, encoding="utf-8") as firewall_file:
         for line in firewall_file:
                fields = line.split()
                source_fields = [f for f in fields if f.startswith("src=")]
                
                if not source_fields:
                        firewall_skipped += 1
                        continue
                if "ALLOW" in line:
                        allow_count += 1
                        continue
                if "DENY" in line:
                        deny_count += 1
                        
                if "DROP" in line:
                        drop_count += 1

                ip_address = source_fields[0].split("=", 1)[1]
                firewall_counts[ip_address] = firewall_counts.get(ip_address, 0) + 1
except FileNotFoundError:
        print(f"Kunde inte hitta {FIREWALL_LOG}")
        report_lines.append(f"VARNING: {FIREWALL_LOG} kunde inte läsas. Siffrorna nedan saknar firewall-data.")

report_lines.append(f"Skippade i firewall.log: {firewall_skipped}")
report_lines.append(f"Antal unika blockerade ip-adresser i firewall.log: {len(firewall_counts)}")
report_lines.append(f"Antal nekade anslutningar: {deny_count}")
report_lines.append(f"Antal droppade anslutningar: {drop_count}")
report_lines.append(f"Antal tillåtna anslutningar: {allow_count}")


for ip_address, count in sorted(firewall_counts.items()):
    report_lines.append(f"Blockerade anslutningar från {ip_address}: {count}")

report_lines.append("")

# Läser IOC-listan där varje rad är en IP-adress. strip() tar bort radbrytningen, annars matchar adresserna aldrig mot dem från loggarna. Tomma rader hoppas över.
try:
        with open(SUS_IP, encoding="utf-8") as susip_file:
         for line in susip_file:
                ip = line.strip()
                if not ip:
                 continue
                suspicious_ips.add(ip)
except FileNotFoundError:
        print(f"Kunde inte hitta {SUS_IP}")
        report_lines.append(f"VARNING: {SUS_IP} kunde inte läsas. Filerna har inte jämförts med suspicious_ips-data i denna körning.")

# Här jämförs ip adresser som dykt upp i de andra filerna mot ip adresserna som finns i suspicious_ips.txt och om det blir en träff så skrivs det ut i rapporten att det bör analyseras vidare.
for ip_address, count in sorted(ip_counts.items()):
       if ip_address in suspicious_ips:
              report_lines.append(f"IOC träff i auth.log bör kontrolleras: {ip_address} ({count} misslyckade inloggningar)")

for ip_address, count in sorted(firewall_counts.items()):
       if ip_address in suspicious_ips:
              report_lines.append(f"IOC träff i firewall.log bör kontrolleras: {ip_address} ({count} blockerade anslutningar)")

# observationen och begränsningarna är manuellt skrivna och kommer skrivas ut automatiskt oavsett om någon av loggfilerna inte kunde läsas. Detta står skrivet i README.md då det är värt att
# veta innan man kör programmet.
report_lines.append("")
report_lines.append("Observation: 203.0.113.15 förekommer i både auth.log och firewall.log och är även listad i suspicious_ips.txt")
report_lines.append("Begränsning: Endast auth.log och firewall.log analyseras, access.log kollas inte.")
report_lines.append("Begränsning: Observationen är manuellt skriven och kommer därför stå likadant oavsett om en fil inte hittades. Observationen utgår från att filerna har lästs in rätt.")

# Här skrivs alla rader i report_lines till rapportfilen. "w" gör att filen skrivs över vid varje körning. write lägger inte till någon
# radbrytning själv, därför använder jag "\n". Bekräftelsen på att rapporten är skriven ligger inne i try så att den bara skrivs ut om filen faktiskt skapades.
try:
        with open("output/security_report.txt", "w", encoding="utf-8") as report_file:
         for line in report_lines:
             report_file.write(line + "\n")
        print("Rapport skriven till output/security_report.txt")
except FileNotFoundError:
       print("Kunde inte hitta mappen att skriva rapport till.")