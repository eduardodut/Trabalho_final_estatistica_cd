import random

class Individuo():
    
    SADIO = 0
    INFECTADO_TIPO_1 = 1
    INFECTADO_TIPO_2 = 2
    CURADO = 3
    MORTO = 4
    

    def __init__(self, status, chance_infeccao, chance_infeccao_tipo2, chance_morte, atualizacoes_cura):
        
        self.status = status
        self.chance_infeccao = chance_infeccao
        self.chance_infeccao_tipo2 = chance_infeccao_tipo2
        self.chance_morte = chance_morte
        self.atualizacoes = atualizacoes_cura

    def infectar_vizinhos(self, lista_vizinhos):
        lista_infectados_tipo1 = []
        lista_infectados_tipo2 = []
        for vizinho in lista_vizinhos:
            self.infectar(vizinho)
            if vizinho.status == Individuo.INFECTADO_TIPO_2:
                lista_infectados_tipo2.append(vizinho)
            elif vizinho.status == Individuo.INFECTADO_TIPO_1:
                lista_infectados_tipo1.append(vizinho)
        return 
        
    def infectar(self, vizinho):

        if self.status == Individuo.INFECTADO_TIPO_2 and vizinho.status == Individuo.SADIO:
            #número aleatório para chance de infectar o vizinho
            rng_infeccao = random.random()
            if rng_infeccao <= self.chance_infeccao:
                #número aleatório para chance de infecção tipo 1 ou 2
                rng_infeccao_tipo2 = random.random()
                if rng_infeccao_tipo2 <= self.chance_infeccao_tipo2:
                    vizinho.status = Individuo.INFECTADO_TIPO_2
                else:
                    vizinho.status = Individuo.INFECTADO_TIPO_1
        return 
    
    def checagem_morte(self):
        if self.status == Individuo.INFECTADO_TIPO_2:
            rng_morte = random.random()
            if rng_morte <= self.chance_morte:
                self.status = Individuo.MORTO

    def checagem_cura(self):
        if self.status == Individuo.INFECTADO_TIPO_2 or self.status == Individuo.INFECTADO_TIPO_1:
            self.atualizacoes_cura -=1
            if self.atualizacoes_cura == 0:
                self.status = Individuo.CURADO


        self.atualizacoes


        

individuo_doente = Individuo(Individuo.INFECTADO_TIPO_2, 0.5, 0.5, 0.2, 10)
individuo_sadio = Individuo(Individuo.SADIO, 0.5, 0.5, 0.2, 10)

individuo_doente.infectar(vizinho= individuo_sadio)

print(individuo_sadio.status)

print(individuo_sadio.chance_morte)