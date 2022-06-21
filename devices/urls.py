from django.urls import path
from .views import api_get_devices, api_get_rooms, rooms_view, devices_view, api_device, door_infomation_view, api_get_door_info

urlpatterns = [
    path(('rooms/'), rooms_view, name = 'rooms'),
    path(('rooms/<int:roomId>/devices'), devices_view, name = 'devices'),
    path(('doorLogs/'), door_infomation_view, name = 'door_info'),
    path(('api/doorLogs'), api_get_door_info, name = 'door_info_api'),
    path(('api/rooms'), api_get_rooms, name = 'rooms_api'),
    path(('api/rooms/<int:roomId>/devices'), api_get_devices ,name = 'devices_api'),
    path(('api/rooms/<int:roomId>/devices/<int:deviceId>'), api_device, name = 'device_api')
]