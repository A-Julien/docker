# nodejs image
#
# ------------------------------------------------------------------------------
#               NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
#                       PLEASE DO NOT EDIT IT DIRECTLY.
# ------------------------------------------------------------------------------

FROM multiarch/debian-debootstrap:arm64-jessie
    LABEL maintainer = "julien.alaimo@gmail.com"

# Set download urls
ENV DOMI_URL="https://hub.docker.com/r/jalaimo/nodejs"
# Set variables

ENV	APPDIR="/nodejs"

ENV \
    	INITSYSTEM on \
    	DEBIAN_FRONTEND=noninteractive \
    	LANG=C.UTF-8\
    	LC_ALL=C.UTF-8

# Basic build-time metadata as defined at http://label-schema.org
ARG BUILD_DATE
ARG VCS_REF
LABEL org.label-schema.build-date=$BUILD_DATE \
    	org.label-schema.docker.dockerfile="/Dockerfile" \
    	org.label-schema.name="nodejs" \
    	org.label-schema.url="https://hub.docker.com/r/jalaimo/nodejs"
RUN apt-get update --fix-missing && \
    apt-get -y dist-upgrade && \
\
#--------------Install basepackages--------------# 
\
 	apt-get install --no-install-recommends -y \
        build-essential && \
curl && \
    	apt-get clean \
\
#--------------Nodejs--------------#
\
apt-get install -y curl python-software-properties &&\
curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    	apt-get install -y nodejs npm
