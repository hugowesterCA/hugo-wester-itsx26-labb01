SUS_IP= "data/suspicious_ips.txt"
ACCESS_FILE= "data/access.log"
def load_suspicious_ips(path):
    try:
        with open(path, encoding="utf-8") as ioc_file:
            suspicious_ips = {line.strip() for line in ioc_file if line.strip()}
        return suspicious_ips
    except FileNotFoundError:
        print("kunde inte hitta suspicious_ips.txt")
        exit(1)

def loadandmatch_accessfile(path, indicators):
    try:
        matches= {}
        skipped= 0
        with open(path, encoding ="utf-8") as access_file:
            for line in access_file:
                
                fields = line.split()
                source_fields = [f for f in fields if f.startswith("src=")]
                if not source_fields:
                    skipped += 1
                    continue
                
                ip_address = source_fields[0].split("=", 1)[1]

                if ip_address in indicators:
                    matches[ip_address] = matches.get(ip_address, 0) +1
            return {"matches": matches, "skipped": skipped}
    except FileNotFoundError:
        print("Loggfil kunde inte hittas")
        exit(1)

def main():
    suspicious_ips = load_suspicious_ips(SUS_IP)
    results = loadandmatch_accessfile(ACCESS_FILE, suspicious_ips)
    print(f"IOC matchning: {results['matches']}")
    print(f"skipped: {results['skipped']}")

main()