import random

class Individuo():
    
    SADIO = 0
    INFECTADO_TIPO_1 = 1
    INFECTADO_TIPO_2 = 2
    MORTO = 3
    CURADO = 4

    def __init__(self, status, chance_infeccao, chance_infeccao_tipo2):
        
        self.status = status
        self.atualizacoes = 10

    def infectar_vizinhos(lista_vizinhos):
        for vizinho in lista_vizinhos:
            
            
            end
        
        
        return 
    def infectar(vizinho):
        if self.status == Individuo.INFECTADO_TIPO_2 and vizinho.status == Individuo.SADIO:
            
            rng_infeccao = random.random()

            if rng_infeccao <= self.chance_infeccao:
                rng_infeccao_tipo2 = random.random()
                if rng_infeccao_tipo2 <= self.chance_infeccao_tipo2:
                    vizinho.status = Individuo.INFECTADO_TIPO_2
                else:
                    vizinho.status = Individuo.INFECTADO_TIPO_1

            
            
            
            end

        return 