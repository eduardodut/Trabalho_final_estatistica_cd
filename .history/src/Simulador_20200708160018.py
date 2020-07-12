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
        self.individuos_curados = []
        self.individuos_mortos = []
        self.lista_matrizes_posicionamento = []
        self.matriz_status = np.zeros([tamanho_matriz,tamanho_matriz], dtype= int)
        
        self.fabrica_individuo = Fabrica_individuo(
                                                chance_infeccao,
                                                chance_infeccao_tipo2, 
                                                chance_morte, 
                                                atualizacoes_cura)

        self.matriz_individuos = pd.DataFrame(columns=range(tamanho_matriz), index=range(tamanho_matriz))
        self.matriz_individuos.loc[:] = self.fabrica_individuo.criar_individuo(Individuo.SADIO,(0,0))
        self.matriz_status[:] = Individuo.SADIO
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
        self.dataframe = pd.DataFrame(index = [0])
        self.salvar_posicionamento()
    
    
  
    def salvar_posicionamento(self):
        self.lista_matrizes_posicionamento.append(self.matriz_status)
        

    def verificar_infeccao(self, lista_infectantes):
        lista_novos_infectados_tipo1 = []
        lista_novos_infectados_tipo2 = []
        #itera sobre sobre a lista de individuos que infectam e cada um realiza a tividade de infectar
        for indice in lista_infectantes:
            #busca os vizinhos do infectante atual
            lista_vizinhos = self.matriz_esferica.get_vizinhos(indice[0], indice[1])
            #Para cada vizinho, se ele for sadio, é gerado um número aleatório para verificar se foi infectado
            for vizinho in lista_vizinhos:
                x = vizinho[0]
                y = vizinho[1]
                #verificação de SADIO
                if self.matriz_status[x,y] == Individuo.SADIO:
                    #verificação do novo status
                    novo_status = self.matriz_individuos.loc[indice[0], indice[1]].infectar()
                    #se for um infectado tipo 1
                    if novo_status == Individuo.INFECTADO_TIPO_1:
                        #adiciona na lista de novos tipo 1
                        lista_novos_infectados_tipo1.append((x,y))
                        #modifica o status do objeto recém infectado
                        self.matriz_individuos.loc[x,y].status = Individuo.INFECTADO_TIPO_1
                        #modifica o status na matriz de status
                        self.matriz_status[x,y] = Individuo.INFECTADO_TIPO_1
                    if novo_status == Individuo.INFECTADO_TIPO_2:
                        #adiciona na lista de novos tipo 2
                        lista_novos_infectados_tipo2.append((x,y))
                        #modifica o status do objeto recém infectado
                        self.matriz_individuos.loc[x,y].status = Individuo.INFECTADO_TIPO_2
                        #modifica o status na matriz de status
                        self.matriz_status[x,y] = Individuo.INFECTADO_TIPO_2
        return lista_novos_infectados_tipo1, lista_novos_infectados_tipo2

    def verificar_morte(self, lista_infectantes_tipo2):
        lista_mortos = []
        for indice in lista_infectantes_tipo2:
            novo_status = self.matriz_individuos.loc[indice[0], indice[1]].checagem_morte()
            if novo_status == Individuo.MORTO:
                lista_mortos.append(indice)
                self.matriz_status[indice[0], indice[1]] = Individuo.MORTO

        return lista_mortos
    
    
    def verificar_cura(self, lista_infectantes):
        lista_curados = []
        for indice in lista_infectantes:
            novo_status = self.matriz_individuos.loc[indice[0], indice[1]].checagem_cura()
            if novo_status == Individuo.CURADO:
                lista_curados.append(indice)
                self.matriz_status[indice[0], indice[1]] = Individuo.CURADO
        
        return lista_curados
    
    
    
    
    def iterar(self):

        #Verifica os novos infectados a partir dos atuais infectantes na matriz
        lista_novos_infectados_tipo1_1, lista_novos_infectados_tipo2_1 = self.verificar_infeccao(self.individuos_infectados_tipo_1)
        lista_novos_infectados_tipo1_2, lista_novos_infectados_tipo2_2 = self.verificar_infeccao(self.individuos_infectados_tipo_2)
        
        #Verifica morte dos tipo 2
        lista_mortos = self.verificar_morte(self.individuos_infectados_tipo_2)
        
        

        #retirar os mortos da atualização da lista de infectados tipo 2
        self.individuos_infectados_tipo_2 = [i for i in self.individuos_infectados_tipo_2 if i not in lista_mortos]

        #adiciona os novos mortos na lista geral de mortos
        self.individuos_infectados_mortos = self.individuos_infectados_mortos + lista_mortos


        #Verificar cura
        lista_curados_tipo1 = verificar_cura(self.individuos_infectados_tipo_1)
        lista_curados_tipo2 = verificar_cura(self.individuos_infectados_tipo_2)

        #retirar os curados das lista de infectados tipo 1 e 2
        self.individuos_infectados_tipo_2 = [i for i in self.individuos_infectados_tipo_2 if i not in lista_curados_tipo2]
        self.individuos_infectados_tipo_1 = [i for i in self.individuos_infectados_tipo_1 if i not in lista_curados_tipo1]

        #adiciona os novos curados na lista geral de curados
        # self.  #movimentar infectantes:
        for i in range(len(self.individuos_infectados_tipo_1)):
            self.individuos_infectados_tipo_1[i] = self.mover_infectante(self.individuos_infectados_tipo_1[i])
        
        for i in range(len(self.individuos_infectados_tipo_2)):
            self.individuos_infectados_tipo_2[i] = self.mover_infectante(self.individuos_infectados_tipo_2[i])


        #adicionar os novos infectados tipo 1 e 2 para as respectivas listas
        self.individuos_infectados_tipo_2 = self.individuos_infectados_tipo_2 + lista_novos_infectados_tipo2_1 + lista_novos_infectados_tipo2_2
        self.individuos_infectados_tipo_1 = self.individuos_infectados_tipo_1 + lista_novos_infectados_tipo1_1 + lista_novos_infectados_tipo1_2  
       

        #salva os resultados da atualização no dataframe:
        num_mortos = len(self.individuos_mortos)
        
        num_curados = len(self.individuos_curados)

        num_tipo_1 = len(self.individuos_infectados_tipo_1)

        num_tipo_2 = len(self.individuos_infectados_tipo_2)
         
        dict = {
                'num_sadios':self.populacao_inicial - num_mortos - num_curados - num_tipo_1 - num_tipo_2 ,
                'num_infect_t1':num_tipo_1,
                'num_infect_t2':num_tipo_2,
                'num_curados':num_curados,
                'num_mortos':num_mortos}
        
        self.dataframe = self.dataframe.append(dict, ignore_index=True)



        #salva a nova matriz de status
        self.salvar_posicionamento()

        #adiciona 1 ao número de atualizações realizadas na matriz
        self.num_atualizacoes +=1

        
    
    def popular(self, tamanho_matriz):
        #lista de possíveis combinações de índices da matriz de dados
        permutacoes = permutations(list(range(tamanho_matriz)),2)
        #conversão para lista de tuplas(x,y)
        lista_indices = list(permutacoes)
        #embaralhamento dos índices
        random.shuffle(lista_indices)
        
        #cria o primeiro tipo1:
        indice = lista_indices.pop()
        ind_x = indice[0]
        ind_y = indice[1]
        self.matriz_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
        #self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
        self.individuos_infectados_tipo_1.append((ind_x,ind_y))
        self.matriz_status[ind_x,ind_y] = Individuo.INFECTADO_TIPO_1
        
        #cria o restante dos tipos 1
        for i in range(1,self.num_inicial_tipo1):
            indice = lista_indices.pop()
            ind_x = indice[0]
            ind_y = indice[1]
            self.matriz_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
            #self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
            self.individuos_infectados_tipo_1.append((ind_x,ind_y))
            self.matriz_status[ind_x,ind_y] = Individuo.INFECTADO_TIPO_1

        #cria o restante dos tipo 2:
        for indice in range(self.num_inicial_tipo2):
            indice = lista_indices.pop()
            ind_x = indice[0]
            ind_y = indice[1]
            self.matriz_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_2,(ind_x,ind_y))
            #self.matriz_individuos[ind_x, ind_y] = Individuo.INFECTADO_TIPO_1
            self.individuos_infectados_tipo_2.append((ind_x,ind_y))
            self.matriz_status[ind_x,ind_y] = Individuo.INFECTADO_TIPO_2
    
      
    def mover_infectante(self, indice):
        pos_x, pos_y = indice[0], indice[1]
        rng_posicao = random.random()
        if rng_posicao <=0.25:
            #move pra cima
            pos_x -= 1
        elif rng_posicao <=0.5:
            #move pra baixo
            pos_x += 1
        elif rng_posicao <=0.75:
            #move para esquerda
            pos_y -= 1
        else:
            #move para direita
            pos_y += 1
        
        novo_x, novo_y = self.matriz_esferica.validar(pos_x, pos_y)
        #troca os valores no dataframe
        aux = self.matriz_individuos.loc[novo_x, novo_y]
        self.matriz_individuos.loc[novo_x, novo_y] = self.matriz_individuos.loc[pos_x, pos_y]
        self.matriz_individuos.loc[pos_x, pos_y] = aux

        #troca os valores na matriz de status
        aux = self.matriz_status[novo_x, novo_y]
        self.self.matriz_status[novo_x, novo_y] = self.matriz_status[pos_x, pos_y]
        self.self.matriz_status[pos_x, pos_y] = aux


        return (novo_x, novo_y)
        

                                            


chance_infeccao = 0.3             
chance_infeccao_tipo2 = 0.2       
chance_morte = 0.2                
atualizacoes_cura = 10           
percentual_inicial_tipo1 = 0.   
percentual_inicial_tipo2 = 0.


sim = Simulador(
    10000,
    percentual_inicial_tipo1, 
    percentual_inicial_tipo2, 
    chance_infeccao,
    chance_infeccao_tipo2,
    chance_morte,atualizacoes_cura)

#print(sim.lista_matrizes_posicionamento[0])
#print(sim.individuos_infectados_tipo_2)
#print(sim.individuos_infectados_tipo_1)
#cmap = ListedColormap(['w', 'y', 'yellow', 'red'])
#plt.matshow(sim.matriz_individuos, cmap = cmap);plt.show();

sim.iterar()

matriz =  sim.matriz_status

#print(sim.lista_matrizes_posicionamento[0])
        
