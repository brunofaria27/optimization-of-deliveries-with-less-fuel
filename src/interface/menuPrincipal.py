# Bibliotecas do python
import PySimpleGUI as sg

# Funções importadas do próprio projeto
import solutions.algoritmos as algo

sg.theme('LightGray1') 
layout = [
    [sg.Text("OTIMIZAÇÃO DE ENTREGAS", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [sg.Text("Bruno Faria, Lucas de Paula, Maria Luísa Tomich Raso", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [sg.Text("-----------------------------------------------------------------------------", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [sg.Text(" ", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [[sg.Text("ESCOLHA ARQUIVO DE ENTRADA: ", font=("Helvetica", 15)), sg.FileBrowse("ESCOLHER", font=("Helvetica", 15), key="-FILEBROWSE-")]],
    [sg.Text("Quantidade de produtos máximo no caminhão: ", font=("Helvetica", 15)), sg.Input(key="-K_PRODUTOS-", font=("Helvetica", 15), size=(10,1), enable_events=True, justification='center', text_color='black', background_color='white')],
    [[sg.Text("ESCOLHA UM DOS ALGORÍTMOS: ", font=("Helvetica", 15)), sg.Button("FORÇA BRUTA", font=("Helvetica", 15)), sg.Button("BRANCH-AND-BOUND", font=("Helvetica", 15))]],
]

janela = sg.Window("TRABALHO 2 - PROJETO E ANÁLISE DE ALGORÍTMOS", layout, size=(1000, 300), text_justification="center", element_justification="center")

while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED or evento == "Cancelar":
        break
    if evento == "FORÇA BRUTA":
        algo.bruteForce(valores["-FILEBROWSE-"], valores["-K_PRODUTOS-"])
    if evento == "BRANCH AND BOUND":
        algo.branchAndBound(valores["-FILEBROWSE-"], valores["-K_PRODUTOS-"])
janela.close()