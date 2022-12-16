from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from . import views

from .views import (
    CategoryView,
    CreateNewsView,
    LoginView,
    ProfileUpdateView,
    ProfileView,
    RegisterView,
    HomepageView,
    view_news,
)

# all url patterns to access
urlpatterns = [
    path("", HomepageView.as_view(), name="home"),
    path("category/<str:cat_name>/", CategoryView.as_view(), name="cat_view"),
    path("news/create/", CreateNewsView.as_view(), name="create_news"),
    path("news/<slug:slug>/", view_news, name="view_news"),
    path("weather/", views.weather_api, name="Weather"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="view_profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="update_profile"),
    path("addnews/", views.add_news, name="addnews"),
    path("reportnews/<int:pk>", views.report_news, name="reportnews"),
    path("addcomment/<int:pk>", views.add_comment, name="addcomment"),
    path("addevidence/<int:pk>", views.add_evidence, name="addevidence"),
    path("requestad/", views.request_ad, name="requestad"),
    path("reedemcoin/", views.redeem_coins, name="reedemcoin"),
]
