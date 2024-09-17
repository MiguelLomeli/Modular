# algortimos.py
from math import sqrt

def distancia_euclidiana(x_1:float, y_1:float, x_2:float, y_2:float):
    distancia = sqrt((x_2-x_1)**2 + (y_2-y_1)**2)
    return distancia
    #return distancia


def puntos_mas_cercanos(puntos_list)->list:
    resultado = []
    for punto_i in puntos_list:
        x1 = punto_i["x"]
        y1 = punto_i["y"]
        min = 1000
        cercano = (0,0)
        for punto_j in puntos_list:
            if punto_i != punto_j:
                x2 = punto_j["x"]
                y2 = punto_j["y"]
                d = distancia_euclidiana(x1,y1,x2,y2)
                if d<min:
                    min = d
                    cercano = (x2,y2)

        resultado.append((punto_i, cercano))
    return resultado