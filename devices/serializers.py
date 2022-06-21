from rest_framework import serializers

from .models import Room, Device, Door_Infomation

class RoomSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Room
        fields = ('name','id')

class DeviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Device
        fields = ('id','pin', 'name', 'status', 'last_Active')

class DoorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Door_Infomation
        fields = ('id','status', 'time')
