# Bibliotecas do python
import math
import copy
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Funções
import utils.utils_solutions as utils

# Objetos
from models.List import ListaLimitada

def permutacoes(lojas):
    lojas_filiais = list(lojas.keys())
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação

    def generate_permutations(lista_lojas):
        if len(lista_lojas) == 0: return [[]]

        permutacoes = []
        for i in range(len(lista_lojas)):
            elementos_restantes = lista_lojas[:i] + lista_lojas[i + 1:] 
            permutacoes_restantes = generate_permutations(elementos_restantes)
            for perm in permutacoes_restantes:
                permutacoes.append([lista_lojas[i]] + perm)
        return permutacoes
    permutacoes = generate_permutations(lojas_filiais)
    permutacoes_com_zero = [[0] + perm + [0] for perm in permutacoes] # Adicionando destino e origem na permutação
    return permutacoes_com_zero

def calculate_distance(xA, yA, xB, yB):
    return math.sqrt((xA - xB)**2 + (yA - yB)**2)

def calcula_viagem_total(lojas, caminho, k_produtos):
    lista_rendimento_plotar = list()
    lista_produtos = list()

    produtos_pegos = ListaLimitada(k_produtos)
    lojas_copy = copy.deepcopy(lojas)
    rendimento = 10

    for loja in range(len(caminho) - 1):
        if caminho[loja] != 0:
            produtos_loja = lojas[caminho[loja]][2].copy()

            # Verificar se tem entrega
            if caminho[loja] in produtos_pegos.lista:
                for entrega in produtos_pegos.lista.copy():
                    if entrega == caminho[loja]:
                        produtos_pegos.remover_por_valor(caminho[loja])
                        rendimento += 0.5
            
            # Pegar produtos
            if len(produtos_loja) != []:
                for produto in produtos_loja:
                    if produtos_pegos.adicionar(produto):
                        lojas_copy[caminho[loja]][2].remove(produto)
                        rendimento -= 0.5
                produtos_loja.clear()
                
        xA, yA = lojas[caminho[loja]][0], lojas[caminho[loja]][1]
        xB, yB = lojas[caminho[loja + 1]][0], lojas[caminho[loja + 1]][1]
        distancia = calculate_distance(xA, yA, xB, yB)
        lista_rendimento_plotar.append(distancia / rendimento)
        lista_produtos.append(produtos_pegos.lista.copy())
    return len(produtos_pegos), lojas_copy, lista_rendimento_plotar, lista_produtos

def verificaProdutosEntregues(lojas):
    for entregas in lojas.values():
        if entregas[2]:  # Verifica se a lista de entregas da loja não está vazia
            return False
    return True

def bruteForce(filename, k_produtos):
    lojas = utils.load_stores(filename)
    possiveis_caminhos = generate_permutations(lojas)

    melhor_caminho = None
    melhor_custo = float('inf')
    lista_melhor_custo = None
    lista_itens_caminhao = None

    for caminho in possiveis_caminhos:
        itens_caminhao, lojas_copy, lista_rendimento_plotar, lista_teste = calcula_viagem_total(lojas, caminho, int(k_produtos))
        custo_viagem = sum(lista_rendimento_plotar)
        if itens_caminhao == 0 and custo_viagem < melhor_custo and verificaProdutosEntregues(lojas_copy):
            melhor_caminho = caminho
            melhor_custo = custo_viagem
            lista_melhor_custo = lista_rendimento_plotar
            lista_itens_caminhao = lista_teste
    print("Melhor caminho: " + str(melhor_caminho))
    print("Custo total distância: " + str(melhor_custo))
    print("Itens caminhão: " + str(lista_itens_caminhao))
    plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_caminhao)

def plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_caminhao):
    fig, ax = plt.subplots(figsize=(10, 8))
    xC = []
    yC = []

    for loja_id, loja_info in lojas.items():
        x_coord, y_coord, _ = loja_info  
        xC.append(x_coord)
        yC.append(y_coord)

    plt.scatter(xC, yC)

    def update(frame):
        time.sleep(0.5)
        ax.clear()
        ax.scatter(xC, yC)
        
        # Atualize o caminho percorrido no gráfico
        x = [lojas[loja][0] for loja in melhor_caminho[:frame+1]]
        y = [lojas[loja][1] for loja in melhor_caminho[:frame+1]]
        ax.plot(x, y, 'bo-')

        # Adicione o índice da loja aos pontos
        for i, (xi, yi) in enumerate(zip(x, y)):
            ax.text(xi, yi, str(melhor_caminho[i]), ha='center', va='bottom')

        # Atualize o gasto de combustível
        gasto_combustivel = sum(lista_melhor_custo[:frame])
        ax.set_title(f"Gasto de Combustível: {gasto_combustivel:.2f} L")

        ax.set_xlabel("Coordenada X")
        ax.set_ylabel("Coordenada Y")
        ax.set_xlim(min(lojas.values(), key=lambda x: x[0])[0] - 10, max(lojas.values(), key=lambda x: x[0])[0] + 10)
        ax.set_ylim(min(lojas.values(), key=lambda x: x[1])[1] - 10, max(lojas.values(), key=lambda x: x[1])[1] + 10)

        # Adicione a legenda com o índice do array lista_itens_caminhao
        if frame < len(lista_itens_caminhao):
            legenda = f"Produtos no caminhão: {lista_itens_caminhao[frame]}"
            ax.text(0.5, -0.1, legenda, transform=ax.transAxes, ha='center', fontsize=12)

    anim = animation.FuncAnimation(fig, update, frames=len(melhor_caminho), interval=500) # Cria a animação frame por frame
    plt.show()

def branchAndBound(filename, k_produtos):
    print("Branch and bound")
