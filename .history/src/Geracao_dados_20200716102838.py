from Simulador import Simulador
import math
import pandas as pd

# d = pd.read_pickle('C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/simulacoes_chance_30%.pkl')
# d.to_csv(r'C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/simulacoes_chance_30%.txt', sep=' ', index=False)
# d = pd.read_pickle('C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/simulacoes_chance_100%.pkl')
# d.to_csv(r'C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/simulacoes_chance_100%.txt', sep=' ', index=False)
# print(d.head())
nome_simulacao = "simulacoes_chance_100%" 
n_simulacoes = 100
tamanho_matriz = 40
chance_infeccao = 1 
chance_infeccao_sintomatico = 0.2

chance_morte = 0.02 
atualizacoes_cura = 10 
inserir_infectados_aleatorios = False
import numpy as np
import random                                         

dados_simulacoes = pd.DataFrame(dtype=np.int)
for i in range(n_simulacoes):
  random.seed()

  sim = Simulador(
      tamanho_matriz,
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
                                     "tipo1_n/2_100%_infectados",
                                     "tipo2_n/2_100%_infectados",
                                     "curados_n/2_100%_infectados",
                                     "mortos_n/2_100%_infectados",

                                     "n/2+1_100%_infectados",
                                     "tipo1_n/2+1_100%_infectados",
                                     "tipo2_n/2+1_100%_infectados",
                                     "curados_n/2+1_100%_infectados",
                                     "mortos_n/2+1_100%_infectados",

                                     "n_100%_infectados",
                                     "tipo1_n_100%_infectados",
                                     "tipo2_n_100%_infectados",
                                     "curados_n_100%_infectados",
                                     "mortos_n_100%_infectados",
                                     
                                     "n/2_pico",
                                     "tipo1_n/2_pico",
                                     "tipo2_n/2_pico",
                                     "curados_n/2_pico",
                                     "mortos_n/2_pico",
                                    
                                     "n/2+1_pico",
                                     "tipo1_n/2+1_pico",
                                     "tipo2_n/2+1_pico",
                                     "curados_n/2+1_pico",
                                     "mortos_n/2+1_pico",

                                     "n_pico",
                                     "tipo1_n_pico",
                                     "tipo2_n_pico",
                                     "curados_n_pico",
                                     "mortos_n_pico",
                                     
                                     "n_total",
                                     "sadios_n_total",
                                     "curados_n_total",
                                     "mortos_n_total"]].astype(int)





dados_simulacoes.to_csv('C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/'+ nome_simulacao + '.txt', sep=' ', index=False)

print(dados_simulacoes)
nome_simulacao = "simulacoes_chance_30%" 
chance_infeccao = 0.3 

dados_simulacoes = pd.DataFrame(dtype=np.int)
for i in range(n_simulacoes):
  random.seed()
  sim = Simulador(
      tamanho_matriz,
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
                                     "tipo1_n/2_100%_infectados",
                                     "tipo2_n/2_100%_infectados",
                                     "curados_n/2_100%_infectados",
                                     "mortos_n/2_100%_infectados",

                                     "n/2+1_100%_infectados",
                                     "tipo1_n/2+1_100%_infectados",
                                     "tipo2_n/2+1_100%_infectados",
                                     "curados_n/2+1_100%_infectados",
                                     "mortos_n/2+1_100%_infectados",

                                     "n_100%_infectados",
                                     "tipo1_n_100%_infectados",
                                     "tipo2_n_100%_infectados",
                                     "curados_n_100%_infectados",
                                     "mortos_n_100%_infectados",
                                     
                                     "n/2_pico",
                                     "tipo1_n/2_pico",
                                     "tipo2_n/2_pico",
                                     "curados_n/2_pico",
                                     "mortos_n/2_pico",
                                    
                                     "n/2+1_pico",
                                     "tipo1_n/2+1_pico",
                                     "tipo2_n/2+1_pico",
                                     "curados_n/2+1_pico",
                                     "mortos_n/2+1_pico",

                                     "n_pico",
                                     "tipo1_n_pico",
                                     "tipo2_n_pico",
                                     "curados_n_pico",
                                     "mortos_n_pico",
                                     
                                     "n_total",
                                     "sadios_n_total",
                                     "curados_n_total",
                                     "mortos_n_total"]].astype(int)


dados_simulacoes.to_csv('C:/Users/Eduar/Documents/GitHub/Trabalho_final_estatistica_cd/dados/'+ nome_simulacao + '.txt', sep=' ', index=False)

print(dados_simulacoes)