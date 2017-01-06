from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core import serializers
from .models import Reading
import json
from datetime import datetime

# Create your views here.
def index(request):
    readings = Reading.objects.all().order_by('-date_time')[:2000]

    template = loader.get_template('sensor/index.html')

    data = serializers.serialize('json', readings)

    context = { 'readings': readings, 'data': data}

    # return HttpResponse(template.render(context, request))
    return render(request, 'sensor/index.html', context)

def today(request):
    # get integer number of today
    today = datetime.now().day

    # get readings, filter for today only
    readings = Reading.objects.filter(date_time__day=today).order_by('-date_time')

    template = loader.get_template('sensor/index.html')

    data = serializers.serialize('json', readings)

    context = { 'readings': readings, 'data': data}

    return render(request, 'sensor/today.html', context)
