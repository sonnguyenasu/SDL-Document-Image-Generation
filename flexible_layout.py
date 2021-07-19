from helper.text_render import fill_text, get_img
from helper.config import Config
from helper.font_handler import get_font, get_font_size
from helper.tbd import info
import datetime
from multiprocessing import Pool
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import numpy as np
import json
import time,os
cnames = ['paragraph', 'table', 'figure', 'title', 'all', 'all']

def get_boxes(height, width, left, top, \
              min_height = 400, min_width = 400, spacing = 40):
    
    boxes = []

    # if height and width is small enough, we stop dividing
    if not (height > min_height*2 + spacing \
            or width > min_width*2 + spacing):
        boxes.append((left,top,width,height, 5))
        return boxes
    
    # if box is not that small, but we just decided to stop dividing
    if (height < 3*min_height or width < 3*min_width) \
            and (np.random.rand() < 0.15):
        boxes.append((left,top,width,height,np.random.randint(2)))
        return boxes
    
    # else we are gonna divide the boxes into half
    else: 
        # Determine the direction to divide our layout
        if not height > min_height*2 + spacing:
            direction   = 'row'
        elif not width > min_width*2 + spacing:
            direction   = 'column'
        else: #if the box is big both vertically and horizontally
            direction   = np.random.choice(['row', 'column'])

        
        if direction   == 'row':
            break_point = np.random.randint(left + min_width, left + width - min_width - spacing)
            box1        = get_boxes(height,break_point-left,left,top)
            box2        = get_boxes(height,left+width-spacing-break_point,break_point+spacing,top)
            return box1 + box2
        else: 
            break_point = np.random.randint(top + min_height, top + height - min_height - spacing)
            box1        = get_boxes(break_point-top,width,left,top)
            box2        = get_boxes(top+height-spacing-break_point,
                                    width,left,break_point+spacing)
            return box1 + box2





def render_from_layout(args, bboxes, im_height, im_width):
    '''
    render a page from list of bounding boxes that make the page
    bboxes: list of bbox, shape: (x,y,w,h,c) x n
            where x,y,w,h are coordinate and c is the class of the bounding box
    '''
    final_image                = Image.new('RGBA', (im_width, im_height))
    img                        = final_image.copy()
    
    fontsize                   = int(np.random.choice(args.fontsize_set))
    font_title                 = get_font(args, fontsize, bold=True)
    font                       = get_font(args, fontsize)

    paras                      = []
    texts                      = []
    for (x, y, w, h, c) in bboxes:
        c_name                 = cnames[c]
        out_img, para, _, text = fill_text(
                                    args, img, (x, y, w, h), font, 
                                    font_title, fontsize, render_type=c_name
                                )
        
        
        final_image            = Image.composite(out_img, final_image, out_img)
        if isinstance(para, list):            
            paras.extend(para)
        else:
            paras.append(para)
        texts.extend(text)

    para                       = {'para': paras}
    para['bbox']               = [0, 0, img.size[0], img.size[1]]
    para['text']               = texts


    return final_image, para

def main(args):
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little')) 
    total_time = 0
    os.makedirs('output/images', exist_ok=True)
    os.makedirs('output/jsons', exist_ok=True)
    for idx, im_name in enumerate(range(args.resume_from, args.resume_from+args.repeat)):
        t                      = time.time()
        page_height            = np.random.randint(1500,2500)
        page_width             = np.random.randint(1500,2500)
        padding                = 100
        bboxes                 = get_boxes(page_height-2*padding,page_width-2*padding
                                           ,padding,padding,spacing=args.col_spacing)
        
        im, para               = render_from_layout(args, bboxes, page_height, page_width)
        fin                    = get_img('assets/bg', 1.0).resize((page_width, page_height))
        fin                    = Image.composite(im, fin, im)
        fin.save(f'output/images/{im_name}.jpg')
        
        json.dump(para, open(f'output/jsons/{im_name}.json', 'w', encoding='utf-8'))

        #timing and logging the time
        total_time             += (time.time() - t)
        
        if (idx + 1) % args.print_freq == 0:
            avg_time           = total_time / (idx + 1)
            eta                = avg_time * args.repeat - total_time
            eta                = str(datetime.timedelta(seconds=round(eta)))
            ttime              = str(datetime.timedelta(seconds=round(total_time)))
            info(f"Generated {(idx+args.resume_from+1)}/{args.repeat+args.resume_from}"+
                 f": average time: {avg_time:.2f}s eta: {ttime}/{eta}")

if __name__ == '__main__':
    import argparse
    parser                  = argparse.ArgumentParser(description="Generator Argument")
    parser.add_argument('-n','--num_core',default=16,type=int,
                        help='# cores are used for generation')
    parser.add_argument('-c','--config_file',default='configs/page.yaml',type=str)
    args                    = parser.parse_args()
    
    num_core, config_file   = args.num_core, args.config_file
    args_set                = []
    for _ in range(num_core):
        args_set.append(Config())

    for i, args in enumerate(args_set):
        args.merge_from_file(config_file)
        args.words          = [
                                word.strip() for word in 
                                open(args.words, 'r', encoding='utf-8').readlines()
                            ]
        args.text_color     = (np.random.randint(0, 80),np.random.randint(0, 80),np.random.randint(0, 80)
                                ,np.random.randint(200, 255))
        args.col_spacing    = np.random.randint(40, 50)
        args.resume_from    = i*args.repeat
    pool = Pool(processes=num_core)
    pool.map(main, args_set)
