from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import numpy as np
import cv2
from tkinter import messagebox
import face_recognition
import pickle
import mysql.connector
import threading

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x650+0+0")
        self.root.title("Update Model")
        
        tit_l5 = Label(self.root, text="Update your Model by Training with new data", 
                      font=("times new roman", 35, "bold"), bg="#212121", fg="#f4f4f4")
        tit_l5.place(x=0, y=0, width=1200, height=55)

        img1 = Image.open("images/icon_2.jpeg")
        img1 = img1.resize((1200, 595))
        self.photoimg1 = ImageTk.PhotoImage(img1)

        l1 = Label(self.root, image=self.photoimg1)
        l1.place(x=0, y=55, width=1200, height=595)

        self.status_label = Label(self.root, text="Status: Ready to train", 
                                 font=("times new roman", 14, "bold"), bg="#f4f4f4")
        self.status_label.place(x=410, y=360, width=350, height=30)
        
        self.progress_label = Label(self.root, text="", 
                                   font=("times new roman", 12), bg="#f4f4f4")
        self.progress_label.place(x=410, y=390, width=350, height=30)

        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, 
                                       length=350, mode='determinate')
        self.progress.place(x=410, y=420, width=350, height=20)

        self.train_button = Button(self.root, text="Update and Train your model", 
                                  cursor="hand2", font=("times new roman", 15, "bold"), 
                                  bg="#f4f4f4", fg="#212121", command=self.start_training)
        self.train_button.place(x=410, y=300, width=350, height=50)
    
    def start_training(self):
        self.train_button.config(state=DISABLED)
        self.status_label.config(text="Status: Initializing training process...")
        self.progress.config(value=0)
        
        training_thread = threading.Thread(target=self.train_classifier)
        training_thread.daemon = True
        training_thread.start()
    
    def train_classifier(self):
        try:
            data_dir = "data"
            
            if not os.path.exists(data_dir):
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    "Data directory not found. Please capture student images first.", parent=self.root))
                self.root.after(0, lambda: self.train_button.config(state=NORMAL))
                return
                
            if len(os.listdir(data_dir)) == 0:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    "No training data found. Please capture student images first.", parent=self.root))
                self.root.after(0, lambda: self.train_button.config(state=NORMAL))
                return
            
            try:
                conn = mysql.connector.connect(
                    host="localhost", 
                    username="root", 
                    password="sqll00", 
                    database="aittendance_db", 
                    port=3375
                )
                cursor = conn.cursor()
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Database Error", 
                    f"Could not connect to database: {str(e)}", parent=self.root))
                self.root.after(0, lambda: self.train_button.config(state=NORMAL))
                return
            
            self.root.after(0, lambda: self.status_label.config(text="Status: Finding training images..."))
            
            image_paths = []
            for file in os.listdir(data_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_paths.append(os.path.join(data_dir, file))
            
            total_images = len(image_paths)
            
            if total_images == 0:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    "No valid images found in data directory.", parent=self.root))
                self.root.after(0, lambda: self.train_button.config(state=NORMAL))
                conn.close()
                return
            
            self.root.after(0, lambda: self.status_label.config(
                text=f"Status: Processing {total_images} images..."))
            
            known_encodings = []
            known_ids = []
            
            processed = 0
            skipped = 0
            
            for i, image_path in enumerate(image_paths):
                try:
                    student_id = int(os.path.split(image_path)[1].split('.')[1])
                    
                    progress_percent = int((i / total_images) * 100)
                    self.root.after(0, lambda p=progress_percent: self.progress.config(value=p))
                    self.root.after(0, lambda i=i, t=total_images: self.progress_label.config(
                        text=f"Processing image {i+1}/{t}"))
                    
                    image = face_recognition.load_image_file(image_path)
                    
                    face_locations = face_recognition.face_locations(image)
                    
                    if len(face_locations) != 1:
                        skipped += 1
                        continue  
                    
                    encoding = face_recognition.face_encodings(image, face_locations)[0]
                    
                    known_encodings.append(encoding)
                    known_ids.append(student_id)
                    
                    processed += 1
                    
                except Exception as e:
                    skipped += 1
                    print(f"Error processing {image_path}: {str(e)}")
            
            if len(known_encodings) == 0:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    "Could not extract any valid face encodings from images.", parent=self.root))
                self.root.after(0, lambda: self.train_button.config(state=NORMAL))
                conn.close()
                return
            
            self.root.after(0, lambda: self.status_label.config(text="Status: Saving model..."))
            
            data = {
                "encodings": known_encodings,
                "ids": known_ids
            }
            
            with open("face_encodings.pkl", "wb") as f:
                pickle.dump(data, f)
            
            
            with open("classifier.xml", "w") as f:
                f.write("<!-- This file exists for compatibility purposes only -->")
            
            self.root.after(0, lambda: self.status_label.config(text="Status: Updating database..."))
            
            for student_id in set(known_ids):
                try:
                    cursor.execute(
                        "UPDATE students SET photoSample='yes' WHERE id=%s", 
                        (student_id,)
                    )
                except Exception as e:
                    print(f"Error updating student {student_id}: {str(e)}")
            
            conn.commit()
            conn.close()
            
            self.root.after(0, lambda: self.status_label.config(
                text=f"Status: Training completed successfully!"))
            self.root.after(0, lambda: self.progress_label.config(
                text=f"Processed {processed} images, skipped {skipped} images"))
            self.root.after(0, lambda: self.progress.config(value=100))
            
            success_msg = (f"Training completed successfully!\n"
                          f"Processed {processed} images for {len(set(known_ids))} unique students.\n"
                          f"Skipped {skipped} images due to errors or no face detected.")
            
            self.root.after(0, lambda: messagebox.showinfo("Success", success_msg, parent=self.root))
            self.root.after(0, lambda: self.train_button.config(state=NORMAL))
            
        except Exception as e:
            error_msg = f"An error occurred during training:\n{str(e)}"
            self.root.after(0, lambda: self.status_label.config(text="Status: Error occurred"))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg, parent=self.root))
            self.root.after(0, lambda: self.train_button.config(state=NORMAL))


if __name__=="__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()