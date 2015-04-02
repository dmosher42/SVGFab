__author__ = 'dee'
import xml.etree.cElementTree as ET
#import string as ST
tree = ET.parse('test.svg')
root = tree.getroot()
ns = {'svg':'http://www.w3.org/2000/svg','is':'http://www.inkscape.org/namespaces/inkscape'}

tree2 = ET.parse('test2.fab')


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
print(paths)

print("=======GET SVG REC:======")



print("=======MAKE FAB(ULOUS):======")
root = tree2.getroot()
for child in root:
    print child.tag
