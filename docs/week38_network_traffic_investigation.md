# Del A: miljö och metod
• OCI: Oracle cloud instans med Canonical Ubuntu 26.04

• Beskriv vilket interface du fångade på eller varför du använde any.Jag valde att fånga ens3 interfacet därför att det står som default route och har status UP. Det är genom detta interface som all internet trafik går igenom när den ska till min instans.

• Jag valde att använda egen fångst då jag har möjligheten och jag får en chans att lära mig hur det fungerar.

• Jag begränsade fångsten i tid genom att använda kommandot "sudo timeout 30 tcpdump -i ens3 -s 0 -w traffic_week38.pcap" där timeout 3o sätter en begränsning för fångsten på 30 sec.

• Beskriv hur pcap och skärmbilder har hanterats och sanerats.

• Förklara relevanta skillnader mot lärarens OCI-demonstration
