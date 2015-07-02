import json
from operator import itemgetter

def ranking(dados):#ordenado pelo numero de membros
    dados_ordenados = sorted(dados, key=itemgetter('members'), reverse=True)

    for meetup in dados_ordenados:
        print meetup['name'], meetup['members']

def main():
    dados = [json.loads(linha) for linha in open("meetups_technology.json")]
    ranking(dados)

if __name__ == "__main__":
    main()
