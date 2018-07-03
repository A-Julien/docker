# Shutdown RPI
* Connect the gpio to the GND.
* Choose the GPIO in config.json (*BCM* mode)
* Create directory in ```mkdir /opt/powerOff ```
* Paste the config file in the directory ```cp config.json /opt/powerOff ```
* Run container :  

```		
docker run \
        -tid \
        --privileged \
        -v /opt/powerOff:/opt/powerOff \
        -v /var/run/systemd:/var/run/systemd \
        jalaimo/power_off_pi
``` 
        
