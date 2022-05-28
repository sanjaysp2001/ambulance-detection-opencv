import cv2
import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

model = tf.keras.models.load_model('model/model.h5')
count = 0
def predict_image(img_path):
    abs_path = './test/crops/'+img_path
    filename = os.path.splitext(img_path)[0]
    imgname = filename.split("_")[0]
    prediction=0
    
    #calculate the area of the image. If the area is too small we ignore it
    img = plt.imread(abs_path)
    height, width, _ = img.shape
    area = height*width

    if(area>5000):
        IMG_SIZE = 224
        img_array = cv2.imread(abs_path)
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        x=model.predict(new_array.reshape(-1,IMG_SIZE, IMG_SIZE, 3))
        res = np.argmax(x)
        if res == 1:
            prediction=1

            #If the image is an ambulance then get the bounding box coordinates and 
            # draw the bounding box on the detected image

            box = open("test/crops/{}.txt".format(filename),'r')
            bbox = box.readline().split(" ")
            x = int(bbox[0])
            y = int(bbox[1])
            w = int(bbox[2])
            h = int(bbox[3])

            final_img = cv2.imread("test/detected/{}.jpg".format(imgname))
            cv2.rectangle(final_img,(x-2, y-2),(x + w + 2, y + h + 2),(255,0,0),2)
            cv2.putText(final_img, "ambulance" , (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,0,0), 2)
            cv2.imwrite("test/final/{}.jpg".format(imgname),final_img)
            
        return prediction
    else:
        return -1




