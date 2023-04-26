# Bibliotecas do python
import itertools

# Funções importadas do próprio projeto
import solutions.utils_solutions as utils # Funções que serão usadas tanto no força bruta e no branch and bound

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

def generate_perm(lojas):
    lojas_filiais = list(lojas.keys())
    lojas_filiais.remove(0)  # Origem e destino não entram na permutação
    def generate_permutations_(lista_lojas):
        if len(lista_lojas) <= 1: return [lista_lojas]
        permutacoes = []
        for i in range(len(lista_lojas)):
            elemento_atual = lista_lojas[i]
            elementos_restantes = lista_lojas[:i] + lista_lojas[i + 1:]
            permutacoes_restantes = generate_permutations_(elementos_restantes)
            for perm in permutacoes_restantes:
                permutacoes.append([elemento_atual] + perm)
        return permutacoes
    return generate_permutations_(lojas_filiais)

def bruteForce(filename, k_produtos):
    lojas = utils.load_stores(filename)
    print(len(generate_perm(lojas)))

def branchAndBound(filename, k_produtos):
    print("Branch and bound")