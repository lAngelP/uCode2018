import json
import requests


url1="http://data.nba.net/10s/prod/v1/calendar.json"
url2_1="http://data.nba.net/10s/prod/v2/"
url2_2="/scoreboard.json"


def buscarFechas():
    resp= requests.get(url=url1)
    Fechas= resp.json()
    del Fechas['_internal']
    del Fechas['startDate']
    del Fechas['endDate']
    del Fechas['startDateCurrentSeason']
    Numeros = list(filter(lambda fecha: int(fecha) > 20180309 and Fechas[fecha] > 0, Fechas))
    Numeros.sort(key=lambda x: int(x))
    return Numeros

def sacarDatos(Fechas):
    for i in Fechas:
        datos= requests.get(url= url2_1 + i + url2_2)
        Partidos= datos.json()
        Emparejamientos = []
        for games in Partidos['games']:
            Emparejamientos.append({
                'Arena_name': games['arena']['name'],
                'City_name': games['arena']['city'],
                'Date': games['startDateEastern'],
                'Home_team': games['vTeam']['triCode'],
                'Away_team': games['hTeam']['triCode']


            })

        return(Emparejamientos)


if __name__=='__main__':
    Datos= buscarFechas()
    sacarDatos(Datos)
