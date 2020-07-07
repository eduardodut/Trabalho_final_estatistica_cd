

class Individuo():
    SADIO = 0
    INFECTADO_TIPO_1 = 1
    INFECTADO_TIPO_2 = 2
    MORTO = 3

    def __init__(self, posicao, status):
        self.posicao = posicao


print(Individuo.SADIO)