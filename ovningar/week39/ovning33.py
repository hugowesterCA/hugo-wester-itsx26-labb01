LOGGFIL= "week39/ovning33_auth.log"
ip_counts= {}
with open(LOGGFIL, encoding="utf-8") as log_file:
    for line in log_file:
        fields = line.split()
        source_fields = [f for f in fields if f.startswith("src=")]
        if not source_fields:
            continue
        ip_address = source_fields[0].split("=", 1)[1]
        ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1

# denna sista del är ai för att sortera ip adresserna i rätt ordning
# för ip adresser räkna sorterat i följande ordning- dela upp ip_counts i par (.items())
# key är en instruktion att "titta på detta när du jämför" i ip_counts, lambda är en funktion som man använder direkt och 
# återanvänds inte som en def funktion. x matar in ett par med ip adress och antal, x[1] plockar ut andra delen av paret
# alltså antalet av adresserna, standard listas ordningen minst till störst så med reverse=true vänder vi så störst är först
# [:3] säger att funktionen ska plocka ut dem 3 första i listan alltså dem 3 mest förekommna adresserna.
# print raden skrievr ut dem 3 mest förekommna adresserna.
for ip_address, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"{ip_address}: {count}")        
            


