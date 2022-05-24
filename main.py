import os
import glob
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
            j=j+1
            yolo_detector(frame,j)
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
        play_vid()

    else:
        print("----------------------------\n"+result+"\n----------------------------") 

    delete_detected = glob.glob('./test/detected/*.jpg')
    delete_crops = glob.glob('./test/crops/*.jpg')
    delete_overall = glob.glob('./test/overall/*.jpg')
    for i in delete_detected:
        os.remove(i)
    for i in delete_crops:
        os.remove(i)
    for i in delete_overall:
        os.remove(i)
    
else:
    print("No such video is available")

