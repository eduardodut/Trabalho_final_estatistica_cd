
import random

class Matriz_esferica():

    def __init__(self, tamanho):
        self.tamanho = tamanho

    def get_vizinho_esquerda(self, indice_x: int, indice_y: int):
        return self.checa_limite_matriz(indice_x), self.checa_limite_matriz(indice_y -1)

    def get_vizinho_direita(self, indice_x: int, indice_y: int):
        return self.checa_limite_matriz(indice_x), self.checa_limite_matriz(indice_y + 1)

    def get_vizinho_cima(self, indice_x: int, indice_y: int):
        return self.checa_limite_matriz(indice_x - 1), self.checa_limite_matriz(indice_y)

    def get_vizinho_baixo(self, indice_x: int, indice_y: int):
        return self.checa_limite_matriz(indice_x + 1), self.checa_limite_matriz(indice_y)

    def get_vizinhos(self, indice):
        indice_x = indice[0]
        indice_y = indice[1]
        return self.get_vizinho_cima(indice_x,indice_y), self.get_vizinho_baixo(indice_x,indice_y),  self.get_vizinho_esquerda(indice_x,indice_y), self.get_vizinho_direita(indice_x,indice_y)

    def checa_limite_matriz(self, indice):

        if indice < 0:
            return self.tamanho + indice
        elif indice > self.tamanho - 1:
            return indice - self.tamanho 
        else:
            return indice

    def valida_ponto_matriz(self, indice_x: int, indice_y: int):

        return self.checa_limite_matriz(indice_x), self.checa_limite_matriz(indice_y)

    #devolve um ponto aleatório vizinho da matriz a partir do ponto especificado em uma das 8 direções
    def passo(self, indice_x: int, indice_y: int, tamanho_max_passo: int):

        passo_x = tamanho_max_passo if random.random() >=0.5 else -tamanho_max_passo
        passo_y = tamanho_max_passo if random.random() >=0.5 else -tamanho_max_passo
        return self.checa_limite_matriz(indice_x + passo_x), self.checa_limite_matriz(indice_y + passo_y)


