import pandas as pd
import numpy as np
from Matriz_esferica import Matriz_esferica
from Individuo import Individuo, Fabrica_individuo
import random
from itertools import permutations 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.sparse import csr_matrix, lil_matrix




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
        self.lista_infectados_tipo_2 = []
        self.lista_infectados_tipo_1 = []
        self.num_curados = 0
        self.num_mortos = 0

        self.chance_infeccao = chance_infeccao
        self.chance_infeccao_tipo2 = chance_infeccao_tipo2
        self.chance_morte = chance_morte
        
        self.populacao_inicial = int(tamanho_matriz**2)
        self.num_inicial_tipo2 = int(self.populacao_inicial * percentual_inicial_tipo2)
        self.num_inicial_tipo1 = int(self.populacao_inicial * percentual_inicial_tipo1)
        self.num_inicial_sadios = self.populacao_inicial - (self.num_inicial_tipo2 + self.num_inicial_tipo1)
        self.fabrica_individuo = Fabrica_individuo(atualizacoes_cura)



        self.df_individuos = pd.DataFrame(index= range(tamanho_matriz), columns=range(tamanho_matriz))
        self.df_individuos.loc[:,:] = 0
        self.popular(tamanho_matriz)
        print(self.df_individuos.values)
        #lista que guarda o posicionamento 
        self.lista_matrizes_posicionamento = []
        #guarda em matriz esparsa o status de saúde de cada elemento
        

        

        #objeto que é responsável por validar a movimentação no grid n x n    
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)
        
        array = self.df_individuos.to_numpy()
        print(array)
        self.matriz_status = lil_matrix(array)

        print(self.df_individuos)
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
        for infectante in lista_infectantes:
            indice_x = infectante.posicao[0]
            indice_y = infectante.posicao[1]
            #busca os vizinhos do infectante atual
            lista_vizinhos = self.matriz_esferica.get_vizinhos(indice_x, indice_y)
            #Para cada vizinho, se ele for sadio, é gerado um número aleatório para verificar se foi infectado
            for vizinho in lista_vizinhos:
                x = vizinho[0]
                y = vizinho[1]
                #verificação de SADIO
                if self.matriz_status[x,y] == Individuo.SADIO:
                    #verificação do novo status
                    novo_status = infectante.infectar(chance_infeccao, chance_infeccao_tipo2)
                    #se for um infectado tipo 1
                    if novo_status == Individuo.INFECTADO_TIPO_1:
                        #adiciona na lista de novos tipo 1
                        lista_novos_infectados_tipo1.append(self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(x,y)))
                        #modifica o status na matriz de status
                        self.matriz_status[x,y] = Individuo.INFECTADO_TIPO_1
                        self.matriz_localizacao[x,y] = len(lista_novos_infectados_tipo1) - 1
                    if novo_status == Individuo.INFECTADO_TIPO_2:
                        #adiciona na lista de novos tipo 2
                        lista_novos_infectados_tipo2.append(self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_2,(x,y)))
                        #modifica o status na matriz de status
                        self.matriz_status[x,y] = Individuo.INFECTADO_TIPO_2
                        self.matriz_localizacao[x,y] = len(lista_novos_infectados_tipo2) - 1
        return lista_novos_infectados_tipo1, lista_novos_infectados_tipo2

    def verificar_morte(self, lista_infectantes_tipo2):
        num_mortos = 0
        num_curados = 0
        for infectante in lista_infectantes_tipo2:
            novo_status = infectante.checagem_morte(self.chance_morte)
            if novo_status == Individuo.MORTO:
                num_mortos += 1
                self.matriz_status[infectante.posicao[0], infectante.posicao[1]] = Individuo.MORTO
                lista_infectantes_tipo2.remove(infectante)
            if novo_status == Individuo.CURADO:
                num_curados += 1
                self.matriz_status[infectante.posicao[0], infectante.posicao[1]] = Individuo.CURADO
                lista_infectantes_tipo2.remove(infectante)

        return num_mortos, num_curados
    
    
    def verificar_cura(self, lista_infectantes):
        num_curados = 0
        for infectante in lista_infectantes:
            novo_status = infectante.checagem_cura()
            if novo_status == Individuo.CURADO:
                num_curados += 1
                self.matriz_status[infectante.posicao[0], infectante.posicao[1]] = Individuo.CURADO
                lista_infectantes_tipo.remove(infectante)
        
        return num_curados
    
    
    
    
    def iterar(self):

        #Verifica os novos infectados a partir dos atuais infectantes na matriz
        lista_novos_infectados_tipo1_1, lista_novos_infectados_tipo2_1 = self.verificar_infeccao(self.lista_infectados_tipo_1)
        lista_novos_infectados_tipo1_2, lista_novos_infectados_tipo2_2 = self.verificar_infeccao(self.lista_infectados_tipo_2)
        
        #Verifica morte dos tipo 2
        num_mortos_atualizacao, num_curados_t2_atualizacao = self.verificar_morte(self.lista_infectados_tipo_2)
        
        

        #retirar os mortos da atualização da lista de infectados tipo 2
        self.lista_infectados_tipo_2 = [i for i in self.lista_infectados_tipo_2 if i.status != Individuo.MORTO]

        #atualiza o novo número de mortos
        self.num_mortos += num_mortos_atualizacao


        #Verificar cura
        num_curados_t1_atualizacao = self.verificar_cura(self.lista_infectados_tipo_1)
        

        #retirar os curados das lista de infectados tipo 1 e 2
        self.lista_infectados_tipo_2 = [i for i in self.lista_infectados_tipo_2 if i.status != Individuo.CURADO]
        self.lista_infectados_tipo_1 = [i for i in self.lista_infectados_tipo_1 if i.status != Individuo.CURADO]

        #adiciona os novos curados na lista geral de curados
        self.num_curados = self.num_curados + num_curados_t1_atualizacao + num_curados_t2_atualizacao



        # self.  #movimentar infectantes:
        for infectante in self.lista_infectados_tipo_1:
            self.mover_infectante(infectante)
        
        for infectante in self.lista_infectados_tipo_2:
            self.mover_infectante(infectante)


        #adicionar os novos infectados tipo 1 e 2 para as respectivas listas
        self.lista_infectados_tipo_2 = self.lista_infectados_tipo_2 + lista_novos_infectados_tipo2_1 + lista_novos_infectados_tipo2_2
        self.lista_infectados_tipo_1 = self.lista_infectados_tipo_1 + lista_novos_infectados_tipo1_1 + lista_novos_infectados_tipo1_2  
       

       
        num_tipo_1 = len(self.lista_infectados_tipo_1)

        num_tipo_2 = len(self.lista_infectados_tipo_2)
         
        dict = {
                'num_sadios':self.populacao_inicial - self.num_mortos - self.num_curados - num_tipo_1 - num_tipo_2 ,
                'num_infect_t1':num_tipo_1,
                'num_infect_t2':num_tipo_2,
                'num_curados':self.num_curados,
                'num_mortos':self.num_mortos}
        
        self.dataframe = self.dataframe.append(dict, ignore_index=True)

        print("num t1: ", num_tipo_1)
        print("num t2: ", num_tipo_2)
        print("num curados: ", self.num_curados)
        print("num mortos: ", self.num_mortos)
        print("---------")
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
        self.lista_infectados_tipo_1.append((ind_x,ind_y))
        self.df_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
        
        #cria o restante dos tipos 1
        for i in range(1,self.num_inicial_tipo1):
            indice = lista_indices.pop()
            ind_x = indice[0]
            ind_y = indice[1]
            self.lista_infectados_tipo_1.append((ind_x,ind_y))
            self.df_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_1,(ind_x,ind_y))
        

        #cria o restante dos tipo 2:
        for indice in range(self.num_inicial_tipo2):
            indice = lista_indices.pop()
            ind_x = indice[0]
            ind_y = indice[1]
            self.lista_infectados_tipo_2.append((ind_x,ind_y))
            self.df_individuos.loc[ind_x,ind_y] = self.fabrica_individuo.criar_individuo(Individuo.INFECTADO_TIPO_2,(ind_x,ind_y))
        
    
    def trocar_status_localizacao(self,ponto_ini,ponto_final):
        x_ini = ponto_ini[0]
        y_ini = ponto_ini[1]
        x_fin = ponto_final[0]
        y_fin = ponto_final[1]

        aux1 = self.matriz_status[x_fin,y_fin]
        self.matriz_status[x_fin,y_fin] = self.matriz_status[x_ini,y_ini]
        self.matriz_status[x_ini,y_ini] = aux1

        aux2 = self.matriz_localizacao[x_fin,y_fin]
        self.matriz_localizacao[x_fin,y_fin] = self.matriz_localizacao[x_ini,y_ini]
        self.matriz_localizacao[x_ini,y_ini] = aux2



    def mover_infectante(self, infectante):
        pos_x, pos_y = infectante.posicao[0], infectante.posicao[1]
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
        
        novo_x, novo_y = self.matriz_esferica.valida_ponto_matriz(pos_x, pos_y)
        #descobre qual individuo ocupa atualmente a posição para atribuí-lo a posição de quem o está substituindo
        status = self.matriz_status[novo_x, novo_y]
        if status == Individuo.INFECTADO_TIPO_1:
            individuo_ocupante_destino = self.matriz_localizacao[novo_x, novo_y]
            print(status)
            print(individuo_ocupante_destino)
            print(len(self.lista_infectados_tipo_1))
            
            self.lista_infectados_tipo_1[individuo_ocupante_destino].posicao = infectante.posicao
        elif status == Individuo.INFECTADO_TIPO_2:
            individuo_ocupante_destino = self.matriz_localizacao[novo_x, novo_y]
            print(status)
            print(individuo_ocupante_destino)
            print(len(self.lista_infectados_tipo_2))
            self.lista_infectados_tipo_2[individuo_ocupante_destino].posicao = infectante.posicao
        
        # elif status == Individuo.CURADO:
        #     individuo_ocupante_destino = self.matriz_localizacao[novo_x, novo_y]
        #     self.lista_curados[individuo_ocupante_destino].posicao = infectante.posicao
        # elif status == Individuo.MORTO:
        #     individuo_ocupante_destino = self.matriz_localizacao[novo_x, novo_y]
        #     self.lista_matrizes_posicionamento[individuo_ocupante_destino].posicao = infectante.posicao


        self.trocar_status_localizacao(infectante.posicao,(novo_x, novo_y))

       
        

                                            


chance_infeccao = 1            
chance_infeccao_tipo2 = 0.      
chance_morte = 0.2                
atualizacoes_cura = 10           
percentual_inicial_tipo1 = 0.01   
percentual_inicial_tipo2 = 0.01


sim = Simulador(
    100,
    percentual_inicial_tipo1, 
    percentual_inicial_tipo2, 
    chance_infeccao,
    chance_infeccao_tipo2,
    chance_morte,atualizacoes_cura)

#print(sim.lista_matrizes_posicionamento[0])
#print(sim.lista_infectados_tipo_2)
#print(sim.lista_infectados_tipo_1)
#cmap = ListedColormap(['w', 'y', 'yellow', 'red'])



# plt.matshow(sim.lista_matrizes_posicionamento[0].toarray())#, cmap = cmap)
# sim.iterar()


# plt.matshow(sim.lista_matrizes_posicionamento[1].toarray())#, cmap = cmap)
# sim.iterar()

# plt.matshow(sim.lista_matrizes_posicionamento[2].toarray())#, cmap = cmap)
# sim.iterar()

# plt.matshow(sim.lista_matrizes_posicionamento[3].toarray())#, cmap = cmap)
# sim.iterar()

# plt.matshow(sim.lista_matrizes_posicionamento[4].toarray())#, cmap = cmap)
# sim.iterar()


# plt.matshow(sim.lista_matrizes_posicionamento[5].toarray())#, cmap = cmap)
# sim.iterar()
# plt.show(); 



 
