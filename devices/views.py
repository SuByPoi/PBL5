from django.http import JsonResponse
from django.shortcuts import render
from .models import Device, Room, Door_Infomation
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
#import picamera
import time
from PIL import Image
import random
import string
from io import BytesIO

from .serializers import DoorSerializer, RoomSerializer, DeviceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
#import RPi.GPIO as GPIO
# Create your views here.

doorPin = 20

@api_view((['GET']))
@permission_classes([IsAuthenticated])
def api_get_rooms(request):
    #get_status()
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many = True)
    return JsonResponse(serializer.data, safe = False)


@api_view((['GET']))
@permission_classes([IsAuthenticated])
def api_get_door_info(request):
    infomation = Door_Infomation.objects.all()
    serializer = DoorSerializer(infomation, many = True)
    return JsonResponse(serializer.data, safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_devices(request, roomId):
    #get_status()
    devices = Device.objects.filter(room = roomId)
    serializer = DeviceSerializer(devices, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_device(request, roomId, deviceId):
    #get_status()
    queryset = Device.objects.filter(room = roomId).filter(id = deviceId)
    if not queryset.exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    device = queryset.get(id = deviceId)

    if request.method == 'POST':
        now = datetime.now()
        if device.status == True:
            #GPIO.output(device.pin, GPIO.LOW)

            device.status = False
            device.last_Active = now

            if device.pin == doorPin:
                #img_path = capture_picture()
                info = Door_Infomation()
                info.status = False
                info.time = now
                info.user = request.user
                #info.img = img_path
                info.save()
            
        else:
            #GPIO.output(device.pin, GPIO.HIGH)
            device.status = True

            if device.pin == doorPin:
                info = Door_Infomation()
                info.status = True
                info.time = now
                info.user = request.user
                info.img = None
                info.save()
        device.save()
        data = DeviceSerializer(device)
        return JsonResponse(data.data, safe=False)
    
    serializer = DeviceSerializer(device)
    return JsonResponse(serializer.data, safe=False)

@login_required
def rooms_view(request):
    #get_status()
    queryset = Room.objects.all()
    context = {
        'rooms': queryset,
        'username' : request.user
    }
    return render(request, 'rooms.html', context)

@login_required
def door_infomation_view(request):
    #get_status()
    queryset = Door_Infomation.objects.all()
    context = {
        'infomations': queryset.order_by('-time'),
        'username' : request.user
    }
    return render(request, 'infomations.html', context)

@login_required
@csrf_exempt
def devices_view(request, roomId):
    #get_status()
    if request.method == 'POST':
        pin = request.POST.get('pin')
        if pin != None:
            pin = int(pin)
            now = datetime.now()
            device = Device.objects.get(pin = pin)
            if device.status == True:
                #GPIO.output(pin, GPIO.LOW)
                device.status = False
                device.last_Active = now

                if device.pin == doorPin:
                    #img_path = capture_picture()
                    info = Door_Infomation()
                    info.status = False
                    info.user = request.user
                    #info.img = img_path
                    info.time = now
                    info.save()
            else:
                #GPIO.output(pin, GPIO.HIGH)
                device.status = True

                if device.pin == doorPin:
                    info = Door_Infomation()
                    info.status = True
                    info.user = request.user
                    info.time = now
                    info.img = None
                    info.save()
            device.save()

    room = Room.objects.filter(id = roomId)
    room = room.first()
    queryset = Device.objects.filter(room = roomId)
    context = {
        'devices': queryset,
        'room': room,
        'username': request.user
        }
    return render(request, 'devices.html', context)


# def get_status():
#     devices = Device.objects.all()
#     GPIO.setwarnings(False)               
#     GPIO.setmode(GPIO.BCM)
#     for device in devices:
#         GPIO.setup(device.pin, GPIO.OUT)
#         device.status = GPIO.input(device.pin)
#         device.save()  
# def get_random_string(length):
#     # choose from all lowercase letter
#     letters = string.ascii_lowercase
#     result_str = ''.join(random.choice(letters) for i in range(length))
#     return result_str + ('.jpg')
# def capture_picture():
#     try:
#         with picamera.PiCamera() as camera:
#             camera.resolution = (1024, 768)
#             camera.start_preview()
#             time.sleep(2)
#             file_name = get_random_string(30)
#             save_path = "media/documents/" + file_name
#             file_path = "documents/" + file_name
#             camera.capture(save_path, resize=(640, 480))
#             camera.stop_preview()
#             return file_path
#     except:
#         print('Something is error')