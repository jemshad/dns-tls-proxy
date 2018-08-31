# dns-tls-proxy
DNS Queries over TLS

## Design Choices and Implementation
As readily available clients were not an option, the simplest option was to run a Simple DNS Server on port 53 where clients would send queries and then intercepting those packets and having something that can do the lookup on TLS over TCP.

For the simple DNSServer, dnslib provided good options with both UDP and TCP Support.
For the dns queries over TLS to the required endpoint (in this case, the cloudflare DNS Server - 1.1.1.1), getdns python libraries were used as it was fairly straightforward.




                           
                            ___________________
      ______________       |  ______    _____  |        _______________ 
     |              |      | |DNS   |  |TLS  | |       |  Cloudflare   | 
     |   Clients    |----->| |Server|..|Tran | |-----> |DNS (TLS)- 853 |
     |______________|      | |_(53)_|  |sport| |       |_______________|
                           |___________________|
                           
