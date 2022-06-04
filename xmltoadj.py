import sys
from gistfile1 import *

G = read_osm("map.osm.xml")
networkx.write_adjlist(G, "UESB.adjlist")

