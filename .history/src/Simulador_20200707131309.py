import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo
class Simulador():

    def __init__(self, tamanho_matriz,):
        self.num_iteracoes = 0
        self.matriz_individuos = np.asmatrix(tamanho_matriz)
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)

        self.dataframe = pd.DataFrame(columns= [''])


    pass


sim = Simulador(2)

print(sim.matriz_individuos)