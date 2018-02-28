# KS_serv image
#
# ------------------------------------------------------------------------------
#               NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
#                       PLEASE DO NOT EDIT IT DIRECTLY.
# ------------------------------------------------------------------------------

FROM multiarch/debian-debootstrap:armhf-jessie
    LABEL maintainer = "julien.alaimo@gmail.fr"
RUN apt-get update --fix-missing && \
        apt-get -y dist-upgrade

ENV \
    	INITSYSTEM on \
    	DEBIAN_FRONTEND=noninteractive \
    	DOMI_MQTT_PORT="1884"

# Basic build-time metadata as defined at http://label-schema.org
ARG BUILD_DATE
ARG VCS_REF
LABEL org.label-schema.build-date=$BUILD_DATE \
    	org.label-schema.docker.dockerfile="/Dockerfile" \
    	org.label-schema.name="Ksp_server"

#--------------Install basepackages--------------# 
RUN apt-get install -y \
    	mono-complete

# Execute command
EXPOSE 6702
ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
