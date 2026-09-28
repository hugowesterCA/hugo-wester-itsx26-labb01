error_count= 0
failed_count= 0
warning_count= 0
with open("data/ovning14.log", encoding="utf-8") as log_file:
    for line in log_file:
        if "ERROR" in line:
            error_count += 1
            continue
        if "FAILED" in line:
            failed_count += 1
            continue
        if "WARNING" in line:
            warning_count += 1
            continue

print(f"antal error: {error_count}")
print(f"antal failed: {failed_count}")
print(f"antal warning: {warning_count}")

