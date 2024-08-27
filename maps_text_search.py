import pandas as pd
from google_apis import create_service
import TripAdvisor_API

client_secret_file = 'client_secret.json'
API_NAME = 'places'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

service = create_service(client_secret_file, API_NAME, API_VERSION, SCOPES)
def get_atractions(place,focus):
    places_list = []
    query = "top attractions in " + place
    #CASO DE QUERER VER NATURALEZA
    if focus == 1:
        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "national_park" 
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "park" #Parque
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

    #CASO DE QUERER VER CULTURA
    elif focus == 2:
        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "art_gallery" #Galerias de arte
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "performing_arts_theater" #Teatro
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "church" #Iglesia
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

    #CASO DE QUERER VER HISTORICO
    elif focus == 3:
        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "historical_landmark" 
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "museum" #Museo
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "tourist_attraction" #En este tipo generalmente entran edificios
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass
    
    #CASO DE QUERER COMER BUENA COMIDA
    elif focus == 4:
        request_body = {
            "textQuery": "Mejores lugares para comer en "+ place,
            "regionCode": 'MX',
            #"includedType" : "banquet_hall" 
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

    #CASO DE QUERER UN VIAJE BARATO                   // Nota personal: no funciona así
    elif focus == 5:
        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "priceLevels": ["PRICE_LEVEL_MODERATE"]
        }

        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        places_list = response['places']

    places_list = complete_list(places_list)
    df = pd.DataFrame(places_list)
    df.to_csv("places_results.csv", index = False)

def complete_list(places_list):
    new_places_list = []
    for place in places_list:
        place["hours"] = TripAdvisor_API.busqueda(place["displayName"]["text"])
        if place not in new_places_list:
            new_places_list.append(place)
    return places_list
