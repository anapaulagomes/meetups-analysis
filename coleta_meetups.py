import requests
from api_chave import chave
import json

url = "https://api.meetup.com/find/groups?key="+ chave
parametros = {"location": "Belo Horizonte", "category": 34, "order": "most_active"}#a categoria eh Tech (id obtido da consulta de categorias)
resposta = requests.get(url, params=parametros)

dados = resposta.json()
arquivo = open("meetups_technology.json", "w")
for meetup in dados:
    arquivo.write(json.dumps(meetup) + "\n")
arquivo.close()
