


def initialSolution(data):
    return

# Algoritmo de busca local simples.
# Interacoes - criterio de parada
# estrategia - define o tipo de retorno: 
#   1- retorna a melhor melhoria entre todos os vizinhos
#   2 -retorna o primeiro vizinho melhor
def localSearch(data, interacoes = 50, estrategia = 2):
    # Retorna uma solução inicial de maneira aletório que será permutada durante a busca local 
    best_network, best_temp = initialSolution(data)

    qtd_iteracoes = interacoes
    
    while int(qtd_iteracoes) > 0 :
        network_curent, min_cmax  = escolheMelhorVizinho(best_seq, data, nb_jobs, nb_machines, estrategia)        
        if(min_cmax < best_temp):
            best_temp = min_cmax
            best_network = network_curent
        qtd_iteracoes = qtd_iteracoes - 1

    return best_network, best_temp