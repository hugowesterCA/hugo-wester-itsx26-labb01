fail_count= 0

with open("data/auth.log", encoding="utf-8") as log_file:
    for line in log_file:
        if "failed login" in line.lower():
            fail_count += 1

print(f"antal misslyckade inlogg: {fail_count}")
