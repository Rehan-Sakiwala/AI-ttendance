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

    def face_recognize(self):
        if not os.path.exists(self.model_path):
            messagebox.showerror("Error", "Face recognition model not found. Please train the model first.", parent=self.root)
            return
        
        try:
            self.status_label.config(text="Status: Loading recognition model...")
            self.root.update()
            
            with open(self.model_path, "rb") as f:
                data = pickle.load(f)
                known_face_encodings = data["encodings"]
                known_face_ids = data["ids"]
            
            if len(known_face_encodings) == 0:
                messagebox.showerror("Error", "No face data in the model. Please train the model first.", parent=self.root)
                return
                
            self.status_label.config(text=f"Status: Model loaded with {len(known_face_encodings)} faces")
            
            conn = mysql.connector.connect(
                host="localhost", 
                username="root", 
                password="sqll00", 
                database="aittendance_db", 
                port=3375
            )
            cursor = conn.cursor()
            
            self.status_label.config(text="Status: Starting camera...")
            self.root.update()
            
            video_cap = cv2.VideoCapture(0)
            
            if not video_cap.isOpened():
                messagebox.showerror("Error", "Cannot open webcam. Please check your camera connection.", parent=self.root)
                return
            
            self.status_label.config(text="Status: Recognition active (Press Enter to quit)")
            
            process_this_frame = True
            
            while True:
                ret, frame = video_cap.read()
                if not ret:
                    messagebox.showerror("Error", "Failed to capture image from webcam", parent=self.root)
                    break
                
                if process_this_frame:
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                    
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    
                    face_names = []
                    student_ids = []
                    
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.40)
                        name = "Unknown"
                        student_id = None
                        
                        if True in matches:
                            matched_indexes = [i for i, match in enumerate(matches) if match]
                            if matched_indexes:
                                matched_id = known_face_ids[matched_indexes[0]]
                                student_id = matched_id
                                
                                try:
                                    cursor.execute("SELECT std_name, roll FROM students WHERE id=%s", (matched_id,))
                                    student_info = cursor.fetchone()
                                    if student_info:
                                        name = student_info[0]
                                        roll = student_info[1]
                                        self.mark_attendance(matched_id, name, roll)
                                except Exception as e:
                                    print(f"Database error: {str(e)}")
                                    name = f"ID: {matched_id}"
                        
                        face_names.append(name)
                        student_ids.append(student_id)
                
                process_this_frame = not process_this_frame
                
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    
                    if name == "Unknown":
                        color = (0, 0, 255) 
                    else:
                        color = (0, 255, 0) 
                        
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), 
                               cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                
                cv2.imshow("Face Recognition", frame)
                
                #Enter key
                if cv2.waitKey(1) == 13:
                    break
            
            video_cap.release()
            cv2.destroyAllWindows()
            conn.close()
            self.status_label.config(text="Status: Recognition completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Recognition failed: {str(e)}", parent=self.root)
            self.status_label.config(text="Status: Error occurred")

if __name__ == "__main__":
    root = Tk()
    obj = Recognition(root)
    root.mainloop()