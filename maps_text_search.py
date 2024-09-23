import pandas as pd
from google_apis import create_service
import TripAdvisor_API
from pso.pso_main import *
from algoritmos import distancia_euclidiana
import operator

client_secret_file = 'client_secret.json'
API_NAME = 'places'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

service = create_service(client_secret_file, API_NAME, API_VERSION, SCOPES)

weekdays = {'l':0,
            'm':1,
            'i':2,
            'j':3,
            'v':4,
            's':5,
            'd':6,}

times = {'national_park' : 12,
         'park' : 3,
         'art_gallery' : 3,
         'performing_arts_theater' : 4,
         'church' : 2,
         'historical_landmark' : 2,
         'museum' : 4,
         'tourist_attraction' : 2,
         'cultural_center' : 2,
         'zoo' : 6,
         'aquarium' : 4,
         'amusement_park' : 6
}

def get_atractions(pais, estado, municipio, focus,weekday):
    places_list = []
    query = f"top attractions in {municipio}, {estado}, {pais}"

    # Define the focus types mapping
    focus_dict = {
        1: ["national_park", "park","aquarium","zoo"],  # Naturaleza
        2: ["art_gallery", "performing_arts_theater", "church", "museum", "cultural_center"],  # Cultura
        3: ["historical_landmark", "museum", "tourist_attraction"],  # Historia
        4: [],  # Gastronomía (special handling)
        5: [],   # Viaje económico (special handling)
        6: ["amusement_park","aquarium","zoo"]
    }

    if focus in focus_dict:
        included_types = focus_dict[focus]
        
        if focus == 4:  # Gastronomía
            query = f"Mejores lugares para comer comida tipica en {municipio}, {estado}, {pais}"
            request_body = {
                "textQuery": query,
                "regionCode": 'MX',
            }
            response = service.places().searchText(
                body=request_body,
                fields="places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri,places.reviews,places.location"
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
                fields="places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri,places.reviews,places.location"
            ).execute()
            try:
                places_list += response['places']
            except:
                pass

        else:  # Otros focus
            for included_type in included_types:
                request_body = {
                    "textQuery": query,
                    "regionCode": 'MX',
                    "includedType": included_type
                }
                response = service.places().searchText(
                    body=request_body,
                    fields="places.id,places.displayName.text,places.types,places.rating,places.shortFormattedAddress,places.googleMapsUri,places.websiteUri,places.reviews,places.location"
                ).execute()
                try:
                    places_list += response['places']
                except:
                    pass

    places_list = complete_list(places_list)
    graph = prepare_graph(places_list,weekdays[weekday])
    orden = run_pso(graph)
    places_list = reorden(places_list,orden)
    df = pd.DataFrame(places_list)
    df.to_csv("places_results.csv", index=False)

def complete_list(places_list):
    new_places_list = []
    for place in places_list:
        place["hours"],place["ranking"] = TripAdvisor_API.busqueda(place["displayName"]["text"])
        place["displayName"] = place["displayName"]["text"]
        place["reviews"] = place.get("reviews", [{}])[0].get("text", {}).get("text", "No reviews")
        place["latitude"] = place["location"]["latitude"]
        place["longitude"] = place["location"]["longitude"]
        place["time"] = 0
        for type in place["types"]:
            try:
                if times[type] > place["time"]:
                    place["time"] = times[type]
            except:
                pass
        if place not in new_places_list:
            new_places_list.append(place)
    return new_places_list

def prepare_graph(places_list,weekday):
    nodos = []
    posible_nodes = []
    sorted_places = sorted(places_list, key=lambda place: place["ranking"])
    time_spend = 0

    place1 = sorted_places[0]
    coordenada1 = dict()
    coordenada1["x"] = (float(place1["location"]["latitude"]) + 180)*1000
    coordenada1["y"] = (float(place1["location"]["longitude"]) + 180)*1000
    coordenada1["name"] = place1["displayName"]
    coordenada1["open_time"] = int(place1["hours"][weekday][-13]+place1["hours"][weekday][-12]+place1["hours"][weekday][-10]+place1["hours"][weekday][-9])
    nodos.append(coordenada1)
    sorted_places.remove(place1)

    for place in sorted_places:
        try:
            if place["hours"][weekday][-6]!="C" and time_spend < 12:
                coordenada = dict()
                coordenada["x"] = (float(place["location"]["latitude"]) + 180)*1000
                coordenada["y"] = (float(place["location"]["longitude"]) + 180)*1000
                coordenada["name"] = place["displayName"]
                coordenada["open_time"] = int(place["hours"][weekday][-13]+place["hours"][weekday][-12]+place["hours"][weekday][-10]+place["hours"][weekday][-9])
                if coordenada["open_time"] < nodos[0]["open_time"]:
                    nodos.insert(0,coordenada)
                else:
                    nodos.append(coordenada)
                time_spend = time_spend+place["time"]
        except:
            coordenada = dict()
            coordenada["x"] = (float(place["location"]["latitude"]) + 180)*1000
            coordenada["y"] = (float(place["location"]["longitude"]) + 180)*1000
            coordenada["name"] = place["displayName"]
            coordenada["open_time"] = 25
            posible_nodes.append(coordenada)

        print(nodos)
            

    amount = len(nodos)
    print(amount)
    graph = Graph(amount_vertices=amount, starting_vertex=nodos[0]["name"])
    for i in range(amount):
        for j in range(i+1,amount):
            origen = dict()
            destino = dict()
            origen["x"] = nodos[i]["x"]
            origen["y"] = nodos[i]["y"]
            destino["x"] = nodos[j]["x"]
            destino["y"] = nodos[j]["y"]
            distancia = distancia_euclidiana(origen["x"],origen["y"], destino["x"], destino["y"])

            graph.add_edge(nodos[i]["name"], nodos[j]["name"],distancia)

    return graph


def run_pso(graph):
    pso = PSO(graph, iterations=100, size_population=30, beta=2, alpha=2)
    pso.run()
    evolutions = pso.evolutions
    return evolutions[99]

def reorden(places_list,orden):
    sorted_places_list = []
    for i in orden:
        for place in places_list:
            if place["displayName"] == i:
                sorted_places_list.append(place)
    
    return sorted_places_list

