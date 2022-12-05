from django.shortcuts import render
from django.http import HttpResponse

import requests
import json

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

urlWeather = "https://weatherapi-com.p.rapidapi.com/current.json"
headersweather = {
	"X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

urlCurrency = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/symbols"

# Create your views here.
def index(request):
    return HttpResponse('This is homepage.')


def horoscopeapi(request):
    horoscope = ['pisces','aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpion', 'sagittarius', 'capricorn']
    if request.method == "POST":
        sign = request.POST.get('sign')
        querystring = {"sign":sign,"day":"today"}
        response = requests.request("POST", urlHoroscope, headers=headershoroscope, params=querystring)
        return render(request,"horoscope.html", {'response':response.text, 'horoscope':horoscope})

    return render(request,"horoscope.html", {'horoscope':horoscope})

def weatherapi(request):
    cities = [
        'Kathmandu', 'Pokhara', 'Lumbini', 'Butwal', 'Jhapa', 'Illam', 'Humla', 'Jumla'
    ]
    if request.method == "POST":
        city = request.POST.get('city')
        querystring = {"q":city+", NP"}
        #querystring = {"q": "30.0052, 81.9535"}
        response = requests.request("GET", urlWeather, headers=headersweather, params=querystring)
        return render(request,"weather.html", {'cities':cities, 'response':response.text})
    
    return render(request,'weather.html', {'cities':cities})


def forexapi(request):
    currency = requests.request("GET", urlCurrency, headers=headersforex)
    currency = json.loads(currency.text)
    if request.method=="POST":
        fro = request.POST.get('fromcurrency')
        print(fro)
        to = request.POST.get('tocurrency')
        print(to)
        amount = request.POST.get('amount')
        print(amount)
        querystring = {"from":fro,"to":to,"amount":amount}
        response = requests.request("GET", urlForex, headers=headersforex, params=querystring)
        print(response.text)
        return render(request,"forex.html", {'currency':currency['symbols'], 'response':response.text})

    return render(request,"forex.html", {'currency':currency['symbols']})