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