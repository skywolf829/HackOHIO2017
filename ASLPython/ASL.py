import cv2
import numpy as np
import util as ut
import svm_train as st
import re
model=st.trainSVM(26)
#create and train SVM model each time coz bug in opencv 3.1.0 svm.load() https://github.com/Itseez/opencv/issues/4969
cam=int(raw_input("Enter Camera number: "))
cap=cv2.VideoCapture(cam)
font = cv2.FONT_HERSHEY_SIMPLEX

min_skin = (97, 131, 119)
max_skin = (255, 173, 133)

def nothing(x) :
    pass

text= " "

temp=0
previouslabel=None
previousText=" "
label = None

fgbg = cv2.createBackgroundSubtractorMOG2()

while(cap.isOpened()):
    _,img=cap.read()
    img = cv2.flip(img,1)
    img = cv2.resize(img, (640, 480))
    cv2.rectangle(img,(240,0),(640,400),(255,0,0),3) # bounding box which captures ASL sign to be detected by the system
    img1=img[0:400,240:640]

    img_ycrcb = cv2.cvtColor(img1, cv2.COLOR_BGR2YCR_CB) # get into better color space

    #GaussianBlur
    blur = cv2.GaussianBlur(img_ycrcb,(11,11),0)
    cv2.imshow('yes', blur)

    skin_ycrcb_min = np.array(min_skin)
    skin_ycrcb_max = np.array(max_skin)
    mask = cv2.inRange(blur, skin_ycrcb_min, skin_ycrcb_max)  # detecting the hand in the bounding box using skin detection

    #Background subtraction
    #fgMask = fgbg.apply(img_ycrcb)
    totalMask = mask#cv2.bitwise_or(fgMask, cv2.bitwise_and(mask, cv2.bitwise_not(fgMask)))
    #totalMask = cv2.addWeighted(fgMask,0.3, mask, 1,0)
    #(thresh, totalMask) = cv2.threshold(totalMask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    imc, contours, hierarchy = cv2.findContours(totalMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('totalMask', totalMask)

    cnt=ut.getMaxContour(contours,5000)                          # using contours to capture the skin filtered image of the hand

    if cnt is not None:
        gesture,label=ut.getGestureImg(cnt,img1,totalMask,model)   # passing the trained model for prediction and fetching the result
        if(label is not None):
            print label
            if(temp==0):
                previouslabel=label
            if previouslabel==label :
                previouslabel=label
                temp+=1
            else :
                temp=0
            if(temp==40):
#                if(label=='P'):
#
#                    label=" "
#                text= text + label
#                if(label=='Q'):
#                    words = re.split(" +",text)
#                    words.pop()
#                    text = " ".join(words)
#                    #text=previousText
                print text

        cv2.imshow('PredictedGesture',gesture)                  # showing the best match or prediction
        cv2.putText(img,label,(50,150), font,8,(0,125,155),2)  # displaying the predicted letter on the main screen
        cv2.putText(img,text,(50,450), font,3,(0,0,255),2)
    cv2.imshow('Frame',img)
    k = 0xFF & cv2.waitKey(10)
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
