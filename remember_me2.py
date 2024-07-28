import json
#Carrega o nome do usuário se foi armazenado anteriormente
#Caso contrario, pede para que o usuário forneça o nome e armazena essa informação

filename = 'username.json'
try:
    with open(filename) as f_obj:
        username = json.load(f_obj)
except FileNotFoundError:
    username = input("Whats is your name?")
    with open(filename, 'w') as f_obj:
        json.dump(username, f_obj)
        print("We'll remember you when you come back, " +username+ "!")
else:
    print("Welcome back, " + username + "!")