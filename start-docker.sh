#!/bin/bash

# Address to bind to (default all)
#address="127.0.0.1"

# Port to bind to (both udp and tcp. default 53)
#port=

sudo docker build -t dns-proxy-image .

dockerImage=dns-proxy-image

sudo docker run -d 	\
	--rm	\
	--net=host 	\
	-e DNS_LISTEN_ADDRESS=${address:-127.0.0.1} \
    -e DNS_PORT=${port:-53} \
	--name dns-proxy-container $dockerImage
