def imports():
    import cv2, json, time, os
    import numpy as np
    from tqdm import tqdm
    global cv2, np, json, time, os, tqdm

def load_data(idx, data_path):
    data = json.load(open(os.path.join(data_path, 'jsons', f'{idx}.json')))
    img  = cv2.imread(os.path.join(data_path, 'images', f'{idx}.jpg'))
    return img, data

def extract_box(data):
    box = []
    for component in data['para']:
        if component['component'] in ['title','paragraph']:
            for line in component['lines']:
                bx = line['bbox']
                box.append([[bx[0],bx[1]],[bx[2],bx[1]],[bx[2],bx[3]],[bx[0],bx[3]]])
    box = np.array(box,dtype=np.float32)
    return box

def estimate_tps(h, w):
    global tps
    pts1 = []
    for i in range(100,w,600):
        for j in range(100,h,500):
            pts1.append([i,j])
    pts1 = np.array(pts1,dtype=np.float32)
    pts2 = pts1.copy()
    pts1 += np.random.randint(-10, 10, size=(len(pts1), 2))
    pts2 += np.random.randint(-10, 10, size=(len(pts1), 2))
    matches = [cv2.DMatch(i, i, 0) for i in range(len(pts1))]
    tps.estimateTransformation(np.array(pts1).reshape(
        (-1, len(pts1), 2)), np.array(pts2).reshape((-1, len(pts2), 2)), matches)

def get_tps_contours(h,w):
    mask = np.zeros((h,w),dtype=np.uint8)
    mask = cv2.drawContours(mask, box.astype(np.int32), -1, color=255, thickness=cv2.FILLED)

    new_mask = tps.warpImage(mask)

    contours,_ = cv2.findContours(new_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours
def write_to_file(idx, data_path):
    f = open(os.path.join(data_path, 'lines', f'{idx}.txt'),'w')
    for contour in contours:
        contour = cv2.approxPolyDP(contour, epsilon=1, closed=True)
        text = contour.reshape([-1]).__repr__().replace('\n','').replace(' ', '')[7:-14]
        f.write(text)
        f.write(',a')
        f.write('\n')
    f.close()

if __name__ == '__main__':
    imports()
    tps                             = cv2.createThinPlateSplineShapeTransformer()
    output_path                     = 'output'
    idx_set                         = [file.split('/')[-1].split('.')[0] 
                                       for file in os.listdir(os.path.join(output_path,'images'))]
    for idx in tqdm(idx_set):
        img, data                   = load_data(idx, output_path)
        h, w, _                     = img.shape
        estimate_tps(h, w)
        box                         = extract_box(data)
        dst                         = tps.warpImage(img)
        contours                    = get_tps_contours(h,w)
        os.makedirs(os.path.join(output_path,'lines'),exist_ok=True)
        os.makedirs(os.path.join(output_path,'wraped'),exist_ok=True)
        write_to_file(idx, output_path)
        cv2.imwrite(os.path.join(output_path,'wraped',f'{idx}.jpg'), dst)