import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .font_handler import get_font, get_font_size
<<<<<<< HEAD
from .text_render_ import render_text_line, render_paragraph, fill_text, render_table
=======
from ._text_render import render_text_line, render_paragraph, fill_text, render_table
>>>>>>> 60067811e5ad5b88814b1ae5fbf1df85b0ff3524
import os,sys
from .tbd import error

#get_img: return the image for background
#path is the path of the background image
def get_img(path,threshold=1.0):
    if not os.path.exists(path):
        error(f"Path {path} does not exist")
        sys.exit(0)
    imgs = [os.path.join(path, img) for img in os.listdir(path)]
    i = np.random.randint(0, len(imgs))
    r = np.random.rand() 
    if r < threshold:
        try:
            img = Image.open(imgs[i])
        except:
            os.remove(imgs[i])
            return get_img(path, threshold)

    else:
        colors = np.random.randint(150,255,3)
        img = np.zeros((12,16,3),dtype='uint8')+np.random.randint(0,20,(12,16,3),dtype='uint8')
        for i in range(3):
            img[:,:,i] += colors[i]
        img = Image.fromarray(img)
    return img



'''
TODO: make render_page be more flexible, i.e.: no more hard code
'''
def render_page(args, img):
    out_img = np.zeros((img.size[1], img.size[0], 4), dtype=np.uint8)
    out_img = Image.fromarray(out_img)
    fontsize = get_font_size(args.fontsize)
    font = get_font(args,fontsize)
    font_title = get_font(args,fontsize,bold=True)
    xs = [img.size[0]//20, 19*img.size[0]//20]
    ratio = np.random.rand()*0.5 + 0.1
    table_top = np.random.rand() < 0.8
    if table_top:
        ratio = 0
    num_col = np.random.randint(*args.col_range)
    
    
    prob_image = args.prob_image/num_col
    prob_table = args.prob_table/num_col
    
    
    start = np.random.rand() * 0.1 + ratio
    y0 = int(start*img.size[1])
    paras = []
    if not table_top:
        out_img, para, _, texts = fill_text(args, out_img, \
            (int(xs[0]),y0-int((ratio-0.05)*img.size[1]),\
            int(xs[1]-xs[0]),int((ratio-0.05)*img.size[1]-2*args.spacing*fontsize)),font,font_title,\
            fontsize,prob_image=prob_image,prob_table=prob_table,render_type=np.random.choice(['table','figure']))
        if isinstance(para,dict):
            paras.append(para)
        else: 
            for par in para:
                paras.append(par)
    if num_col == 1:
        num_comp = np.random.randint(3,10)
        hs = (np.random.rand(num_comp)+0.5)/3
        hs /= hs.sum(axis=0)
        hs *= (0.8-ratio)*img.size[1]
        hs = hs.astype('int')
        hs = hs.tolist()
        last = hs.pop(-1)
        img_idx = np.random.randint(0,num_comp-1)
        hs[img_idx] += last
        for i in range(num_comp-1):
            out_img, para, _, texts = fill_text(args, out_img, (int(xs[0]),y0,int(xs[1]-xs[0]),hs[i]),font,font_title,fontsize,prob_image=prob_image,prob_table=prob_table)
            
            if isinstance(para,dict):
                paras.append(para)
            else: 
                for par in para:
                    paras.append(par)
            y0 += hs[i]+(args.spacing)*fontsize
    else:
        x0 = xs[0]
        for _ in range(num_col):
            num_comp = np.random.randint(3,10)
            hs = (np.random.rand(num_comp)+0.5)/3
            hs /= hs.sum(axis=0)
            hs *= (0.8-ratio)*img.size[1]
            hs = hs.astype('int')
            y0 = int(start*img.size[1])
            
            for i in range(num_comp):
                out_img, para, _, texts = fill_text(args, out_img, (int(x0),y0,int((xs[1]-xs[0])/num_col-args.col_spacing/2),hs[i]),font,font_title,fontsize,prob_image=prob_image,prob_table=prob_table)
                
                if isinstance(para,dict):
                    
                    paras.append(para)
                else: 
                    for par in para:
                        paras.append(par)
                y0 += hs[i]+(args.spacing)*fontsize
                
            x0 += int((xs[1]-xs[0])/num_col+args.col_spacing/2)
            
    para = {'para':paras}
    para['bbox'] = [0,0,img.size[0],img.size[1]]
    para['text'] = texts
    return out_img, para
    

# the main function for rendering the page
def render(args, img):
    if args.type=='page':
        return render_page(args, img)
    elif args.type=='table':
        from functools import reduce
        fontsize = get_font_size(args.fontsize)
        x = np.random.randint(10,350)
        y = np.random.randint(10,400)
        w = np.random.randint(500,1100)#1100
        h = np.random.randint(500,1400)
        bbox = (x,y,w,h)
        font_text = get_font(args,fontsize)
        font_title = get_font(args,fontsize, bold = True)
        img, para, _, texts = render_table(
            args, img, bbox,font_text, font_title, fontsize)
        para['bbox'] = [bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]]
        para['text'] = texts
        return img, para
    else:
        assert False, "the type to generate should be either page or table."
