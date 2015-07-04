import json
import networkx as nx
import itertools
from operator import itemgetter
import sys

reload(sys)
sys.setdefaultencoding('Cp1252')

def grafo_comunidades_relacionadas(usuarios_comunidades):
    G = nx.Graph()

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
    dados = [json.loads(linha) for linha in open("dados/grupos/Ionic BH_members_meetups_technology.json")]#Google Developers Group - Belo Horizonte_members_meetups_technology
    #grafo_topicos(dados)

if __name__ == "__main__":
    main()
