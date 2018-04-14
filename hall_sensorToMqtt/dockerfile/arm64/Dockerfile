# hall_sensorToMqtt image
#
# ------------------------------------------------------------------------------
#               NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
#                       PLEASE DO NOT EDIT IT DIRECTLY.
# ------------------------------------------------------------------------------

FROM multiarch/debian-debootstrap:arm64-jessie
    LABEL maintainer = "julien.alaimo@gmail.com"
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
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y
    RUN apt-get install -y python \
    	python-pip \
python-dev

RUN apt-get install -y build-essential
RUN pip install paho-mqtt RPi.GPIO
# Execute command
EXPOSE 1883
ADD hall_sensor.py ${APPDIR}/
ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
