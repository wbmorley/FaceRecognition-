import os 
import cv2
import face_recognition
import tkinter as tk
from tkinter import *
from tkinter import filedialog

# ask user to select directory
def askDirect():
    global filePath
    filePath = filedialog.askdirectory()


known_faces_direc = "known_faces" #directory for known faces
tolerance = 0.65 #tolerance for matching criteria
model = "hog" #hisotgram of oriented gradients 


known_faces = []
known_names = []


# iterate through the known faces directory and grab the face encodings and names to store in arrays declared above
for name in os.listdir(known_faces_direc):
    for filename in os.listdir(f"{known_faces_direc}/{name}"):
        image = face_recognition.load_image_file(f"{known_faces_direc}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)


# tkinter window for photo directory selection
root = tk.Tk()
root.geometry("250x350")
root.minsize(200, 200)
root.title("Face Recognition")

askFile = tk.Label(root, text="Select a directory to find faces")
askFile.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.25)

select_button = tk.Button(root, text="Select a directory", command=askDirect)
select_button.place(relx=0.35, rely=0.7, relwidth=0.5, relheight=0.15)

done_button = tk.Button(root, text="Done", comman=root.quit)
done_button.place(relx=0.35, rely=0.8, relheight=0.15, relwidth=0.5)

root.mainloop()

# iterate through unkown faces images, locate the faces in a picture & grab facial encodings
for filename in os.listdir(filePath):
    image = face_recognition.load_image_file(f"{filePath}/{filename}")
    locations = face_recognition.face_locations(image, model=model)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # for every found face compare the encodings to known faces with matching tolerance incorporated
    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, tolerance)
        match = None
        if True in results:
            match = known_names[results.index(True)]

            #draw rectangle over face
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = [0, 0, 0]

            cv2.rectangle(image, top_left, bottom_right, color, 3)

            #location to put name
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+18)

            #draw rectangle and display name 
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3]+10,face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
   
    #display image
    cv2.imshow(filename, image)
    cv2.waitKey(0)
    cv2.destroyWindow(filename)
