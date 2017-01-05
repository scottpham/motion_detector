from django.core.management.base import BaseCommand, CommandError
import RPi.GPIO as GPIO
import time
import datetime
from django.utils import timezone

from sensor.models import Reading

class Command(BaseCommand):
    help = "Starts the raspberry pi sensor"

    def handle(self, *args, **options):

        #GPIO 17 connects to middle plug of sensor
        sensor = 17

        #GPIO Boilerplate
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

        # date formatter
        formatter = "%Y-%m-%d %H:%M"

        # states list
        states = []


        def recordChange(value):
            # record time
            now = datetime.datetime.now().strftime(formatter)
            #
            # if value == 1:
            #     print "There was movement at %s" % (now)
            # else:
            #     print "there was no movement at %s" % (now)

            # save to database
            r = Reading(date_time = timezone.now(), value = value)

            r.save()

        # run this continuously
        while True:
            # wait a second
            time.sleep(1)

            # take reading
            current_state = GPIO.input(sensor)

            # write state to list of states
            states.append(current_state)

            # log state to the console
            # print current_state

            # after 60 seconds, log value to csv
            if len(states) >= 60:
                if states.count(1) >= 1:
                    recordChange(1)
                else:
                    recordChange(0)

                #empty list
                states = []
