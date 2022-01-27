class Parser:
    """
    Clase auxiliar para poder parsear los archivos de 
    prueba
    """
    def __init__(self, path):
        self.customers = 0
        self.vehicles = 0
        self.capacity = 0
        self.locations = []
        self.center = []
        self.parser_file(path)

    def parser_file(self,path):
        file = open(path, "r")
        first_line = False
        second_line = False
        for line in file:
            if not(first_line):
                first_line = True
                temp_customers, temp_vehicle, temp_capacity = line.split(' ')
                self.customers = int(temp_customers)
                self.vehicles = int(temp_vehicle)
                self.capacity = int(temp_capacity)
            elif not(second_line):
                second_line = True
                self.center = self.parser_location(line)[1:]
            elif line != "":
                location = self.parser_location(line)
                self.locations.append(location)

    def parser_location(self, line):
        data = line.replace("\n", "").split(' ')
        location = [int(data[0]), float(data[1]), float(data[2])]
        return location


    def get_data(self):
        return self.customers, self.vehicles, self.capacity, self.locations, self.center