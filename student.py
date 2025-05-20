from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import mysql.connector
import cv2
import os

class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1200x650+0+0")
        self.root.title("Student Info")

        #------------------Variables
        self.v_dep = StringVar()
        self.v_course = StringVar()
        self.v_year = StringVar()
        self.v_semester = StringVar()
        self.v_std_id = StringVar()
        self.v_std_name = StringVar()
        self.v_div = StringVar()
        self.v_roll = StringVar()
        self.v_gender = StringVar()
        self.v_dob = StringVar()
        self.v_email = StringVar()
        self.v_phone = StringVar()
        self.v_address = StringVar()
        self.v_rank = StringVar()



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

        #Main Frame
        self.bg_frame = Frame(self.root, bg="#fdfdfd")
        self.bg_frame.place(x=0, y=150, width=1200, height=500)

        tit_l5 = Label(self.bg_frame,text="Students Information", font=("times new roman",35,"bold"),bg="#212121",fg="#f4f4f4")
        tit_l5.place(x=0,y=0,width=1200, height=55)

        ###############################Left Frame
        left_frame = LabelFrame(self.bg_frame,bd=2, relief=GROOVE,text="Students Data Form", font=("times new roman",15,"bold"),fg="#212121",bg="#fdfdfd")
        left_frame.place(x=10,y=60,width=600, height=450)

        #Left Upper Frame
        course_lbl = LabelFrame(left_frame,bd=2, relief=GROOVE,text="Department and Course", font=("times new roman",15,"bold"),fg="#212121",bg="#fdfdfd")
        course_lbl.place(x=10,y=0,width=575, height=100)
        
        dep_lbl=Label(course_lbl,font=("times new roman",12),text="Department : ",bg="#fdfdfd")
        dep_lbl.grid(row=0,column=0)

        dep_combo=ttk.Combobox(course_lbl, textvariable=self.v_dep ,font=("times new roman",12),width=17,state="readonly")
        dep_combo['values']=("Select Department","CSE","Civil","Mechanical","Textile")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1)

        #second
        course_l1=Label(course_lbl,font=("times new roman",12),text="Course : ",bg="#fdfdfd")
        course_l1.grid(row=0,column=2)

        course_combo=ttk.Combobox(course_lbl,textvariable=self.v_course ,font=("times new roman",12),width=12,state="readonly")
        course_combo['values']=("Select Course","MCA","BE","ME","MSc")
        course_combo.current(0)
        course_combo.grid(row=0,column=3)


        #year
        year_label=Label(course_lbl,font=("times new roman",12),text="Current Year  : ",bg="#fdfdfd")
        year_label.grid(row=1,column=0,padx=2,pady=8)

        year_combo=ttk.Combobox(course_lbl,textvariable=self.v_year,font=("times new roman",12),width=17,state="readonly")
        year_combo['values']=("Select Year","1","2","3","4")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=8)

        #Semester
        sem_label=Label(course_lbl,font=("times new roman",12),text="Current Semester : ",bg="#fdfdfd")
        sem_label.grid(row=1,column=2,padx=2,pady=8)

        sem_combo=ttk.Combobox(course_lbl,textvariable=self.v_semester,font=("times new roman",12),width=12,state="readonly")
        sem_combo['values']=("Select Sem","1","2","3","4")
        sem_combo.current(0)
        sem_combo.grid(row=1,column=3,padx=2,pady=8)

        ################################# Left bottom
        class_student_frame = LabelFrame(left_frame, bd=2, relief=GROOVE, text="Student Information", font=("times new roman", 15, "bold"), fg="#212121", bg="#fdfdfd")
        class_student_frame.place(x=10, y=100, width=575, height=320)

        # Student PRN
        student_id = Label(class_student_frame, font=("times new roman", 12), text="Student PRN : ", bg="#fdfdfd")
        student_id.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        id_entry = ttk.Entry(class_student_frame, textvariable=self.v_std_id,width=20, font=("times new roman", 12))
        id_entry.grid(row=0, column=1, padx=2, pady=2)

        # Student Name
        student_name = Label(class_student_frame, font=("times new roman", 12), text="Student Name : ", bg="#fdfdfd")
        student_name.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        name_entry = ttk.Entry(class_student_frame, textvariable=self.v_std_name ,width=20, font=("times new roman", 12))
        name_entry.grid(row=0, column=3, padx=2, pady=2)

        # Roll No
        roll_lbl = Label(class_student_frame, font=("times new roman", 12), text="Roll No : ", bg="#fdfdfd")
        roll_lbl.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        roll_entry = ttk.Entry(class_student_frame, textvariable=self.v_roll, width=20, font=("times new roman", 12))
        roll_entry.grid(row=1, column=1, padx=2, pady=2)

        # Division
        div_lbl = Label(class_student_frame, font=("times new roman", 12), text="Division : ", bg="#fdfdfd")
        div_lbl.grid(row=1, column=2, padx=2, pady=2, sticky=W)
        div_entry = ttk.Entry(class_student_frame, textvariable=self.v_div ,width=20, font=("times new roman", 12, "bold"))
        div_entry.grid(row=1, column=3, padx=2, pady=2)

        # Gender
        gender_lbl = Label(class_student_frame, font=("times new roman", 12), text="Gender : ", bg="#fdfdfd")
        gender_lbl.grid(row=2, column=0, padx=2, pady=2, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.v_gender ,font=("times new roman", 12), width=18, state="readonly")
        gender_combo['values'] = ("Select", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=2, pady=2)

        # DOB
        dob_lbl = Label(class_student_frame, font=("times new roman", 12), text="DOB : ", bg="#fdfdfd")
        dob_lbl.grid(row=2, column=2, padx=2, pady=2, sticky=W)
        dob_entry = ttk.Entry(class_student_frame,textvariable=self.v_dob ,width=20, font=("times new roman", 12))
        dob_entry.grid(row=2, column=3, padx=2, pady=2)

        # Email
        email_lbl = Label(class_student_frame, font=("times new roman", 12), text="Email : ", bg="#fdfdfd")
        email_lbl.grid(row=3, column=0, padx=2, pady=2, sticky=W)
        email_entry = ttk.Entry(class_student_frame, textvariable=self.v_email,width=20, font=("times new roman", 12))
        email_entry.grid(row=3, column=1, padx=2, pady=2)

        # Phone
        phone_lbl = Label(class_student_frame, font=("times new roman", 12), text="Phone : ", bg="#fdfdfd")
        phone_lbl.grid(row=3, column=2, padx=2, pady=2, sticky=W)
        phone_entry = ttk.Entry(class_student_frame, textvariable=self.v_phone, width=20, font=("times new roman", 12))
        phone_entry.grid(row=3, column=3, padx=2, pady=2)

        # Address
        address_lbl = Label(class_student_frame, font=("times new roman", 12), text="Address : ", bg="#fdfdfd")
        address_lbl.grid(row=4, column=0, padx=2, pady=2, sticky=W)
        address_entry = ttk.Entry(class_student_frame, textvariable=self.v_address, width=20, font=("times new roman", 12))
        address_entry.grid(row=4, column=1, columnspan=3, padx=2, pady=2, sticky=W)

        # Rank
        rank_lbl = Label(class_student_frame, font=("times new roman", 12), text="Rank : ", bg="#fdfdfd")
        rank_lbl.grid(row=4, column=2, padx=2, pady=2, sticky=W)
        rank_entry = ttk.Entry(class_student_frame,textvariable=self.v_rank ,width=20, font=("times new roman", 12))
        rank_entry.grid(row=4, column=3, padx=2, pady=2)

        #Photo Choice
        self.v_radio1 = StringVar()
        self.v_radio1.set("")
        rad1 = Radiobutton(class_student_frame, variable=self.v_radio1,text="Photo sample now",value="yes",bg="#fdfdfd", font=("times new roman", 12), )
        rad1.grid(row=5,column=0,columnspan=2)

        rad2 = Radiobutton(class_student_frame, variable=self.v_radio1,text="Photo sample later",value="no",bg="#fdfdfd", font=("times new roman", 12))
        rad2.grid(row=6,column=0,columnspan=2)


        #Buttons
        save_button = Button(class_student_frame,bd=2, text="Save", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=10, command=self.add_data)
        save_button.grid(row=7,column=0,padx=10)

        update_button = Button(class_student_frame,bd=2, text="Update", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=10, command=self.update_data)
        update_button.grid(row=7,column=1)

        delete_button = Button(class_student_frame,bd=2, text="Delete", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=10, command=self.delete_data)
        delete_button.grid(row=7,column=2)

        reset_button = Button(class_student_frame,bd=2, text="Reset", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=10, command=self.reset_data)
        reset_button.grid(row=7,column=3)

        take_button_button = Button(class_student_frame,bd=2, text="Take Photo Sample", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=20, command=self.generate_dataset)
        take_button_button.grid(row=8,column=0,columnspan=2,pady=5)

        update_photo_button = Button(class_student_frame,bd=2, text="Update photo Sample", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=20)
        update_photo_button.grid(row=8,column=2,columnspan=2,pady=5)

        
        ######################Right Frame
        right_frame = LabelFrame(self.bg_frame,bd=2, relief=GROOVE,text="Student Details", font=("times new roman",15,"bold"),fg="#212121",bg="#fdfdfd")
        right_frame.place(x=620,y=60,width=568, height=450)

        #===Searching system
        search_frame = LabelFrame(right_frame,bd=2, relief=GROOVE,text="Search System", font=("times new roman",15,"bold"),fg="#212121",bg="#fdfdfd")
        search_frame.place(x=10,y=0,width=550, height=70)

        search_label = Label(search_frame, font=("times new roman", 12,"bold"), text="Search by : ", bg="#fdfdfd")
        search_label.grid(row=0, column=0, padx=2, pady=2, sticky=W)

        search_combo=ttk.Combobox(search_frame,font=("times new roman",12),width=12,state="readonly")
        search_combo['values']=("Select Field","Roll No","Name","PRN","Phone No","Email")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=8)

        search_entry = ttk.Entry(search_frame, width=20, font=("times new roman", 12))
        search_entry.grid(row=0, column=2, padx=2, pady=2)

        search_button = Button(search_frame,bd=2, text="Search", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=7)
        search_button.grid(row=0,column=3,padx=5)

        show_all_button = Button(search_frame,bd=2, text="Show all", relief=RIDGE, bg="#212121", fg="#f4f4f4",font=("times new roman",11,"bold"), width=7)
        show_all_button.grid(row=0,column=4,padx=5)

        ##Records Frame
        record_frame = LabelFrame(right_frame,bd=2, relief=GROOVE,fg="#212121",bg="#fdfdfd")
        record_frame.place(x=10,y=80,width=550, height=320)

        scroll_x=ttk.Scrollbar(record_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(record_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(record_frame,column=('Dep','Course','Year','Sem','Name','Roll','PRN','Gender','Div','DOB',"Email",'Phone','Address','Photo'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        self.student_table.heading("Dep", text="Department")
        self.student_table.heading("Course", text="Course")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("Sem", text="Semester")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Roll", text="Roll No")
        self.student_table.heading("PRN", text="PRN No")
        self.student_table.heading("Gender", text="Gender")
        self.student_table.heading("Div", text="Division")
        self.student_table.heading("DOB", text="Date of Birth")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("Phone", text="Phone No")
        self.student_table.heading("Address", text="Address")
        self.student_table.heading("Photo", text="Photo Sample")
        self.student_table['show']="headings"

        self.student_table.column("Dep",width=100)
        self.student_table.column("Course", width=100)
        self.student_table.column("Year", width=100)
        self.student_table.column("Sem", width=100)
        self.student_table.column("Name", width=100)
        self.student_table.column("Roll", width=100)
        self.student_table.column("PRN", width=100)
        self.student_table.column("Gender", width=100)
        self.student_table.column("Div", width=100)
        self.student_table.column("DOB", width=100)
        self.student_table.column("Email", width=100)
        self.student_table.column("Phone", width=100)
        self.student_table.column("Address", width=100)
        self.student_table.column("Photo", width=100)

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

    def add_data(self):
        if (
        self.v_dep.get() == "Select Department" or
        self.v_course.get() == "Select Course" or
        self.v_year.get() == "Select Year" or
        self.v_semester.get() == "Select Sem" or
        self.v_std_id.get() == "" or
        self.v_std_name.get() == "" or
        self.v_roll.get() == "" or
        self.v_div.get() == "" or
        self.v_gender.get() == "Select" or
        self.v_dob.get() == ""
        ):
            messagebox.showerror("Error","All Fields are Required!!",parent=self.root)
            return

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.v_email.get()):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.",parent=self.root)
            return
        
        if not self.v_phone.get().isdigit() or len(self.v_phone.get()) != 10:
            messagebox.showerror("Invalid Phone", "Phone number must be exactly 10 digits.",parent=self.root)
            return
        
        try:
            conn = mysql.connector.connect(host="localhost",username="root",password="sqll00",database="aittendance_db",port=3375)
            my_cursor = conn.cursor()
            my_cursor.execute("INSERT INTO students (dep, course, year, semester, std_prn, std_name, `div`, roll, gender, dob, email, phone, address, `rank`, photoSample) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (self.v_dep.get(), 
                    self.v_course.get(), 
                    self.v_year.get(), 
                    self.v_semester.get(), 
                    self.v_std_id.get(), 
                    self.v_std_name.get(), 
                    self.v_div.get(), 
                    self.v_roll.get(), 
                    self.v_gender.get(), 
                    self.v_dob.get(), 
                    self.v_email.get(), 
                    self.v_phone.get(), 
                    self.v_address.get(), 
                    self.v_rank.get(),
                    self.v_radio1.get()
                    ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Students details has been added successfully!!",parent=self.root)
        except Exception as e:
           messagebox.showerror("Error",f"Cannot add data due to :{str(e)}",parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",username="root",password="sqll00",database="aittendance_db",port=3375)
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT dep, course, year, semester, std_name, roll, std_prn, gender, `div`, dob, email, phone, address, photoSample FROM students")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content['values']

        if data:
            self.v_dep.set(data[0])           # Department
            self.v_course.set(data[1])        # Course
            self.v_year.set(data[2])          # Year
            self.v_semester.set(data[3])      # Semester
            self.v_std_name.set(data[4])      # Name
            self.v_roll.set(data[5])          # Roll No
            self.v_std_id.set(data[6])        # PRN No
            self.v_gender.set(data[7])        # Gender
            self.v_div.set(data[8])           # Division
            self.v_dob.set(data[9])           # DOB
            self.v_email.set(data[10])        # Email
            self.v_phone.set(data[11])        # Phone
            self.v_address.set(data[12])      # Address
            self.v_radio1.set(data[13])       #Photo taken or not
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="sqll00", database="aittendance_db", port=3375)
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT `rank` FROM students WHERE std_prn = %s", (self.v_std_id.get(),))
            rank_data = my_cursor.fetchone()
            if rank_data:
                self.v_rank.set(rank_data[0])
            else:
                self.v_rank.set("")
            conn.close()
        except Exception as e:
            print(f"Error fetching rank: {str(e)}")
            self.v_rank.set("")

    def update_data(self):
        if (
        self.v_dep.get() == "Select Department" or
        self.v_course.get() == "Select Course" or
        self.v_year.get() == "Select Year" or
        self.v_semester.get() == "Select Sem" or
        self.v_std_id.get() == "" or
        self.v_std_name.get() == "" or
        self.v_roll.get() == "" or
        self.v_div.get() == "" or
        self.v_gender.get() == "Select" or
        self.v_dob.get() == ""
        ):
            messagebox.showerror("Error","All Fields are Required!!",parent=self.root)
            return
        try:
            update=messagebox.askyesno("Confirmation","Do you want to make changes?",parent=self.root)
            if update>0:
                conn = mysql.connector.connect(host="localhost",username="root",password="sqll00",database="aittendance_db",port=3375)
                my_cursor = conn.cursor()
                my_cursor.execute("UPDATE students SET dep=%s, course=%s, year=%s, semester=%s, std_name=%s, `div`=%s, roll=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, `rank`=%s, photoSample=%s WHERE std_prn=%s", 
                    (self.v_dep.get(), 
                    self.v_course.get(), 
                    self.v_year.get(), 
                    self.v_semester.get(), 
                    self.v_std_name.get(), 
                    self.v_div.get(), 
                    self.v_roll.get(), 
                    self.v_gender.get(), 
                    self.v_dob.get(), 
                    self.v_email.get(), 
                    self.v_phone.get(), 
                    self.v_address.get(), 
                    self.v_rank.get(),
                    self.v_radio1.get(),
                    self.v_std_id.get()
                    ))
            else:
                if not update:
                    return
            messagebox.showinfo("Success","Details updated successfully!",parent=self.root)
            conn.commit()
            self.fetch_data()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error",f"Erro due to : {str(e)}",parent=self.root)
    
    def delete_data(self):
        if self.v_std_id.get=="":
            messagebox.showerror("Error","Student PRN is required!",parent=self.root)
            return
        try:
            delete=messagebox.askyesno("Confirmation","Do you want to delete student record?",parent=self.root)
            if delete>0:
                conn = mysql.connector.connect(host="localhost",username="root",password="sqll00",database="aittendance_db",port=3375)
                my_cursor = conn.cursor()
                sql="delete from students where std_prn = %s"
                my_cursor.execute(sql,(self.v_std_id.get(),))
            else:
                if not delete:
                    return
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Student deleted successfully!",parent=self.root)
        except Exception as e:
            messagebox.showerror("Error",f"Erro due to : {str(e)}",parent=self.root)

    def reset_data(self):
        self.v_dep.set("Select Department")
        self.v_course.set("Select Course")
        self.v_year.set("Select Year")
        self.v_semester.set("Select Sem")
        self.v_std_id.set("")
        self.v_std_name.set("")
        self.v_div.set("")
        self.v_roll.set("")
        self.v_gender.set("Select")
        self.v_dob.set("")
        self.v_email.set("")
        self.v_phone.set("")
        self.v_address.set("")
        self.v_rank.set("")
        self.v_radio1.set("")

#Generating dataset and photo sample collection
    def generate_dataset(self):
        if (
        self.v_dep.get() == "Select Department" or
        self.v_course.get() == "Select Course" or
        self.v_year.get() == "Select Year" or
        self.v_semester.get() == "Select Sem" or
        self.v_std_id.get() == "" or
        self.v_std_name.get() == "" or
        self.v_roll.get() == "" or
        self.v_div.get() == "" or
        self.v_gender.get() == "Select" or
        self.v_dob.get() == ""
        ):
            messagebox.showerror("Error","All Fields are Required!!",parent=self.root)
            return
        try:
            conn = mysql.connector.connect(host="localhost",username="root",password="sqll00",database="aittendance_db",port=3375)
            my_cursor = conn.cursor()
            
            # Check if the student exists and get their database ID
            my_cursor.execute("SELECT id FROM students WHERE std_prn = %s", (self.v_std_id.get(),))
            student_record = my_cursor.fetchone()
            
            if student_record:
                # Student exists, use the existing ID
                id = student_record[0]
            else:
                # Student doesn't exist in database, get the next ID
                my_cursor.execute("SELECT MAX(id) FROM students")
                result = my_cursor.fetchone()
                if result[0] is None:
                    id = 1
                else:
                    id = result[0] + 1
            
            # Update student record and set photoSample to 'Yes'
            my_cursor.execute("UPDATE students SET dep=%s, course=%s, year=%s, semester=%s, std_name=%s, `div`=%s, roll=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, `rank`=%s, photoSample='Yes' WHERE std_prn=%s", 
                    (self.v_dep.get(), 
                    self.v_course.get(), 
                    self.v_year.get(), 
                    self.v_semester.get(), 
                    self.v_std_name.get(), 
                    self.v_div.get(), 
                    self.v_roll.get(), 
                    self.v_gender.get(), 
                    self.v_dob.get(), 
                    self.v_email.get(), 
                    self.v_phone.get(), 
                    self.v_address.get(), 
                    self.v_rank.get(),
                    self.v_std_id.get()
                    ))
            
            conn.commit()
            self.fetch_data()
            conn.close()

            if not os.path.exists("data"):
                os.makedirs("data")

            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                
                if len(faces) == 0:
                    return None
                    
                for (x, y, w, h) in faces:
                    face_cropped = img[y:y+h, x:x+w]
                    return face_cropped
            
            cap = cv2.VideoCapture(0)
            img_id = 0
            
            while True:
                ret, my_frame = cap.read()
                if not ret:
                    messagebox.showerror("Camera Error", "Could not access the camera.", parent=self.root)
                    break
                    
                cropped_face = face_cropped(my_frame)
                if cropped_face is not None:
                    img_id += 1
                    face = cv2.resize(cropped_face, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"data/user.{id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Face Capture", face)

                if cv2.waitKey(1) == 13 or int(img_id) == 100:  # 13 code Enter key
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            self.v_radio1.set("Yes")
            
            messagebox.showinfo("Result", f"Dataset generation completed successfully! Captured {img_id} images.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Cannot proceed further: {str(e)}", parent=self.root)
            if (
            self.v_dep.get() == "Select Department" or
            self.v_course.get() == "Select Course" or
            self.v_year.get() == "Select Year" or
            self.v_semester.get() == "Select Sem" or
            self.v_std_id.get() == "" or
            self.v_std_name.get() == "" or
            self.v_roll.get() == "" or
            self.v_div.get() == "" or
            self.v_gender.get() == "Select" or
            self.v_dob.get() == ""
            ):
                messagebox.showerror("Error","All Fields are Required!!",parent=self.root)
                return
            try:
                conn = mysql.connector.connect(host="localhost",username="root",password="sqll00",database="aittendance_db",port=3375)
                my_cursor = conn.cursor()
                my_cursor.execute("select * from students")
                myResult = my_cursor.fetchall()
                id=0
                for x in myResult:
                    id+=1
                
                my_cursor.execute("UPDATE students SET dep=%s, course=%s, year=%s, semester=%s, std_name=%s, `div`=%s, roll=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, `rank`=%s, photoSample=%s WHERE std_prn=%s", 
                        (self.v_dep.get(), 
                        self.v_course.get(), 
                        self.v_year.get(), 
                        self.v_semester.get(), 
                        self.v_std_name.get(), 
                        self.v_div.get(), 
                        self.v_roll.get(), 
                        self.v_gender.get(), 
                        self.v_dob.get(), 
                        self.v_email.get(), 
                        self.v_phone.get(), 
                        self.v_address.get(), 
                        self.v_rank.get(),
                        self.v_radio1.get(),
                        self.v_std_id.get()==id+1
                        ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                
                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)  #1.3 - scaling factor, 5 - Minimum neighbour

                    for(x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped
                
                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    ret,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_cropped(my_frame),(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path = "data/user."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Face ",face)

                    if cv2.waitKey(1)==13 or int(img_id) == 100:
                        break
                
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Generating dataset completed successfully!")


            except Exception as e:
                messagebox.showerror("Error",f"Cannot proceed further as {str(e)}")
            

if __name__=="__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()
