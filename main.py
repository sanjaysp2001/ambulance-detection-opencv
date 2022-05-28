import os
import glob
import cv2
import sys
import playsound
from detect import predict_image
from extract import extract_frames
from yolo import yolo_detector
from play_video import play_vid

video_path = sys.argv[1]
sound_path = os.path.join("sound","")
positive_count = 0
alarm = 0
if(os.path.exists(video_path)):
    extract_frames(video_path)
    j=0
    for frame in os.listdir('./test/overall/'):
        if(frame.endswith('.jpg')):
            print(frame)
            yolo_detector(frame)
            for img in os.listdir('./test/crops/'):
                if(img.endswith('.jpg')):
                    if(predict_image(img) == 1):
                        positive_count = positive_count+1
            if(positive_count >=2):
                result="There is an ambulance!"
                alarm = 1
            else:
                result="There is no ambulance!"
    if(alarm == 1):
        print("----------------------------\n"+result+"\n----------------------------") 
        playsound.playsound(sound_path+'\\alarm.wav')

        #The detected images are displayed with the position of ambulances
        final_images = glob.glob('./test/final/*.jpg')
        for img in final_images:
            i = cv2.imread(img)
            cv2.imshow("Detected",i)
            cv2.waitKey(2000)

        #Play the simulation of changing the traffic lights    
        play_vid() 
    else:
        #If no ambulance is detecte, then just a message will be displayed
        print("----------------------------\n"+result+"\n----------------------------") 
        playsound.playsound(sound_path+'\\alarm.wav')


    delete_detected = glob.glob('./test/detected/*.jpg')
    delete_crops = glob.glob('./test/crops/*')
    delete_overall = glob.glob('./test/overall/*.jpg')
    for i in delete_detected:
        os.remove(i)
    for i in delete_crops:
        os.remove(i)
    for i in delete_overall:
        os.remove(i)
    
else:
    print("No such video is available")

