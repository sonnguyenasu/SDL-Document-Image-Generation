from PIL import Image
imgs = []
for name in ['char','word','line','all']:
    img = Image.open(name+".jpg")
    imgs.append(img)
img, *imgs = [im for im in imgs]
img.save(fp="assets/illustration/see.gif", format='GIF', append_images=imgs,
                 save_all=True, duration=2000, loop=0)