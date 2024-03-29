# Ciências da Computação - Projeto e Análise de Algoritmos
# Bruno Faria - 742238
# Lucas de Paula - 727840
# Maria Luisa Raso - 698215

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
            if loja in produtos_caminhao: #confere se tem o produto daquela loja no caminhao
                return True
            return False
    return True

def verificaProdutosEntregues(lojas):
    for entregas in lojas.values():
        if entregas[2]:  # Verifica se a lista de entregas da loja não está vazia
            return False
    return True

def permutacoesBranchAndBoundAlternativo(lojas, entregas, matriz_distancias, k_produtos_caminhao):
    PERMUTACOES = 0
    PODAS = 0

    lojas_filiais = list(lojas.keys()) #ids das lojas
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação
    lojas_lb = copy.deepcopy(lojas)
    del lojas_lb[0]

    melhor_caminho = None
    melhor_custo = float('inf')
    lista_melhor_custo = None
    lista_itens_do_caminhao_total_caminho = None #tudo zerado, para ser substituido depois

    def generate_permutations(lista_lojas, permutacao_atual, lojas_lb, ultimo_rendimento):
        nonlocal melhor_caminho, melhor_custo, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS

        if len(lista_lojas) == 0:
            caminho = permutacao_atual + [0]
            PERMUTACOES += 1 #controle de quantidade de permutacoes
            qtd_caminhao, lojas_copy, lista_rendimento_plotar, produtos_caminhao, caminho = calculaViagemTotalBranchAndBound(lojas, caminho, matriz_distancias, int(k_produtos_caminhao), ultimo_rendimento)
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
            _, _, consumo_combustivel_atual, produtos_caminhao, _  = calculaViagemTotalBranchAndBound(lojas, permutacao_atual + [loja_atual], matriz_distancias, int(k_produtos_caminhao), ultimo_rendimento)
            if consumo_combustivel_atual is not None: custo_atual = sum(consumo_combustivel_atual)
            if consumo_combustivel_atual is not None and (melhor_caminho == None or melhor_custo > custo_atual):
                if isRamoValido(loja_atual, produtos_caminhao[-1], entregas):
                    del lojas_lb[loja_atual]
                    somatorio = deliveryAnalyzer.pegarMenoresArestas(lojas_lb, matriz_distancias)
                    lower_bound = custo_atual + somatorio
                    if lower_bound * (0.95) < melhor_custo:
                        generate_permutations(elementos_restantes, permutacao_atual + [loja_atual], lojas_lb, consumo_combustivel_atual)
                    else: PODAS += 1 #se nao for melhor que o melhor custo, poda ele
                    lojas_lb[loja_atual] = (lojas[loja_atual][0], lojas[loja_atual][1], lojas[loja_atual][2])
                else: PODAS += 1 #se o ramo nao e valido, poda ele
            else: PODAS += 1
    generate_permutations(lojas_filiais, [0], lojas_lb, [[]])
    return melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS

def permutacoesBranchAndBoundNormal(lojas, entregas, matriz_distancias, k_produtos_caminhao):
    PERMUTACOES = 0
    PODAS = 0

    lojas_filiais = list(lojas.keys()) #ids das lojas
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação

    melhor_caminho = None
    melhor_custo = float('inf')
    lista_melhor_custo = None
    lista_itens_do_caminhao_total_caminho = None #tudo zerado, para ser substituido depois

    def generate_permutations(lista_lojas, permutacao_atual, ultimo_rendimento):
        nonlocal melhor_caminho, melhor_custo, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS

        if len(lista_lojas) == 0:
            caminho = permutacao_atual + [0]
            PERMUTACOES += 1
            qtd_caminhao, lojas_copy, lista_rendimento_plotar, produtos_caminhao, caminho = calculaViagemTotalBranchAndBound(lojas, caminho, matriz_distancias, int(k_produtos_caminhao), ultimo_rendimento)
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
            _, _, consumo_combustivel_atual, produtos_caminhao, _  = calculaViagemTotalBranchAndBound(lojas, permutacao_atual + [loja_atual], matriz_distancias, int(k_produtos_caminhao), ultimo_rendimento)
            if consumo_combustivel_atual is not None: lower_bound_atual = sum(consumo_combustivel_atual)
            if consumo_combustivel_atual is not None and (melhor_caminho == None or melhor_custo > lower_bound_atual):
                if isRamoValido(loja_atual, produtos_caminhao[-1], entregas):
                    if lower_bound_atual < melhor_custo: #condicao de poda do branch and bound, usando lower bound
                        generate_permutations(elementos_restantes, permutacao_atual + [loja_atual], consumo_combustivel_atual)
                    else: PODAS += 1 #se nao for melhor que o melhor custo, poda ele
                else: PODAS += 1 #se nao e valido, poda ele
            else: PODAS += 1
    generate_permutations(lojas_filiais, [0], [[]])
    return melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS

def calculaViagemTotalBranchAndBound(lojas, caminho, matriz_distancias, k_produtos_caminhao, ultimo_rendimento):
    lista_rendimento_plotar = []
    lista_de_produtos = []

    produtos_pegos = ListaLimitada(k_produtos_caminhao) #so pode pegar quantidades até o numero k determinado no inicio da execucao
    lojas_copy = copy.deepcopy(lojas)
    rendimento_combustivel = 10 #padrao do problema

    for loja in range(len(caminho) - 1):
        for i in range(len(ultimo_rendimento)):
            try:
                if ultimo_rendimento[i] < lista_rendimento_plotar[i]: return None, None, None, None, None
            except: continue

        if caminho[loja] != 0:
            produtos_loja = lojas_copy[caminho[loja]][2].copy() #copia os produtos da loja, caso ela exista

            # Verificar se tem entrega
            if caminho[loja] in produtos_pegos.lista:
                for entrega in produtos_pegos.lista.copy():
                    if entrega == caminho[loja]:
                        produtos_pegos.remover_por_valor(caminho[loja])
                        rendimento_combustivel += 0.5
            
            # Pegar produtos
            if len(produtos_loja) != []:
                for produto in produtos_loja:
                    if produtos_pegos.adicionar(produto):
                        lojas_copy[caminho[loja]][2].remove(produto)
                        rendimento_combustivel -= 0.5
                    else: return None, None, None, None, None
                produtos_loja.clear()
                
        distancia = matriz_distancias[caminho[loja]][caminho[loja + 1]]
        lista_rendimento_plotar.append(distancia / rendimento_combustivel) #vai colocando o rendimento no grafico
        lista_de_produtos.append(produtos_pegos.lista.copy()) #vai colocando os produtos no grafico
    return len(produtos_pegos), lojas_copy, lista_rendimento_plotar, lista_de_produtos, caminho

def branchAndBound(filename, k_produtos_caminhao, isTriangulacao):
    lojas, lista_de_produtos = deliveryAnalyzer.load_stores(filename)
    k_valido = deliveryAnalyzer.pegarNumeroMaximoLojas(lojas) # o k, numero de itens do caminhao, nunca pode ser maior que o numero de lojas
    if int(k_produtos_caminhao) < k_valido or int(k_produtos_caminhao) >= 20:
        raise ValueError(f'Valor de K deve ser {k_valido} >= K < 20')
    time_start_branch_and_bound = time.time() # Inicio da execução branch and bound
    matriz_distancias = deliveryAnalyzer.preCalcularMatrizDistancias(lojas)
    if isTriangulacao: # flag que determina se vai ser usado o branch and bound normal ou com triangulação
        melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS = permutacoesBranchAndBoundAlternativo(lojas, lista_de_produtos, matriz_distancias, int(k_produtos_caminhao))
    else:
        melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES, PODAS = permutacoesBranchAndBoundNormal(lojas, lista_de_produtos, matriz_distancias, int(k_produtos_caminhao))
    time_end_branch_and_bound = time.time() # Fim da execução branch and bound
    if melhor_caminho != None:
        print("Melhor caminho: " + str(melhor_caminho))
        print("Custo total distância: " + str(sum(lista_melhor_custo)))
        print("Itens caminhão: " + str(lista_itens_do_caminhao_total_caminho))
        print("Número de permutações BRANCH AND BOUND: " + str(PERMUTACOES))
        print("Número de podas BRANCH AND BOUND: " + str(PODAS))
        print("Tempo de execução: " + str(time_end_branch_and_bound - time_start_branch_and_bound))
        print("Podas por seg: " + str(PODAS / (time_end_branch_and_bound - time_start_branch_and_bound)))
    else: print('Entrada inválida, nenhum caminho encontrado.')
    plotting.plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho)
