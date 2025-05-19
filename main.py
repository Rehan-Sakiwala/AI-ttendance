from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student
import os
from train import Train
from recognition import Recognition
from attendance import Attendance

class Main:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1200x650+0+0")
        self.root.title("AI-ttendance")

        # Img1
        img=Image.open(r"images\icon_3.jpeg")
        img=img.resize((400,150))
        self.photoimg=ImageTk.PhotoImage(img)

        l1 = Label(self.root, image=self.photoimg)
        l1.place(x=0,y=0,width=400,height=150)

        # Img2
        img2=Image.open(r"images\icon_4.jpeg")
        img2=img2.resize((400,150))
        self.photoimg2=ImageTk.PhotoImage(img2)

        l2 = Label(self.root, image=self.photoimg2)
        l2.place(x=400,y=0,width=400,height=150)

        # Img3
        img3=Image.open(r"images\icon_5.jpeg")
        img3=img3.resize((400,150))
        self.photoimg3=ImageTk.PhotoImage(img3)

        l3 = Label(self.root, image=self.photoimg3)
        l3.place(x=800,y=0,width=400,height=150)

        #Background
        self.bg_frame = Frame(self.root, bg="#fdfdfd")
        self.bg_frame.place(x=0, y=150, width=1200, height=500)

        tit_l5 = Label(self.bg_frame,text="AI-ttendance | A smart way of tracking attendance!", font=("times new roman",35,"bold"),bg="#212121",fg="#f4f4f4")
        tit_l5.place(x=0,y=0,width=1200, height=55)

        #Student-Details
        img4=Image.open(r"images\std_icon.png")
        img4=img4.resize((220,220))
        self.photoimg4=ImageTk.PhotoImage(img4)
        b1=Button(self.bg_frame,image=self.photoimg4, command=self.student_details_press, cursor="hand2")
        b1.place(x=80,y=150,width=220,height=220)
        b1_1=Button(self.bg_frame,text="Student Details", command=self.student_details_press, cursor="hand2",font=("times new roman",15,"bold"),bg="#212121",fg="#f4f4f4")
        b1_1.place(x=80,y=350,width=220,height=40)

        #Face-Detection
        img5=Image.open(r"images\face2.png")
        img5=img5.resize((220,220))
        self.photoimg5=ImageTk.PhotoImage(img5)
        b2=Button(self.bg_frame,image=self.photoimg5, cursor="hand2",command=self.face_recognition)
        b2.place(x=350,y=150,width=220,height=220)
        b2_1=Button(self.bg_frame,text="Face Detection",cursor="hand2",font=("times new roman",15,"bold"),bg="#212121",fg="#f4f4f4",command=self.face_recognition)
        b2_1.place(x=350,y=350,width=220,height=40)

        #Attendance
        img6=Image.open(r"images\atnd.png")
        img6=img6.resize((220,220))
        self.photoimg6=ImageTk.PhotoImage(img6)
        b3=Button(self.bg_frame,image=self.photoimg6, cursor="hand2",command=self.attendance_mgmt)
        b3.place(x=640,y=150,width=220,height=220)
        b3_1=Button(self.bg_frame,text="Attendance",cursor="hand2",font=("times new roman",15,"bold"),bg="#212121",fg="#f4f4f4",command=self.attendance_mgmt)
        b3_1.place(x=640,y=350,width=220,height=40)

        #Photos
        img7=Image.open(r"images\photo.png")
        img7=img7.resize((220,220))
        self.photoimg7=ImageTk.PhotoImage(img7)
        b4=Button(self.bg_frame,image=self.photoimg7, cursor="hand2",command=self.open_img)
        b4.place(x=930,y=150,width=220,height=220)
        b4_1=Button(self.bg_frame,text="Photo Directory",cursor="hand2",font=("times new roman",15,"bold"),bg="#212121",fg="#f4f4f4",command=self.open_img)
        b4_1.place(x=930,y=350,width=220,height=40)


        #Train data
        b5 = Button(self.bg_frame, text="Update Model", cursor="hand2", font=("times new roman",15,"bold"),bg="#333333",fg="#eaeaea", command=self.update_model)
        b5.place(x=1025,y=80,width=150,height=40)
        
        #Exit
        img8=Image.open(r"images\cancel.png")
        img8=img8.resize((30,30))
        self.photoimg8=ImageTk.PhotoImage(img8)
        b6=Button(self.root,image=self.photoimg8, cursor="hand2",bg="#fdfdfd", border=0, command=self.close)
        b6.place(x=1180,y=0,width=20,height=20)

        #Developers Copyright
        credit_label = Label(self.bg_frame,text="© All rights reserved. Developed by Rehan Sakiwala & Ansh Khanchandani.",bg="#fdfdfd",font=("",10,"italic"))
        credit_label.place(x=740,y=450)


    def student_details_press(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def update_model(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)

    def face_recognition(self):
        self.new_window=Toplevel(self.root)
        self.app=Recognition(self.new_window)

    def attendance_mgmt(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)

    def open_img(self):
        os.startfile("data")
    
    def close(self):
        self.root.destroy()


if __name__=="__main__":
    root=Tk()
    obj=Main(root)
    root.mainloop()
