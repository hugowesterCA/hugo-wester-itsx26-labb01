with open("data/auth.log", encoding="utf-8") as log_file:
    for line in log_file:
        if "Failed login" in line:
            print(line.strip())