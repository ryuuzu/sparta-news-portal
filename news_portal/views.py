from django.shortcuts import render
from .forms import NewsForm, EvidenceForm, CommentForm, ReportedNewsForm, AdRequestForm
import requests
import json

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

urlWeather = "https://weatherapi-com.p.rapidapi.com/current.json"
headersweather = {
    "X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
}

urlCurrency = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/symbols"

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


def login(request):
    return render(request, "news_portal/users/login.html")


# the page to add news
def addNews(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()

        return render(request, "news_portal/checkformlogic.html", {"form": form})
    return render(request, "news_portal/checkformlogic.html")


# handle the reported news
def reportNews(request, pk):
    pass


# handle comments added in news
def addComment(request, pk):
    pass


# handle evidence added for news
def addEvidence(request, pk):
    pass


def requestAd(request):
    if request.method == "POST":
        form = AdRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
        return render(request, "news_portal/checkformlogic.html", {"form": form})
    return render(request, "news_portal/checkformlogic.html")


# get horoscope from api and render result
def horoscopeapi(request):
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
def weatherapi(request):
    cities = [
        "Kathmandu",
        "Pokhara",
        "Lumbini",
        "Butwal",
        "Jhapa",
        "Illam",
        "Humla",
        "Jumla",
    ]
    if request.method == "POST":
        city = request.POST.get("city")
        querystring = {"q": city + ", NP"}
        response = requests.request(
            "GET", urlWeather, headers=headersweather, params=querystring
        )
        return render(
            request,
            "news_portal/weather.html",
            {"cities": cities, "response": response.text},
        )

    return render(request, "news_portal/weather.html", {"cities": cities})


# get forex from api and render result
def forexapi(request):
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
