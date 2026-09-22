AUTH_LOG= "data/auth.log" 
FIREWALL_LOG= "data/firewall.log"
SEARCH_TERM= "Failed login"
ip_counts = {}
fail_count= 0
skipped= 0
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

print(f"Antal unika ip-adresser i auth.log: {len(ip_counts)}")

print(f"Skipped: {skipped}")

for ip_address, count in sorted(ip_counts.items()):
    print(f"Antal misslyckade inloggningar från {ip_address}: {count}")

print(f"Antal misslyckade inloggningar: {fail_count}")

