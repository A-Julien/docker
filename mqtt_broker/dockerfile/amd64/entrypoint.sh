#!/bin/bash
cat /logo
pwd

#************************************************
# Start mosquitto
#************************************************

/usr/sbin/mosquitto

#************************************************
# keep container alive
#************************************************
exec "$@"