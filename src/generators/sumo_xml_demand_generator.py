import subprocess
import shutil
import os

class SumoXmlDemandGenerator:
    def __init__(self, net_file, rou_file):
        self.net_file = net_file
        self.rou_file = rou_file
        sumo_path = shutil.which('sumo')
        self.sumo_dir = os.path.dirname(sumo_path)
        self.duarouter_path = os.path.join(self.sumo_dir, "duarouter")
    
    def generateDemand(self, num_vehicles, probability, seed):
        command = ["python", "src/generators/randomTrips.py", "-n", self.net_file, "-r", self.rou_file, "-e", str(num_vehicles), "-p", str(probability), "-s", str(seed)]
        subprocess.call(command)

    def generateDemandByTaz(self, taz_file):
        command = [self.duarouter_path, "-n", self.net_file, "-r", taz_file, "-o", self.rou_file]
        subprocess.call(command)