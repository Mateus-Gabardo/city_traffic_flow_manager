import random
import math

def nova_lane(arestas, modifications, json_mod, current_modification, budget):
    budget_number = budget
    
    # escolha aleatoriamente uma das arestas
    aresta = random.choice(list(arestas.keys()))

    # verifique se essa aresta já foi modificada anteriormente
    while aresta in modifications:
        aresta = random.choice(list(arestas.keys()))
    
    # Verificar se está dento do budget
    vertice1 = arestas[aresta].split("-")[0]
    vertice2 = arestas[aresta].split("-")[1]
    distancia = retorna_distancia(json_mod, vertice1, vertice2)
    if budget_number <= distancia:
        budget_number -= distancia

            # adicionar mais uma lane à aresta escolhida
        arestas[aresta]["numLanes"] += 1
        json_mod['arestas'] = arestas

        # adicionar a aresta escolhida na lista de modificações e diminuir do budget
        current_modification.append(aresta)

    return json_mod, current_modification, budget_number

def nova_aresta(vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget):
    budget_number = budget
    tamanho_inicial = len(current_modification)
    while tamanho_inicial == len(current_modification):
        # escolha aleatoriamente uma possível nova aresta
        vertice = random.choice(list(vertices))

        arestas_possiveis = ret_nova_arestas(vertice, arestas, arestas_criadas, coordenadas)

        if len(arestas_possiveis) > 0:
            isok = False
            while(not isok):
                new_edge_name = random.choice(arestas_possiveis)
                    # Verificar se está dento do budget
                vertice1 = json_mod['arestas'][new_edge_name].split("-")[0]
                vertice2 = json_mod['arestas'][new_edge_name].split("-")[1]
                distancia = retorna_distancia(json_mod, vertice1, vertice2)
                if budget_number <= distancia:
                    budget_number -= distancia
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
                else:
                    arestas_possiveis.remove(new_edge_name)
                    if len(arestas_possiveis) == 0:
                        isok = True

    return json_mod, current_modification, budget_number

def ret_nova_arestas(verticeOrigem, arestas, arestas_criadas, coordenadas):
    arestas_encontradas = []
    arestas_possiveis = []
    for aresta in arestas.keys():
        if aresta.split('-')[0] == verticeOrigem:
            arestas_encontradas.append(aresta)

    for aresta_encotrada in arestas_encontradas:
        for aresta in arestas.keys():
            if aresta_encotrada.split('-')[1] == aresta.split('-')[0] and aresta_encotrada.split('-')[0] != aresta.split('-')[1]:
                if calcular_reta(arestas.keys(), aresta_encotrada.split('-')[0], aresta.split('-')[1], aresta.split('-')[0], coordenadas) == False:
                    if aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1] not in arestas_possiveis:
                        arestas_possiveis.append(aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1])

    for aresta_possivel in arestas_possiveis:
        if aresta_possivel in arestas_criadas:
            arestas_possiveis.remove(aresta_possivel)
    
    return arestas_possiveis

def calcular_reta(arestas, vertice1, vertice2, vertice3, coordenadas):
    
    isNotPossivel = False
    ponto1 = ret_coordenadas(vertice1, coordenadas)
    ponto2 = ret_coordenadas(vertice2, coordenadas)
    ponto3 = ret_coordenadas(vertice3, coordenadas)

    # Calcula a equação da reta y = mx + b, onde m é o coeficiente angular e b é o coeficiente linear.
    if ponto2[0] - ponto1[0] != 0:
        m = (ponto2[1] - ponto1[1]) / (ponto2[0] - ponto1[0])
        b = ponto1[1] - m * ponto1[0]
    else:
        # Caso a reta seja vertical, não há coeficiente angular e b é simplesmente o valor de x do ponto.
        m = float('inf')
        b = ponto1[0]

    # Verifica se o ponto 3 está na reta
    x3, y3 = ponto3
    if ponto1[0] == ponto2[0] == x3 or ponto1[1] == ponto2[1] == y3:
        isNotPossivel = True
    else:
        if abs(y3 - (m * x3 + b)) < 1e-10:  # Usamos a função abs() para evitar problemas com coordenadas negativas
            isNotPossivel = True

    # Calcular as retas do ponto 2 para ver ser cruza com a nova reta:
    for aresta in arestas:
        vertice_a, vertice_b = aresta.split('-')
        if vertice_a == vertice3 or vertice_b == vertice3:
            ponto_a = ret_coordenadas(vertice_a, coordenadas)
            ponto_b = ret_coordenadas(vertice_b, coordenadas)

            if ponto_a[0] - ponto_b[0] != 0:
                m_aresta = (ponto_a[1] - ponto_b[1]) / (ponto_a[0] - ponto_b[0])
                b_aresta = ponto_a[1] - m_aresta * ponto_a[0]
            else:
                m_aresta = float('inf')
                b_aresta = ponto_a[0]

            if m != m_aresta:
                x_intersecao = (b_aresta - b) / (m - m_aresta)
                y_intersecao = m * x_intersecao + b

                if min(ponto_a[0], ponto_b[0]) <= x_intersecao <= max(ponto_a[0], ponto_b[0]) and \
                min(ponto_a[1], ponto_b[1]) <= y_intersecao <= max(ponto_a[1], ponto_b[1]):
                    isNotPossivel = True
                    break

    return isNotPossivel

def ret_coordenadas(vertice, coordenadas):
    for coordenada in coordenadas.keys():
        if vertice == coordenada:
            x = float(coordenadas[coordenada]["x"])
            y = float(coordenadas[coordenada]["y"])

    retorno = []
    retorno.append(x)
    retorno.append(y)
    return retorno

def retorna_distancia(json_mod, vertice1, vertice2):
    
    vertice1x = json_mod["coordenadas"][vertice1]["x"]
    vertice1y = json_mod["coordenadas"][vertice1]["y"]

    vertice2x = json_mod["coordenadas"][vertice2]["x"]
    vertice2y = json_mod["coordenadas"][vertice2]["y"]

    distancia = math.sqrt((vertice2x - vertice1x)**2 + (vertice2y - vertice1y)**2)

    return distancia