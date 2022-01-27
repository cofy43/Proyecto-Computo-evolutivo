import math
import random
import numpy as np
from math import dist
from parser_vrp import Parser

"""
@author: Alex Fernandez y Martin Espinal
"""

class EA:
    
    def __init__(self, pc, pm, ul, li, ng, np, customers, vehicles, capacity, locations, center):
        """
        pc: Porcentaje de cuza
        pm: Porcentaje de mutacion
        ul: Límite inferior
        li: Límite superior
        ng: Número de generaciones
        np: Número de población
        parser: Parser con información del problema
        customers: Cantidad de consumidores
        vehicles: Cantidad me vehículos
        capacity: Capacidad máxima
        locations: Lista de tuplas donde la primer
                   entrada es la demanda, la segunda
                   entrada es la coordenada x y la tercer
                   entrada es la coordenada y.
        center: Punto de distribucion en el problema.
        """
        self.pc = pc
        self.pm = pm
        self.ul = ul
        self.li = li
        self.ng = ng
        self.np = np
        self.customers = customers-1
        self.vehicles = vehicles
        self.capacity = capacity
        self.locations = locations
        self.center = center

    def inicialitation(self):
        """
        Funcion que se encarga de asignar aleatoriamente 
        las locaciones a la los vehículos disponibles
        procurando no exceder la capacidad indicada
        """
        #Generamos una lista con dos entradas, la primera
        #representará la capacidad del vehículo e irá
        #actualizando según la locación aleatoriamente
        #seleccionada. La segunda entrada representará la
        #lista de locaciones para un vehículo
        routes = [[self.capacity, []] for _ in range(self.vehicles)]
        for i in range(self.customers):
            idx_vehicle = random.randint(0, self.vehicles-1)
            location = self.locations[i]
            diff = routes[idx_vehicle][0] - location[0]
            #Verificamos que la locación seleccionada para un
            #vehículo no exceda la capacidad máxima
            if diff >= 0:
                routes[idx_vehicle][1].append(location)
                routes[idx_vehicle][0] = diff
            else:
            #Si excede repetimos el experimento
                i -= 1
        return routes, routes, self.fitnes(routes)

    def euclidian_distance(self, p1, p2):
        """
        Función auxiliar que se encarga de calcular
        la distancia euclidiana de dos puntos con
        la ayuda de la paqueteria math
        """
        return dist(p1, p2)

    def fitnes(self, routes):
        """
        Funcion encargada de la evaluacion de la
        distancia recorrida por los vehiculos
        """
        apts = []
        for vehicle in routes:
            total = 0
            length = 0
            if len(vehicle) > 0: 
                length = len(vehicle[1])
            #Verificamos que los vehículos tengan
            #asignados al menos una ruta
            if length > 0 and vehicle[0] >= 0:
                #Distancia entre el origen y el primer
                #punto de distribucion de i-esimo vehiculo
                p1 = vehicle[1][0][1:]
                total += self.euclidian_distance(self.center, p1)
                for i in range(0, length-1, 2):                    
                    p1 = vehicle[1][i][1:]
                    p2 = vehicle[1][i+1][1:]
                    total += self.euclidian_distance(p1, p2)
                #Como recorremos la lista de puntos de distribucion
                #de los vehículos en pasos de dos podemos caer en 
                #caso de que dicha liste tenga una longitud impar y
                #esta condicion se encarga de cubrir ese caso para que
                #la suma de distacia sea correcta
                if length%2 != 0 and length > 1:
                    p1 = vehicle[1][length-2][1:]
                    p2 = vehicle[1][length-1][1:]
                    total += self.euclidian_distance(p1, p2)
                #Calculamos la distancia del último punto de distribución
                #al punto de origen
                p1 = vehicle[1][length-1][1:]
                total += self.euclidian_distance(p1, self.center)
            elif vehicle[0] < 0:
                total = -1
            apts.append(total)
        return apts

    def tournament_selection(self, aptitudes, npop):
        parents = []
        print()
        temp_aptitudes = aptitudes.copy()
        for _ in range(npop):
            c1 = np.random.randint(low=0, high=len(temp_aptitudes)) if len(temp_aptitudes)>0 else 0
            c2 = np.random.randint(0, len(temp_aptitudes)) if len(temp_aptitudes)>0 else 0
            p1 = temp_aptitudes[c1]
            p2 = temp_aptitudes[c2]
            if p1 > p2:
                parents.append(c1)
            else:
                parents.append(c2)
            temp_aptitudes.pop()
        return parents

    def crossover(self, idx, genotipos, pc):
        """
        Función encargada de realizar la cruza de un punto
        pero por la representación elegida (una lista de
        locaciones), la cruza se realizara de manera individual
        indx: Indices de los padres elegidos
        genotipos: Padres con la siguiente estructura.
                   La primer entrada es la capacidad máxima
                   disponible y la segunda es la lista con
                   las locaciones que recorrerá
        pc: Probabilidad de cruza
        """
        hijos_genitipo = []
        """
        for i in indx:
            flip = np.random.uniform() <= pc
            if flip and len(genotipos[i]) > 0:
                print("se hace cruza")
                individuo = genotipos[i]
                ruta = individuo[1]
                punto_cruza = 0
                nueva_ruta = []
                if len(ruta)-1 > 0:
                    punto_cruza = np.random.randint(0, len(ruta)-1)
                    nueva_ruta = [ruta[punto_cruza]] + ruta[0:punto_cruza] + ruta[punto_cruza+1:] + [ruta[punto_cruza+1]]
                nuevo_individuo = [individuo[0], nueva_ruta]
                hijos_genitipo.append(nuevo_individuo)
            else:
                hijos_genitipo.append(genotipos[i])
        """
        for i,j in zip(idx[::2], idx[1::2]):
            flip = np.random.uniform()<=pc
            if flip:
                punto_cruza = 0
                ruta1 = genotipos[i][1]
                ruta2 = genotipos[j][1]
                length1 = len(ruta1)
                length2 = len(ruta2)
                if length1 > length2:
                    punto_cruza = np.random.randint(0, length2) if length2 > 0 else 0
                elif length1 < length2:
                    punto_cruza = np.random.randint(0, length1) if length1 > 0 else 0
                else :
                    punto_cruza = np.random.randint(0, length2) if length2 > 0 else 0
                nueva_ruta1 = ruta1[0:punto_cruza] + ruta2[punto_cruza:]
                nueva_ruta2 = ruta2[0:punto_cruza] + ruta1[punto_cruza:]
                utilizado = 0
                for punto in nueva_ruta1:
                    utilizado += punto[0]
                nueva_capacidad1 = self.capacity - utilizado
                utilizado = 0
                for punto in nueva_ruta2:
                    utilizado += punto[0]
                nueva_capacidad2 = self.capacity - utilizado
                hijos_genitipo.append([nueva_capacidad1, nueva_ruta1])
                hijos_genitipo.append([nueva_capacidad2, nueva_ruta2])
            else :
                hijos_genitipo.append(genotipos[i])
                hijos_genitipo.append(genotipos[j])
        return hijos_genitipo

    def mutation(self, genotipos_hijos, pm):
        """
        genotipos_hijos: Resultados de la curza
        pm: Porcentaje de muta
        """
        hijos_genitipo = []
        for gen in genotipos_hijos:
            flip = np.random.uniform() <= pm
            if flip and len(gen[1]) > 0:
                ruta = gen[1]
                p1 = np.random.randint(0, len(ruta))
                p2 = np.random.randint(0, len(ruta))
                temp = ruta[p1]
                ruta[p1] = ruta[p2]
                ruta[p2] = temp
                hijos_genitipo.append([gen[0], ruta])
            else:
                hijos_genitipo.append(gen)
        return hijos_genitipo

    def estadisticas(self, generacion, genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes, padres):
        print('---------------------------------------------------------')
        print('Generación:', generacion)
        print('Población:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1,1), genotipos, fenotipos, aptitudes.reshape(-1, 1), aptitudes.reshape(-1, 1)/np.sum(aptitudes)), 1))
        print('Padres:', padres)
        print('frecuencia de padres:', np.bincount(padres))
        #print('Hijos:\n', np.concatenate((np.arange(len(aptitudes)).reshape(-1, 1), hijos_genotipo, hijos_fenotipo, hijos_aptitudes.reshape(-1, 1), hijos_aptitudes.reshape(-1, 1)/np.sum(hijos_aptitudes)), 1))
        print('Desempeño en línea para t=1: ', np.mean(aptitudes))
        print('Desempeño fuera de línea para t=1: ', np.max(aptitudes))
        print('Mejor individuo en la generación: ', np.argmax(aptitudes))

    def seleccion_mas(self, genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes):
        add_one = True if len(fenotipos)%2 !=0 else False
        mitad = int(len(fenotipos)/2)
        indices_mejores_padres = np.argpartition(aptitudes, -mitad)[-mitad:]
        if add_one:
            mitad+=1
        indices_mejores_hijos = np.argpartition(hijos_aptitudes, -mitad)[-mitad:]
        # nuevo_fenotipo = fenotipos[indices_mejores_padres] + hijos_fenotipo[indices_mejores_hijos]
        nuevo_fenotipo = []
        nuevo_aptitudes = []
        for i in indices_mejores_padres:
            nuevo_aptitudes.append(aptitudes[i])
            nuevo_fenotipo.append(fenotipos[i])

        for i in indices_mejores_hijos:
            nuevo_aptitudes.append(hijos_aptitudes[i])
            nuevo_fenotipo.append(hijos_fenotipo[i])
        nuevo_genotipo = nuevo_fenotipo
        return nuevo_fenotipo, nuevo_genotipo, nuevo_aptitudes


    def EA(self):
        """
        Ejecución del algoritmo evolutivo
        """
        genotipos, fenotipos, aptitudes = self.inicialitation()
        #minima = np.copy(genotipos[np.argmin(aptitudes)])
        #media = np.median(aptitudes)
        #maximo = np.copy(genotipos[np.argmax(aptitudes)])
        #desviacion = np.std(aptitudes)
        #ba = np.zeros((self.ng, 1))
        print(len(aptitudes))
        for i in range(self.ng):
            #Seleccion de padres
            indx = self.tournament_selection(aptitudes, self.np)
            #Cruza
            hijos_genotipo = self.crossover(indx,genotipos,self.pc)
            #Mutación
            hijos_genotipo = self.mutation(hijos_genotipo, self.pm)
            hijos_fenotipo = hijos_genotipo
            hijos_aptitudes = self.fitnes(hijos_genotipo)
            self.estadisticas(i, genotipos, fenotipos, np.array(aptitudes), np.array(hijos_genotipo), np.array(hijos_fenotipo), np.array(hijos_aptitudes), indx)
            #Seleccion de la siguiente generación
            genotipos, fenotipos, aptitudes = self.seleccion_mas(genotipos, fenotipos, aptitudes, hijos_genotipo, hijos_fenotipo, hijos_aptitudes)
        return genotipos, aptitudes



if __name__ == "__main__":
    path = "vrp_5_4_1"
    #path = "vrp_484_19_1"
    parser = Parser(path)
    customers, vehicles, capacity, locations, center = parser.get_data()
    ea = EA(0.5,0.4,0.5,10000,customers,vehicles, customers, vehicles, capacity, locations, center)
    rutas,distancias =  ea.EA()
    print()
    print("Output Format")
    print(sum(distancias), '0')
    for vehiculo in rutas:
        print(rutas)