# Jenkins_Status
Python project to broadcast Jenkins project build status using the MQTT protocol. 
Jenkins_indicator.py is the main program to be run from this project, this will pool Jenkins API for the status of project names provided in a JSON formated file called indicator_config.json, the server credential are provided in another file called server_config.json.
The application can be run as follows: 
```python jenkins_indicator.py --indicator_config ../config/indicator_config.json --server_config ../config/server_config.json --interval 10```

The configuration files are stored in the config folder and log outputs will be stored in the log folder. 


