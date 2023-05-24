# Bibliotecas do python
import math
import copy

# Funções
import utils.fileTreatment as fileTreatment
import interface.pathPlotting as plotting

# Objetos
from models.List import ListaLimitada

def permutacoes(lojas, k_produtos):
    lojas_filiais = list(lojas.keys())
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação

    melhor_caminho = None
    melhor_custo = float('inf')
    lista_melhor_custo = None
    lista_itens_caminhao = None

    def generate_permutations(lista_lojas, permutacao_atual):
        nonlocal melhor_caminho, melhor_custo, lista_melhor_custo, lista_itens_caminhao # Atribuir valores a variáveis do escopo externo

        if len(lista_lojas) == 0:
            caminho = permutacao_atual + [0]
            itens_caminhao, lojas_copy, lista_rendimento_plotar, lista_teste, caminho = calcula_viagem_total(lojas, caminho, int(k_produtos))
            if itens_caminhao == 0 and verificaProdutosEntregues(lojas_copy):
                custo_viagem = sum(lista_rendimento_plotar)
                if custo_viagem < melhor_custo:
                    melhor_caminho = caminho
                    melhor_custo = custo_viagem
                    lista_melhor_custo = lista_rendimento_plotar
                    lista_itens_caminhao = lista_teste
            return

        for i in range(len(lista_lojas)):
            loja_atual = lista_lojas[i]
            elementos_restantes = lista_lojas[:i] + lista_lojas[i + 1:]
            generate_permutations(elementos_restantes, permutacao_atual + [loja_atual])
    generate_permutations(lojas_filiais, [0])
    return melhor_caminho, lista_melhor_custo, lista_itens_caminhao

def calculate_distance(xA, yA, xB, yB):
    return math.sqrt((xA - xB)**2 + (yA - yB)**2)

def verificaProdutosEntregues(lojas):
    for entregas in lojas.values():
        if entregas[2]:  # Verifica se a lista de entregas da loja não está vazia
            return False
    return True

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
    return len(produtos_pegos), lojas_copy, lista_rendimento_plotar, lista_produtos, caminho

def bruteForce(filename, k_produtos):
    lojas = fileTreatment.load_stores(filename)
    melhor_caminho, lista_melhor_custo, lista_itens_caminhao = permutacoes(lojas, int(k_produtos))
    print("Melhor caminho: " + str(melhor_caminho))
    print("Custo total distância: " + str(sum(lista_melhor_custo)))
    print("Itens caminhão: " + str(lista_itens_caminhao))
    plotting.plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_caminhao)

def branchAndBound(filename, k_produtos):
    print("Branch and bound")
