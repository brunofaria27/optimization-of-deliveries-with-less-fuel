def load_stores(filename):
    lojas = {}
    with open(filename) as arquivo:
        for linha in arquivo:
            campos = linha.split()
            loja_id = int(campos[0])
            x_coord, y_coord = int(campos[1]), int(campos[2])
            lista_destinos = []
            if len(campos) > 3: # Se tiver uma lista de destinos
                lista_destinos = [int(d) for d in campos[3:]]
            lojas[loja_id] = (x_coord, y_coord, lista_destinos)
    return lojas