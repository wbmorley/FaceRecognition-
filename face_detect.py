import cv2
import sys 
import os 
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

 #load xml for classifying faces
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 

#title on tkinter GUI 
root = tk.Tk()
root.title("Face Detect")

# function to ask for photo
def askDirect():
    global filePath
    filePath = filedialog.askopenfilename()
    
    
# tkinter GUI for face detect
askFile = Label(root, text = "Select a photo to face detect").grid(row=0, column=2)
blank0 = Label(root, text = "            ").grid(row=0,column=1)
blank1 = Label(root, text = "            ").grid(row=1,column=2)
blank2 = Label(root, text = "            ").grid(row=2,column=2)
blank3 = Label(root, text = "            ").grid(row=0,column=3)

#insert select photo button 
select_button = Button(root, text = "Select a photo", command = askDirect)
select_button.grid(row = 3, column = 2)

#insert done button 
done_button = Button(root, text = "Done", command = root.quit)
done_button.grid(row = 4 , column = 2)

#run GUI 
root.mainloop()

#print file path 
print("The file you have selected is: " + filePath)


out_img = filePath

#read the image
img = cv2.imread(out_img) 
#convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

#detect faces 
faces = face_cascade.detectMultiScale(gray, 1.1, 6)

#draw rectangle around face
for(x,y,w,h) in faces:
    img =cv2.rectangle(img,(x,y),(x+w,y+h),(2,33,233),7) 
    roi_gray = gray[y:y+h, x:x+w] 
    roi_color = img[y:y+h, x:x+w] 

#show image with all faces detected 
cv2.imshow('img', img) 
cv2.waitKey(0)
cv2.destroyAllWindows()

#path for directory of known faces
directory = r'C:\Users\William\3D Objects\Desktop\Python\known_faces' 
directory_python = r'C:\Users\William\3D Objects\Desktop\Python'

#change directory to known faces
os.chdir(directory) 

 # crop the image with a single face and show cropped image 
for(x,y,w,h) in faces:
    crop_image = img[y:y+h, x:x+w] 
    cv2.imshow("Cropped", crop_image) 
    cv2.waitKey(1)

    # ask for user to input the name of person in image 
    name = input("Who is in this photo? ") 

    path = os.path.join(directory, name) #create new directory path name
    os.mkdir(path) # create new directory 
    os.chdir(path) # change path to newly created directory 

    # save cropped image as the name of the person in a unique directory
    cv2.imwrite(name + ".jpg",crop_image) 
    cv2.waitKey(1)


