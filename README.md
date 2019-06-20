# Jenkins_Status
Python project to broadcast Jenkins project build status by voice (TTS) using google-speech and change an IOT RGB light color using the MQTT protocol, more details about the IOT RGB light below.

The main program to be run from this project is jenkins_indicator.py, this will pull Jenkins API for the status of different project names provided in a JSON formated file called indicator_config.json, the server credential are provided in another file called server_config.json, this file also contains the MQTT broker credentials.

The application can be run as follows: 
```python jenkins_indicator.py --indicator_config ../config/indicator_config.json --server_config ../config/server_config.json --interval 10```

The configuration files location, names and interval, are defaulted so if they are not changed then it can be run without this parameters. The interval is the wating time before a new status is pulled from jenkins server, by default is 10 sec. 

To display help run ```python jenkins_indicator.py -h``` and to list all the projects available from a particular jenkins server use -l option ```python jenkins_indicator.py -l```

The configuration files are stored in the config folder and log outputs will be stored in the log folder. 

# IOT RGB Light
This light was developed using the Expressif 8266 wifi microcontroller board. For this project the board was programmed using the Mongoose OS (Cesanta) development kit.
The board controls an RGB led ring array, Neopixel from Adafruit. The board is suscribe to a topic to a given mqtt mosquito broker where a message can be broadcasted, the message is formated as a jason string where the build status is advertised, then based on the status the light color is changed to red (broken), blue (successful) and green (in progress).
```{"gpio":{"status":"broken"}}```. For more details, code and files to 3D print all the parts see githuh repo:



