# dns-tls-proxy
DNS Queries over TLS

## Design Choices and Implementation
As readily available clients were not an option, the simplest option was to run a Simple DNS Server on port 53 where clients would send queries and then intercepting those packets and having something that can do the lookup on TLS over TCP.

For the simple DNSServer, dnslib provided good options with both UDP and TCP Support.
For the dns queries over TLS to the required endpoint (in this case, the cloudflare DNS Server - 1.1.1.1), getdns python libraries were used as it was fairly straightforward.

The `dns-proxy.py` is the script which implements both the DNSServer and the TLS transport portion to talk to Cloudflare DNS Server `1.1.1.1` on port 853.

For process control, this application is run under `supervisor` inside the docker container.

For easiness in setup (not having to depend on iptable rules for bridged mode networking), the container is made to work with host mode networking. This also gives performance advantage as it is directly using the host machine's networking interface bypassing the virtual interfaces that come into picture when using the bridge mode networking. I think this would be a fair assumption as clients usually query on UDP 53 and fallback to TCP in case of truncated replies.

In Microservices architecture, since different applications doesn't need separate DNS resolvers, this can be deployed as a standalone container to serve all the DNS needs of all the containers in the cluster. Multiple instances can be made available for redundancy and therefore high availability. On a further large scale, excellent DNS aware load balancers like https://dnsdist.org/ can be used for load balancing, high availability and increased performance by detecting the best performing backends.


## Query Flow Diagram

                           
                            ___________________
      ______________       |  ______    _____  |        _______________ 
     |              |      | |DNS   |  |TLS  | |       |  Cloudflare   | 
     |   Clients    |----->| |Server|..|Tran | |-----> |DNS (TLS)- 853 |
     |______________|      | |_(53)_|  |sport| |       |_______________|
                           |___________________|
                           
## Building the container and Running
Just need to run the provided shell script
`start-docker.sh`

This will create the image with latest Ubuntu as the base and then start the container. Container is started with --rm option so that it will automatically clean up on exit.

### Customization Options
By editing the shell script, the following parameters can be modified:

1. Address - Bind address for the DNS Server. Default value `127.0.0.1`
1. Port Number - Port to bind to. Both TCP and UDP instances will be listening on this same port. Default value `53`

## TODO
1. A callback function for handling multiple queries at the same time.
1. Currently, the application is written to handle/answer only `A` record queries. This can be extended to other queries too.


