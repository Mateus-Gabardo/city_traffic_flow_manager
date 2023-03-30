import os 
import sys
import traci
import time

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "D:/Documents/Programas/sumo-1.16.0/bin/sumo"
sumoCmd = [sumoBinary, "-c", "instancias\config.sumocfg"]

def main():
    try:
        traci.start(sumoCmd)
    except traci.TraCIException:
        print("Erro ao conectar ao servidor TraCI, tentando novamente em 10 segundos...")
        time.sleep(10)
        main()

    # Faz uma simulação até que todos os veículos cheguem
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
    traci.close()
    print('finalizou')

main()