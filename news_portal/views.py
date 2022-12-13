# all required imports
from django.shortcuts import render, redirect
from .forms import NewsForm, EvidenceForm, CommentForm, ReportedNewsForm, AdRequestForm
from .models import News, Reporter, RewardGranted
import requests
import json

#urls and headers for apis
urlForex = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
headersforex = {
	"X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
	"X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
}

urlHoroscope = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"
headershoroscope = {
	"X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
	"X-RapidAPI-Host": "sameer-kumar-aztro-v1.p.rapidapi.com"
}

urlCurrency = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/symbols"

# views for generating reward based on coins
def redeem_coins(request, pk):
    if request.method == "POST":
        reporter = Reporter.objects.get(id=pk)
        all_news = News.objects.filter(created_by=reporter)
        total_reward = 0
        for news in all_news:
            current_reward = news.view_count - news.coin_generated
            total_reward += current_reward
            news.coin_generated = news.view_count
            news.save()
        reward = RewardGranted(user_id =reporter, coins_reedemed = total_reward, monetary_value = total_reward)
        reward.save()
        return redirect('index') #coin generated page
    return redirect('index') #cannot access through get

#the main page of the app.
def index(request):
    news = NewsForm()
    report = ReportedNewsForm()
    comment = CommentForm()
    evidence = EvidenceForm()
    ad = AdRequestForm()
    context = {
        "news":news,
        "report":report,
        "comment":comment,
        "evidence":evidence,
        "ad":ad
    }
    return render(request, "renderforms.html", context)


# view to render login
def login(request):
    return render(request, "login.html")


#the page to add news
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
       
        return render(request, "checkformlogic.html", {"form":form})
    return render(request, "checkformlogic.html")


#handle the reported news
def report_news(request, pk):
    pass

#handle comments added in news
def add_comment(request, pk):
    pass

#handle evidence added for news
def add_evidence(request, pk):
    pass

#the page to request ads
def request_ad(request):
    if request.method == "POST":
        form = AdRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
        return render(request, "checkformlogic.html", {"form":form})
    return render(request, "checkformlogic.html")

#get horoscope from api and render result
def horoscope_api(request):
    horoscope = ['pisces','aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpion', 'sagittarius', 'capricorn']
    if request.method == "POST":
        sign = request.POST.get('sign')
        querystring = {"sign":sign,"day":"today"}
        response = requests.request("POST", urlHoroscope, headers=headershoroscope, params=querystring)
        return render(request,"horoscope.html", {'response':response.text, 'horoscope':horoscope})

    return render(request,"horoscope.html", {'horoscope':horoscope})

#get weather from api and render result
def weather_api(request):
    cities = [
        'Kathmandu', 'Pokhara', 'Lumbini', 'Butwal', 'Biratnagar'
    ]
    if request.method == "POST":
        city = request.POST.get('city')
        response = requests.request("POST", "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=9cafb52078077411bf7a0a82cbc790c3&units=metric")
        return render(request,"weather.html", {'cities':cities, 'response':response.text})
    
    return render(request,'weather.html', {'cities':cities})

#get forex from api and render result
def forex_api(request):
    currency = requests.request("GET", urlCurrency, headers=headersforex)
    currency = json.loads(currency.text)
    if request.method=="POST":
        fro = request.POST.get('fromcurrency')
        to = request.POST.get('tocurrency')
        amount = request.POST.get('amount')
        querystring = {"from":fro,"to":to,"amount":amount}
        response = requests.request("GET", urlForex, headers=headersforex, params=querystring)
        return render(request,"forex.html", {'currency':currency['symbols'], 'response':response.text})

    return render(request,"forex.html", {'currency':currency['symbols']})
