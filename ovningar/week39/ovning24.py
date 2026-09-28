from datetime import datetime

timestamp = datetime.now().isoformat(timespec="seconds")


with open("security.log", "a", encoding="utf-8") as report_file:
    report_file.write(f"{timestamp} Händelse: test\n")