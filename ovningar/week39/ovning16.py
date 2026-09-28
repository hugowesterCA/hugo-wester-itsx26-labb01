fail_count = 0

logs = [
    "FAILED LOGIN",
    "FAILED LOGIN",
    "FAILED LOGIN",
    "SUCCESFULL LOGIN",
    "SUCCESFULL LOGIN",
    "SUCCESFULL LOGIN",
    "FAILED LOGIN",
    "FAILED LOGIN",
    "SUCCESFULL LOGIN",
    "SUCCESFULL LOGIN",
]

for line in logs:
    if "FAILED LOGIN" in line:
        fail_count += 1

print(f"Antal misslyckade inlogg: {fail_count}")