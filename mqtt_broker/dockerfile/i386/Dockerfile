# Mqtt image
#
# ------------------------------------------------------------------------------
#               NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
#                       PLEASE DO NOT EDIT IT DIRECTLY.
# ------------------------------------------------------------------------------

FROM multiarch/debian-debootstrap:i386-jessie
    LABEL maintainer = "julien.alaimo@gmail.com"
RUN apt-get update --fix-missing && \
        apt-get -y dist-upgrade

ENV	APPDIR="/MQTT_BROKER"

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
#--------------Mosquito--------------#
RUN apt-get install --no-install-recommends -y \
    	mosquitto-clients \
    	mosquitto

# Execute command
EXPOSE 1883
ADD entrypoint.sh /
ADD logo /
RUN chmod +x /entrypoint.sh
CMD ["/usr/sbin/mosquitto"]

