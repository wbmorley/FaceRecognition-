import cv2
import sys 
import os 
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# load xml for classifying faces
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 

# title on tkinter GUI
root = tk.Tk()
root.geometry("300x350")
root.minsize(200, 200)
root.title("Face Detect")

# function to ask for photo
def askPic():
    global filePath
    filePath = filedialog.askopenfilename()
    print(filePath)

# function to ask for directory to save known faces
def askKnownDirec():
    global directory
    directory = filedialog.askdirectory()

# submit button function
def submit():
    global name
    name = name_var.get()
    
    
# tkinter GUI for face detect
askFile = tk.Label(root, text="Select a photo to face detect", font=("Arial Black", 10))
askFile.place(relx=0.15, rely=0.1, relheight=0.3, relwidth=0.7)

# insert select photo button
select_button = tk.Button(root, text="Select a photo", command=askPic, font=("Arial Black", 8 ))
select_button.place(relx=0.30, rely=0.5, relheight=0.1, relwidth=0.35)

# insert done button
done_button = tk.Button(root, text="Done", command=root.destroy, font=("Arial Black", 8))
done_button.place(relx=0.30, rely=0.65, relheight=0.1, relwidth=0.35)

# run GUI
root.mainloop()

# read the image
img = cv2.imread(filePath)

# convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 6)

# draw rectangle around face
for(x,y,w,h) in faces:
    img = cv2.rectangle(img, (x, y), (x+w, y+h), (2, 33, 233), 3)
    roi_gray = gray[y:y+h, x:x+w] 
    roi_color = img[y:y+h, x:x+w]

# tkinter window for selecting directory to save known faces
root2 = tk.Tk()
root2.geometry("300x350")
root2.minsize(400,400)
root2.title("Select Known Faces Directory")

prompt = tk.Label(root2, text="Select a directory to store tagged faces:", font=("Arial Black", 10))
prompt.place(relx=0.1, rely=0.25, relheight=0.3, relwidth=0.85)

select_button2 = tk.Button(root2, text="Select a directory", command=askKnownDirec, font=("Arial Black", 8 ))
select_button2.place(relx=0.30, rely=0.5, relheight=0.1, relwidth=0.35)

done_button2 = tk.Button(root2, text="Done", command=root2.destroy, font=("Arial Black", 8))
done_button2.place(relx=0.30, rely=0.65, relheight=0.1, relwidth=0.35)

root2.mainloop()

# change directory to known faces and if not created, create directory for detected faces
os.chdir(directory)
path1 = os.path.join(directory, "detectedFaces")
if not os.path.exists(path1):
    os.mkdir(path1)

# write detected faces image to directory
os.chdir(path1)
cv2.imwrite("detected.jpg", img)


# tkinter window for displaying face detected image
root3 = tk.Tk()
root3.minsize(400, 400)
root3.geometry("600x400")
root3.title("Detected Faces")

canvas = tk.Canvas(root3, width=500, height=300)
canvas.pack()
canvasImg = ImageTk.PhotoImage(Image.open("detected.jpg"))
canvas.create_image(0, 0, anchor="nw", image=canvasImg)

done_button3 = tk.Button(root3, text="Done", command=root3.destroy, font=("Arial Black", 8))
done_button3.place(relx=0.33, rely=0.78, relwidth=0.3, relheigh=0.15)
root3.mainloop()



# tkinter windows to display each detected face and prompt for name entry from the user
for(x,y,w,h) in faces:
    os.chdir(path1)
    root4 = tk.Tk()
    root4.minsize(200, 300)
    root4.geometry("300x300")
    root4.title("Tag Face")

    canvas2 = tk.Canvas(root4)
    canvas2.place(relx=0.4, rely=0.35, relwidth=0.5, relheight=0.5)

    crop_image = img[y:y+h, x:x+w]
    cv2.imwrite("face.jpg", crop_image)
    canvasImg2 = ImageTk.PhotoImage(Image.open("face.jpg"))
    canvas2.create_image(0, 0, anchor="nw", image=canvasImg2)

    name_label = tk.Label(root4, text="Enter a name: ")
    name_label.place(relx=0.05, rely=0.7, relheight=0.1, relwidth=0.35)

    name_var = tk.StringVar()
    name_entry = tk.Entry(root4, textvariable=name_var)
    name_entry.place(relx=0.45, rely=0.73, relheight=0.05, relwidth=0.5)

    submit = tk.Button(root4, text="Submit", command=root4.destroy)
    submit.place(relx=0.35, rely=0.85, relheight=0.05, relwidth=0.35)
    root4.mainloop()

    # write tagged face image to its own directory
    path2 = os.path.join(directory, name_var.get())
    os.mkdir(path2)
    os.chdir(path2)

    cv2.imwrite(name_var.get() + ".jpg", crop_image)

