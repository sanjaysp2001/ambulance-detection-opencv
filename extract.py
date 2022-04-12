import cv2 
import os

def extract_frames(video_path):
    vidcap = cv2.VideoCapture(video_path) 
    def getFrame(sec): 
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
        hasFrames,image = vidcap.read() 
        if hasFrames: 
            cv2.imwrite("test/overall/frame_"+str(sec)+".jpg", image)
            print("Frame Saved")
        return hasFrames 
    sec = 0 
    frameRate = 2
    success = getFrame(sec) 
    while success: 
        sec = sec + frameRate 
        sec = round(sec, 2) 
        success = getFrame(sec) 

    

