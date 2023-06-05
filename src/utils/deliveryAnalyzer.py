# Ciências da Computação - Projeto e Análise de Algoritmos
# Bruno Faria - 742238
# Lucas de Paula - 727840
# Maria Luisa Raso - 698215

import math

def load_stores(filename):
    lojas = {}
    produtos = []
    with open(filename) as arquivo_entrada:
        for linha in arquivo_entrada:
            campos_linha = linha.split() #divide as informações das linhas do arquivo de entrada
            loja_id = int(campos_linha[0]) #id é sempre a primeira posicao da linha
            x_coord, y_coord = int(campos_linha[1]), int(campos_linha[2]) #coordenadas x e y da loja filial
            lista_destinos = []
            if len(campos_linha) > 3: # Se tiver uma lista de destinos
                for value in campos_linha[3:]:
                    lista_destinos += [int(value)]
                    produtos.append(int(value)) #pega quais produtos serao entregues
            lojas[loja_id] = (x_coord, y_coord, lista_destinos)
    return lojas, produtos

def pegarNumeroMaximoLojas(lojas):
    listas_entregas = [entregas[2] for entregas in lojas.values()]
    comprimento_maximo = max(len(entregas) for entregas in listas_entregas)
    return comprimento_maximo

def calculaDistancia(xA, yA, xB, yB):
    return math.sqrt((xA - xB)**2 + (yA - yB)**2)

def preCalcularMatrizDistancias(lojas):
    num_lojas = len(lojas)
    matriz_distancias = [[0] * num_lojas for _ in range(num_lojas)]

    for i in range(num_lojas):
        xA, yA = lojas[i][0], lojas[i][1]

        for j in range(num_lojas):
            xB, yB = lojas[j][0], lojas[j][1]
            distancia = calculaDistancia(float(xA), float(yA), float(xB), float(yB))
            matriz_distancias[i][j] = distancia
    return matriz_distancias

def pegarMenoresArestas(lojas, matriz_distancias):
    if len(lojas) >= 3:
        menores_arestas = {}

        for loja_id, _ in lojas.items():
            distancias = []
            for proxima_loja_id, _ in lojas.items():
                if loja_id != proxima_loja_id:
                    distancia = matriz_distancias[loja_id][proxima_loja_id]
                    distancias.append((proxima_loja_id, distancia))
            distancias.sort(key=lambda x: x[1])
            menores_arestas[loja_id] = [x[1] for x in distancias[:2]]
            calculo_lower = sum(sum(distancias) for distancias in menores_arestas.values())
        return (calculo_lower / 20) # divide por 2 e por 10, que é o rendimento do combustivel padrao
    elif len(lojas) > 1:
        comb = [(loja_id, proxima_loja_id) for loja_id in lojas for proxima_loja_id in lojas if loja_id != proxima_loja_id]
        for loja_id, proxima_loja_id in comb:
            distancia = matriz_distancias[loja_id][proxima_loja_id] 
        return (distancia / 10)
    return 0.0