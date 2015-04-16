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

from xml.etree import ElementTree


import xml.etree.ElementTree as ET
#import sys
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path

#import xml.etree.ElementTree as ET2
#import string as ST
tree = ET.parse(filelocation)
root = tree.getroot()
ns = {'svg':'http://www.w3.org/2000/svg','is':'http://www.inkscape.org/namespaces/inkscape'}

#tree2 = ET.parse('test2.fab')

convunit = .264583
xoffset = 80
yoffset = 50
pointz = 0.390000
dplaces = '%.6f'  #number of decimal places. dplaces % number


def indent(elem, level=0):
    i = "\n" + level*"   "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "   "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


#print(sys.version)

paths = []
points = []

print(root)
for child in root:
    print child.tag

print("=======GET SVG PATHS:======")

points=[]

for path in root.findall('svg:path',ns):
    print(path.get('d'))
    parpath = parse_path(path.get('d'))
    print(len(parpath))
    for i in range(0,len(parpath)):
        pt = []
        pt.append(parpath[i].point(0).real)
        pt.append(parpath[i].point(0).imag)
        points.append(pt)
        print(pt)
    paths.append(points)


'''
    points=(str.split(path.get('d')))
    points.pop(0) #remove the M/m
    for i in range(len(points)):
        points[i] = str.split(points[i],",")
        if "z" in points[i]:
            points.pop()
    paths.append(points)
    #points.append()
'''

print("=======GET SVG RECTS:======")
#not really needed right now
print("=======GET MAT CONFIG:======")
#not really needed right now. Just use a single, hardcoded one

print("=======MAKE FAB(ULOUS):======")
#root = tree2.getroot()



print(points)

#REMINDER: Change to:
#a = ET.Element('a')
#b = ET.SubElement(a, 'b')

builder=ET.TreeBuilder()
fabhpr = ET.fromstring("<fabAtHomePrinter><printAcceleration>100</printAcceleration><materialCalibration><clearance>2</clearance><depositionRate>0.005</depositionRate><name>epoxy</name><pathSpeed>5</pathSpeed><pathWidth>1</pathWidth><pausePaths>30</pausePaths><pitch>0.000397</pitch><pushout>0.3</pushout><suckback>0.25</suckback><suckbackDelay>0</suckbackDelay></materialCalibration><materialCalibration><clearance>1</clearance><depositionRate>0.00085</depositionRate><name>silicone</name><pathSpeed>9</pathSpeed><pathWidth>0.4</pathWidth><pausePaths>300</pausePaths><pitch>0.000397</pitch><pushout>0.11</pushout><suckback>0.11</suckback><suckbackDelay>0</suckbackDelay></materialCalibration></fabAtHomePrinter>")
indent(fabhpr)

for j in range(len(paths)):
    print(paths[j])
    builder.start('path', {})
    builder.end("path")
    pathr = builder.close()

    pathr.insert(0,ET.fromstring("<materialCalibrationName>epoxy</materialCalibrationName>"))

    for i in range(len(paths[j])):
        print(paths[j][i])
        builder.start('point', {})
        builder.end("point")
        pointr = builder.close()

        builder.start('x', {})
        builder.data(str(float(paths[j][i][0])*convunit+xoffset))
        builder.end("x")
        xr = builder.close()

        builder.start('y', {})
        builder.data(str(float(paths[j][i][1])*convunit++yoffset))
        builder.end("y")
        yr = builder.close()

        builder.start('z', {})
        builder.data(str(dplaces%pointz))
        builder.end('z')
        zr = builder.close()

        pointr.insert(0,xr)
        pointr.insert(1,yr)
        pointr.insert(2,zr)
        pathr.insert(j+i+1,pointr)
    fabhpr.insert(j+3,pathr)
    indent(pathr)



print("\n\nDEBUGTIME")

for der in fabhpr:
    print(der.tag)
print ET.tostring(fabhpr)

print(pathr.tag)
indent(pathr)

print ET.tostring(pathr)
fulltree=ET.ElementTree(fabhpr)
#The tree is initialized with the contents of the XML file if given.


fulltree.write("page.fab",
           xml_declaration=True,encoding='utf-8',
           method="xml")
