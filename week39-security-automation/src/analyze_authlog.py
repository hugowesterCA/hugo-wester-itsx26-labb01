skipped = 0
ip_counts = {}
fail_count = 0

with open("data/auth.log", encoding="utf-8") as log_file:
    for line in log_file:
        fields = line.split()
        source_fields = [f for f in fields if f.startswith("src=")]

        if not source_fields:
            skipped += 1
            continue

        if "Failed login" not in line:
            continue

        fail_count += 1

        ip_address = source_fields[0].split("=", 1)[1]
        ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1

print(f"unika ip adresser: {len(ip_counts)}")

for ip_address, count in sorted(ip_counts.items()):
    print(f"{ip_address}: {count}")

print(f"Skipped: {skipped}")
print(f"Antal misslyckade inloggningar: {fail_count}")