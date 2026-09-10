#!/usr/bin/env bash
# Syfte: detta script är till för att göra en grundläggande säkerhetskontroll, den kollar miljööversikt, dns kontroll, lokal tjänstekontroll, port översikt och en summering av resultaten.

# Säkerhetsavgränsning: detta script är endast avsett för att köras på en lokal enhet och ska inte användas för att skanna externa nätverk eller enheter. Det kräver inte sudo, och inga lösenord, nycklar eller tokens hanteras eller loggas.

# variabler som kommmer användas i scriptet. 
# sätter OK och FAIL count till 0 för att kunna räkna antal fel eller ok kontroller.
DOMAIN=("example.com"  "google.com" "github.com")
TEST_PORT=8080
OK_COUNT=0
FAIL_COUNT=0

# Här är variabler med loggfilens namn och tidstämpel, tidstämpeln förenklar granskning och gör så att en ny loggfil skapas för varje körning och inte ersätter den gamla.
#  LOG_DIR säger var log mappen ska vara. mkdir -p betyder att den ska skapa mappen sålänge mappen inte redan finns.
LOG_DIR="$HOME/secure_network_check_logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/secure_network_check_$(date +%Y%m%d_%H%M%S).log"
# här skapar jag en log funktion som tar emot status och meddelande som argument och skriver dem i logfilen.
log() {
    local status="$1"
    local message="$2"
    echo "[$status] $message" | tee -a "$LOG_FILE"

# en if sats för att uppdatera ok/FAIL count beroende på statusen som skickas in. elif är en förkortning på else if.
    if [[ "$status" == "OK" ]]; then
       OK_COUNT=$((OK_COUNT + 1))
    elif [[ "$status" == "FAIL" ]]; then
       FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}
# funktion för att rensa upp efter skriptet, i detta fall finns det inget att städa upp.
 cleanup(){
    log "INFO" "Scriptet skapar inga temporära filer eller startar någon server men skulle det vara så hade det varit här cleanupen hade skett"
    
}   
# en loop som kontrollerar dns uppslag för varje domän (som bestämt längst upp i domän variabeln).
#if getent hosts betyder hämtar ip adressen för domänen och om informationen fås skickas den till /dev/null.
for domain in "${DOMAIN[@]}"; do
    if getent hosts "$domain" > /dev/null; then
        log "OK" "DNS-uppslag lyckades för $domain"
    else
        log "FAIL" "DNS-uppslag misslyckades för $domain"
    fi
done
# Kontrollerar om TEST_PORT är definierad (inte tom) i variabeln längst upp med hjälp av -z flaggan., om den ör tom hoppar den över denna kontroll.
# Om den är definierad kollar den om det går att ansluta och loggar resultat.
# curl -s används för att fråga om tjänsten är igång och svarar, -s flaggan gör att curl inte skriver ut/med onödig information.
if [[ -z "$TEST_PORT" ]]; then
     log "FAIL" "TEST_PORT är inte definierad, hoppar över lokal tjänstekontroll"
else
    if curl -s "http://localhost:$TEST_PORT" > /dev/null; then
       log "OK" "Lokal tjänst på port $TEST_PORT är tillgänglig"
    else
       log "FAIL" "Lokal tjänst på port $TEST_PORT är inte tillgänglig"
   fi
fi

# kontrollerar öppna portar på systemet med ss -tuln och pipe till tee -a betyder att resultatet 
# ska skrivas till både terminalen och logg filen.
log "INFO" "kontrollerar öppna portar på systemet"
ss -tuln | tee -a "$LOG_FILE"
log "OK" "portkontroll slutförd, resultat sparat"

# ip address används för att skriva ut alla ip adresser samt broadcast adress och mac adress men då använder jag en
# pipe till grep "inet" för att filtrera ut och endast skriva ut de rader som innehåller "inet" alltså ipv4 och ipv6 adresser.
# pipe tee för resultat till terminal och loggfilen.
log "INFO" "Kontrollerar IP-adresser"
ip address | grep "inet" | tee -a "$LOG_FILE"
log "OK" "IP-adresser sparade"

# ip route skriver ut alla route vägar. pipe till grep "default" för att filtrera ut endast default route.
# pipe till tee -a för att skriva till terminal och loggfilen.
log "INFO" "Kontrollerar default route"
ip route | grep "default" | tee -a "$LOG_FILE"
log "OK" "Default route sparad"

# summerar resultatet av kontrollerna och loggar det. Tack vare if satsen som lägger till 1 på OK eller FAIL
# beroende på resultat av varje kontroll summeras antalet här.
log "INFO" "Sammanfattning: $OK_COUNT kontroller lyckades, $FAIL_COUNT kontroller misslyckades"
log "INFO" "Fullständig logg finns i $LOG_FILE"

#här anropas cleanup funktionen som är definierad längre upp men tom i detta fallet.
cleanup
# exit status baserat på FAIL_COUNT, om det är större än 0 skickas exit 1 vilket betyder att skriptet någonstans
# har misslyckats, annars skickas exit 0 vilket betyder att skriptet har lyckats med alla kontroller.
if [[ "$FAIL_COUNT" -gt 0 ]]; then
exit 1
else
exit 0
fi