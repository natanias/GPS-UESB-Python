import math
import re
import plot_pontos as g
from collections import defaultdict
import matplotlib.pyplot as plt
from haversine import haversine, Unit

def onclick(event, clickx=list(),clicky=list()):

    if event.xdata is not None and event.ydata is not None:

        

        click = list()
        click.append(event.xdata)
        click.append(event.ydata)

        ponto = vertex_mais_proximo_do_click(click)

        if len(ponto) == 2:

            dist, caminho = g.min_path(ponto[1], ponto[2])

            if caminho is not None:
                print(caminho)
                print('Distancia: {} km\n'.format(round(dist,3)))
                for i in caminho:
                    clickx.append(g.get_vertex(i).lat)
                    clicky.appende(g.get_vertex(i).long)

                plt.plot(clickx,clicky, "r")

                fig.canvas.draw()

            
      

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
