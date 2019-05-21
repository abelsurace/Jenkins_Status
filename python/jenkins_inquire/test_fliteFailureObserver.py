#!/usr/bin/python

from unittest import TestCase, main
from jenkins_watchdog import  TTSFailureObserver
#name, description, is_success, is_failed, was_good_previously, is_running, start_time, estimated_time

class TestTTSFailureObserver(TestCase):
    def test_on_new_build_info(self):
        observer = TTSFailureObserver({"SO1-android": 14})
        observer.on_new_build_info("SO1-android", "iglass editor", False, True, False, False, 0, 0)
        observer.on_new_build_info("SO1-android", "iglass portal", True, False, False, False, 0, 0)
        observer.on_new_build_info("SO1-android", "Work Manager", False, False, False, False, 0, 0)


if __name__ == '__main__':
    main()
