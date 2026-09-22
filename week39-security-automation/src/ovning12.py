fail_count= 0

logs = [
    "SUCCESFULL LOGIN",
    "SUCCESFULL LOGIN",
    "SUCCESFULL LOGIN", 
    "FAILED LOGIN",
    "FAILED LOGIN",
    "SUCCESFULL LOGIN", 
    "SUCCESFULL LOGIN", 
    ]
for lines in logs:
    if "FAILED LOGIN" in lines:
        fail_count += 1
if fail_count >= 3:
    print("Möjligt brute-force attack upptäckt!")
else:
    print("Inga avvikelser")

