from os import remove
from tkinter import Button
import matplotlib.pyplot as plt
from grafo import Graph
import re

from collections import defaultdict

from haversine import haversine, Unit
from matplotlib.backend_bases import MouseButton    
    
g = Graph()
# busca o arquivo na pasta do projeto




file_vertex = "map.osm.txt"
file_edges = "uesb.adjlist"
plot_ponts = "map.osm.txt"




with open(file_vertex) as fp:  # abre o arquivo e garante seu fechamento
    for line in fp:
        points = re.findall(r'[-+]?\d+.\d+', line)
        g.add_vertex(points[0], float(points[1]), float(points[2]))
               

# adiciona as conexões do grafo

def calc_dist(de, para):
   
      start = (de.lat, de.lon)
      end = (para.lat, de.lon)
      weight = haversine(start, end, unit = Unit.METERS)
      return weight



with open(file_edges) as fp:
    for line in fp:
        points = re.findall(r'[-+]?\d+', line)
        
        for point in points[1:]:
            deVertex = g.get_vertex(points[0])
            tamanho = points
            pointVertex = g.get_vertex(point)
            g.add_edge(tamanho[0], point, haversine((deVertex.lat, deVertex.lon), (pointVertex.lat, pointVertex.lon)))
                    

with open(plot_ponts) as fp:
    x = list()
    y = list()
    for i in g.get_edges():
        x.append(g.get_vertex(i[0]).lat)
        y.append(g.get_vertex(i[0]).lon)

    print("X :",x,"Y: ",y)


def vertex_mais_proximo_do_click(event):
    menor = 1e309

    for i in g.get_edges(): # Pega as arestas
        vertex = g.get_vertex(i[0]) # pega os vertex do grafo
        menor_valor = haversine((event[0], event[1]), (float(vertex.lat), float(vertex.lon)))
        if menor_valor < menor:  # verifica qual o ponto de mais próximo do click
            menor = menor_valor
            point = vertex.id # pega o id da vertex no mapa

    return point

def onclick(event, clickx=list(),clicky=list(), ponto=list()):

    if event.button is MouseButton.LEFT: # faz o button ter uma identidade do mouse

        if event.xdata is None and event.xdata is None: # tratamento caso click no branco
            return

        click = list()
        click.append(event.xdata)
        click.append(event.ydata)

        ponto.append(vertex_mais_proximo_do_click(click))
        #print(event.xdata, event.ydata)
        #print(len(ponto))
        if len(ponto) == 2:

            dist, caminho = g.min_path(ponto[0], ponto[1])
            
            if caminho is not None:
                print(caminho)
                print('Distancia: {} km\n'.format(round(dist,3)))
                

                for i in caminho:
                    clickx.append(g.get_vertex(i).lat)
                    clicky.append(g.get_vertex(i).lon)

                l = ax.plot(clickx,clicky, "r")
                fig.canvas.draw()
                l.pop(0).remove()
            else:
                print("Indisponivel")

            ponto.clear()
            clickx.clear()
            clicky.clear()
         
      

fig, ax = plt.subplots()
p, = plt.plot(x, y, 'o')
fig.canvas.mpl_connect('button_press_event', onclick)  # adiciona o evento
plt.show()
