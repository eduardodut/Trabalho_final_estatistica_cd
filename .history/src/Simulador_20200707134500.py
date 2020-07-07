import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo


class Simulador():

    def __init__(
        self,
        tamanho_matriz,             #numero de linhas e colunas da matriz esférica
        chance_infeccao,            #chance que um infectado tipo 2 tem de infectar um indivíduo saudável
        chance_infeccao_tipo2,      #chance de um indivíduo infectado se tornar contagioso
        chance_morte,               #chance de um indivíduo tipo 2 morrer ao fim de uma atualização
        atualizacoes_cura,          #número de atualizações necessárias para a cura de um indivíduo tipo 1 ou 2
        percentual_inicial_tipo1,   #percentual inicial da população que será infectada tipo 1
        percentual_inicial_tipo2):  #percentual inicial da população que será infectada tipo 2
        
        
        
        self.num_iteracoes = 0

        self.indices_infectados_tipo_2 = []
        self.indices_infectados_tipo_1 = []
        

        self.matriz_individuos = []
        self.num_max_individuos = tamanho_matriz^2
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)

        self.dataframe = pd.DataFrame(columns= ['num_sadios', 'num_infect_t1', 'num_infect_t2', 'num_curados', 'num_mortos'])


    pass




sim = Simulador(2)

print(sim.matriz_individuos)