# all required imports
from typing import Any
from venv import create
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import authenticate, login
import django.contrib.messages as messages

from news_portal.api import get_forex, get_horoscopes

from .forms import (
    NewsForm,
    EvidenceForm,
    CommentForm,
    ReportedNewsForm,
    AdRequestForm,
    UserForm,
    UserRegistrationForm,
    UserEditForm,
)
from .choices import NewsCategory, UserTypes
from .models import News, Reporter, RewardGranted, PortalUser

from .choices import NewsCategory
from .models import News, Reporter, RewardGranted

import requests
import json


# urls and headers for apis
urlForex = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
headersforex = {
    "X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
    "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
}

urlHoroscope = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"
headershoroscope = {
    "X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
    "X-RapidAPI-Host": "sameer-kumar-aztro-v1.p.rapidapi.com",
}

urlCurrency = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/symbols"


def update_profile(request):
    instance = request.user
    user_form = UserEditForm(instance=instance)
    if request.method == "POST":
        get_data = UserEditForm(request.POST)
        if get_data.is_valid():
            get_data.save()
            return redirect("")  # redirect to profile
    return render(request, "", {"user_form": user_form})  # render the edit field


# views for generating reward based on coins
def redeem_coins(request: HttpRequest):
    reporter: PortalUser = request.user
    total_reward = reporter.redeemable
    if total_reward < 100:
        messages.error(request, "You have cannot redeem coins below 100.")
        return redirect("view_profile", reporter.id)
    total_money = total_reward * 0.001
    reward = RewardGranted(
        user_id=reporter,
        coins_redeemed=total_reward,
        monetary_value=total_money,
    )
    reward.save()
    messages.success(request, f"{total_money} coins redeemed successfully")
    return redirect("view_profile", reporter.id)  # coin generated page


# the main page of the app.
def index(request):
    news = NewsForm()
    report = ReportedNewsForm()
    comment = CommentForm()
    evidence = EvidenceForm()
    ad = AdRequestForm()
    context = {
        "news": news,
        "report": report,
        "comment": comment,
        "evidence": evidence,
        "ad": ad,
    }
    return render(request, "news_portal/renderforms.html", context)


def view_news(request: HttpRequest, slug):
    news = get_object_or_404(News, slug=slug)
    news.view_count += 1
    news.save()
    context = {
        "news": news,
        "news_categories": NewsCategory.choices,
        "active_cat": news.category,
        "horoscopes": get_horoscopes(),
        "forex": get_forex(),
    }
    return render(request, "news_portal/news/index.html", context)


class ProfileView(DetailView):
    model = PortalUser
    template_name = "news_portal/users/profile.html"

    def get(self, request: HttpRequest, pk=None, *args: Any, **kwargs: Any):
        if pk:
            user = get_object_or_404(PortalUser, pk=pk)
        else:
            user = request.user
        context = {
            "user_profile": user,
            "news_categories": NewsCategory.choices,
            "active_cat": "profile",
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, pk=None, *args: Any, **kwargs: Any):
        user_form = UserEditForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.error(request, "Profile was updated successfully.")
        else:
            messages.error(request, "Profile wasn't updated.")
        return redirect("view_profile", request.user.id)  # render the edit field


class ProfileUpdateView(TemplateView):
    template_name = "news_portal/users/update.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        user = request.user
        user_form = UserEditForm(instance=user)
        context = {
            "user": user,
            "news_categories": NewsCategory.choices,
            "active_cat": "profile",
            "user_form": user_form,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, pk=None, *args: Any, **kwargs: Any):
        user_form = UserEditForm(request.POST)
        if user_form.is_valid():
            if user_form.has_changed():
                print(user_form.changed_data)
                data = {
                    changed_data: user_form.cleaned_data[changed_data]
                    for changed_data in user_form.changed_data
                }
                if request.FILES.get("photo"):
                    data["photo"] = request.FILES.get("photo")
                for key, value in data.items():
                    setattr(request.user, key, value)
                request.user.save()
            messages.success(request, "Profile was updated successfully.")
        else:
            messages.error(request, "Profile wasn't updated.")
        return redirect("view_profile", request.user.id)  # render the edit field


class HomepageView(TemplateView):
    template_name = "news_portal/home/index.html"

    def get(self, request: HttpRequest):
        breaking_news = News.objects.order_by("-upload_date")[:5]

        partial_news = {}

        for cat in NewsCategory.values:
            partial_news[cat] = News.objects.filter(category=cat).order_by(
                "-upload_date"
            )[:4]

        context = {
            "news_categories": NewsCategory.choices,
            "active_cat": "news",
            "breaking_news": breaking_news,
            "partial_news": partial_news,
        }
        return render(request, self.template_name, context)


class CreateNewsView(TemplateView):
    template_name = "news_portal/news/create.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        create_form = NewsForm()
        context = {"form": create_form}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        create_form = NewsForm(request.POST, request.FILES)
        if create_form.is_valid():
            news = create_form.save(request.user)
            return redirect("view_news", slug=news.slug)


class CategoryView(TemplateView):
    template_name = "news_portal/news/category.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        cat_news = News.objects.filter(category=kwargs["cat_name"]).order_by(
            "-upload_date"
        )[:10]
        if kwargs["cat_name"] not in NewsCategory.values:
            messages.error(request, "Category not found!")
            return redirect("home")
        context = {
            "news_categories": NewsCategory.choices,
            "active_cat": kwargs["cat_name"],
            "all_cat_news": cat_news,
        }
        return render(request, self.template_name, context)


class LoginView(TemplateView):
    template_name = "news_portal/users/login.html"

    def post(self, request: HttpRequest):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")

        messages.error(request, "Username/Password Incorrect")
        return redirect("login")


class RegisterView(TemplateView):
    template_name = "news_portal/users/register.html"

    # get view to send the form
    def get(self, request: HttpRequest):
        form = UserRegistrationForm()
        return render(request, self.template_name, {"form": form})

    # post view to create a user
    def post(self, request: HttpRequest):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


# the page to add news
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()

        return render(request, "news_portal/checkformlogic.html", {"form": form})
    return render(request, "news_portal/checkformlogic.html")


# handle the reported news
def report_news(request, pk):
    pass


# handle comments added in news
def add_comment(request, pk):
    pass


# handle evidence added for news
def add_evidence(request, pk):
    pass


# the page to request ads


def request_ad(request):
    if request.method == "POST":
        form = AdRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
        return render(request, "news_portal/checkformlogic.html", {"form": form})
    return render(request, "news_portal/checkformlogic.html")


# get horoscope from api and render result
def horoscope_api(request):
    horoscope = [
        "pisces",
        "aries",
        "taurus",
        "gemini",
        "cancer",
        "leo",
        "virgo",
        "libra",
        "scorpion",
        "sagittarius",
        "capricorn",
    ]
    if request.method == "POST":
        sign = request.POST.get("sign")
        querystring = {"sign": sign, "day": "today"}
        response = requests.request(
            "POST", urlHoroscope, headers=headershoroscope, params=querystring
        )
        return render(
            request,
            "news_portal/horoscope.html",
            {"response": response.text, "horoscope": horoscope},
        )

    return render(request, "news_portal/horoscope.html", {"horoscope": horoscope})


# get weather from api and render result
def weather_api(request):
    cities = ["Kathmandu", "Pokhara", "Lumbini", "Butwal", "Biratnagar"]
    if request.method == "POST":
        city = request.POST.get("city")
        response = requests.request(
            "POST",
            "https://api.openweathermap.org/data/2.5/weather?q="
            + city
            + "&appid=9cafb52078077411bf7a0a82cbc790c3&units=metric",
        )
        return render(
            request, "weather.html", {"cities": cities, "response": response.text}
        )

    return render(request, "weather.html", {"cities": cities})


# get forex from api and render result
def forex_api(request):
    currency = requests.request("GET", urlCurrency, headers=headersforex)
    currency = json.loads(currency.text)
    if request.method == "POST":
        fro = request.POST.get("fromcurrency")
        to = request.POST.get("tocurrency")
        amount = request.POST.get("amount")
        querystring = {"from": fro, "to": to, "amount": amount}
        response = requests.request(
            "GET", urlForex, headers=headersforex, params=querystring
        )
        return render(
            request,
            "news_portal/forex.html",
            {"currency": currency["symbols"], "response": response.text},
        )

    return render(request, "news_portal/forex.html", {"currency": currency["symbols"]})
