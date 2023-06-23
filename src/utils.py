import random
import math

def nova_lane(arestas, modifications, json_mod, current_modification, budget):
    
    # escolha aleatoriamente uma das arestas
    aresta = random.choice(list(arestas.keys()))

    # verifique se essa aresta já foi modificada anteriormente
    while aresta in modifications:
        aresta = random.choice(list(arestas.keys()))
    
    # Verificar se está dento do budget
    distancia = json_mod["arestas"][aresta]["length"]
    if distancia <= budget:
        budget -= distancia

        # adicionar mais uma lane à aresta escolhida
        arestas[aresta]["numLanes"] += 1
        json_mod['arestas'] = arestas

        # adicionar a aresta escolhida na lista de modificações e diminuir do budget
        current_modification.append(aresta)

    return json_mod, current_modification, budget

def nova_aresta(vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget):
    tamanho_inicial = len(current_modification)
    while tamanho_inicial == len(current_modification):
        
        # escolher aleatoriamente uma possível nova aresta
        vertice = random.choice(list(vertices))
        arestas_possiveis = ret_nova_arestas(vertice, arestas, arestas_criadas, coordenadas)

        if len(arestas_possiveis) > 0:
            isok = False
            while not isok:
                new_edge_name = random.choice(arestas_possiveis)

                # Verificar se está dento do budget
                distancia = 1
                #json_mod["arestas"][new_edge_name]["length"]
                if distancia <= budget:
                    budget -= distancia
                    isok = True
                    new_edge = {
                        "lenght": 20,
                        "maxSpeed": random.randint(30, 70),
                        "numLanes": 1,
                        "priority": random.randint(80, 100)
                    }
                    arestas[new_edge_name] = new_edge
                    json_mod['arestas'] = arestas
                    arestas_criadas.append(new_edge_name)
                    current_modification.append(new_edge_name)
                    isok = True
                else:
                    arestas_possiveis.remove(new_edge_name)
                    if not arestas_possiveis:
                        isok = True
        else:
            tamanho_inicial += 1


    return json_mod, current_modification, arestas_criadas, budget

def ret_nova_arestas(verticeOrigem, arestas, arestas_criadas, coordenadas):
    arestas_encontradas = []
    arestas_possiveis = []
    for aresta in arestas.keys():
        if aresta.split('-')[0] == verticeOrigem:
            arestas_encontradas.append(aresta)

    for aresta_encotrada in arestas_encontradas:
        for aresta in arestas.keys():
            if aresta_encotrada.split('-')[1] == aresta.split('-')[0] and aresta_encotrada.split('-')[0] != aresta.split('-')[1]:
                if calcular_reta(arestas.keys(), aresta_encotrada.split('-')[0], aresta.split('-')[1], aresta.split('-')[0], coordenadas, arestas_criadas) == False:
                    if aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1] not in arestas_possiveis:
                        arestas_possiveis.append(aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1])

    for aresta_possivel in arestas_possiveis:
        if aresta_possivel in arestas_criadas:
            arestas_possiveis.remove(aresta_possivel)
    
    return arestas_possiveis

def calcular_reta(arestas, vertice1, vertice2, vertice3, coordenadas, arestas_criadasa):
    # Verifica se o ponto 3 está na reta entre o ponto 1 e o ponto 2
    ponto1 = ret_coordenadas(vertice1, coordenadas)
    ponto2 = ret_coordenadas(vertice2, coordenadas)
    ponto3 = ret_coordenadas(vertice3, coordenadas)
    
    if ponto2[0] - ponto1[0] != 0:
        m = (ponto2[1] - ponto1[1]) / (ponto2[0] - ponto1[0])
        b = ponto1[1] - m * ponto1[0]
    else:
        # Caso a reta seja vertical, não há coeficiente angular e b é simplesmente o valor de x do ponto.
        m = float('inf')
        b = ponto1[0]

    # Verifica se o ponto 3 está na reta
    x3, y3 = ponto3
    # if x3 == ponto2[0] or y3 == ponto2[1]:
    #     return True
    # el
    if ponto1[0] == ponto2[0] == x3 or ponto1[1] == ponto2[1] == y3:
        return True
    else:
        if abs(y3 - (m * x3 + b)) < 1e-10:  # Usamos a função abs() para evitar problemas com coordenadas negativas
            return True

    # Verifica se a reta do ponto 1 ao ponto 2 cruza com qualquer reta que tenha o ponto 3
    # Verifica arestas iniciais
    for aresta in arestas:
        vertice_a, vertice_b = aresta.split('-')
        if vertice_a == vertice3 or vertice_b == vertice3:
            ponto_a = ret_coordenadas(vertice_a, coordenadas)
            ponto_b = ret_coordenadas(vertice_b, coordenadas)

            x1, y1 = ponto1
            x2, y2 = ponto2
            x3, y3 = ponto_a
            x4, y4 = ponto_b
    
            # Calcula o ponto de interseção usando a fórmula de interseção de retas
            denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
            
            if denom != 0:
                ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
                ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

                # Verifica se o ponto de interseção está dentro dos limites das retas
                if 0 < ua < 1 and 0 < ub < 1:
                    return True
    
    # Verifica arestas criadas
    for aresta in arestas_criadasa:
        vertice_a, vertice_b = aresta.split('-')
        if vertice_a == vertice3 or vertice_b == vertice3:
            ponto_a = ret_coordenadas(vertice_a, coordenadas)
            ponto_b = ret_coordenadas(vertice_b, coordenadas)

            x1, y1 = ponto1
            x2, y2 = ponto2
            x3, y3 = ponto_a
            x4, y4 = ponto_b
    
            # Calcula o ponto de interseção usando a fórmula de interseção de retas
            denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
            
            if denom != 0:
                ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
                ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

                # Verifica se o ponto de interseção está dentro dos limites das retas
                if 0 < ua < 1 and 0 < ub < 1:
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