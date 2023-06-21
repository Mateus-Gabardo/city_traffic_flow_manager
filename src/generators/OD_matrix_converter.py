class ODMatrixConverter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert_OD_matrix(self, scala = 1):
        with open(self.input_file, 'r') as file:
            lines = file.read().splitlines()
        
        data = []
        for line in lines:
            line = line.strip().replace(" ", "")
            if line and not line.startswith("<"):
                data.append(line)

        with open(self.output_file, 'w') as file:
            file.write('<routes>\n')
            file.write('    <interval  begin="0" end="3600">\n')
            origin = 0
            id = 0
            for line in data:
                if line.startswith("Origin"):
                    origin = line.split("\t")[1]
                else:
                   destinies = line.split(";")
                   destinies = [dest.rstrip() for dest in destinies if dest.rstrip()]
                   for destiny in destinies:
                        flows = destiny.split(":")
                        dest_id = flows[0]
                        flow = float(flows[1]) / scala
                        flow = round(flow)
                        if flow != 0.0:
                            file.write(f'      <flow id="{id}" from="{origin}" to="{dest_id}"/>\n')

            file.write('    </interval>\n')
            file.write('</routes>')
