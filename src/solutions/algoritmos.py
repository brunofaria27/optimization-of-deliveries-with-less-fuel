# Bibliotecas do python

# Funções importadas do próprio projeto
import solutions.utils_solutions as utils # Funções que serão usadas tanto no força bruta e no branch and bound

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

def bruteForce(filename, k_produtos):
    lojas = utils.load_stores(filename)
    print(permutacoes(lojas))

def branchAndBound(filename, k_produtos):
    print("Branch and bound")