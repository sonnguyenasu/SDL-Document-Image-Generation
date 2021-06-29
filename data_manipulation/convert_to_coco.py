import json
import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
from PIL import Image
images = []
annotations = []
categories = [
    {'name':'paragraph', 'id': 1, 'supercategory': ''},
    {'name':'title', 'id': 2, 'supercategory': ''},
    {'name':'table', 'id': 3, 'supercategory': ''},
    {'name':'figure', 'id': 4, 'supercategory': ''},
    {'name':'plot', 'id': 5, 'supercategory': ''},
    {'name':'formula', 'id': 6, 'supercategory': ''},
]
anno_id = 0
image_id = 0
for i, fname in enumerate(tqdm(os.listdir('output/jsons'))):
    if True:
        fname = fname[:-5]
        f = json.load(open(f'output/jsons/{fname}.json', 'r'))
        image_id += 1
        img_info = {}
        imz = Image.open(f'output/images/{fname}.jpg')
        img_info['width'] = imz.size[0]
        img_info['height'] = imz.size[1]
        img_info['file_name'] = fname+'.jpg'
        img_info['id'] = image_id
        images.append(img_info)
        
        paras = []
        for _, para in enumerate(f['para']):
            if isinstance(para,list):
                paras.extend(para)
            else:
                paras.append(para)
        for _, para in enumerate(paras):
            annotation = {}
            if isinstance(para,list):
                print(para)
            anno_id += 1
            annotation['id'] = anno_id
            annotation['image_id'] = image_id
            annotation['bbox'] = (para['bbox'][0], para['bbox'][1], para['bbox'][2] - para['bbox'][0],para['bbox'][3] - para['bbox'][1])
            annotation['iscrowd'] = 0
            if para['component'] == 'paragraph':
                annotation['category_id'] = 1
            elif para['component'] == 'natural_image':
                annotation['category_id'] = 4
            elif para['component'] == 'plot':
                annotation['category_id'] = 5
            elif para['component'] == 'formula':
                annotation['category_id'] = 6
            elif para['component'] == 'title':
                annotation['category_id'] = 2
            elif para['component'] == 'table':
                annotation['category_id'] = 3
            annotations.append(annotation)
    else: pass
res = {'images': images, 'annotations': annotations, 'categories': categories}
json.dump(res, open('train.json','w'))
