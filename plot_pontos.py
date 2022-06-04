from os import remove
from tkinter import Button
import matplotlib.pyplot as plt
import numpy as np
import re

from collections import defaultdict
from vertex_mapa import Vertex
from haversine import haversine, Unit
from grafo import Graph
from matplotlib.backend_bases import MouseButton


g = Graph()
coordenadasX = []
coordenadasY = []
path = None

file_name = "map.osm.txt"
fig = plt.figure()

ax = fig.add_subplot(1,1,1)


with open(file_name) as fp:
    for line in fp:
        
        points = re.findall(r'[-+]?\d+.\d+', line)
        key = int(points[0])
        lat = float(points[1])
        lon = float(points[2])
        g.add_vertex(key, lat, lon)
        
        ax.plot(float(points[1]), float(points[2]), "ro")


def calc_dist(de, para):
   
      start = (de.lat, de.lon)
      end = (para.lat, de.lon)
      weight = haversine(start, end, unit = Unit.METERS)
      return weight
  
file_name = "uesb.adjlist"
with open(file_name) as fp:
    for line in fp:
        points = re.findall(r'[-+]?\d+', line)
        de = int(points[0])
        deVertex = g.get_vertex(de)
        for point in points[1:]:
            point = int(point)
            pointVertex = g.get_vertex(point)
            g.add_edge(de, point, calc_dist(deVertex, pointVertex))
          
            

def vertex_mais_proximo_do_click(event):
    
    
    file_name = "map.osm.txt"
    print(event)
    id = 0
    ix, iy = float(event[0]), float(event[1])
    #ix, iy = float(event.xdata), float(event.ydata)
    menor = 1e309
    with open(file_name) as fp:
        for line in fp:
            point = re.findall(r'[-+]?\d+.\d+', line)
            menor_valor= haversine((ix, iy),(float(point[1]),float(point[2])))
            if menor>menor_valor:
                menor = menor_valor
                id = int(point[0])
    print(menor, id)
    return menor
         

def onclick(event, clickx=list(),clicky=list(), ponto=list()):

    if event.button is MouseButton.LEFT: # faz o button ter uma identidade do mouse

        if event.xdata is None and event.xdata is None: # tratamento caso click no branco
            return

        click = list()
        click.append(event.xdata)
        click.append(event.ydata)

        ponto.append(vertex_mais_proximo_do_click(click))

        print(len(ponto))
        print(event.xdata, event.ydata)
        if len(ponto) == 2:

            dist, caminho = g.min_path(ponto[0], ponto[1])

            if caminho is not None:
                print(caminho)
                print('Distancia: {} km\n'.format(round(dist,3)))
                for i in caminho:
                    clickx.append(g.get_vertex(i).lat)
                    clicky.append(g.get_vertex(i).lon)

                l = ax.plot(clickx,clicky, "g")
                fig.canvas.draw()
                l.pop(0).remove()
            else:
                print("Indisponivel")

            ponto.clear()
            clickx.clear()
            clicky.clear()

            



          
      
 

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
