# Bibliotecas do python
import math
import copy
import time

# Funções
import utils.deliveryAnalyzer as deliveryAnalyzer
import interface.pathPlotting as plotting

# Objetos
from models.List import ListaLimitada

# Globals
time_start_branch_and_bound = 0
time_end_branch_and_bound = 0

def isRamoValido(loja, produtos_caminhao, entregas):
    for produto in entregas:    # Todos os produtos a serem entregues
        if produto == loja:     # Caso exista entrega para a loja
            if loja in produtos_caminhao:
                return True
            return False
    return True

def destinoProdutoJaEntregue(loja_destino, lista_produtos):
    return loja_destino in lista_produtos

def temProdutosRestantes(lojas_copy, caminho_atual):
    for loja in caminho_atual:
        if loja != 0 and lojas_copy[loja][2]:
            return True
    return False

def verificaProdutosEntregues(lojas):
    for entregas in lojas.values():
        if entregas[2]:  # Verifica se a lista de entregas da loja não está vazia
            return False
    return True

def permutacoesBranchAndBound(lojas, entregas, matriz_distancias, k_produtos):
    PERMUTACOES = 0
    PODAS = 0

    lojas_filiais = list(lojas.keys())
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação

    melhor_caminho = None
    melhor_custo = float('inf')
    lista_melhor_custo = None
    lista_itens_do_caminhao_total_caminho = None

    def generate_permutations(lista_lojas, permutacao_atual):
        nonlocal melhor_caminho, melhor_custo, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS

        if len(lista_lojas) == 0:
            caminho = permutacao_atual + [0]
            PERMUTACOES += 1
            qtd_caminhao, lojas_copy, lista_rendimento_plotar, produtos_caminhao, caminho = calculaViagemTotalBranchAndBound(lojas, caminho, matriz_distancias, int(k_produtos))
            if qtd_caminhao == 0 and verificaProdutosEntregues(lojas_copy):
                custo_viagem_atual = sum(lista_rendimento_plotar)
                if custo_viagem_atual < melhor_custo:
                    melhor_caminho = caminho
                    melhor_custo = custo_viagem_atual
                    lista_melhor_custo = lista_rendimento_plotar
                    lista_itens_do_caminhao_total_caminho = produtos_caminhao
            return

        for i in range(len(lista_lojas)):
            loja_atual = lista_lojas[i]
            elementos_restantes = lista_lojas[:i] + lista_lojas[i + 1:]
            _, _, rendimento_viagem, produtos_caminhao, _  = calculaViagemTotalBranchAndBound(lojas, permutacao_atual + [loja_atual], matriz_distancias, int(k_produtos))
            lower_bound_atual = sum(rendimento_viagem)
            if isRamoValido(loja_atual, produtos_caminhao[-1], entregas):
                if lower_bound_atual < melhor_custo:
                    generate_permutations(elementos_restantes, permutacao_atual + [loja_atual])
                else: PODAS += 1
            else: PODAS += 1
    generate_permutations(lojas_filiais, [0])
    return melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS

def calculaViagemTotalBranchAndBound(lojas, caminho, matriz_distancias, k_produtos):
    lista_rendimento_plotar = []
    lista_de_produtos = []

    produtos_pegos = ListaLimitada(k_produtos)
    lojas_copy = copy.deepcopy(lojas)
    rendimento = 10

    for loja in range(len(caminho) - 1):
        if caminho[loja] != 0:
            produtos_loja = lojas_copy[caminho[loja]][2].copy()

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
                
        distancia = matriz_distancias[caminho[loja]][caminho[loja + 1]]
        lista_rendimento_plotar.append(distancia / rendimento)
        lista_de_produtos.append(produtos_pegos.lista.copy())
    return len(produtos_pegos), lojas_copy, lista_rendimento_plotar, lista_de_produtos, caminho

def branchAndBound(filename, k_produtos):
    lojas, lista_de_produtos = deliveryAnalyzer.load_stores(filename)
    k_valido = deliveryAnalyzer.pegarNumeroMaximoLojas(lojas)
    if int(k_produtos) < k_valido or int(k_produtos) >= 20:
        raise ValueError(f'Valor de K deve ser {k_valido} >= K < 20')
    time_start_branch_and_bound = time.time() # Inicio da execução branch and bound
    matriz_distancias = deliveryAnalyzer.preCalcularMatrizDistancias(lojas)
    melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS = permutacoesBranchAndBound(lojas, lista_de_produtos, matriz_distancias, int(k_produtos))
    time_end_branch_and_bound = time.time() # Fim da execução branch and bound
    print("Melhor caminho: " + str(melhor_caminho))
    print("Custo total distância: " + str(sum(lista_melhor_custo)))
    print("Itens caminhão: " + str(lista_itens_do_caminhao_total_caminho))
    print("Número de permutações BRANCH AND BOUND: " + str(PERMUTACOES))
    print("Número de podas BRANCH AND BOUND: " + str(PODAS))
    print("Tempo de execução: " + str(time_end_branch_and_bound - time_start_branch_and_bound))
    print("Podas por seg: " + str(PODAS / (time_end_branch_and_bound - time_start_branch_and_bound)))
    plotting.plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho)