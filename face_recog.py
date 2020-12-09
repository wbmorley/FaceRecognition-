import os 
import cv2
import face_recognition
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

known_faces_direc = "known_faces" #directory for known faces
unknown_faces_direc = "unknown_faces" #directory of unknown faces
tolerance = 0.9 #tolerance for matching criteria
frame_thickness = 3 #pixels
font_thinckness = 2 
model = "hog" #hisotgram of oriented gradients 

print("Loading known faces")

known_faces = [] #array of known faces
known_names = [] #array of known names



for name in os.listdir(known_faces_direc): #iterate through known faces directory 
    for filename in os.listdir(f"{known_faces_direc}/{name}"): #iterate through images in directory 
        image = face_recognition.load_image_file(f"{known_faces_direc}/{name}/{filename}") #load the image file  
        encoding = face_recognition.face_encodings(image)[0] #encode loaded image 
        known_faces.append(encoding) #appends face encoding to array of known faces
        known_names.append(name) # appends name to array of known names

print("Processing unkown faces")

root = tk.Tk() #start tkinter gui 
root.title("Face Recognition")

def askDirect(): # ask user to select directory 
    global filePath
    filePath = filedialog.askdirectory()
    
    
# tkinter gui to select a directory 
askFile = Label(root, text = "Select a directory to find faces").grid(row=0, column=2)
blank0 = Label(root, text = "            ").grid(row=0,column=1)
blank1 = Label(root, text = "            ").grid(row=1,column=2)
blank2 = Label(root, text = "            ").grid(row=2,column=2)
blank3 = Label(root, text = "            ").grid(row=0,column=3)

#insert select directory button 
select_button = Button(root, text = "Select a directory", command = askDirect)
select_button.grid(row = 3, column = 2)

#insert done button 
done_button = Button(root, text = "Done", command = root.quit)
done_button.grid(row = 4 , column = 2)

#run GUI 
root.mainloop()
print("The file you have selected is: " + filePath)

unknown_faces_direc = filePath

for filename in os.listdir(unknown_faces_direc): #iterate through unkown faces directory
    print(filename)
    image = face_recognition.load_image_file(f"{unknown_faces_direc}/{filename}") #load unknown image
    locations = face_recognition.face_locations(image, model = model) #locate faces 
    encodings = face_recognition.face_encodings(image, locations) #grab face encodings
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #convert image from rgb to bgr 

    for face_encoding, face_location in zip(encodings, locations): #iterate through locations and encodings of unknowkn faces 
        results = face_recognition.compare_faces(known_faces, face_encoding, tolerance) #compare unkown encodings to known faces 
        match = None
        if True in results: #if there is a match print the match found 
            match = known_names[results.index(True)]
            print(f"Match found: {match}")

            #draw rectangle over face
            #find top left and bottom right of face 
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            #color of rectangle
            color = [255,255,255]

            #draw rectangle 
            cv2.rectangle(image, top_left, bottom_right, color, frame_thickness)

            #location to put name
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+18)

            #draw rectangle and display name 
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3]+10,face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), font_thinckness)
   
    #display image
    cv2.imshow(filename, image)
    cv2.waitKey(0)
    cv2.destroyWindow(filename)
