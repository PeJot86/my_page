import datetime
from requests import get
from json import loads


def get_city (cities):    
    list_city = []
    url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
    response = (get(url))
    
    for i in (loads(response.text)):
        city = extract_city(i['stationName'])
        if city in cities:
            list_city.append (i['stationName'])
    return (list_city)


def get_id(cities):
    list_id = []
    url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
    response = (get(url))
    for i in (loads(response.text)):
        city = extract_city(i['stationName'])
        if city in cities:
            list_id.append (i['id'])            
    return (list_id)


def extract_city (city_with_adress):
    return city_with_adress.split(',')[0]


def get_air (cities):   
    list_id = get_id(cities)
    id_air=[]
    for i in list_id:
        url = "https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/%d" % i
        response = (get(url))
        data = (loads(response.text))
        d = (data ['stIndexLevel'])
        id_air.append (d['indexLevelName'])
    return (id_air)


def main_air(cities): 
    city = get_city(cities)
    id_air = get_air(cities)
    rows = []
    for c in city:
        for i in id_air:
            rows.append (c)
            rows.append (F" - {i.upper()}.")
            break
    return rows


def main_weather (cities):
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    response = get(url)
    rows = []
    for i in (loads(response.text)):
        if i['stacja'] in cities:
            rows.append ({
            'Miasto': i['stacja'],
            'Godzina pomiaru': i['godzina_pomiaru'],
            'Temperatura st. C': i['temperatura'],
            'Opady %':i['suma_opadu'],
            'Wiatr km/h': i['predkosc_wiatru']
            })
    return rows




    
