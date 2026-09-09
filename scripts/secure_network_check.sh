#!/bin/bash
# Syfte: detta script är till för att göra en grundläggande säkerhetskontroll, den kollar miljööversikt, dns kontroll, lokal tjänstekontroll, port översikt och en summering av resultaten.

# Säkerhetsavgränsning: detta script är endast avsett för att köras på en lokal enhet och ska inte användas för att skanna externa nätverk eller enheter. Det kräver inte sudo, och inga lösenord, nycklar eller tokens hanteras eller loggas.

DOMAIN=("example.com"  "google.com" "github.com")
TEST_PORT=8080
LOG_DIR="$HOME/secure_network_check_logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/secure_network_check_$(date +%Y%m%d_%H%M%S).log"
OK_COUNT=0
FAIL_COUNT=0

log() {
    local status="$1"
    local message="$2"
    echo "[$status] $message" | tee -a "$LOG_FILE"
}
cleanup() {
    log "INFO" "Scriptet skapar inga temporära filer eller startar någon server men skulle det vara så hade det varit här cleanupen hade skett"
    
}   

    if [[ "$status" == "OK" ]]; then
       OK_COUNT=$((OK_COUNT + 1))
    elif [[ "$status" == "FAIL" ]]; then
       FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}
for domain in "${DOMAIN[@]}"; do
    if getent hosts "$domain" > /dev/null; then
        log "OK" "DNS-uppslag lyckades för $domain"
    else
        log "FAIL" "DNS-uppslag misslyckades för $domain"
    fi
done
if [[ -z "$TEST_PORT" ]]; then
log "FAIL" "TEST_PORT är inte definierad, hoppar över lokal tjänstekontroll"
else
if curl -s "http://localhost:$TEST_PORT" > /dev/null; then
log "OK" "Lokal tjänst på port $TEST_PORT är tillgänglig"
else
log "FAIL" "Lokal tjänst på port $TEST_PORT är inte tillgänglig"
fi
fi

log "INFO" "kontrollerar öppna portar på systemet"
ss -tuln | tee -a "$LOG_FILE"
log "OK" "portkontroll slutförd, resultat sparat"

log "INFO" "Kontrollerar IP-adresser"
ip address | grep "inet" | tee -a "$LOG_FILE"
log "OK" "IP-adresser sparade"

log "INFO" "Kontrollerar default route"
ip route | grep "default" | tee -a "$LOG_FILE"
log "OK" "Default route sparad"

log "INFO" "Sammanfattning: $OK_COUNT kontroller lyckades, $FAIL_COUNT kontroller misslyckades"
log "INFO" "Fullständig logg finns i $LOG_FILE"

cleanup

if [[ "$FAIL_COUNT" -gt 0 ]]; then
exit 1
else
exit 0
fi