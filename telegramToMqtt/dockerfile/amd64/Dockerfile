# Mqtt image
#
# ------------------------------------------------------------------------------
#               NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
#                       PLEASE DO NOT EDIT IT DIRECTLY.
# ------------------------------------------------------------------------------

FROM multiarch/debian-debootstrap:amd64-jessie
    LABEL maintainer = "julien.alaimo@gmail.com"
RUN apt-get update --fix-missing && \
        apt-get -y upgrade

ENV	APPDIR="/telegram"

ENV \
    	INITSYSTEM on \
    	DEBIAN_FRONTEND=noninteractive \
    	DOMI_MQTT_PORT="1884"

# Basic build-time metadata as defined at http://label-schema.org
ARG BUILD_DATE
ARG VCS_REF
LABEL org.label-schema.build-date=$BUILD_DATE \
    	org.label-schema.docker.dockerfile="/Dockerfile" \
    	org.label-schema.name="MQTT BROKER"
#--------------Install basepackages--------------# 
RUN apt-get install --no-install-recommends -y \
    	python \
    	python-pip

RUN pip install requests
RUN pip install paho-mqtt
RUN pip install python-telegram-bot --upgrade
# Execute command
EXPOSE 1883
ADD telegramToMqtt.py ${APPDIR}/
ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
