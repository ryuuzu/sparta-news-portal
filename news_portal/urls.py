from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

from .views import LoginView, RegisterView, HomepageView

# all url patterns to access
urlpatterns = [
    path('', HomepageView.as_view(), name="home"),
    path('forex/', views.forex_api, name="Forex"),
    path('horoscope/', views.horoscope_api, name="Horoscope"),
    path('weather/', views.weather_api, name="Weather"),

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),

    path('addnews/', views.add_news, name="addnews"),
    path('reportnews/<int:pk>', views.report_news, name="reportnews"),
    path('addcomment/<int:pk>', views.add_comment, name="addcomment"),
    path('addevidence/<int:pk>', views.add_evidence, name="addevidence"),
    path('requestad/', views.request_ad, name="requestad"),
    path('reedemcoin/', views.redeem_coins, name="reedemcoin"),
]
