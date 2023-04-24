import PySimpleGUI as sg

sg.theme('LightGray1') 
layout = [
    [sg.Text("OTIMIZAÇÃO DE ENTREGAS", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [sg.Text("Bruno Faria, Lucas de Paula, Maria Luísa Tomich Raso", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [sg.Text("-----------------------------------------------------------------------------", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [sg.Text(" ", size=(90, 1), justification='center', font=("Helvetica", 15))],
    [[sg.Text("ESCOLHA ARQUIVO DE ENTRADA: ", font=("Helvetica", 15)), sg.FileBrowse("ESCOLHER", font=("Helvetica", 15))]],
    [[sg.Text("ESCOLHA UM DOS ALGORÍTMOS: ", font=("Helvetica", 15)), sg.Button("FORÇA BRUTA", font=("Helvetica", 15)), sg.Button("BRANCH-AND-BOUND", font=("Helvetica", 15))]],
]

janela = sg.Window("TRABALHO 2 - PROJETO E ANÁLISE DE ALGORÍTMOS", layout, size=(900, 250), text_justification="center", element_justification="center")

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