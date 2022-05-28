import numpy
import numpy as npy 
import matplotlib.pyplot as plt
import os
import cv2
import random

#Loading the yolo model
class_path = os.path.sep.join(['yolo-coco', "coco.names"])
class_names = open(class_path).read().strip().split("\n")

weightsPath = os.path.sep.join(['yolo-coco', "yolov3.weights"])
configPath = os.path.sep.join(['yolo-coco', "yolov3.cfg"])
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

#setting random colors for class labels
npy.random.seed(42)
colours = npy.random.randint(0, 255, size=(len(class_names), 3),dtype="uint8")

def yolo_detector(img_path):

    abs_path = './test/overall/'+img_path
    image = cv2.imread(abs_path)
    (H, W) = image.shape[:2]

    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (224, 224),swapRB=True, crop=False)
    net.setInput(blob)
    out = net.forward(ln)

    box1 = []
    classID1 = []
    confidence1 = []

    for o in out:
        for det in o:
            s1 = det[5:]
            classID = npy.argmax(s1)
            confidence = s1[classID]
            if confidence > 0.7:
                box = det[0:4] * npy.array([W, H, W, H])
                (cX, cY, w1, h1) = box.astype("int")
                x = int(cX - (w1 / 2))
                y = int(cY - (h1 / 2))
                box1.append([x, y, int(w1), int(h1)])
                confidence1.append(float(confidence))
                classID1.append(classID)
    id1 = cv2.dnn.NMSBoxes(box1, confidence1, 0.5, 0.3)
    
    if len(id1) > 0:
        for i in id1.flatten():
            j=0
            (x, y) = (box1[i][0], box1[i][1])
            (w, h) = (box1[i][2], box1[i][3])
            cl = [int(c) for c in colours[classID1[i]]]
            text = "{}".format(class_names[classID1[i]])
            if text == "truck":
                area=w*h
                cv2.rectangle(image, (x-2, y-2), (x + w + 2, y + h + 2), cl, 2)
                cv2.putText(image, text +" , "+str("{:.2f}".format(confidence1[i])) , (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, cl, 2)
                cv2.imwrite("test/detected/d{}.jpg".format(i),image)
                if area>100:
                    im_refined = cv2.imread("test/detected/d{}.jpg".format(i))
                    crop = im_refined[int(y):int(y+h),int(x):int(x+w)]
                    if(crop.size != 0):
                        j=j+1
                        cv2.imwrite("test/crops/d{}_c{}.jpg".format(i,j),crop)
                        f = open("test/crops/d{}_c{}.txt".format(i,j),"w+")
                        f.write(str(x) +" "+ str(y) +" "+ str(w) +" "+str(h))
                        f.close()
                        print("Detecting vehicles...")
                
