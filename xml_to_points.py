import xml.etree.ElementTree as ET

file_name = "map.osm.xml"

tree = ET.parse(file_name)

root = tree.getroot()

f=open("map.osm.txt", "w")

for node in root.iter('node'):
    ident = node.attrib['id']
    lat = node.attrib['lat']
    lon = node.attrib['lon']
    f.write("{} {} {}\n".format(ident,lat,lon))
f.close()



