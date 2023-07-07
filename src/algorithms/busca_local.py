import src.utils as util
import json
import random
import copy
from src.sumo_simulation import SumoSimulation

# Realiza a criação de uma matriz de adjacencia a partir dog rafo existente
def criar_matriz_adjacencia(grafo):
    vertices = grafo["vertices"]
    
    num_vertices = len(vertices)
    matriz_adj = [[None] * num_vertices for _ in range(num_vertices)]
    atributos = {}
    arestas_possiveis = {}
    for id_aresta, dados in grafo["arestas"].items():
        vertice_origem, vertice_destino = map(int, id_aresta.split("-"))
        matriz_adj[vertice_origem-1][vertice_destino-1] = id_aresta

    for i in range(num_vertices):
        arestas_possiveis.update(avalia_criacao_aresta(str(i+1), grafo["arestas"], grafo["coordenadas"]))
        for j in range(num_vertices):
            id_aresta = matriz_adj[i][j]

            if id_aresta is not None:
                propriedade_atualizada = grafo["arestas"][id_aresta]
                propriedade_atualizada['numLanes'] += 1
                atributos[id_aresta] = ['A', propriedade_atualizada]
            else:
                new_id_aresta = f"{i}-{j}"
                new_length  = arestas_possiveis.get(new_id_aresta)
                if new_length  is not None:
                    new_length = round(float(new_length), 2)
                    atributos[new_id_aresta] = ['C', {"length": new_length,"maxSpeed": 50,"numLanes": 1,"priority": 100}]

    return matriz_adj, atributos

# Retorna todas as arestas possíveis criacões de arestas a partir de um vértice
def avalia_criacao_aresta(verticeOrigem, arestas, coordenadas):
    arestas_possiveis = util.ret_nova_arestas(verticeOrigem, arestas, [], coordenadas)
    map_arestas_possiveis = {}

    for valor in arestas_possiveis:
        id, lenght = valor.split(';')
        map_arestas_possiveis[id] = lenght
    return map_arestas_possiveis

# Verifique a possibilidade da nova aresta criada ser incluida no grafo, uma vez que ela precisa respeitar algumas restriçoes
def permite_inserir_aresta(aresta, coordenadas, arestas_completas):
    vertice1, vertice2 = aresta.split('-')
    ponto1 = ret_coordenadas(vertice1, coordenadas)
    ponto2 = ret_coordenadas(vertice2, coordenadas)

    for aresta_completa in arestas_completas:
        vertice_a, vertice_b = aresta_completa.split('-')
        ponto_a = ret_coordenadas(vertice_a, coordenadas)
        ponto_b = ret_coordenadas(vertice_b, coordenadas)

        if intersecao_segmentos(ponto1, ponto2, ponto_a, ponto_b):
            return False

    return True


def intersecao_segmentos(ponto1, ponto2, ponto3, ponto4):
    x1, y1 = ponto1
    x2, y2 = ponto2
    x3, y3 = ponto3
    x4, y4 = ponto4

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return False
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return True
    return False

def ret_coordenadas(vertice, coordenadas):
    for coordenada in coordenadas.keys():
        if vertice == coordenada:
            x = float(coordenadas[coordenada]["x"])
            y = float(coordenadas[coordenada]["y"])

    retorno = []
    retorno.append(x)
    retorno.append(y)
    return retorno

import random

def reduzir_budget(solucao_inicial, atributos, budget_total):
    budget_restante = budget_total
    conjuntos_removidos = []
    total_peso_solucao = sum(atributos[conjunto][1]['length'] for conjunto in solucao_inicial)
    valor_a_reduzir = total_peso_solucao * 0.5

    solucao_embaralhada = random.sample(solucao_inicial, len(solucao_inicial))

    for conjunto in solucao_embaralhada:
        chave_conjunto = conjunto
        peso_conjunto = atributos[chave_conjunto][1]['length']

        if peso_conjunto <= valor_a_reduzir:
            budget_restante -= peso_conjunto
            valor_a_reduzir -= peso_conjunto
            conjuntos_removidos.append(conjunto)

        if valor_a_reduzir <= 0:
            break

    solucao_final = [conjunto for conjunto in solucao_inicial if conjunto not in conjuntos_removidos]
    return solucao_final, budget_restante


def avalia_melhoria(solucao, atributos, network, demanda):
    novo_tempo = float("inf")
    novo_network = copy.deepcopy(network)

    # Inserimos a solucao no grafo
    for id_aresta in solucao:
        nova_propriedade = atributos[id_aresta]
        if nova_propriedade[0] == 'C':
           if permite_inserir_aresta(id_aresta, novo_network['coordenadas'], novo_network['arestas'].keys()):
               novo_network['arestas'][id_aresta] = nova_propriedade[1]
        else:
            novo_network['arestas'][id_aresta] = nova_propriedade[1]

    # Executamos a simulacao com o novo grafo.
    simulador = SumoSimulation(novo_network, demanda)
    novo_tempo = simulador.run_simulation()
    return novo_tempo, novo_network

# solucao_atual = S = [1-6, 2-4]
# Network - corresponde ao grafo da instancia
def gerar_vizinhos(solucao_atual, network, budget_restante, matriz_adj, atributos, vertice_inicial, estrategia, demanda):
    melhor_solucao = solucao_atual
    menor_tempo = float("inf")
    melhor_network = copy.deepcopy(network)
    
    def buscar(solucao_atual, budget_restante):
        nonlocal melhor_solucao, menor_tempo, melhor_network
        
        if budget_restante < 0:
            return
        
        if solucao_atual:
            novo_tempo, novo_network = avalia_melhoria(solucao_atual, atributos, network, demanda)
            
            if novo_tempo < menor_tempo:
                menor_tempo = novo_tempo
                melhor_solucao = solucao_atual
                melhor_network = novo_network

                if estrategia == 2:
                    return
        
        for i in range(len(matriz_adj)):
            vertice_adjacente = matriz_adj[vertice_inicial][i]
            if vertice_adjacente is not None and vertice_adjacente in atributos:
                node = atributos[vertice_adjacente]
                if i != vertice_inicial and node[1]['length'] <= budget_restante:
                    nova_solucao = solucao_atual + [vertice_adjacente]
                    novo_budget = budget_restante - node[1]['length']
                    buscar(nova_solucao, novo_budget)

                    if estrategia == 2 and menor_tempo < float("inf"):
                        return
    
    buscar(solucao_atual, budget_restante)
    return melhor_solucao, melhor_network, menor_tempo

def buscar_solucao_inicial(grafo, budget, demanda, atributos):
    solucao = []
    melhor_network = grafo
    melhor_tempo = 0
    
    atributos_lista = list(atributos.keys())
    
    while budget > 0 and atributos_lista:
        indice_sorteado = random.choice(atributos_lista)
        atributo_sorteado = atributos[indice_sorteado]
        
        if budget >= atributo_sorteado[1]['length']:
            solucao.append(indice_sorteado)
            budget -= atributo_sorteado[1]['length']
        
        atributos_lista.remove(indice_sorteado)

    melhor_tempo, melhor_network = avalia_melhoria(solucao, atributos, grafo, demanda)
    return solucao, melhor_network, melhor_tempo

# Algoritmo de busca local aplicado ao Network Design Problem
#
# A solucão será representada da seguinte maneira:
#
# S = [1-6, 2-4] 
# 
# no qual, se referem do grafo que sofreram algum tipo de modificacao.
# As informaçoes mais espepecíficas sobre a modificação em estarao em hashMap que possui todas as modificacoes possiveis do grafo passado
# onde o indice será a propria aresta.
# O exemplo desses atributos será da segunte maneira: 
# 
# {1-6: ['A', {'length': 20, 'maxSpeed': 80, 'numLanes': 1, 'priority': 100}]}
def busca_local(grafo, budget, interacoes=10, estrategia=1, vehicles = 50):
    matriz_adj, atributos = criar_matriz_adjacencia(grafo)
    melhor_solucao, melhor_network, melhor_tempo = buscar_solucao_inicial(grafo, budget, vehicles, atributos)
    qtd_iteracoes = interacoes
    vertice_inicial = 0

    while int(qtd_iteracoes) > 0:
        #Aplicamos a perturbação na solução atual
        solucao_reduzida, budget_restante = reduzir_budget(melhor_solucao, atributos, budget)

        # Buscamos os vizinhos
        nova_solucao, novo_network, novo_tempo = gerar_vizinhos(solucao_reduzida, grafo, budget_restante, matriz_adj, atributos, vertice_inicial, estrategia, vehicles)
        if novo_tempo < melhor_tempo:
            melhor_tempo = novo_tempo
            melhor_network = novo_network
            melhor_solucao = nova_solucao
        qtd_iteracoes = qtd_iteracoes - 1

    return melhor_network, melhor_solucao, melhor_tempo

def run():
    with open('src/data/siouxFalls/siouxFalls.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)

    busca_local(data, 10)

run()