# -*- coding: utf-8 -*-
import json
import os
from operator import itemgetter

def topicos_relacionados(arquivo):
    topicos = {}

    for linha in open(arquivo):
        membro = json.loads(linha)
        for topico in membro['topics']:
            if topicos.get(topico['name']):
                topicos[topico['name']] = topicos.get(topico['name']) + 1
            else:
                topicos[topico['name']] = 1

    topicos_ordenados = sorted(topicos.iteritems(), key=itemgetter(1), reverse=True)
    return topicos_ordenados

def ranking(dados):#ordenado pelo numero de membros
    dados_ordenados = sorted(dados, key=itemgetter('members'), reverse=True)
    print "### Ranking dos Meetups por número de membros\n"

    for meetup in dados_ordenados:
        print "* ", meetup['name'].encode("utf-8"), " - ", meetup['members'], " membros"

def ranking_topicos_meetups(diretorio_grupos):#"dados/grupos/"
    for root, diretorio, arquivos in os.walk(diretorio_grupos, topdown=False):
        for arquivo in arquivos:
            print "\n### ",arquivo[:arquivo.find("_")], "\n"
            topicos = topicos_relacionados(os.path.join(root, arquivo))

            total = sum([topico[1] for topico in topicos])
            top_topicos = 10 if len(topicos) > 9 else len(topicos)

            for topico in range(0, top_topicos):#5 topicos mais populares
                print "* ", topicos[topico][0].encode("utf-8"), round(float((topicos[topico][1] * 100))/total, 2), "%"

def ranking_topicos_meetup(arquivo_grupo):#"dados/grupos/Google Developers Group - Belo Horizonte_members_meetups_technology.json"
    topicos = topicos_relacionados(arquivo_grupo)
    total = sum([topico[1] for topico in topicos])

    for topico in topicos:
        print "* ", topico[0].encode("utf-8"), round(float((topico[1] * 100))/total, 2), "%"

def main():
    dados = [json.loads(linha) for linha in open("dados/meetups_technology.json")]
    ranking(dados)

if __name__ == "__main__":
    main()
