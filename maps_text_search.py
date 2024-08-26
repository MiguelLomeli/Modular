import pandas as pd
from google_apis import create_service

client_secret_file = 'client_secret.json'
API_NAME = 'places'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

service = create_service(client_secret_file, API_NAME, API_VERSION, SCOPES)
def get_atractions(place,focus):
    query = "top attractions in " + place
    #CASO DE QUERER VER NATURALEZA
    if focus == 1:
        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "historical_landmark" #Solo puede ser un solo tipo, hasta ahora para naturaleza yo digo que park y historical_landmark
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list = response['places']
        except:
            places_list = []

        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "park"
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
            places_list = response['places']
        except:
            places_list = []

        request_body = {
            "textQuery": query,
            "regionCode": 'MX',
            "includedType" : "museum"
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
            "includedType" : "performing_arts_theater"
        }
        response = service.places().searchText(
            body = request_body,
            fields = "places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri"
        ).execute()
        try:
            places_list += response['places']
        except:
            pass

    #CASO DE QUERER UN VIAJE BARATO
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

    df = pd.DataFrame(places_list)
    df.to_csv("places_results.csv", index = False)