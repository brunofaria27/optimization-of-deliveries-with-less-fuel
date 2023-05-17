class ListaLimitada:
    def __init__(self, tamanho_maximo):
        self.lista = []
        self.tamanho_maximo = tamanho_maximo

    def adicionar(self, item):
        if len(self.lista) < self.tamanho_maximo:
            self.lista.append(item)
        else:
            raise Exception('Não é possível adicionar mais itens à lista')
        
    def remover_por_valor(self, valor):
        if valor in self.lista:
            self.lista.remove(valor)
        else:
            raise ValueError(f'O valor {valor} não está presente na lista')

    def __len__(self):
        return len(self.lista)

    def __str__(self):
        return str(self.lista)