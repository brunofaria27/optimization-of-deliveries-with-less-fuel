# Ciência da Computação - Projeto e Análise de Algoritmos
# Bruno Faria - 
# Lucas de Paula - 
# Maria Luisa Raso - 698215

import PySimpleGUI as sg # Importar o módulo PySimpleGUI para o GUI

import src.interfaceInicial as interfaceInicial # Importar o módulo próprio do GUI

layout = [ ]

def main():

    window = sg.Window('Trabalho 1 - Ciência da Computação', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'exit':
            break
        elif event == 'interfaceInicial':
            interfaceInicial.main()