import subprocess

class SumoXmlDemandGenerator:
    def __init__(self, net_file, rou_file, num_vehicles, probability, seed):
        self.net_file = net_file
        self.rou_file = rou_file
        self.num_vehicles = num_vehicles
        self.probability = probability
        self.seed = seed
    
    def generateDemand(self):
        command = ["python", "src/generators/randomTrips.py", "-n", self.net_file, "-r", self.rou_file, "-e", str(self.num_vehicles), "-p", str(self.probability), "-s", str(self.seed)]
        subprocess.call(command)
