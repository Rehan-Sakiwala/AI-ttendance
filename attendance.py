from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import datetime
import pandas as pd
import os
import csv
from tkinter import filedialog
from fpdf import FPDF

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x650+0+0")
        self.root.title("Attendance Management")

        # Variables
        self.v_date = StringVar()
        self.v_student_id = StringVar()
        self.v_department = StringVar()
        self.v_course = StringVar()
        self.v_year = StringVar()
        self.v_semester = StringVar()
        self.v_from_date = StringVar()
        self.v_to_date = StringVar()
        
        # Set default date to today
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.v_date.set(today)
        self.v_from_date.set(today)
        self.v_to_date.set(today)

        # Header Images
        img = Image.open(r"images\icon_3.jpeg")
        img = img.resize((400, 150))
        self.photoimg = ImageTk.PhotoImage(img)
        l1 = Label(self.root, image=self.photoimg)
        l1.place(x=0, y=0, width=400, height=150)

        img2 = Image.open(r"images\icon_4.jpeg")
        img2 = img2.resize((400, 150))
        self.photoimg2 = ImageTk.PhotoImage(img2)
        l2 = Label(self.root, image=self.photoimg2)
        l2.place(x=400, y=0, width=400, height=150)

        img3 = Image.open(r"images\icon_5.jpeg")
        img3 = img3.resize((400, 150))
        self.photoimg3 = ImageTk.PhotoImage(img3)
        l3 = Label(self.root, image=self.photoimg3)
        l3.place(x=800, y=0, width=400, height=150)

        # Main Frame
        self.bg_frame = Frame(self.root, bg="#fdfdfd")
        self.bg_frame.place(x=0, y=150, width=1200, height=500)

        # Title
        title_lbl = Label(self.bg_frame, text="Attendance Management System", 
                          font=("times new roman", 35, "bold"), bg="#212121", fg="#f4f4f4")
        title_lbl.place(x=0, y=0, width=1200, height=55)

        # Left Frame - Filters
        left_frame = LabelFrame(self.bg_frame, bd=2, relief=GROOVE, text="Attendance Filters", 
                                font=("times new roman", 15, "bold"), fg="#212121", bg="#fdfdfd")
        left_frame.place(x=10, y=60, width=380, height=430)

        # Date Filter
        date_label = Label(left_frame, text="Date:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        date_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        date_entry = ttk.Entry(left_frame, textvariable=self.v_date, width=20, font=("times new roman", 12))
        date_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        # Date Range
        from_date_label = Label(left_frame, text="From Date:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        from_date_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        from_date_entry = ttk.Entry(left_frame, textvariable=self.v_from_date, width=20, font=("times new roman", 12))
        from_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        to_date_label = Label(left_frame, text="To Date:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        to_date_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        to_date_entry = ttk.Entry(left_frame, textvariable=self.v_to_date, width=20, font=("times new roman", 12))
        to_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        
        # Student ID
        student_id_label = Label(left_frame, text="Student PRN:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        student_id_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        student_id_entry = ttk.Entry(left_frame, textvariable=self.v_student_id, width=20, font=("times new roman", 12))
        student_id_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)
        
        # Department
        dep_label = Label(left_frame, text="Department:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        dep_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        dep_combo = ttk.Combobox(left_frame, textvariable=self.v_department, font=("times new roman", 12), 
                                width=17, state="readonly")
        dep_combo['values'] = ("All Departments", "CSE", "Civil", "Mechanical", "Textile")
        dep_combo.current(0)
        dep_combo.grid(row=4, column=1, padx=10, pady=10)
        
        # Course
        course_label = Label(left_frame, text="Course:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        course_label.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        course_combo = ttk.Combobox(left_frame, textvariable=self.v_course, font=("times new roman", 12), 
                                  width=17, state="readonly")
        course_combo['values'] = ("All Courses", "MCA", "BE", "ME", "MSc")
        course_combo.current(0)
        course_combo.grid(row=5, column=1, padx=10, pady=10)
        
        # Year
        year_label = Label(left_frame, text="Year:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        year_label.grid(row=6, column=0, padx=10, pady=10, sticky=W)
        year_combo = ttk.Combobox(left_frame, textvariable=self.v_year, font=("times new roman", 12), 
                                width=17, state="readonly")
        year_combo['values'] = ("All Years", "1", "2", "3", "4")
        year_combo.current(0)
        year_combo.grid(row=6, column=1, padx=10, pady=10)
        
        # Semester
        sem_label = Label(left_frame, text="Semester:", font=("times new roman", 12, "bold"), bg="#fdfdfd")
        sem_label.grid(row=7, column=0, padx=10, pady=10, sticky=W)
        sem_combo = ttk.Combobox(left_frame, textvariable=self.v_semester, font=("times new roman", 12), 
                               width=17, state="readonly")
        sem_combo['values'] = ("All Semesters", "1", "2", "3", "4")
        sem_combo.current(0)
        sem_combo.grid(row=7, column=1, padx=10, pady=10)
        
        # Action Buttons
        btn_frame = Frame(left_frame, bd=0, relief=RIDGE, bg="#fdfdfd")
        btn_frame.place(x=10, y=360, width=360, height=60)
        
        # Filter button
        filter_btn = Button(btn_frame, text="Apply Filters", command=self.fetch_data, 
                           width=15, font=("times new roman", 12, "bold"), bg="#212121", fg="#f4f4f4")
        filter_btn.grid(row=0, column=0, padx=5, pady=10)
        
        # Reset button
        reset_btn = Button(btn_frame, text="Reset", command=self.reset_filters, 
                          width=15, font=("times new roman", 12, "bold"), bg="#212121", fg="#f4f4f4")
        reset_btn.grid(row=0, column=1, padx=5, pady=10)
        
        right_frame = LabelFrame(self.bg_frame, bd=2, relief=GROOVE, text="Attendance Record", 
                                font=("times new roman", 15, "bold"), fg="#212121", bg="#fdfdfd")
        right_frame.place(x=400, y=60, width=780, height=400)
        
        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="#fdfdfd")
        table_frame.place(x=5, y=5, width=765, height=280)
        
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        self.attendance_table = ttk.Treeview(
            table_frame, 
            columns=("id", "student_id", "name", "roll", "department", "course", "year", "semester", "date", "time"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)
        
        self.attendance_table.heading("id", text="ID")
        self.attendance_table.heading("student_id", text="Student Id")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("roll", text="Roll No")
        self.attendance_table.heading("department", text="Department")
        self.attendance_table.heading("course", text="Course")
        self.attendance_table.heading("year", text="Year")
        self.attendance_table.heading("semester", text="Semester")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("time", text="Time")
        
        self.attendance_table["show"] = "headings"
        
        self.attendance_table.column("id", width=50)
        self.attendance_table.column("student_id", width=100)
        self.attendance_table.column("name", width=120)
        self.attendance_table.column("roll", width=80)
        self.attendance_table.column("department", width=100)
        self.attendance_table.column("course", width=80)
        self.attendance_table.column("year", width=60)
        self.attendance_table.column("semester", width=80)
        self.attendance_table.column("date", width=80)
        self.attendance_table.column("time", width=80)
        
        self.attendance_table.pack(fill=BOTH, expand=1)
        
        status_frame = LabelFrame(right_frame, bd=2, relief=GROOVE, text="Status", 
                                font=("times new roman", 15, "bold"), fg="#212121", bg="#fdfdfd")
        status_frame.place(x=5, y=280, width=765, height=50)

        self.status_label = Label(status_frame, text="Total records: 0", font=("times new roman", 12), bg="#fdfdfd")
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        export_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="#fdfdfd")
        export_frame.place(x=5, y=335, width=765, height=40)
        
        export_width = 765 // 3 - 10

        export_excel_btn = Button(export_frame, text="Export to Excel", command=self.export_to_excel,
                                width=15, font=("times new roman", 12, "bold"), bg="#009688", fg="#ffffff")
        export_excel_btn.place(x=5, y=5, width=export_width)

        export_csv_btn = Button(export_frame, text="Export to CSV", command=self.export_to_csv,
                            width=15, font=("times new roman", 12, "bold"), bg="#009688", fg="#ffffff")
        export_csv_btn.place(x=export_width + 15, y=5, width=export_width)

        export_pdf_btn = Button(export_frame, text="Export to PDF", command=self.export_to_pdf,
                            width=15, font=("times new roman", 12, "bold"), bg="#009688", fg="#ffffff")
        export_pdf_btn.place(x=(export_width + 15) * 2, y=5, width=export_width)
        
        self.fetch_data()

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost", 
                username="root", 
                password="sqll00", 
                database="aittendance_db", 
                port=3375
            )
            my_cursor = conn.cursor()
            
            query = """
            SELECT a.id, a.student_id, a.student_name, a.roll, s.dep, s.course, s.year, s.semester, 
                   a.attendance_date, a.attendance_time 
            FROM attendance a
            LEFT JOIN students s ON a.student_id = s.id
            WHERE 1=1
            """
            params = []
            
            # Apply date filter
            if self.v_date.get() != "" and self.v_from_date.get() == self.v_to_date.get() == datetime.datetime.now().strftime("%Y-%m-%d"):
                query += " AND a.attendance_date = %s"
                params.append(self.v_date.get())
            
            # Apply date range filter
            elif self.v_from_date.get() != "" and self.v_to_date.get() != "":
                query += " AND a.attendance_date BETWEEN %s AND %s"
                params.append(self.v_from_date.get())
                params.append(self.v_to_date.get())
            
            # Apply student ID filter
            if self.v_student_id.get() != "":
                query += " AND s.std_prn = %s"
                params.append(self.v_student_id.get())
            
            # Apply department filter
            if self.v_department.get() != "All Departments" and self.v_department.get() != "":
                query += " AND s.dep = %s"
                params.append(self.v_department.get())
            
            # Apply course filter
            if self.v_course.get() != "All Courses" and self.v_course.get() != "":
                query += " AND s.course = %s"
                params.append(self.v_course.get())
            
            # Apply year filter
            if self.v_year.get() != "All Years" and self.v_year.get() != "":
                query += " AND s.year = %s"
                params.append(self.v_year.get())
            
            # Apply semester filter
            if self.v_semester.get() != "All Semesters" and self.v_semester.get() != "":
                query += " AND s.semester = %s"
                params.append(self.v_semester.get())
            
            # Order by date and time
            query += " ORDER BY a.attendance_date DESC, a.attendance_time DESC"
            
            my_cursor.execute(query, params)
            data = my_cursor.fetchall()
            
            # Update the table
            self.attendance_table.delete(*self.attendance_table.get_children())
            
            for row in data:
                self.attendance_table.insert("", END, values=row)
            
            # Update status label
            self.status_label.config(text=f"Total records: {len(data)}")
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching attendance data: {str(e)}", parent=self.root)

    def reset_filters(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.v_date.set(today)
        self.v_from_date.set(today)
        self.v_to_date.set(today)
        self.v_student_id.set("")
        self.v_department.set("All Departments")
        self.v_course.set("All Courses")
        self.v_year.set("All Years")
        self.v_semester.set("All Semesters")
        self.fetch_data()

    def export_to_excel(self):
        try:
            if len(self.attendance_table.get_children()) < 1:
                messagebox.showinfo("No Data", "No data available to export", parent=self.root)
                return
            
            file_path = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save Excel File",
                filetypes=(("Excel Files", "*.xlsx"), ("All Files", "*.*")),
                defaultextension=".xlsx"
            )
            
            if file_path == "":
                return
            
            data = []
            columns = ["ID", "Student PRN", "Name", "Roll No", "Department", "Course", 
                      "Year", "Semester", "Date", "Time"]
            
            # Append column headers
            data.append(columns)
            
            # Get all rows
            for item in self.attendance_table.get_children():
                row_data = []
                for value in self.attendance_table.item(item, "values"):
                    row_data.append(value)
                data.append(row_data)
            
            # Create DataFrame and export to Excel
            df = pd.DataFrame(data[1:], columns=data[0])
            df.to_excel(file_path, index=False)
            
            messagebox.showinfo("Data Exported", f"Data exported to Excel successfully\n{file_path}", parent=self.root)
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting data: {str(e)}", parent=self.root)

    def export_to_csv(self):
        try:
            if len(self.attendance_table.get_children()) < 1:
                messagebox.showinfo("No Data", "No data available to export", parent=self.root)
                return
            
            # Ask user for file name and location
            file_path = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save CSV File",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
                defaultextension=".csv"
            )
            
            if file_path == "":
                return
            
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["ID", "Student PRN", "Name", "Roll No", "Department", "Course", 
                                "Year", "Semester", "Date", "Time"])
                
                # Write data rows
                for item in self.attendance_table.get_children():
                    row_data = []
                    for value in self.attendance_table.item(item, "values"):
                        row_data.append(value)
                    writer.writerow(row_data)
            
            messagebox.showinfo("Data Exported", f"Data exported to CSV successfully\n{file_path}", parent=self.root)
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting data: {str(e)}", parent=self.root)
    
if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()