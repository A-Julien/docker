# powerOff pi image
#
# ------------------------------------------------------------------------------
#               NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
#                       PLEASE DO NOT EDIT IT DIRECTLY.
# ------------------------------------------------------------------------------

FROM multiarch/debian-debootstrap:armhf-jessie
    LABEL maintainer = "julien.alaimo@gmail.com"
ENV	APPDIR="/powerOff"

ENV \
    	INITSYSTEM on \
    	DEBIAN_FRONTEND=noninteractive \

# Basic build-time metadata as defined at http://label-schema.org
ARG BUILD_DATE
ARG VCS_REF
LABEL org.label-schema.build-date=$BUILD_DATE \
    	org.label-schema.docker.dockerfile="/Dockerfile" \
    	org.label-schema.name="POWER OFF"

#--------------Install basepackages--------------# 
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y
    RUN apt-get install -y --no-install-recommends \
python \
python-dev \
python-pip \
build-essential 
RUN pip install rpi.gpio
RUN pip install paho-mqtt		
# Execute command
ADD gpio_mqtt.py ${APPDIR}/
ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
