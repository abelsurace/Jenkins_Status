import subprocess

from jenkins_inquire.mqtt_wrapper import State, MQTTBroadcast
import os
import logging

log = logging.getLogger('jenkins_indicator')


class Watcher(object):
    def on_new_build_info(self, name, description, is_success, is_failed, was_good_previously, is_running, start_time,
                          estimated_time):
        pass

    def on_no_info_available(self, name):
        pass


class VoiceWatcher(Watcher):
    def __init__(self, configuration, audio_file):
        self.is_oks = {}
        self.configuration = configuration
        self.audio_file = audio_file
        for c in configuration.keys():
            self.is_oks[c] = True

    def on_no_info_available(self, name):
        self.is_oks[name] = State.Off

    def on_new_build_info(self, name, description, is_success, is_failed, was_good_previously, is_running, start_time,
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


class TTSFailureObserver(Watcher):
    def __init__(self, configuration):
        self.is_oks = {}
        self.configuration = configuration
        for c in configuration.keys():
            self.is_oks[c] = True

    def on_no_info_available(self, name):
        self.is_oks[name] = State.Off

    def on_new_build_info(self, name, description, is_success, is_failed, was_good_previously, is_running, start_time,
                          estimated_time):
        template_fail = "espeak -s140 -ven-english-5+m3 --stdout '{}' | aplay"
        template_success = "espeak -s140 -ven-english-5+m3 --stdout '{}' | aplay"
        if not is_running:
            previous_good = self.is_oks[name]

            if is_success:
                self.is_oks[name] = True

            if is_failed:
                self.is_oks[name] = False

            now_ok = self.is_oks[name]

            if previous_good and (not now_ok):
                message = '{} - Build has been broken'.format(description)
                log.debug("Speaking message :{}".format(message))
                command = template_fail.format(message)
                log.debug("running command =" + command)
                os.system(command)
            if (not previous_good) and now_ok:
                message = '{} - Build is back to normal'.format(description)
                log.debug("Speaking message :{}".format(message))
                command = template_success.format(message)
                log.debug("running command =" + command)
                os.system(command)
