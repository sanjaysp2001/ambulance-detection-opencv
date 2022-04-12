import os
import glob
import cv2
from detect import predict_image
from extract import extract_frames
from yolo import yolo_detector

video_path = "./videos/video.avi";
positive_count = 0
if(os.path.exists(video_path)):
    extract_frames(video_path)
    j=0
    for frame in os.listdir('./test/overall/'):
        print(frame)
        j=j+1
        yolo_detector(frame,j)
        for img in os.listdir('./test/crops/'):
            if(predict_image(img) == 1):
                positive_count = positive_count+1
        if(positive_count >=2):
            result="There is an ambulance!"
        else:
            result="There is no ambulance!"

        delete_detected = glob.glob('./test/detected/*.jpg')
        delete_crops = glob.glob('./test/crops/*.jpg')
        for i in delete_detected:
            os.remove(i)
        for i in delete_crops:
            os.remove(i)
    print(result) 
    delete_overall = glob.glob('./test/overall/*.jpg')
    for i in delete_overall:
        os.remove(i)
    
else:
    print("No such video is available")

