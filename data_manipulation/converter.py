import os
import pickle
import xml.etree.ElementTree as ET
path = 'output/xmls'
files = os.listdir(path)
datas = []
for f in files:
    root = ET.parse(os.path.join(path,f)).getroot()
    boxes = []
    for word in root.findall('.//word'):
        attr = word.attrib
        x1,y1,x2,y2 = attr['x1'],attr['y1'],attr['x2'],attr['y2']
        x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
        bbox = [x1,y1,x2,y2]
        text = word.text
        boxes.append([x1,y1,x2,y1,x2,y2,x1,y2,text])
    
    datas.append([f.split('/')[-1][:-3]+'png', boxes])

pickle.dump(datas, open('word.pkl', 'wb'))
