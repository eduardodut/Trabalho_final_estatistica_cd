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
        atualizacoes_cura,
        posicao):
        
        self.status = status
        self.atualizacoes_cura = atualizacoes_cura
        self.posicao = posicao
    def __repr__(self):
        return  str(self.status)

           
    def infectar(self, chance_infeccao, chance_infeccao_tipo2):
        saida = Individuo.SADIO    
        if (self.status == Individuo.INFECTADO_TIPO_2 or self.status == Individuo.INFECTADO_TIPO_1):
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
    
    def checagem_morte(self, chance_morte):
        
        if self.status == Individuo.INFECTADO_TIPO_2:
            rng_morte = random.random()
            if rng_morte <= chance_morte:
                self.status = Individuo.MORTO
                return self.status
            
        return self.checagem_cura()

    def checagem_cura(self):
        if self.status == Individuo.INFECTADO_TIPO_2 or self.status == Individuo.INFECTADO_TIPO_1:
            self.atualizacoes_cura = self.atualizacoes_cura - 1
            
            if self.atualizacoes_cura == 0:
                self.status = Individuo.CURADO
        
        return self.status
   
      

class Fabrica_individuo():
    
    def __init__(
        self,
        atualizacoes_cura):             #número de atualizações necessárias para a cura de um indivíduo tipo 1 ou 2
        
        self.atualizacoes_cura = atualizacoes_cura
        
    def criar_individuo(self, status_inicial, posicao):
        
        return Individuo(
            status_inicial, 
            self.atualizacoes_cura,
            posicao)
            

