import json
import networkx as nx
import itertools
from operator import itemgetter
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def grafo_usuarios_relacionados(usuarios_comunidades):#utf-8
    meetups = {}#meetup e usuarios

    for usuario_meetups in usuarios_comunidades:
        usuario = usuario_meetups['usuario']
        meetups_usuario = usuario_meetups['meetups']

        for meetup in meetups_usuario:

            if meetups.get(meetup):
                temp = meetups.get(meetup)
                temp.append(usuario)
                meetups[meetup] = temp
            else:
                meetups[meetup] = [usuario]

    G = nx.Graph()

    for meetup, usuarios in meetups.items():

        permutacoes = itertools.permutations(usuarios, 2)

        for aresta in permutacoes:
            no_anterior = aresta[0]
            no_sucessor = aresta[1]

            if G.get_edge_data(no_anterior,no_sucessor, default=0) == 0:#adicionar label
                G.add_edge(no_anterior, no_sucessor, weight=1)
            else:
                G[no_anterior][no_sucessor]['weight'] = G[no_anterior][no_sucessor]['weight'] + 1

    exibe_arestas_peso(G)
    nx.write_gml(G, "resultados/grafos/grafo_usuarios_relacionadas.gml")

def grafo_comunidades_relacionadas(usuarios_comunidades):#utf-8
    G = nx.Graph()

    for usuario_meetups in usuarios_comunidades:
        meetups = usuario_meetups['meetups']
        permutacoes = itertools.permutations(meetups, 2)

        for aresta in permutacoes:
            no_anterior = aresta[0]
            no_sucessor = aresta[1]

            if G.get_edge_data(no_anterior,no_sucessor, default=0) == 0:#adicionar label
                G.add_edge(no_anterior, no_sucessor, weight=1)
            else:
                G[no_anterior][no_sucessor]['weight'] = G[no_anterior][no_sucessor]['weight'] + 1

    exibe_arestas_peso(G)
    nx.write_gml(G, "resultados/grafos/grafo_comunidades_relacionadas.gml")

def grafo_topicos(membros):
    G = nx.Graph()
    for membro in membros:
        topicos = []

        for topico in membro['topics']:
            topicos.append(topico['name'])
        permutacoes = itertools.permutations(topicos, 2)
        #G.add_edges_from([aresta for aresta in permutacoes])#adiciona sem pesos

        for aresta in permutacoes:
            no_anterior = aresta[0]
            no_sucessor = aresta[1]

            if G.get_edge_data(no_anterior,no_sucessor, default=0) == 0:#adicionar label
                G.add_edge(no_anterior, no_sucessor, weight=1)
            else:
                G[no_anterior][no_sucessor]['weight'] = G[no_anterior][no_sucessor]['weight'] + 1

    #print G.edges(data=True)
    nx.write_gml(G, "resultados/grafos/grafo_topicos_gdg.gml")

def exibe_arestas_peso(G):
    arestas = sorted(G.edges(data=True), key=itemgetter(2), reverse=True)
    for aresta in arestas:
        print aresta

def main():
    dados = [json.loads(linha) for linha in open("dados/membros_meetups.json")]#Google Developers Group - Belo Horizonte_members_meetups_technology
    grafo_usuarios_relacionados(dados)

if __name__ == "__main__":
    main()
