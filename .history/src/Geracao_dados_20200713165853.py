from Simulador import Simulador
import math
nome_simulacao = "simulacoes_chance_100%" 
n_simulacoes = 5
tamanho_matriz = 10
chance_infeccao = 1 
chance_infeccao_sintomatico = 0.2

chance_morte = 0.02 
atualizacoes_cura = 10 
inserir_infectados_aleatorios = True
import numpy as np
import random                                         
import pandas as pd
dados_simulacoes = pd.DataFrame(dtype=np.int)
for i in range(n_simulacoes):
#   num_inicial_infectados = random.randint(0,tamanho_matriz*tamanho_matriz-1)
  
#   proporcao_t1_t2 = random.random()

#   num_inicial_t1 = round(inserir_infectados_aleatorios*proporcao_t1_t2*num_inicial_infectados)
#   num_inicial_t2 = round(inserir_infectados_aleatorios*(1-proporcao_t1_t2)*num_inicial_infectados)

  sim = Simulador(
      tamanho_matriz,
    #   num_inicial_t1, 
    #   num_inicial_t2, 
      chance_infeccao,
      chance_infeccao_sintomatico,
      chance_morte,
      atualizacoes_cura,
      inserir_infectados_aleatorios)


  sim.executar_simulacao()   
  
  dados_simulacoes = dados_simulacoes.append(sim.dict_resumo, ignore_index = True)

dados_simulacoes = dados_simulacoes[["pop_inicial", 
                                     "tipo1_inicial",
                                     "tipo2_inicial", 
                                     "n/2_100%_infectados",
                                     "tipo1_n/2",
                                     "tipo2_n/2",
                                     "curados_n/2",
                                     "mortos_n/2",
                                     "n_atualizacoes_100%_infectados",
                                     "tipo1_n",
                                     "tipo2_n",
                                     "curados_n",
                                     "mortos_n",
                                     "numero_total_atualizacoes",
                                     "sadios_final",
                                     "curados_final",
                                     "mortos_final"]].astype(int)

dados_simulacoes.to_pickle('C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/'+ nome_simulacao + '.pkl')


nome_simulacao = "simulacoes_chance_30%" 
chance_infeccao = 0.3 

dados_simulacoes = pd.DataFrame(dtype=np.int)
for i in range(n_simulacoes):
#   num_inicial_infectados = random.randint(0,tamanho_matriz*tamanho_matriz-1)
  
#   proporcao_t1_t2 = random.random()

#   num_inicial_t1 = round(inserir_infectados_aleatorios*proporcao_t1_t2*num_inicial_infectados)
#   num_inicial_t2 = round(inserir_infectados_aleatorios*(1-proporcao_t1_t2)*num_inicial_infectados)

  sim = Simulador(
      tamanho_matriz,
    #   num_inicial_t1, 
    #   num_inicial_t2, 
      chance_infeccao,
      chance_infeccao_sintomatico,
      chance_morte,
      atualizacoes_cura,      
      inserir_infectados_aleatorios)


  sim.executar_simulacao()   
  
  dados_simulacoes = dados_simulacoes.append(sim.dict_resumo, ignore_index = True)

dados_simulacoes = dados_simulacoes[["pop_inicial", 
                                     "tipo1_inicial",
                                     "tipo2_inicial", 
                                     "n/2_100%_infectados",
                                     "tipo1_n/2",
                                     "tipo2_n/2",
                                     "curados_n/2",
                                     "mortos_n/2",
                                     "n/2+1_100%_infectados",
                                     "tipo1_n/2+1",
                                     "tipo2_n/2+1",
                                     "curados_n/2+1",
                                     "mortos_n/2+1",
                                     "n_atualizacoes_100%_infectados",
                                     "tipo1_n",
                                     "tipo2_n",
                                     "curados_n",
                                     "mortos_n",
                                     "numero_total_atualizacoes",
                                     "sadios_final",
                                     "curados_final",
                                     "mortos_final"]].astype(int)

dados_simulacoes.to_pickle('C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/'+ nome_simulacao + '.pkl')

print(dados_simulacoes)