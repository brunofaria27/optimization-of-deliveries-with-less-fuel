# Bibliotecas do python
import itertools
import math

# Funções importadas do próprio projeto
import solutions.utils_solutions as utils # Funções que serão usadas tanto no força bruta e no branch and bound

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
    distancia_total = 0
    produtos_pegos = ListaLimitada(k_produtos)
    rendimento = 10
    rendimento_total = 0

    for loja in range(len(caminho) - 1):
        if caminho[loja] != 0:
            produtos_loja = lojas[caminho[loja]][2].copy()

            if len(produtos_loja) != []:
                for produto in produtos_loja:
                    produtos_pegos.adicionar(produto)
                    rendimento -= 0.5
                produtos_loja.clear()
                
            # Verificar se tem entrega
            if caminho[loja] in produtos_pegos.lista:
                for entrega in produtos_pegos.lista.copy():
                    if entrega == caminho[loja]:
                        produtos_pegos.remover_por_valor(caminho[loja])
                        rendimento += 0.5

        xA, yA = lojas[caminho[loja]][0], lojas[caminho[loja]][1]
        xB, yB = lojas[caminho[loja + 1]][0], lojas[caminho[loja + 1]][1]
        distancia = calculate_distance(xA, yA, xB, yB)
        rendimento_total += distancia / rendimento
        distancia_total += distancia
        produtos_caminhao = len(produtos_pegos)
    return rendimento_total, distancia_total, produtos_caminhao

def bruteForce(filename, k_produtos):
    lojas = utils.load_stores(filename)
    possiveis_caminhos = generate_permutations(lojas)
    melhor_caminho = None
    melhor_custo = float('inf')
    melhor_distancia = None
    for caminho in possiveis_caminhos:
        custo_viagem, distancia_total, itens_caminhao = calcula_viagem_total(lojas, caminho, int(k_produtos))
        if itens_caminhao == 0 and custo_viagem < melhor_custo:
            melhor_caminho = caminho
            melhor_distancia = distancia_total
            melhor_custo = custo_viagem
    print("Melhor caminho: " + str(melhor_caminho))
    print("Distância total: " + str(melhor_distancia))
    print("Custo total distância: " + str(melhor_custo))
        
def branchAndBound(filename, k_produtos):
    print("Branch and bound")

# 10 KM/L
# 1 PRODUTO = 9.5 KM/L
# 10 PRODUTOS = 5 KM/L
# 100KM / 5KM/L = 20 L -> DISTANCIA / GASTO DO CAMINHAO (10 - (0.5  * QUANTIDADE DE ITENS NO CAMINHÃO)) = LITROS GASTOS
