import os
import glob

def get_img_and_json_files(data_path):
    imgs = os.listdir(os.path.join(data_path, 'images'))
    jsons = os.listdir(os.path.join(data_path, 'jsons'))
    imgs.sort()
    jsons.sort()

    return imgs, jsons


def reorganize(img_list, json_list, data_path, output_path):
    os.makedirs(os.path.join(output_path, 'jsons'),exist_ok=True)
    os.makedirs(os.path.join(output_path, 'images'),exist_ok=True)
    for idx in range(len(img_list)):
        img_idx = img_list[idx].split('.')[0]
        json_idx = json_list[idx].split('.')[0]
        assert img_idx == json_idx, "{}, {}".format(img_idx, json_idx)
        os.rename(os.path.join(data_path, 'images', img_idx+'.jpg'),
                  os.path.join(output_path, 'images', str(8642+idx)+'.jpg'))
        os.rename(os.path.join(data_path, 'jsons', json_idx+'.json'),
                  os.path.join(output_path, 'jsons', str(8642+idx)+'.json'))

def move_file(from_dir, to_dir):
    files = glob.glob(from_dir+'/*')
    for f in files:
        os.rename(f, os.path.join(to_dir, f.split('/')[-1])) 

if __name__ == '__main__':
    # img_list, json_list = get_img_and_json_files('organize_output')
    # reorganize(img_list, json_list, 'organize_output', 'output')
    move_file('output/images','/media/bigdata/HungLX/sss/ICD_2015/segment_model/DB/datasets/total_text/images')
    move_file('output/jsons','/media/bigdata/HungLX/sss/ICD_2015/segment_model/DB/datasets/total_text/jsons')