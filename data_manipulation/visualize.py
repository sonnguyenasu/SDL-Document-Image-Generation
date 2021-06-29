import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image, ImageDraw, ImageFont
import sys, os
from tqdm import tqdm
import json
# i = sys.argv[1]
comp = sys.argv[1]
imgs = []
comps = {
    'paragraph': 0,
    'char': 1,
    'word': 2,
    'line': 3,
    'cell': 4,
    'table': 5,
    'figure': 6,
    'formula': 1,
    'title': 2,
    'plot': 3
}
if comp == 'all':
    compz = ['paragraph','table','figure','formula', 'title','plot']
else: 
    compz = [comp]
colors = [(0,255,0,64),(255,0,0,64),(0,0,255,64),(0,255,255,64),
        (255,0,255,64),(255,255,0,128),(64,64,64,150)]
font=ImageFont.truetype('assets/fonts/regular/arial.ttf',30)
# colors = ['green','red','pink','orange','blue','yellow','black']
def to_xml(fname: str):
    f = json.load(open(f'.//output/jsons/{fname}.json', 'r'))
    im = Image.open(f'.//output/images/{fname}.jpg')
    label = ET.Element('label')
    img_info = ET.SubElement(label, 'info')

    img_info.set('width', f'{im.size[0]}')
    img_info.set('height', f'{im.size[1]}')
    img_info.set('file_name', fname+'.jpg')

    data = ET.SubElement(label, 'data')
    data.set('name','global')
    data.set('x1',str(f['bbox'][0]))
    data.set('y1', str(f['bbox'][1]))
    data.set('x2', str(f['bbox'][2]))
    data.set('y2', str(f['bbox'][3]))
    line_idx = 0
    word_idx = 0
    para_id = 0
    table_id = 0
    figure_id = 0
    formula_id = 0
    title_id = 0
    paras = []
    for _, para in enumerate(f['para']):
        paras.append(para)
    for _, para in enumerate(paras):
        if isinstance(para,list):
            print(fname)
            print(para)
        if para['component'] == 'paragraph':
            para_id += 1
            para_ = ET.SubElement(data, 'paragraph')
            para_.set('name', f'para_{para_id}')
            para_.set('x1', str(para['bbox'][0]))
            para_.set('y1', str(para['bbox'][1]))
            para_.set('x2', str(para['bbox'][2]))
            para_.set('y2', str(para['bbox'][3]))
            for j, line in enumerate(para['lines']):
                line_idx += 1
                line_ = ET.SubElement(para_, f'line')
                line_.set('name', f'line_{line_idx}')
                line_.set('x1', str(line['bbox'][0]))
                line_.set('y1', str(line['bbox'][1]))
                line_.set('x2', str(line['bbox'][2]))
                line_.set('y2', str(line['bbox'][3]))
                for k, word in enumerate(line['words']):
                    word_idx += 1
                    word_ = ET.SubElement(line_, 'word')
                    word_.set('name', f'word_{word_idx}')
                    word_.set('x1', str(word['bbox'][0]))
                    word_.set('y1', str(word['bbox'][1]))
                    word_.set('x2', str(word['bbox'][2]))
                    word_.set('y2', str(word['bbox'][3]))
                    word_.text = word['text']
                    for c in word['cbox']:
                        char_ = ET.SubElement(word_, 'char')
                        char_.set('x1', str(c[0]))
                        char_.set('y1', str(c[1]))
                        char_.set('x2', str(c[2]))
                        char_.set('y2', str(c[3]))
        elif para['component'] == 'natural_image':
            figure_id += 1
            component_ = ET.SubElement(data,'figure')
            component_.set('name',f'figure_{figure_id}')
            component_.set('x1', str(para['bbox'][0]))
            component_.set('y1', str(para['bbox'][1]))
            component_.set('x2', str(para['bbox'][2]))
            component_.set('y2', str(para['bbox'][3]))
        elif para['component'] == 'plot':
            figure_id += 1
            component_ = ET.SubElement(data,'plot')
            component_.set('name',f'figure_{figure_id}')
            component_.set('x1', str(para['bbox'][0]))
            component_.set('y1', str(para['bbox'][1]))
            component_.set('x2', str(para['bbox'][2]))
            component_.set('y2', str(para['bbox'][3]))
        elif para['component'] == 'formula':
            formula_id += 1
            component_ = ET.SubElement(data,'formula')
            component_.set('name',f'formula_{formula_id}')
            component_.set('x1', str(para['bbox'][0]))
            component_.set('y1', str(para['bbox'][1]))
            component_.set('x2', str(para['bbox'][2]))
            component_.set('y2', str(para['bbox'][3]))
        elif para['component'] == 'title':
            # formula_id += 1
            component_ = ET.SubElement(data,'title')
            component_.set('name',f'title_{title_id}')
            component_.set('x1', str(para['bbox'][0]))
            component_.set('y1', str(para['bbox'][1]))
            component_.set('x2', str(para['bbox'][2]))
            component_.set('y2', str(para['bbox'][3]))
            for j, line in enumerate(para['lines']):
                line_idx += 1
                line_ = ET.SubElement(component_, f'line')
                line_.set('name', f'line_{line_idx}')
                line_.set('x1', str(line['bbox'][0]))
                line_.set('y1', str(line['bbox'][1]))
                line_.set('x2', str(line['bbox'][2]))
                line_.set('y2', str(line['bbox'][3]))
                for k, word in enumerate(line['words']):
                    word_idx += 1
                    word_ = ET.SubElement(line_, 'word')
                    word_.set('name', f'word_{word_idx}')
                    word_.set('x1', str(word['bbox'][0]))
                    word_.set('y1', str(word['bbox'][1]))
                    word_.set('x2', str(word['bbox'][2]))
                    word_.set('y2', str(word['bbox'][3]))
                    word_.text = word['text']
                    for c in word['cbox']:
                        char_ = ET.SubElement(word_, 'char')
                        char_.set('x1', str(c[0]))
                        char_.set('y1', str(c[1]))
                        char_.set('x2', str(c[2]))
                        char_.set('y2', str(c[3]))
            # component_.text = ' '.join(para['text'])
        elif para['component'] == 'table':
            table_id += 1
            table_ = ET.SubElement(data, 'table')
            table_.set('name', f'table_{table_id}')
            table_.set('x1', str(para['bbox'][0]))
            table_.set('y1', str(para['bbox'][1]))
            table_.set('x2', str(para['bbox'][2]))
            table_.set('y2', str(para['bbox'][3]))
            for j, cell in enumerate(para['cells']):
                cell_ = ET.SubElement(table_, f'cell')
                cell_id = f'{table_id}_' +'_'.join([str(cell['cell_id'][0]),str(cell['cell_id'][1])])
                cell_.set('name',f'cell_{cell_id}')
                cell_.set('x1', str(cell['bbox'][0]))
                cell_.set('y1', str(cell['bbox'][1]))
                cell_.set('x2', str(cell['bbox'][2]))
                cell_.set('y2', str(cell['bbox'][3]))
                for j, line in enumerate(cell['lines']):
                    line_idx += 1
                    line_ = ET.SubElement(cell_, f'line')
                    line_.set('name', f'line_{line_idx}')
                    line_.set('x1', str(line['bbox'][0]))
                    line_.set('y1', str(line['bbox'][1]))
                    line_.set('x2', str(line['bbox'][2]))
                    line_.set('y2', str(line['bbox'][3]))
                    for k, word in enumerate(line['words']):
                        word_idx += 1
                        word_ = ET.SubElement(line_, 'word')
                        word_.set('name', f'word_{word_idx}')
                        word_.set('x1', str(word['bbox'][0]))
                        word_.set('y1', str(word['bbox'][1]))
                        word_.set('x2', str(word['bbox'][2]))
                        word_.set('y2', str(word['bbox'][3]))
                        word_.text = word['text']
                        for c in word['cbox']:
                            char_ = ET.SubElement(word_, 'char')
                            char_.set('x1', str(c[0]))
                            char_.set('y1', str(c[1]))
                            char_.set('x2', str(c[2]))
                            char_.set('y2', str(c[3]))
    return label
for i in [0]:
    root = to_xml(str(i))
    info = root.findall('.//info')[0]
    w,h = info.attrib['width'],info.attrib['height']
    img = np.zeros((int(h),int(w),4),dtype='uint8')
    img = Image.fromarray(img)
    img2 = Image.open(f'.//output/images/{i}.jpg')#f'output/images/{i}.png').convert('RGBA')
    draw = ImageDraw.Draw(img)
    imgs.append(img2.resize((1500,2000)))
    for comp in compz:
        comp_id = comps[comp]
        words = root.findall(f'.//{comp}')
        for word in words:
            attr = word.attrib
            x1,y1,x2,y2 = attr['x1'],attr['y1'],attr['x2'],attr['y2']
            x1,y1,x2,y2 = int(float(x1)),int(float(y1)),int(float(x2)),int(float(y2))
            draw.rectangle((x1,y1,x2,y2),fill=colors[comp_id], outline=(0,0,0),width=1)
            if len(compz) > 1:
                draw.rectangle(draw.textbbox((x1,y1),comp,font=font),fill=(0,0,0,170))
                draw.text((x1,y1),comp,fill='white',width=1, font=font)
            
    img = Image.composite(img,img2,Image.fromarray(np.array(img)[:,:,3]))
    img = img.resize((1500,2000))
    img.save(sys.argv[1]+".jpg")
    imgs.append(img)
img, *imgs = [im for im in imgs]
img.save(fp="assets/illustration/see.gif", format='GIF', append_images=imgs,
                 save_all=True, duration=2000, loop=0)
