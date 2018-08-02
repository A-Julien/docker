#!/bin/bash

arches="armhf arm64"

print_header() {
	cat > $1 <<-EOI
	# powerOff pi image
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
EOI
}


# Set working directory and execute command
print_command() {
	cat >> $1 <<-'EOI'
	# Execute command
	ADD power_off.py ${APPDIR}/
	ADD entrypoint.sh /
	RUN chmod +x /entrypoint.sh
	ENTRYPOINT ["/entrypoint.sh"]
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
		print_command ${file};
		cp entrypoint.sh dockerfile/${arch}/entrypoint.sh
		cp power_off.py dockerfile/${arch}/power_off.py
		echo "done"
done
