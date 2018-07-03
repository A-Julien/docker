# Shutdown RPI
* Connect the gpio to the GND.
* Choose the GPIO in config.json (*BCM* mode)
* Create directory in ```mkdir /opt/power0ff ```
* Paste the config file in the directory ```cp config.json /opt/power0ff ```
* Run container :  

```		
docker run \
		-tid \
		-v /opt/power0ff:/opt/power0ff \
		--privileged \
		jalaimo/power0ff
``` 
        
