# Evidensbeskrivning – Vecka 38

## trafikmix.pcap
- Datum: 2026-09-14
- Miljö: OCI, Canonical Ubuntu 26.04
- Interface: ens3
- Kommando: sudo timeout 30 tcpdump -i ens3 -s 0 -w trafikmix.pcap
- Trafik: genererad med trafikmix.sh (ping, DNS, HTTP, HTTPS mot example.com/8.8.8.8), 3 varv
- Storlek: 82K
- Sanering: rå pcap hålls lokalt, ej i github.
- pcap hash (SHA256): 5a790aef31ef9a2de5747450389faac729e98208337c5ab27081cfca90d7d338 (trafikmix2.pcap)
