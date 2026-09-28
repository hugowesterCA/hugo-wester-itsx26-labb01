with open("data/firewall.log", encoding="utf-8") as log_file:
    for line in log_file:
        print(line.strip())