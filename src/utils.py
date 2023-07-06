import random
import math

def nova_lane(arestas, modifications, json_mod, current_modification, budget):
    
    # escolha aleatoriamente uma das arestas
    aresta = random.choice(list(arestas.keys()))

    # verifique se essa aresta já foi modificada anteriormente
    while aresta in modifications:
        aresta = random.choice(list(arestas.keys()))
    
    if not aresta:
        isBudget = False
    else:
        isBudget = True   
        # Verificar se está dento do budget
        distancia = json_mod["arestas"][aresta]["length"]
        if distancia <= budget:
            budget -= distancia

            # adicionar mais uma lane à aresta escolhida
            arestas[aresta]["numLanes"] += 1
            json_mod['arestas'] = arestas

            # adicionar a aresta escolhida na lista de modificações e diminuir do budget
            current_modification.append(aresta)

    return json_mod, current_modification, budget, isBudget

def nova_aresta(vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget):
    tamanho_inicial = len(current_modification)
    while tamanho_inicial == len(current_modification):
        
        # escolher aleatoriamente uma possível nova aresta
        vertice = random.choice(list(vertices))
        arestas_possiveis = ret_nova_arestas(vertice, arestas, arestas_criadas, coordenadas)
        isBudget = True

        if len(arestas_possiveis) > 0:
            isok = False
            while not isok:

                new_edge_name_aux = random.choice(arestas_possiveis)
                new_edge_name = new_edge_name_aux.split(';')[0]

                # Verificar se está dento do budget
                distancia = 1
                #json_mod["arestas"][new_edge_name]["length"]
                if distancia <= budget:
                    budget -= distancia
                    isok = True
                    new_edge = {
                        "lenght": new_edge_name_aux.split(';')[1],
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
            isBudget = False


    return json_mod, current_modification, arestas_criadas, budget, isBudget

def ret_nova_arestas(verticeOrigem, arestas, arestas_criadas, coordenadas):
    arestas_encontradas = []
    arestas_possiveis = []
    for aresta in arestas.keys():
        if aresta.split('-')[0] == verticeOrigem:
            arestas_encontradas.append(aresta)

    for aresta_encotrada in arestas_encontradas:
        for aresta in arestas.keys():
            if aresta_encotrada.split('-')[1] == aresta.split('-')[0] and aresta_encotrada.split('-')[0] != aresta.split('-')[1]:
                is_Not_Reta, new_lenght = calcular_reta(arestas.keys(), aresta_encotrada.split('-')[0], aresta.split('-')[1], aresta.split('-')[0], coordenadas, arestas_criadas, arestas)
                if is_Not_Reta == False:
                    if aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1] not in arestas_possiveis:
                        arestas_possiveis.append(aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1]+';'+str(new_lenght))

    for aresta_possivel in arestas_possiveis:
        if aresta_possivel.split(';')[0] in arestas_criadas:
            arestas_possiveis.remove(aresta_possivel)
    
    return arestas_possiveis

def calcular_reta(arestas, vertice1, vertice2, vertice3, coordenadas, arestas_criadasa, arestas_completas):
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
    if ponto1[0] == ponto2[0] == x3 or ponto1[1] == ponto2[1] == y3:
        return True, 0
    else:
        if abs(y3 - (m * x3 + b)) < 1e-10:  # Usamos a função abs() para evitar problemas com coordenadas negativas
            return True, 0

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
                    return True, 0
    
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
                    return True, 0

    #Calcula nova lenght
    lenght1 = ret_length(vertice1,vertice3, arestas_completas)
    lenght2 = ret_length(vertice3, vertice2, arestas_completas)
    new_lenght = math.sqrt(lenght1 ** 2 + lenght2 ** 2)
    return False, new_lenght

def ret_coordenadas(vertice, coordenadas):
    for coordenada in coordenadas.keys():
        if vertice == coordenada:
            x = float(coordenadas[coordenada]["x"])
            y = float(coordenadas[coordenada]["y"])

    retorno = []
    retorno.append(x)
    retorno.append(y)
    return retorno

def ret_length(vertice1, vertice2, arestas):
    new_aresta = f"{vertice1}-{vertice2}"
    aresta_info = arestas.get(new_aresta)
    if aresta_info:
        return aresta_info.get("length", 0)
    return 0