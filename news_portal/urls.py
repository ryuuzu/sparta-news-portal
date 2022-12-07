from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="Home Page"),
    path('forex/', views.forexapi, name="Forex"),
    path('horoscope/', views.horoscopeapi, name="Horoscope"),
    path('weather/', views.weatherapi, name="Weather"),
    path('addnews/', views.addNews, name="addnews"),
    path('reportnews/<int:pk>', views.reportNews, name="reportnews"),
    path('addcomment/<int:pk>', views.addComment, name="addcomment"),
    path('addevidence/<int:pk>', views.addEvidence, name="addevidence"),
    path('requestad/', views.requestAd, name="requestad"),
]
