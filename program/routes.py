from flask import render_template, redirect, request, session, flash
import json
from program import app
from program.weather import *
from program.warehouse import *
from program.calculator import *
from program.sendmail import *
import random



@app.route("/", methods=["GET", "POST"])
def my_page():
    session["attempt"] = 1
    fortune = random.randrange(1, 100)
    session["fortune"] = fortune
    message = "" 
    if request.method == 'POST':
        data = request.form
        mail_name = data.get("sendmail_name")
        mail_from = data.get("sendmail_email")
        mail_subject = data.get("sendmail_subject")
        mail_message = data.get("sendmail_message")
        send_email_from_page (mail_name, mail_from, mail_subject, mail_message)
        flash ("Dziękujemy! Twoja wiadomość została wysłana!", "success")
        return redirect(url_for("my_page"))
    return render_template("homepage.html", message=message) 
    

@app.route("/shut_down")
def shut_down():
    return redirect("http://www.google.com")


@app.route("/weather", methods=["GET", "POST"])
def weather():
    cities = ""
    air=""
    weather=""
    time = datetime.datetime.now()
    if time.month < 10:
        show =  (F"Pogoda z dnia: {time.day}.0{time.month}.{time.year} r. Źródło: IMGW")
    else:
        show =  (F"Pogoda z dnia: {time.day}.{time.month}.{time.year} r. Źródło: IMGW")
    if request.method == "POST":
        data = request.form
        cities = data.get("city")
        get_city(cities)
        get_id(cities)
        get_air(cities)
        air = main_air(cities)
        weather = main_weather(cities)
    return render_template("weather.html", cities=cities, time=time, show=show, weather=weather, air=air)


@app.route("/game", methods=["GET", "POST"])
def game():
    fortune = session.get("fortune")
    attempt = session.get("attempt")
    resp=""
    if request.method == "POST":
        data = request.form
        get_number = data.get("number")
        number = int(get_number)
        if number < fortune: 
            resp = (f"Próba: {attempt}.\nTo za mało, próbuj dalej...")
            session["attempt"] += 1
        elif number > fortune: 
            resp = (f"Próba: {attempt}.\nTo za dużo, próbuj dalej...")
            session["attempt"] += 1  
        elif number == fortune and attempt == 1:
            resp = ("Złoty strzał! GRATULACJE! Może zagrasz w Totolotka?")
            session["fortune"] = random.randrange(1, 100)
            session["attempt"] = 1
        else: 
            resp = (f"Tak, gratulacje, ta liczba to {fortune}. Ilość prób: {attempt}")       
            session["fortune"] = random.randrange(1, 100)
            session["attempt"] = 1
    return render_template("game.html", resp=resp)

