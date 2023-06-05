# Ciências da Computação - Projeto e Análise de Algoritmos
# Bruno Faria - 742238
# Lucas de Paula - 727840
# Maria Luisa Raso - 698215

class ListaLimitada:
    def __init__(self, tamanho_maximo):
        self.lista = []
        self.tamanho_maximo = tamanho_maximo

    def adicionar(self, item):
        if len(self.lista) < self.tamanho_maximo:
            self.lista.append(item)
            return True
        return False
        
    def remover_por_valor(self, valor):
        if valor in self.lista:
            self.lista.remove(valor)
            return True
        return False

    def __len__(self):
        return len(self.lista)

    def __str__(self):
        return str(self.lista)