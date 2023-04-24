# Bibliotecas do python

# Funções importadas do próprio projeto
import solutions.utils_solutions as utils # Funções que serão usadas tanto no força bruta e no branch and bound

RENDIMENTO_LITRO = 10

def generate_permutations(lojas):
    def helper(current_permutation, remaining_lojas):
        if len(remaining_lojas) == 0:
            return [current_permutation + [0]]
        permutations = []
        for i, loja_id in enumerate(remaining_lojas):
            next_permutation = current_permutation + [loja_id]
            next_remaining = remaining_lojas[:i] + remaining_lojas[i+1:]
            permutations.extend(helper(next_permutation, next_remaining))
        return permutations
    loja_ids = list(lojas.keys())[1:]  # remove a loja 0
    return helper([0], loja_ids)

def bruteForce(filename, k_produtos):
    lojas = utils.load_stores(filename)
    print(len(generate_permutations(lojas)))

def branchAndBound(filename, k_produtos):
    print("Branch and bound")