import requests
#from api_chave import chave
import json
import sys
"""
Coleta de todos os grupos: "/find/groups"
Parametros: {"location": "Belo Horizonte", "category": 34, "order": "most_active"}#a categoria eh Tech (id obtido da consulta de categorias)

Coleta dos membros: "/2/members"
Parametros: {"group_id": id_grupo, "page": 500}
"""

def coleta(request_uri, parametros, total_membros):
    dados = []
    paginas = (total_membros/200) + 1

    for pagina in range(0, paginas):
        print pagina
        try:
            url = "https://api.meetup.com" + request_uri + "?key=" + chave
            parametros['offset'] = pagina
            resposta = requests.get(url, params=parametros)
            dados.append(resposta.json()['results'])
        except:
            print "Deu ruim :( ", sys.exc_info()[0]
    return dados

def grava_arquivo(dados, nome_arquivo):
    arquivo = open(nome_arquivo, "w")
    for lista in dados:
        for meetup in lista:
            arquivo.write(json.dumps(meetup) + "\n")
    arquivo.close()

def separa_grupos(arquivo):
    grupos = {}#separa grupos unicos para coleta-los

    for linha in open(arquivo):
        meetup = json.loads(linha)
        if not grupos.get(meetup['id']):
            grupos[meetup['id']] = [meetup['name'].encode('utf-8'), meetup['members']]

    return grupos

def main():
    grupos = separa_grupos("dados/meetups_technology.json")

    for id_grupo, infos_grupo in grupos.items():
        parametros = {"group_id": id_grupo, "page": 500, "status": "past"}
        dados = coleta("/2/events", parametros, infos_grupo[1])
        print infos_grupo[0]#nome do grupo e tamanho dos dados
        grava_arquivo(dados, "dados/eventos/" + infos_grupo[0] + "_events_meetups_technology.json")

if __name__ == "__main__":
    main()
