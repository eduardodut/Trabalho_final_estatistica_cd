import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo
import random

class Simulador():

    def __init__(
        self,
        tamanho_matriz,                 #numero de linhas e colunas da matriz esférica
        
        densidade_populacional_inicial): #percentual de ocupação inicial da matriz
       
        
        
        
        self.num_iteracoes = 0

        self.indices_infectados_tipo_2 = []
        self.indices_infectados_tipo_1 = []
        

        self.matriz_individuos = []
        self.fabrica_individuo = []
        self.num_max_individuos = tamanho_matriz^2
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)
        
        
        
        self.dataframe = pd.DataFrame(columns= ['num_sadios', 'num_infect_t1', 'num_infect_t2', 'num_curados', 'num_mortos'])
        
    pass

    def condicoes_iniciais(
        chance_infeccao,                #chance que um infectado tipo 2 tem de infectar um indivíduo saudável
        chance_infeccao_tipo2,          #chance de um indivíduo infectado se tornar contagioso
        chance_morte,                   #chance de um indivíduo tipo 2 morrer ao fim de uma atualização
        atualizacoes_cura,              #número de atualizações necessárias para a cura de um indivíduo tipo 1 ou 2
        percentual_inicial_tipo1,       #percentual inicial da população que será infectada tipo 1
        percentual_inicial_tipo2):      #percentual inicial da população que será infectada tipo 2
        self.fabrica_individuo = Fabrica_individuo(
                                                chance_infeccao,
                                                chance_infeccao_tipo2, 
                                                chance_morte, 
                                                atualizacoes_cura, 
                                                percentual_inicial_tipo1, 
                                                percentual_inicial_tipo2 )

class Fabrica_individuo():
    
    def __init__(
        chance_infeccao,                #chance que um infectado tipo 2 tem de infectar um indivíduo saudável
        chance_infeccao_tipo2,          #chance de um indivíduo infectado se tornar contagioso
        chance_morte,                   #chance de um indivíduo tipo 2 morrer ao fim de uma atualização
        atualizacoes_cura,              #número de atualizações necessárias para a cura de um indivíduo tipo 1 ou 2
        percentual_inicial_tipo1,       #percentual inicial da população que será infectada tipo 1
        percentual_inicial_tipo2):      #percentual inicial da população que será infectada tipo 2

        self.chance_infeccao = chance_infeccao
        self.chance_infeccao_tipo2 = chance_infeccao_tipo2
        self.chance_morte = chance_morte
        self.atualizacoes_cura = atualizacoes_cura
        self.percentual_inicial_tipo1 = percentual_inicial_tipo1 + percentual_inicial_tipo2
        self.percentual_inicial_tipo2 = percentual_inicial_tipo2

    def criar_individuo():

        rng_status_inicial = random.random()
        status_inicial = Individuo.SADIO        
        if rng_status_inicial <= percentual_inicial_tipo2:
            status_inicial = Individuo.INFECTADO_TIPO_2
        elif rng_status_inicial <= percentual_inicial_tipo1:
            status_inicial = Individuo.INFECTADO_TIPO_1
        
        return Individuo(
            status_inicial, 
            self.chance_infeccao, 
            self.chance_infeccao_tipo2, 
            self.chance_morte, 
            self.atualizacoes_cura)


sim = Simulador(2)

print(sim.matriz_individuos)