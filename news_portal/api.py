import requests

urlHoroscope = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"
headershoroscope = {
    "X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
    "X-RapidAPI-Host": "sameer-kumar-aztro-v1.p.rapidapi.com",
}

urlForex = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
headersforex = {
    "X-RapidAPI-Key": "bb0db28f73msh13b9827639755afp1f8800jsnaba709482da2",
    "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
}


class Horoscope:
    def __init__(self, name, details, date, date_range):
        self.name = name
        self.details = details
        self.date = date
        self.date_range = date_range

    def __str__(self) -> str:
        return self.name


class Forex:
    def __init__(self, currency, buy_rate, sell_rate):
        self.currency = currency
        self.buy_rate = buy_rate
        self.sell_rate = sell_rate

    def __str__(self) -> str:
        return self.currency


def get_forex():
    try:
        response = requests.get("https://www.nrb.org.np/api/forex/v1/rate")
        json_data = response.json()
    except requests.ConnectTimeout:
        return None
    inr = json_data["data"]["payload"]["rates"][0]
    usd = json_data["data"]["payload"]["rates"][1]
    eur = json_data["data"]["payload"]["rates"][2]
    pound = json_data["data"]["payload"]["rates"][3]

    forex = [
        Forex(inr["currency"]["name"], inr["buy"], inr["sell"]),
        Forex(usd["currency"]["name"], usd["buy"], usd["sell"]),
        Forex(eur["currency"]["name"], eur["buy"], eur["sell"]),
        Forex(pound["currency"]["name"], pound["buy"], pound["sell"]),
    ]
    return forex


def get_horoscopes():
    horoscopes_list = [
        "pisces",
        # "aries",
        # "taurus",
        # "gemini",
        # "cancer",
        # "leo",
        # "virgo",
        # "libra",
        # "scorpio",
        # "sagittarius",
        # "capricorn",
    ]
    horoscope = []
    for horoscope_name in horoscopes_list:
        querystring = {"sign": horoscope_name, "day": "today"}
        response = requests.post(
            urlHoroscope, headers=headershoroscope, params=querystring
        )
        horoscope_data = response.json()
        horoscope.append(
            Horoscope(
                horoscope_name,
                horoscope_data["description"],
                horoscope_data["current_date"],
                horoscope_data["date_range"],
            )
        )
    return horoscope
