import pandas as pd
import numpy as np
import Matriz_esferica as me
class Simulador():

    def __init__(self, tamanho_matriz,):
        self.num_iteracoes = 0
        self.dataframe = pd.DataFrame()
        self.matriz_esferica = me.Matriz_esferica(tamanho_matriz)



    pass


sim = Simulador(10)