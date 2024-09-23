import maps_text_search as maps

focus = "nada"
pais = input("¿Where do you want to go?")
estado = input()
municipio = input()
focus = int(input("What do you want to see?\n1)nature\n2)Culture\n3)History\n4)Gastronomic\n5)Bucket friendly\n6)Entretainment"))
weekday = input("Que dia de la semana planeas ir?(l,m,i,j,v,s,d)")
maps.get_atractions(pais,estado,municipio,focus,weekday)