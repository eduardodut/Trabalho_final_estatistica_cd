import numpy as np
import random
#regras de movimentacao
class Matriz_esferica():


    def __init__(self, tamanho):
        self.tamanho = tamanho
        

    def get_vizinho_esquerda(self, ponto):
        pass

    def get_vizinho_direita(self, ponto):
        pass

    def get_vizinho_cima(self, ponto):
        pass

    def get_vizinho_baixo(self, ponto):
        pass

    def checa_limite_matriz(self, indice):

        if indice < 0:
            return self.tamanho + indice
        elif indice > self.tamanho - 1:
            return indice - self.tamanho 
        else:
            return indice


    #devolve um ponto aleatório vizinho da matriz a partir do ponto especificado em uma das 8 direções
    def passo(self, indice_x: int, indice_y: int, tamanho_max_passo: int):

        passo_x = tamanho_max_passo if random.random() >=0.5 else -tamanho_max_passo
        passo_y = tamanho_max_passo if random.random() >=0.5 else -tamanho_max_passo
        return self.checa_limite_matriz(indice_x + passo_x), self.checa_limite_matriz(indice_y + passo_y)

    def passo(self, indice_x: int, indice_y: int):
        return Matriz_esferica.passo(indice_x, indice_y, 1)

matriz = Matriz_esferica(11)


print(matriz.passo(5,5, 1))