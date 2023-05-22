# Bibliotecas do python
import itertools
import math
import copy
import matplotlib

# Funções
import solutions.utils_solutions as utils # Funções que serão usadas tanto no força bruta e no branch and bound

# Objetos
from models.List import ListaLimitada

def generate_permutations_first_products(lojas):
    lojas_sem_lista = list(lojas.keys())

    lojas_com_lista = []
    for loja in lojas_sem_lista:
        if lojas[loja][2]:
            lojas_com_lista.append(loja)

    lojas = list(lojas.keys())
    lojas.remove(0)
    caminho = [0]
    permutacoes = []
    for loja_com_lista in lojas_com_lista:
        lojas.remove(loja_com_lista)
        caminho.append(loja_com_lista)
        for perm in itertools.permutations(lojas):
            permutacoes.append(caminho + list(perm) + [0])
        caminho.pop()
        lojas.append(loja_com_lista)
    return permutacoes # Número de lojas - 2 = N * Número de lojas com lista = Quantidade de caminhos possiveis

def generate_permutations(lojas):
    permutacoes = []
    lojas_filiais = list(lojas.keys())
    lojas_filiais.remove(0) # Origem e destino não entra na permutação
    for perm in itertools.permutations(lojas_filiais):
        permutacoes.append([0] + list(perm) + [0])
    return permutacoes # Quantidade de caminhos possiveis = (len(lojas) - 1)!

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
    produtos_pegos = ListaLimitada(k_produtos)
    lojas_copy = copy.deepcopy(lojas)
    rendimento = 10

    lista_rendimento_plotar = list()
    lista_distancia_plotar = list()

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
        lista_distancia_plotar.append(distancia)
    return lista_rendimento_plotar, lista_distancia_plotar, len(produtos_pegos), lojas_copy

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
    lista_melhor_distancia = None

    for caminho in possiveis_caminhos:
        lista_custo_viagem, lista_distancia_total, itens_caminhao, lojas_copy = calcula_viagem_total(lojas, caminho, int(k_produtos))
        custo_total = sum(lista_custo_viagem) # Somar todos custos de cada parte do caminho (gasolina)
        if itens_caminhao == 0 and custo_total < melhor_custo and verificaProdutosEntregues(lojas_copy):
            melhor_caminho = caminho
            lista_melhor_custo = lista_custo_viagem
            lista_melhor_distancia = lista_distancia_total
    plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_melhor_distancia)

def plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_melhor_distancia):
    return
        
def branchAndBound(filename, k_produtos):
    print("Branch and bound")
