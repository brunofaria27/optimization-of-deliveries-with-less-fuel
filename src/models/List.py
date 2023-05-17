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