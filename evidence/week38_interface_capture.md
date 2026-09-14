# Vecka 38 – Interface-val och trafikfångst
- **Interface:** ens3
- **Varför:** ens3 är det interface som står som default route 
  (ip route) och har status UP. All internettrafik går via detta 
  interface. Andra alternativ (lo, any, bluetooth-monitor, dbus-*) 
  uteslöts eftersom de antingen är interna (lo), fångar allt 
  oprecist (any), eller är helt orelaterade till nätverkstrafik.
- **Trafik jag avsåg att skapa:** ping mot example.com
- **Begränsningar:** genom att välja ens3 specifikt missar jag 
  loopback-trafik (lo). Troligen mindre relevant här eftersom 
  jag är intresserad av trafik som går ut/in via internet.

  ## fångst
  
  **komando:** sudo timeout 30 tcpdump -i ens3 -s 0 -w traffic_week38.pcap

  **Resultat:** 171 packets captured
171 packets received by filter
0 packets dropped by kernel
