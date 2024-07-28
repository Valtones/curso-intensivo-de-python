import json

def numero_armazenado():
    """Obtém o numero do usuário já armazenado se estiver disponível"""
    filename = 'numero.json'
    try:
        with open(filename) as num:
            numero = json.load(num)
    except FileNotFoundError:
        return None
    else:
        return numero
def numero_novo():
    """Pede um novo numero""" 
    numero = input("Qual seu número favorito?")
    filename = 'numero.json'
    with open(filename, 'w') as num:
        json.dump(numero,num)
    return numero

def boas_vindas():
    """Saúda o usuário pelo nome"""
    numero = numero_armazenado()
    if numero:
        print("Bem vindo novamente, seu número é " + numero+ "!")
    else:
        numero = numero_novo()
        print("Seu número "+numero +" ficará guardado!") 
boas_vindas()  