# -*- coding: utf-8 -*-
import json
import os
import sys
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

def separa_usuarios(diretorio_grupos):
    usuarios = {}#nome e meetups

    for root, diretorio, arquivos in os.walk(diretorio_grupos, topdown=False):
        for arquivo in arquivos:
            meetup = arquivo[:arquivo.find("_")]

            try:
                dados = [json.loads(linha) for linha in open(os.path.join(root, arquivo))]
                for usuario in dados:
                    #print meetup, usuario['name']
                    if usuarios.get(usuario['name']):
                        temp = usuarios.get(usuario['name'])
                        temp.append(meetup)
                        usuarios[usuario['name']] = temp
                    else:
                        usuarios[usuario['name']] = [meetup]
            except:
                print "Deu ruim :(", sys.exc_info()
    arquivo = open("dados/membros_meetups.json", "w")
    for usuario, meetups in usuarios.items():
        arquivo.write(json.dumps({"usuario": usuario.encode('utf-8'), "meetups": meetups})+"\n")
    arquivo.close()

def main():
    separa_usuarios("dados/grupos/")

if __name__ == "__main__":
    main()
