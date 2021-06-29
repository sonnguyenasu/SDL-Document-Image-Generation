import json
import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

for fname in tqdm(os.listdir('output/jsons')):
    fname = fname[:-5]
    f = json.load(open(f'output/jsons/{fname}.json', 'r'))
    
    label = ET.Element('label')
    img_info = ET.SubElement(label, 'info')

    img_info.set('width', '1500')
    img_info.set('height', '2000')
    img_info.set('file_name', fname+'.png')

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
        if isinstance(para,list):
            paras.extend(para)
        else:
            paras.append(para)
    for _, para in enumerate(paras):
        if isinstance(para,list):
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
    mydata = ET.tostring(label, encoding="unicode")
    myfile = open(f'output/xmls/{fname}.xml', 'w',encoding='utf-8')
    myfile.write(mydata)
