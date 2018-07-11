#!/bin/bash
# Generate header

arches="amd64 armhf i386 arm64"
print_header() {
	cat > $1 <<-EOI
	# nodejs image
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

	# Set download urls
	ENV DOMI_URL="https://hub.docker.com/r/jalaimo/nodejs"
	EOI
}

# Print metadata && basepackages
print_basepackages() {
	cat >> $1 <<-'EOI'
	# Set variables
	
	ENV	APPDIR="/domi_cube"

	ENV \
    	INITSYSTEM on \
    	DEBIAN_FRONTEND=noninteractive \
    	DOMI_MQTT_PORT="1884" \
    	LANG=C.UTF-8\
    	LC_ALL=C.UTF-8

	# Basic build-time metadata as defined at http://label-schema.org
	ARG BUILD_DATE
	ARG VCS_REF
	LABEL org.label-schema.build-date=$BUILD_DATE \
    	org.label-schema.docker.dockerfile="/Dockerfile" \
    	org.label-schema.name="nodejs" \
    	org.label-schema.url="https://hub.docker.com/r/jalaimo/nodejs"

	#--------------Install basepackages--------------# 
	RUN apt-get install --no-install-recommends -y \
        build-essential && \
    	apt-get clean

EOI
}
#            libavahi-compat-libdnssd-dev \
#            net-tools \

# Update system
print_update(){
	cat >> $1 <<-'EOI'
	RUN apt-get update --fix-missing && \
        apt-get -y dist-upgrade

EOI
}

# install Nodejs 8.x and dependencies
print_nodejs(){
	cat >> $1 <<-'EOI'
	#--------------Nodejs--------------#
#	RUN apt-get install -y nodejs npm\
#    	&& npm install debug 
#   	&& npm install mdns

	RUN apt-get install -y curl python-software-properties

    RUN	curl -sL https://deb.nodesource.com/setup_8.x | bash - \
    	&& apt-get install -y nodejs \
    	&& npm install debug \
    	&& npm install mdns
EOI
}

# Build the Dockerfiles
if [ ! -d "dockerfile" ]; then
    mkdir dockerfile
fi
for arch in ${arches}
do
	file=dockerfile/${arch}/Dockerfile
		mkdir -p `dirname ${file}` 2>/dev/null
		echo -n "Writing $file..."
		print_header        ${file};
		print_baseimage     ${file};
		print_update        ${file};
		print_basepackages  ${file};
		print_nodejs        ${file};
		echo "done"
done
