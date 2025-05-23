from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import numpy as np
import cv2
from tkinter import messagebox
import mysql.connector
import face_recognition
import pickle
from datetime import datetime

class Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x650+0+0")
        self.root.title("Face Recognition | Tracking you digitally")
        
        # Create title
        tit_l1 = Label(self.root, text="Face Recognition | Identifying you digitally", 
                      font=("times new roman", 35, "bold"), bg="#212121", fg="#f4f4f4")
        tit_l1.place(x=0, y=0, width=1200, height=55)
        
        # Background image
        img1 = Image.open("images/bg1.jpeg")  # Fixed path format
        img1 = img1.resize((1200, 595))
        self.photoimg1 = ImageTk.PhotoImage(img1)

        l1 = Label(self.root, image=self.photoimg1)
        l1.place(x=0, y=55, width=1200, height=595)

        # Recognition button
        b4_1 = Button(self.root, text="Recognize Face", cursor="hand2", 
                     font=("times new roman", 15, "bold"), bg="aqua", fg="#212121",
                     command=self.face_recognize)
        b4_1.place(x=530, y=550, width=150, height=50)
        
        # Status labels
        self.status_label = Label(self.root, text="Status: Ready", 
                                 font=("times new roman", 14, "bold"), bg="#f4f4f4")
        self.status_label.place(x=400, y=450, width=400, height=30)
        
        self.result_label = Label(self.root, text="", 
                                 font=("times new roman", 14), bg="#f4f4f4")
        self.result_label.place(x=400, y=480, width=400, height=30)
        
        # Check if the model exists
        self.model_path = "face_encodings.pkl"
        if not os.path.exists(self.model_path):
            self.status_label.config(text="Status: Model not found. Please train first.")
        
    def mark_attendance(self, student_id, student_name, roll):
        try:
            conn = mysql.connector.connect(
                host="localhost", 
                username="root", 
                password="sqll00", 
                database="aittendance_db", 
                port=3375
            )
            cursor = conn.cursor()
            
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            
            cursor.execute(
                "SELECT * FROM attendance WHERE student_id=%s AND attendance_date=%s", 
                (student_id, current_date)
            )
            
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO attendance (student_id, student_name, roll, attendance_date, attendance_time) VALUES (%s, %s, %s, %s, %s)",
                    (student_id, student_name, roll, current_date, current_time)
                )
                conn.commit()
                self.result_label.config(text=f"Attendance marked for {student_name}")
            else:
                self.result_label.config(text=f"Attendance already marked for {student_name}")
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark attendance: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Recognition(root)
    root.mainloop()