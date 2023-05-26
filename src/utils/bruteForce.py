# Bibliotecas do python
import math
import copy
import time

# Funções
import utils.fileTreatment as fileTreatment
import interface.pathPlotting as plotting

# Objetos
from models.List import ListaLimitada

# Globals
PERMUTACOES = list()
time_start_bruteforce = 0
time_end_bruteforce = 0

def calculaDistancia(xA, yA, xB, yB):
    return math.sqrt((xA - xB)**2 + (yA - yB)**2)

def verificaProdutosEntregues(lojas):
    for entregas_da_loja in lojas.values():
        if entregas_da_loja[2]:  # Verifica se a lista de entregas da loja não está vazia
            return False
    return True

def permutacoes(lojas, k_produtos):
    lojas_filiais = list(lojas.keys())
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação

    melhor_caminho = None
    melhor_custo = float('inf')
    lista_melhor_custo = None
    lista_itens_do_caminhao_total_caminho = None

    def generate_permutations(lista_lojas, permutacao_atual):
        nonlocal melhor_caminho, melhor_custo, lista_melhor_custo, lista_itens_do_caminhao_total_caminho # Atribuir valores a variáveis do escopo externo


# itens caminhão = quantidade de itens do caminhão do ultimo ponto para a volta a origem
#  lista_itens_caminhao = todo o log de itens pegos durante o caminho

        if len(lista_lojas) == 0:
            caminho = permutacao_atual + [0]
            PERMUTACOES.append(caminho)
            itens_caminhao_volta_origem, lojas_copy, lista_rendimento_plotar, lista_itens_caminhao_teste_de_custo, caminho = calculaViagemTotal(lojas, caminho, int(k_produtos))
            if itens_caminhao_volta_origem == 0 and verificaProdutosEntregues(lojas_copy):
                custo_viagem_atual = sum(lista_rendimento_plotar)
                if custo_viagem_atual < melhor_custo:
                    melhor_caminho = caminho
                    melhor_custo = custo_viagem_atual
                    lista_melhor_custo = lista_rendimento_plotar
                    lista_itens_do_caminhao_total_caminho = lista_itens_caminhao_teste_de_custo
            return

        for i in range(len(lista_lojas)):
            loja_atual = lista_lojas[i]
            elementos_restantes = lista_lojas[:i] + lista_lojas[i + 1:]
            generate_permutations(elementos_restantes, permutacao_atual + [loja_atual])
    generate_permutations(lojas_filiais, [0])
    return melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho

def calculaViagemTotal(lojas, caminho, k_produtos):
    lista_rendimento_plotar = list()
    lista_de_produtos = list()

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
        distancia = calculaDistancia(xA, yA, xB, yB)
        lista_rendimento_plotar.append(distancia / rendimento)
        lista_de_produtos.append(produtos_pegos.lista.copy())
    return len(produtos_pegos), lojas_copy, lista_rendimento_plotar, lista_de_produtos, caminho

def bruteForce(filename, k_produtos):
    PERMUTACOES.clear()
    time_start_bruteforce = time.time() # Inicio da execução brute force
    lojas, _ = fileTreatment.load_stores(filename)
    melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho = permutacoes(lojas, int(k_produtos))
    time_end_bruteforce = time.time() # Fim da execução brute force
    print("Melhor caminho: " + str(melhor_caminho))
    print("Custo total distância: " + str(sum(lista_melhor_custo)))
    print("Itens caminhão: " + str(lista_itens_do_caminhao_total_caminho))
    print("Número de permutações BRUTE FORCE: " + str(len(PERMUTACOES)))
    print("Tempo de execução: " + str(time_end_bruteforce - time_start_bruteforce))
    plotting.plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_do_caminhao_total_caminho)