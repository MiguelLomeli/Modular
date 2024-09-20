import requests
import TripAdvisor_Credentials

def actualizar_numero_usos():
    with open("uso_trip_advisor.txt", 'r+') as f:
        numero = f.read()
        f.seek(0)
        f.truncate()
        nuevo = int(numero)+1
        f.write(str(nuevo))
    f.close()

def verificar_numero_usos():
    f = open("uso_trip_advisor.txt")
    numero = f.read()
    if int(numero)>=4900:
        return False
    elif int(numero)>4000:
        print("ALERT: Few free uses left")
        return True
    else:
        return True

def details(id):
    url = "https://api.content.tripadvisor.com/api/v1/location/"+id+"/details?language=es&currency=USD&key="+TripAdvisor_Credentials.get_key()

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    actualizar_numero_usos()

    API_Data = response.json() 

    try:
        return(API_Data["hours"]["weekday_text"],int(API_Data["ranking_data"]["ranking"]))
    except:
        return("",1000)
    

def busqueda(text_search):
    if verificar_numero_usos():

        url = "https://api.content.tripadvisor.com/api/v1/location/search?searchQuery="+text_search+"&language=en&key="+TripAdvisor_Credentials.get_key()

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        actualizar_numero_usos()

        API_Data = response.json() 

        hours , rank = details(API_Data["data"][0]["location_id"])
            
        return (hours, rank)
        