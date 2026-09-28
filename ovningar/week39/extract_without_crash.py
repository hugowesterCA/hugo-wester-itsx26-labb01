skipped = 0

with open("data/auth.log", encoding="utf-8") as log_file:
    for line in log_file:
        fields = line.split()
        source_fields = [f for f in fields if f.startswith("src=")]

        if not source_fields:
            skipped += 1
            continue

        ip_address = source_fields[0].split("=", 1)[1]
        print(f"IP address: {ip_address}")

print(f"Skipped: {skipped}")