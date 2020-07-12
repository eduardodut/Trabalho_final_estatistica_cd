import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo, Fabrica_individuo
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
        self.lista_matrizes_posicionamento = []
        #self.matriz_individuos = np.zeros([tamanho_matriz,tamanho_matriz])
        
        self.fabrica_individuo = Fabrica_individuo(
                                                chance_infeccao,
                                                chance_infeccao_tipo2, 
                                                chance_morte, 
                                                atualizacoes_cura)

        self.matriz_individuos = pd.DataFrame(columns=range(tamanho_matriz), index=range(tamanho_matriz))
        self.matriz_individuos.loc[:] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(0,0))
        
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
                'num_mortos':0}
            

        #dataframe que guardará os resultados de cada atualização  
        self.dataframe = pd.DataFrame(dict, index = [0])
        #self.salvar_posicionamento()

    def salvar_posicionamento(self):
        self.lista_matrizes_posicionamento.append(self.matriz_individuos.apply(self.get_status_individuo))
    
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
        self.matriz_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
        #self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
        self.individuos_infectados_tipo_1.append((ind_x,ind_y))
        
        #cria o restante dos tipos 1
        for i in range(1,self.num_inicial_tipo1):
            ind_x = lista_indices.pop()[0]
            ind_y = lista_indices.pop()[1]
            self.matriz_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
            #self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
            self.individuos_infectados_tipo_1.append((ind_x,ind_y))

        #cria o restante dos tipo 2:
        for indice in range(self.num_inicial_tipo2):
            ind_x = lista_indices.pop()[0]
            ind_y = lista_indices.pop()[1]
            self.matriz_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_2,(ind_x,ind_y))
            #self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
            self.individuos_infectados_tipo_2.append((ind_x,ind_y))
    
    
    
    def get_status_individuo(self, individuo: Individuo):
        return individuo.status

    def mover_infectado(self, individuo: Individuo):
        pos_x, pos_y = individuo.posicao[0], individuo.posicao[1]
        pass

                                            


chance_infeccao = 0.3             
chance_infeccao_tipo2 = 0.2       
chance_morte = 0.2                
atualizacoes_cura = 10           
percentual_inicial_tipo1 = 0.01   
percentual_inicial_tipo2 = 0.00


sim = Simulador(
    10,
    percentual_inicial_tipo1, 
    percentual_inicial_tipo2, 
    chance_infeccao,
    chance_infeccao_tipo2,
    chance_morte,atualizacoes_cura)

#print(sim.lista_matrizes_posicionamento[0])
print(sim.individuos_infectados_tipo_2)
print(sim.individuos_infectados_tipo_1)
#cmap = ListedColormap(['w', 'y', 'yellow', 'red'])
#plt.matshow(sim.matriz_individuos, cmap = cmap);plt.show();
def get_status_individuo( individuo: Individuo):
    return individuo.status



dataframe_individuos = sim.matriz_individuos[:,:].apply(get_status_individuo)
