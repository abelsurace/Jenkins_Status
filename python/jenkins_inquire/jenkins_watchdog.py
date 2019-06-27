import subprocess

from mqtt_wrapper import State, MQTTBroadcast
import os
import logging

log = logging.getLogger('jenkins_indicator')


class Watcher(object):
    def on_new_build_info(self, name, topic, description, is_success, is_failed, was_good_previously, is_running, start_time,
                          estimated_time):
        pass

    def on_no_info_available(self, name):
        pass
class MqttBroker(object):
    def __init__(self, address, port, username, password):
        self.address = address
        self.port = port
        self.username = username
        self.password = password


class MQTTFailureObserver(Watcher):
    def __init__(self, broker, configuration):
        self.configuration = configuration
        self.mqtt_broadcast = MQTTBroadcast(broker)
        self.broker = broker
        self.previous_running = {}
        self.is_oks ={}
        for c in configuration.keys():
            self.is_oks[c] = True
            self.previous_running[c] = False
    def on_no_info_available(self, name):
        self.is_oks[name] = State.Off

    def on_new_build_info(self, name, topic, description, is_success, is_failed, was_good_previously, is_running, start_time,
                          estimated_time):
        if not is_running:
            previous_good = self.is_oks[name]
            self.previous_running = {}
            self.previous_running[name] = False
            if is_success:
                self.is_oks[name] = True
            if is_failed:
                self.is_oks[name] = False
            now_ok = self.is_oks[name]
            if previous_good and (not now_ok):
                self.mqtt_broadcast.send_project_info( topic, "broken")
            if (not previous_good) and now_ok:
                self.mqtt_broadcast.send_project_info( topic, "successful")
        if is_running:
            if (not self.previous_running[name]):
                self.mqtt_broadcast.send_project_info( topic, "inprogress")
            self.previous_running[name] = True


        
class TTSFailureObserver(Watcher):
    def __init__(self, configuration):
        self.is_oks = {}
        self.previous_running = {}
        self.configuration = configuration
        for c in configuration.keys():
            self.is_oks[c] = True
            self.previous_running[c] = False

    def on_no_info_available(self, name):
        self.is_oks[name] = State.Off

    def on_new_build_info(self, name, topic, description, is_success, is_failed, was_good_previously, is_running, start_time,
                          estimated_time):
        template = "google_speech -l en '{}'"
        if not is_running:
            previous_good = self.is_oks[name]
            self.previous_running[name] = False

            if is_success:
                self.is_oks[name] = True

            if is_failed:
                self.is_oks[name] = False

            now_ok = self.is_oks[name]

            if previous_good and (not now_ok):
                message = '{} - Build has been broken'.format(name)
                log.debug("Speaking message :{}".format(message))
                command = template.format(message)
                log.debug("running command =" + command)
                os.system(command)
            if (not previous_good) and now_ok:
                message = '{} - Build is back to normal'.format(name)
                log.debug("Speaking message :{}".format(message))
                command = template.format(message)
                log.debug("running command =" + command)
                os.system(command)

        if is_running:
            if (not self.previous_running[name]):
                message = '{} - build in progress'.format(name)
                log.debug("Speaking message :{}".format(message))
                command = template.format(message)
                log.debug("running command =" + command)
                os.system(command)
            self.previous_running[name] = True

class VoiceWatcher(Watcher):
    def __init__(self, configuration, audio_file):
        self.is_oks = {}
        self.is_running = {}
        self.configuration = configuration
        self.audio_file = audio_file
        for c in configuration.keys():
            self.is_oks[c] = True
            self.is_running[c] = False

    def on_no_info_available(self, name):
        self.is_oks[name] = State.Off

    def on_new_build_info(self, name, topic, description, is_success, is_failed, was_good_previously, is_running, start_time,
                          estimated_time):
        if not is_running:
            previous_good = self.is_oks[name]

            if is_success:
                self.is_oks[name] = True

            if is_failed:
                self.is_oks[name] = False

            now_ok = self.is_oks[name]

            if (previous_good and (not now_ok)):
                subprocess.call(("omxplayer", self.audio_file))


