import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo
import random
from itertools import permutations 

class Simulador():

    def __init__(
        self,
        tamanho_matriz,                 #numero de linhas e colunas da matriz esférica
        densidade_populacional_inicial, #percentual de ocupação inicial da matriz
        percentual_inicial_tipo1,       #percentual inicial da população que será infectada tipo 1
        percentual_inicial_tipo2,       #percentual inicial da população que será infectada tipo 2
        chance_infeccao,                #chance que um infectado tipo 2 tem de infectar um indivíduo saudável
        chance_infeccao_tipo2,          #chance de um indivíduo infectado se tornar contagioso
        chance_morte,                   #chance de um indivíduo tipo 2 morrer ao fim de uma atualização
        atualizacoes_cura):             #número de atualizações necessárias para a cura de um indivíduo tipo 1 ou 2

        self.num_atualizacoes = 0       
        self.indices_infectados_tipo_2 = []
        self.indices_infectados_tipo_1 = []
        self.matriz_individuos = np.zeros([tamanho_matriz,tamanho_matriz])
        
        self.fabrica_individuo = Fabrica_individuo(
                                                chance_infeccao,
                                                chance_infeccao_tipo2, 
                                                chance_morte, 
                                                atualizacoes_cura)
            
        #objeto que é responsável por validar a movimentação no grid n x n    
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)
        
        self.populacao_inicial = int(densidade_populacional_inicial * tamanho_matriz**2)
        self.num_inicial_tipo2 = int(self.populacao_inicial * percentual_inicial_tipo2)
        self.num_inicial_tipo1 = int(self.populacao_inicial * percentual_inicial_tipo1)
        self.num_inicial_sadios = self.populacao_inicial - (self.num_inicial_tipo2 + self.num_inicial_tipo1)

        dict = {
                'num_sadios':self.num_inicial_sadios,
                'num_infect_t1':self.num_inicial_tipo1,
                'num_infect_t2':self.num_inicial_tipo2,
                'num_curados':0,
                'num_mortos':0}

        #dataframe que guardará os resultados de cada atualização  
        self.dataframe = pd.DataFrame(dict, index = [0])
        self.popular(tamanho_matriz)


    def popular(self, tamanho_matriz):
        #lista de possíveis combinações de índices da matriz de dados
        permutacoes = permutations(list(range(tamanho_matriz)),2)

        lista_indices = list(permutacoes)

        random.shuffle(lista_indices)

        #cria o primeiro tipo2:
        self.indices_infectados_tipo_2.append(lista_indices[0])
        self.matriz_individuos[lista_indices[0][0], lista_indices[0][1]] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_2)
        #cria o restante dos tipo 2:
        for indice in lista_indices[1:self.num_inicial_tipo2-2]:
            print(indice)
        #cria os tipo1:


        #cria a população saudável:

        for i in lista_indices[0:]: 
            print(i)  


        
                
                                            

class Fabrica_individuo():
    
    def __init__(
        self,
        chance_infeccao,                #chance que um infectado tipo 2 tem de infectar um indivíduo saudável
        chance_infeccao_tipo2,          #chance de um indivíduo infectado se tornar contagioso
        chance_morte,                   #chance de um indivíduo tipo 2 morrer ao fim de uma atualização
        atualizacoes_cura):             #número de atualizações necessárias para a cura de um indivíduo tipo 1 ou 2
        
        self.chance_infeccao = chance_infeccao
        self.chance_infeccao_tipo2 = chance_infeccao_tipo2
        self.chance_morte = chance_morte
        self.atualizacoes_cura = atualizacoes_cura
        
    def criar_individuo(self, status_inicial, posicao):
        
        return Individuo(
            status_inicial, 
            self.chance_infeccao, 
            self.chance_infeccao_tipo2, 
            self.chance_morte, 
            self.atualizacoes_cura,
            posicao)





chance_infeccao = 0.3             
chance_infeccao_tipo2 = 0.2       
chance_morte = 0.2                
atualizacoes_cura = 10           
percentual_inicial_tipo1 = 0.05    
percentual_inicial_tipo2 = 0.01





sim = Simulador(
    1000, 
    1, 
    percentual_inicial_tipo1, 
    percentual_inicial_tipo2, 
    chance_infeccao,
    chance_infeccao_tipo2,
    chance_morte,atualizacoes_cura)


ind = sim.fabrica_individuo.criar_individuo(Individuo.MORTO, (0,0))





dict = {'num_sadios':1,
                'num_infect_t1':2,
                'num_infect_t2':3,
                'num_curados':4,
                'num_mortos':5}
s = pd.Series(dict)                
sim.dataframe = sim.dataframe.append(s, ignore_index=True)

print(sim.dataframe)
#print(sim.num_inicial_tipo2)





