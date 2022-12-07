from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="Home Page"),
    path('forex/', views.forexapi, name="Forex"),
    path('horoscope/', views.horoscopeapi, name="Horoscope"),
    path('weather/', views.weatherapi, name="Weather"),
    path('login/', views.login, name="login"),
]
