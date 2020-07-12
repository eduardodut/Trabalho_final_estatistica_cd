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
    SADIO = 0
    INFECTADO_TIPO_1 = 1 #assintomáticos e o infectado inicial
    INFECTADO_TIPO_2 = 2 #sintomático
    CURADO = 3
    MORTO = 4

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
        self.atualizacoes_cura = atualizacoes_cura
        
        self.populacao_inicial = int(tamanho_matriz**2)
        self.num_inicial_tipo2 = int(self.populacao_inicial * percentual_inicial_tipo2)
        self.num_inicial_tipo1 = 1 + int(self.populacao_inicial * percentual_inicial_tipo1)
        self.num_inicial_sadios = self.populacao_inicial - (self.num_inicial_tipo2 + self.num_inicial_tipo1)
       


        
        self.matriz_status = lil_matrix((tamanho_matriz, tamanho_matriz),dtype= np.uint8)
        self.matriz_atualizacoes_cura = lil_matrix((tamanho_matriz, tamanho_matriz),dtype= np.uint8)



        #self.matriz_status = self.df_individuos.to_numpy()
        self.popular(tamanho_matriz)
      
        self.lista_matrizes_status = []
        

        #objeto que é responsável por validar a movimentação no grid n x n    
        self.matriz_esferica = Matriz_esferica(tamanho_matriz)
         
        

       
        dict = {
                'num_sadios':self.num_inicial_sadios,
                'num_infect_t1':self.num_inicial_tipo1,
                'num_infect_t2':self.num_inicial_tipo2,
                'num_curados':0,
                'num_mortos':0}
            

        #dataframe que guardará os resultados de cada atualização  
        self.dataframe = pd.DataFrame(dict,index = [0])
        self.salvar_posicionamento()
    
    
    def criar_individuo(self, status, posicao):
        self.matriz_status[posicao[0], posicao[1]] = status
        if status == self.INFECTADO_TIPO_1 or status == self.INFECTADO_TIPO_2:
            self.matriz_status[posicao[0], posicao[1]] = self.atualizacoes_cura
           
        

    def salvar_posicionamento(self):
        
        self.lista_matrizes_status.append(self.matriz_status)
        

    def verificar_infeccao(self, lista_infectantes):
        lista_novos_infectados_tipo1 = []
        lista_novos_infectados_tipo2 = []
        #itera sobre sobre a lista de individuos que infectam e cada um realiza a tividade de infectar
        print(lista_infectantes)
        for indice_infectante in lista_infectantes:            
            print("Infectante na posição: ", indice_infectante)
            #busca os vizinhos do infectante atual
            lista_vizinhos = self.matriz_esferica.get_vizinhos(indice_infectante)
            print("Lista vizinhos: ", lista_vizinhos)
            #Para cada vizinho, se ele for sadio, é gerado um número aleatório para verificar se foi infectado
            for indice_vizinho in lista_vizinhos:
                
                #verificação de SADIO
                if self.verifica_status(indice_vizinho) == self.SADIO:
                    #verificação do novo status
                    novo_status = self.infectar(chance_infeccao, chance_infeccao_tipo2)
                    #se for um infectado tipo 1
                    if novo_status == Individuo.INFECTADO_TIPO_1:
                        #adiciona na lista de novos tipo 1
                        lista_novos_infectados_tipo1.append(indice_vizinho)
                        self.criar_individuo(Individuo.INFECTADO_TIPO_1,indice_vizinho)
                                               
                    if novo_status == Individuo.INFECTADO_TIPO_2:
                        #adiciona na lista de novos tipo 1
                        lista_novos_infectados_tipo2.append(indice_vizinho)
                        self.criar_individuo(Individuo.INFECTADO_TIPO_2,indice_vizinho)
               
        return lista_novos_infectados_tipo1, lista_novos_infectados_tipo2

    def verificar_morte(self, lista_infectantes_tipo2):
        lista_curados = []
        lista_mortos = []
        for x,y in lista_infectantes_tipo2:
            novo_status = self.df_individuos.loc[x,y].checagem_morte(self.chance_morte)
            if novo_status == Individuo.MORTO:
                
                self.matriz_status[x,y] = Individuo.MORTO
                lista_mortos.append((x,y))
            if novo_status == Individuo.CURADO:
                
                self.matriz_status[x,y] = Individuo.CURADO
                lista_curados.append((x,y))

        return lista_mortos, lista_curados
    
    
    def verificar_cura(self, lista_infectantes):
        lista_curados = []
        for x,y in lista_infectantes:
            print("AQUI======>: ", self.df_individuos.loc[x,y])
            novo_status = self.df_individuos.loc[x,y].checagem_cura()
            if novo_status == Individuo.CURADO:
                
                self.matriz_status[x,y] = Individuo.CURADO
                lista_curados.append((x,y))
        
        return lista_curados
    
    
    
    
    def iterar(self):

        #Verifica os novos infectados a partir dos atuais infectantes na matriz
        lista_novos_infectados_tipo1, lista_novos_infectados_tipo2 = self.verificar_infeccao(self.lista_infectados_tipo_1)
        lista_novos_infectados_tipo1, lista_novos_infectados_tipo2 = self.verificar_infeccao(self.lista_infectados_tipo_2)

        
        #Verifica morte dos tipo 2
        lista_mortos_atualizacao, lista_curados_t2_atualizacao = self.verificar_morte(self.lista_infectados_tipo_2)
        
        self.lista_infectados_tipo_2 = [indice for indice in self.lista_infectados_tipo_2 if indice not in lista_mortos_atualizacao and indice not in lista_curados_t2_atualizacao]
        

        #atualiza o novo número de mortos
        self.num_mortos += len(lista_mortos_atualizacao)
        #Verificar cura
        lista_curados_t1_atualizacao = self.verificar_cura(self.lista_infectados_tipo_1)
        self.lista_infectados_tipo_1 = [indice for indice in self.lista_infectados_tipo_1 if indice not in lista_curados_t1_atualizacao ]
        #adiciona os novos curados na lista geral de curados
        self.num_curados = self.num_curados + len(lista_curados_t1_atualizacao) + len(lista_curados_t2_atualizacao)

        # self.  #movimentar infectantes:
        # for x,y in self.lista_infectados_tipo_1:
        #     self.mover_infectante((x,y))
        
        # for x,y in self.lista_infectados_tipo_2:
        #     self.mover_infectante((x,y))

        #adicionar os novos infectados tipo 1 e 2 para as respectivas listas
        self.lista_infectados_tipo_2 = self.lista_infectados_tipo_2 + lista_novos_infectados_tipo2
        self.lista_infectados_tipo_1 = self.lista_infectados_tipo_1 + lista_novos_infectados_tipo1
                
         
        dict = {
                'num_sadios':self.populacao_inicial - self.num_mortos - self.num_curados - len(self.lista_infectados_tipo_1) - len(self.lista_infectados_tipo_2) ,
                'num_infect_t1':len(self.lista_infectados_tipo_1),
                'num_infect_t2':len(self.lista_infectados_tipo_2),
                'num_curados':self.num_curados,
                'num_mortos':self.num_mortos}
        
        self.dataframe = self.dataframe.append(dict, ignore_index=True)
        
        print("num t1: ", len(self.lista_infectados_tipo_1))
        print("num t2: ", len(self.lista_infectados_tipo_2))
        print("num curados: ", self.num_curados)
        print("num mortos: ", self.num_mortos)
        print("---------")
        #salva a nova matriz de status
        self.salvar_posicionamento()

        #adiciona 1 ao número de atualizações realizadas na matriz
        self.num_atualizacoes +=1

    def infectar(self, chance_infeccao, chance_infeccao_tipo2):
        saida = Individuo.SADIO    
    
        #número aleatório para chance de infectar o vizinho
        rng_infeccao = random.random()
        if rng_infeccao <= chance_infeccao:
            #número aleatório para chance de infecção tipo 1 ou 2
            rng_infeccao_tipo2 = random.random()
            if rng_infeccao_tipo2 <= chance_infeccao_tipo2:
                saida = Individuo.INFECTADO_TIPO_2
            else:
                saida = Individuo.INFECTADO_TIPO_1
        return saida
    
    def popular(self, tamanho_matriz):
       
        #self.df_individuos.iloc[:,:] = self.criar_individuo(Individuo.SADIO,(0,0))

        #lista de possíveis combinações de índices da matriz de dados
        permutacoes = permutations(list(range(tamanho_matriz)),2)
        #conversão para lista de tuplas(x,y)
        lista_indices = list(permutacoes)
        #embaralhamento dos índices
        random.shuffle(lista_indices)
         
        #cria o primeiro tipo1:
        indice = lista_indices.pop()
        self.criar_individuo(Individuo.INFECTADO_TIPO_1,indice)
        self.lista_infectados_tipo_1.append(indice)
        #cria o restante dos tipos 1
        for i in range(1,self.num_inicial_tipo1):
            indice = lista_indices.pop()
            self.criar_individuo(Individuo.INFECTADO_TIPO_1,indice)
            self.lista_infectados_tipo_1.append(indice)
        #cria o restante dos tipo 2:
        for indice in range(self.num_inicial_tipo2):
            indice = lista_indices.pop()
            self.criar_individuo(Individuo.INFECTADO_TIPO_2,indice)
            self.lista_infectados_tipo_2.append(indice)
    
    def trocar_status_localizacao(self,ponto_ini,ponto_final):
        x_ini = ponto_ini[0]
        y_ini = ponto_ini[1]
        x_fin = ponto_final[0]
        y_fin = ponto_final[1]

        aux = self.df_individuos.loc[x_fin,y_fin]
        print("Aux2====>: ",self.df_individuos.loc[x_fin,y_fin])
        self.df_individuos.loc[x_fin,y_fin], self.df_individuos.loc[x_ini,y_ini] = self.df_individuos.loc[x_ini,y_ini], self.df_individuos.loc[x_fin,y_fin]
        # self.df_individuos.loc[x_fin,y_fin] = self.df_individuos.loc[x_ini,y_ini]
        # self.df_individuos.loc[x_ini,y_ini] = aux2
        
        self.matriz_status[x_fin,y_fin] = self.df_individuos.loc[x_fin,y_fin].status
        self.matriz_status[x_ini,y_ini] = self.df_individuos.loc[x_ini,y_ini].status

    def verifica_status(self,indice):
        return self.matriz_status(indice[0], indice[1])

    def mover_infectante(self, posicao_inicial):
        pos_x, pos_y = posicao_inicial[0], posicao_inicial[1]
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
        
        posicao_final= self.matriz_esferica.valida_ponto_matriz(pos_x, pos_y)
        
        self.trocar_status_localizacao(posicao_inicial, posicao_final)
       
       
        

                                            


chance_infeccao = 1        
chance_infeccao_tipo2 = 0.2     
chance_morte = 0.1                
atualizacoes_cura = 10           
percentual_inicial_tipo1 = 0.01
percentual_inicial_tipo2 = 0.01


sim = Simulador(
    10,
    percentual_inicial_tipo1, 
    percentual_inicial_tipo2, 
    chance_infeccao,
    chance_infeccao_tipo2,
    chance_morte,atualizacoes_cura)

#print(sim.lista_matrizes_posicionamento[0])
#print(sim.lista_infectados_tipo_2)
#print(sim.lista_infectados_tipo_1)
cmap = ListedColormap(['w', 'y', 'r', 'blue', 'black'])


# while sim.dataframe.iloc[-1]['num_infect_t1']+sim.dataframe.iloc[-1]['num_infect_t2'] > 0:
#     print(sim.df_individuos)
#     #print("xxxxxxxxxxxxxxxxxTipo: ",type(sim.lista_matrizes_posicionamento[len(sim.lista_matrizes_posicionamento)-1].toarray()))
#     #plt.matshow(sim.lista_matrizes_posicionamento[0], cmap = cmap, vmin= 0, vmax = 4)
#     #plt.show()
#     sim.iterar()

    
print(sim.dataframe)
print(sim.lista_infectados_tipo_1)
print(sim.lista_infectados_tipo_2)

# print("status inicial: ", sim.df_individuos[1][0].status)   

# print("Novos infectados: ", sim.verificar_infeccao(sim.lista_infectados_tipo_1))

# plt.show()


 
