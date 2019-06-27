#!/usr/bin/python

from unittest import TestCase, main
from jenkins_watchdog import  TTSFailureObserver, MQTTFailureObserver, MqttBroker
#name, description, is_success, is_failed, was_good_previously, is_running, start_time, estimated_time
broker = MqttBroker("52.36.159.178", "1883", "mosco", "mosco")


class TestTTSFailureObserver(TestCase):
    def test_on_new_build_info(self):
        observer = TTSFailureObserver({"SO1-android": "jenkins"})
        observer.on_new_build_info("SO1-android", "jenkins", "iglass editor", False, True, False, False, 0, 0)
        observer.on_new_build_info("SO1-android", "jenkins", "iglass portal", True, False, False, False, 0, 0)
        observer.on_new_build_info("SO1-android", "jenkins", "Work Manager", False, False, False, False, 0, 0)

class TestMQTTFailureObserver(TestCase):
    def test_on_new_build_info(self):
        observer2 = MQTTFailureObserver(broker, {"SO1-android": "jenkins"})
        observer2.on_new_build_info("SO1-android", "jenkins", "iglass editor", False, True, False, False, 0, 0)
        observer2.on_new_build_info("SO1-android", "jenkins", "iglass portal", True, False, False, False, 0, 0)
        observer2.on_new_build_info("SO1-android", "jenkins", "Work Manager", False, False, False, False, 0, 0)



if __name__ == '__main__':
    main()
