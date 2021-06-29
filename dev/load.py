import numpy as np
import cv2
import json
import time
t = time.time()
fr = open('output/lines/0.txt','r')
lines = fr.read().splitlines() 
lines = [np.array(json.loads(line)) for line in lines]

img = cv2.imread('warped.jpg')
cv2.drawContours(img,lines,-1, color=255, thickness=2)
cv2.imshow('',img)
print(time.time()-t)
cv2.waitKey(0)

fr.close()