#!/usr/bin/python

from enum import IntEnum
import logging

log = logging.getLogger('jenkins_indicator')


class State(IntEnum):
    Off = 0
    Succeeded = 1
    Failed = 2
    InProgressLastSucceeded = 3
    InProgressLastFailed = 4


class MQTTBroadcast(object):
    def __init__(self, broadcast_address, ce_pin=25):
        status = 'OK'
        #self.radio = RF24(ce_pin, 0)
        #self.radio.begin()
        #self.radio.setRetries(0, 0)
        #self.radio.setAutoAck(False)
        #self.radio.setChannel(70)
        #self.radio.setPALevel(RF24_PA_MAX)
        #self.radio.setDataRate(RF24_250KBPS)
        #self.radio.openWritingPipe(broadcast_address)
        #self.radio.printDetails()
        #self.radio.stopListening()

    def send_project_info(self, project_id, indicator_status, progress):
        if progress < 0.30:
            progress = 0.30
        if progress > 1.0:
            progress = 0.9

        byte_progress = int(255 * progress)

        for _ in range(10):
            message = chr(project_id) + chr(indicator_status) + chr(byte_progress)
            log.debug("Sending message " + str(map(ord, message)))
            #self.radio.write(message)
