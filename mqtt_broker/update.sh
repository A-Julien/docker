#!/bin/bash

arches="amd64 armhf i386 arm64"

print_header() {
	cat > $1 <<-EOI
	# Mqtt image
	#
	# ------------------------------------------------------------------------------
	#               NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
	#
	#                       PLEASE DO NOT EDIT IT DIRECTLY.
	# ------------------------------------------------------------------------------
	
	EOI
}

# Print selected image
print_baseimage() {
	cat >> $1 <<-EOI
	FROM multiarch/debian-debootstrap:${arch}-jessie
    LABEL maintainer = "julien.alaimo@gmail.com"
	EOI
}

# Print metadata && basepackages
print_basepackages() {
	cat >> $1 <<-'EOI'	
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
EOI
}

# update system
print_update(){
	cat >> $1 <<-'EOI'
	RUN apt-get update --fix-missing && \
        apt-get -y dist-upgrade

EOI
}


# install Mosquito
print_mosquito(){
	cat >> $1 <<-'EOI'
	#--------------Mosquito--------------#
	RUN apt-get install --no-install-recommends -y \
    	mosquitto-clients \
    	mosquitto

EOI
}




# Set working directory and execute command
print_command() {
	cat >> $1 <<-'EOI'
	# Execute command
	EXPOSE 1883
	ADD entrypoint.sh /
	ADD logo /
	RUN chmod +x /entrypoint.sh
	CMD ["/usr/sbin/mosquitto"]

EOI
} 

# Build the Dockerfiles
mkdir dockerfile
for arch in ${arches}
do
	file=dockerfile/${arch}/Dockerfile
		mkdir -p `dirname ${file}` 2>/dev/null
		echo -n "Writing $file..."
		print_header ${file};
		print_baseimage ${file};
		print_update ${file};
		print_basepackages ${file};
		print_mosquito ${file};
		print_command ${file};
		cp entrypoint.sh dockerfile/${arch}/entrypoint.sh
		cp logo dockerfile/${arch}/logo
		echo "done"
done