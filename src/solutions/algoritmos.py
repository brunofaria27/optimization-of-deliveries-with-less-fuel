# Bibliotecas do python

# Funções importadas do próprio projeto
import solutions.utils_solutions as utils # Funções que serão usadas tanto no força bruta e no branch and bound

RENDIMENTO_LITRO = 10

def bruteForce(filename, k_produtos):
    print(utils.load_stores(filename))
    print(int(k_produtos))

def branchAndBound(filename, k_produtos):
    print("Branch and bound")