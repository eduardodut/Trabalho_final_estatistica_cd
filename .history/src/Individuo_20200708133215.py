import random

class Individuo():
    
    SADIO = 0
    INFECTADO_TIPO_1 = 1 #assintomáticos e o infectado inicial
    INFECTADO_TIPO_2 = 2 #sintomático
    CURADO = 3
    MORTO = 4
    
    def __init__(
        self, 
        status, 
        chance_infeccao, 
        chance_infeccao_tipo2, 
        chance_morte, 
        atualizacoes_cura,
        posicao):
        
        self.status = status
        self.chance_infeccao = chance_infeccao
        self.chance_infeccao_tipo2 = chance_infeccao_tipo2
        self.chance_morte = chance_morte
        self.atualizacoes_cura = atualizacoes_cura
        self.posicao = posicao
    def __repr__(self):
        return  self.status
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

        if (self.status == Individuo.INFECTADO_TIPO_2 or self.status == Individuo.INFECTADO_TIPO_1):
            #número aleatório para chance de infectar o vizinho
            rng_infeccao = random.random()
            if rng_infeccao <= self.chance_infeccao:
                #número aleatório para chance de infecção tipo 1 ou 2
                rng_infeccao_tipo2 = random.random()
                if rng_infeccao_tipo2 <= self.chance_infeccao_tipo2:
                    vizinho.status = Individuo.INFECTADO_TIPO_2
                else:
                    vizinho.status = Individuo.INFECTADO_TIPO_1
        
        self.checagem_morte()
              
        
        return 
    
    def checagem_morte(self):
        if self.status == Individuo.INFECTADO_TIPO_2:
            rng_morte = random.random()
            if rng_morte <= self.chance_morte:
                self.status = Individuo.MORTO
            else:
                self.checagem_cura()

    def checagem_cura(self):
        if self.status == Individuo.INFECTADO_TIPO_2 or self.status == Individuo.INFECTADO_TIPO_1:
            self.atualizacoes_cura = self.atualizacoes_cura - 1
            
            if self.atualizacoes_cura == 0:
                self.status = Individuo.CURADO
    def get_status(self):
        return self.status
      

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
            

