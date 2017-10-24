import tkinter as tk
import tkinter as ttk
import random
import cv2
import os
import time
from _thread import start_new_thread
from PIL import Image
from PIL import ImageTk
import numpy as np


def main():
    #creates master list of possible quiz answers from text file
    listMaster = []
    pathToFile = 'FOOD.txt'

    with open(pathToFile) as file:
        for x in range(28): #all text files have 28 words
            words = file.readline()
            end = len(words)-1
            listMaster.append(words[0:end])
    file.close()

    #makes gross list of letters
    # purposefully skips J,Q and Z as those letters are difficult to read
    listA  = ["A - ","B - ","C - ","D - "]
    listE = ["E - ","F - ","G - ","H - "]
    listH = ["H - ","I - ","K - ","L - "]
    listL = ["M - ","N - ","O - ","P - "]
    listR = ["R - ","S - ","T - ","U - "]
    listV = ["V - ","W - ","X - ","Y - "]
    listABC = [listA, listE, listH, listL, listR,listV]

#sets up GUI
    window = tk.Tk()
    window.title("ASL Test")

    labelFrame = ttk.LabelFrame(window, text='What word is being signed?')
    labelFrame.grid(column=0, row=1, padx=20, pady=40)

    # removes 4 possible answers from master list and creates a new list with them
    top = 28 #all text files have 28 words

    #loop or something starts here to create multiple questions
    for y in range(7):
        listAnswers = []
        for x in range (4):
            ans = int(random.random()*top)
            listAnswers.append(listMaster[ans])
            listMaster.remove(listMaster[ans])
            top = top-1
    chosenLocation = int (random.random()*6)
    chosenList = listABC[chosenLocation]

    #puts the questions nicely into grid leading with letters
    ttk.Label(labelFrame, text = chosenList[0] + listAnswers[0]).grid(column=0,row=0)
    ttk.Label(labelFrame, text = chosenList [1] + listAnswers[1]).grid(column=1,row=0)
    ttk.Label(labelFrame, text = chosenList [2] + listAnswers[2]).grid(column=0,row=1)
    ttk.Label(labelFrame, text = chosenList [3] + listAnswers[3]).grid(column=1,row=1)

    for child in labelFrame.winfo_children():
        child.grid_configure(padx=20, pady=10)

    correctLocation = int (random.random()*4) #picks correct answer

    path = os.path.join(os.getcwd(), "Video_Clips");
    path = os.path.join(path, listAnswers[correctLocation] +".mp4")

    videoFrame = ttk.LabelFrame(window)
    videoFrame.grid(column=0, row=0, padx=10, pady=1)

    cap = cv2.VideoCapture(path)
    lmain = tk.Label(window)
    lmain.grid(row=0, column=0)

    def show_frame():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        print(len(frame))
        lmain.after(10, show_frame)

    show_frame()

    correctAns = chosenList[correctLocation][0:1]
    print(correctAns)
    window.mainloop() #runs GUI




if __name__ == '__main__':
    main()

