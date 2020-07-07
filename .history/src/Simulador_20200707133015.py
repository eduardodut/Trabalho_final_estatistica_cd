import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo


class Simulador():

    def __init__(self, tamanho_matriz):
        self.num_iteracoes = 0

        self.vector_infectados_tipo_2 = []
        self.vector_infectados_tipo_1 = []

        self.matriz_individuos = []
        self.num_max_individuos = tamanho_matriz^2
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)

        self.dataframe = pd.DataFrame(columns= ['num_sadios', 'num_infect_t1', 'num_infect_t2', 'num_curados', 'num_mortos'])


    pass


sim = Simulador(2)

print(sim.matriz_individuos)