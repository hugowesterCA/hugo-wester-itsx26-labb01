AUTH_LOG= "data/auth.log" 
FIREWALL_LOG= "data/firewall.log"
SUS_IP= "data/suspicious_ips.txt"
SEARCH_TERM= "Failed login"
suspicious_ips= set()
ip_counts = {}
firewall_counts= {}
firewall_skipped= 0
fail_count= 0
skipped= 0
deny_count= 0
allow_count= 0
drop_count= 0
report_lines = []
report_lines.append(f"Källor: {AUTH_LOG}, {FIREWALL_LOG}, {SUS_IP}")
report_lines.append("")


try:
        with open(AUTH_LOG, encoding="utf-8") as auth_file:
         for line in auth_file:
                fields = line.split()
                source_fields = [f for f in fields if f.startswith("src=")]

                if not source_fields:
                                skipped += 1
                                continue

                if SEARCH_TERM not in line:
                                continue
                fail_count += 1

                ip_address = source_fields[0].split("=", 1)[1]
                ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1
except FileNotFoundError:
        print(f"Kunde inte hitta {AUTH_LOG}")
        report_lines.append(f"VARNING: {AUTH_LOG} kunde inte läsas. Siffrorna nedan saknar auth-data.")

report_lines.append(f"Antal unika ip-adresser i auth.log: {len(ip_counts)}")

report_lines.append(f"Skippade i auth.log: {skipped}")

for ip_address, count in sorted(ip_counts.items()):
    report_lines.append(f"Antal misslyckade inloggningar från {ip_address}: {count}")

report_lines.append(f"Antal misslyckade totalt: {fail_count}")

report_lines.append("")

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

for ip_address, count in sorted(ip_counts.items()):
       if ip_address in suspicious_ips:
              report_lines.append(f"IOC träff i auth.log bör kontrolleras: {ip_address} ({count} misslyckade inloggningar)")

for ip_address, count in sorted(firewall_counts.items()):
       if ip_address in suspicious_ips:
              report_lines.append(f"IOC träff i firewall.log bör kontrolleras: {ip_address} ({count} blockerade anslutningar)")

report_lines.append("")
report_lines.append("Observation: 203.0.113.15 förekommer i både auth.log och firewall.log och är även listad i suspicious_ips.txt")
report_lines.append("Begränsning: Endast auth.log och firewall.log analyseras, access.log kollas inte.")
report_lines.append("Begränsning: Observationen är manuellt skriven och kommer därför stå likadant oavsett om en fil inte hittades. Observationen utgår från att filerna har lästs in rätt.")
try:
        with open("output/security_report.txt", "w", encoding="utf-8") as report_file:
         for line in report_lines:
             report_file.write(line + "\n")
        print("Rapport skriven till output/security_report.txt")
except FileNotFoundError:
       print("Kunde inte hitta mappen att skriva rapport till.")

