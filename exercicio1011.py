import json

numero = input("Qual é o seu número favorito?")
filename = 'numero.json'
with open(filename, 'w') as num:
    json.dump(numero, num)
    print("Eu sei qual é o seu número favorito! É " +numero+ "!")