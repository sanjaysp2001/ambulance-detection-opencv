import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

model = tf.keras.models.load_model('model/model_trained.h5')
count = 0
def predict_image(img_path):
    abs_path = './test/crops/'+img_path
    prediction=0
    #calculate the area of the image. If the area is too small we ignore it
    img = plt.imread(abs_path)
    height, width, _ = img.shape
    area = height*width
    # print(area)

    if(area>5000):
        IMG_SIZE = 224
        img_array = cv2.imread(abs_path)
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        x=model.predict(new_array.reshape(-1,IMG_SIZE, IMG_SIZE, 3))
        if x ==1:
            prediction=1
            global count 
            count = count+1
            cv2.imwrite("./test/final/img_{}.jpg".format(count),img_array)
        return prediction
    else:
        return -1




