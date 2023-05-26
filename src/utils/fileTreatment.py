def load_stores(filename):
    lojas = {}
    produtos = []
    with open(filename) as arquivo_entrada:
        for linha in arquivo_entrada:
            campos_linha = linha.split()
            loja_id = int(campos_linha[0])
            x_coord, y_coord = int(campos_linha[1]), int(campos_linha[2])
            lista_destinos = []
            if len(campos_linha) > 3: # Se tiver uma lista de destinos
                for value in campos_linha[3:]:
                    lista_destinos += [int(value)]
                    produtos.append(int(value))
            lojas[loja_id] = (x_coord, y_coord, lista_destinos)
    return lojas, produtos