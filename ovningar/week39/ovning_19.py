logg = [
    "ERROR",
    "ERROR",
    "ERROR",
    "ERROR",
]

def errorräknare (logs):
                error_count= 0
                for lines in logs:
                  if "ERROR" in lines:
                    error_count += 1
                return error_count

print(errorräknare(logg))