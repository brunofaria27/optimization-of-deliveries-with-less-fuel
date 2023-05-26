import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plotBestTrip(lojas, melhor_caminho, lista_melhor_custo, lista_itens_caminhao):
    fig, ax = plt.subplots(figsize=(10, 8))
    xC = []
    yC = []

    for loja_info in lojas.items():
        x_coord, y_coord, _ = loja_info  
        xC.append(x_coord)
        yC.append(y_coord)

    plt.scatter(xC, yC)

    def update(frame):
        time.sleep(0.5)
        ax.clear()
        ax.scatter(xC, yC)
        
        # Atualize o caminho percorrido no gráfico
        x = [lojas[loja][0] for loja in melhor_caminho[:frame+1]]
        y = [lojas[loja][1] for loja in melhor_caminho[:frame+1]]
        ax.plot(x, y, 'bo-')

        # Adicione o índice da loja aos pontos
        for i, (xi, yi) in enumerate(zip(x, y)):
            ax.text(xi, yi, str(melhor_caminho[i]), ha='center', va='bottom')

        # Atualize o gasto de combustível
        gasto_combustivel = sum(lista_melhor_custo[:frame])
        ax.set_title(f"Gasto de Combustível: {gasto_combustivel:.2f} L")

        ax.set_xlabel("Coordenada X")
        ax.set_ylabel("Coordenada Y")
        ax.set_xlim(min(lojas.values(), key=lambda x: x[0])[0] - 10, max(lojas.values(), key=lambda x: x[0])[0] + 10)
        ax.set_ylim(min(lojas.values(), key=lambda x: x[1])[1] - 10, max(lojas.values(), key=lambda x: x[1])[1] + 10)

        # Adicione a legenda com o índice do array lista_itens_caminhao
        if frame < len(lista_itens_caminhao):
            legenda = f"Produtos no caminhão: {lista_itens_caminhao[frame]}"
            ax.text(0.5, -0.1, legenda, transform=ax.transAxes, ha='center', fontsize=12)
    anim = animation.FuncAnimation(fig, update, frames=len(melhor_caminho), interval=500) # Cria a animação frame por frame
    plt.show()