import PySimpleGUI as sg

sg.theme('LightGray1') 
layout = [
    [sg.Text("TRABALHO 1 - PROJETO E ANÁLISE DE ALGORÍTMOS")],
    [sg.Text("-----------------------------------------------------------------------------")],
    [[sg.Text("ESCOLHA ARQUIVO DE ENTRADA: "), sg.FileBrowse("ESCOLHER")]],
    [sg.Button("FORÇA BRUTA")],
    [sg.Button("BRANCH-AND-BOUND")],
]

janela = sg.Window("TRABALHO 1 - PROJETO E ANÁLISE DE ALGORÍTMOS", layout, size=(500, 200))

while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED or evento == "Cancelar":
        break
    if evento == "FORÇA BRUTA":
        print()
        # import src.forcaBruta as forcaBruta
        # forcaBruta.main()
    if evento == "BRANCH AND BOUND":
        print()
        # import src.branchAndBound as branchAndBound   
        # branchAndBound.main()

janela.close()