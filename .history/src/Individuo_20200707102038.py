import random

class Individuo():
    
    SADIO = 0
    INFECTADO_TIPO_1 = 1
    INFECTADO_TIPO_2 = 2
    CURADO = 3
    MORTO = 4
    

    def __init__(self, status, chance_infeccao, chance_infeccao_tipo2, chance_morte):
        
        self.status = status
        self.chance_infeccao = chance_infeccao
        self.chance_infeccao_tipo2 = chance_infeccao_tipo2
        self.chance_morte = chance_morte
        self.atualizacoes = 10

    def infectar_vizinhos(self, lista_vizinhos):
        for vizinho in lista_vizinhos:
            self.infectar(vizinho)            
            
        return 
        
    def infectar(self, vizinho):

        if self.status == Individuo.INFECTADO_TIPO_2 and vizinho.status == Individuo.SADIO:
            
            rng_infeccao = random.random()

            if rng_infeccao <= self.chance_infeccao:
                rng_infeccao_tipo2 = random.random()
                if rng_infeccao_tipo2 <= self.chance_infeccao_tipo2:
                    vizinho.status = Individuo.INFECTADO_TIPO_2
                else:
                    vizinho.status = Individuo.INFECTADO_TIPO_1
        return 
    
    def checagem_morte(self):
        rng_morte = random.random()
        if rng_morte <= self.chance_morte:
            self.status = Individuo.MORTO




        

individuo_doente = Individuo(Individuo.INFECTADO_TIPO_2, 0.5, 0.5,0.2)
individuo_sadio = Individuo(Individuo.SADIO, 0.5,0.5,0.2)


individuo_doente.infectar(vizinho= individuo_sadio)


print(individuo_sadio.status)
print(individuo_sadio.chance_morte)