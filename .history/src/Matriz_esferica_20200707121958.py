import numpy as np
import random
#regras de movimentacao
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


matriz = Matriz_esferica(10)


#print(matriz.passo(9,9, 2))

ponto = [9,9]
