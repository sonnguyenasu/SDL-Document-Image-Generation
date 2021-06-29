import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from .tbd import info
####
# TODO:
# 1. write function to render a text line
#   a. the function should contain information about the line, the word bounding box, even character boudning box
#   b. the function should render a text line that best fit with the line width


####
# Functions handling the fonts:
#     a. _get_font_size
#     b. _get_font

def get_font_size(fs_range):
    '''
    get a np.random fontsize from the given range
    input:
        fs_range: range of the fontsize that we're gonna pick from
    output:
        a np.random fontsize
    '''
    return np.random.randint(*fs_range)


def get_font(args,fontsize,bold=False, mixed=False):
    
    if bold:
        fonts = os.listdir(os.path.join(args.font_path,'bold'))
        i = np.random.randint(0,len(fonts))
        return ImageFont.truetype(os.path.join(args.font_path,'bold',fonts[i]),fontsize)
    elif mixed:
        fonts = os.listdir(os.path.join(args.font_path,'mixed'))
        i = np.random.randint(0,len(fonts))
        return ImageFont.truetype(os.path.join(args.font_path,'mixed',fonts[i]),fontsize)
    fonts = os.listdir(os.path.join(args.font_path,'regular'))
    i = np.random.randint(0,len(fonts))
    return ImageFont.truetype(os.path.join(args.font_path,'regular',fonts[i]),fontsize)
    
