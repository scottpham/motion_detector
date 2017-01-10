from django.core.management.base import BaseCommand, CommandError
import RPi.GPIO as GPIO
import time
import datetime
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from time import sleep

from sensor.models import Reading

class Command(BaseCommand):
    help = "Starts the raspberry pi sensor"

    def handle(self, *args, **options):

        #GPIO 17 connects to middle plug of sensor
        sensor = 17

        #GPIO Boilerplate
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

        def recordChange(value):
            print "recording change"
            # date formatter
            # formatter = "%Y-%m-%d %H:%M"
            # record time
            # now = datetime.datetime.now().strftime(formatter)
            # if value == 1:
            #     print "There was movement at %s" % (now)
            # else:
            #     print "there was no movement at %s" % (now)

            # save to database
            r = Reading(date_time = timezone.now(), value = value)
            print r

            r.save()
        # watch each second for 60 seconds and then record result
        def watch():
            # states list
            reading_list = []

            while len(reading_list) < 60:
                # take reading
                current_reading = GPIO.input(sensor)
                # write state to list of states
                reading_list.append(current_reading)
                # log state to the console
                print current_reading
                sleep(1)

            # 60 seconds later...
            # if there is 1 or more instance of '1'
            if reading_list.count(1) > 0:
                recordChange(1)
            else:
                recordChange(0)

            #empty list
            reading_list = []

        watch()

        # # sched = BlockingScheduler()
        # sched = BackgroundScheduler()
        #
        # # Schedules job_function to be run once each minute
        # sched.add_job(watch, 'cron', minute='0-59')
        #
        # sched.start()
