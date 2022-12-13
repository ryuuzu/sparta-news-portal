from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="Home Page"),
    path('forex/', views.forex_api, name="Forex"),
    path('horoscope/', views.horoscope_api, name="Horoscope"),
    path('weather/', views.weather_api, name="Weather"),

    path('login/', views.login, name="login"),

    path('addnews/', views.add_news, name="addnews"),
    path('reportnews/<int:pk>', views.report_news, name="reportnews"),
    path('addcomment/<int:pk>', views.add_comment, name="addcomment"),
    path('addevidence/<int:pk>', views.add_evidence, name="addevidence"),
    path('requestad/', views.request_ad, name="requestad"),

]
