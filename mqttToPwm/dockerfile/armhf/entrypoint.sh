#!/bin/bash
pwd
#************************************************
# Start mosquitto
#************************************************

python ${APPDIR}/PWM.py

#************************************************
# keep container alive
#************************************************
exec "$@"