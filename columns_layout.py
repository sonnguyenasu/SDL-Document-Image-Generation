import argparse
from helper.util import get_img, render
from PIL import Image, ImageFont, ImageEnhance
from multiprocessing import Pool

import numpy as np
import time
import matplotlib.pyplot as plt
import os
import json
from tqdm import tqdm
from helper.tbd import info, error
from helper.config import Config
import datetime
import sys
import cv2
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def main(args):
    total_time = 0
    for idx, im in enumerate(
            range(args.resume_from, args.resume_from + args.repeat)):
        args.text_color     = (*np.random.randint(0, 80, 3).tolist(),
                                np.random.randint(200, 255))
        args.col_spacing    = np.random.randint(*args.col_spacing_)
        t                   = time.time()

        img                 = get_img(args.bg_img)
        img                 = cv2.GaussianBlur(np.array(img), (5, 5), cv2.BORDER_DEFAULT)
        img                 = Image.fromarray(img)
        img                 = img.resize((args.img_width, args.img_height))
        

        # most important line of code: code to render the layout
        out_img, para       = render(args, img)
        
        if args.blur:
            out_img         = cv2.GaussianBlur(np.array(out_img), (5, 5),
                                       cv2.BORDER_DEFAULT)
            out_img         = Image.fromarray(out_img)
        
        # writing label into json file
        json.dump(
            para,
            open(os.path.join(args.output_path, 'jsons', f'{im}.json'),
                 'w', encoding='utf-8'))

        # pasting transparent image into the background paper
        img2                = Image.fromarray(np.array(out_img)[:, :, :3])
        mask                = Image.fromarray(np.array(out_img)[:, :, 3])
        out_img             = Image.composite(img2, img, mask)

        contrast            = ImageEnhance.Contrast(out_img)
        out_img             = contrast.enhance(0.8 + 0.3 * np.random.rand())
        enhancer            = ImageEnhance.Brightness(out_img)
        out_img             = enhancer.enhance(0.9 + 0.3 * np.random.rand())

        out_img.save(os.path.join(args.output_path, 'images', f'{im}.jpg'))

        total_time          += (time.time() - t)

        # logging the time out
        if (idx + 1) % args.print_freq == 0:
            avg_time        = total_time / (idx + 1)
            eta             = avg_time * args.repeat - total_time
            eta             = str(datetime.timedelta(seconds=round(eta)))
            ttime           = str(datetime.timedelta(seconds=round(total_time)))

            info(f"Generated {(idx+args.resume_from+1)}/{args.repeat+args.resume_from}"+\
                 f": average time: {avg_time:.2f}s eta: {ttime}/{eta}")


def format_range(given_range, name):
    if type(given_range) != str:
        error(f'{name} should be a string')
        sys.exit()
    if '-' not in given_range:
        error(
            f'{name} should have form of a-b where a and b are integers and a<b'
        )
        sys.exit()

    res     = [int(s) for s in given_range.split('-')]
    res[-1] += 1

    if len(res) != 2:
        error(f'length of {name} should be 2')
        sys.exit()
    if not res[0] < res[1]:
        error(
            f'first number in {name} should not be greater than second number in {name}'
        )
        sys.exit()

    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config_file',
        default='configs/page.yaml',
        type=str
    )
    parser.add_argument(
        '-o',
        '--output_path',
        default='output',
        type=str
    )
    parser.add_argument(
        "--num_core",
        default=12,
        type = int,
        help = 'number of cores used to generate the layout'
    )
    args_    = parser.parse_args()
    
    args_set = []
    for _ in range(args_.num_core):
        args_set.append(Config())
    
    
    for i, args in enumerate(args_set):
        
        args.merge_from_args(args_)
        args.merge_from_file(args_.config_file)

        args.words          = [
            word.strip()
            for word in open(args.words, 'r', encoding='utf-8').readlines()
        ]

        args.fontsize       = format_range(args.fontsize, "fontsize")
        args.col_range      = format_range(args.col_range, "col_range")
        args.col_spacing_   = format_range(args.col_spacing, 'col_spacing')
        args.resume_from    = i * args.repeat
    
    pool = Pool(processes=12)
    pool.map(main, args_set)
