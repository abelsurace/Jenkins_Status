
#      _____                      __        __                     
#     /     |                    /  |      /  |                    
#     $$$$$ |  ______   _______  $$ |   __ $$/  _______    _______ 
#        $$ | /      \ /       \ $$ |  /  |/  |/       \  /       |
#   __   $$ |/$$$$$$  |$$$$$$$  |$$ |_/$$/ $$ |$$$$$$$  |/$$$$$$$/ 
#  /  |  $$ |$$    $$ |$$ |  $$ |$$   $$<  $$ |$$ |  $$ |$$      \ 
#  $$ \__$$ |$$$$$$$$/ $$ |  $$ |$$$$$$  \ $$ |$$ |  $$ | $$$$$$  |
#  $$    $$/ $$       |$$ |  $$ |$$ | $$  |$$ |$$ |  $$ |/     $$/ 
#   $$$$$$/   $$$$$$$/ $$/   $$/ $$/   $$/ $$/ $$/   $$/ $$$$$$$/  
# \033[1;33m
#    ______    __                  __                              
#   /      \  /  |                /  |                             
#  /$$$$$$  |_$$ |_     ______   _$$ |_    __    __   _______      
#  $$ \__$$// $$   |   /      \ / $$   |  /  |  /  | /       |     
#  $$      \$$$$$$/    $$$$$$  |$$$$$$/   $$ |  $$ |/$$$$$$$/      
#   $$$$$$  | $$ | __  /    $$ |  $$ | __ $$ |  $$ |$$      \      
#  /  \__$$ | $$ |/  |/$$$$$$$ |  $$ |/  |$$ \__$$ | $$$$$$  |     
#  $$    $$/  $$  $$/ $$    $$ |  $$  $$/ $$    $$/ /     $$/      
#   $$$$$$/    $$$$/   $$$$$$$/    $$$$/   $$$$$$/  $$$$$$$/       
#                                                                
#  by Abel Surace    

import argparse
import optparse
import textwrap
import sys
import json
import logging.handlers
import copy
from os.path import dirname
from jenkins_inquire.jenkins_watchdog import TTSFailureObserver
from jenkins_inquire import jenkins_poller

log = logging.getLogger('jenkins_indicator')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
fh = logging.handlers.TimedRotatingFileHandler(filename="../log/indicator.log", when='midnight', backupCount=4)
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

log.addHandler(fh)
log.addHandler(ch)
                                            
ROOT_DIR = dirname(__file__)

# Parsing arguments
parser = argparse.ArgumentParser(description='Pulls jenkins and delivers notifications')
parser.add_argument("--indicator_config", "-ic", type=argparse.FileType("r"), default="../config/indicator_config.json", help="Defaults to ../config/indicator_config.json")
parser.add_argument("--server_config", "-sc", type=argparse.FileType('r'),
                    default="../config/server_config.json", help="Defaults to ../config/server_config.json")
parser.add_argument("--interval", "-i", default=10, help="Pooling Interval defaults to 10 seconds")
parser.add_argument("--list_jobs", "-l", action="store_true", dest="list_jobs", default= False , help="List all jobs available from server")
arguments = parser.parse_args()
log.info("Startup arguments:  indicator = {} , server={} ".format(arguments.indicator_config.name,
                                                                  arguments.server_config.name))

with arguments.indicator_config as json_file:
    indicator_config = json.load(json_file)
    log.info("Indicator Configuration loaded:")
    log.info(indicator_config)

with arguments.server_config as json_file:
    server_config = json.load(json_file)
    log.info("Server Configuration loaded:")
    hidden = copy.copy(server_config)
    hidden[u'password'] = "***"
    log.info(hidden)

observers = [TTSFailureObserver(indicator_config)]

jenkins_poller.poll(server_config['url'], server_config['user'], server_config['password'], indicator_config, observers,
                    arguments.interval, arguments.list_jobs)
