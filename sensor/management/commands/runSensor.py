from django.core.management.base import BaseCommand, CommandError
import RPi.GPIO as GPIO
import time
import datetime
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler

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

        def recordChange(value):
            # record time
            now = datetime.datetime.now().strftime(formatter)
            # if value == 1:
            #     print "There was movement at %s" % (now)
            # else:
            #     print "there was no movement at %s" % (now)

            # save to database
            r = Reading(date_time = timezone.now(), value = value)

            r.save()

        def watch():
            # states list
            states = []

            while len(states) < 60:
                # take reading
                current_state = GPIO.input(sensor)
                # write state to list of states
                states.append(current_state)
                # log state to the console
                print current_state
                sleep(1)

            # 60 seconds later...
            # if there is 1 or more instance of '1'
            if states.count(1) > 0:
                recordChange(1)
            else:
                recordChange(0)

            #empty list
            states = []

        sched = BlockingScheduler()

        # Schedules job_function to be run once each minute
        sched.add_job(watch, 'cron', minute='0-59')

        sched.start()
