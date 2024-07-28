import json
#Carrega o numero preferido do usuário se foi armazenado anteriormente
#Caso contrario, pede para que o usuário forneça o numero e armazena essa informação

filename = 'numero.json'
try:
    with open(filename) as num:
        numero = json.load(num)
except FileNotFoundError:
    numero = input("Qual é seu numero favorito?")
    with open(filename, 'w') as num:
        json.dump(numero, num)
        print("Seu número favorito é , " +numero+ "!")
else:
    print("Bem vindo novamente, seu número é " + numero + "!")