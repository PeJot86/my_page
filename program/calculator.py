from flask import Flask, render_template, request
from program import app
import requests
import datetime

from sqlalchemy import null

items=["PLN", "PLN"]

response = requests.get('http://api.nbp.pl/api/exchangerates/tables/A?format=json')
data = response.json()

rates = data[0]["rates"]
exchange_rate_mid = {'PLN':1.0}


for rate in rates:
    exchange_rate_mid[rate["code"]] = rate["mid"]



@app.route("/calculator", methods=["GET"])
def calculator():
    euro = (exchange_rate_mid["EUR"])
    return render_template("calculator/exchange.html", euro=euro)


def test():
    return ['ddd','test']


@app.route("/calculator", methods=["GET", "POST"])
def calculate_mid():
    if request.method == "POST":
        data = request.form
        choice_quantity = data.get("number")
        choice_have_currency = data.get('have_currency')
        items.append (choice_have_currency)
        choice_want_currency = data.get('want_currency')
        items.append(choice_want_currency)
        currency_have_value = exchange_rate_mid[choice_have_currency]  
        currency_want_value = exchange_rate_mid[choice_want_currency]
        calc = float(choice_quantity) * float(currency_have_value) / float(currency_want_value)
        calc_heading = float(currency_have_value) / float(currency_want_value)
        heading = (round (calc_heading, 2))
        result = (round (calc, 2))
        return render_template("calculator/exchange.html", result = result, choice_have_currency=choice_have_currency, choice_quantity=choice_quantity, choice_want_currency=choice_want_currency, currency_want_value=currency_want_value, heading=heading)       
    return render_template("calculator/exchange.html")


@app.context_processor
def date_time ():
    d = datetime.datetime.utcnow()
    return dict(day=(f"{d:%d}"), month=(f"{d:%m}"), year=d.year, hour=(f"{d:%H}"), minute=(f"{d:%M} UTC"))


@app.context_processor
def home():
    choice_quantity = ""
    choice_have_currency = items[-2]
    choice_want_currency = items[-1]
    number = 1
    return dict(choice_quantity=choice_quantity, choice_have_currency=choice_have_currency,choice_want_currency=choice_want_currency, number=number )

