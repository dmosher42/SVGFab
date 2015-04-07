__author__ = 'dee'
#References:
'''
https://docs.python.org/2/library/xml.etree.elementtree.html
https://docs.python.org/2/tutorial/controlflow.html
http://wiki.inkscape.org/wiki/index.php/Inkscape_SVG_vs._plain_SVG
https://docs.python.org/2/library/string.html
http://www.tutorialspoint.com/python/python_lists.htm
https://docs.python.org/2/tutorial/modules.html
'''

filelocation = 'test.svg'

import xml.etree.ElementTree as ET
import sys
#import xml.etree.ElementTree as ET2
#import string as ST
tree = ET.parse(filelocation)
root = tree.getroot()
ns = {'svg':'http://www.w3.org/2000/svg','is':'http://www.inkscape.org/namespaces/inkscape'}

#tree2 = ET.parse('test2.fab')


print(sys.version)

paths = []
points = []

print(root)
for child in root:
    print child.tag

print("=======GET SVG PATHS:======")

for path in root.findall('svg:path',ns):
    points=(str.split(path.get('d')))
    points.pop(0) #remove the M/m
    for i in range(len(points)):
        points[i] = str.split(points[i],",")
    paths.append(points)
    #points.append()

print("=======GET SVG RECTS:======")
#not really needed right now

print("=======GET MAT CONFIG:======")
#not really needed right now. Just use a single, hardcoded one

print("=======MAKE FAB(ULOUS):======")
#root = tree2.getroot()

builder=ET.TreeBuilder()
builder.start('hi', {})
builder.data("some text")
builder.end("hi")

root2 = builder.close()
print(root2.tag)
print ET.tostring(root2)

