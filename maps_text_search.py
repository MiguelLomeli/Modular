import pandas as pd
from google_apis import create_service
import TripAdvisor_API

client_secret_file = 'client_secret.json'
API_NAME = 'places'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

service = create_service(client_secret_file, API_NAME, API_VERSION, SCOPES)

def get_atractions(pais, estado, municipio, focus):
    places_list = []
    query = f"top attractions in {municipio}, {estado}, {pais}"

    # Define the focus types mapping
    focus_dict = {
        1: ["national_park", "park"],  # Naturaleza
        2: ["art_gallery", "performing_arts_theater", "church"],  # Cultura
        3: ["historical_landmark", "museum", "tourist_attraction"],  # Historia
        4: [],  # Gastronomía (special handling)
        5: []   # Viaje económico (special handling)
    }

    if focus in focus_dict:
        included_types = focus_dict[focus]
        
        if focus == 4:  # Gastronomía
            query = f"Mejores lugares para comer en {municipio}, {estado}, {pais}"
            request_body = {
                "textQuery": query,
                "regionCode": 'MX',
            }
            response = service.places().searchText(
                body=request_body,
                fields="places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri,places.reviews"
            ).execute()
            try:
                places_list += response['places']
            except:
                pass

        elif focus == 5:  # Viaje económico
            request_body = {
                "textQuery": query,
                "regionCode": 'MX',
                "priceLevels": ["PRICE_LEVEL_MODERATE"]
            }
            response = service.places().searchText(
                body=request_body,
                fields="places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri,places.reviews"
            ).execute()
            try:
                places_list += response['places']
            except:
                pass

        else:  # Otros focos
            for included_type in included_types:
                request_body = {
                    "textQuery": query,
                    "regionCode": 'MX',
                    "includedType": included_type
                }
                response = service.places().searchText(
                    body=request_body,
                    fields="places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri,places.reviews"
                ).execute()
                try:
                    places_list += response['places']
                except:
                    pass

    places_list = complete_list(places_list)
    df = pd.DataFrame(places_list)
    df.to_csv("places_results.csv", index=False)

def complete_list(places_list):
    new_places_list = []
    for place in places_list:
        place["hours"] = TripAdvisor_API.busqueda(place["displayName"]["text"])
        place["displayName"] = place["displayName"]["text"]
        place["reviews"] = place.get("reviews", [{}])[0].get("text", {}).get("text", "No reviews")
        if place not in new_places_list:
            new_places_list.append(place)
    return new_places_list
