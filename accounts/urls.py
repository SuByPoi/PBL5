from django.urls import path , include
from .views import login, logout, register,homepage

urlpatterns = [
    path('', login),
    path('home/',homepage),
    path('logout', logout),
    path('register', register)
]