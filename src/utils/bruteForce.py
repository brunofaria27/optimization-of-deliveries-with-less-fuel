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
time_start_bruteforce = 0
time_end_bruteforce = 0

def verificaProdutosEntregues(lojas):
    for entregas_da_loja in lojas.values():
        if entregas_da_loja[2]:  # Verifica se a lista de entregas da loja não está vazia
            return False
    return True

def permutacoesBruteForce(lojas, matriz_distancias, k_produtos):
    PERMUTACOES = 0

    lojas_filiais = list(lojas.keys()) #ids das lojas
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação

    melhor_caminho = None
    melhor_custo = float('inf')
    lista_melhor_custo = None
    lista_itens_do_caminhao_total_caminho = None #tudo zerado, para ser substituido em seguida

    def generate_permutations(lista_lojas, permutacao_atual):
        nonlocal melhor_caminho, melhor_custo, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES # Atribuir valores a variáveis do escopo externo

        if len(lista_lojas) == 0:
            caminho = permutacao_atual + [0]
            PERMUTACOES += 1 #controle de permutacoes
            itens_caminhao_volta_origem, lojas_copy, lista_rendimento_plotar, lista_itens_caminhao_teste_de_custo, caminho = calculaViagemTotalBruteForce(lojas, caminho, matriz_distancias, int(k_produtos))
            if itens_caminhao_volta_origem == 0 and verificaProdutosEntregues(lojas_copy):
                custo_viagem_atual = sum(lista_rendimento_plotar)
                if custo_viagem_atual < melhor_custo:
                    melhor_caminho = caminho
                    melhor_custo = custo_viagem_atual
                    lista_melhor_custo = lista_rendimento_plotar
                    lista_itens_do_caminhao_total_caminho = lista_itens_caminhao_teste_de_custo #atualiza os valores caso seja o melhor
            return

        for i in range(len(lista_lojas)):
            loja_atual = lista_lojas[i]
            elementos_restantes = lista_lojas[:i] + lista_lojas[i + 1:]
            generate_permutations(elementos_restantes, permutacao_atual + [loja_atual]) #chama a permutacao para todos os casos
    generate_permutations(lojas_filiais, [0])
    return melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES

def calculaViagemTotalBruteForce(lojas, caminho, matriz_distancias, k_produtos):
    lista_rendimento_plotar = list()
    lista_de_produtos = list()

    produtos_pegos = ListaLimitada(k_produtos) #nao pode ser maior que o k definido no inicio do programa
    lojas_copy = copy.deepcopy(lojas)
    rendimento_combustivel = 10 #padrao do problema

    for loja in range(len(caminho) - 1):
        if caminho[loja] != 0:
            produtos_loja = lojas[caminho[loja]][2].copy()

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
                produtos_loja.clear()
                
        distancia = matriz_distancias[caminho[loja]][caminho[loja + 1]]
        lista_rendimento_plotar.append(distancia / rendimento_combustivel)
        lista_de_produtos.append(produtos_pegos.lista.copy())
    return len(produtos_pegos), lojas_copy, lista_rendimento_plotar, lista_de_produtos, caminho

def bruteForce(filename, k_produtos):
    lojas, _ = deliveryAnalyzer.load_stores(filename)
    k_valido = deliveryAnalyzer.pegarNumeroMaximoLojas(lojas) #k nao pode ser maior que o numero de lojas
    if int(k_produtos) < k_valido or int(k_produtos) >= 20:
        raise ValueError(f'Valor de K deve ser {k_valido} >= K < 20')
    time_start_bruteforce = time.time() # Inicio da execução brute force
    matriz_distancias = deliveryAnalyzer.preCalcularMatrizDistancias(lojas)
    melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho, PERMUTACOES = permutacoesBruteForce(lojas, matriz_distancias, int(k_produtos))
    time_end_bruteforce = time.time() # Fim da execução brute force
    if melhor_caminho != None:
        print("Melhor caminho: " + str(melhor_caminho))
        print("Custo total distância: " + str(sum(lista_melhor_custo)))
        print("Itens caminhão: " + str(lista_itens_do_caminhao_total_caminho))
        print("Número de permutações BRUTE FORCE: " + str(PERMUTACOES))
        print("Tempo de execução: " + str(time_end_bruteforce - time_start_bruteforce))
    else: print('Entrada inválida, nenhum caminho encontrado.')
    plotting.plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho)