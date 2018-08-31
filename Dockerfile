FROM ubuntu
MAINTAINER jemshad dot ok at gmail dot com

ENV DEBIAN_FRONTEND noninteractive
	
RUN apt-get update
RUN apt-get install -y python3 \
                       python3-getdns \
                       python3-dnslib \
                       supervisor

COPY dns-proxy.py /usr/bin/dns-proxy
COPY dns-proxy-supervisor.conf /etc/supervisor/conf.d/dns-proxy.conf

RUN chmod 755 /usr/bin/dns-proxy

# Run supervisord in the foreground
CMD ["/usr/bin/supervisord", "-n"]
