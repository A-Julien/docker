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

	# Basic build-time metadata as defined at http://label-schema.org
	ARG VCS_REF
	ARG	BUILD_DATE
    LABEL maintainer = "julien.alaimo@gmail.com" \
			org.label-schema.build-date=$BUILD_DATE \
			org.label-schema.docker.dockerfile="/Dockerfile" \
			org.label-schema.name="MQTT BROKER"
	EOI
}

# Print metadata && basepackages
print_basepackages() {
	cat >> $1 <<-'EOI'	
	ENV \
    	INITSYSTEM on \
    	DEBIAN_FRONTEND=noninteractive \
    	DOMI_MQTT_PORT="1884" \
		APPDIR="/MQTT_BROKER"
EOI
}

# install Mosquito
print_mosquito(){
	cat >> $1 <<-'EOI'
	#--------------Mosquito--------------#
	RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
	RUN apt-get -qq update > /dev/null && DEBIAN_FRONTEND=noninteractive apt-get -qq -y --no-install-recommends install \
    	mosquitto-clients \
		avahi-daemon \
    	mosquitto && \
		apt-get clean && \
		rm -rf /var/lib/apt/lists/ */tmp/* /var/tmp/*

EOI
}

# Set working directory and execute command
print_command() {
	cat >> $1 <<-'EOI'
	# Execute command
	EXPOSE 1883
	#ADD entrypoint.sh /
	ADD logo /
	#RUN chmod +x /entrypoint.sh
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
		print_basepackages ${file};
		print_mosquito ${file};
		print_command ${file};
		cp logo dockerfile/${arch}/logo
		echo "done"
done