import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo
import random
from itertools import permutations 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class Simulador():

    def __init__(
        self,
        tamanho_matriz,                 #numero de linhas e colunas da matriz esférica
        percentual_inicial_tipo1,       #percentual inicial da população que será infectada tipo 1
        percentual_inicial_tipo2,       #percentual inicial da população que será infectada tipo 2
        chance_infeccao,                #chance que um infectado tipo 2 tem de infectar um indivíduo saudável
        chance_infeccao_tipo2,          #chance de um indivíduo infectado se tornar contagioso
        chance_morte,                   #chance de um indivíduo tipo 2 morrer ao fim de uma atualização
        atualizacoes_cura):             #número de atualizações necessárias para a cura de um indivíduo tipo 1 ou 2

        self.num_atualizacoes = 0       
        self.individuos_infectados_tipo_2 = []
        self.individuos_infectados_tipo_1 = []
        self.individuos_infectados_curados = []
        self.individuos_infectados_mortos = []
        self.matriz_individuos = np.zeros([tamanho_matriz,tamanho_matriz])
        
        self.fabrica_individuo = Fabrica_individuo(
                                                chance_infeccao,
                                                chance_infeccao_tipo2, 
                                                chance_morte, 
                                                atualizacoes_cura)
            
        #objeto que é responsável por validar a movimentação no grid n x n    
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)
        
        self.populacao_inicial = int(tamanho_matriz**2)
        self.num_inicial_tipo2 = int(self.populacao_inicial * percentual_inicial_tipo2)
        self.num_inicial_tipo1 = int(self.populacao_inicial * percentual_inicial_tipo1)
        self.num_inicial_sadios = self.populacao_inicial - (self.num_inicial_tipo2 + self.num_inicial_tipo1)
        self.popular(tamanho_matriz)
        dict = {
                'num_sadios':self.num_inicial_sadios,
                'num_infect_t1':self.num_inicial_tipo1,
                'num_infect_t2':self.num_inicial_tipo2,
                'num_curados':0,
                'num_mortos':0,
                'matriz_posicionamento':self.matriz_individuos.flatten()}

        #dataframe que guardará os resultados de cada atualização  
        self.dataframe = pd.DataFrame(dict, index = [0])
        


    def popular(self, tamanho_matriz):
        #lista de possíveis combinações de índices da matriz de dados
        permutacoes = permutations(list(range(tamanho_matriz)),2)
        #conversão para lista de tuplas(x,y)
        lista_indices = list(permutacoes)
        #embaralhamento dos índices
        random.shuffle(lista_indices)

        #cria o primeiro tipo1:
        ind_x = lista_indices.pop()[0]
        ind_y = lista_indices.pop()[1]
        indiv = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
        self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
        self.individuos_infectados_tipo_1.append(indiv)
        
        #cria o restante dos tipos 1
        for i in range(1,self.num_inicial_tipo1):
            ind_x = lista_indices.pop()[0]
            ind_y = lista_indices.pop()[1]
            indiv = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
            self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
            self.individuos_infectados_tipo_1.append(indiv)

        #cria o restante dos tipo 2:
        for indice in range(self.num_inicial_tipo2):
            ind_x = lista_indices.pop()[0]
            ind_y = lista_indices.pop()[1]
            indiv = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_2,(ind_x,ind_y))
            self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_2
            self.individuos_infectados_tipo_2.append(indiv)

          
                                            

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


