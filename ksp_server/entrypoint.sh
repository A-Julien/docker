#!/bin/bash

#************************************************
#  Start up DSPServer
#************************************************
echo 'start up'

sleep 5
mono /DMPServer/DMPServer.exe 

#keep container alive
exec "$@"