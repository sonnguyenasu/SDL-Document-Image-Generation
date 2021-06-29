import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from .font_handler import get_font, get_font_size
import os
import math
import sys 
from .tbd import error,info
def get_img(path,threshold=1.0):
    if not os.path.exists(path):
        error(f"Path {path} does not exist")
        sys.exit(1)
    imgs = [os.path.join(path, img) for img in os.listdir(path)]
    i = np.random.randint(0, len(imgs))
    r = np.random.rand() 
    if r < threshold:
        try:
            img = Image.open(imgs[i])
            h,w = img.size
            if h*w == 0:
                os.remove(imgs[i])
                return get_img(path, threshold)
        except:
            os.remove(imgs[i])
            return get_img(path, threshold)

    else:
        img = Image.fromarray(np.random.randint(128,255,(1500,2000,3),dtype='uint8'))
    return img


def get_word(dictionary):
    '''
    returns a random word from the dictionary file
    dictionary: a list of words that we're gonna choose from
    output: a random word
    '''
    word = dictionary[np.random.randint(len(dictionary))]
    connectors = ['','—','-',':',';',',','?','!']
    connector = np.random.choice(connectors,p=(0.75,0.04,0.03,0.01,0.1,0.03,0.02,0.02))
    return word + connector

def render_text_line(args, img, xy, max_width, font, text_type='text', starting=False, ending=False, in_table=False, title=False):
    '''
    this function is for generating text line on an image
    input:
        img: background image
        xy: origin to write image
        max_width: maximum width to write text on
        font: font that the text will be rendered
        starting: whether this line is the first line of a paragraph
        ending: whether this line is the last line of a paragraph
    output:
        out_img: a RGBA image having all text generated
        data: a dictionary containing all the information of the paragraph (i.e.: coordinate of it and texts inside it)
    '''
    text = []
    text_joint = ''
    out_img = img.copy()
    start = True
    prefixes = ['A','B','C','D','I','II','III','IV',1,2,3,4,5,6]
    '''
    if text_type is number: we return a number that ends with 000. else we return the textline
    '''
    if text_type == 'number':
        if np.random.rand() > 0.2:
            len_number = min(3*max_width // font.getsize('222,')[0],9)
            word = str(np.random.randint(1, 10**(len_number)))
            res = '' 
            for i in range(0, len(word)):
                if (i-len(word)) % 3 == 2:
                    res += word[i]+','
                else:
                    res += word[i]
            word = res[:-1]
        else:
            word = ''
        text_joint = word
        text = [word]
    elif text_type == 'text':
        while True:
            word = get_word(args.words)
            # randomly place end-of-sentence period at points
            if np.random.exponential(args.period_prob) > 2*args.period_prob:
                word += '.'

            if start and (starting or title):
                word = word.capitalize()
            if start and starting and title and np.random.rand() < 0.6:
                prefix = str(np.random.choice(prefixes))
                if np.random.rand() < 0.3:
                    prefix += '.' + str(np.random.randint(1,5))
                    word = f'{prefix}. '+ word
            text.append(word)
            if len(text_joint) > 0:
                text_joint += ' '+word
            else:
                text_joint += word
            w, _ = font.getsize(text_joint)
            # cut the text when its length exceeds a given value
            if w > max_width: 
                exceeded = min(
                    max(int((w-max_width)/w*len(text_joint)), 1), len(text[-1]))+2
                text_joint = text_joint[:-exceeded].strip()
                text[-1] = text[-1][:-exceeded]
                if len(text[-1]) == 0:
                    text = text[:-1]
                w, _ = font.getsize(text_joint)
                under_fit = (max_width - w)//font.getsize('.')[0]
                text = text_joint.split(' ')
                if not in_table:
                    if under_fit > 0:
                        indexes = np.random.randint(0,len(text),under_fit)
                        for i in indexes:
                            text[i] += ' '#np.random.choice(['i','r','.','l',':',';','I','!'])
                        text_joint = ' '.join(text)
                    if font.getsize(text_joint)[0] > max_width:
                        text[-1] = text[-1][:-1]
                        text_joint = ' '.join(text)
                        break   
                break
            # we would end the line with a period. only happen at the last sentence of the parapgraph
            if ending: 
                text_joint += '.'
                break
            start = False
    else:
        error("text_type must be either text or number")
        sys.exit()
    # draw helps write the text down on the image
    draw = ImageDraw.Draw(out_img)
    if title and np.random.rand() < 0.2:
        text_joint = text_joint.upper()
        text = [t.upper() for t in text]
    draw.text(xy, text_joint, fill=args.text_color, font=font)
    line_bbox = draw.textbbox(xy, text_joint, font=font)
    line_bbox = [int(l) for l in line_bbox]  
    x0, y0 = xy
    words = []
    pad = draw.textlength(' ', font=font)
    for i, w in enumerate(text_joint.split(' ')):
        if w == '': 
            x0 += pad
            continue
        wbox = draw.textbbox((x0, y0), w, font=font)
        word = {'bbox': [int(wd) for wd in wbox], 'text': w, 'cbox':[]}
        x1 = x0
        for c in w:
            word['cbox'].append([int(cd) for cd in draw.textbbox((x1,y0),c,font=font)])
            x1 += draw.textlength(c, font=font)
        words.append(word)
        x0 += draw.textlength(w+' ', font=font)
    if args.vis_line:
        draw.rectangle(draw.textbbox(xy, text_joint, font=font),
                       fill=None, outline='yellow', width=1)
    if args.vis_word:
        x0, y0 = xy
        for i, c in enumerate(text_joint.split(' ')):
            draw.rectangle(draw.textbbox((x0, y0), c, font=font),
                           fill=None, outline='green', width=1)
            x0 += draw.textlength(c+' ', font=font)
    if args.vis_char:
        x0, y0 = xy
        for i, c in enumerate(text_joint):
            draw.rectangle(draw.textbbox((x0, y0), c, font=font),
                           fill=None, outline='red', width=1)
            x0 += draw.textlength(c, font=font)
    line_data = {'bbox': line_bbox, 'words': words, 'texts': text}
    return out_img, line_data


def render_paragraph(args, img, xy, font, fontsize, num_line,spacing, width=None, tab_at_start=True, text_type='text', in_table=False, title=False):
    '''
    render a paragraph
    input:
        img: the background image, type: PIL Image
        xy: the left top coordinate of the paragraph where are gonna paste the paragraph in. (float, float)
        font: font we're gonna render the text
        fontsize: size of text in pixel
        num_line: number of lines that the paragraph has
    '''
    
    if width is None:
        width = args.para_width
    out_img = img.copy()
    lines = [] # list of dictionary, each dictionary contains information of a line in the paragraph. 
    word_bboxes = [] # list of numpy array, each represent coordinate of a word in (x1,y1,x2,y2) manner.
    texts = [] # list of text appearing in the paragraph.

    if tab_at_start:
        out_img, line = render_text_line(
            args, out_img, [xy[0]+fontsize, xy[1]], width-fontsize, font, starting=True, in_table=in_table, text_type=text_type,title=title)
    else:
        out_img, line = render_text_line(
            args, out_img, [xy[0], xy[1]], width,font, starting=False, in_table=in_table, text_type=text_type,title=title)
    if len(line['texts']) > 0:
        if line['texts'][0] != '':
            lines.append(line)
            word_bboxes.extend(line['words'])
            texts.extend(line['texts'])
    for i in range(1, num_line-1):
        out_img, line = render_text_line(
            args, out_img, [xy[0], xy[1]+fontsize*i*(1+spacing)], width, font, in_table=in_table, text_type=text_type,title=title)
        if len(line['texts']) > 0:
            if line['texts'][0] != '':
                lines.append(line)
                word_bboxes.extend(line['words'])
                texts.extend(line['texts'])
    if num_line > 1:
        out_img, line = render_text_line(
            args, out_img, (xy[0], xy[1]+fontsize*(num_line-1)*(1+spacing)), width, font, ending=True, in_table=in_table, text_type=text_type,title=title)
        if len(line['texts']) > 0:
            if line['texts'][0] != '':
                lines.append(line)
                word_bboxes.extend(line['words'])
                texts.extend(line['texts'])
    
    para = {'lines': lines, 'words': word_bboxes, 'texts': texts}

    return out_img, para, word_bboxes, texts

def fill_text(args, img, bbox, font, font_title, fontsize, text_type = 'text', in_table = False, render_type='all', title=False, prob_image=None, prob_table=None):
    '''
    fill text into the bounding box
    bbox has form of x,y,w,h where x,y is top left coordinate
    '''
    if not in_table and not title:
        if np.random.rand() < 0.2: font = get_font(args,fontsize,mixed=True)
    if prob_image is None: prob_image = args.prob_image
    if prob_table is None: prob_table = args.prob_table
    if len(bbox) != 4:
        error("Length of the bbox must be 4: x,y,w,h")
        sys.exit()
    if type(fontsize) != int:
        error("The fontsize must be an integer")
        sys.exit()
    bbox = [int(b) for b in bbox]
    # randomly placed image into the document
    if bbox[3]>100 and bbox[3]/bbox[2] > 0.3 and render_type=='all':
        out_img = np.array(img)
        r = np.random.rand()
        if r < prob_image:
            return render_figure(args, out_img, bbox, font,font_title,fontsize)
        elif np.random.rand() < prob_table/(1-prob_image):
            return render_table(args, Image.fromarray(out_img), bbox, font, font_title, fontsize)
        elif np.random.rand() < 0.25/((1-prob_table)*(1 - prob_image)):
            return render_formula(args, Image.fromarray(out_img), bbox, font, font_title, fontsize)
        elif np.random.rand() < 0.5:
            return render_title(args, Image.fromarray(out_img), bbox, font, font_title, fontsize)
    if render_type == 'table':
        return render_table(args,img,bbox,font,font_title,fontsize)
    if render_type == 'figure':
        # out_img = np.array(img)
        return render_figure(args,np.array(img),bbox,font,font_title,fontsize)
    # calculating number of line in the paragraph
    # then re-calculate the value of spacing between lines 
    # so that we can fit perfectly the paragraph into the bounding box.
    num_line = (bbox[3]+args.spacing)/((1+args.spacing)*fontsize)
    num_line = int(num_line)
    spacing = (-bbox[3] + num_line * fontsize)/(1-num_line*fontsize)

    # manipulating the image
    out_img = img.copy()
    tab = args.tab_at_start and not in_table
    out_img, para, words, texts = render_paragraph(
        args, out_img, bbox[:2], font, fontsize, num_line, spacing,width=bbox[2], in_table=in_table, tab_at_start=tab, text_type=text_type,title=title)
    if args.vis_cell:
        draw = ImageDraw.Draw(out_img)
        draw.rectangle((bbox[0], bbox[1], bbox[0]+bbox[2],
                        bbox[1]+bbox[3]), outline=(0, 0, 0, 255))

    # format output data
    if not in_table:
        para = para['lines']
        para = {'component':'paragraph', 'lines': para, 'bbox':(int(bbox[0]), int(bbox[1]), int(bbox[0])+math.ceil(bbox[2]),
                        int(bbox[1])+math.ceil(bbox[3]))}
    else:
        lines = para['lines']
        para = {'lines':lines, 'words': para['words']}
    return out_img, para, words, texts

def render_figure(args,img,bbox,font_text,font_title,fontsize):
    if bbox[3]/bbox[2] < 0.25:
        return render_table(args,Image.fromarray(img),bbox,font_text,font_title,fontsize)
    if np.random.rand() < 0.5:
        s_img = get_img(args.background_path,threshold=1.0).convert('RGBA').resize((bbox[2],bbox[3]))
        para = {'component': 'natural_image', 'bbox':(int(bbox[0]), int(bbox[1]), int(bbox[0])+math.ceil(bbox[2]),int(bbox[1])+math.ceil(bbox[3]))}
    else: 
        
        s_img = get_img(args.plot_path,1).convert('RGBA').resize((bbox[2],bbox[3]))
        enhancer = ImageEnhance.Brightness(s_img)
        s_img = enhancer.enhance(0.8)
        para = {'component': 'plot', 'bbox':(int(bbox[0]), int(bbox[1]), int(bbox[0])+math.ceil(bbox[2]),int(bbox[1])+math.ceil(bbox[3]))}
        
    s_img = np.array(s_img)
    img[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2],:] += s_img
    words = []
    texts = []
    return Image.fromarray(img), para, words, texts

def render_table(args, img, bbox, font_text, font_title, fontsize, padding=5):
    out_img = img.convert('RGBA')
    x, y, w, h = bbox
    num_line = 1
    min_column = 2
    max_column = min(6,w//70)
    num_column = np.random.randint(min_column, max_column)  # number of table columns
    # Getting columns' width (randomly placed)
    column_widths = np.random.rand(num_column)+0.4
    column_widths /= sum(column_widths)
    column_widths *= w

    num_row = (h-(args.spacing+1)*fontsize*num_line*0.3) / \
        (fontsize*(args.spacing+1)*1.2*num_line) + 0.25
    num_row = int(num_row)
    # re-evaluate the spacing:
    spacing = (h-(args.spacing+1)*fontsize*num_line*0.3) / \
        (fontsize*(num_row-0.25)*1.2*num_line)-1
    # spacing = args.spacing
    x0 = x
    y0 = y
    draw = ImageDraw.Draw(out_img)
    color = np.random.randint(0, 255, 3)
    column = np.random.rand() > args.visible_column_prob
    if np.random.rand() < 0.9:
        for i in range(num_row+1):
            if i == 0:
                if np.random.rand() < 0.3:
                    draw.rectangle((x, int(y0), x+w,
                                    int(y0+(spacing+1)*fontsize*num_line*1.2)), fill=(*color, 100))
                draw.line((x, int(y0), x+w, int(y0)),
                        fill=(0, 0, 0, 255), width=2)
                draw.line((x, int(y0+(spacing+1)*fontsize*num_line*1.2), x+w, int(y0+(spacing+1)*fontsize*num_line*1.2)),
                        fill=(0, 0, 0, 255), width=2)
            else:
                if np.random.rand() > 1.0 and i < num_row:
                    draw.rectangle((x, int(y0), x+w,
                                    int(y0+(spacing+1)*fontsize*num_line*1.2)), fill=(*color, 50))
                if np.random.rand() < 0.5:
                    draw.line((x, int(y0), x+w, int(y0)),
                        fill=(0, 0, 0, 255), width=1)
            y0 += (spacing+1)*fontsize*num_line*1.2
        draw.line((x, int(y0-(spacing+1)*fontsize*num_line*1.2), x+w, int(y0-(spacing+1)*fontsize*num_line*1.2)),
                        fill=(0, 0, 0, 255), width=1)

    if column:
        x0 = x
        for j in range(len(column_widths)+1):
            draw.line((x0, y, x0, y+h), fill=(0, 0, 0, 255), width=1)
            if j < len(column_widths):
                x0 += column_widths[j]

    y0 = y+(args.spacing+1)*fontsize*num_line*0.3
    cells = []
    words = []
    texts = []
    for row_id in range(num_row):

        x0 = x
        font = font_title
        for column_id in range(len(column_widths)):
            if column_id != 0 and row_id != 0:
                text_type = 'number'
            else:
                text_type = 'text'
            width = column_widths[column_id]

            if row_id > 0:
                font = font_text

                out_img, cell, word, text = fill_text(args, out_img, (x0+padding, y0-(spacing+1)*fontsize*num_line*0.2, np.random.randint(60, max(column_widths[column_id]-padding, 61)),
                                                                      (spacing+1)*fontsize*num_line), font, font_title, fontsize, text_type=text_type, in_table=True)
                
                cell['cell_id'] = (row_id, column_id)
                box = (x0,y0-(spacing+1)*fontsize*num_line*0.2,x0+column_widths[column_id],y0+(spacing+1)*fontsize*num_line-(spacing+1)*fontsize*num_line*0.2)
                cell['bbox'] = [int(box[0]),int(box[1]),math.ceil(box[2]),math.ceil(box[3])]
                cells.append(cell)
                words.extend(word)
                texts.extend(text)
            else:
                pwidth = np.random.randint(
                    50, max(51, column_widths[column_id]*0.6-padding))
                pad = 0
                if column:
                    pad = (column_widths[column_id] - pwidth)/2
                out_img, cell, word, text = fill_text(args, out_img, (x0+padding+pad, y0-(spacing+1)*fontsize *
                                                                      num_line*0.1, pwidth, (spacing+1)*fontsize*num_line), font,font_title, fontsize, text_type=text_type, in_table=True)
                
                cell['cell_id'] = (row_id, column_id)
                box = (x0,y0-(spacing+1)*fontsize*num_line*0.2,x0+column_widths[column_id],y0+(spacing+1)*fontsize*num_line-(spacing+1)*fontsize*num_line*0.1)
                cell['bbox'] = [int(box[0]),int(box[1]),math.ceil(box[2]),math.ceil(box[3])]
                cells.append(cell)
                words.extend(word)
                texts.extend(text)
            x0 += width
        y0 += (spacing+1)*fontsize*num_line*1.2
    para = {'component':'table','cells': cells, 'bbox':(int(bbox[0]), int(bbox[1]), int(bbox[0])+math.ceil(bbox[2]),int(bbox[1])+math.ceil(bbox[3])), 'texts':texts}
    return out_img, para, words, texts

def render_title(args, img, bbox, font, font_title, fontsize):
    x,y,w,h = bbox
    paras = []
    out_img = img.copy()
    tat = args.tab_at_start
    args.tab_at_start = False
    new_fs = fontsize + int(np.random.choice([*range(1,5),min(10,int(h/(1+args.spacing)))]))
    font_title = get_font(args, new_fs,mixed=True)
    color = args.text_color
    if np.random.rand() < 0.2:
        args.text_color = (*np.random.randint(0,88,3).tolist(),255)
    if np.random.rand() < 0.5:
        out_img, para, word, text = fill_text(args, out_img,(x,y,w*(0.3+np.random.rand()*0.7),new_fs),font_title,font_title,new_fs, title=True)
    else:
        width = w*(0.3+np.random.rand()*0.7)
        out_img, para, word, text = fill_text(args, out_img,(x+(w-width)/2,y,width,new_fs),font_title,font_title,new_fs, title=True)
    args.text_color = color
    para['component'] = 'title'
    paras.append(para)
    words = word
    texts = text
    y += (1 + args.spacing + np.random.rand())*new_fs
    args.tab_at_start = tat
    out_img, para, word, text = fill_text(args, out_img, (x,y,w,bbox[1]+h-y),font,font_title,fontsize, render_type='paragraph')
    paras.append(para)
    words.extend(word)
    texts.extend(text)
    return out_img, paras, words, texts

def render_list(args, img, bbox, font, font_title, fontsize):
    num_line = num_line = (bbox[3]+args.spacing)/((1+args.spacing)*fontsize)
    num_line = int(num_line)

def render_formula(args, img, bbox, font, font_title, fontsize):
    padding = 10
    out_img = np.array(img)
    formula = get_img(args.formula_path,1.0)
    w, h = formula.size

    if w*h == 0:
        return render_formula(args, img, bbox, font, font_title, fontsize)
    if w > bbox[2]:
        formula = formula.resize((bbox[2],h))
    if h > bbox[3]:
        formula = formula.resize((w,bbox[3]))
    w, h = formula.size
    para = []
    x,y = bbox[0]+bbox[2]/2-w/2,bbox[1]-h/2
    y += (0.4*np.random.rand()+0.3)*bbox[3]
    x,y,w,h = int(x),int(y),math.ceil(w),math.ceil(h)
    formula = np.array(formula).astype('float64')
    formula[:,:,:3] += 1
    formula[:,:,:3] *= np.uint8(args.text_color[:3])
    formula[:,:,3] *= args.text_color[3]/255

    out_img[y:y+h,x:x+w] += (formula).astype('uint8')
    out_img = Image.fromarray(out_img)
    box = (bbox[0],bbox[1],bbox[2],y-bbox[1]-padding)
    if box[3] > fontsize*1.1:
        out_img, p, _, _ = fill_text(args, out_img, box, font,font_title,fontsize)
        para.append(p)
    para.append({'component':'formula','bbox':(x,y,x+w,y+h)})
    args.tab_at_start = False
    box = (bbox[0],y+h+padding,bbox[2],bbox[1]+bbox[3]-y-h-padding)
    if box[3] > fontsize*1.1:
        out_img, p, _, _ = fill_text(args, out_img, box, font,font_title,fontsize)
        para.append(p)
    args.tab_at_start = True
    return out_img,para,[],[]
if __name__ == '__main__':
    from config import Config
    img = get_img('assets').convert("RGBA").resize((1500,2000))
    out_img = Image.fromarray(np.zeros_like(img))
    bbox = (500,500,500,300)

    fontsize = 20
    font_title = ImageFont.truetype('fonts/bold/arial-bold.ttf',fontsize)
    font = ImageFont.truetype('fonts/regular/arial.ttf',fontsize)
    args = Config()
    args.merge_from_file('page.yaml')
    args.text_color = (0,0,0,255)
    args.vis_line = False
    args.vis_word = True
    args.vis_char = False
    args.vis_cell = False
    args.prob_image = 0.2
    args.prob_table = 0.2
    args.visible_column_prob = 1.0
    args.words = 'corpus/words.txt'
    out_img, _, _, _ = render_title(args, out_img, bbox, font,font_title,fontsize)
    out_img = Image.composite(out_img,img,out_img)
    out_img.show()
